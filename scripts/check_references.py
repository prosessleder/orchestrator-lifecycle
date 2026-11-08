#!/usr/bin/env python3
"""Audit the manuscript bibliography with the pinned RefChecker, without an LLM."""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REFCHECKER_VERSION = '3.1.6'


def bibliography_entries(source):
    """Read the final References section; never scan body prose as citations."""
    sections = re.split(r'^# References \{\.unnumbered\}\s*$', source, flags=re.M)
    if len(sections) != 2 or not sections[1].strip():
        raise ValueError('Expected one nonempty final References section')
    if re.search(r'^# ', sections[1], re.M):
        raise ValueError('References must be the final manuscript section')
    return [re.sub(r'\s+', ' ', entry.strip())
            for entry in re.split(r'\n\s*\n', sections[1].strip())]


def bibtex_entry(entry, number):
    """Adapt this paper's author-year/italic-title prose to structured BibTeX.

    This deliberately supports the manuscript's formatting conventions, rather
    than guessing at arbitrary citation styles. Unsupported entries stop the build.
    The complete original entry is retained in the audit's input index.
    """
    dated = re.match(r'^(.+?) \((\d{4})(?:,[^)]*)?\)\. (.+)$', entry)
    if dated:
        authors, year, rest = dated.groups()
    else:
        undated = re.match(r'^(.+?)\. (\*.+)$', entry)
        if not undated:
            raise ValueError(f'Unsupported author/date format in reference {number}: {entry}')
        authors, rest = undated.groups()
        year = None  # An access date is not a publication year.

    if rest.startswith('*'):
        title_match = re.match(r'^\*([^*]+)\*', rest)
    else:
        # Nonitalic titles end before a venue, chapter container, preprint
        # designation, report publisher, or dated web-publication statement.
        title_match = re.match(
            r'^(.+?[.?])\s+(?=\*|In |Preprint[,.]|Hugging Face,|'
            r'Anthropic Research,|SaaStr\.|\d{1,2} [A-Z][a-z]+\.)', rest)
    if not title_match:
        raise ValueError(f'Unsupported title boundary in reference {number}: {entry}')
    title = title_match[1].removesuffix('.')
    corporate_author = None
    if re.search(r', [A-Z]\.', authors):
        # Preserve surname-first initials and multiword surnames for BibTeX.
        authors = authors.replace(', and ', ' and ')
        authors = re.sub(r'(?<=\.), (?=[^,]+, [A-Z]\.)', ' and ', authors)
    else:
        corporate_author = authors
        authors = '{' + authors + '}'  # Corporate author, including names with spaces.

    urls = re.findall(r'https?://[^\s<>)]*', entry)
    if not urls:
        raise ValueError(f'Reference {number} has no source URL')
    fields = {'author': authors, 'title': title, 'url': urls[0]}
    if year:
        fields['year'] = year
    doi = next((url.removeprefix('https://doi.org/') for url in urls
                if url.startswith('https://doi.org/')), None)
    if doi:
        fields['doi'] = doi
    remainder = rest[title_match.end():].lstrip('., ')
    venue = re.search(r'\*([^*]+)\*', remainder)
    if venue:
        fields['journal'] = venue[1]
        pagination = re.match(r', (\d+)(?:\((\d+)\))?, ([\d-]+)', remainder[venue.end():])
        if pagination:
            fields['volume'] = pagination[1]
            if pagination[2]:
                fields['number'] = pagination[2]
            fields['pages'] = pagination[3]

    def escape(value):
        return value.replace('&', r'\&')

    bib = '@misc{ref' + str(number).zfill(3) + ',\n'
    bib += ''.join('  ' + key + ' = {' + escape(value) + '},\n'
                   for key, value in fields.items()) + '}\n'
    primary_url = urls[0]
    web_page = (not doi and not re.search(r'arxiv\.org/(abs|pdf)/', primary_url)
                and not urlparse(primary_url).path.lower().endswith('.pdf'))
    return bib, {'number': number, 'original': entry, 'corporate_author': corporate_author,
                 'web_page': web_page, **fields}


def validate_report(report, expected_count):
    summary = report['summary']
    if (summary['total_papers_processed'] != 1
            or summary['total_references_processed'] != expected_count):
        raise ValueError('RefChecker did not process every manuscript reference')
    return summary


def run_reference_check(manuscript, report_dir, strict=False):
    try:
        installed = version('academic-refchecker')
    except PackageNotFoundError as error:
        raise RuntimeError('Install requirements-refchecker.txt with this Python interpreter') from error
    if installed != REFCHECKER_VERSION:
        raise RuntimeError(f'Expected academic-refchecker=={REFCHECKER_VERSION}; found {installed}')
    from refchecker.core.refchecker import ArxivReferenceChecker
    from refchecker.utils.bibtex_parser import parse_bibtex_references
    from reference_sources import CitedWebPageChecker, DOIReferenceChecker

    manuscript = Path(manuscript).resolve()
    report_dir = Path(report_dir).resolve()
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / 'refchecker.json'
    run_path = report_dir / 'run.json'
    report_path.unlink(missing_ok=True)  # A failed run must not leave an old successful report.
    run_path.unlink(missing_ok=True)
    source_bytes = manuscript.read_bytes()
    entries = bibliography_entries(source_bytes.decode('utf-8'))
    converted = [bibtex_entry(entry, i) for i, entry in enumerate(entries, 1)]
    bibliography = '\n'.join(item[0] for item in converted)
    parsed = parse_bibtex_references(bibliography)
    if len(parsed) != len(entries):
        raise ValueError('RefChecker could not parse every generated BibTeX entry')
    # RefChecker 3.1.6 truncates some corporate authors containing "and".
    # Keep the complete literal author from the manuscript in the engine input.
    for reference, (_, original) in zip(parsed, converted):
        if original['corporate_author']:
            reference['authors'] = [original['corporate_author']]
        reference['_web_page'] = original['web_page']
    bib_path = report_dir / 'references.bib'
    bib_path.write_text(bibliography, encoding='utf-8')
    (report_dir / 'inputs.json').write_text(json.dumps({
        'manuscript_sha256': hashlib.sha256(source_bytes).hexdigest(),
        'references': [item[1] for item in converted],
        'parsed_references': parsed,
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    provenance = {
        'started_at_utc': datetime.now(timezone.utc).isoformat(),
        'refchecker_version': installed,
        'manuscript_sha256': hashlib.sha256(source_bytes).hexdigest(),
        'expected_references': len(entries),
        'llm_enabled': False,
        'status': 'running',
    }
    def save_run():
        run_path.write_text(json.dumps(provenance, indent=2) + '\n', encoding='utf-8')

    save_run()
    try:
        class ManuscriptReferenceChecker(ArxivReferenceChecker):
            def extract_bibliography(self, paper, debug_mode=False, input_spec=None):
                self.last_bibliography_extraction_method = 'bib'
                return copy.deepcopy(parsed)

            def verify_reference(self, source_paper, reference):
                # Avoid upstream extraction fixups altering known source fields
                # (for example W3C becoming WC) before an identity-anchored check.
                if reference.get('doi'):
                    data, errors, url = DOIReferenceChecker().verify_reference(reference)
                    return errors or None, url, data
                if reference.get('_web_page'):
                    data, errors, url = CitedWebPageChecker(reference).verify_reference(reference)
                    return errors or None, url, data
                return super().verify_reference(source_paper, copy.deepcopy(reference))

        # Explicitly disable LLM extraction and deep hallucination checks even
        # when a developer has configured providers in their personal settings.
        checker = ManuscriptReferenceChecker(
            llm_config={'disabled': True}, max_workers=3,
            report_file=str(report_path), report_format='json')
        # The upstream constructor can discover a web-search LLM independently
        # of its disabled extraction flag. Disable that fallback explicitly too.
        checker.report_builder.web_searcher = None
        checker.report_builder.llm_verifier = None
        if checker.fatal_error:
            raise RuntimeError('RefChecker initialization failed')
        checker.run(local_pdf_path=str(bib_path))
        if checker.fatal_error:
            raise RuntimeError('RefChecker could not finish the audit')
        summary = validate_report(json.loads(report_path.read_text()), len(entries))
        provenance.update(status='completed', summary=summary)
        issues = sum(summary[key] for key in (
            'total_errors_found', 'total_warnings_found', 'total_unverified_refs'))
        print(f'RefChecker processed all {len(entries)} references; report: {report_path}')
        print('Findings require source review; unverified references are not proof of fabrication.')
        if strict and issues:
            raise RuntimeError('Strict reference check failed: errors, warnings, or unverified references')
    except Exception as error:
        provenance.update(status='failed', error=str(error))
        raise
    finally:
        provenance['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
        save_run()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manuscript', type=Path, default=ROOT / 'paper.md')
    parser.add_argument('--report-dir', type=Path, default=ROOT / 'tmp/refchecker')
    parser.add_argument('--strict', action='store_true', help='Also fail on citation findings')
    args = parser.parse_args()
    run_reference_check(args.manuscript, args.report_dir, args.strict)


if __name__ == '__main__':
    main()

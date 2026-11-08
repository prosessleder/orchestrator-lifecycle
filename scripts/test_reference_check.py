#!/usr/bin/env python3
"""Regression checks for citation extraction and incomplete-audit rejection."""
import sys
import contextlib
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
from check_references import ROOT, bibliography_entries, bibtex_entry, run_reference_check, validate_report


class ReferenceCheckTests(unittest.TestCase):
    def test_doi_identity_preserves_publication_year_and_all_book_containers(self):
        from reference_sources import DOIReferenceChecker

        class PublisherChecker(DOIReferenceChecker):
            def get_work_by_doi(self, doi):
                return {'DOI': doi, 'title': 'A survey',
                        'author': [{'given': 'Jane', 'family': 'Doe'}],
                        'published-print': {'date-parts': [[2017]]},
                        'container-title': 'Lecture Notes in Computer Science',
                        '_container_titles': ['Lecture Notes in Computer Science', 'Reasoning Web']}

        ref = {'doi': '10.1000/example', 'title': 'A survey', 'authors': ['Doe, J.'],
               'year': 2017, 'journal': 'Reasoning Web'}
        _, errors, _ = PublisherChecker().verify_reference(ref)
        self.assertEqual(errors, [])
        _, errors, _ = PublisherChecker().verify_reference({**ref, 'title': 'A completely unrelated work'})
        self.assertIn('title', [error.get('error_type') for error in errors])
        _, errors, _ = PublisherChecker().verify_reference({**ref, 'authors': ['Smith, A.']})
        self.assertIn('author', [error.get('error_type') for error in errors])
        _, errors, _ = PublisherChecker().verify_reference({**ref, 'year': 2000})
        self.assertIn('year', [error.get('warning_type') for error in errors])

    def test_unavailable_doi_is_not_replaced_by_title_match(self):
        from reference_sources import DOIReferenceChecker
        with patch.object(DOIReferenceChecker, 'get_work_by_doi', return_value=None):
            data, errors, _ = DOIReferenceChecker().verify_reference({
                'doi': '10.1000/example', 'title': 'Provenance', 'authors': ['Example']})
        self.assertIsNone(data)
        self.assertEqual(errors[0]['error_type'], 'unverified')

    def test_web_specification_uses_cited_page_and_preserves_access_warning(self):
        from reference_sources import CitedWebPageChecker
        ref = {'url': 'https://slsa.dev/spec/v1.0/provenance',
               'title': 'Provenance', 'authors': ['SLSA']}
        response = SimpleNamespace(status_code=200, url=ref['url'],
                                   headers={'content-type': 'text/html'},
                                   content=b'<html><title>SLSA - Provenance</title><h1>Provenance</h1></html>')
        with patch.object(CitedWebPageChecker, '_respectful_request', return_value=response):
            data, errors, url = CitedWebPageChecker(ref).verify_reference(ref)
        self.assertEqual(url, ref['url'])
        self.assertEqual(data['_matched_database'], 'Web Page')
        self.assertEqual(errors, [])
        response.status_code = 403
        with patch.object(CitedWebPageChecker, '_respectful_request', return_value=response):
            _, errors, _ = CitedWebPageChecker(ref).verify_reference(ref)
        self.assertTrue(errors)

    def test_primary_page_bibtex_authors_are_checked_against_matching_title(self):
        from bs4 import BeautifulSoup
        from reference_sources import CitedWebPageChecker
        ref = {'url': 'https://www.anthropic.com/research/example',
               'title': 'Agentic Misalignment: How LLMs Could Be Insider Threats', 'authors': ['Doe, J.', 'Smith, A.']}
        soup = BeautifulSoup('<pre>@article{study, title={Agentic Misalignment: How LLMs Could be an Insider Threat}, '
                             'author={Jane Doe and Alex Smith}, year={2025}}</pre>', 'html.parser')
        checker = CitedWebPageChecker(ref)
        info = checker._extract_site_info(soup, ref['url'])
        self.assertTrue(checker._check_author_match('', info, ref['url']))
        checker.reference = {**ref, 'authors': ['Wrong, N.']}
        self.assertFalse(checker._check_author_match('', info, ref['url']))
        checker.reference = {**ref, 'title': 'A completely different publication'}
        self.assertNotIn('citation_authors', checker._extract_site_info(soup, ref['url']))

    def test_missing_individual_authorship_is_information_not_an_org_mismatch(self):
        from reference_sources import CitedWebPageChecker
        ref = {'url': 'https://example.org/', 'title': 'Example book', 'authors': ["O'Brien, T."]}
        response = SimpleNamespace(status_code=200, url=ref['url'],
                                   headers={'content-type': 'text/html'},
                                   content=b'<html><title>Example book</title></html>')
        with patch.object(CitedWebPageChecker, '_respectful_request', return_value=response):
            data, errors, _ = CitedWebPageChecker(ref).verify_reference(ref)
        self.assertEqual(data['authors'], [])
        self.assertEqual([error.get('info_type') for error in errors], ['author'])

    def test_specific_heading_can_identify_a_source_with_a_generic_html_title(self):
        from bs4 import BeautifulSoup
        from reference_sources import CitedWebPageChecker
        ref = {'url': 'https://opengitops.dev/', 'title': 'GitOps Principles', 'authors': ['OpenGitOps']}
        soup = BeautifulSoup('<title>Home | OpenGitOps</title><h2>OpenGitOps Principles</h2>', 'html.parser')
        self.assertEqual(CitedWebPageChecker(ref)._extract_page_title(soup), 'OpenGitOps Principles')

    def test_author_metadata_on_a_matching_page_precedes_domain_guess(self):
        from bs4 import BeautifulSoup
        from reference_sources import CitedWebPageChecker
        ref = {'url': 'https://nickbostrom.com/papers/example/',
               'title': 'Ethical Issues', 'authors': ['Bostrom, N.']}
        soup = BeautifulSoup('<title>Ethical Issues</title><meta name="author" '
                             'content="Nick Bostrom">', 'html.parser')
        checker = CitedWebPageChecker(ref)
        info = checker._extract_site_info(soup, ref['url'])
        self.assertTrue(checker._check_author_match('', info, ref['url']))
        checker.reference = {**ref, 'authors': ['Wrong, X.']}
        self.assertFalse(checker._check_author_match('', info, ref['url']))

    def test_manuscript_round_trip(self):
        from refchecker.utils.bibtex_parser import parse_bibtex_references
        entries = bibliography_entries((ROOT / 'paper.md').read_text())
        bibliography = '\n'.join(bibtex_entry(entry, i)[0]
                                 for i, entry in enumerate(entries, 1))
        parsed = parse_bibtex_references(bibliography)
        self.assertEqual(len(parsed), len(entries))
        self.assertEqual(len({ref['bibtex_key'] for ref in parsed}), len(entries))
        for reference, original in zip(parsed, entries):
            self.assertIn(reference['title'], original)
            self.assertTrue(reference['url'])
            self.assertNotEqual(reference['authors'], ['Unknown Author'])

    def test_access_date_is_not_publication_year(self):
        bib, data = bibtex_entry('Example Foundation. *Example documentation*. '
                                '[Docs](https://example.org/docs/). Accessed 9 October 2026.', 1)
        self.assertNotIn('year', data)
        self.assertNotIn('year =', bib)
        self.assertEqual(data['corporate_author'], 'Example Foundation')

    def test_multiple_initials_and_multiword_surname(self):
        _, data = bibtex_entry('Kamburjan, E., Bencomo, N., Johnsen, E. B., and '
                              'Tapia Tarifa, S. L. (2026). Declarative Lifecycle Management '
                              'for Self-Adaptive Systems. *Software and Systems Modeling*, '
                              '25, 787-814. <https://doi.org/10.1007/s10270-026-01358-w>.', 1)
        self.assertEqual(data['author'], 'Kamburjan, E. and Bencomo, N. and '
                         'Johnsen, E. B. and Tapia Tarifa, S. L.')
        self.assertEqual(data['journal'], 'Software and Systems Modeling')
        self.assertEqual(data['pages'], '787-814')

    def test_multisentence_title(self):
        _, data = bibtex_entry('Lemkin, J. (2025). A first sentence. A second sentence? '
                              'SaaStr. [Account](https://example.org/).', 1)
        self.assertEqual(data['title'], 'A first sentence. A second sentence?')

    def test_unsupported_format_stops_instead_of_skipping(self):
        with self.assertRaises(ValueError):
            bibtex_entry('An unstructured citation https://example.org/', 1)
        with self.assertRaises(ValueError):
            bibliography_entries('# References {.unnumbered}\n\nCitation\n\n# Appendix\n')
        with self.assertRaises(ValueError):
            bibliography_entries('# References {.unnumbered}\n')

    def test_incomplete_audit_cannot_pass(self):
        for papers, references in [(0, 0), (1, 0), (1, 36), (2, 37)]:
            with self.assertRaises(ValueError):
                validate_report({'summary': {'total_papers_processed': papers,
                                            'total_references_processed': references}}, 37)
        complete = {'total_papers_processed': 1, 'total_references_processed': 37}
        self.assertEqual(validate_report({'summary': complete}, 37), complete)

    def test_engine_receives_complete_corporate_author_and_strict_mode_fails(self):
        received = {}

        class FakeChecker:
            fatal_error = False

            def __init__(self, **kwargs):
                received.update(kwargs)
                self.report_builder = SimpleNamespace(web_searcher=object(), llm_verifier=object())

            def run(self, **kwargs):
                received['web_searcher'] = self.report_builder.web_searcher
                received['llm_verifier'] = self.report_builder.llm_verifier
                references = self.extract_bibliography(None)
                received['references'] = references
                Path(received['report_file']).write_text(json.dumps({'summary': {
                    'total_papers_processed': 1,
                    'total_references_processed': len(references),
                    'total_errors_found': 0, 'total_warnings_found': 0,
                    'total_unverified_refs': 1,
                }}))

        with tempfile.TemporaryDirectory() as directory:
            report_dir = Path(directory)
            manuscript = report_dir / 'paper.md'
            manuscript.write_text('# References {.unnumbered}\n\nNational Institute of '
                                  'Standards and Technology (2023). *AI framework*. '
                                  '[Framework](https://example.org/).\n')
            with patch('refchecker.core.refchecker.ArxivReferenceChecker', FakeChecker):
                with contextlib.redirect_stdout(io.StringIO()):
                    run_reference_check(manuscript, report_dir)
                    self.assertEqual(json.loads((report_dir / 'run.json').read_text())['status'], 'completed')
                    with self.assertRaisesRegex(RuntimeError, 'Strict reference check failed'):
                        run_reference_check(manuscript, report_dir, strict=True)
            self.assertEqual(received['llm_config'], {'disabled': True})
            self.assertIsNone(received['web_searcher'])
            self.assertIsNone(received['llm_verifier'])
            self.assertEqual(received['references'][0]['authors'],
                             ['National Institute of Standards and Technology'])
            self.assertEqual(json.loads((report_dir / 'run.json').read_text())['status'], 'failed')


if __name__ == '__main__':
    unittest.main()

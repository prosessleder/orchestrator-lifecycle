"""Source identity adapters for RefChecker 3.1.6.

Explicit DOIs select the publisher record. Explicit web citations select the
cited page, including pages the upstream URL heuristic does not recognize.
"""
import re
import time
from difflib import SequenceMatcher
from urllib.parse import quote

import requests
from refchecker.checkers.crossref import CrossRefReferenceChecker, _normalize_crossref_work
from refchecker.checkers.webpage_checker import WebPageChecker
from refchecker.utils.bibtex_parser import parse_bibtex_references
from refchecker.utils.text_utils import (
    are_venues_substantially_different, calculate_title_similarity, compare_authors,
)


def same_title(left, right):
    def normalized(value):
        return ''.join(char for char in value.casefold() if char.isalnum())
    left, right = normalized(left), normalized(right)
    return bool(left and right) and SequenceMatcher(None, left, right).ratio() >= 0.9


class DOIReferenceChecker(CrossRefReferenceChecker):
    """Preserve all Crossref containers and check the exact cited work."""

    def get_work_by_doi(self, doi):
        url = 'https://api.crossref.org/works/' + quote(doi, safe='')
        for attempt in range(3):
            try:
                response = requests.get(url, headers=self.headers, timeout=30)
                if response.status_code == 200:
                    raw = response.json()['message']
                    work = _normalize_crossref_work(raw)
                    work['_container_titles'] = raw.get('container-title', [])
                    return work
                if response.status_code not in (429, 500, 502, 503, 504):
                    break
            except (requests.RequestException, ValueError, KeyError):
                pass
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
        return None

    def search_works(self, *args, **kwargs):
        return []  # A title match must not replace an unavailable cited DOI.

    def search_works_bibliographic(self, *args, **kwargs):
        return []

    def verify_reference(self, reference):
        data, errors, url = super().verify_reference(reference)
        if data is None:
            return None, [{'error_type': 'unverified', 'error_details':
                           'Could not retrieve the exact cited DOI from Crossref'}], reference.get('url')
        title = reference.get('title', '')
        if calculate_title_similarity(title, data.get('title', '')) < 0.85:
            errors.append({'error_type': 'title', 'error_details':
                           f"Cited DOI title mismatch: {title!r} vs {data.get('title')!r}"})
        containers = data.get('_container_titles', [])
        cited_venue = reference.get('journal') or reference.get('venue')
        if cited_venue and containers and all(are_venues_substantially_different(
                cited_venue, venue, paper_title=title) for venue in containers):
            # Acronym/year conference labels cannot be resolved from a book
            # container alone. Keep that limitation visible as information.
            abbreviation = re.fullmatch(r'[A-Z0-9 .\'-]+', cited_venue)
            kind = 'info' if abbreviation else 'warning'
            errors.append({kind + '_type': 'venue', kind + '_details':
                           f'Container comparison: cited {cited_venue!r}; Crossref lists {containers!r}'})
        data.update(
            _matched_database='CrossRef (cited DOI)',
            year=self.extract_best_publication_year(data),
            authors=[{'name': author.get('name') or ' '.join(filter(None, (
                author.get('given'), author.get('family'))))} for author in data.get('author', [])],
            venue=cited_venue if cited_venue in containers else data.get('container-title', ''),
        )
        return data, errors, url


class CitedWebPageChecker(WebPageChecker):
    """Use page-provided citation authors before inferring an organization."""

    def __init__(self, reference):
        super().__init__()
        self.reference = reference
        self.explicit_authors = None

    def is_web_page_url(self, url):
        return url == self.reference['url'] or super().is_web_page_url(url)

    def _extract_site_info(self, soup, url):
        info = super()._extract_site_info(soup, url)
        # Restrict evidence to a citation whose title matches this page's cited
        # work, rather than accepting names from arbitrary body text/references.
        for block in soup.find_all(['code', 'pre']):
            text = block.get_text(' ', strip=True)
            if not re.search(r'@\w+\s*\{', text):
                continue
            for citation in parse_bibtex_references(text):
                if same_title(self.reference['title'], citation.get('title', '')):
                    authors = citation.get('authors', [])
                    if authors and authors != ['Unknown Author']:
                        info['citation_authors'] = authors
                        self.explicit_authors = authors
                        return info
        if same_title(self.reference['title'], self._extract_page_title(soup) or ''):
            authors = [meta.get('content', '').strip() for meta in soup.find_all('meta')
                       if meta.get('name', '').lower() in ('citation_author', 'dc.creator', 'author')]
            authors = [author for author in authors if author]
            if authors:
                info['citation_authors'] = authors
                self.explicit_authors = authors
        return info

    def _extract_page_title(self, soup):
        title = super()._extract_page_title(soup)
        if same_title(self.reference['title'], title or ''):
            return title
        # A generic HTML title such as "Home" must not override the actual
        # named specification or principles section on that same source page.
        cited = re.sub(r'\W+', '', self.reference['title']).casefold()
        for heading in soup.find_all(['h1', 'h2', 'h3']):
            text = heading.get_text(' ', strip=True)
            normalized = re.sub(r'\W+', '', text).casefold()
            if normalized and (cited == normalized or cited in normalized):
                return text
        return title

    def _check_author_match(self, cited_authors, site_info, url):
        if site_info.get('citation_authors'):
            return compare_authors(self.reference.get('authors', []), site_info['citation_authors'])[0]
        if self._personal_authors():
            # A site organization is not contradictory evidence about named
            # individual authors. Report unavailable authorship below instead.
            return True
        return super()._check_author_match(cited_authors, site_info, url)

    def _determine_authors(self, cited_authors, site_info, url):
        if self._personal_authors() and not site_info.get('citation_authors'):
            return []
        return site_info.get('citation_authors') or super()._determine_authors(cited_authors, site_info, url)

    def _personal_authors(self):
        return any(re.search(r', [A-Z]\.', author) for author in self.reference.get('authors', []))

    def verify_reference(self, reference):
        data, errors, url = super().verify_reference(reference)
        if data and self._personal_authors() and not self.explicit_authors:
            errors.append({'info_type': 'author', 'info_details':
                           'The cited page was checked, but explicit individual-author metadata was unavailable'})
        return data, errors, url

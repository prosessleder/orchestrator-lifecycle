# The Orchestrator: Lifecycle Architecture

**The Orchestrator: A Lifecycle Architecture for Self-Developing, Self-Operating, and Self-Improving Agentic Systems**

Timothy O'Brien · [ORCID](https://orcid.org/0009-0001-2589-347X) · Version 0.2.10 · 15 October 2026 · Unpublished citation revision

[Published version 0.2.9 on Zenodo](https://zenodo.org/records/23332590) · [Read the manuscript](paper.md) · [Download the PDF](release/paper.pdf) · [Download supplementary source](release/orchestrator-lifecycle-0.2.10-source.zip)

This architectural preprint proposes DEVELOP, OPERATE, and IMPROVE as responsibilities connected by durable orchestration and an immutable operating bundle. The bundle binds semantic interpretation, capabilities, authority, evaluation, and state compatibility. Observations can challenge the approved model through a governed change process.

The contribution is an architectural synthesis supported by illustrative contracts and a falsifiable evaluation design. Operational effectiveness and the additional value of ontology-based controls remain unevaluated. The paper explains how ontology evolution, capability admission, task governance, and evaluation semantics connect through one approved release and its operational action boundary.

## Repository scope

This repository publishes the paper and its supporting artifacts. Internal discussion, planning, preliminary code, and exploratory research belong in the [private companion repository](https://github.com/prosessleder/orchestrator-lifecycle-internal). See [the contribution workflow](CONTRIBUTING.md) for moving selected results into this publication repository.

## Manuscript format

The PDF uses the standard [Elsevier `elsarticle` manuscript class](https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions) in single-column preprint mode: 12-point serif text, native title and abstract, keywords, numbered sections, and author-year citations. It is an independent preprint; use of this class does not indicate submission to or acceptance by a journal. ORCID and preprint status appear in first-page notes.

## Contents

| Artifact | Purpose |
|---|---|
| [paper.md](paper.md) | Manuscript, bibliography, and declarations |
| [release/paper.pdf](release/paper.pdf) | Typeset preprint |
| [release/paper.tex](release/paper.tex) | Standalone LaTeX source with embedded vector diagrams |
| [architecture/](architecture/) | Components, lifecycle, semantics, governance, interfaces, and failure modes |
| [schemas/](schemas/) | Illustrative interface schemas, fixtures, and validation checks |
| [integration/books.md](integration/books.md) | Conceptual relationship to the three Orchestrator books |
| [release/metadata.json](release/metadata.json) | Prepared Zenodo record fields |
| [release/zenodo-upload.md](release/zenodo-upload.md) | Deposit instructions |
| [release/SHA256SUMS](release/SHA256SUMS) | PDF and source-archive checksums |

## Rebuild

Requirements: Python 3.11+, Pandoc, network access for reference verification, and a TeX distribution containing `elsarticle`. The PDF export command uses Tectonic. The generated LaTeX embeds the diagram and formatting definitions and does not depend on additional project files.

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-validation.txt -r requirements-refchecker.txt
python3 scripts/build_paper.py       # audit references and generate release/paper.tex
python3 scripts/build_paper.py --pdf # audit references and also export the PDF
python3 schemas/test_contracts.py   # validate illustrative contracts and fixtures
python3 scripts/package_release.py  # rebuild source archive and checksums
python3 scripts/check_publication_scope.py # check public inventory and archive
```

Edit `paper.md` and regenerate the LaTeX/PDF. `scripts/journal-template.tex` supplies the manuscript frontmatter through the standard class interfaces. The generator converts the two Mermaid figures to embedded TikZ diagrams. `publication-files.json` explicitly lists source-package inputs; files added beside them are not included automatically.

Every normal build runs [RefChecker](https://github.com/markrussinovich/refchecker), pinned in `requirements-refchecker.txt`, before rendering. The adapter reads the final References section of `paper.md`, derives structured metadata, and checks that the engine processes every entry. DOI citations are checked against the exact Crossref record, retaining print dates and all chapter/book container titles. Web citations are checked at their cited URL; matching page-provided BibTeX authors take precedence over an inferred site organization. Other sources use RefChecker's normal verification. Unavailable DOI records and inaccessible pages remain visible as unverified findings or access warnings. Titles, authors, publication years, the primary URL/DOI, and available venue metadata are checked where the selected source provides them. Secondary links, edition statements, and whether sources support the manuscript's claims require separate review. LLM extraction and deep hallucination checks are disabled; no LLM account or API key is needed. Optional `SEMANTIC_SCHOLAR_API_KEY` can improve scholarly API rate limits.

Reports go to the ignored `tmp/refchecker/` directory: `refchecker.json` contains findings, `inputs.json` maps the extracted fields to the original entries, `references.bib` is the generated bibliography, and `run.json` records the input hash, tool version, coverage, and completion status. Unsupported bibliography formatting, missing dependencies, incomplete coverage, and execution failures stop the build. Citation errors, warnings, and unverified sources are advisory by default; use `--strict-references` to fail on those findings too. Database coverage and source availability vary, especially for websites and recent papers; an unverified source is not proof of fabrication. A reported match can also identify a different work with a generic title; compare the matched source with the cited URL. Source text is never automatically corrected.

Use `--skip-reference-check` for an explicit offline rendering build, or `--reference-report-dir PATH` to save an audit elsewhere. Run only the audit with `python3 scripts/check_references.py`, or its offline regression tests with `python3 scripts/test_reference_check.py`. The manually dispatched **Build and check references** GitHub Actions workflow runs the normal build and retains the audit as a temporary workflow artifact. Local research interpretations belong in the private companion; reports are excluded from the publication archive.

## Related books and license

The [Orchestrator series](https://readorchestrator.com) develops the professional, engineering, and organizational implications of delegated intelligence. Its [canonical book source](https://github.com/prosessleder/orchestrator) is maintained separately.

Copyright 2026 Timothy O'Brien. The paper and its original embedded diagrams are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). [RIGHTS.md](RIGHTS.md) specifies the paper-only scope and separate rights in other supplementary material. This working copy is an unpublished citation revision. Version 0.2.9 remains published on Zenodo: [DOI 10.5281/zenodo.23332590](https://doi.org/10.5281/zenodo.23332590). The deposit contains the paper PDF; supplementary source remains available here. The [all-versions DOI](https://doi.org/10.5281/zenodo.23332589) identifies the evolving work.

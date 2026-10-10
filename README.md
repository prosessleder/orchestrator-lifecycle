# The Orchestrator: Lifecycle Architecture

**The Orchestrator: A Lifecycle Architecture for Self-Developing, Self-Operating, and Self-Improving Agentic Systems**

Timothy O'Brien · [ORCID](https://orcid.org/0009-0001-2589-347X) · Version 0.2.8 · 10 October 2026

[Read the manuscript](paper.md) · [Download the PDF](release/paper.pdf) · [Download supplementary source](release/orchestrator-lifecycle-0.2.8-source.zip)

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

Requirements: Python 3, Pandoc, and a TeX distribution containing `elsarticle`. The PDF export command uses Tectonic. The generated LaTeX embeds the diagram and formatting definitions and does not depend on additional project files.

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-validation.txt
python3 scripts/build_paper.py       # generate release/paper.tex
python3 scripts/build_paper.py --pdf # also export the PDF
python3 schemas/test_contracts.py   # validate illustrative contracts and fixtures
python3 scripts/package_release.py  # rebuild source archive and checksums
python3 scripts/check_publication_scope.py # check public inventory and archive
```

Edit `paper.md` and regenerate the LaTeX/PDF. `scripts/journal-template.tex` supplies the manuscript frontmatter through the standard class interfaces. The generator converts the two Mermaid figures to embedded TikZ diagrams. `publication-files.json` explicitly lists source-package inputs; files added beside them are not included automatically.

## Related books and license

The [Orchestrator series](https://readorchestrator.com) develops the professional, engineering, and organizational implications of delegated intelligence. Its [canonical book source](https://github.com/prosessleder/orchestrator) is maintained separately.

Copyright 2026 Timothy O'Brien. The paper and its original embedded diagrams are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). [RIGHTS.md](RIGHTS.md) specifies the paper-only scope and separate rights in other supplementary material. This public repository provides the manuscript and supporting artifacts; no Zenodo DOI has been assigned.

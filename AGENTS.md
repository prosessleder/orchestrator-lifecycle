# Public paper repository

This repository publishes the Orchestrator lifecycle paper and its supporting publication artifacts.

## Where work belongs

- Put internal discussion, planning, review notes, exploratory research, initial code, prototypes, and unpublished experimental results in the private companion: `prosessleder/orchestrator-lifecycle-internal` (normally the sibling checkout `../orchestrator-lifecycle-internal`).
- Keep this repository limited to the manuscript, publication metadata, source/build tools, and the literature evidence, specifications, fixtures, or reproducibility artifacts that support the paper.
- The private companion's `publication/` directory is a working copy for candidate publication material. Transfer selected reviewed files; never merge its private history or mirror the entire private repository here.
- A user request to edit or publish the paper authorizes the necessary publication work. A research or brainstorming request alone does not authorize publishing its internal records.
- Do not add internal progress reports, agent reviews, drafting conversations, or private archive links to the source package.

## Publication inventory and verification

`publication-files.json` is the explicit inventory for the public tree and supplementary source archive. Add a path only when its content is intended to support the publication. New files in an approved directory are not automatically approved archive inputs.

For manuscript edits, update `paper.md`, regenerate `release/paper.tex` and the PDF, compile, and inspect the rendered pages. Keep the author-provided declarations, ORCID, omitted affiliation, and paper-only CC BY 4.0 scope consistent.

After any packaged source changes:

```sh
python3 scripts/package_release.py
python3 scripts/check_publication_scope.py
```

Run `python3 schemas/test_contracts.py` when contracts or fixtures change. Check the actual contents of newly published artifacts as well as their paths. The inventory check controls file inclusion; it does not determine whether prose or data is ready to publish.

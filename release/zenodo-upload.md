# Zenodo upload package

Prepared 10 October 2026 for **manual author upload**. No record was created, no DOI was reserved, and no Zenodo publication occurred.

Upload `paper.pdf` as the primary article, licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**. Optionally upload `orchestrator-lifecycle-0.2.6-source.zip` as supplementary source. The source archive contains the manuscript, standalone LaTeX, literature search record, architecture documents, schemas, build scripts, and conceptual mapping to the books; `RIGHTS.md` specifies the paper license and the separate rights of other material, as described in that rights statement. Preserve that scope notice in the record description if uploading the archive. `SHA256SUMS` identifies the primary PDF and source archive.

## Record fields

| Field | Prepared value |
|---|---|
| Resource type | Publication / Preprint |
| Title | The Orchestrator: A Lifecycle Architecture for Self-Developing, Self-Operating, and Self-Improving Agentic Systems |
| Creator | O'Brien, Timothy |
| Publication date | 2026-10-10 (change if the public release uses another date) |
| Version | 0.2.6 |
| Language | English |
| Description | Use the abstract in `metadata.json` or `paper.md` |
| Keywords | Agentic systems; ontology evolution; self-adaptive systems; semantic contracts; delegated intelligence; lifecycle governance |
| Related work | The Orchestrator Series, https://readorchestrator.com |
| Related source | https://github.com/prosessleder/orchestrator-lifecycle (public) |
| License | Creative Commons Attribution 4.0 International (CC BY 4.0); identifier `cc-by-4.0` |
| License scope | Paper and its original embedded diagrams. Supplementary archive includes material with separate rights; see `RIGHTS.md`. |
| File access | Choose the desired Zenodo access setting when depositing; the GitHub repository is public |
| ORCID | https://orcid.org/0009-0001-2589-347X |
| Affiliation | Omitted at the author’s request |
| Funding | No external funding |
| Competing interests | Authorship and publication of The Orchestrator book series; no additional competing interests |
| DOI | Leave empty until Zenodo assigns/reserves one; do not reuse another work's DOI |

## Upload

1. Sign in to Zenodo and create a new upload.
2. Upload the primary PDF and the selected supplementary source files. Check `SHA256SUMS` if transferring the files through another service.
3. Enter the prepared fields and select **Creative Commons Attribution 4.0 International (CC BY 4.0)** for the paper. Select the desired file-access setting. If uploading the source archive, use Zenodo's mixed-license options to declare its separate supplementary rights as well, adding a custom rights statement when needed. Include the scope notice: "The paper and its original embedded diagrams are licensed under CC BY 4.0. Supplementary material retains the separate rights specified in the archive's RIGHTS.md."
4. Save the draft and inspect the metadata and preview. If reserving a DOI, add that exact DOI to the manuscript and citation metadata, then regenerate and replace files before publishing.
5. Publish only when the author has accepted the manuscript and declarations. This package does not publish automatically.
6. After publication, update `CITATION.cff`, the manuscript artifact statement, and repository links with the actual record DOI. Make a new version when changing published files.

`metadata.json` is a prepared **UI field guide**, not a promise of API-schema conformance or a submission response. It records the author's CC BY 4.0 choice for the paper. No automated deposit configuration is supplied; the supplementary archive's separate rights are described explicitly for manual upload.

Zenodo's [quick start](https://help.zenodo.org/docs/get-started/quickstart/) explains upload, describe, and publish; its [licenses guide](https://help.zenodo.org/docs/deposit/describe-records/licenses/) explains standard/custom licenses; [record versioning](https://help.zenodo.org/docs/deposit/manage-versions/) describes later file revisions. These pages were checked 9 October 2026.

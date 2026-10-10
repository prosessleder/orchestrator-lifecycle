# Contributing to the paper

This public repository contains the manuscript and supporting publication artifacts. Internal research and development takes place in the [private companion repository](https://github.com/prosessleder/orchestrator-lifecycle-internal).

Use the private repository for working discussions, plans, draft reviews, initial research code, exploratory experiments, raw results, and material that is not yet selected for publication. Its Issues track tasks; its Discussions support open questions and research conversations.

A public change should improve the paper or provide a specific supporting artifact, such as a specification, source comparison, illustrative fixture, or reproducibility package. Internal review logs and general prototype development remain private. The existing public literature search record and contribution assessment are publication supplements.

## Moving a result into the public repository

1. Prepare the selected manuscript or supporting files in the private repository's `publication/` working copy, or make a directly requested paper edit here.
2. Review the proposed public diff for relevance, accuracy, attribution, rights, and unintended internal content. Transfer only the selected files; do not merge private Git history or mirror the private repository.
3. Update `publication-files.json` when publication inputs change. It names every approved source and repository-support file explicitly.
4. Rebuild affected artifacts, run relevant contract checks, regenerate the source archive, and run `python3 scripts/check_publication_scope.py`.
5. Commit the public change under the author's publication direction. Record the resulting public commit in the private repository's pairing record or planning log.

There is no automatic synchronization between the repositories. File-inventory and checksum checks detect accidental inclusion and stale packages; content review remains necessary.

## Rights

The paper and its original embedded diagrams use CC BY 4.0. Other material has the separate rights described in [RIGHTS.md](RIGHTS.md). Moving code or research material into this repository does not silently extend the paper's license to it.

# Contribution scope and evaluation hypotheses

Initial assessment: **9 October 2026, America/Los_Angeles**. Security and scope comparison updated **10 October 2026**.

The architecture combines substantially anticipated ingredients into an explicit reference contract and a falsifiable research agenda. The literature study does **not** establish originality or priority of the exact combination. No complete operational implementation or empirical validation is reported.

The evidence and access levels are in [related-work.md](related-work.md), [search-log.md](search-log.md), and [references.md](../references.md). The comparison below distinguishes established mechanisms from the proposed integration.

## Relationship to established mechanisms

| Architectural ingredient | Relevant antecedents | Contribution boundary |
|---|---|---|
| Continuous operate/analyze/improve/redeploy loop | IBM blueprint, Rainbow, models@run.time | Established feedback-control architecture |
| Coordinated development, operation, and improvement responsibilities | Composable managing systems and MAPE-K | Explanatory decomposition within an established architecture family |
| Shared ontological semantics | Ontology engineering and ontology-backed adaptation/security | Established modeling and adaptation practice |
| Ontology branches, semantic diffs, approval, migration, and rollback | Stojanovic et al.; Klein and Noy; Quit Store | Established ontology-evolution and version-control mechanisms |
| Operational evidence driving gated ontology/tool evolution | EvoOntology | Direct modern precedent |
| Policy/behavior/recovery compatibility for capability versions | Governed Capability Evolution | Direct lifecycle-governance precedent |
| Semantic change analysis for security and dependent systems | Peldszus et al. | Established security co-evolution concern |
| Ontology as a semantic contract for bounded delegated authority | Jørgensen and Ma; Symbolic Separation | Direct semantic/authority-contract precedents |
| Versioned evidence for reconstructable release decisions | PROV-O, in-toto, MLflow, EIO-Agents | Established provenance and evaluation mechanisms |
| Purpose, knowledge limits, and task alignment | NIST AI RMF; Task Shield; OWASP excessive-agency guidance | Established governance/security concerns; lifecycle integration is the proposed contribution |
| Joint contract connecting semantic mismatch, dependencies, authority effects, deployment epochs, and state rollback | Combined antecedents above | Proposed specification and integration; exact-combination originality unestablished |

Sources: [IBM](https://users.cs.fiu.edu/~sadjadi/Teaching/Autonomic%20Grid%20Computing/CIS-6612-Summer-2006/AC-Blueprint-WhitePaper-V7.pdf), [Klein–Noy](https://ceur-ws.org/Vol-71/Klein.pdf), [EvoOntology](https://arxiv.org/html/2609.15779v1), [Governed Capability Evolution](https://arxiv.org/html/2604.08059v6), [Peldszus et al.](https://researcher.itu.dk/p/en/research-outputs/ontology-driven-evolution-of-software-security), [Jørgensen–Ma](https://doi.org/10.3390/info17090923), [EIO-Agents](https://arxiv.org/abs/2610.07675v1).

## Architectural limits and alternative explanations

1. **Architecture family.** The lifecycle belongs to the MAPE-K and governed-deployment tradition. Its focus is the explicit contract for semantic dependencies and lifecycle authority.
2. **Existing ontology loop.** EvoOntology already provides a versioned content/schema/tool state and an evaluated evolution loop. Benefits of the additional contract obligations proposed here remain hypotheses.
3. **Composition and originality.** A specification can clarify interactions among established mechanisms without originating them. Absence of a paper with the same terminology does not establish novelty of the composition.
4. **Ontology-free alternatives.** Conventional schemas, typed APIs, dependency graphs, and policy gates may provide similar benefits. Formal entailments and concept-level dependencies are proposed advantages to compare against maintenance and reasoning cost.
5. **Fallible mismatch detection.** Evidence, task failure, constraints, and representation coverage support diagnosis, but cannot identify every missing concept. Incomplete facts, unknown instances, contradictory assertions, missing procedures, and conceptual gaps remain distinct possibilities.
6. **Consistency versus compatibility.** Logical consistency does not preserve deployed behavior. Compatibility is relative to named consumers, imports, queries, mappings, policies, and datasets; additions can broaden a class consumed by an old capability or policy.
7. **Enforced independence.** Governance depends on credentials, protected criteria, immutable evidence, and admission controls outside candidate-edit authority. Separate prompts under one unrestricted credential do not establish that boundary.
8. **Configuration versus behavior.** A manifest supports reconstruction to the extent artifacts and services remain available. External responses, provider changes, scheduler order, retrieval state, and nondeterminism limit behavioral replay.
9. **Recovery versus reversal.** Artifact rollback does not undo completed actions or lossy knowledge migration. Checkpoints, compensation, suspension, and forward repair have different applicability and limits.
10. **Semantic authority.** Domain meaning, evidence status, and permission are different objects. A semantic change can enlarge effective permission under unchanged policy bytes, requiring analysis of authority effects at promotion and enforcement at action time.

These constraints concern the proposal and its evaluation. They do not assert that all comparators lack the described protections.

## Proposed contribution

The reference architecture synthesizes autonomic control, ontology evolution, and governed deployment. It specifies evidence-bearing handoffs, immutable bindings among semantic and executable artifacts, and independently enforced admission conditions to make semantic and authority changes inspectable across development, operation, and improvement. Its exact-combination originality and practical benefits remain unestablished. Conditional coherence and configuration reconstruction are narrower properties than domain safety, conceptual adequacy, or identical repeated execution.

## Evidence that would change the assessment

| Hypothesis | Necessary comparator | Falsifying result |
|---|---|---|
| Named semantic dependencies improve change-impact detection | Same workflow with schema/API checks and a dependency graph | Similar coverage/cost without ontology-specific mechanisms |
| Joint semantic/authority gates detect otherwise hidden escalation | Gated capability upgrade with policy checks alone | No additional faults found, or gains explained only by larger test budget |
| Binding an interpretation regime prevents mixed-version errors | GitOps with ordinary artifact manifests | No improvement under import drift, stale caches, and rolling deployment |
| Role separation improves diagnosis and audit | Unseparated adaptive controller with identical permissions and evaluation | No improvement in diagnosis or reconstructability |
| State-aware rollback improves recovery | Artifact-only rollback and standard migration practice | Recovery no better, or checks cannot identify irreversible cases |

A prospective evaluation includes adversarial semantic changes, taxonomy additions, policy class broadening, stale replicas, failed/irreversible migrations, and evidence poisoning. Separate test and tuning sets, repeated stochastic runs, rejection cases, and reported reasoning coverage would help distinguish contract effects from tuning or test-budget effects. No empirical results are reported.

## Limits of the study

This was an English-language, targeted web search with backward/adjacent leads and current primary documentation. It did not systematically search every publisher index, all languages, patents, unpublished work, commercial deployments, or every repository history. Primary abstracts were used where full texts were inaccessible; those cannot support negative absence claims. Recent preprints may change and should be rechecked before release. A novelty guarantee cannot follow from this search, and the evidence actively argues against broad novelty.

## Security comparison qualification

The 10 October follow-up supports a distinction among control objectives, not a claim that identity, access control, or business processes exhaust prior research. The added manuscript section defines semantic, epistemic, and task/action scope and explains a conditional risk: overbroad tools or mutable decision inputs can allow an agent's expanded task interpretation to produce effects beyond its delegation. Correctly enforced resource restrictions remain effective. The ontology and orchestration mechanisms require comparative evaluation against context-aware policy and task-alignment baselines; no security advantage is established by terminology alone.

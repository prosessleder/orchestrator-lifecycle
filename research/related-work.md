# Related work and architectural comparison

Review date: **9 October 2026, America/Los_Angeles**. This is a targeted primary-source review, not an exhaustive systematic review. The [search log](search-log.md) preserves queries, screening scope, and access limits. Bibliographic keys resolve in [references.md](../references.md).

## The architectural loop is established

Autonomic computing provides a foundation for the proposed lifecycle. Kephart and Chess establish the self-management vision [kephart2003]. IBM’s 2005 blueprint describes shared semantic knowledge, orchestrating managers, configurable human participation, and requests/plans that precede change execution [ibm2005]. The proposed roles map onto that tradition; the feedback loop is an established architectural ingredient. [IBM primary blueprint](https://users.cs.fiu.edu/~sadjadi/Teaching/Autonomic%20Grid%20Computing/CIS-6612-Summer-2006/AC-Blueprint-WhitePaper-V7.pdf).

| Proposed responsibility | Closest MAPE-K correspondence | What the framing clarifies |
|---|---|---|
| OPERATE | Managed system plus observation interfaces; may contain its own local control loop | Running assigned work and reporting semantic uncertainty are explicit responsibilities |
| IMPROVE | Analysis and part of planning | Evidence interpretation and candidate semantic change are separated from live execution |
| DEVELOP | Realization of a plan, build/test machinery, and capability production | Creation of executable artifacts is distinguished from operational actions |
| ORCHESTRATOR and deployment controls | Managing-system coordination, execution controls, and manual/policy management | Lifecycle admission is a durable, enforceable workflow |
| Ontology, policies, evidence, and state | Different parts of K | K is decomposed into separately versioned artifacts with different authority |

This is an analytical mapping, not a proof that the decompositions are identical. A MAPE-K implementation may encompass the entire proposal; a task agent may itself contain a MAPE loop. DEVELOP/OPERATE/IMPROVE names are useful role vocabulary, not evidence of scientific novelty.

Rainbow supplies an external architecture-based adaptation mechanism and explicit strategies, anticipating the separation of application behavior from an adaptation controller [garlan2004]. Models@run.time supplies causally connected representations used during adaptation [blair2009]. A domain ontology is not necessarily the same thing as a self-model: an implementation needs an explicit mapping between domain semantics, system architecture, and observations. [Rainbow](https://www.cs.cmu.edu/~able/publications/computer04/), [Models@run.time](https://research.aston.ac.uk/en/publications/modelsruntime/).

## Ontology evolution is already a lifecycle discipline

Stojanovic and colleagues describe a controlled evolution process, consistency preservation, dependency propagation, and use-driven refinement [stojanovic2002]. Klein and Noy integrate change logs, structural/conceptual differences, transformations, approval, and selective rollback [klein_noy2003]. Noy and Klein distinguish semantic compatibility from database-schema compatibility [noy_klein2004]. These works directly anticipate most ontology-change workflow requirements. [Author manuscript](https://www.cs.ox.ac.uk/boris.motik/pubs/smms02userdriven.pdf), [component framework](https://ceur-ws.org/Vol-71/Klein.pdf), [semantic compatibility](https://research.vu.nl/en/publications/ontology-evolution-not-the-same-as-schema-evolution/).

The logical-difference and conservative-extension literature makes compatibility relative to vocabulary and query language, with nontrivial computational limits [botoeva2017]. A finite regression suite provides evidence about tested consumers, not a universal guarantee. Unsupported reasoning, timeout, partial coverage, and unknown compatibility remain distinct outcomes in the reference contract. [Primary survey](https://arxiv.org/abs/1804.07805v1).

Quit Store brings branches, merges, synchronization, and provenance to RDF datasets [quit2018; journal publication 2019]. Semantic artifact version control therefore has a direct precedent. A storage-level merge is not itself evidence that the resulting ontology preserves meaning for a deployed capability. [Primary preprint](https://arxiv.org/abs/1805.03721v3).

## Ontologies already support adaptation and security

Evesti and colleagues integrate ontology knowledge, an adaptation loop, and access-control enforcement [evesti2013]. ROSA places adaptation knowledge in a central knowledge base used by MAPE components and supports task/architecture co-adaptation [rosa2025]. Kamburjan and colleagues formalize declarative lifecycle stages, including OWL semantic stages and compatibility of the managing system’s components [kamburjan2026]. Ontology-backed orchestration and lifecycle control therefore have direct architectural precedents. [Security architecture](https://doi.org/10.3390/computers2010034), [ROSA](https://doi.org/10.3389/frobt.2025.1531743), [declarative lifecycle](https://link.springer.com/article/10.1007/s10270-026-01358-w).

Peldszus and colleagues’ primary abstract specifies semantic editing patterns, dependent-system co-evolution proposals, adaptation of security checks, and incremental compliance analysis [peldszus2021]. It establishes a direct precedent for connecting ontology change to security impact. Full-text access was limited; no claim about an omitted mechanism’s absence follows. [Institutional primary abstract](https://researcher.itu.dk/p/en/research-outputs/ontology-driven-evolution-of-software-security).

## Closest contemporary agent systems

EvoOntology is a close direct modern comparator. It maintains versioned content/schema/tool state; a builder constructs the initial ontology and an evolution agent uses execution trajectories to propose typed interventions, admitted through paired validation. Rejected changes are not deployed [evoontology2026]. The inspected method anticipates selective ontology services, evidence-linked edits, semantic/tool co-evolution, and validation before deployment. [Inspected §§3.1–3.3](https://arxiv.org/html/2609.15779v1).

Governed Capability Evolution provides four compatibility dimensions and a staged version-admission pipeline with sandbox, shadow, activation, monitoring, rollback, and audit. Its capability metadata includes policy and recovery concerns [governed2026]. Read alongside EvoOntology, it is a strong combined anticipation of the proposed architecture. A single-source novelty test is insufficient. [Current accepted manuscript §§3–5](https://arxiv.org/html/2604.08059v6).

SciToolAgent-Evo couples reusable skills/experience with an ontologized tool graph and acquisition of unfamiliar tools [scitool2026]. MEGA’s abstract describes evidence-driven optimization of both agents and a typed Wisdom Graph [mega2026]. Darwin Gödel Machine modifies agent code and validates candidates [dgm2025]. Continuous agent improvement and knowledge-guided adaptation are established research agendas. The reference architecture addresses the contracts connecting such changes to deployment and operational authority. [SciToolAgent-Evo](https://arxiv.org/html/2607.28692v1), [MEGA](https://arxiv.org/abs/2608.10504v1), [DGM](https://arxiv.org/abs/2505.22954v3).

EIO-Agents explicitly targets typed evaluation evidence and content-addressed, verifiable evaluation records [eio2026]. Symbolic Separation uses ontology-constrained operations and deterministic checks [symbolic2026]. Jørgensen and Ma describe ontology, contextual evidence, process, and authority contracts bound within an externally governed task envelope [jorgensen_ma2026]. These are relevant counterexamples to broad claims about semantic contracts, independently checked evidence, or governed delegated intelligence. [EIO-Agents](https://arxiv.org/abs/2610.07675v1), [Symbolic Separation](https://arxiv.org/abs/2609.17107v1), [bounded-autonomy framework](https://doi.org/10.3390/info17090923).

The following comparison identifies overlap and specification questions. Its last column does not assert that a comparator omits the proposed answer.

| Closest comparison | Verified overlap | Question for this reference contract |
|---|---|---|
| [Declarative Lifecycle Management, Kamburjan et al. (2026)](https://doi.org/10.1007/s10270-026-01358-w) | Semantic lifecycle stages and adaptation of managing-system components | How do lifecycle stages bind to delegated work, release evidence, and effective authority? |
| [EvoOntology, Chong et al. (2026)](https://arxiv.org/abs/2609.15779v1) | Versioned content/schema/tool layer, trajectory-derived edits, paired validation before admission | Which semantic dependencies and consumer consequences must one release pin and check? |
| [Governed Capability Evolution, Qin et al. (2026), v6](https://arxiv.org/abs/2604.08059v6) | Interface/policy/behavior/recovery compatibility and staged activation, monitoring, rollback, audit | How is ontology-dependent authority impact incorporated into capability admission and action-time enforcement? |
| [Bounded-autonomy framework, Jørgensen and Ma (2026)](https://doi.org/10.3390/info17090923) | Ontology, evidence, process, and authority contracts in an externally governed task envelope | How does the envelope remain tied to an exact evolving semantic release and compatible state? |
| [EIO-Agents (2026)](https://arxiv.org/abs/2610.07675v1); [Symbolic Separation (2026)](https://arxiv.org/abs/2609.17107v1) | Typed/content-addressed evaluation evidence; ontology-grounded deterministic operational checks, respectively (abstract review) | How do such checks cover promotion, activation epochs, and state-aware recovery together? |

## Engineering mechanisms are inherited

OpenGitOps supplies declarative, immutable, pulled, reconciled deployment; MLflow tracks code, parameters, metrics, and artifacts; PROV-O represents lineage; in-toto verifies supply-chain integrity [opengitops, mlflow, prov_o, in_toto2019]. The operating bundle extends ordinary dependency/provenance accounting with a named semantic dependency and interpretation regime. Configuration reconstruction remains distinct from deterministic LLM outputs. [OpenGitOps](https://opengitops.dev/), [MLflow](https://mlflow.org/docs/latest/ml/tracking/), [PROV-O](https://www.w3.org/TR/prov-o/), [in-toto](https://www.usenix.org/conference/usenixsecurity19/presentation/torres-arias).

Current primary project documents also describe governed semantic artifacts, ontology edit ledgers, and evolution/operation planes [inferal_draft, agent_utilities, self_evolving_software]. Their archival chronology has not been established; their content is a lead for follow-up, not a dated priority proof. [Inferal draft](https://ontosome.com/modules/artifact-evolution/spec/), [ontology system](https://github.com/Knuckles-Team/agent-utilities/blob/main/docs/architecture/ontology_system.md), [self-evolving software](https://github.com/douglas-grishen/self-evolving-software).

## Contribution scope

The contribution is an **architectural synthesis and explicit reference contract**: one inspectable path from an operational mismatch to a candidate semantic change, dependent capability development, independent promotion, and state-aware rollback. Originality of that exact combination remains unestablished. The contract specifies joint obligations, failure boundaries, and a way to evaluate their interaction. A new algorithm, empirical improvement, formal global safety guarantee, or first-of-kind system is not established by this study. The [contribution assessment](contribution-assessment.md) relates those limits to proposed evaluation hypotheses.

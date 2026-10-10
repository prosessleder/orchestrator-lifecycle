# Failure modes, adversarial cases and unresolved questions

These cases identify design obligations and suggested future experiments. They are analytical examples, not measured test results.

## What cannot be represented?

The system can retain a raw observation and its evidence even when it cannot assign an adequate authoritative interpretation. OPERATE should classify the mismatch provisionally; IMPROVE may revise that classification after investigation. More than one category may apply.

| Report category | Example | First response | When ontology change is justified |
|---|---|---|---|
| `missing_fact` | The product model of a known returned device is absent | Retrieve evidence or request a fact; preserve uncertainty | Only if the required kind of fact/relationship cannot be expressed |
| `unknown_entity` | A previously unregistered device identifier appears in an intake record | Establish identity and create a governed instance assertion | Only if no adequate category/relationship covers it |
| `contradictory_observation` | Two intake records assert incompatible locations for the same returned item | Check provenance, noise, temporal scope and logical/shape consistency; quarantine affected inference | If the contradiction exposes a genuine modeling defect rather than bad data |
| `constraint_violation` | A required handling-clearance record is absent | Hold the affected action under the declared company-policy validation rule | Only if investigation identifies a modeling defect; a failed requirement alone does not establish one |
| `schema_gap` | A damaged-battery report requires a distinction and assessment relation absent from the return model | Preserve the raw report; investigate alternative models and impacts | When evidence supports a new/revised concept, relation or constraint |
| `procedure_gap` | The model can describe the reported condition, but no approved exception-review workflow applies | Suspend that procedure or escalate; propose a capability/workflow change | Ontology change may be unnecessary; a procedure can be missing in an adequate model |
| `unclassified` | An intake observation cannot yet be assigned a supported diagnosis | Retain raw evidence and explain the uncertainty without inventing a concept | Only after investigation establishes whether the cause is conceptual, factual, procedural or something else |

A SHACL failure alone is not proof of a missing concept. OWL's open-world interpretation is not a license to treat unproven observations as false; application policy must specify where absence triggers uncertainty, validation failure or denial. A diagnostic classifier's confidence is evidence about its estimate, not a formal guarantee that it selected the right category.

## Adversarial cases

| Failure | Counterexample or trigger | Required handling | Residual limitation |
|---|---|---|---|
| Ontology drift | Unlocked remote import changes while root commit stays fixed | Retain and pin full closure; reject unresolved imports | Artifact correctness and conceptual adequacy remain unknown |
| Conflicting branches | Two extensions introduce incompatible identity/constraint assumptions | Compare against current base; rebase/merge; rerun affected checks and approval | Semantic merges need domain judgment |
| Incompatible capability | New subtype enters a broad handler that assumes ordinary physiology | Analyze inferred membership and procedure dependencies; add adversarial category cases | Tests cannot cover every future instance |
| Stale operational agent | Worker resumes old history after promotion | Enforce epoch/lease at receiving action resource | Unmanaged credentials invalidate fencing |
| Invalid knowledge migration | Multiple identities collapse and cannot be separated afterward | Check transformations, checkpoints, invariants and recovery conditions | Lossy migrations may permit only forward repair |
| Incorrect novelty diagnosis | A missing product-model fact is reported as a missing ontology class | Triage categories, alternative explanations and provenance | False positives add cost; false negatives may suppress needed change |
| Recursive improvement loop | Every new model produces another mismatch proposal | Deduplicate; bound depth, budgets and deployment rate; record stop conditions | Poor thresholds can suppress useful learning |
| Unbounded self-modification | Candidate rewrites evaluator or adds credentials in its deployment config | Independent evaluator/gate ownership; governance change path; deny candidate-controlled grants | Compromised control plane defeats separation |
| Rollback failure | New actions and state schema cannot be interpreted by old bundle | Assess compatible state; use repair/compensation path | Past external effects may be irreversible |
| Ontology completeness illusion | All known shapes pass although a phenomenon is absent from the vocabulary | Permit raw evidence and unresolved reports; evaluate coverage claims separately | Unknown unknowns cannot be eliminated by versioning |
| Silent authority change | `DamagedBatteryReturn ⊑ ReturnItem` can expand a category-based permission; the warehouse clearance guard still denies unassessed cases | Compare effective policy denotation under candidate closure; require a separate grant if permissions expand | Complete open-world authority comparison may be infeasible |
| Model nondeterminism | Same prompt/model versions produce different diagnoses | Record actual outputs and evaluation conditions; use probabilistic/behavioral evaluations | Configuration replay does not guarantee output replay |
| Communication failure | Duplicate delivery schedules the same migration twice | Durable IDs, deduplication, CAS and idempotency/reconciliation | External resources may lack idempotency support |
| Approval bottleneck | Human reviews cannot keep up with mismatch volume | Risk-tiered preapproved gates, batching, explicit operational disposition | More automation can weaken review if coverage is poor |
| Rolling version skew | New ontology, old policy adapter and old knowledge schema execute together | Commit bundle/state binding; stage then fence; explicit coexistence protocol if needed | Base protocol may require temporary service interruption |
| Mutable validation context | Shape import or reasoner config changes after checks | Pin validation inputs and exact evaluator/environment; invalidate changed evidence | Provider-hosted models may not remain retrievable |
| Time-of-check/time-of-use | State eligibility changes after policy decision | Recheck critical facts transactionally at the action resource or use bounded reservation | Cross-resource guarantees require extra protocols |
| Partial deployment | Pointer updated but new runtime never becomes ready | Verify readiness before commit; define timeout, fencing and recovery state | Capacity loss can preserve safety while harming liveness |
| Evidence poisoning | A report embeds instructions to approve itself | Structured parsing; isolate candidate data and evaluator authority | Human/evaluator interpretation can still be manipulated |
| Information leakage | Evidence copied into logs includes secrets or protected records | Scoped evidence references, access control, redaction and retention policy | Redaction may reduce later reconstruction fidelity |

## Detailed semantic failure in the warehouse example

The constructed warehouse scenario uses `ReturnItem` and an ordinary-return capability that prepares dispatch. A company-defined policy requires an independent handling clearance and holds unassessed exceptions. An intake record reports a damaged battery in a returned device. The record is evidence of a report, not a confirmed condition or a clearance. OPERATE preserves the observation and holds the affected dispatch while IMPROVE investigates the missing distinction and workflow.

A competing proposal introduces `DamagedBatteryReturn ⊑ ReturnItem` and retains the ordinary dispatch capability, claiming that the addition is harmless. RDF parsing can succeed, selected logical checks can find no contradiction, and the test knowledge graph can meet its shapes. A separate differential fixture contains `DamagedBatteryReturn(x)` without asserting `ReturnItem(x)`; the subclass axiom newly routes that case into the ordinary-return path. The observed device was already a return item, so this fixture isolates the additional entailment effect rather than claiming that the same device gains its original classification.

Dependency analysis identifies the broad return-item handler, dispatch routing and clearance policy. A regression case requires designated specialist review and a hold pending explicit clearance, while the retained ordinary path proposes proceeding. Routing eligibility has increased; the independent clearance guard still prevents the prohibited dispatch. The gate rejects or holds the candidate because syntactic validity and additive axioms have not established compatibility. If a faulty implementation treats category membership as clearance or bypasses the guard, an effect could occur outside the stated enforcement assumptions.

The revised candidate models `DamagedBatteryReturn`, `HandlingAssessment` and an assessment relation, and develops the specialist-review handoff. The capability keeps dispatch on hold until the independent service supplies an explicit clearance within the approved authority envelope. An unconstrained proposal generator might instead remove the clearance precondition or weaken the evaluator's expected outcome to pass the case. Those are consequential capability/evaluator/authority changes; the candidate cannot authorize them by editing its own tests. This example defines hypothetical company workflow rules and makes no claim about an actual handling procedure.

## Open questions and falsification opportunities

- Can semantic dependency analysis detect changed procedure or authority applicability at acceptable false-positive/false-negative rates for a bounded ontology profile?
- Which projections preserve the inferences needed for a capability, and can their sufficiency be checked rather than assumed?
- What is the cost of pinned semantic queries, migration validation and independent gates compared with an ordinary versioned configuration workflow?
- Does report taxonomy improve diagnosis and reduce unnecessary schema changes, or simply relocate uncertainty to IMPROVE?
- How should operational continuity be balanced against suspending affected domains after unknown or contradictory observations?
- Which stateful workflows can survive ontology upgrades or recovery without losing meaning or repeating effects?
- Can an independently controlled authority boundary remain effective when candidates change models, prompts, adapters, facts and evaluator requests together?
- Does the additional semantic bundle materially improve incident reconstruction when providers cannot retain old model versions and evidence must be redacted?

The proposed model would be weakened if a conventional MAPE-K/GitOps design with explicit versioned knowledge and independent policy gates provides the same behavior at lower complexity. It would also be weakened if semantic impact checks systematically miss authority changes, or if maintaining compatible state dominates any operational benefit. Those comparisons belong in a future prototype and controlled failure-injection study.

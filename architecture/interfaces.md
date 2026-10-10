# Typed handoffs and operational contracts

The JSON Schemas in [`../schemas`](../schemas) use Draft 2020-12 and specify structural constraints for a proposed interface. Schema validity does not prove that evidence is true, digests resolve, identities are authorized, semantic impact analysis is complete, or a migration is safe. Implementations must perform those checks separately.

Artifact digest values identify retained byte content with SHA-256. Domain identifiers, correlation identifiers, workflow identifiers and proposal identifiers are opaque stable strings. Wall-clock timestamps support expiration and provenance; lifecycle order comes from control revisions and durable events. Clock assumptions and acceptable skew must be explicit for expiring approvals/leases.

## Contracts

| Contract | Producer → consumer | Meaning |
|---|---|---|
| `OntologyMismatchReport` | OPERATE → orchestration/IMPROVE | Pinned execution context, raw observation reference, evidence, provisional taxonomy, failed concepts/procedures and consequence |
| `OntologyChangeProposal` | IMPROVE → orchestration/gate | Base/candidate snapshot, semantic diff, rationale, dependencies, compatibility, authority delta and unresolved questions |
| `DevelopmentWorkOrder` | Orchestration → DEVELOP | Exact semantic candidate, development-only approval, isolated environment, bounded tools/budget and required outputs |
| `OperatingBundleManifest` | DEVELOP/registry → evaluation/deployment | Complete immutable binding of semantics, executable behavior, policy, tools, evaluations, configuration and state/recovery artifacts |
| `ValidationEvidence` | Evaluation service → approval gateway | Exact candidate and inputs, evaluator build, scoped checks/results, unknowns, retained report and expiry |
| `LifecycleApproval` | Independent approval gateway → orchestration/controller | Exact candidate/domain, base/revision precondition, gate-policy version, evidence, grants, approver and validity interval |
| `LifecycleEvent` | Control services → durable event history | Authorized transition, expected/new revision, aggregate/correlation identity, referenced context and payload digest |
| `DeploymentRecord` | Controller → runtimes/action gateways/audit | Approved bundle, monotone epoch, compatible state epoch, approval reference and predecessor context |
| `DecisionRecord` | Trusted runtime/action gateway → audit | Attested binding, authenticated principal, actual evidence read view/state revision, policy receipt, action-time freshness revalidation and observed/uncertain outcome |

Development authorization and production approval have different `approval_kind` values. A consumer must check that the kind matches the requested transition, and check domain, candidate digest, evidence validity, base/revision, expiry and issuer. Structural schemas cannot express these cross-document trust checks.

Execution context is supplied or attested by a trusted runtime and independently checked by the action gate. An LLM's self-reported bundle ID, ontology version or principal is insufficient. A `runtime_attestation` reference identifies a runtime-produced binding receipt; the proposal does not claim hardware attestation or a cryptographic verifier implementation. `AuthenticationMetadata` and `AuthenticatedEnvelope` define sidecar metadata for authenticated transport, trusted registry records or detached signatures over exact retained payload bytes. Receivers must verify issuer, trust, signature/transport, coverage and payload equality independently. Payload schemas remain separate from envelopes to avoid self-referential hashes.

## Suggested operations

These are illustrative API shapes, not implemented endpoints.

```text
POST /domains/{domain}/mismatch-reports
  body: OntologyMismatchReport; Idempotency-Key: report_id
  result: report_id, accepted_event_id, lifecycle_revision, disposition

POST /proposals
  body: OntologyChangeProposal; Idempotency-Key: proposal_id/revision
  result: immutable proposal reference, lifecycle state/revision

GET /semantic-snapshots/{digest}
  result: verified manifest with full pinned import closure

POST /semantic-snapshots/{digest}/query
  body: query artifact/text, projection scope, entailment mode,
        domain_id, bundle_digest, knowledge snapshot or consistency mode
  result: answer, semantic_snapshot_digest, knowledge_read_view,
          projection_scope, closure/completeness qualifications

POST /proposals/{id}/development-authorizations
  body: exact candidate digest, isolated scope, budget, expected revision
  result: development-kind LifecycleApproval or structured refusal

POST /bundles/{digest}/evaluations
  body: evaluation-plan digest, input snapshot refs, expected candidate
  result: run id; later immutable ValidationEvidence

POST /proposals/{id}/production-approvals
  body: bundle digest, evidence refs, domain, base/revision precondition
  result: production-kind LifecycleApproval or refusal/findings

POST /domains/{domain}/deployments
  body: bundle digest, approval ref, expected bundle/control revision,
        prepared state epoch, idempotency key
  result: DeploymentRecord or conflict/recovery-required result

POST /domains/{domain}/actions
  body: principal, action, target, context, critical read-view,
        authorization evidence, idempotency key
  result: permitted-and-recorded outcome, denial, or uncertain-effect state
```

Reject malformed, unresolved or cross-domain references. Return a conflict when the expected revision/base no longer matches, a policy denial for insufficient authority, and a recovery-required status for ambiguous state/effects. Retrying with the same idempotency key returns the known outcome or resumes the same operation; it must not silently create a second consequential effect.

A semantic query answer records whether it reflects an exact knowledge snapshot, a transaction/read watermark, or a weaker freshness guarantee. Consumers cannot infer a stable fact read from an ontology version alone. For actions whose eligibility can change, enforce critical fact checks at execution or reserve the relevant state under a specified protocol.

`DecisionRecord` records the evidence actually read, its state revision/read view and maximum allowed staleness. `freshness_revalidation` identifies critical inputs, the execution-time state revision and the receiving resource's check/reservation receipt. Compatibility of a state schema with a bundle is a separate property from freshness of the facts used to authorize an action. A structurally valid `pass` receipt is still only a claim until verified against the trusted resource.

## Report taxonomy and provisional interpretations

`mismatch_categories` is a nonempty array of `missing_fact`, `unknown_entity`, `contradictory_observation`, `constraint_violation`, `schema_gap`, `procedure_gap`, or `unclassified`. It may contain several provisional diagnoses. A required clearance or other failed validation condition can be a `constraint_violation` without implying a conceptual gap. `schema_gap` corresponds to the paper's suspected conceptual gap. `unclassified` permits a challenge whose diagnosis is not yet expressible or established; raw evidence and a free-text explanation remain admissible without invented failed concepts or procedures. The diagnostic labels are not asserted domain truth or a claim that every future discrepancy fits a known class.

`diagnosis_status` is always `provisional` when OPERATE produces the report. `provisional_interpretation` is optional and kept distinct from asserted knowledge. A confidence score is optional and does not convert the report into a verified conceptual claim. The `unclassified-mismatch-report.json` fixture and targeted checks illustrate this reporting route; a separate check admits constraint violations without forcing `schema_gap`.

The report's operational disposition identifies whether affected work continued, was suspended or escalated, and links the independently approved rule used to make that decision. It does not grant new action authority. Evidence is referenced by digest/location rather than forced into unrestricted message payloads.

## Event delivery and retention

Every accepted command produces a durable event before downstream work can advance the lifecycle. An event records the authenticated producer principal and payload digest; authentication/signature checks are outside JSON Schema. Deduplicate event IDs and command idempotency keys, and reject conflicting payloads under the same identity. Use expected revisions to serialize aggregate transitions; duplicate delivery of an already committed event is not a fresh transition.

Retention includes raw/canonical artifacts, required imported documents, evaluator builds, actual model outputs, evidence access controls and versioned event schemas. A digest without retained bytes supports identity checking but not reconstruction. Retention periods and lawful redactions can limit forensic replay; record those limits.

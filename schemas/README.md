# Proposed lifecycle message contracts

The eleven JSON Schema files specify payload structure using Draft 2020-12. The common definitions include sidecar authenticated envelopes and signature metadata. No orchestration service, approval gateway, attestation verifier or signature-verification implementation is supplied.

Fixtures in `fixtures/` are illustrative documents. Some artifact references identify other fixture files by their actual byte digest; evidence, capabilities, runtime attestations and signatures otherwise use explicit `fixture:` placeholders. They are not proof that a build, evaluation, approval, deployment or action happened. No fixture is suitable for production authorization.

`test_contracts.py` checks meta-schema validity, representative payloads and meaningful structural rejection cases. It also demonstrates that well-formed changed candidate digests and expired approval timestamps remain structurally valid and require independent runtime checks. An attestation field or authenticated envelope must be authenticated and bound to the consumed payload by the receiving service; an LLM can invent syntactically valid claims.

Reports include an explicit `unclassified` route when the current diagnosis taxonomy cannot adequately label an observation. The targeted fixture preserves raw evidence without requiring a failed concept, failed procedure or invented interpretation. `constraint_violation` separately identifies failures such as a missing required clearance; it does not force the conclusion that the ontology lacks a concept. All report diagnoses remain provisional.

Run with a Python environment containing `jsonschema`:

```sh
python3 schemas/test_contracts.py
```

The documented check used `jsonschema==4.26.0`, pinned in `requirements-contracts.txt` and installed in a temporary validation directory. These checks concern document contracts and fixture-byte integrity only; they are not architecture implementation or empirical validation.

For review, distinguish these obligations:

| Layer | Example obligation | Supplied evidence |
|---|---|---|
| JSON structure | Digest syntax; required pinned bindings; allowed report taxonomy; freshness receipt structure | Schemas and contract checks |
| Cross-document binding | Approval candidate matches bundle; semantic descriptor matches bundle; prepared state matches deployment | Contract requirement; fixtures illustrate fields |
| Authentication | Trusted runtime supplied context; principal/issuer is verified; signature covers exact bytes | Metadata structure only |
| Time and concurrency | Approval not expired; base/revision current; epoch active; critical facts revalidated at resource | Design obligations only |
| Semantic correctness | Impact analysis and authority delta adequate; evidence true; migration compatible | Design obligations and proposed future study |

Payloads avoid self-hashes. Retained canonical payload bytes receive an external `ArtifactRef`; sidecar authentication covers those bytes under a versioned coverage specification. An envelope's `covered_artifact` must match its `payload`, but JSON Schema alone does not establish that cross-document equality or validate signatures.

Domain control revisions, proposal lifecycle revisions, and immutable proposal/candidate revision numbers are separate counters. Consumers must enforce the relevant ordering and binding. State-schema compatibility does not imply current fact eligibility: `DecisionRecord` records actual evidence reads and action-time freshness checks separately.

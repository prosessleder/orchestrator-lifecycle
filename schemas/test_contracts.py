"""Document-contract checks only; this does not implement an orchestrator or gate.

Requires jsonschema >= 4 with Draft 2020-12 support. Fixtures contain illustrative
placeholder evidence and signatures. These tests cannot authenticate them.
"""

import copy
import hashlib
import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


HERE = Path(__file__).resolve().parent
SCHEMAS = {}
for path in HERE.glob("*.schema.json"):
    document = json.loads(path.read_text())
    # Local resource identities permit offline resolution without publishing a
    # schema hostname. These IDs are validator inputs, not edits to the schemas.
    document["$id"] = path.as_uri()
    SCHEMAS[path.name] = document
REGISTRY = Registry().with_resources(
    (document["$id"], Resource.from_contents(document))
    for document in SCHEMAS.values()
)


def fixture(name):
    return json.loads((HERE / "fixtures" / name).read_text())


def validator(name):
    return Draft202012Validator(
        SCHEMAS[name], registry=REGISTRY, format_checker=FormatChecker()
    )


class ContractTests(unittest.TestCase):
    def test_local_fixture_artifact_digests_match_bytes(self):
        def inspect(value):
            if isinstance(value, dict):
                locator = value.get("locator", "")
                if locator.startswith("fixtures/"):
                    retained_bytes = (HERE / locator).read_bytes()
                    self.assertEqual(value["sha256"], "sha256:" + hashlib.sha256(retained_bytes).hexdigest())
                for child in value.values():
                    inspect(child)
            elif isinstance(value, list):
                for child in value:
                    inspect(child)

        for path in (HERE / "fixtures").glob("*.json"):
            inspect(json.loads(path.read_text()))

    def test_all_schemas_satisfy_draft_2020_12_meta_schema(self):
        for name, document in SCHEMAS.items():
            with self.subTest(schema=name):
                Draft202012Validator.check_schema(document)

    def test_representative_payloads_validate(self):
        names = [
            "semantic-snapshot",
            "ontology-mismatch-report",
            "ontology-change-proposal",
            "operating-bundle-manifest",
            "validation-evidence",
            "lifecycle-approval",
            "development-work-order",
            "deployment-record",
            "decision-record",
        ]
        for name in names:
            with self.subTest(contract=name):
                validator(name + ".schema.json").validate(fixture(name + ".json"))
        validator("lifecycle-approval.schema.json").validate(
            fixture("development-approval.json")
        )

    def test_malformed_digest_is_rejected(self):
        value = fixture("ontology-mismatch-report.json")
        value["context"]["bundle_digest"] = "sha256:not-a-digest"
        self.assertFalse(validator("ontology-mismatch-report.schema.json").is_valid(value))

    def test_missing_semantic_and_policy_bindings_are_rejected(self):
        for field in ["semantic_snapshot", "authority_policy", "instructions"]:
            value = fixture("operating-bundle-manifest.json")
            del value[field]
            with self.subTest(field=field):
                self.assertFalse(validator("operating-bundle-manifest.schema.json").is_valid(value))
        value = fixture("semantic-snapshot.json")
        del value["reasoner_configuration"]
        self.assertFalse(validator("semantic-snapshot.schema.json").is_valid(value))

    def test_production_approval_cannot_be_development_candidate(self):
        value = fixture("lifecycle-approval.json")
        value["candidate_kind"] = "semantic_snapshot"
        self.assertFalse(validator("lifecycle-approval.schema.json").is_valid(value))

    def test_self_reported_context_is_rejected(self):
        value = fixture("decision-record.json")
        value["context"]["context_origin"] = "llm_self_report"
        self.assertFalse(validator("decision-record.schema.json").is_valid(value))

    def test_unclassified_report_without_forced_concept_is_admitted(self):
        # Novelty may challenge the diagnostic taxonomy itself. Raw evidence
        # must remain reportable without inventing a failed concept/procedure
        # or asserting a provisional interpretation to satisfy the contract.
        value = fixture("unclassified-mismatch-report.json")
        self.assertEqual(value["mismatch_categories"], ["unclassified"])
        self.assertEqual(value["failed_concepts"], [])
        self.assertEqual(value["insufficient_procedure_refs"], [])
        self.assertNotIn("provisional_interpretation", value)
        validator("ontology-mismatch-report.schema.json").validate(value)

    def test_constraint_violation_does_not_require_a_schema_gap(self):
        value = fixture("ontology-mismatch-report.json")
        value["mismatch_categories"] = ["constraint_violation"]
        value["failed_concepts"] = []
        value["explanation"] = "Required affected-asset authorization is absent."
        validator("ontology-mismatch-report.schema.json").validate(value)

    def test_permitted_consequential_action_requires_freshness_receipt(self):
        value = fixture("decision-record.json")
        value["freshness_revalidation"]["result"] = "fail"
        self.assertFalse(validator("decision-record.schema.json").is_valid(value))
        value = fixture("decision-record.json")
        value["freshness_revalidation"]["mode"] = "no_consequential_action"
        self.assertFalse(validator("decision-record.schema.json").is_valid(value))

    def test_sidecar_signature_structure(self):
        envelope_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$ref": SCHEMAS["common.schema.json"]["$id"] + "#/$defs/AuthenticatedEnvelope",
        }
        envelope_validator = Draft202012Validator(envelope_schema, registry=REGISTRY)
        value = fixture("authenticated-envelope.json")
        envelope_validator.validate(value)
        del value["authentication"]["signature_artifact"]
        self.assertFalse(envelope_validator.is_valid(value))

    def test_changed_candidate_is_a_service_level_obligation(self):
        original = fixture("lifecycle-approval.json")
        changed = copy.deepcopy(original)
        changed["candidate"]["sha256"] = "sha256:" + "f" * 64
        # A syntactically valid digest does not establish candidate binding.
        validator("lifecycle-approval.schema.json").validate(changed)
        self.assertNotEqual(changed["candidate"]["sha256"], original["candidate"]["sha256"])

    def test_expiration_is_a_service_level_obligation(self):
        value = fixture("lifecycle-approval.json")
        value["valid_until"] = "2000-01-01T00:00:00Z"
        # Schema checks the timestamp's representation; the gate checks the time.
        validator("lifecycle-approval.schema.json").validate(value)
        expires = datetime.fromisoformat(value["valid_until"].replace("Z", "+00:00"))
        reference_time = datetime(2026, 10, 10, tzinfo=timezone.utc)
        self.assertLess(expires, reference_time)


if __name__ == "__main__":
    unittest.main(verbosity=2)

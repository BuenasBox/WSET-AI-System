"""Tests for the Phase 4A.3.5 Diagnostic Outcome JSON Schema."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMA_PATH = (
    Path(__file__).parents[1]
    / "knowledge"
    / "enrichment"
    / "diagnostic_outcome.schema.json"
)


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def valid_outcome() -> dict:
    return {
        "schema_version": "diagnostic_outcome_v1",
        "identity": {
            "outcome_id": "outcome_001",
            "item_id": "item_001",
            "attempt_id": "attempt_001",
            "outcome_version": "1.0.0",
            "generated_by": "phase_4a3_5_schema_fixture",
            "training_diagnostic_only": True,
        },
        "attempt_observation": {
            "selected_option_id": "B",
            "is_correct": False,
            "response_time_ms": 18000,
            "answer_changed": True,
            "confidence_self_report": "high",
            "hesitation_flag": True,
        },
        "diagnostic_classification": {
            "diagnosed_error_type": "misconception_reinforced",
            "confidence_alignment": "overconfident_wrong",
        },
        "source_trace": {
            "item_source_ids": ["CC_SCHEMA_EXAMPLE"],
            "selected_option_diagnostic_role": "misconception",
            "misconception_id": "MC_SCHEMA_EXAMPLE",
            "causal_chain_id": "CC_SCHEMA_EXAMPLE",
            "sat_relevance": ["acidity"],
            "topic": "viticulture",
            "subtopic": "climate_and_acidity",
            "ra_id": "RA1",
        },
        "timing_interpretation": {
            "timing_band": "slow",
            "timing_interpretation": "hesitation",
        },
        "remediation_routing": {
            "recommended_next_action": "review_misconception",
            "remediation_target_type": "misconception",
            "remediation_target_id": "MC_SCHEMA_EXAMPLE",
            "feedback_priority": "high",
        },
        "learner_state_effect_placeholders": {
            "mastery_signal": "Suggest later review of topic confidence.",
            "confidence_signal": "High confidence on a wrong answer suggests mismatch.",
            "retention_signal": None,
            "misconception_signal": "Possible misconception reinforcement.",
            "recommended_ledger_event": "diagnostic_sba_misconception_signal",
        },
        "governance": {
            "safe_for_examiner": False,
            "examiner_scoring_allowed": False,
            "official_wset_score": False,
            "training_diagnostic_only": True,
            "uses_llm": False,
            "uses_api": False,
            "uses_embeddings": False,
            "uses_vector_db": False,
            "cloud_services_active": False,
        },
    }


class DiagnosticOutcomeSchemaTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_schema()
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def assertValid(self, outcome: dict) -> None:
        errors = sorted(self.validator.iter_errors(outcome), key=lambda err: list(err.path))
        self.assertEqual(errors, [], [error.message for error in errors])

    def assertInvalid(self, outcome: dict) -> None:
        errors = sorted(self.validator.iter_errors(outcome), key=lambda err: list(err.path))
        self.assertGreater(len(errors), 0, "Expected schema validation errors.")


class TestDiagnosticOutcomeSchema(DiagnosticOutcomeSchemaTestCase):
    def test_valid_diagnostic_outcome_passes(self) -> None:
        self.assertValid(valid_outcome())

    def test_missing_identity_fails(self) -> None:
        outcome = valid_outcome()
        del outcome["identity"]
        self.assertInvalid(outcome)

    def test_missing_attempt_observation_fails(self) -> None:
        outcome = valid_outcome()
        del outcome["attempt_observation"]
        self.assertInvalid(outcome)

    def test_invalid_selected_option_id_fails(self) -> None:
        outcome = valid_outcome()
        outcome["attempt_observation"]["selected_option_id"] = "E"
        self.assertInvalid(outcome)

    def test_invalid_diagnosed_error_type_fails(self) -> None:
        outcome = valid_outcome()
        outcome["diagnostic_classification"]["diagnosed_error_type"] = "official_failure"
        self.assertInvalid(outcome)

    def test_invalid_confidence_alignment_fails(self) -> None:
        outcome = valid_outcome()
        outcome["diagnostic_classification"]["confidence_alignment"] = "certain_fail"
        self.assertInvalid(outcome)

    def test_invalid_timing_band_fails(self) -> None:
        outcome = valid_outcome()
        outcome["timing_interpretation"]["timing_band"] = "exam_fail_speed"
        self.assertInvalid(outcome)

    def test_invalid_recommended_next_action_fails(self) -> None:
        outcome = valid_outcome()
        outcome["remediation_routing"]["recommended_next_action"] = "award_marks"
        self.assertInvalid(outcome)

    def test_invalid_remediation_target_type_fails(self) -> None:
        outcome = valid_outcome()
        outcome["remediation_routing"]["remediation_target_type"] = "official_grade"
        self.assertInvalid(outcome)

    def test_unsafe_governance_true_fails(self) -> None:
        outcome = valid_outcome()
        outcome["governance"]["examiner_scoring_allowed"] = True
        self.assertInvalid(outcome)

    def test_official_scoring_field_rejected(self) -> None:
        outcome = valid_outcome()
        outcome["official_score"] = 88
        self.assertInvalid(outcome)

    def test_pass_fail_field_rejected(self) -> None:
        outcome = valid_outcome()
        outcome["pass_fail"] = "pass"
        self.assertInvalid(outcome)

    def test_certification_wording_rejected(self) -> None:
        outcome = valid_outcome()
        outcome["learner_state_effect_placeholders"]["recommended_ledger_event"] = (
            "certification readiness achieved"
        )
        self.assertInvalid(outcome)

    def test_learner_state_fields_are_placeholders_only(self) -> None:
        outcome = valid_outcome()
        placeholders = outcome["learner_state_effect_placeholders"]
        self.assertEqual(
            set(placeholders),
            {
                "mastery_signal",
                "confidence_signal",
                "retention_signal",
                "misconception_signal",
                "recommended_ledger_event",
            },
        )
        placeholders["official_score"] = "not allowed"
        self.assertInvalid(outcome)

    def test_schema_requires_training_diagnostic_only_true(self) -> None:
        outcome = valid_outcome()
        outcome["identity"]["training_diagnostic_only"] = False
        self.assertInvalid(outcome)
        outcome = valid_outcome()
        outcome["governance"]["training_diagnostic_only"] = False
        self.assertInvalid(outcome)

    def test_no_examiner_authority_allowed(self) -> None:
        outcome = valid_outcome()
        outcome["learner_state_effect_placeholders"]["confidence_signal"] = (
            "examiner judgment says this is complete"
        )
        self.assertInvalid(outcome)


if __name__ == "__main__":
    unittest.main()

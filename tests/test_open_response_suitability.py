from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.question_generation.master_bank import MASTER_BANK_PATH, SAFE_GOVERNANCE
from tools.question_generation.open_response_suitability import (
    CLASSIFICATIONS,
    OUTPUT_PATH,
    build_open_response_suitability_report,
    classify_open_response_suitability,
    validate_open_response_suitability_report,
    write_open_response_suitability_report,
)


ROOT = Path(__file__).resolve().parents[1]


class OpenResponseSuitabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bank = json.loads((ROOT / MASTER_BANK_PATH).read_text(encoding="utf-8"))
        cls.report = build_open_response_suitability_report(cls.bank)
        cls.persisted = json.loads((ROOT / OUTPUT_PATH).read_text(encoding="utf-8"))
        cls.by_source = {
            item["source_question_id"]: item for item in cls.bank["items"]
        }
        cls.result_by_source = {
            item["source_question_id"]: item for item in cls.report["records"]
        }

    def test_report_covers_all_616_records_without_quota(self) -> None:
        self.assertEqual(self.report["record_count"], 616)
        self.assertIsNone(self.report["quota_target"])
        self.assertEqual(sum(self.report["classification_counts"].values()), 616)
        self.assertEqual(
            set(self.report["classification_counts"]), set(CLASSIFICATIONS)
        )

    def test_shadow_classification_counts(self) -> None:
        self.assertEqual(
            self.report["classification_counts"],
            {
                "open_response_candidate": 27,
                "human_review_required": 0,
                "sba_only": 589,
                "inactive": 0,
            },
        )

    def test_existing_approved_open_response_records_remain_candidates(self) -> None:
        approved = [
            item
            for item in self.bank["items"]
            if item["status"]["review_state"] == "approved_open_response"
        ]
        self.assertEqual(len(approved), 26)
        self.assertTrue(
            all(
                self.result_by_source[item["source_question_id"]][
                    "open_response_candidate"
                ]
                for item in approved
            )
        )

    def test_q14_is_new_strong_candidate_from_cognitive_signals(self) -> None:
        result = self.result_by_source["14"]
        self.assertEqual(result["classification"], "open_response_candidate")
        self.assertFalse(result["sba_eligible"])
        self.assertTrue(result["signals"]["requires_explanation"])
        self.assertTrue(result["signals"]["requires_causal_chain"])
        self.assertTrue(result["signals"]["answer_boundary_support"])
        self.assertEqual(result["confidence"], "high")

    def test_reviewed_explanation_sba_is_finalized_as_sba(self) -> None:
        result = self.result_by_source["19"]
        self.assertEqual(result["classification"], "sba_only")
        self.assertTrue(result["signals"]["requires_explanation"])
        self.assertFalse(result["signals"]["answer_boundary_support"])
        self.assertEqual(result["confidence"], "high")

    def test_recognition_question_remains_sba_only(self) -> None:
        result = self.result_by_source["2"]
        self.assertEqual(result["classification"], "sba_only")
        self.assertTrue(result["sba_only"])
        self.assertTrue(result["sba_eligible"])
        self.assertTrue(result["signals"]["recognition_only_sufficient"])

    def test_public_review_exceptions_are_resolved_and_remain_sba_eligible(self) -> None:
        public_review = [
            self.result_by_source[source_id]
            for source_id in ("356", "421", "464")
        ]
        self.assertTrue(
            all(record["classification"] == "sba_only" for record in public_review)
        )
        self.assertTrue(all(record["sba_eligible"] for record in public_review))

    def test_no_inactive_suitability_backlog_remains(self) -> None:
        inactive = [
            record
            for record in self.report["records"]
            if record["classification"] == "inactive"
        ]
        self.assertEqual(inactive, [])

    def test_comparison_and_justification_signals_are_detected(self) -> None:
        comparison = self.result_by_source["805"]
        justification = self.result_by_source["799"]
        self.assertTrue(comparison["signals"]["requires_comparison"])
        self.assertTrue(justification["signals"]["requires_justification"])

    def test_report_is_deterministic_and_pure(self) -> None:
        before = copy.deepcopy(self.bank)
        second = build_open_response_suitability_report(copy.deepcopy(self.bank))
        self.assertEqual(self.report, second)
        self.assertEqual(self.bank, before)

    def test_persisted_report_matches_generated_report(self) -> None:
        self.assertEqual(self.persisted, self.report)
        self.assertEqual(validate_open_response_suitability_report(self.persisted), [])

    def test_report_does_not_activate_runtime_or_public_lab(self) -> None:
        integration = self.report["integration"]
        self.assertFalse(integration["runtime_active"])
        self.assertFalse(integration["master_bank_rewritten"])
        self.assertFalse(integration["public_lab_changed"])
        self.assertFalse(integration["open_response_runtime_changed"])

    def test_governance_is_safe_at_report_and_record_level(self) -> None:
        self.assertEqual(self.report["governance"], SAFE_GOVERNANCE)
        self.assertTrue(
            all(record["governance"] == SAFE_GOVERNANCE for record in self.report["records"])
        )
        self.assertTrue(
            all(record["activation_status"] == "inactive" for record in self.report["records"])
        )

    def test_validator_rejects_quota_and_activation(self) -> None:
        invalid = copy.deepcopy(self.report)
        invalid["quota_target"] = 116
        invalid["records"][0]["activation_status"] = "active"
        errors = validate_open_response_suitability_report(invalid)
        self.assertIn("quota_target must remain null", errors)
        self.assertTrue(any("activation_status must be inactive" in error for error in errors))

    def test_write_round_trip_uses_explicit_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = write_open_response_suitability_report(
                self.report,
                path=Path("knowledge/report.json"),
                root=tmp,
            )
            loaded = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(loaded, self.report)


if __name__ == "__main__":
    unittest.main()

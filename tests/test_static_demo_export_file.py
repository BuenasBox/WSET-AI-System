from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.question_generation.export_static_demo_questions import assert_allowed_output_path
from tools.question_generation.static_demo_exporter import (
    SAFE_ITEM_GOVERNANCE,
    validate_static_demo_export_payload,
)


EXPORT_PATH = Path("frontend/diagnostic-sba/preguntas.json")
DRAFTS_PATH = Path("knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json")
REVIEWS_PATH = Path("knowledge/question-bank/diagnostic_sba/reviews/first_5_human_review_records.json")
FRONTEND_INDEX_PATH = Path("frontend/diagnostic-sba/index.html")
EXPECTED_SOURCE_IDS = [
    "2",
    "21",
    "83",
    "105",
    "107",
    "206",
    "216",
    "228",
    "230",
    "232",
    "240",
    "258",
    "265",
    "268",
    "269",
    "270",
    "277",
    "287",
    "301",
    "308",
    "309",
    "325",
    "356",
    "395",
    "402",
    "421",
    "424",
    "438",
    "440",
    "441",
    "464",
    "493",
    "498",
    "515",
    "659",
    "834",
]
FORBIDDEN_AUTHORITY_PHRASES = (
    "approved_for_production",
    "official score",
    "official wset score",
    "pass/fail",
    "certification readiness",
    "examiner authority",
    "examiner_scoring_allowed\": true",
    "safe_for_examiner\": true",
)


def load_export_payload() -> dict:
    with EXPORT_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise AssertionError("static demo export must be a JSON object")
    return data


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


class StaticDemoExportFileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = load_export_payload()

    def test_frontend_preguntas_json_exists(self) -> None:
        self.assertTrue(EXPORT_PATH.exists())

    def test_payload_validates(self) -> None:
        self.assertEqual(validate_static_demo_export_payload(self.payload), [])

    def test_contains_exactly_thirty_six_items(self) -> None:
        self.assertEqual(len(self.payload["items"]), 36)

    def test_item_ids_match_gold_bank_target_set(self) -> None:
        self.assertEqual([item["source_question_id"] for item in self.payload["items"]], EXPECTED_SOURCE_IDS)

    def test_historical_non_gold_ids_absent(self) -> None:
        selected_ids = {item["source_question_id"] for item in self.payload["items"]}

        for source_id in ("1", "4", "5", "12", "13", "15", "17", "20", "30", "44", "50", "78", "87", "108", "247", "253", "386", "510"):
            self.assertNotIn(source_id, selected_ids)

    def test_items_have_no_correctness_leakage(self) -> None:
        render_text = self._render_text()

        self.assertNotIn("correct_option_id", render_text)
        self.assertNotIn("correct_answer", render_text)
        self.assertNotIn("is_correct", render_text)

    def test_items_have_no_diagnostic_role_leakage(self) -> None:
        render_text = self._render_text()

        self.assertNotIn("diagnostic_role", render_text)
        self.assertNotIn("diagnostic_note", render_text)
        self.assertNotIn("misconception_id", render_text)

    def test_items_have_no_rationale_or_remediation_leakage(self) -> None:
        render_text = self._render_text().lower()

        self.assertNotIn("rationale", render_text)
        self.assertNotIn("feedback", render_text)
        self.assertNotIn("why_other_options_are_wrong", render_text)
        self.assertNotIn("remediation", render_text)
        self.assertNotIn("causal_chain", render_text)

    def test_outcomes_by_item_id_exists_and_contains_matching_ids(self) -> None:
        outcome_ids = set(self.payload["outcomes_by_item_id"])
        render_ids = {item["item_id"] for item in self.payload["items"]}

        self.assertEqual(outcome_ids, render_ids)
        for outcome in self.payload["outcomes_by_item_id"].values():
            self.assertIn("correct_option_id", outcome)
            self.assertIn("option_diagnostics", outcome)

    def test_governance_flags_safe(self) -> None:
        self.assertTrue(self.payload["static_demo_only"])
        for item in self.payload["items"]:
            self.assertEqual(item["governance"], SAFE_ITEM_GOVERNANCE)
            self.assertTrue(item["training_item_only"])
            self.assertTrue(item["static_demo_only"])
            self.assertFalse(item["official_wset_question"])
            self.assertFalse(item["safe_for_examiner"])
            self.assertFalse(item["examiner_scoring_allowed"])
        for outcome in self.payload["outcomes_by_item_id"].values():
            self.assertEqual(outcome["governance"], SAFE_ITEM_GOVERNANCE)

    def test_deterministic_ordering(self) -> None:
        self.assertEqual(self.payload["export_metadata"]["source_question_ids"], EXPECTED_SOURCE_IDS)
        self.assertEqual([item["source_question_id"] for item in self.payload["items"]], EXPECTED_SOURCE_IDS)

    def test_no_production_fields(self) -> None:
        text = json.dumps(self.payload, ensure_ascii=False).lower()

        self.assertNotIn("approved_for_production", text)
        self.assertNotIn("\"production\"", text)

    def test_no_official_examiner_certification_claims(self) -> None:
        text = json.dumps(self.payload, ensure_ascii=False).lower()

        for phrase in FORBIDDEN_AUTHORITY_PHRASES:
            self.assertNotIn(phrase, text)

    def test_source_drafts_and_review_files_unchanged_by_file_validation(self) -> None:
        drafts_before = copy.deepcopy(load_json(DRAFTS_PATH))
        reviews_before = copy.deepcopy(load_json(REVIEWS_PATH))

        load_export_payload()
        validate_static_demo_export_payload(self.payload)

        self.assertEqual(load_json(DRAFTS_PATH), drafts_before)
        self.assertEqual(load_json(REVIEWS_PATH), reviews_before)

    def test_no_frontend_html_modified(self) -> None:
        before = FRONTEND_INDEX_PATH.read_text(encoding="utf-8")

        load_export_payload()

        self.assertEqual(FRONTEND_INDEX_PATH.read_text(encoding="utf-8"), before)

    def test_cli_dry_run_does_not_modify_export_file(self) -> None:
        before = EXPORT_PATH.read_text(encoding="utf-8")

        result = subprocess.run(
            [sys.executable, "-m", "tools.question_generation.export_static_demo_questions", "--dry-run"],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn("eligible_item_count: 36", result.stdout)
        self.assertEqual(EXPORT_PATH.read_text(encoding="utf-8"), before)

    def test_cli_rejects_output_path_outside_frontend_diagnostic_sba(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            outside = Path(temp_dir) / "preguntas.json"
            with self.assertRaises(ValueError):
                assert_allowed_output_path(outside)

    def _render_text(self) -> str:
        return json.dumps(self.payload["items"], ensure_ascii=False)


if __name__ == "__main__":
    unittest.main()

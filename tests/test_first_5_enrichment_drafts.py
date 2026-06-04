from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools.question_generation.diagnostic_sba_validator import validate_diagnostic_sba_item


DRAFTS_PATH = Path("knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json")
SOURCE_BANK_PATH = Path("knowledge/question-bank/structured/wset3_questions.json")
EXPECTED_SOURCE_IDS = [
    "1",
    "2",
    "12",
    "13",
    "15",
    "17",
    "20",
    "30",
    "44",
    "50",
    "83",
    "108",
    "247",
    "253",
    "4",
    "5",
    "78",
    "87",
    "386",
    "510",
]
EXPECTED_ENRICHMENT_VERSIONS = {
    "first_5_enrichment_draft_v0",
    "phase_4a3_7_27_batch_1_v0",
    "phase_4a3_7_29_batch_2_v0",
}
SAFE_GOVERNANCE = {
    "safe_for_examiner": False,
    "examiner_scoring_allowed": False,
    "official_wset_question": False,
    "training_item_only": True,
    "uses_llm": False,
    "uses_api": False,
    "uses_embeddings": False,
    "uses_vector_db": False,
    "cloud_services_active": False,
}
INCOMPLETE_STATUSES = {
    "source_support_missing",
    "option_diagnostics_missing",
    "rationale_missing",
    "remediation_missing",
    "governance_incomplete",
    "defer_for_human_review",
}
FORBIDDEN_OUTPUT_PATHS = (
    Path("knowledge/question-bank/diagnostic_sba/preguntas.json"),
    Path("knowledge/question-bank/diagnostic_sba/converted"),
    Path("knowledge/question-bank/diagnostic_sba/pilot_bank.json"),
)
FORBIDDEN_AUTHORITY_PHRASES = (
    "official wset question",
    "official wset score",
    "examiner mark",
    "certified result",
    "guaranteed pass",
    "pass/fail",
)


def load_drafts() -> list[dict]:
    with DRAFTS_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise AssertionError("first 5 enrichment drafts must be a list")
    return data


def load_source_bank() -> list[dict]:
    with SOURCE_BANK_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise AssertionError("structured source bank must be a list")
    return data


class FirstFiveEnrichmentDraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.drafts = load_drafts()

    def test_file_exists(self) -> None:
        self.assertTrue(DRAFTS_PATH.exists())

    def test_exactly_twenty_drafts(self) -> None:
        self.assertEqual(len(self.drafts), 20)

    def test_source_question_ids_are_expected(self) -> None:
        ids = [draft["identity"]["source_question_id"] for draft in self.drafts]

        self.assertEqual(ids, EXPECTED_SOURCE_IDS)

    def test_every_draft_has_lineage(self) -> None:
        for draft in self.drafts:
            lineage = draft.get("lineage", {})
            self.assertEqual(lineage.get("source_question_id"), draft["identity"]["source_question_id"])
            self.assertEqual(lineage.get("source_bank_path"), SOURCE_BANK_PATH.as_posix())
            self.assertEqual(lineage.get("adapter_version"), "structured_adapter_v0")
            self.assertIn(lineage.get("enrichment_version"), EXPECTED_ENRICHMENT_VERSIONS)
            self.assertTrue(lineage.get("transformation_notes"))

    def test_every_draft_has_governance_safe_values(self) -> None:
        for draft in self.drafts:
            self.assertEqual(draft.get("governance"), SAFE_GOVERNANCE)

    def test_every_draft_has_human_review_required(self) -> None:
        for draft in self.drafts:
            self.assertIs(draft["human_review"]["required"], True)

    def test_every_draft_has_risk_level(self) -> None:
        for draft in self.drafts:
            self.assertIn(draft["human_review"]["risk_level"], {"low", "medium", "high"})

    def test_no_draft_claims_official_authority(self) -> None:
        for draft in self.drafts:
            text = json.dumps(draft, ensure_ascii=False).lower()
            for phrase in FORBIDDEN_AUTHORITY_PHRASES:
                self.assertNotIn(phrase, text)

    def test_no_draft_has_safe_for_examiner_true(self) -> None:
        for draft in self.drafts:
            self.assertIs(draft["governance"]["safe_for_examiner"], False)

    def test_no_draft_mutates_source_bank(self) -> None:
        source_bank = load_source_bank()
        before = copy.deepcopy(source_bank)

        load_drafts()

        self.assertEqual(source_bank, before)

    def test_no_preguntas_json_is_created(self) -> None:
        self.assertFalse(Path("knowledge/question-bank/diagnostic_sba/preguntas.json").exists())

    def test_no_production_converted_bank_is_created(self) -> None:
        for path in FORBIDDEN_OUTPUT_PATHS:
            if path == DRAFTS_PATH:
                continue
            self.assertFalse(path.exists(), str(path))

    def test_drafts_are_validator_valid_or_explicitly_incomplete(self) -> None:
        for draft in self.drafts:
            errors = validate_diagnostic_sba_item(draft)
            if errors:
                self.assertIn(draft.get("enrichment_status"), INCOMPLETE_STATUSES)
            else:
                self.assertEqual(draft.get("enrichment_status"), "defer_for_human_review")

    def test_option_diagnostics_include_exactly_four_options(self) -> None:
        for draft in self.drafts:
            self.assertEqual(set(draft["options"].keys()), {"A", "B", "C", "D"})
            for key in ("A", "B", "C", "D"):
                self.assertTrue(draft["options"][key].get("diagnostic_role"))

    def test_exactly_one_correct_option_per_draft(self) -> None:
        for draft in self.drafts:
            correct = [key for key, option in draft["options"].items() if option["is_correct"]]
            self.assertEqual(len(correct), 1, draft["identity"]["source_question_id"])
            self.assertEqual(draft["options"][correct[0]]["diagnostic_role"], "correct")


if __name__ == "__main__":
    unittest.main()

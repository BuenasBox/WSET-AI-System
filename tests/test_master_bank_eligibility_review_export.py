from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.question_generation.master_bank import MASTER_BANK_PATH, SAFE_GOVERNANCE
from tools.question_generation.master_bank_eligibility import (
    load_open_response_suitability_index,
)
from tools.question_generation.master_bank_eligibility_review_export import (
    DOCS_OUTPUT_DIR,
    JSON_OUTPUT_PATH,
    build_review_packet,
    validate_review_packet,
    write_review_packet,
)


ROOT = Path(__file__).resolve().parents[1]


class MasterBankEligibilityReviewExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bank = json.loads((ROOT / MASTER_BANK_PATH).read_text(encoding="utf-8"))
        cls.suitability = load_open_response_suitability_index(root=ROOT)
        cls.packet = build_review_packet(cls.bank, cls.suitability)

    def test_packet_counts_and_groups(self) -> None:
        self.assertEqual(
            self.packet["counts"],
            {
                "total_master_bank": 616,
                "inactive": 24,
                "review_pool": 68,
                "public_lab_review_exceptions": 3,
                "inactive_groups": {
                    "truly_inactive": 6,
                    "recoverable": 2,
                    "unclear": 16,
                },
                "review_reason_groups": {
                    "missing_metadata": 0,
                    "possible_open_response": 15,
                    "weak_support": 53,
                    "duplicate_risk": 0,
                    "difficulty_uncertainty": 0,
                    "governance_concern": 0,
                    "other": 0,
                },
            },
        )

    def test_public_exceptions_are_exact_and_sba_eligible(self) -> None:
        records = self.packet["public_lab_review_exceptions"]
        self.assertEqual({record["question_id"] for record in records}, {"356", "421", "464"})
        self.assertTrue(
            all(record["eligibility_flags"]["sba_eligible"] for record in records)
        )

    def test_urgent_cases_are_structurally_invalid_853_to_857(self) -> None:
        self.assertEqual(
            {case["question_id"] for case in self.packet["urgent_cases"]},
            {"853", "854", "855", "856", "857"},
        )

    def test_every_record_has_empty_human_recommendation(self) -> None:
        records = [
            *self.packet["inactive_items"],
            *self.packet["review_pool_items"],
        ]
        self.assertTrue(all(record["recommendation"] is None for record in records))
        self.assertTrue(all(len(record["recommendation_options"]) == 5 for record in records))

    def test_packet_is_deterministic_pure_and_governance_clean(self) -> None:
        before = copy.deepcopy(self.bank)
        second = build_review_packet(copy.deepcopy(self.bank), copy.deepcopy(self.suitability))
        self.assertEqual(self.packet, second)
        self.assertEqual(self.bank, before)
        self.assertEqual(self.packet["governance"], SAFE_GOVERNANCE)
        self.assertEqual(validate_review_packet(self.packet), [])

    def test_write_creates_all_five_requested_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            outputs = write_review_packet(self.packet, root=tmp)
            expected = {
                Path(tmp) / JSON_OUTPUT_PATH,
                Path(tmp) / DOCS_OUTPUT_DIR / "inactive_items_review_packet.md",
                Path(tmp) / DOCS_OUTPUT_DIR / "review_pool_items_review_packet.md",
                Path(tmp) / DOCS_OUTPUT_DIR / "public_lab_review_exceptions.md",
                Path(tmp) / DOCS_OUTPUT_DIR / "master_bank_eligibility_review_summary.md",
            }
            self.assertEqual(set(outputs), expected)
            self.assertTrue(all(path.exists() for path in expected))


if __name__ == "__main__":
    unittest.main()

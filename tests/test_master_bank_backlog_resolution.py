from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

from tools.question_generation.master_bank import MASTER_BANK_PATH, SAFE_GOVERNANCE
from tools.question_generation.master_bank_eligibility import build_eligibility_index
from tools.question_generation.master_bank_resolution import (
    RESOLUTION_PATH,
    load_resolution_index,
)
from tools.question_generation.resolve_master_bank_backlog import (
    build_resolution_artifact,
)


ROOT = Path(__file__).resolve().parents[1]


class MasterBankBacklogResolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.resolution = json.loads((ROOT / RESOLUTION_PATH).read_text(encoding="utf-8"))
        cls.bank = json.loads((ROOT / MASTER_BANK_PATH).read_text(encoding="utf-8"))
        cls.eligibility = build_eligibility_index(cls.bank)

    def test_resolution_artifact_is_deterministic_and_complete(self) -> None:
        self.assertEqual(build_resolution_artifact(ROOT), self.resolution)
        self.assertEqual(self.resolution["record_count"], 92)
        self.assertEqual(len(load_resolution_index(root=ROOT)), 92)
        self.assertEqual(self.resolution["governance"], SAFE_GOVERNANCE)

    def test_all_transitions_are_final_and_recovery_first(self) -> None:
        self.assertEqual(
            self.resolution["transitions"],
            {
                "review_to_sba": 68,
                "review_to_open_response": 0,
                "review_to_quarantine": 0,
                "inactive_to_sba": 18,
                "inactive_to_open_response": 6,
                "inactive_to_quarantine": 0,
            },
        )
        destinations = Counter(
            record["destination"] for record in self.resolution["records"]
        )
        self.assertEqual(destinations, {"sba_operational": 86, "open_response_candidate": 6})
        self.assertTrue(
            all(record["evidence_reviewed"] for record in self.resolution["records"])
        )

    def test_no_review_or_inactive_operational_backlog_remains(self) -> None:
        counts = self.eligibility["operational_counts"]
        self.assertEqual(counts["sba_operational_pool"], 589)
        self.assertEqual(counts["open_response_candidate_pool"], 27)
        self.assertEqual(counts["open_response_review_pool"], 0)
        self.assertEqual(counts["inactive"], 0)
        self.assertEqual(counts["public_lab"], 36)

    def test_recovered_true_false_items_are_open_response_not_sba(self) -> None:
        by_source = {
            item["source_question_id"]: item for item in self.bank["items"]
        }
        for source_id in ("853", "854", "855", "856", "857"):
            item = by_source[source_id]
            self.assertEqual(item["question_type"], "open_response")
            self.assertEqual(item["source_content"]["options"], {})
            self.assertIsNone(item["source_content"]["correct_answer_letter"])
            self.assertEqual(item["status"]["review_state"], "approved_open_response")

    def test_public_lab_membership_is_unchanged(self) -> None:
        public_ids = [
            item["source_question_id"]
            for item in self.bank["items"]
            if item["status"]["public_lab"]
        ]
        self.assertEqual(len(public_ids), 36)
        self.assertTrue({"356", "421", "464"}.issubset(public_ids))


if __name__ == "__main__":
    unittest.main()

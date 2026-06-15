import json
import unittest
from pathlib import Path

from tools.question_generation.master_bank_eligibility import (
    build_eligibility_index,
)


ROOT = Path(__file__).resolve().parents[1]
STRUCTURED_PATH = ROOT / "knowledge/question-bank/structured/wset3_questions.json"
MASTER_PATH = ROOT / "knowledge/question-bank/master_bank/master_bank.json"
SUITABILITY_PATH = (
    ROOT
    / "knowledge/question-bank/open_response/suitability/"
    / "master_bank_open_response_suitability.json"
)
DIAGNOSTIC_PATH = ROOT / "frontend/diagnostic-sba/preguntas_data.js"
ADAPTIVE_PATH = ROOT / "frontend/adaptive-session/session_bank.js"
BATCH_IDS = {str(value) for value in range(858, 952)}


def _load_js_payload(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return json.loads(text[text.index("=") + 1 :].strip().rstrip(";"))


class CanonicalSbaReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.structured = json.loads(STRUCTURED_PATH.read_text(encoding="utf-8"))
        cls.master = json.loads(MASTER_PATH.read_text(encoding="utf-8"))
        cls.suitability = json.loads(SUITABILITY_PATH.read_text(encoding="utf-8"))
        cls.diagnostic = _load_js_payload(DIAGNOSTIC_PATH)
        cls.adaptive = _load_js_payload(ADAPTIVE_PATH)

    def test_all_validated_batch_ids_are_canonical(self):
        structured_ids = {
            str(record["question_id"]) for record in self.structured
        }
        master_ids = {
            item["source_question_id"] for item in self.master["items"]
        }

        self.assertTrue(BATCH_IDS.issubset(structured_ids))
        self.assertTrue(BATCH_IDS.issubset(master_ids))
        self.assertEqual(len(structured_ids), 710)
        self.assertEqual(len(master_ids), 710)

    def test_suitability_index_covers_the_reconciled_master_bank(self):
        suitability_ids = {
            record["source_question_id"] for record in self.suitability["records"]
        }

        self.assertEqual(self.suitability["record_count"], 710)
        self.assertTrue(BATCH_IDS.issubset(suitability_ids))
        eligibility = build_eligibility_index(self.master)
        self.assertEqual(
            eligibility["operational_counts"]["sba_operational_pool"],
            670,
        )

    def test_all_validated_batch_ids_are_learner_discoverable(self):
        diagnostic_ids = {
            item["source_question_id"] for item in self.diagnostic["items"]
        }
        adaptive_ids = {
            item["source_question_id"] for item in self.adaptive["sba_items"]
        }

        self.assertEqual(self.diagnostic["total_items"], 670)
        self.assertEqual(self.adaptive["total_sba"], 670)
        self.assertTrue(BATCH_IDS.issubset(diagnostic_ids))
        self.assertTrue(BATCH_IDS.issubset(adaptive_ids))
        self.assertEqual(diagnostic_ids, adaptive_ids)

    def test_reconciled_payload_governance_remains_fail_closed(self):
        for payload in (self.diagnostic, self.adaptive):
            self.assertIs(payload["governance"]["safe_for_examiner"], False)
            self.assertIs(
                payload["governance"]["examiner_scoring_allowed"],
                False,
            )
        for item in self.diagnostic["items"]:
            self.assertIs(item["governance"]["safe_for_examiner"], False)
            self.assertIs(
                item["governance"]["examiner_scoring_allowed"],
                False,
            )


if __name__ == "__main__":
    unittest.main()

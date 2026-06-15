"""Contract tests for the 25-item SBA enrichment Batch 6."""

from __future__ import annotations

import unittest

from tools.question_generation.sba_enrichment_deriver import derive, load_frontend_items


BATCH6_IDS = {
    "wset3_8",
    "wset3_34",
    "wset3_44",
    "wset3_55",
    "wset3_69",
    "wset3_77",
    "wset3_79",
    "wset3_96",
    "wset3_116",
    "wset3_122",
    "wset3_200",
    "wset3_225",
    "wset3_233",
    "wset3_249",
    "wset3_253",
    "wset3_274",
    "wset3_284",
    "wset3_292",
    "wset3_302",
    "wset3_328",
    "wset3_357",
    "wset3_366",
    "wset3_394",
    "wset3_420",
    "wset3_439",
}


class Batch6PromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = derive()
        cls.records = cls.payload["items_by_source_question_id"]
        cls.by_item_id = {record["item_id"]: record for record in cls.records.values()}
        cls.source_items = {item["id"]: item for item in load_frontend_items()}

    def test_batch_adds_exactly_25_items(self):
        self.assertEqual(len(BATCH6_IDS), 25)
        self.assertEqual(len(self.records), 285)

    def test_all_batch_items_are_promoted(self):
        self.assertTrue(BATCH6_IDS.issubset(self.by_item_id))

    def test_batch_promotions_have_explicit_provenance(self):
        for item_id in BATCH6_IDS:
            provenance = self.by_item_id[item_id]["_provenance"]["causal_chain"]
            self.assertEqual(provenance["derived_from"], "manual_review_v1")
            self.assertTrue(provenance["node_id"].startswith("HC_"))
            self.assertTrue(provenance["review_reason"].strip())
            self.assertTrue(provenance["learner_caveat"].strip())

    def test_correct_answer_and_spanish_caveat_are_visible(self):
        for item_id in BATCH6_IDS:
            source = self.source_items[item_id]
            answer = source["options"][source["correct_index"]]
            record = self.by_item_id[item_id]
            feedback = " ".join(record["feedback_by_mode"].values())
            self.assertIn(answer, feedback)
            self.assertIn("Matiz:", feedback)

    def test_no_negative_polarity_or_identification_items_are_promoted(self):
        for item_id in BATCH6_IDS:
            stem = self.source_items[item_id]["text"].lower()
            self.assertNotIn("incorrecta", stem)
            self.assertNotRegex(stem, r"^¿qué (región|país|variedad)")

    def test_governance_and_uniqueness_remain_locked(self):
        self.assertEqual(len(self.by_item_id), len(self.records))
        governance = self.payload["governance"]
        self.assertFalse(governance["safe_for_examiner"])
        self.assertFalse(governance["examiner_scoring_allowed"])
        self.assertFalse(governance["uses_llm"])
        self.assertFalse(governance["uses_api"])


if __name__ == "__main__":
    unittest.main()

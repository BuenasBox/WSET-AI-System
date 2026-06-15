"""Contract tests for the 25-item SBA enrichment Batch 7."""

from __future__ import annotations

import unittest

from tools.question_generation.sba_enrichment_deriver import (
    MANUAL_REVIEW_PROMOTIONS,
    NODE_ES,
    _is_identification_stem,
    _is_negative_polarity_stem,
    derive,
    load_frontend_items,
)


PREVIOUS_ENRICHED_COUNT = 285
BATCH_ITEM_IDS = {
    "wset3_229", "wset3_231", "wset3_246", "wset3_255", "wset3_259",
    "wset3_281", "wset3_283", "wset3_285", "wset3_288", "wset3_305",
    "wset3_320", "wset3_359", "wset3_368", "wset3_369", "wset3_375",
    "wset3_376", "wset3_399", "wset3_403", "wset3_441", "wset3_463",
    "wset3_465", "wset3_471", "wset3_503", "wset3_721", "wset3_734",
}


class Batch7PromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in cls.payload["items_by_source_question_id"].values()
        }
        cls.items = {item["id"]: item for item in load_frontend_items()}

    def test_batch_adds_exactly_25_items(self):
        self.assertEqual(len(BATCH_ITEM_IDS), 25)
        self.assertEqual(
            len(self.payload["items_by_source_question_id"]),
            PREVIOUS_ENRICHED_COUNT + len(BATCH_ITEM_IDS),
        )

    def test_all_batch_items_are_promoted(self):
        self.assertTrue(BATCH_ITEM_IDS.issubset(self.records))

    def test_batch_promotions_have_explicit_provenance(self):
        for item_id in BATCH_ITEM_IDS:
            promotion = MANUAL_REVIEW_PROMOTIONS[item_id]
            self.assertIn(promotion["node_id"], NODE_ES, item_id)
            self.assertTrue(promotion["reason"].strip(), item_id)
            self.assertTrue(promotion["caveat"].strip(), item_id)
            provenance = self.records[item_id]["_provenance"]["causal_chain"]
            self.assertEqual(provenance["promotion_method"], "manual_review_v1", item_id)
            self.assertEqual(provenance["node_id"], promotion["node_id"], item_id)

    def test_no_negative_polarity_or_identification_items_are_promoted(self):
        for item_id in BATCH_ITEM_IDS:
            stem = self.items[item_id]["text"]
            self.assertFalse(_is_negative_polarity_stem(stem), item_id)
            self.assertFalse(_is_identification_stem(stem), item_id)

    def test_correct_answer_and_spanish_caveat_are_visible(self):
        for item_id in BATCH_ITEM_IDS:
            item = self.items[item_id]
            correct = item["options"][item["correct_index"]]
            feedback = self.records[item_id]["feedback_by_mode"]["mentor"]
            self.assertIn(correct, feedback, item_id)
            self.assertIn("Matiz:", feedback, item_id)
            self.assertNotIn("The correct answer", feedback, item_id)

    def test_governance_and_uniqueness_remain_locked(self):
        governance = self.payload["governance"]
        self.assertIs(governance["safe_for_examiner"], False)
        self.assertIs(governance["examiner_scoring_allowed"], False)
        self.assertIs(governance["uses_llm"], False)
        self.assertIs(governance["uses_api"], False)
        item_ids = [record["item_id"] for record in self.records.values()]
        self.assertEqual(len(item_ids), len(set(item_ids)))


if __name__ == "__main__":
    unittest.main()

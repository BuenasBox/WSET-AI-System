"""Contract tests for the 50-item SBA enrichment Batch 8."""

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


PREVIOUS_ENRICHED_COUNT = 310
BATCH_ITEM_IDS = {
    "wset3_63", "wset3_97", "wset3_105", "wset3_121", "wset3_211",
    "wset3_213", "wset3_235", "wset3_237", "wset3_250", "wset3_256",
    "wset3_260", "wset3_267", "wset3_268", "wset3_272", "wset3_276",
    "wset3_280", "wset3_290", "wset3_293", "wset3_295", "wset3_299",
    "wset3_307", "wset3_313", "wset3_314", "wset3_324", "wset3_327",
    "wset3_332", "wset3_337", "wset3_343", "wset3_348", "wset3_374",
    "wset3_383", "wset3_395", "wset3_412", "wset3_419", "wset3_423",
    "wset3_425", "wset3_456", "wset3_508", "wset3_512", "wset3_517",
    "wset3_657", "wset3_712", "wset3_728", "wset3_729", "wset3_730",
    "wset3_735", "wset3_822", "wset3_827", "wset3_833", "wset3_851",
}


class Batch8PromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in cls.payload["items_by_source_question_id"].values()
        }
        cls.items = {item["id"]: item for item in load_frontend_items()}

    def test_batch_adds_exactly_50_items(self):
        self.assertEqual(len(BATCH_ITEM_IDS), 50)
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

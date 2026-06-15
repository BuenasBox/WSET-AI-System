"""Controlled manual-review promotion contract for SBA enrichment batch 5."""

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


PREVIOUS_ENRICHED_COUNT = 235
BATCH_ITEM_IDS = {
    "wset3_28",
    "wset3_49",
    "wset3_67",
    "wset3_76",
    "wset3_212",
    "wset3_227",
    "wset3_247",
    "wset3_262",
    "wset3_322",
    "wset3_323",
    "wset3_329",
    "wset3_347",
    "wset3_358",
    "wset3_367",
    "wset3_386",
    "wset3_389",
    "wset3_390",
    "wset3_393",
    "wset3_396",
    "wset3_413",
    "wset3_701",
    "wset3_715",
    "wset3_723",
    "wset3_726",
    "wset3_738",
}


class Batch5PromotionTests(unittest.TestCase):
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

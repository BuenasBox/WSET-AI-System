"""Controlled manual-review promotion contract for SBA enrichment batch 4."""

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


PREVIOUS_ENRICHED_COUNT = 210
BATCH_ITEM_IDS = {
    "wset3_11",
    "wset3_65",
    "wset3_104",
    "wset3_113",
    "wset3_208",
    "wset3_210",
    "wset3_219",
    "wset3_230",
    "wset3_251",
    "wset3_266",
    "wset3_282",
    "wset3_321",
    "wset3_339",
    "wset3_341",
    "wset3_345",
    "wset3_401",
    "wset3_421",
    "wset3_460",
    "wset3_466",
    "wset3_499",
    "wset3_514",
    "wset3_669",
    "wset3_673",
    "wset3_740",
    "wset3_850",
}


class Batch4PromotionTests(unittest.TestCase):
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

    def test_promotions_have_explicit_node_reason_and_caveat(self):
        self.assertEqual(set(MANUAL_REVIEW_PROMOTIONS), BATCH_ITEM_IDS)
        for item_id, promotion in MANUAL_REVIEW_PROMOTIONS.items():
            self.assertIn(promotion["node_id"], NODE_ES, item_id)
            self.assertTrue(promotion["reason"].strip(), item_id)
            self.assertTrue(promotion["caveat"].strip(), item_id)

    def test_batch_provenance_records_manual_review(self):
        for item_id in BATCH_ITEM_IDS:
            provenance = self.records[item_id]["_provenance"]["causal_chain"]
            self.assertEqual(provenance["promotion_method"], "manual_review_v1", item_id)
            self.assertTrue(provenance["review_reason"], item_id)
            self.assertTrue(provenance["learner_caveat"], item_id)

    def test_no_negative_polarity_or_identification_items_are_promoted(self):
        for item_id in BATCH_ITEM_IDS:
            stem = self.items[item_id]["text"]
            self.assertFalse(_is_negative_polarity_stem(stem), item_id)
            self.assertFalse(_is_identification_stem(stem), item_id)

    def test_correct_answer_is_named_in_learner_feedback(self):
        for item_id in BATCH_ITEM_IDS:
            item = self.items[item_id]
            correct = item["options"][item["correct_index"]]
            feedback = self.records[item_id]["feedback_by_mode"]["mentor"]
            self.assertIn(correct, feedback, item_id)

    def test_batch_copy_is_spanish_and_governance_is_locked(self):
        self.assertIs(self.payload["governance"]["safe_for_examiner"], False)
        self.assertIs(self.payload["governance"]["examiner_scoring_allowed"], False)
        self.assertIs(self.payload["governance"]["uses_llm"], False)
        self.assertIs(self.payload["governance"]["uses_api"], False)
        for item_id in BATCH_ITEM_IDS:
            record = self.records[item_id]
            copy = " ".join(record["causal_chain"].values())
            copy += " " + " ".join(record["feedback_by_mode"].values())
            self.assertNotIn("The correct answer", copy, item_id)
            self.assertNotIn("This wine", copy, item_id)

    def test_no_duplicate_item_ids(self):
        item_ids = [record["item_id"] for record in self.records.values()]
        self.assertEqual(len(item_ids), len(set(item_ids)))


if __name__ == "__main__":
    unittest.main()

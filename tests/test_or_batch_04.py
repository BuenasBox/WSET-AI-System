"""Validation contract for Open Response expansion Batch 4."""

from __future__ import annotations

import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "knowledge/question-bank/open_response/open_response_bank.json"
BATCH_PATH = ROOT / "knowledge/question-bank/open_response/or_batch_04_expansion.json"
BATCH_IDS = tuple(f"OR_{number:03d}" for number in range(107, 139))
VERBS = {
    "describe",
    "explain",
    "compare",
    "assess",
    "evaluate",
    "discuss",
    "recommend",
    "identify_and_explain",
}
REQUIRED_FIELDS = {
    "item_id",
    "question_id",
    "question_text",
    "ra_id",
    "command_verb",
    "expected_concepts",
    "response_depth_target",
    "causal_chain_reference",
    "feedback_profile",
    "safe_for_examiner",
    "examiner_scoring_allowed",
}
SWEET_PRODUCTION_TERMS = {
    "icewine",
    "eiswein",
    "tokaji",
    "aszú",
    "aszu",
    "sauternes",
    "botrytis",
    "noble rot",
    "passito",
    "appassimento",
}
RA5_TERMS = {
    "serve",
    "service",
    "storage",
    "store",
    "pair",
    "food",
    "customer",
    "recommend",
    "health",
    "consumption",
    "fault",
    "decant",
    "temperature",
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalized_question(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()


class OpenResponseBatch4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.batch = _load(BATCH_PATH)
        cls.items = cls.batch["items"]
        cls.bank = _load(BANK_PATH)

    def test_batch_has_32_contiguous_items(self) -> None:
        self.assertEqual(len(self.items), 32)
        self.assertEqual(tuple(item["item_id"] for item in self.items), BATCH_IDS)
        self.assertEqual(
            tuple(item["question_id"] for item in self.items),
            BATCH_IDS,
        )

    def test_bank_contains_138_unique_contiguous_items(self) -> None:
        ids = [item["item_id"] for item in self.bank["items"]]
        self.assertEqual(len(ids), 138)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(ids, [f"OR_{number:03d}" for number in range(1, 139)])
        self.assertEqual(self.bank["total_items"], 138)
        self.assertEqual(self.bank["last_batch"], 4)

    def test_required_fields_and_governance(self) -> None:
        for item in self.items:
            self.assertFalse(REQUIRED_FIELDS - set(item), item["item_id"])
            self.assertFalse(item["safe_for_examiner"])
            self.assertFalse(item["examiner_scoring_allowed"])
            self.assertFalse(item["governance"]["safe_for_examiner"])
            self.assertFalse(item["governance"]["examiner_scoring_allowed"])
            self.assertTrue(item["expected_concepts"])
            self.assertIn(item["response_depth_target"], {"developing", "strong"})
            self.assertEqual(item["question_id"], item["item_id"])

    def test_exact_ra_distribution(self) -> None:
        self.assertEqual(
            Counter(item["ra_id"] for item in self.items),
            Counter({"RA1": 6, "RA2": 12, "RA4": 8, "RA5": 6}),
        )

    def test_exact_balanced_verb_distribution(self) -> None:
        counts = Counter(item["command_verb"] for item in self.items)
        self.assertEqual(set(counts), VERBS)
        self.assertEqual(set(counts.values()), {4})

    def test_no_duplicate_question_text_in_batch_or_bank(self) -> None:
        all_questions = [
            _normalized_question(item["question_text"])
            for item in self.bank["items"]
        ]
        self.assertEqual(len(all_questions), len(set(all_questions)))

    def test_causal_chain_references_exist(self) -> None:
        valid = {
            path.stem.upper()
            for path in (
                ROOT / "knowledge/knowledge-map/causal-chains"
            ).glob("*.json")
        }
        for item in self.items:
            self.assertIsInstance(item["causal_chain_reference"], list)
            for chain_id in item["causal_chain_reference"]:
                self.assertIn(chain_id.upper(), valid, item["item_id"])

    def test_sweet_wine_taxonomy_never_defaults_to_ra5(self) -> None:
        for item in self.items:
            text = f"{item['topic']} {item['question_text']}".casefold()
            is_sweet_topic = any(term in text for term in SWEET_PRODUCTION_TERMS)
            if item["ra_id"] != "RA5" or not is_sweet_topic:
                continue
            self.assertTrue(
                any(term in text for term in RA5_TERMS),
                f"{item['item_id']} maps sweet production to RA5 without an RA5 frame",
            )

    def test_legacy_ra5_sweet_production_mislabels_are_corrected(self) -> None:
        by_id = {item["item_id"]: item for item in self.bank["items"]}
        for item_id in ("OR_050", "OR_081", "OR_106"):
            self.assertEqual(by_id[item_id]["ra_id"], "RA2")

    def test_feedback_profile_is_formative_and_complete(self) -> None:
        for item in self.items:
            profile = item["feedback_profile"]
            self.assertEqual(
                set(profile),
                {
                    "FOUNDATIONAL_RESPONSE",
                    "DEVELOPING_RESPONSE",
                    "STRONG_RESPONSE",
                },
            )
            combined = " ".join(profile.values()).casefold()
            for forbidden in ("official score", "pass prediction", "examiner mark"):
                self.assertNotIn(forbidden, combined)


if __name__ == "__main__":
    unittest.main()


from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools.question_generation.master_bank import MASTER_BANK_PATH, SAFE_GOVERNANCE
from tools.question_generation.sba_session_composer import (
    SESSION_SIZES,
    compose_sba_session,
    select_sba_session_items,
)


ROOT = Path(__file__).resolve().parents[1]


class SbaSessionComposerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.master_bank = json.loads(
            (ROOT / MASTER_BANK_PATH).read_text(encoding="utf-8")
        )

    def test_session_size_contract(self) -> None:
        self.assertEqual(SESSION_SIZES, {"short": 5, "standard": 10, "long": 20})

    def test_short_standard_and_long_sessions(self) -> None:
        self.assertEqual(
            len(select_sba_session_items(self.master_bank, session_size="short")), 5
        )
        self.assertEqual(
            len(select_sba_session_items(self.master_bank, session_size="standard")), 10
        )
        self.assertEqual(
            len(select_sba_session_items(self.master_bank, session_size="long")), 20
        )

    def test_selection_is_deterministic_and_does_not_mutate_bank(self) -> None:
        before = copy.deepcopy(self.master_bank)
        first = select_sba_session_items(self.master_bank, session_size="long")
        second = select_sba_session_items(
            copy.deepcopy(self.master_bank), session_size="long"
        )

        self.assertEqual(first, second)
        self.assertEqual(self.master_bank, before)

    def test_default_selection_uses_public_sba_only(self) -> None:
        selected = select_sba_session_items(self.master_bank, session_size=36)

        self.assertEqual(len(selected), 36)
        self.assertTrue(
            all(item["question_type"] == "single_best_answer" for item in selected)
        )
        self.assertTrue(all("public_lab" in item["collections"] for item in selected))
        self.assertTrue(all(item["status"]["public_lab"] for item in selected))

    def test_ra_filter(self) -> None:
        selected = select_sba_session_items(
            self.master_bank, ra="RA1", session_size=20
        )

        self.assertEqual([item["source_question_id"] for item in selected], ["83", "230", "440", "493", "515"])
        self.assertTrue(all(item["curriculum"]["ra"] == "RA1" for item in selected))

    def test_topic_filter(self) -> None:
        selected = select_sba_session_items(
            self.master_bank, topic="sparkling", session_size=20
        )

        self.assertTrue(selected)
        self.assertTrue(
            all("sparkling" in item["curriculum"]["topic"] for item in selected)
        )

    def test_difficulty_filter(self) -> None:
        selected = select_sba_session_items(
            self.master_bank, difficulty="intermediate", session_size="short"
        )

        self.assertEqual(len(selected), 5)
        self.assertTrue(
            all(item["curriculum"]["difficulty"] == "intermediate" for item in selected)
        )

    def test_conceptual_duplicates_are_deferred_when_metadata_matches(self) -> None:
        synthetic_items = []
        for source_id, keyword in (("1", "acid"), ("2", "acid"), ("3", "tannin")):
            synthetic_items.append(
                {
                    "master_item_id": f"wset3_{source_id}",
                    "source_question_id": source_id,
                    "question_type": "single_best_answer",
                    "curriculum": {
                        "ra": "RA1",
                        "topic": "test",
                        "difficulty": "intermediate",
                        "expected_topics": ["wine structure"],
                        "expected_keywords": [keyword],
                        "expected_causal_links": [],
                    },
                    "collections": ["single_best_answer", "public_lab"],
                    "status": {"public_lab": True},
                }
            )
        synthetic = {
            "collections": {
                "public_lab": [item["master_item_id"] for item in synthetic_items]
            },
            "items": synthetic_items,
        }

        selected = select_sba_session_items(synthetic, session_size=2)

        self.assertEqual(
            [item["source_question_id"] for item in selected],
            ["1", "3"],
        )

    def test_compose_session_keeps_exam_parts_separate(self) -> None:
        session = compose_sba_session(self.master_bank, session_size="short")

        self.assertEqual(session["exam_part"], "diagnostic_sba")
        self.assertEqual(session["frontend_route"], "frontend/diagnostic-sba/")
        self.assertEqual(
            session["open_response_route"], "frontend/open-response-lab/"
        )
        self.assertNotEqual(
            session["frontend_route"], session["open_response_route"]
        )
        self.assertEqual(session["governance"], SAFE_GOVERNANCE)

    def test_composer_does_not_activate_open_response(self) -> None:
        session = compose_sba_session(self.master_bank, session_size="long")

        self.assertTrue(
            all(item["question_type"] == "single_best_answer" for item in session["items"])
        )
        self.assertNotIn("open_response", session["collection"])

    def test_integer_size_and_invalid_sizes(self) -> None:
        self.assertEqual(
            len(select_sba_session_items(self.master_bank, session_size=7)), 7
        )
        with self.assertRaises(ValueError):
            select_sba_session_items(self.master_bank, session_size="medium")
        with self.assertRaises(ValueError):
            select_sba_session_items(self.master_bank, session_size=0)


if __name__ == "__main__":
    unittest.main()

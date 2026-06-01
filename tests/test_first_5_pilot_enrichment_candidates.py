from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools.question_generation.structured_question_bank_adapter import (
    AdapterStatus,
    classify_structured_question,
)


SOURCE_BANK_PATH = Path("knowledge/question-bank/structured/wset3_questions.json")
SELECTED_IDS = ("1", "2", "12", "13", "17")
FORBIDDEN_OUTPUT_PATHS = (
    Path("knowledge/question-bank/diagnostic_sba/converted"),
    Path("knowledge/question-bank/diagnostic_sba/pilot_bank.json"),
    Path("knowledge/question-bank/diagnostic_sba/generated"),
    Path("knowledge/question-bank/diagnostic_sba/preguntas.json"),
)


def load_source_bank() -> list[dict]:
    with SOURCE_BANK_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise AssertionError("structured source bank must be a list")
    return data


def selected_items(source_bank: list[dict]) -> list[dict]:
    by_id = {str(item.get("question_id")): item for item in source_bank}
    return [by_id[item_id] for item_id in SELECTED_IDS]


def normalize_text(value: object) -> str:
    return " ".join(str(value).lower().split())


class FirstFivePilotEnrichmentCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source_bank = load_source_bank()
        cls.items = selected_items(cls.source_bank)

    def test_exactly_five_candidates_selected(self) -> None:
        self.assertEqual(len(SELECTED_IDS), 5)
        self.assertEqual(len(self.items), 5)
        self.assertEqual([str(item["question_id"]) for item in self.items], list(SELECTED_IDS))

    def test_all_candidates_classify_as_adapter_ready_clean_pilot(self) -> None:
        statuses = [classify_structured_question(item) for item in self.items]

        self.assertEqual(set(statuses), {AdapterStatus.ADAPTER_READY_CLEAN_PILOT})

    def test_all_candidates_are_safe_for_examiner_false(self) -> None:
        self.assertTrue(all(item.get("safe_for_examiner") is False for item in self.items))

    def test_no_candidate_has_duplicate_option_text(self) -> None:
        for item in self.items:
            options = item["options"]
            normalized = [normalize_text(options[key]) for key in ("A", "B", "C", "D")]
            self.assertEqual(len(normalized), len(set(normalized)), item["question_id"])

    def test_all_candidates_have_valid_correct_answer(self) -> None:
        for item in self.items:
            answer_letter = item.get("correct_answer_letter")
            self.assertIn(answer_letter, {"A", "B", "C", "D"})
            self.assertTrue(item.get("correct_answer_text"))
            self.assertEqual(
                normalize_text(item["options"][answer_letter]),
                normalize_text(item["correct_answer_text"]),
                item["question_id"],
            )

    def test_all_candidates_have_expected_topics_reasoning_keywords_and_causal_links(self) -> None:
        for item in self.items:
            self.assertTrue(item.get("expected_topics"), item["question_id"])
            self.assertTrue(item.get("expected_reasoning_type"), item["question_id"])
            self.assertTrue(item.get("expected_keywords"), item["question_id"])
            self.assertTrue(item.get("expected_causal_links"), item["question_id"])

    def test_report_selection_does_not_mutate_source_bank(self) -> None:
        before = copy.deepcopy(self.source_bank)

        selected_items(self.source_bank)
        for item in self.items:
            classify_structured_question(item)

        self.assertEqual(self.source_bank, before)

    def test_no_converted_files_are_created(self) -> None:
        before = {path: path.exists() for path in FORBIDDEN_OUTPUT_PATHS}

        selected_items(self.source_bank)

        after = {path: path.exists() for path in FORBIDDEN_OUTPUT_PATHS}
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()

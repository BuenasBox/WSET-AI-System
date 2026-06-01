from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools.question_generation.diagnostic_sba_validator import validate_diagnostic_sba_item
from tools.question_generation.structured_question_bank_adapter import (
    AdapterStatus,
    classify_structured_question,
    map_structured_question_skeleton,
)


SOURCE_BANK_PATH = Path("knowledge/question-bank/structured/wset3_questions.json")
SOURCE_BANK_PATH_TEXT = SOURCE_BANK_PATH.as_posix()
FORBIDDEN_OUTPUT_PATHS = (
    Path("knowledge/question-bank/diagnostic_sba/converted"),
    Path("knowledge/question-bank/diagnostic_sba/pilot_bank.json"),
    Path("knowledge/question-bank/diagnostic_sba/generated"),
)


def load_source_bank() -> list[dict]:
    with SOURCE_BANK_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise AssertionError("structured source bank must be a JSON list")
    return data


def normalized_option_texts(item: dict) -> list[str]:
    options = item.get("options")
    if not isinstance(options, dict):
        return []
    texts = []
    for key in ("A", "B", "C", "D"):
        value = options.get(key)
        if isinstance(value, str) and value.strip():
            texts.append(" ".join(value.lower().split()))
    return texts


def is_clean_pilot_candidate(item: dict) -> bool:
    options = item.get("options")
    if item.get("question_type") != "theory":
        return False
    if item.get("safe_for_examiner") is not False:
        return False
    if not isinstance(options, dict) or set(options.keys()) != {"A", "B", "C", "D"}:
        return False
    if any(not isinstance(options.get(key), str) or not options[key].strip() for key in ("A", "B", "C", "D")):
        return False
    texts = normalized_option_texts(item)
    if len(texts) != len(set(texts)):
        return False
    answer_letter = item.get("correct_answer_letter")
    if answer_letter not in {"A", "B", "C", "D"}:
        return False
    if not isinstance(item.get("correct_answer_text"), str) or not item["correct_answer_text"].strip():
        return False
    if " ".join(options[answer_letter].lower().split()) != " ".join(item["correct_answer_text"].lower().split()):
        return False
    if not item.get("expected_topics"):
        return False
    if not item.get("expected_reasoning_type"):
        return False
    return True


def has_duplicate_options(item: dict) -> bool:
    texts = normalized_option_texts(item)
    return bool(texts) and len(texts) != len(set(texts))


def has_empty_option(item: dict) -> bool:
    options = item.get("options")
    return isinstance(options, dict) and any(
        not isinstance(options.get(key), str) or not options[key].strip() for key in ("A", "B", "C", "D")
    )


def has_invalid_correct_answer(item: dict) -> bool:
    return item.get("correct_answer_letter") not in {"A", "B", "C", "D"}


def first_n(items: list[dict], predicate, count: int) -> list[dict]:
    return [item for item in items if predicate(item)][:count]


class StructuredQuestionBankAdapterPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source_bank = load_source_bank()
        cls.clean_items = first_n(cls.source_bank, is_clean_pilot_candidate, 5)
        cls.short_answer_items = first_n(
            cls.source_bank, lambda item: item.get("question_type") == "short_answer", 5
        )
        non_short_answer = [
            item for item in cls.source_bank if item.get("question_type") != "short_answer"
        ]
        cls.duplicate_items = first_n(non_short_answer, has_duplicate_options, 1)
        cls.invalid_answer_items = first_n(non_short_answer, has_invalid_correct_answer, 1)
        cls.empty_option_items = first_n(non_short_answer, has_empty_option, 1)
        seen_ids = set()
        invalid_candidates = []
        for item in cls.duplicate_items + cls.invalid_answer_items + cls.empty_option_items:
            item_id = item.get("question_id")
            if item_id not in seen_ids:
                invalid_candidates.append(item)
                seen_ids.add(item_id)
        for item in cls.source_bank:
            if len(invalid_candidates) >= 5:
                break
            if item.get("question_type") == "short_answer":
                continue
            if classify_structured_question(item) == AdapterStatus.REJECT_OR_DEFER:
                item_id = item.get("question_id")
                if item_id not in seen_ids:
                    invalid_candidates.append(item)
                    seen_ids.add(item_id)
        cls.invalid_items = invalid_candidates[:5]
        cls.sampled_items = cls.clean_items + cls.invalid_items + cls.short_answer_items

    def test_source_bank_loads_with_expected_total_count(self) -> None:
        self.assertEqual(len(self.source_bank), 616)
        self.assertTrue(all(isinstance(item, dict) for item in self.source_bank))

    def test_deterministic_samples_include_required_categories(self) -> None:
        self.assertEqual(len(self.clean_items), 5)
        self.assertEqual(len(self.short_answer_items), 5)
        self.assertGreaterEqual(len(self.invalid_items), 1)
        self.assertGreaterEqual(len(self.duplicate_items), 1)
        self.assertGreaterEqual(len(self.invalid_answer_items), 1)
        self.assertGreaterEqual(len(self.empty_option_items), 1)
        self.assertLess(len(self.sampled_items), len(self.source_bank))

    def test_adapter_classifies_sampled_items_without_exception(self) -> None:
        statuses = [classify_structured_question(item) for item in self.sampled_items]

        self.assertEqual(len(statuses), len(self.sampled_items))
        self.assertTrue(all(isinstance(status, str) for status in statuses))

    def test_clean_pilot_candidates_are_adapter_ready(self) -> None:
        statuses = [classify_structured_question(item) for item in self.clean_items]

        self.assertIn(AdapterStatus.ADAPTER_READY_CLEAN_PILOT, statuses)
        self.assertEqual(set(statuses), {AdapterStatus.ADAPTER_READY_CLEAN_PILOT})

    def test_short_answer_items_are_preserved_for_open_response(self) -> None:
        statuses = [classify_structured_question(item) for item in self.short_answer_items]

        self.assertEqual(set(statuses), {AdapterStatus.PRESERVE_FOR_OPEN_RESPONSE})

    def test_invalid_or_deferred_examples_are_rejected_or_deferred(self) -> None:
        statuses = [classify_structured_question(item) for item in self.invalid_items]

        self.assertIn(AdapterStatus.REJECT_OR_DEFER, statuses)
        self.assertEqual(set(statuses), {AdapterStatus.REJECT_OR_DEFER})

    def test_skeleton_preserves_source_question_id_and_stem(self) -> None:
        item = self.clean_items[0]
        skeleton = map_structured_question_skeleton(item, SOURCE_BANK_PATH_TEXT)

        self.assertEqual(skeleton["identity"]["source_question_id"], item["question_id"])
        self.assertEqual(skeleton["question"]["stem"], item["question_text"])

    def test_skeleton_preserves_options(self) -> None:
        item = self.clean_items[0]
        skeleton = map_structured_question_skeleton(item, SOURCE_BANK_PATH_TEXT)

        for key in ("A", "B", "C", "D"):
            self.assertEqual(skeleton["options"][key]["option_text"], item["options"][key])

    def test_skeleton_sets_exactly_one_correct_option_for_clean_item(self) -> None:
        item = self.clean_items[0]
        skeleton = map_structured_question_skeleton(item, SOURCE_BANK_PATH_TEXT)

        correct_options = [key for key, option in skeleton["options"].items() if option["is_correct"]]

        self.assertEqual(correct_options, [item["correct_answer_letter"]])

    def test_skeleton_output_remains_intentionally_incomplete(self) -> None:
        skeleton = map_structured_question_skeleton(self.clean_items[0], SOURCE_BANK_PATH_TEXT)

        self.assertEqual(skeleton["adapter_status"], "requires_enrichment")
        self.assertFalse(skeleton["valid_diagnostic_item"])
        self.assertEqual(skeleton["source_support"]["status"], "missing")
        self.assertEqual(skeleton["feedback"]["status"], "missing")
        self.assertIn("source_support", skeleton["enrichment_required"])
        self.assertIn("diagnostic_role", skeleton["enrichment_required"])

    def test_validator_rejects_skeleton_until_enrichment_is_added(self) -> None:
        skeleton = map_structured_question_skeleton(self.clean_items[0], SOURCE_BANK_PATH_TEXT)

        errors = validate_diagnostic_sba_item(skeleton)

        self.assertTrue(errors)
        self.assertIn("source_support.source_ids must be a non-empty list", errors)
        self.assertIn("feedback.correct_rationale must be present and non-empty", errors)

    def test_source_bank_object_is_not_mutated(self) -> None:
        source_snapshot = copy.deepcopy(self.source_bank)

        for item in self.sampled_items:
            classify_structured_question(item)
            map_structured_question_skeleton(item, SOURCE_BANK_PATH_TEXT)

        self.assertEqual(self.source_bank, source_snapshot)

    def test_no_converted_files_are_created(self) -> None:
        before = {path: path.exists() for path in FORBIDDEN_OUTPUT_PATHS}

        for item in self.sampled_items:
            map_structured_question_skeleton(item, SOURCE_BANK_PATH_TEXT)

        after = {path: path.exists() for path in FORBIDDEN_OUTPUT_PATHS}
        self.assertEqual(after, before)

    def test_no_bulk_migration_occurs(self) -> None:
        skeletons = [map_structured_question_skeleton(item, SOURCE_BANK_PATH_TEXT) for item in self.clean_items]

        self.assertEqual(len(skeletons), 5)
        self.assertLess(len(skeletons), len(self.source_bank))
        self.assertTrue(all(isinstance(skeleton, dict) for skeleton in skeletons))

    def test_governance_values_remain_safe(self) -> None:
        skeleton = map_structured_question_skeleton(self.clean_items[0], SOURCE_BANK_PATH_TEXT)

        self.assertFalse(skeleton["governance"]["safe_for_examiner"])
        self.assertFalse(skeleton["governance"]["examiner_scoring_allowed"])
        self.assertFalse(skeleton["governance"]["official_wset_question"])
        self.assertTrue(skeleton["governance"]["training_item_only"])
        self.assertFalse(skeleton["governance"]["uses_llm"])
        self.assertFalse(skeleton["governance"]["uses_api"])
        self.assertFalse(skeleton["governance"]["uses_embeddings"])
        self.assertFalse(skeleton["governance"]["uses_vector_db"])
        self.assertFalse(skeleton["governance"]["cloud_services_active"])

    def test_lineage_includes_source_path_and_adapter_version(self) -> None:
        skeleton = map_structured_question_skeleton(self.clean_items[0], SOURCE_BANK_PATH_TEXT)
        lineage = skeleton["adapter_lineage"]

        self.assertEqual(lineage["source_bank_path"], SOURCE_BANK_PATH_TEXT)
        self.assertEqual(lineage["adapter_version"], "structured_adapter_v0")
        self.assertEqual(lineage["source_question_id"], self.clean_items[0]["question_id"])


if __name__ == "__main__":
    unittest.main()

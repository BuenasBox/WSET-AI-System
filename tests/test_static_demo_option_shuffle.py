from __future__ import annotations

import copy
import json
import unittest

from tools.question_generation.static_demo_exporter import (
    OPTION_IDS,
    OPTION_SHUFFLE_STRATEGY,
    build_static_demo_export_payload,
    build_static_demo_outcome_payload,
    build_static_demo_render_payload,
)


def make_draft(item_id: str = "draft_diag_sba_structured_2") -> dict:
    return {
        "identity": {
            "item_id": item_id,
            "source_question_id": item_id.rsplit("_", 1)[-1],
        },
        "curriculum": {
            "ra_id": "RA4",
            "topic": "fortified_wines",
            "subtopic": "port_fortification",
            "difficulty": "intermediate",
            "learning_objective": "Training-only diagnostic item.",
        },
        "question": {
            "stem": "What is the best answer?",
            "question_type": "single_best_answer",
        },
        "options": {
            "A": {
                "option_id": "A",
                "option_text": "Alpha",
                "is_correct": False,
                "diagnostic_role": "distractor",
            },
            "B": {
                "option_id": "B",
                "option_text": "Bravo",
                "is_correct": False,
                "diagnostic_role": "distractor",
            },
            "C": {
                "option_id": "C",
                "option_text": "Charlie",
                "is_correct": True,
                "diagnostic_role": "correct",
            },
            "D": {
                "option_id": "D",
                "option_text": "Delta",
                "is_correct": False,
                "diagnostic_role": "distractor",
            },
        },
        "feedback": {
            "correct_rationale": "Charlie is correct.",
            "why_other_options_are_wrong": {
                "A": "Alpha is wrong.",
                "B": "Bravo is wrong.",
                "C": "Charlie is correct.",
                "D": "Delta is wrong.",
            },
            "remediation_recommendation": "Review the concept.",
            "remediation_target": {"target_type": "topic", "target_id": "port_fortification"},
        },
    }


def make_review(draft: dict) -> dict:
    identity = draft["identity"]
    return {
        "review_id": f"review_{identity['source_question_id']}",
        "source_question_id": identity["source_question_id"],
        "draft_id": identity["item_id"],
        "approval_scope": "static_demo_only",
    }


class StaticDemoOptionShuffleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.drafts = [
            make_draft("draft_diag_sba_structured_2"),
            make_draft("draft_diag_sba_structured_83"),
            make_draft("draft_diag_sba_structured_105"),
        ]
        cls.reviews = [make_review(draft) for draft in cls.drafts]
        cls.items = [
            build_static_demo_render_payload(draft, review)
            for draft, review in zip(cls.drafts, cls.reviews)
        ]
        cls.outcomes = {
            item["item_id"]: build_static_demo_outcome_payload(draft, review)
            for item, draft, review in zip(cls.items, cls.drafts, cls.reviews)
        }

    def test_export_metadata_documents_shuffle_strategy(self) -> None:
        payload = build_static_demo_export_payload([], [])

        self.assertEqual(
            payload["export_metadata"]["option_shuffle_strategy"],
            OPTION_SHUFFLE_STRATEGY,
        )

    def test_render_options_use_visual_letters_and_preserve_canonical_ids(self) -> None:
        for item in self.items:
            options = item["options"]
            self.assertEqual([option["visual_option_id"] for option in options], list(OPTION_IDS))
            self.assertEqual(sorted(option["option_id"] for option in options), list(OPTION_IDS))
            self.assertEqual(len({option["option_id"] for option in options}), 4)

    def test_every_item_is_visually_permuted_from_canonical_order(self) -> None:
        for item in self.items:
            canonical_order = [option["option_id"] for option in item["options"]]
            self.assertNotEqual(canonical_order, list(OPTION_IDS))

    def test_shuffle_is_deterministic_from_item_identity(self) -> None:
        draft = make_draft("draft_diag_sba_structured_2")
        review = make_review(draft)
        first = build_static_demo_render_payload(draft, review)
        second = build_static_demo_render_payload(copy.deepcopy(draft), copy.deepcopy(review))

        self.assertEqual(first["options"], second["options"])

    def test_shuffle_does_not_mutate_source_drafts_or_reviews(self) -> None:
        drafts_before = copy.deepcopy(self.drafts)
        reviews_before = copy.deepcopy(self.reviews)

        for draft, review in zip(self.drafts, self.reviews):
            build_static_demo_render_payload(draft, review)
            build_static_demo_outcome_payload(draft, review)

        self.assertEqual(self.drafts, drafts_before)
        self.assertEqual(self.reviews, reviews_before)

    def test_visual_mapping_traces_to_diagnostics_and_correctness_by_option_id(self) -> None:
        for item in self.items:
            outcome = self.outcomes[item["item_id"]]
            visual_to_option = {
                option["visual_option_id"]: option["option_id"]
                for option in item["options"]
            }
            correct_option_id = outcome["correct_option_id"]

            self.assertIn(correct_option_id, outcome["option_diagnostics"])
            self.assertIn(correct_option_id, visual_to_option.values())
            for option_id in visual_to_option.values():
                diagnostic = outcome["option_diagnostics"][option_id]
                self.assertIn("is_correct", diagnostic)
                self.assertIn("diagnostic_role", diagnostic)

    def test_pre_submit_options_do_not_expose_correctness_or_diagnostics(self) -> None:
        render_text = json.dumps(self.items, ensure_ascii=False)

        self.assertNotIn("correct_option_id", render_text)
        self.assertNotIn("is_correct", render_text)
        self.assertNotIn("diagnostic_role", render_text)
        self.assertNotIn("diagnostic_note", render_text)

    def test_correctness_is_not_encoded_by_visual_position(self) -> None:
        correct_visual_ids = []
        for item in self.items:
            outcome = self.outcomes[item["item_id"]]
            correct_option_id = outcome["correct_option_id"]
            correct_visual_ids.append(
                next(
                    option["visual_option_id"]
                    for option in item["options"]
                    if option["option_id"] == correct_option_id
                )
            )

        self.assertGreater(len(set(correct_visual_ids)), 1)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools.question_generation.open_response_session_engine import (
    ACTIVE_POOL_IDS,
    EXCLUDED_SOURCE_IDS,
    FEEDBACK_ALLOWED,
    FEEDBACK_PROHIBITED,
    LAB_GOVERNANCE_FLAGS,
    active_pool_manifest,
    compose_session,
    select_session_question_ids,
)


CANDIDATES_PATH = Path("knowledge/question-bank/open_response/normalized/diagnostic_open_response_candidates.json")


def load_candidates() -> list[dict]:
    return json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))


class OpenResponseSessionEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.candidates = load_candidates()

    def test_active_pool_ids_are_exact_initial_pool(self) -> None:
        self.assertEqual(
            ACTIVE_POOL_IDS,
            (
                "798",
                "799",
                "800",
                "801",
                "802",
                "803",
                "804",
                "805",
                "806",
                "808",
                "810",
                "811",
                "812",
                "813",
                "814",
                "815",
                "816",
                "817",
            ),
        )

    def test_excludes_needs_review_ids_807_and_809(self) -> None:
        selected = select_session_question_ids(self.candidates, session_size=25)

        self.assertNotIn("807", selected)
        self.assertNotIn("809", selected)
        self.assertEqual(EXCLUDED_SOURCE_IDS, ("807", "809"))

    def test_selection_is_deterministic(self) -> None:
        first = select_session_question_ids(self.candidates, session_size="standard")
        second = select_session_question_ids(copy.deepcopy(self.candidates), session_size="standard")

        self.assertEqual(first, second)

    def test_selection_preserves_reproducible_pool_order(self) -> None:
        selected = select_session_question_ids(self.candidates, session_size="short")

        self.assertEqual(selected, ["798", "799", "800"])

    def test_short_session_has_three_questions(self) -> None:
        selected = select_session_question_ids(self.candidates, session_size="short")

        self.assertEqual(len(selected), 3)

    def test_standard_session_has_five_questions(self) -> None:
        selected = select_session_question_ids(self.candidates, session_size="standard")

        self.assertEqual(len(selected), 5)

    def test_long_session_has_ten_questions(self) -> None:
        selected = select_session_question_ids(self.candidates, session_size="long")

        self.assertEqual(len(selected), 10)

    def test_integer_session_size_supported(self) -> None:
        selected = select_session_question_ids(self.candidates, session_size=7)

        self.assertEqual(len(selected), 7)

    def test_ra_filter_selects_ra1_pool(self) -> None:
        selected = select_session_question_ids(self.candidates, ra="RA1", session_size="long")

        self.assertEqual(len(selected), 10)
        self.assertTrue(set(selected).issubset(set(ACTIVE_POOL_IDS)))

    def test_topic_filter_is_deterministic(self) -> None:
        selected = select_session_question_ids(self.candidates, topic="suelo", session_size=5)

        self.assertEqual(selected, ["804", "817"])

    def test_difficulty_filter_is_deterministic(self) -> None:
        selected = select_session_question_ids(self.candidates, difficulty="foundational", session_size=5)

        self.assertEqual(selected, ["813", "814", "815"])

    def test_redundant_pairs_are_deferred_when_alternatives_exist(self) -> None:
        selected = select_session_question_ids(self.candidates, session_size=13)

        self.assertIn("804", selected)
        self.assertNotIn("817", selected)
        self.assertIn("810", selected)
        self.assertNotIn("812", selected)

    def test_compose_session_is_inactive(self) -> None:
        session = compose_session(self.candidates, session_size="standard")

        self.assertEqual(session["activation_status"], "inactive")
        self.assertEqual(session["source_question_ids"], ["798", "799", "800", "801", "802"])

    def test_compose_session_governance_is_safe(self) -> None:
        session = compose_session(self.candidates, session_size="standard")

        self.assertEqual(session["governance_flags"], LAB_GOVERNANCE_FLAGS)
        self.assertFalse(session["governance_flags"]["safe_for_examiner"])
        self.assertFalse(session["governance_flags"]["examiner_scoring_allowed"])
        self.assertFalse(session["governance_flags"]["uses_llm"])
        self.assertFalse(session["governance_flags"]["uses_api"])
        self.assertFalse(session["governance_flags"]["uses_embeddings"])
        self.assertFalse(session["governance_flags"]["uses_vector_db"])
        self.assertFalse(session["governance_flags"]["cloud_services_active"])
        self.assertFalse(session["governance_flags"]["public_frontend_active"])
        self.assertFalse(session["governance_flags"]["open_response_lab_active"])

    def test_feedback_boundaries_allow_only_formative_categories(self) -> None:
        self.assertEqual(
            FEEDBACK_ALLOWED,
            (
                "present_concepts",
                "missing_concepts",
                "missing_causal_links",
                "revision_suggestions",
                "orientative_answer_model",
            ),
        )

    def test_feedback_boundaries_prohibit_assessment_authority(self) -> None:
        self.assertIn("score", FEEDBACK_PROHIBITED)
        self.assertIn("percentage", FEEDBACK_PROHIBITED)
        self.assertIn("pass_fail", FEEDBACK_PROHIBITED)
        self.assertIn("wset_equivalence", FEEDBACK_PROHIBITED)
        self.assertIn("examiner_judgement", FEEDBACK_PROHIBITED)
        self.assertIn("official_grade", FEEDBACK_PROHIBITED)

    def test_active_pool_manifest_documents_readiness(self) -> None:
        manifest = active_pool_manifest()

        self.assertEqual([item["source_question_id"] for item in manifest], list(ACTIVE_POOL_IDS))
        readiness = {item["source_question_id"]: item["readiness"] for item in manifest}
        self.assertEqual(readiness["800"], "READY")
        self.assertEqual(readiness["798"], "READY_WITH_MINOR_GAPS")

    def test_engine_does_not_mutate_candidates(self) -> None:
        before = copy.deepcopy(self.candidates)

        select_session_question_ids(self.candidates, session_size="long")

        self.assertEqual(self.candidates, before)

    def test_invalid_session_size_rejected(self) -> None:
        with self.assertRaises(ValueError):
            select_session_question_ids(self.candidates, session_size="medium")

    def test_non_positive_integer_session_size_rejected(self) -> None:
        with self.assertRaises(ValueError):
            select_session_question_ids(self.candidates, session_size=0)


if __name__ == "__main__":
    unittest.main()

import inspect
import unittest
from unittest import mock

from tools.self_eval import answer_comparator
from tools.self_eval.answer_comparator import compare_answer


CONTEXT_PACKAGE = {
    "retrieved_context": [],
    "governance": {"safe_for_examiner": False},
}


def _sat_question(**overrides):
    question = {
        "question_id": "sat_strength_test",
        "question_type": "sat",
        "question_text": "Assess the wine quality using BICL.",
        "expected_keywords": [],
        "expected_causal_links": [],
        "expected_topics": [],
        "expected_reasoning_type": "",
    }
    question.update(overrides)
    return question


class ComparatorSatStrengthTests(unittest.TestCase):
    def _strengths_for(self, answer: str, question: dict | None = None) -> set[str]:
        result = compare_answer(question or _sat_question(), answer, CONTEXT_PACKAGE)
        return set(result["strengths"])

    def test_sat_answer_with_bicl_tier_and_causal_language_has_all_sat_strengths(self):
        strengths = self._strengths_for(
            "The balance, intensity, complexity and length support a very good "
            "quality assessment because all BICL evidence is clearly present."
        )

        self.assertIn("bicl_criteria_present", strengths)
        self.assertIn("quality_tier_stated", strengths)
        self.assertIn("causal_quality_link_present", strengths)

    def test_sat_answer_without_causal_term_does_not_have_causal_quality_link(self):
        strengths = self._strengths_for(
            "Balance is evident and the quality assessment is good."
        )

        self.assertIn("bicl_criteria_present", strengths)
        self.assertIn("quality_tier_stated", strengths)
        self.assertNotIn("causal_quality_link_present", strengths)

    def test_sat_answer_without_bicl_terms_has_no_sat_strength_labels(self):
        strengths = self._strengths_for(
            "The wine is pleasant and the conclusion is simple."
        )

        self.assertFalse(
            {
                "bicl_criteria_present",
                "quality_tier_stated",
                "causal_quality_link_present",
            }
            & strengths
        )

    def test_theory_question_does_not_fire_sat_strengths_for_bicl_terms(self):
        question = _sat_question(
            question_type="theory",
            question_text="Explain canopy management.",
        )
        strengths = self._strengths_for(
            "Balance, intensity, complexity and length support good quality "
            "because the evidence is clear.",
            question,
        )

        self.assertNotIn("bicl_criteria_present", strengths)
        self.assertNotIn("quality_tier_stated", strengths)
        self.assertNotIn("causal_quality_link_present", strengths)

    def test_spanish_sat_answer_has_all_sat_strength_labels(self):
        strengths = self._strengths_for(
            "El balance, la complejidad y el length apuntan a una calidad muy "
            "buena; por tanto, la evaluación de calidad está justificada.",
            _sat_question(question_text="Evalúa la calidad del vino."),
        )

        self.assertIn("bicl_criteria_present", strengths)
        self.assertIn("quality_tier_stated", strengths)
        self.assertIn("causal_quality_link_present", strengths)

    def test_bicl_criteria_present_fires_for_each_individual_bicl_term(self):
        for term in ("balance", "intensity", "complexity", "length"):
            with self.subTest(term=term):
                strengths = self._strengths_for(f"The answer cites {term}.")
                self.assertIn("bicl_criteria_present", strengths)

    def test_quality_tier_stated_fires_for_each_quality_tier_term(self):
        for tier in (
            "outstanding",
            "very good",
            "good",
            "sobresaliente",
            "muy buena",
            "buena",
        ):
            with self.subTest(tier=tier):
                strengths = self._strengths_for(f"The quality tier is {tier}.")
                self.assertIn("quality_tier_stated", strengths)

    def test_existing_failure_labels_still_fire_for_empty_sat_answer(self):
        result = compare_answer(_sat_question(), "", CONTEXT_PACKAGE)

        self.assertTrue(result["failure_labels"])
        self.assertIn("incomplete_balance_justification", result["failure_labels"])
        self.assertIn("weak_sat_commitment", result["failure_labels"])
        self.assertFalse(
            {
                "bicl_criteria_present",
                "quality_tier_stated",
                "causal_quality_link_present",
            }
            & set(result["strengths"])
        )

    def test_sat_reasoner_unavailable_degrades_without_sat_strengths(self):
        with mock.patch.object(answer_comparator, "_SAT_REASONER_AVAILABLE", False):
            result = compare_answer(
                _sat_question(),
                "Balance and length indicate a very good quality assessment because "
                "the evidence supports it.",
                CONTEXT_PACKAGE,
            )

        self.assertFalse(
            {
                "bicl_criteria_present",
                "quality_tier_stated",
                "causal_quality_link_present",
            }
            & set(result["strengths"])
        )

    def test_compare_answer_is_deterministic_for_sat_strengths(self):
        question = _sat_question()
        answer = (
            "Balance, intensity, complexity and length point toward a very good "
            "quality assessment because the evidence is integrated."
        )

        first = compare_answer(question, answer, CONTEXT_PACKAGE)
        second = compare_answer(question, answer, CONTEXT_PACKAGE)

        self.assertEqual(first, second)

    def test_compare_answer_signature_is_unchanged(self):
        signature = inspect.signature(compare_answer)
        self.assertEqual(
            list(signature.parameters),
            ["question", "answer_text", "context_package", "strictness"],
        )
        self.assertEqual(signature.parameters["strictness"].default, "hard")


if __name__ == "__main__":
    unittest.main()

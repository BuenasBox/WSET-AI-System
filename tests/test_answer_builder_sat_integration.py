import unittest
from unittest.mock import patch

from tools.tutor import answer_builder


AUTHORITY_TERMS = (
    "I grade",
    "I score",
    "mark",
    "award",
    "pass",
    "fail",
    "I certify",
)


def _package(query: str, language: str = "en", act: str = "normal_explanation") -> dict:
    package = {
        "student_query": query,
        "language": language,
        "pedagogical_act": act,
        "retrieved_context": [],
        "governance": {
            "safe_for_examiner": False,
            "examiner_scoring_allowed": False,
        },
    }
    if act == "misconception_intervention":
        package["matched_misconception"] = {
            "misconception_id": "MC_TEST",
            "misconception": "Test misconception",
            "corrected_understanding": "Use evidence and mechanism rather than a shortcut.",
            "why_incorrect": "The claim skips the mechanism.",
        }
    return package


class AnswerBuilderSatIntegrationTests(unittest.TestCase):
    def test_english_sat_query_renders_sat_section(self) -> None:
        answer = answer_builder.render_answer(
            _package("Assess quality: high acidity, high tannin, long finish, balanced, high complexity."),
            "en",
        )
        self.assertIn("## SAT Quality Assessment", answer)

    def test_spanish_sat_query_renders_sat_section(self) -> None:
        answer = answer_builder.render_answer(
            _package(
                "Evalúa la calidad: acidez alta, tanino alto, final largo, equilibrado, complejidad alta.",
                "es",
            ),
            "es",
        )
        self.assertIn("## Evaluación de Calidad SAT", answer)

    def test_non_sat_theory_query_does_not_render_sat_section(self) -> None:
        answer = answer_builder.render_answer(
            _package("How does cool climate affect acidity?"),
            "en",
        )
        self.assertNotIn("SAT Quality Assessment", answer)
        self.assertNotIn("Evaluación de Calidad SAT", answer)

    def test_misconception_path_does_not_render_sat_section(self) -> None:
        answer = answer_builder.render_answer(
            _package(
                "Assess quality: high acidity, high tannin, long finish, balanced, high complexity.",
                "en",
                "misconception_intervention",
            ),
            "en",
        )
        self.assertNotIn("SAT Quality Assessment", answer)
        self.assertNotIn("Evaluación de Calidad SAT", answer)

    def test_sat_query_with_empty_observations_does_not_render_sat_section(self) -> None:
        answer = answer_builder.render_answer(
            _package("How do balance and intensity relate to quality?"),
            "en",
        )
        self.assertNotIn("SAT Quality Assessment", answer)
        self.assertNotIn("Evaluación de Calidad SAT", answer)

    def test_sat_output_has_no_examiner_authority_language(self) -> None:
        answer = answer_builder.render_answer(
            _package("Assess quality: high acidity, high tannin, long finish, balanced, high complexity."),
            "en",
        )
        lowered = answer.casefold()
        self.assertFalse(any(term.casefold() in lowered for term in AUTHORITY_TERMS))

    def test_tutor_disclaimer_remains_for_english_and_spanish_sat_queries(self) -> None:
        english = answer_builder.render_answer(
            _package("Assess quality: high acidity, long finish, balanced, high complexity."),
            "en",
        )
        spanish = answer_builder.render_answer(
            _package("Evalúa la calidad: acidez alta, final largo, equilibrado, complejidad alta.", "es"),
            "es",
        )
        self.assertIn(answer_builder.DISCLAIMER_EN, english)
        self.assertIn(answer_builder.DISCLAIMER_ES, spanish)

    def test_sat_rendering_is_deterministic(self) -> None:
        package = _package("Assess quality: high acidity, high tannin, long finish, balanced, high complexity.")
        self.assertEqual(
            answer_builder.render_answer(dict(package), "en"),
            answer_builder.render_answer(dict(package), "en"),
        )

    def test_sat_reasoner_unavailable_preserves_no_sat_section_behavior(self) -> None:
        package = _package("Assess quality: high acidity, high tannin, long finish, balanced, high complexity.")
        with patch.object(answer_builder, "_SAT_REASONER_AVAILABLE", False):
            answer = answer_builder.render_answer(package, "en")
        self.assertNotIn("SAT Quality Assessment", answer)
        self.assertNotIn("Evaluación de Calidad SAT", answer)
        self.assertIn("## 3. Cause/Effect Explanation", answer)


if __name__ == "__main__":
    unittest.main()

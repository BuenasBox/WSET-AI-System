import unittest
from pathlib import Path

from tools.tutor import sat_reasoner


AUTHORITY_TERMS = (
    "i grade",
    "i score",
    "mark",
    "award",
    "pass",
    "fail",
    "i certify",
)


class SatReasonerTests(unittest.TestCase):
    def test_is_sat_query_true_for_english_sat_query(self) -> None:
        self.assertTrue(
            sat_reasoner.is_sat_query(
                "Assess quality from high acidity, pronounced intensity and long finish.",
                "en",
            )
        )

    def test_is_sat_query_true_for_spanish_sat_query(self) -> None:
        self.assertTrue(
            sat_reasoner.is_sat_query(
                "Evalúa la calidad con acidez alta, final largo y complejidad alta.",
                "es",
            )
        )

    def test_is_sat_query_false_for_non_sat_theory_question(self) -> None:
        self.assertFalse(
            sat_reasoner.is_sat_query(
                "¿Qué método se usa para detener la fermentación en el vino de Oporto?",
                "es",
            )
        )

    def test_extract_sat_observations_spanish_aliases(self) -> None:
        cases = {
            "acidez alta": ("acidity", "high"),
            "tanino alto": ("tannin", "high"),
            "cuerpo medio": ("body", "medium"),
            "final largo": ("finish", "long"),
            "intensidad pronunciada": ("intensity", "pronounced"),
            "complejidad alta": ("complexity", "high"),
            "equilibrado": ("balance", "balanced"),
            "limpio": ("condition", "clean"),
            "defectuoso": ("condition", "faulty"),
            "desarrollado": ("development", "fully developed"),
        }
        for alias, expected in cases.items():
            with self.subTest(alias=alias):
                self.assertEqual(sat_reasoner.extract_sat_observations(alias, "es"), {expected[0]: expected[1]})

    def test_extract_sat_observations_english_aliases(self) -> None:
        cases = {
            "high acidity": ("acidity", "high"),
            "high tannin": ("tannin", "high"),
            "medium body": ("body", "medium"),
            "long finish": ("finish", "long"),
            "pronounced intensity": ("intensity", "pronounced"),
            "high complexity": ("complexity", "high"),
            "balanced": ("balance", "balanced"),
            "clean": ("condition", "clean"),
            "faulty": ("condition", "faulty"),
            "developed": ("development", "fully developed"),
        }
        for alias, expected in cases.items():
            with self.subTest(alias=alias):
                self.assertEqual(sat_reasoner.extract_sat_observations(alias, "en"), {expected[0]: expected[1]})

    def test_strong_bicl_evidence_favors_higher_quality(self) -> None:
        observations = {
            "balance": "balanced",
            "intensity": "pronounced",
            "complexity": "high",
            "finish": "long",
        }
        scored = sat_reasoner.score_quality_hypotheses(observations)
        best = max(scored, key=scored.get)
        self.assertIn(best, {"very_good", "outstanding"})

    def test_faulty_observation_discards_highest_tiers(self) -> None:
        scored = sat_reasoner.score_quality_hypotheses({"condition": "faulty"})
        surviving = sat_reasoner.discard_invalid_hypotheses(scored, {"condition": "faulty"})
        self.assertEqual(surviving["outstanding"], 0)
        self.assertEqual(surviving["very_good"], 0)

    def test_short_finish_discards_outstanding(self) -> None:
        scored = sat_reasoner.score_quality_hypotheses({"finish": "short"})
        surviving = sat_reasoner.discard_invalid_hypotheses(scored, {"finish": "short"})
        self.assertEqual(surviving["outstanding"], 0)

    def test_unbalanced_discards_outstanding(self) -> None:
        scored = sat_reasoner.score_quality_hypotheses({"balance": "unbalanced"})
        surviving = sat_reasoner.discard_invalid_hypotheses(scored, {"balance": "unbalanced"})
        self.assertEqual(surviving["outstanding"], 0)

    def test_empty_observations_formulation_returns_safe_fallback(self) -> None:
        self.assertEqual(
            sat_reasoner.formulate_quality_assessment({}, {}, "en"),
            "Insufficient observations to assess quality.",
        )
        self.assertEqual(
            sat_reasoner.formulate_quality_assessment({}, {}, "es"),
            "Observaciones insuficientes para evaluar la calidad.",
        )

    def test_spanish_formulation_uses_wset_style_without_authority_language(self) -> None:
        observations = {"balance": "balanced", "finish": "long", "complexity": "high"}
        scored = sat_reasoner.discard_invalid_hypotheses(
            sat_reasoner.score_quality_hypotheses(observations), observations
        )
        text = sat_reasoner.formulate_quality_assessment(observations, scored, "es")
        lowered = text.casefold()
        self.assertIn("calidad", lowered)
        self.assertIn("wset", lowered)
        self.assertIn("la evidencia apunta", lowered)
        self.assertFalse(any(term in lowered for term in AUTHORITY_TERMS))

    def test_english_formulation_uses_wset_style_without_authority_language(self) -> None:
        observations = {"balance": "balanced", "finish": "long", "complexity": "high"}
        scored = sat_reasoner.discard_invalid_hypotheses(
            sat_reasoner.score_quality_hypotheses(observations), observations
        )
        text = sat_reasoner.formulate_quality_assessment(observations, scored, "en")
        lowered = text.casefold()
        self.assertIn("quality", lowered)
        self.assertIn("wset", lowered)
        self.assertIn("the evidence suggests", lowered)
        self.assertFalse(any(term in lowered for term in AUTHORITY_TERMS))

    def test_full_pipeline_is_deterministic(self) -> None:
        query = "High acidity, pronounced intensity, high complexity, long finish and balanced structure."

        def run_pipeline() -> str:
            observations = sat_reasoner.extract_sat_observations(query, "en")
            scored = sat_reasoner.score_quality_hypotheses(observations)
            surviving = sat_reasoner.discard_invalid_hypotheses(scored, observations)
            return sat_reasoner.formulate_quality_assessment(observations, surviving, "en")

        self.assertEqual(run_pipeline(), run_pipeline())

    def test_governance_flags_are_never_true_in_sat_reasoner_source(self) -> None:
        source = Path(sat_reasoner.__file__).read_text(encoding="utf-8").casefold()
        self.assertNotIn("safe_for_examiner = true", source)
        self.assertNotIn("examiner_scoring_allowed = true", source)
        self.assertIs(sat_reasoner.SAFE_FOR_EXAMINER, False)
        self.assertIs(sat_reasoner.EXAMINER_SCORING_ALLOWED, False)


if __name__ == "__main__":
    unittest.main()

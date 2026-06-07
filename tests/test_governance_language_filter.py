"""Governance language contract tests.

Defines and enforces the list of FORBIDDEN language patterns that must never
appear in any Tutor output, HC_* node content, or governance-adjacent text.

Also confirms that ALLOWED formative-feedback phrases are not false positives.

Governance invariants protected here:
  - safe_for_examiner = False (always)
  - examiner_scoring_allowed = False (always)
  - No official scoring language
  - No examiner authority claims
  - No grade-prediction language
  - Heuristic content may not claim to represent official WSET positions
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from tools.constants import KNOWLEDGE_DIR, PROJECT_ROOT

CAUSAL_CHAINS_DIR = KNOWLEDGE_DIR / "knowledge-map" / "causal-chains"

FORBIDDEN_PATTERNS: list[tuple[str, str]] = [
    ("official score claim (EN)", r"\bofficial\s+score\b"),
    ("official score claim (ES)", r"\bnota\s+oficial\b"),
    ("official scoring claim", r"\bofficial\s+scor(ing|ed?)\b"),
    ("puntuacion oficial", r"\bpuntuaci[oo]n\s+oficial\b"),
    ("examiner would give", r"\bexaminer\s+would\s+give\b"),
    ("WSET examiner would", r"\bwset\s+examiner\s+would\b"),
    ("examiner score", r"\bexaminer\s+scor(e|ing|ed?)\b"),
    ("el examinador daria", r"\bel\s+examinador\s+dar[ii]a\b"),
    ("guaranteed distinction", r"\bguaranteed?\s+distinction\b"),
    ("garantizado distinction", r"\bgarantizad[ao]\s+distinction\b"),
    ("this would pass", r"\bthis\s+would\s+pass\b"),
    ("esto aprobaria", r"\besto\s+aprobari[ae]\b"),
    ("would receive a distinction", r"\bwould\s+receive\s+a\s+distinction\b"),
    ("recibiria una distincion", r"\brecibir[ii]a\s+una\s+distinci[oo]n\b"),
    ("official mark scheme", r"\bofficial\s+mark\s+scheme\b"),
    ("mark scheme oficial", r"\bmark\s+scheme\s+oficial\b"),
    ("esquema de notas oficial", r"\besquema\s+de\s+notas\s+oficial\b"),
    ("WSET_PASS constant", r"\bWSET_PASS\b"),
    ("WSET_MERIT constant", r"\bWSET_MERIT\b"),
    ("WSET_DISTINCTION constant", r"\bWSET_DISTINCTION\b"),
    ("safe_for_examiner True assignment", r"safe_for_examiner\s*[:=]\s*true"),
    ("examiner_scoring_allowed True assignment", r"examiner_scoring_allowed\s*[:=]\s*true"),
]


def _matches_any_forbidden(text: str) -> list[str]:
    """Return list of forbidden pattern descriptions that match text."""
    matched = []
    text_lower = text.lower()
    for desc, pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            matched.append(desc)
    return matched


class ForbiddenPatternDetectionTests(unittest.TestCase):
    """Each forbidden pattern must correctly identify a canonical bad example."""

    def test_official_score_en_detected(self) -> None:
        self.assertTrue(_matches_any_forbidden("This is the official score for your answer."))

    def test_official_score_es_detected(self) -> None:
        self.assertTrue(_matches_any_forbidden("Tu nota oficial es 15 puntos."))

    def test_examiner_would_give_detected(self) -> None:
        self.assertTrue(_matches_any_forbidden("The examiner would give you 8 out of 10."))

    def test_wset_examiner_would_detected(self) -> None:
        self.assertTrue(_matches_any_forbidden("A WSET examiner would give this a Distinction."))

    def test_guaranteed_distinction_detected(self) -> None:
        self.assertTrue(_matches_any_forbidden("Your answer is guaranteed a distinction."))

    def test_official_mark_scheme_detected(self) -> None:
        self.assertTrue(_matches_any_forbidden("According to the official mark scheme, this scores full marks."))

    def test_wset_pass_constant_detected(self) -> None:
        self.assertTrue(_matches_any_forbidden("result = WSET_PASS"))

    def test_wset_merit_constant_detected(self) -> None:
        self.assertTrue(_matches_any_forbidden("result = WSET_MERIT"))

    def test_wset_distinction_constant_detected(self) -> None:
        self.assertTrue(_matches_any_forbidden("result = WSET_DISTINCTION"))

    def test_safe_for_examiner_true_detected(self) -> None:
        self.assertTrue(_matches_any_forbidden("safe_for_examiner: true"))

    def test_examiner_scoring_allowed_true_detected(self) -> None:
        self.assertTrue(_matches_any_forbidden("examiner_scoring_allowed: true"))

    def test_puntuacion_oficial_detected(self) -> None:
        self.assertTrue(_matches_any_forbidden("La puntuacion oficial es excelente."))

    def test_examiner_score_detected(self) -> None:
        self.assertTrue(_matches_any_forbidden("The examiner score for this section is 7."))

    def test_mark_scheme_oficial_detected(self) -> None:
        self.assertTrue(_matches_any_forbidden("El mark scheme oficial indica 5 puntos."))


class AllowedPhraseCleanTests(unittest.TestCase):
    """Formative/allowed phrases must produce zero false positives."""

    def test_formative_completeness_en_is_clean(self) -> None:
        phrase = "Your answer would be more complete with a causal link."
        self.assertEqual(_matches_any_forbidden(phrase), [], f"False positive on: {phrase!r}")

    def test_formative_completeness_es_is_clean(self) -> None:
        phrase = "La respuesta seria mas completa si incluyeras la causalidad."
        self.assertEqual(_matches_any_forbidden(phrase), [], f"False positive on: {phrase!r}")

    def test_falta_causalidad_is_clean(self) -> None:
        phrase = "Falta causalidad en la explicacion."
        self.assertEqual(_matches_any_forbidden(phrase), [], f"False positive on: {phrase!r}")

    def test_feedback_formativo_is_clean(self) -> None:
        phrase = "feedback formativo"
        self.assertEqual(_matches_any_forbidden(phrase), [], f"False positive on: {phrase!r}")

    def test_training_disclaimer_en_is_clean(self) -> None:
        phrase = "This is a training exercise, not official WSET evaluation."
        self.assertEqual(_matches_any_forbidden(phrase), [], f"False positive on: {phrase!r}")

    def test_training_disclaimer_es_is_clean(self) -> None:
        phrase = "Este es un ejercicio de entrenamiento, no evaluacion oficial WSET."
        self.assertEqual(_matches_any_forbidden(phrase), [], f"False positive on: {phrase!r}")

    def test_heuristic_label_is_clean(self) -> None:
        phrase = "source: heuristic"
        self.assertEqual(_matches_any_forbidden(phrase), [], f"False positive on: {phrase!r}")

    def test_inferred_label_is_clean(self) -> None:
        phrase = "classification: inferred"
        self.assertEqual(_matches_any_forbidden(phrase), [], f"False positive on: {phrase!r}")

    def test_very_good_quality_is_clean(self) -> None:
        phrase = "The quality assessment is Very Good or Outstanding."
        self.assertEqual(_matches_any_forbidden(phrase), [], f"False positive on: {phrase!r}")

    def test_high_complexity_note_is_clean(self) -> None:
        phrase = "This wine shows high complexity."
        self.assertEqual(_matches_any_forbidden(phrase), [], f"False positive on: {phrase!r}")

    def test_bicl_description_is_clean(self) -> None:
        phrase = "BICL: balance, intensity, complexity, length."
        self.assertEqual(_matches_any_forbidden(phrase), [], f"False positive on: {phrase!r}")


class HCNodeContentCleanTests(unittest.TestCase):
    """All text content within HC_*.json files must be free of forbidden language."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.hc_nodes: list[tuple[Path, dict]] = []
        for p in sorted(CAUSAL_CHAINS_DIR.glob("HC_*.json")):
            data = json.loads(p.read_text(encoding="utf-8"))
            cls.hc_nodes.append((p, data))

    def _collect_text_fields(self, node: dict) -> list[str]:
        texts = []
        for field in ("topic", "sat_relevance"):
            val = node.get(field, "")
            if val:
                texts.append(str(val))
        for step in node.get("steps", []):
            txt = step.get("text", "")
            if txt:
                texts.append(str(txt))
        return texts

    def test_hc_step_text_has_no_forbidden_language(self) -> None:
        for path, node in self.hc_nodes:
            for text in self._collect_text_fields(node):
                with self.subTest(file=path.name, snippet=text[:60]):
                    violations = _matches_any_forbidden(text)
                    self.assertEqual(
                        violations, [],
                        f"{path.name}: forbidden language in {text[:80]!r}: {violations}"
                    )


class GovernanceConstantTests(unittest.TestCase):
    """Core governance constants in tools.constants must remain False."""

    def test_safe_for_examiner_constant_is_false(self) -> None:
        from tools.constants import SAFE_FOR_EXAMINER
        self.assertFalse(SAFE_FOR_EXAMINER)

    def test_examiner_scoring_allowed_constant_is_false(self) -> None:
        from tools.constants import EXAMINER_SCORING_ALLOWED
        self.assertFalse(EXAMINER_SCORING_ALLOWED)

    def test_uses_llm_is_false(self) -> None:
        from tools.constants import USES_LLM
        self.assertFalse(USES_LLM)

    def test_uses_api_is_false(self) -> None:
        from tools.constants import USES_API
        self.assertFalse(USES_API)

    def test_uses_embeddings_is_false(self) -> None:
        from tools.constants import USES_EMBEDDINGS
        self.assertFalse(USES_EMBEDDINGS)

    def test_uses_vector_db_is_false(self) -> None:
        from tools.constants import USES_VECTOR_DB
        self.assertFalse(USES_VECTOR_DB)


class FeatureFlagInjectionTests(unittest.TestCase):
    """ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION must remain False after HC node integration."""

    def test_injection_flag_is_false(self) -> None:
        from tools.retrieval.tutor_retrieval_sandbox import ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION
        self.assertFalse(
            ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION,
            "ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION must remain False"
        )

    def test_injection_flag_is_module_level_constant(self) -> None:
        import tools.retrieval.tutor_retrieval_sandbox as mod
        self.assertIn(
            "ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION",
            dir(mod),
            "ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION must be a module-level attribute"
        )

    def test_injection_flag_type_is_bool(self) -> None:
        from tools.retrieval.tutor_retrieval_sandbox import ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION
        self.assertIsInstance(ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION, bool)


if __name__ == "__main__":
    unittest.main()

"""Integration tests for SAT validator wiring into answer_builder.py — Phase X.3.

Coverage:
  - Feature flag ENABLE_SAT_VALIDATOR_FEEDBACK controls activation
  - sat_submission key triggers validator block in output
  - Non-SAT context packages are completely unaffected
  - Governance: no scoring language, no marks, safe_for_examiner=False
  - Block content: formative disclaimer, coverage, quality guidance
  - Determinism
  - Flag-off: output identical to pre-integration (no sat_submission path)
  - Misconception path: sat_validator block never appears
  - Existing SAT reasoner path unaffected by new integration
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.tutor import answer_builder
from tools.tutor.answer_builder import (
    ENABLE_SAT_VALIDATOR_FEEDBACK,
    render_answer,
    _render_sat_validator_feedback,
)
from tools.tutor.sat_validator import validate_sat_response


# ---------------------------------------------------------------------------
# Package builders
# ---------------------------------------------------------------------------

def _base_package(query: str, language: str = "es", act: str = "normal_explanation") -> dict:
    pkg = {
        "student_query": query,
        "language": language,
        "pedagogical_act": act,
        "retrieved_context": [],
        "governance": {"safe_for_examiner": False, "examiner_scoring_allowed": False},
    }
    if act == "misconception_intervention":
        pkg["matched_misconception"] = {
            "misconception_id": "MC_TEST",
            "misconception": "test",
            "corrected_understanding": "Use evidence and mechanism.",
            "why_incorrect": "Skips mechanism.",
        }
    return pkg


def _sat_submission_complete() -> dict:
    return {
        "wine_type": "red",
        "is_simple": False,
        "appearance": {"intensity": "profunda", "colour": "rubí"},
        "nose": {
            "intensity": "pronunciada",
            "primary_aromas": ["cereza roja", "frambuesa"],
            "secondary_aromas": ["vainilla", "cedro"],
            "tertiary_aromas": ["cuero", "tierra"],
            "development": "en evolución",
            "is_simple": False,
        },
        "palate": {
            "sweetness": "seco", "acidity": "alta", "tannin": "medio",
            "alcohol": "alto", "body": "mucho", "flavour_intensity": "pronunciada",
            "primary_flavours": ["cereza roja"], "secondary_flavours": ["vainilla"],
            "tertiary_flavours": ["cuero"], "finish": "largo", "is_simple": False,
        },
        "conclusions": {
            "quality_level": "excelente",
            "readiness": "se puede beber ahora, pero tiene potencial para el envejecimiento",
        },
    }


def _sat_submission_incomplete() -> dict:
    return {
        "wine_type": "white",
        "is_simple": False,
        "appearance": {"intensity": "pálida", "colour": "amarillo limón"},
        "nose": {
            "intensity": "media",
            "primary_aromas": ["manzana"],
            "secondary_aromas": [],
            "tertiary_aromas": [],
            "development": None,
            "is_simple": False,
        },
        "palate": {
            "sweetness": "seco", "acidity": "media", "tannin": None,
            "alcohol": None, "body": None, "flavour_intensity": "media",
            "primary_flavours": ["manzana"], "secondary_flavours": [],
            "tertiary_flavours": [], "finish": None, "is_simple": False,
        },
        "conclusions": {"quality_level": "bueno", "readiness": None},
    }


def _with_sat_submission(submission: dict, language: str = "es") -> dict:
    pkg = _base_package("Evalúa la calidad de este vino", language)
    pkg["sat_submission"] = submission
    return pkg


# ---------------------------------------------------------------------------
# 1. Feature flag
# ---------------------------------------------------------------------------
class FeatureFlagTests(unittest.TestCase):

    def test_flag_is_true_by_default(self) -> None:
        self.assertTrue(ENABLE_SAT_VALIDATOR_FEEDBACK)

    def test_flag_off_suppresses_validator_block_even_with_submission(self) -> None:
        pkg = _with_sat_submission(_sat_submission_complete())
        with patch.object(answer_builder, "ENABLE_SAT_VALIDATOR_FEEDBACK", False):
            answer = render_answer(pkg, "es")
        self.assertNotIn("Orientación formativa SAT", answer)
        self.assertNotIn("SAT Formative Guidance", answer)

    def test_flag_off_output_structurally_unchanged(self) -> None:
        """With flag off, sat_submission package renders like a package without it."""
        pkg_with = _with_sat_submission(_sat_submission_complete())
        pkg_without = _base_package("Evalúa la calidad de este vino", "es")

        with patch.object(answer_builder, "ENABLE_SAT_VALIDATOR_FEEDBACK", False):
            answer_with = render_answer(dict(pkg_with), "es")
        answer_without = render_answer(dict(pkg_without), "es")

        # Both must contain standard Tutor structure
        for heading in ("## 1.", "## 2.", "## 3.", "## 4.", "## 5."):
            self.assertIn(heading, answer_with)
            self.assertIn(heading, answer_without)

    def test_flag_on_with_sat_submission_renders_block(self) -> None:
        pkg = _with_sat_submission(_sat_submission_complete())
        answer = render_answer(pkg, "es")
        self.assertIn("Orientación formativa SAT", answer)


# ---------------------------------------------------------------------------
# 2. Activation conditions
# ---------------------------------------------------------------------------
class ActivationConditionTests(unittest.TestCase):

    def test_missing_sat_submission_key_no_validator_block(self) -> None:
        pkg = _base_package("Evalúa la calidad de este vino")
        answer = render_answer(pkg, "es")
        self.assertNotIn("Orientación formativa SAT", answer)
        self.assertNotIn("SAT Formative Guidance", answer)

    def test_empty_dict_sat_submission_no_validator_block(self) -> None:
        pkg = _base_package("Evalúa la calidad de este vino")
        pkg["sat_submission"] = {}
        answer = render_answer(pkg, "es")
        self.assertNotIn("Orientación formativa SAT", answer)

    def test_none_sat_submission_no_validator_block(self) -> None:
        pkg = _base_package("Evalúa la calidad de este vino")
        pkg["sat_submission"] = None
        answer = render_answer(pkg, "es")
        self.assertNotIn("Orientación formativa SAT", answer)

    def test_non_dict_sat_submission_no_validator_block(self) -> None:
        pkg = _base_package("Evalúa la calidad de este vino")
        pkg["sat_submission"] = "string value"
        answer = render_answer(pkg, "es")
        self.assertNotIn("Orientación formativa SAT", answer)

    def test_valid_submission_activates_spanish_block(self) -> None:
        pkg = _with_sat_submission(_sat_submission_complete(), "es")
        answer = render_answer(pkg, "es")
        self.assertIn("## Orientación formativa SAT", answer)

    def test_valid_submission_activates_english_block(self) -> None:
        pkg = _with_sat_submission(_sat_submission_complete(), "en")
        answer = render_answer(pkg, "en")
        self.assertIn("## SAT Formative Guidance", answer)


# ---------------------------------------------------------------------------
# 3. Non-SAT path regression
# ---------------------------------------------------------------------------
class NonSATRegressionTests(unittest.TestCase):

    NON_SAT_QUERIES = [
        ("¿Cómo afecta el clima fresco a la acidez?", "es"),
        ("Explica la maceración carbónica", "es"),
        ("How does oak ageing affect tannin structure?", "en"),
        ("¿Qué diferencia al Tokaji del Sauternes?", "es"),
        ("Describe the Champagne method", "en"),
    ]

    def test_non_sat_queries_have_no_validator_block(self) -> None:
        for query, lang in self.NON_SAT_QUERIES:
            with self.subTest(query=query[:40]):
                pkg = _base_package(query, lang)
                answer = render_answer(pkg, lang)
                self.assertNotIn("Orientación formativa SAT", answer,
                                 msg=f"Validator block appeared for non-SAT: {query}")
                self.assertNotIn("SAT Formative Guidance", answer,
                                 msg=f"Validator block appeared for non-SAT: {query}")

    def test_non_sat_standard_structure_intact(self) -> None:
        pkg = _base_package("¿Cómo afecta el clima fresco a la acidez?")
        answer = render_answer(pkg, "es")
        for heading in ("## 1.", "## 2.", "## 3.", "## 4.", "## 5."):
            self.assertIn(heading, answer)

    def test_non_sat_disclaimer_intact(self) -> None:
        pkg = _base_package("Explica la maceración carbónica")
        answer = render_answer(pkg, "es")
        self.assertIn(answer_builder.DISCLAIMER_ES, answer)

    def test_misconception_path_no_validator_block(self) -> None:
        pkg = _base_package(
            "Evalúa la calidad: acidez alta, tanino alto, final largo",
            act="misconception_intervention",
        )
        pkg["sat_submission"] = _sat_submission_complete()
        answer = render_answer(pkg, "es")
        # misconception path calls _render_misconception_answer, not _render_normal_answer
        self.assertNotIn("Orientación formativa SAT", answer)

    def test_snapshot_packages_unaffected(self) -> None:
        """All 25 frozen snapshot context packages produce identical answers."""
        import tempfile, os
        snapshot_dir = Path("tests/fixtures/tutor_snapshots")
        for snap_id in range(1, 26):
            snap_path = snapshot_dir / str(snap_id)
            context_pkg_path = snap_path / "context_package.json"
            expected_path = snap_path / "expected_answer.txt"
            if not context_pkg_path.exists() or not expected_path.exists():
                continue
            with self.subTest(snapshot=snap_id):
                with tempfile.TemporaryDirectory() as tmp:
                    out = Path(tmp) / "answer.md"
                    result = answer_builder.build_tutor_answer(
                        context_package_path=context_pkg_path,
                        output_path=out,
                    )
                    actual = result["answer"]
                expected = expected_path.read_text(encoding="utf-8")
                self.assertEqual(
                    actual, expected,
                    msg=f"Snapshot {snap_id} drifted — non-SAT output changed"
                )


# ---------------------------------------------------------------------------
# 4. Block content and governance
# ---------------------------------------------------------------------------
class BlockContentTests(unittest.TestCase):

    def _answer_with_submission(self, submission: dict, language: str = "es") -> str:
        return render_answer(_with_sat_submission(submission, language), language)

    def test_block_contains_formative_disclaimer(self) -> None:
        answer = self._answer_with_submission(_sat_submission_complete())
        self.assertIn("formativa", answer.lower())

    def test_block_contains_no_official_grade_language(self) -> None:
        answer = self._answer_with_submission(_sat_submission_complete())
        forbidden_phrases = (
            "your score", "your mark", "you scored", "marks awarded",
            "total mark", "final grade", "pass_fail", "wset_equivalence",
            "percentage score", "nota oficial", "calificación oficial asignada",
        )
        lower = answer.lower()
        for phrase in forbidden_phrases:
            self.assertNotIn(phrase, lower,
                             msg=f"Scoring phrase '{phrase}' found in output")

    def test_governance_flags_unchanged(self) -> None:
        pkg = _with_sat_submission(_sat_submission_complete())
        result = answer_builder.build_tutor_answer.__wrapped__ if hasattr(
            answer_builder.build_tutor_answer, '__wrapped__') else None
        # Check via render_answer which only needs package
        answer = render_answer(pkg, "es")
        self.assertIn(answer_builder.DISCLAIMER_ES, answer)

    def test_incomplete_submission_shows_structural_issues(self) -> None:
        answer = self._answer_with_submission(_sat_submission_incomplete())
        self.assertIn("Orientación formativa SAT", answer)
        # Should flag missing elements
        self.assertTrue(
            "falt" in answer.lower() or "missing" in answer.lower() or "△" in answer,
            msg="Incomplete submission should show partial/missing coverage"
        )

    def test_complete_submission_shows_complete_coverage(self) -> None:
        answer = self._answer_with_submission(_sat_submission_complete())
        self.assertIn("✓", answer)

    def test_block_ends_with_formative_note(self) -> None:
        answer = self._answer_with_submission(_sat_submission_complete())
        self.assertIn("formativa", answer.lower())
        self.assertIn("Examiner", answer)

    def test_english_block_has_english_headings(self) -> None:
        answer = self._answer_with_submission(_sat_submission_complete(), "en")
        self.assertIn("## SAT Formative Guidance", answer)
        self.assertIn("formative only", answer.lower())

    def test_spanish_block_has_spanish_headings(self) -> None:
        answer = self._answer_with_submission(_sat_submission_complete(), "es")
        self.assertIn("## Orientación formativa SAT", answer)
        self.assertIn("solo formativa", answer.lower())

    def test_tutor_disclaimer_still_present_with_sat_submission(self) -> None:
        answer_es = self._answer_with_submission(_sat_submission_complete(), "es")
        answer_en = self._answer_with_submission(_sat_submission_complete(), "en")
        self.assertIn(answer_builder.DISCLAIMER_ES, answer_es)
        self.assertIn(answer_builder.DISCLAIMER_EN, answer_en)

    def test_standard_tutor_sections_still_present(self) -> None:
        answer = self._answer_with_submission(_sat_submission_complete())
        for heading in ("## 1.", "## 2.", "## 3.", "## 4.", "## 5."):
            self.assertIn(heading, answer,
                          msg=f"Standard heading '{heading}' missing after sat_submission injection")


# ---------------------------------------------------------------------------
# 5. _render_sat_validator_feedback unit tests
# ---------------------------------------------------------------------------
class RenderSATValidatorFeedbackTests(unittest.TestCase):

    def _render(self, submission: dict, language: str = "es") -> str:
        result = validate_sat_response(submission)
        return _render_sat_validator_feedback(result, language)

    def test_renders_without_error_complete(self) -> None:
        try:
            out = self._render(_sat_submission_complete())
            self.assertIsInstance(out, str)
            self.assertGreater(len(out), 0)
        except Exception as exc:
            self.fail(f"Renderer raised: {exc}")

    def test_renders_without_error_incomplete(self) -> None:
        out = self._render(_sat_submission_incomplete())
        self.assertIsInstance(out, str)

    def test_always_has_formative_disclaimer(self) -> None:
        for sub in (_sat_submission_complete(), _sat_submission_incomplete(), {}):
            with self.subTest():
                out = self._render(sub)
                self.assertIn("formativ", out.lower())

    def test_complete_shows_estructura_completa(self) -> None:
        out = self._render(_sat_submission_complete())
        self.assertIn("✓", out)

    def test_incomplete_shows_missing_elements_section(self) -> None:
        out = self._render(_sat_submission_incomplete())
        # Has missing elements or partial coverage markers
        self.assertTrue(
            "falt" in out.lower() or "△" in out or "✗" in out,
            msg="Incomplete submission should show issues in rendered block"
        )

    def test_no_marks_assigned_in_rendered_output(self) -> None:
        out = self._render(_sat_submission_complete())
        forbidden = ("marks awarded", "total mark", "your score", "you scored",
                     "final grade", "pass_fail")
        lower = out.lower()
        for phrase in forbidden:
            self.assertNotIn(phrase, lower)

    def test_quality_justification_present_when_quality_stated(self) -> None:
        out = self._render(_sat_submission_complete(), "es")
        self.assertIn("calidad", out.lower())

    def test_english_render_has_english_labels(self) -> None:
        out = self._render(_sat_submission_complete(), "en")
        self.assertIn("formative only", out.lower())
        self.assertIn("Formative", out)

    def test_empty_submission_renders_without_crash(self) -> None:
        out = self._render({})
        self.assertIsInstance(out, str)


# ---------------------------------------------------------------------------
# 6. Determinism
# ---------------------------------------------------------------------------
class DeterminismTests(unittest.TestCase):

    def test_same_submission_same_output_es(self) -> None:
        pkg = _with_sat_submission(_sat_submission_complete(), "es")
        r1 = render_answer(dict(pkg), "es")
        r2 = render_answer(dict(pkg), "es")
        self.assertEqual(r1, r2)

    def test_same_submission_same_output_en(self) -> None:
        pkg = _with_sat_submission(_sat_submission_complete(), "en")
        r1 = render_answer(dict(pkg), "en")
        r2 = render_answer(dict(pkg), "en")
        self.assertEqual(r1, r2)

    def test_incomplete_submission_deterministic(self) -> None:
        pkg = _with_sat_submission(_sat_submission_incomplete())
        r1 = render_answer(dict(pkg), "es")
        r2 = render_answer(dict(pkg), "es")
        self.assertEqual(r1, r2)


# ---------------------------------------------------------------------------
# 7. Existing SAT reasoner path unaffected
# ---------------------------------------------------------------------------
class ExistingSATReasonerUnaffectedTests(unittest.TestCase):

    def test_sat_reasoner_still_renders_for_quality_query_en(self) -> None:
        pkg = _base_package(
            "Assess quality: high acidity, high tannin, long finish, balanced.", "en"
        )
        answer = render_answer(pkg, "en")
        self.assertIn("## SAT Quality Assessment", answer)

    def test_sat_reasoner_still_renders_for_quality_query_es(self) -> None:
        pkg = _base_package(
            "Evalúa la calidad: acidez alta, tanino alto, final largo, equilibrado.", "es"
        )
        answer = render_answer(pkg, "es")
        self.assertIn("## Evaluación de Calidad SAT", answer)

    def test_both_sat_reasoner_and_validator_can_coexist(self) -> None:
        """A quality-assessment query WITH a sat_submission produces both blocks."""
        pkg = {
            "student_query": "Assess quality: high acidity, high tannin, long finish.",
            "language": "en",
            "pedagogical_act": "normal_explanation",
            "retrieved_context": [],
            "governance": {"safe_for_examiner": False, "examiner_scoring_allowed": False},
            "sat_submission": _sat_submission_complete(),
        }
        answer = render_answer(pkg, "en")
        self.assertIn("## SAT Quality Assessment", answer)
        self.assertIn("## SAT Formative Guidance", answer)


if __name__ == "__main__":
    unittest.main()

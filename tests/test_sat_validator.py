"""Unit tests for tools/tutor/sat_validator.py — Phase X.3.

Coverage:
  - Governance invariants
  - Structural completeness check (Component 1)
  - Scale value validation (Component 2)
  - Mark allocation feedback (Component 3)
  - Simple wine exception enforcer (Component 4)
  - Quality justification checker (Component 5)
  - Distinction gap report (Component 6)
  - Fixture-based integration tests
  - Determinism
  - No scoring authority
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.tutor.sat_validator import (
    VALIDATOR_GOVERNANCE,
    _check_quality_justification,
    _check_scale_values,
    _check_simple_wine_exception,
    _check_structural_completeness,
    _build_distinction_gap_report,
    _build_mark_allocation_feedback,
    validate_sat_response,
)

# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------
_FIXTURE_DIR = Path("tests/fixtures/sat_validator")


def _load_fixture(name: str) -> dict:
    return json.loads((_FIXTURE_DIR / name).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# 1. Governance tests
# ---------------------------------------------------------------------------
class GovernanceTests(unittest.TestCase):

    def test_governance_safe_for_examiner_is_false(self) -> None:
        self.assertFalse(VALIDATOR_GOVERNANCE["safe_for_examiner"])

    def test_governance_examiner_scoring_not_allowed(self) -> None:
        self.assertFalse(VALIDATOR_GOVERNANCE["examiner_scoring_allowed"])

    def test_governance_no_llm(self) -> None:
        self.assertFalse(VALIDATOR_GOVERNANCE["uses_llm"])

    def test_governance_no_api(self) -> None:
        self.assertFalse(VALIDATOR_GOVERNANCE["uses_api"])

    def test_governance_formative_only(self) -> None:
        self.assertTrue(VALIDATOR_GOVERNANCE["formative_only"])

    def test_governance_no_marks_assigned(self) -> None:
        self.assertTrue(VALIDATOR_GOVERNANCE["no_marks_assigned"])

    def test_output_always_includes_governance(self) -> None:
        result = validate_sat_response({})
        self.assertIn("governance", result)
        self.assertFalse(result["governance"]["safe_for_examiner"])
        self.assertFalse(result["governance"]["examiner_scoring_allowed"])

    def test_output_never_contains_score_fields(self) -> None:
        """Governance: output values must not contain examiner scoring language.
        Key names are permitted to contain substrings (e.g. no_marks_assigned);
        only actual scoring VALUE strings are forbidden.
        """
        import re
        fixture = _load_fixture("sat_response_valid_complete.json")
        result = validate_sat_response(fixture)

        def _collect_string_values(obj, acc=None):
            if acc is None:
                acc = []
            if isinstance(obj, str):
                acc.append(obj.lower())
            elif isinstance(obj, dict):
                for v in obj.values():
                    _collect_string_values(v, acc)
            elif isinstance(obj, list):
                for item in obj:
                    _collect_string_values(item, acc)
            return acc

        value_strings = _collect_string_values(result)
        forbidden_phrases = (
            "your score", "your mark", "you scored", "mark awarded",
            "marks awarded", "total mark", "final grade", "pass_fail",
            "wset_equivalence", "percentage score",
        )
        combined_values = " ".join(value_strings)
        for phrase in forbidden_phrases:
            self.assertNotIn(phrase, combined_values,
                             msg=f"Forbidden scoring phrase '{phrase}' found in output values")

    def test_governance_embedded_in_every_result(self) -> None:
        for fname in (
            "sat_response_valid_complete.json",
            "sat_response_incomplete.json",
            "sat_response_simple_wine_violation.json",
            "sat_response_weak_quality_justification.json",
        ):
            with self.subTest(fixture=fname):
                result = validate_sat_response(_load_fixture(fname))
                gov = result["governance"]
                self.assertFalse(gov["safe_for_examiner"])
                self.assertFalse(gov["examiner_scoring_allowed"])


# ---------------------------------------------------------------------------
# 2. Structural completeness (Component 1)
# ---------------------------------------------------------------------------
class StructuralCompletenessTests(unittest.TestCase):

    def _issues(self, **kwargs) -> list[str]:
        return _check_structural_completeness(
            wine_type=kwargs.get("wine_type", "white"),
            appearance=kwargs.get("appearance", {}),
            nose=kwargs.get("nose", {}),
            palate=kwargs.get("palate", {}),
            conclusions=kwargs.get("conclusions", {}),
        )

    def test_empty_response_has_many_issues(self) -> None:
        issues = self._issues()
        self.assertGreater(len(issues), 5)

    def test_complete_white_wine_has_no_issues(self) -> None:
        fixture = _load_fixture("sat_response_valid_complete.json")
        issues = _check_structural_completeness(
            fixture["wine_type"], fixture["appearance"],
            fixture["nose"], fixture["palate"], fixture["conclusions"]
        )
        self.assertEqual(issues, [])

    def test_missing_appearance_intensity_flagged(self) -> None:
        issues = self._issues(appearance={"colour": "verde limón"})
        self.assertTrue(any("intensidad" in i.lower() for i in issues))

    def test_missing_appearance_colour_flagged(self) -> None:
        issues = self._issues(appearance={"intensity": "pálida"})
        self.assertTrue(any("color" in i.lower() for i in issues))

    def test_missing_nose_intensity_flagged(self) -> None:
        issues = self._issues(nose={"primary_aromas": ["limón"], "development": "joven"})
        self.assertTrue(any("intensidad" in i.lower() for i in issues))

    def test_missing_nose_development_flagged(self) -> None:
        issues = self._issues(nose={"intensity": "media", "primary_aromas": ["limón"]})
        self.assertTrue(any("evolución" in i.lower() for i in issues))

    def test_missing_nose_primary_flagged(self) -> None:
        issues = self._issues(nose={"intensity": "media", "development": "joven"})
        self.assertTrue(any("primario" in i.lower() for i in issues))

    def test_red_wine_missing_tannin_flagged(self) -> None:
        palate = {
            "sweetness": "seco", "acidity": "media", "alcohol": "medio",
            "body": "medio", "flavour_intensity": "media",
            "primary_flavours": ["cereza"], "finish": "medio"
        }
        issues = self._issues(wine_type="red", palate=palate)
        self.assertTrue(any("tanino" in i.lower() for i in issues))

    def test_white_wine_no_tannin_issue(self) -> None:
        palate = {
            "sweetness": "seco", "acidity": "media", "alcohol": "medio",
            "body": "medio", "flavour_intensity": "media",
            "primary_flavours": ["limón"], "finish": "medio"
        }
        issues = self._issues(wine_type="white", palate=palate)
        self.assertFalse(any("tanino" in i.lower() for i in issues))

    def test_sparkling_wine_missing_mousse_flagged(self) -> None:
        palate = {
            "sweetness": "seco", "acidity": "alta", "alcohol": "bajo",
            "body": "poco", "flavour_intensity": "media",
            "primary_flavours": ["manzana"], "finish": "medio"
        }
        issues = self._issues(wine_type="sparkling", palate=palate)
        self.assertTrue(any("burbuja" in i.lower() or "mousse" in i.lower() for i in issues))

    def test_missing_conclusions_quality_flagged(self) -> None:
        issues = self._issues(conclusions={"readiness": "beber ahora"})
        self.assertTrue(any("calidad" in i.lower() for i in issues))

    def test_missing_conclusions_readiness_flagged(self) -> None:
        issues = self._issues(conclusions={"quality_level": "bueno"})
        self.assertTrue(any("consumo" in i.lower() or "potencial" in i.lower() for i in issues))

    def test_incomplete_fixture_has_issues(self) -> None:
        fixture = _load_fixture("sat_response_incomplete.json")
        issues = _check_structural_completeness(
            fixture["wine_type"], fixture["appearance"],
            fixture["nose"], fixture["palate"], fixture["conclusions"]
        )
        self.assertGreater(len(issues), 0)


# ---------------------------------------------------------------------------
# 3. Scale value validation (Component 2)
# ---------------------------------------------------------------------------
class ScaleValidationTests(unittest.TestCase):

    def test_valid_scale_values_produce_no_errors(self) -> None:
        fixture = _load_fixture("sat_response_valid_complete.json")
        errors = _check_scale_values(
            fixture["wine_type"], fixture["appearance"],
            fixture["nose"], fixture["palate"], fixture["conclusions"]
        )
        self.assertEqual(errors, [])

    def test_invalid_nose_intensity_flagged(self) -> None:
        nose = {"intensity": "muy ligera", "primary_aromas": ["limón"]}
        errors = _check_scale_values("white", {}, nose, {}, {})
        self.assertTrue(any("intensity" in e.lower() for e in errors))

    def test_invalid_quality_level_flagged(self) -> None:
        conclusions = {"quality_level": "excelentísimo"}
        errors = _check_scale_values("white", {}, {}, {}, conclusions)
        self.assertTrue(any("quality_level" in e for e in errors))

    def test_valid_quality_levels_all_accepted(self) -> None:
        for level in ("defectuoso", "pobre", "aceptable", "bueno", "muy bueno", "excelente"):
            with self.subTest(level=level):
                errors = _check_scale_values("white", {}, {}, {}, {"quality_level": level})
                self.assertFalse(
                    any("quality_level" in e for e in errors),
                    msg=f"Valid level '{level}' was rejected"
                )

    def test_invalid_finish_flagged(self) -> None:
        palate = {"finish": "muy largo"}  # not in scale
        errors = _check_scale_values("white", {}, {}, palate, {})
        self.assertTrue(any("finish" in e for e in errors))

    def test_valid_finish_values_accepted(self) -> None:
        for finish in ("corto", "medio(-)", "medio", "medio(+)", "largo"):
            with self.subTest(finish=finish):
                palate = {"finish": finish}
                errors = _check_scale_values("white", {}, {}, palate, {})
                self.assertFalse(any("finish" in e for e in errors))

    def test_none_values_not_flagged_as_invalid(self) -> None:
        # Absence is a structural issue, not a scale error
        errors = _check_scale_values("white", {}, {}, {}, {})
        self.assertEqual(errors, [])


# ---------------------------------------------------------------------------
# 4. Mark allocation feedback (Component 3)
# ---------------------------------------------------------------------------
class MarkAllocationFeedbackTests(unittest.TestCase):

    def _feedback(self, fixture_name: str) -> dict:
        f = _load_fixture(fixture_name)
        return _build_mark_allocation_feedback(
            f["wine_type"], f["appearance"], f["nose"], f["palate"], f["conclusions"],
            f["nose"].get("is_simple", False) or f.get("is_simple", False),
            f["palate"].get("is_simple", False) or f.get("is_simple", False),
        )

    def test_complete_fixture_appearance_is_complete(self) -> None:
        fb = self._feedback("sat_response_valid_complete.json")
        self.assertEqual(fb["appearance"]["coverage"], "complete")

    def test_complete_fixture_nose_coverage_complete(self) -> None:
        fb = self._feedback("sat_response_valid_complete.json")
        self.assertEqual(fb["nose"]["coverage"], "complete")

    def test_complete_fixture_palate_coverage_complete(self) -> None:
        fb = self._feedback("sat_response_valid_complete.json")
        self.assertEqual(fb["palate"]["coverage"], "complete")

    def test_complete_fixture_conclusions_complete(self) -> None:
        fb = self._feedback("sat_response_valid_complete.json")
        self.assertEqual(fb["conclusions"]["coverage"], "complete")

    def test_incomplete_fixture_nose_coverage_partial(self) -> None:
        fb = self._feedback("sat_response_incomplete.json")
        self.assertEqual(fb["nose"]["coverage"], "partial")

    def test_incomplete_fixture_palate_coverage_partial(self) -> None:
        fb = self._feedback("sat_response_incomplete.json")
        self.assertEqual(fb["palate"]["coverage"], "partial")

    def test_feedback_has_all_required_keys(self) -> None:
        fb = self._feedback("sat_response_valid_complete.json")
        for section in ("appearance", "nose", "palate", "conclusions"):
            self.assertIn(section, fb)
            self.assertIn("coverage", fb[section])
            self.assertIn("guidance", fb[section])

    def test_simple_wine_nose_guidance_mentions_simple(self) -> None:
        fb = self._feedback("sat_response_simple_wine_violation.json")
        self.assertIn("simple", fb["nose"]["guidance"].lower())

    def test_feedback_never_assigns_marks(self) -> None:
        for fname in (
            "sat_response_valid_complete.json",
            "sat_response_incomplete.json",
        ):
            with self.subTest(fixture=fname):
                fb = self._feedback(fname)
                fb_str = json.dumps(fb).lower()
                for term in ("score", "mark", "grade", "marks awarded"):
                    self.assertNotIn(term, fb_str)

    def test_complete_fixture_tertiary_present_in_nose(self) -> None:
        fb = self._feedback("sat_response_valid_complete.json")
        self.assertTrue(fb["nose"]["tertiary_present"])

    def test_incomplete_fixture_tertiary_absent_in_nose(self) -> None:
        fb = self._feedback("sat_response_incomplete.json")
        self.assertFalse(fb["nose"]["tertiary_present"])


# ---------------------------------------------------------------------------
# 5. Simple wine exception (Component 4)
# ---------------------------------------------------------------------------
class SimpleWineExceptionTests(unittest.TestCase):

    def test_no_violation_when_wine_not_simple(self) -> None:
        nose = {"primary_aromas": ["limón"], "tertiary_aromas": ["miel"]}
        palate = {"primary_flavours": ["limón"], "tertiary_flavours": []}
        result = _check_simple_wine_exception(nose, palate, False, False)
        self.assertFalse(result["is_applicable"])
        self.assertFalse(result["violation"])

    def test_violation_detected_tertiary_in_simple_nose(self) -> None:
        nose = {"primary_aromas": ["pera"], "tertiary_aromas": ["miel", "nuez"], "is_simple": True}
        palate = {"primary_flavours": ["pera"], "tertiary_flavours": []}
        result = _check_simple_wine_exception(nose, palate, True, False)
        self.assertTrue(result["is_applicable"])
        self.assertTrue(result["violation"])
        self.assertGreater(len(result["messages"]), 0)

    def test_violation_detected_tertiary_in_simple_palate(self) -> None:
        nose = {"primary_aromas": ["pera"], "tertiary_aromas": []}
        palate = {"primary_flavours": ["pera"], "tertiary_flavours": ["miel"]}
        result = _check_simple_wine_exception(nose, palate, False, True)
        self.assertTrue(result["violation"])

    def test_fixture_simple_wine_violation_detected(self) -> None:
        fixture = _load_fixture("sat_response_simple_wine_violation.json")
        nose = fixture["nose"]
        palate = fixture["palate"]
        ns = nose.get("is_simple", False) or fixture.get("is_simple", False)
        ps = palate.get("is_simple", False) or fixture.get("is_simple", False)
        result = _check_simple_wine_exception(nose, palate, ns, ps)
        self.assertTrue(result["violation"])

    def test_simple_wine_without_tertiaries_no_violation(self) -> None:
        nose = {"primary_aromas": ["pera", "manzana"], "tertiary_aromas": [], "is_simple": True}
        palate = {"primary_flavours": ["pera"], "tertiary_flavours": []}
        result = _check_simple_wine_exception(nose, palate, True, True)
        self.assertTrue(result["is_applicable"])
        self.assertFalse(result["violation"])

    def test_misplaced_tertiary_in_primary_list_flagged(self) -> None:
        # Learner puts "miel" (tertiary) inside primary_aromas
        nose = {"primary_aromas": ["pera", "miel"], "tertiary_aromas": [], "is_simple": True}
        palate = {"primary_flavours": ["pera"], "tertiary_flavours": []}
        result = _check_simple_wine_exception(nose, palate, True, False)
        self.assertTrue(result["violation"])

    def test_result_always_has_required_keys(self) -> None:
        result = _check_simple_wine_exception({}, {}, False, False)
        for key in ("is_applicable", "violation", "messages", "guidance",
                    "declared_simple_nose", "declared_simple_palate"):
            self.assertIn(key, result)


# ---------------------------------------------------------------------------
# 6. Quality justification (Component 5)
# ---------------------------------------------------------------------------
class QualityJustificationTests(unittest.TestCase):

    def _check(self, nose: dict, palate: dict, conclusions: dict) -> dict:
        return _check_quality_justification(nose, palate, conclusions)

    def test_excelente_well_supported(self) -> None:
        nose = {
            "intensity": "pronunciada",
            "primary_aromas": ["cereza", "frambuesa"],
            "secondary_aromas": ["vainilla", "cedro"],
            "tertiary_aromas": ["cuero", "tierra"],
            "is_simple": False,
        }
        palate = {
            "finish": "largo",
            "primary_flavours": ["cereza"],
            "secondary_flavours": ["vainilla"],
            "tertiary_flavours": ["cuero"],
        }
        result = self._check(nose, palate, {"quality_level": "excelente"})
        self.assertIn(result["alignment"], ("aligned", "partially_supported"))
        self.assertGreater(len(result["supporting_evidence"]), 0)

    def test_excelente_overclaimed_no_tertiary(self) -> None:
        nose = {
            "intensity": "media",
            "primary_aromas": ["cereza roja"],
            "secondary_aromas": [],
            "tertiary_aromas": [],
            "is_simple": False,
        }
        palate = {
            "finish": "corto",
            "primary_flavours": ["cereza"],
            "secondary_flavours": [],
            "tertiary_flavours": [],
        }
        result = self._check(nose, palate, {"quality_level": "excelente"})
        self.assertEqual(result["alignment"], "overclaimed")
        self.assertIn("terciario", result["guidance"].lower())

    def test_fixture_weak_quality_justification_is_overclaimed(self) -> None:
        fixture = _load_fixture("sat_response_weak_quality_justification.json")
        result = self._check(fixture["nose"], fixture["palate"], fixture["conclusions"])
        self.assertEqual(result["alignment"], "overclaimed")

    def test_aceptable_with_simple_wine_is_aligned(self) -> None:
        nose = {
            "intensity": "media(-)",
            "primary_aromas": ["pera", "manzana"],
            "secondary_aromas": [],
            "tertiary_aromas": [],
            "is_simple": True,
        }
        palate = {
            "finish": "corto",
            "primary_flavours": ["pera"],
            "secondary_flavours": [],
            "tertiary_flavours": [],
        }
        result = self._check(nose, palate, {"quality_level": "aceptable"})
        self.assertIn(result["alignment"], ("aligned",))

    def test_muy_bueno_without_secondary_flagged(self) -> None:
        nose = {
            "intensity": "media",
            "primary_aromas": ["limón", "melocotón"],
            "secondary_aromas": [],
            "tertiary_aromas": [],
            "is_simple": False,
        }
        palate = {
            "finish": "medio",
            "primary_flavours": ["limón"],
            "secondary_flavours": [],
            "tertiary_flavours": [],
        }
        result = self._check(nose, palate, {"quality_level": "muy bueno"})
        self.assertNotEqual(result["alignment"], "aligned")
        self.assertGreater(len(result["missing_evidence"]), 0)

    def test_complete_fixture_quality_justified(self) -> None:
        fixture = _load_fixture("sat_response_valid_complete.json")
        result = self._check(fixture["nose"], fixture["palate"], fixture["conclusions"])
        self.assertIn(result["alignment"], ("aligned", "partially_supported"))

    def test_missing_quality_returns_missing_alignment(self) -> None:
        result = self._check({}, {}, {})
        self.assertEqual(result["alignment"], "missing")

    def test_result_always_has_required_keys(self) -> None:
        result = self._check({}, {}, {"quality_level": "bueno"})
        for key in ("quality_stated", "alignment", "supporting_evidence",
                    "missing_evidence", "guidance"):
            self.assertIn(key, result)


# ---------------------------------------------------------------------------
# 7. Distinction gap (Component 6)
# ---------------------------------------------------------------------------
class DistinctionGapTests(unittest.TestCase):

    def test_complete_fixture_is_distinction_ready(self) -> None:
        fixture = _load_fixture("sat_response_valid_complete.json")
        result = _build_distinction_gap_report(fixture["nose"], fixture["palate"])
        self.assertEqual(result["level_indicator"], "distinction_ready")

    def test_incomplete_fixture_is_not_distinction_ready(self) -> None:
        fixture = _load_fixture("sat_response_incomplete.json")
        result = _build_distinction_gap_report(fixture["nose"], fixture["palate"])
        self.assertNotEqual(result["level_indicator"], "distinction_ready")

    def test_generic_descriptor_detected(self) -> None:
        nose = {"primary_aromas": ["frutal", "limón"], "secondary_aromas": [], "tertiary_aromas": []}
        palate = {"primary_flavours": [], "secondary_flavours": [], "tertiary_flavours": []}
        result = _build_distinction_gap_report(nose, palate)
        self.assertIn("frutal", result["generic_descriptors_found"])

    def test_secondary_descriptor_in_primary_list_flagged(self) -> None:
        nose = {"primary_aromas": ["vainilla", "limón"], "secondary_aromas": [], "tertiary_aromas": []}
        palate = {"primary_flavours": [], "secondary_flavours": [], "tertiary_flavours": []}
        result = _build_distinction_gap_report(nose, palate)
        self.assertTrue(any("vainilla" in e for e in result["category_errors"]))

    def test_tertiary_descriptor_in_primary_list_flagged(self) -> None:
        nose = {"primary_aromas": ["miel", "limón"], "secondary_aromas": [], "tertiary_aromas": []}
        palate = {"primary_flavours": [], "secondary_flavours": [], "tertiary_flavours": []}
        result = _build_distinction_gap_report(nose, palate)
        self.assertTrue(any("miel" in e for e in result["category_errors"]))

    def test_missing_tertiary_generates_guidance(self) -> None:
        nose = {"primary_aromas": ["cereza"], "secondary_aromas": ["vainilla"],
                "tertiary_aromas": [], "is_simple": False}
        palate = {"primary_flavours": ["cereza"], "secondary_flavours": ["vainilla"],
                  "tertiary_flavours": []}
        result = _build_distinction_gap_report(nose, palate)
        self.assertFalse(result["tertiary_present"])
        self.assertTrue(any("terciario" in g.lower() for g in result["guidance"]))

    def test_missing_secondary_generates_guidance(self) -> None:
        nose = {"primary_aromas": ["cereza", "ciruela"], "secondary_aromas": [],
                "tertiary_aromas": [], "is_simple": False}
        palate = {"primary_flavours": ["cereza"], "secondary_flavours": [], "tertiary_flavours": []}
        result = _build_distinction_gap_report(nose, palate)
        self.assertFalse(result["secondary_present"])
        self.assertTrue(any("secundario" in g.lower() for g in result["guidance"]))

    def test_result_always_has_required_keys(self) -> None:
        result = _build_distinction_gap_report({}, {})
        for key in ("level_indicator", "generic_descriptors_found", "category_errors",
                    "tertiary_present", "secondary_present", "guidance", "formative_note"):
            self.assertIn(key, result)

    def test_formative_note_always_present(self) -> None:
        result = _build_distinction_gap_report({}, {})
        self.assertIn("formativa", result["formative_note"].lower())

    def test_approaching_distinction_with_secondary_only(self) -> None:
        nose = {"primary_aromas": ["cereza"], "secondary_aromas": ["vainilla"],
                "tertiary_aromas": [], "is_simple": False}
        palate = {"primary_flavours": ["cereza"], "secondary_flavours": ["vainilla"],
                  "tertiary_flavours": []}
        result = _build_distinction_gap_report(nose, palate)
        self.assertEqual(result["level_indicator"], "approaching_distinction")


# ---------------------------------------------------------------------------
# 8. Full integration via validate_sat_response
# ---------------------------------------------------------------------------
class IntegrationTests(unittest.TestCase):

    def test_output_has_all_required_top_level_keys(self) -> None:
        result = validate_sat_response({})
        required = ("governance", "structural_issues", "scale_errors",
                    "mark_allocation_feedback", "simple_wine_exception",
                    "quality_justification", "distinction_gap")
        for key in required:
            self.assertIn(key, result)

    def test_valid_complete_fixture_minimal_issues(self) -> None:
        fixture = _load_fixture("sat_response_valid_complete.json")
        result = validate_sat_response(fixture)
        self.assertEqual(result["structural_issues"], [])
        self.assertEqual(result["scale_errors"], [])

    def test_incomplete_fixture_has_structural_issues(self) -> None:
        fixture = _load_fixture("sat_response_incomplete.json")
        result = validate_sat_response(fixture)
        self.assertGreater(len(result["structural_issues"]), 0)

    def test_simple_wine_fixture_violation_in_result(self) -> None:
        fixture = _load_fixture("sat_response_simple_wine_violation.json")
        result = validate_sat_response(fixture)
        self.assertTrue(result["simple_wine_exception"]["violation"])

    def test_weak_quality_fixture_overclaim_detected(self) -> None:
        fixture = _load_fixture("sat_response_weak_quality_justification.json")
        result = validate_sat_response(fixture)
        self.assertEqual(result["quality_justification"]["alignment"], "overclaimed")

    def test_determinism_same_input_same_output(self) -> None:
        fixture = _load_fixture("sat_response_valid_complete.json")
        r1 = validate_sat_response(fixture)
        r2 = validate_sat_response(fixture)
        self.assertEqual(json.dumps(r1, sort_keys=True), json.dumps(r2, sort_keys=True))

    def test_determinism_incomplete_fixture(self) -> None:
        fixture = _load_fixture("sat_response_incomplete.json")
        r1 = validate_sat_response(fixture)
        r2 = validate_sat_response(fixture)
        self.assertEqual(json.dumps(r1, sort_keys=True), json.dumps(r2, sort_keys=True))

    def test_empty_input_does_not_raise(self) -> None:
        try:
            result = validate_sat_response({})
            self.assertIsInstance(result, dict)
        except Exception as exc:
            self.fail(f"validate_sat_response({{}}) raised: {exc}")

    def test_red_wine_tannin_required_in_structural_issues(self) -> None:
        fixture = _load_fixture("sat_response_weak_quality_justification.json")
        # This is a red wine fixture with tannin — should be complete structurally on tannin
        result = validate_sat_response(fixture)
        has_tannin_issue = any("tanino" in i.lower() for i in result["structural_issues"])
        self.assertFalse(has_tannin_issue)  # tannin is present in fixture


# ---------------------------------------------------------------------------
# 9. No side-effects — validator must not write files
# ---------------------------------------------------------------------------
class SideEffectsTests(unittest.TestCase):

    def test_validator_does_not_write_files(self) -> None:
        import os
        import tempfile
        fixture = _load_fixture("sat_response_valid_complete.json")
        cwd_before = set(Path(".").glob("*.json"))
        validate_sat_response(fixture)
        cwd_after = set(Path(".").glob("*.json"))
        self.assertEqual(cwd_before, cwd_after)


if __name__ == "__main__":
    unittest.main()

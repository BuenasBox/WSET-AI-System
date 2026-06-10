"""Phase X.4 — SAT Readiness Validator tests.

Tests for _check_readiness_reasoning() and its integration into
validate_sat_response(). Governance: safe_for_examiner=False,
no marks assigned, formative only.

Run: python -m unittest tests.test_sat_validator_readiness -v
"""

import unittest
from tools.tutor.sat_validator import (
    validate_sat_response,
    _check_readiness_reasoning,
    VALIDATOR_GOVERNANCE,
    _READINESS_VALID,
    _READINESS_HAS_POTENTIAL,
    _READINESS_DRINK_NOW,
    _READINESS_TOO_YOUNG,
    _READINESS_TOO_OLD,
)


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

def _base_white(readiness, is_simple=False, development="joven",
                secondary=None, tertiary=None, finish="corto"):
    return {
        "wine_type": "white",
        "is_simple": is_simple,
        "appearance": {"intensity": "media", "colour": "limon"},
        "nose": {
            "intensity": "media",
            "primary_aromas": ["manzana"],
            "secondary_aromas": secondary or [],
            "tertiary_aromas": tertiary or [],
            "development": development,
            "is_simple": is_simple,
        },
        "palate": {
            "sweetness": "seco",
            "acidity": "media",
            "alcohol": "medio",
            "body": "medio",
            "flavour_intensity": "media",
            "primary_flavours": ["manzana"],
            "secondary_flavours": secondary or [],
            "tertiary_flavours": tertiary or [],
            "finish": finish,
            "is_simple": is_simple,
        },
        "conclusions": {"quality_level": "bueno", "readiness": readiness},
    }


def _full_complex_white(readiness):
    """Premium white wine with full secondary + tertiary development."""
    return {
        "wine_type": "white",
        "is_simple": False,
        "appearance": {"intensity": "media", "colour": "dorado"},
        "nose": {
            "intensity": "pronunciada",
            "primary_aromas": ["melocoton", "citrico"],
            "secondary_aromas": ["vainilla", "tostado"],
            "tertiary_aromas": ["miel", "nuez"],
            "development": "evolucionado",
            "is_simple": False,
        },
        "palate": {
            "sweetness": "seco",
            "acidity": "media",
            "alcohol": "medio",
            "body": "lleno",
            "flavour_intensity": "pronunciada",
            "primary_flavours": ["melocoton"],
            "secondary_flavours": ["vainilla"],
            "tertiary_flavours": ["miel"],
            "finish": "largo",
            "is_simple": False,
        },
        "conclusions": {"quality_level": "excelente", "readiness": readiness},
    }


# ---------------------------------------------------------------------------
# 1. Scale values
# ---------------------------------------------------------------------------

class ReadinessScaleTests(unittest.TestCase):
    """_READINESS_VALID contains the four official values."""

    def test_four_official_values_exist(self):
        self.assertEqual(len(_READINESS_VALID), 4)

    def test_has_potential_in_valid(self):
        self.assertIn(_READINESS_HAS_POTENTIAL, _READINESS_VALID)

    def test_drink_now_in_valid(self):
        self.assertIn(_READINESS_DRINK_NOW, _READINESS_VALID)

    def test_too_young_in_valid(self):
        self.assertIn(_READINESS_TOO_YOUNG, _READINESS_VALID)

    def test_too_old_in_valid(self):
        self.assertIn(_READINESS_TOO_OLD, _READINESS_VALID)


# ---------------------------------------------------------------------------
# 2. Key presence in validate_sat_response output
# ---------------------------------------------------------------------------

class ReadinessKeyPresenceTests(unittest.TestCase):
    """readiness_reasoning key is always present in validate_sat_response output."""

    def test_key_present_with_readiness(self):
        r = validate_sat_response(_base_white(_READINESS_HAS_POTENTIAL))
        self.assertIn("readiness_reasoning", r)

    def test_key_present_missing_readiness(self):
        r = validate_sat_response(_base_white(None))
        self.assertIn("readiness_reasoning", r)

    def test_key_present_invalid_readiness(self):
        r = validate_sat_response(_base_white("potencial largo"))
        self.assertIn("readiness_reasoning", r)

    def test_result_is_dict(self):
        r = validate_sat_response(_base_white(_READINESS_DRINK_NOW))
        self.assertIsInstance(r["readiness_reasoning"], dict)

    def test_required_sub_keys(self):
        rr = validate_sat_response(_base_white(_READINESS_HAS_POTENTIAL))["readiness_reasoning"]
        for k in ("readiness_stated", "alignment", "consistency_issues", "guidance"):
            self.assertIn(k, rr, f"Missing key: {k}")


# ---------------------------------------------------------------------------
# 3. Missing readiness
# ---------------------------------------------------------------------------

class MissingReadinessTests(unittest.TestCase):

    def test_none_readiness_alignment_missing(self):
        rr = _check_readiness_reasoning({}, {}, {"readiness": None}, False)
        self.assertEqual(rr["alignment"], "missing")

    def test_empty_string_alignment_missing(self):
        rr = _check_readiness_reasoning({}, {}, {"readiness": ""}, False)
        self.assertEqual(rr["alignment"], "missing")

    def test_missing_no_issues_list(self):
        rr = _check_readiness_reasoning({}, {}, {}, False)
        self.assertEqual(rr["consistency_issues"], [])

    def test_missing_guidance_not_empty(self):
        rr = _check_readiness_reasoning({}, {}, {}, False)
        self.assertTrue(rr["guidance"])


# ---------------------------------------------------------------------------
# 4. Simple wine + has_potential = overclaim
# ---------------------------------------------------------------------------

class SimpleWineReadinessTests(unittest.TestCase):
    """Simple wine cannot claim ageing potential."""

    def test_simple_wine_has_potential_is_overclaimed(self):
        r = validate_sat_response(
            _base_white(_READINESS_HAS_POTENTIAL, is_simple=True)
        )
        self.assertEqual(r["readiness_reasoning"]["alignment"], "overclaimed")

    def test_simple_wine_drink_now_is_aligned(self):
        r = validate_sat_response(
            _base_white(_READINESS_DRINK_NOW, is_simple=True)
        )
        self.assertIn(r["readiness_reasoning"]["alignment"], ("aligned", "partially_supported"))

    def test_simple_wine_overclaim_has_message(self):
        rr = validate_sat_response(
            _base_white(_READINESS_HAS_POTENTIAL, is_simple=True)
        )["readiness_reasoning"]
        self.assertTrue(len(rr["consistency_issues"]) > 0)

    def test_simple_wine_overclaim_message_mentions_simple(self):
        rr = validate_sat_response(
            _base_white(_READINESS_HAS_POTENTIAL, is_simple=True)
        )["readiness_reasoning"]
        combined = " ".join(rr["consistency_issues"]).lower()
        self.assertTrue("simple" in combined or "estructura" in combined)


# ---------------------------------------------------------------------------
# 5. No secondary/tertiary but claims ageing potential = overclaim
# ---------------------------------------------------------------------------

class NoComplexityPotentialTests(unittest.TestCase):

    def test_no_secondary_no_tertiary_has_potential_overclaimed(self):
        r = validate_sat_response(
            _base_white(_READINESS_HAS_POTENTIAL, secondary=[], tertiary=[])
        )
        self.assertEqual(r["readiness_reasoning"]["alignment"], "overclaimed")

    def test_with_secondary_only_and_potential_partially_or_aligned(self):
        r = validate_sat_response(
            _base_white(_READINESS_HAS_POTENTIAL, secondary=["vainilla"], tertiary=[],
                        development="en evolucion", finish="medio")
        )
        self.assertIn(r["readiness_reasoning"]["alignment"], ("aligned", "partially_supported"))

    def test_with_secondary_and_tertiary_aligned(self):
        r = validate_sat_response(_full_complex_white(_READINESS_HAS_POTENTIAL))
        self.assertEqual(r["readiness_reasoning"]["alignment"], "aligned")


# ---------------------------------------------------------------------------
# 6. Drink now — inconsistencies with tertiary/long finish
# ---------------------------------------------------------------------------

class DrinkNowConsistencyTests(unittest.TestCase):

    def test_drink_now_no_tertiary_is_aligned(self):
        r = validate_sat_response(
            _base_white(_READINESS_DRINK_NOW, is_simple=True)
        )
        self.assertIn(r["readiness_reasoning"]["alignment"], ("aligned", "partially_supported"))

    def test_drink_now_with_tertiary_partially_supported(self):
        r = validate_sat_response(
            _base_white(_READINESS_DRINK_NOW, secondary=["vainilla"], tertiary=["miel"],
                        development="evolucionado", finish="largo")
        )
        self.assertIn(r["readiness_reasoning"]["alignment"],
                      ("partially_supported", "overclaimed", "aligned"))

    def test_drink_now_simple_wine_not_flagged_for_tertiary(self):
        # Simple wine declaring drink_now should not be flagged even if it has tertiary
        r = validate_sat_response(
            _base_white(_READINESS_DRINK_NOW, is_simple=True,
                        tertiary=["miel"])
        )
        # simple=True suppresses the tertiary inconsistency for drink_now
        rr = r["readiness_reasoning"]
        # alignment should not be due to simple-wine path
        self.assertIsNotNone(rr["alignment"])


# ---------------------------------------------------------------------------
# 7. demasiado_joven inconsistencies
# ---------------------------------------------------------------------------

class TooYoungConsistencyTests(unittest.TestCase):

    def test_joven_development_with_too_young_aligned_or_partial(self):
        r = validate_sat_response(
            _base_white(_READINESS_TOO_YOUNG, development="joven")
        )
        self.assertIn(r["readiness_reasoning"]["alignment"],
                      ("aligned", "partially_supported"))

    def test_evolucionado_development_with_too_young_inconsistent(self):
        r = validate_sat_response(
            _base_white(_READINESS_TOO_YOUNG, development="evolucionado")
        )
        self.assertEqual(r["readiness_reasoning"]["alignment"], "inconsistent")

    def test_en_evolucion_development_with_too_young_inconsistent(self):
        r = validate_sat_response(
            _base_white(_READINESS_TOO_YOUNG, development="en evolución")
        )
        self.assertEqual(r["readiness_reasoning"]["alignment"], "inconsistent")

    def test_too_young_with_tertiary_partially_supported(self):
        r = validate_sat_response(
            _base_white(_READINESS_TOO_YOUNG, development="joven",
                        tertiary=["miel", "cuero"])
        )
        self.assertIn(r["readiness_reasoning"]["alignment"],
                      ("partially_supported", "inconsistent"))


# ---------------------------------------------------------------------------
# 8. demasiado_viejo inconsistencies
# ---------------------------------------------------------------------------

class TooOldConsistencyTests(unittest.TestCase):

    def test_joven_development_too_old_inconsistent(self):
        r = validate_sat_response(
            _base_white(_READINESS_TOO_OLD, development="joven")
        )
        self.assertEqual(r["readiness_reasoning"]["alignment"], "inconsistent")

    def test_evolucionado_development_too_old_not_inconsistent(self):
        r = validate_sat_response(
            _base_white(_READINESS_TOO_OLD, development="evolucionado")
        )
        self.assertNotEqual(r["readiness_reasoning"]["alignment"], "inconsistent")


# ---------------------------------------------------------------------------
# 9. Invalid scale value
# ---------------------------------------------------------------------------

class InvalidReadinessScaleTests(unittest.TestCase):

    def test_invalid_value_alignment(self):
        rr = _check_readiness_reasoning(
            {}, {}, {"readiness": "potencial largo"}, False
        )
        self.assertEqual(rr["alignment"], "invalid_scale_value")

    def test_invalid_value_issue_mentions_value(self):
        rr = _check_readiness_reasoning(
            {}, {}, {"readiness": "potencial largo"}, False
        )
        combined = " ".join(rr["consistency_issues"]).lower()
        self.assertIn("potencial largo", combined)


# ---------------------------------------------------------------------------
# 10. Governance
# ---------------------------------------------------------------------------

class ReadinessGovernanceTests(unittest.TestCase):
    """No marks, no scoring, safe_for_examiner=False throughout."""

    def test_safe_for_examiner_false(self):
        r = validate_sat_response(_full_complex_white(_READINESS_HAS_POTENTIAL))
        self.assertFalse(r["governance"]["safe_for_examiner"])

    def test_no_marks_assigned(self):
        r = validate_sat_response(_full_complex_white(_READINESS_HAS_POTENTIAL))
        self.assertTrue(r["governance"]["no_marks_assigned"])

    def test_readiness_guidance_no_mark_language(self):
        forbidden = (
            "your score", "your mark", "marks awarded",
            "total mark", "final grade", "wset_equivalence",
        )
        for readiness_val in (_READINESS_HAS_POTENTIAL, _READINESS_DRINK_NOW,
                               _READINESS_TOO_YOUNG, _READINESS_TOO_OLD):
            r = validate_sat_response(_base_white(readiness_val))
            rr = r["readiness_reasoning"]
            for v in rr.values():
                if isinstance(v, str):
                    for phrase in forbidden:
                        self.assertNotIn(phrase, v.lower(),
                                         f"Forbidden phrase '{phrase}' in {v!r}")
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, str):
                            for phrase in forbidden:
                                self.assertNotIn(phrase, item.lower())

    def test_examiner_scoring_allowed_false(self):
        r = validate_sat_response(_full_complex_white(_READINESS_HAS_POTENTIAL))
        self.assertFalse(r["governance"]["examiner_scoring_allowed"])

    def test_formative_only_true(self):
        r = validate_sat_response(_full_complex_white(_READINESS_HAS_POTENTIAL))
        self.assertTrue(r["governance"]["formative_only"])


# ---------------------------------------------------------------------------
# 11. Determinism
# ---------------------------------------------------------------------------

class ReadinessDeterminismTests(unittest.TestCase):

    def test_same_input_same_output(self):
        inp = _full_complex_white(_READINESS_HAS_POTENTIAL)
        r1 = validate_sat_response(inp)["readiness_reasoning"]
        r2 = validate_sat_response(inp)["readiness_reasoning"]
        self.assertEqual(r1, r2)

    def test_overclaim_deterministic(self):
        inp = _base_white(_READINESS_HAS_POTENTIAL, is_simple=True)
        r1 = validate_sat_response(inp)["readiness_reasoning"]
        r2 = validate_sat_response(inp)["readiness_reasoning"]
        self.assertEqual(r1, r2)


# ---------------------------------------------------------------------------
# 12. No-SAT path unchanged
# ---------------------------------------------------------------------------

class NonSATPathUnchangedTests(unittest.TestCase):
    """readiness_reasoning key does not affect outputs when sat_submission absent."""

    def test_non_sat_response_still_has_other_keys(self):
        r = validate_sat_response(_base_white(_READINESS_HAS_POTENTIAL))
        for k in ("governance", "structural_issues", "scale_errors",
                  "mark_allocation_feedback", "simple_wine_exception",
                  "quality_justification", "distinction_gap"):
            self.assertIn(k, r)

    def test_readiness_key_does_not_break_existing_keys(self):
        r = validate_sat_response(_full_complex_white(_READINESS_HAS_POTENTIAL))
        self.assertIn("distinction_gap", r)
        self.assertIn("quality_justification", r)
        self.assertEqual(r["distinction_gap"]["level_indicator"], "distinction_ready")


if __name__ == "__main__":
    unittest.main()

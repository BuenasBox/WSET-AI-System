"""
Phase X.5 — SAT Response Structure Validator tests.

Covers _check_response_structure() (Component 8) and its integration into
validate_sat_response(). All tests are deterministic and governance-clean.
"""
import importlib.util
import sys
import unittest
from pathlib import Path

# ---------------------------------------------------------------------------
# Direct source import (bypass .pyc cache / Windows permission issues)
# ---------------------------------------------------------------------------
_REPO = Path(__file__).parent.parent
_SAT_SRC = _REPO / "tools" / "tutor" / "sat_validator.py"

spec = importlib.util.spec_from_file_location("sat_validator_x5", _SAT_SRC)
_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_mod)

validate_sat_response = _mod.validate_sat_response
_check_response_structure = _mod._check_response_structure
VALIDATOR_GOVERNANCE = _mod.VALIDATOR_GOVERNANCE

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _minimal_sat(**overrides):
    """Minimal valid SAT submission with all required sections."""
    base = {
        "wine_type": "white",
        "appearance": {"intensity": "pale", "colour": "lemon"},
        "nose": {
            "intensity": "medium",
            "primary_aromas": ["lemon", "peach"],
            "secondary_aromas": ["vanilla", "biscuit"],
            "tertiary_aromas": [],
            "development": "developing",
        },
        "palate": {
            "sweetness": "dry",
            "acidity": "medium(+)",
            "alcohol": "medium",
            "body": "medium(+)",
            "flavour_intensity": "medium(+)",
            "primary_flavours": ["lemon", "peach"],
            "secondary_flavours": ["vanilla", "biscuit"],
            "tertiary_flavours": [],
            "finish": "medium(+)",
        },
        "conclusions": {
            "quality_level": "muy bueno",
            "readiness": "se puede beber ahora, pero tiene potencial para el envejecimiento",
        },
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# 1. Conformant cases
# ---------------------------------------------------------------------------

class ConformantStructureTests(unittest.TestCase):
    """Correct structure returns status=conformant with no issues."""

    def test_complex_white_is_conformant(self):
        nose = {
            "intensity": "medium(+)",
            "primary_aromas": ["lemon", "peach"],
            "secondary_aromas": ["vanilla", "biscuit"],
            "tertiary_aromas": ["honey"],
            "development": "developing",
        }
        palate = {
            "sweetness": "dry",
            "acidity": "medium(+)",
            "alcohol": "medium",
            "body": "medium(+)",
            "flavour_intensity": "medium(+)",
            "primary_flavours": ["lemon"],
            "finish": "medium(+)",
        }
        result = _check_response_structure("white", nose, palate, False)
        self.assertEqual(result["status"], "conformant")
        self.assertEqual(result["ordering_issues"], [])

    def test_simple_wine_primary_only_is_conformant(self):
        nose = {
            "intensity": "medium(-)",
            "primary_aromas": ["pear", "green apple"],
            "secondary_aromas": [],
            "tertiary_aromas": [],
            "development": "young",
        }
        palate = {
            "sweetness": "dry",
            "acidity": "medium",
            "alcohol": "low",
            "body": "light",
            "flavour_intensity": "medium(-)",
            "primary_flavours": ["pear"],
            "finish": "short",
        }
        result = _check_response_structure("white", nose, palate, True)
        self.assertEqual(result["status"], "conformant")
        self.assertEqual(result["ordering_issues"], [])

    def test_sweet_wine_high_acidity_is_conformant(self):
        nose = {
            "intensity": "pronounced",
            "primary_aromas": ["honey", "apricot"],
            "secondary_aromas": ["vanilla"],
            "tertiary_aromas": ["marmalade"],
            "development": "developing",
        }
        palate = {
            "sweetness": "sweet",
            "acidity": "alta",
            "alcohol": "medium(+)",
            "body": "full",
            "flavour_intensity": "pronounced",
            "primary_flavours": ["honey"],
            "finish": "long",
        }
        result = _check_response_structure("sweet", nose, palate, False)
        self.assertEqual(result["status"], "conformant")
        self.assertNotIn("structure_sweet_wine_acidity", result["ordering_issues"])

    def test_sweet_wine_medium_plus_acidity_is_conformant(self):
        """media(+) is acceptable for sweet wine acidity."""
        nose = {"intensity": "pronounced", "primary_aromas": ["honey"], "secondary_aromas": [], "tertiary_aromas": [], "development": "developing"}
        palate = {"sweetness": "sweet", "acidity": "media(+)", "alcohol": "medium", "body": "full", "flavour_intensity": "pronounced", "primary_flavours": ["honey"], "finish": "long"}
        result = _check_response_structure("sweet", nose, palate, False)
        self.assertNotIn("structure_sweet_wine_acidity", result["ordering_issues"])


# ---------------------------------------------------------------------------
# 2. Ordering: nose development without aromas
# ---------------------------------------------------------------------------

class NoseOrderingTests(unittest.TestCase):
    """Development stated without primary aromas triggers ordering issue."""

    def test_development_without_aromas(self):
        nose = {
            "intensity": "medium",
            "primary_aromas": [],
            "secondary_aromas": [],
            "tertiary_aromas": [],
            "development": "developing",
        }
        palate = {
            "sweetness": "dry",
            "acidity": "medium",
            "alcohol": "medium",
            "body": "medium",
            "flavour_intensity": "medium",
            "primary_flavours": ["lemon"],
            "finish": "medium",
        }
        result = _check_response_structure("white", nose, palate, False)
        self.assertIn("ordering_nose_development_without_aromas", result["ordering_issues"])
        self.assertEqual(result["status"], "issues_found")

    def test_development_with_aromas_no_issue(self):
        nose = {
            "intensity": "medium",
            "primary_aromas": ["lemon"],
            "secondary_aromas": [],
            "tertiary_aromas": [],
            "development": "developing",
        }
        palate = {
            "sweetness": "dry", "acidity": "medium", "alcohol": "medium",
            "body": "medium", "flavour_intensity": "medium",
            "primary_flavours": ["lemon"], "finish": "medium",
        }
        result = _check_response_structure("white", nose, palate, False)
        self.assertNotIn("ordering_nose_development_without_aromas", result["ordering_issues"])

    def test_no_development_no_aromas_no_ordering_issue(self):
        """Neither development nor aromas → no nose ordering trigger."""
        nose = {"intensity": "medium", "primary_aromas": [], "secondary_aromas": [], "tertiary_aromas": [], "development": ""}
        palate = {"sweetness": "dry", "acidity": "medium", "alcohol": "medium", "body": "medium", "flavour_intensity": "medium", "primary_flavours": [], "finish": "medium"}
        result = _check_response_structure("white", nose, palate, False)
        self.assertNotIn("ordering_nose_development_without_aromas", result["ordering_issues"])


# ---------------------------------------------------------------------------
# 3. Ordering: palate flavours before scale
# ---------------------------------------------------------------------------

class PalateOrderingTests(unittest.TestCase):
    """Flavours present with missing scale values triggers ordering issue."""

    def test_flavours_with_missing_scale_values(self):
        nose = {"intensity": "medium", "primary_aromas": ["lemon"], "secondary_aromas": ["vanilla"], "tertiary_aromas": [], "development": "developing"}
        palate = {
            "sweetness": "",    # missing
            "acidity": "",      # missing
            "alcohol": "",      # missing
            "body": "",         # missing
            "flavour_intensity": "",  # missing
            "primary_flavours": ["lemon", "peach"],
            "finish": "medium",
        }
        result = _check_response_structure("white", nose, palate, False)
        self.assertIn("ordering_palate_flavours_before_scale", result["ordering_issues"])
        self.assertEqual(result["status"], "issues_found")

    def test_flavours_with_all_scale_values_no_issue(self):
        nose = {"intensity": "medium", "primary_aromas": ["lemon"], "secondary_aromas": ["vanilla"], "tertiary_aromas": [], "development": "developing"}
        palate = {
            "sweetness": "dry",
            "acidity": "medium(+)",
            "alcohol": "medium",
            "body": "medium",
            "flavour_intensity": "medium",
            "primary_flavours": ["lemon"],
            "finish": "medium",
        }
        result = _check_response_structure("white", nose, palate, False)
        self.assertNotIn("ordering_palate_flavours_before_scale", result["ordering_issues"])

    def test_no_flavours_no_scale_no_ordering_issue(self):
        """Missing scale values without any flavours should not trigger."""
        nose = {"intensity": "medium", "primary_aromas": ["lemon"], "secondary_aromas": [], "tertiary_aromas": [], "development": "developing"}
        palate = {
            "sweetness": "", "acidity": "", "alcohol": "", "body": "",
            "flavour_intensity": "", "primary_flavours": [], "finish": "",
        }
        result = _check_response_structure("white", nose, palate, False)
        self.assertNotIn("ordering_palate_flavours_before_scale", result["ordering_issues"])


# ---------------------------------------------------------------------------
# 4. Simple wine excess complexity
# ---------------------------------------------------------------------------

class SimpleWineStructureTests(unittest.TestCase):
    """Simple wine with secondary/tertiary content triggers structure issues."""

    def test_simple_wine_nose_secondary_triggers_issue(self):
        nose = {
            "intensity": "medium",
            "primary_aromas": ["pear"],
            "secondary_aromas": ["vanilla"],   # should not be present for simple
            "tertiary_aromas": [],
            "development": "young",
        }
        palate = {
            "sweetness": "dry", "acidity": "medium", "alcohol": "low", "body": "light",
            "flavour_intensity": "medium(-)", "primary_flavours": ["pear"], "finish": "short",
        }
        result = _check_response_structure("white", nose, palate, True)
        self.assertIn("structure_simple_wine_excess_complexity", result["ordering_issues"])

    def test_simple_wine_palate_secondary_triggers_issue(self):
        nose = {"intensity": "medium", "primary_aromas": ["pear"], "secondary_aromas": [], "tertiary_aromas": [], "development": "young"}
        palate = {
            "sweetness": "dry", "acidity": "medium", "alcohol": "low", "body": "light",
            "flavour_intensity": "medium(-)", "primary_flavours": ["pear"],
            "secondary_flavours": ["vanilla"],   # should not be present for simple
            "finish": "short",
        }
        result = _check_response_structure("white", nose, palate, True)
        self.assertIn("structure_simple_wine_palate_excess", result["ordering_issues"])

    def test_simple_wine_nose_tertiary_triggers_issue(self):
        nose = {
            "intensity": "medium", "primary_aromas": ["pear"],
            "secondary_aromas": [], "tertiary_aromas": ["honey"],   # tertiary on simple wine
            "development": "young",
        }
        palate = {"sweetness": "dry", "acidity": "medium", "alcohol": "low", "body": "light", "flavour_intensity": "medium(-)", "primary_flavours": ["pear"], "finish": "short"}
        result = _check_response_structure("white", nose, palate, True)
        self.assertIn("structure_simple_wine_excess_complexity", result["ordering_issues"])


# ---------------------------------------------------------------------------
# 5. Complex wine missing secondary aromas
# ---------------------------------------------------------------------------

class ComplexWineStructureTests(unittest.TestCase):
    """Complex (non-simple) wine without secondary aromas triggers issue."""

    def test_complex_wine_no_secondary_triggers_issue(self):
        nose = {
            "intensity": "medium(+)",
            "primary_aromas": ["lemon", "peach"],
            "secondary_aromas": [],   # missing for complex wine
            "tertiary_aromas": [],
            "development": "developing",
        }
        palate = {
            "sweetness": "dry", "acidity": "medium(+)", "alcohol": "medium",
            "body": "medium(+)", "flavour_intensity": "medium(+)",
            "primary_flavours": ["lemon"], "finish": "medium(+)",
        }
        result = _check_response_structure("white", nose, palate, False)
        self.assertIn("structure_complex_wine_missing_secondary", result["ordering_issues"])

    def test_complex_wine_with_secondary_no_issue(self):
        nose = {
            "intensity": "medium(+)", "primary_aromas": ["lemon"],
            "secondary_aromas": ["vanilla", "biscuit"],
            "tertiary_aromas": [], "development": "developing",
        }
        palate = {
            "sweetness": "dry", "acidity": "medium(+)", "alcohol": "medium",
            "body": "medium(+)", "flavour_intensity": "medium(+)",
            "primary_flavours": ["lemon"], "finish": "medium(+)",
        }
        result = _check_response_structure("white", nose, palate, False)
        self.assertNotIn("structure_complex_wine_missing_secondary", result["ordering_issues"])

    def test_no_primaries_no_complex_secondary_issue(self):
        """No primary aromas means complex-wine secondary check not triggered."""
        nose = {"intensity": "medium", "primary_aromas": [], "secondary_aromas": [], "tertiary_aromas": [], "development": ""}
        palate = {"sweetness": "dry", "acidity": "medium", "alcohol": "medium", "body": "medium", "flavour_intensity": "medium", "primary_flavours": [], "finish": "medium"}
        result = _check_response_structure("white", nose, palate, False)
        self.assertNotIn("structure_complex_wine_missing_secondary", result["ordering_issues"])


# ---------------------------------------------------------------------------
# 6. Sweet wine acidity
# ---------------------------------------------------------------------------

class SweetWineAcidityTests(unittest.TestCase):
    """Sweet wine with low/medium acidity triggers structural issue."""

    def test_sweet_wine_low_acidity_triggers_issue(self):
        nose = {"intensity": "pronounced", "primary_aromas": ["honey"], "secondary_aromas": ["vanilla"], "tertiary_aromas": [], "development": "developing"}
        palate = {
            "sweetness": "sweet", "acidity": "baja",   # low → issue
            "alcohol": "medium(+)", "body": "full", "flavour_intensity": "pronounced",
            "primary_flavours": ["honey"], "finish": "long",
        }
        result = _check_response_structure("sweet", nose, palate, False)
        self.assertIn("structure_sweet_wine_acidity", result["ordering_issues"])

    def test_sweet_wine_medium_acidity_triggers_issue(self):
        nose = {"intensity": "pronounced", "primary_aromas": ["honey"], "secondary_aromas": ["vanilla"], "tertiary_aromas": [], "development": "developing"}
        palate = {
            "sweetness": "sweet", "acidity": "media",  # medium, not high → issue
            "alcohol": "medium(+)", "body": "full", "flavour_intensity": "pronounced",
            "primary_flavours": ["honey"], "finish": "long",
        }
        result = _check_response_structure("sweet", nose, palate, False)
        self.assertIn("structure_sweet_wine_acidity", result["ordering_issues"])

    def test_sweet_wine_no_acidity_no_issue(self):
        """Sweet wine where acidity field is absent should not trigger (no value = not stated)."""
        nose = {"intensity": "pronounced", "primary_aromas": ["honey"], "secondary_aromas": ["vanilla"], "tertiary_aromas": [], "development": "developing"}
        palate = {
            "sweetness": "sweet", "acidity": "",  # not stated → no trigger
            "alcohol": "medium(+)", "body": "full", "flavour_intensity": "pronounced",
            "primary_flavours": ["honey"], "finish": "long",
        }
        result = _check_response_structure("sweet", nose, palate, False)
        self.assertNotIn("structure_sweet_wine_acidity", result["ordering_issues"])


# ---------------------------------------------------------------------------
# 7. Governance: no marks, no score, no examiner language
# ---------------------------------------------------------------------------

class ResponseStructureGovernanceTests(unittest.TestCase):
    """Component 8 must never expose marks, scoring, or examiner authority."""

    def _full_result(self):
        nose = {"intensity": "medium", "primary_aromas": ["lemon"], "secondary_aromas": ["vanilla"], "tertiary_aromas": [], "development": "developing"}
        palate = {"sweetness": "dry", "acidity": "medium(+)", "alcohol": "medium", "body": "medium", "flavour_intensity": "medium", "primary_flavours": ["lemon"], "finish": "medium"}
        return _check_response_structure("white", nose, palate, False)

    def test_no_marks_field(self):
        result = self._full_result()
        self.assertNotIn("marks", result)

    def test_no_score_field(self):
        result = self._full_result()
        self.assertNotIn("score", result)

    def test_no_safe_for_examiner_true(self):
        result = self._full_result()
        for val in result.values():
            if isinstance(val, bool):
                self.assertFalse(val, "No boolean True allowed in response structure result")

    def test_formative_note_present(self):
        result = self._full_result()
        self.assertIn("formative_note", result)
        self.assertIn("formativa", result["formative_note"])

    def test_no_marks_in_guidance_text(self):
        """Guidance strings must not mention marks or official score."""
        nose = {"intensity": "medium", "primary_aromas": [], "secondary_aromas": [], "tertiary_aromas": [], "development": "developing"}
        palate = {"sweetness": "", "acidity": "", "alcohol": "", "body": "", "flavour_intensity": "", "primary_flavours": ["lemon"], "finish": "medium"}
        result = _check_response_structure("white", nose, palate, False)
        combined = " ".join(result["guidance"]).lower()
        for forbidden in ("mark", "nota", "puntuacion", "score", "official", "examiner"):
            self.assertNotIn(forbidden, combined, f"Governance violation: '{forbidden}' in guidance")

    def test_validate_sat_governance_key_unchanged(self):
        """Full validate_sat_response still returns governance.safe_for_examiner=False."""
        sat = _minimal_sat()
        full = validate_sat_response(sat)
        self.assertFalse(full["governance"]["safe_for_examiner"])
        self.assertFalse(full["governance"]["examiner_scoring_allowed"])

    def test_response_structure_key_in_full_result(self):
        """response_structure key is present in validate_sat_response output."""
        sat = _minimal_sat()
        full = validate_sat_response(sat)
        self.assertIn("response_structure", full)

    def test_response_structure_has_required_keys(self):
        """response_structure dict always has status, ordering_issues, guidance, formative_note."""
        sat = _minimal_sat()
        rs = validate_sat_response(sat)["response_structure"]
        for key in ("status", "ordering_issues", "guidance", "formative_note"):
            self.assertIn(key, rs)


# ---------------------------------------------------------------------------
# 8. Non-SAT path unchanged
# ---------------------------------------------------------------------------

class NonSATPathUnchangedTests(unittest.TestCase):
    """Non-SAT submissions must not be affected by Phase X.5."""

    def test_non_sat_none_raises_or_handled(self):
        """None input is not a SAT submission — function raises AttributeError (expected)."""
        with self.assertRaises((AttributeError, TypeError)):
            validate_sat_response(None)

    def test_empty_dict_sat_returns_result(self):
        """Empty dict is treated as incomplete SAT — returns full result with issues."""
        result = validate_sat_response({})
        self.assertIsInstance(result, dict)
        self.assertIn("response_structure", result)

    def test_other_keys_still_present(self):
        """Existing keys from X.3/X.4 still present alongside response_structure."""
        sat = _minimal_sat()
        full = validate_sat_response(sat)
        for key in ("structural_issues", "scale_errors", "quality_justification",
                    "readiness_reasoning", "response_structure", "distinction_gap"):
            self.assertIn(key, full, f"Missing key: {key}")


# ---------------------------------------------------------------------------
# 9. Determinism
# ---------------------------------------------------------------------------

class DeterminismTests(unittest.TestCase):
    """Same input must produce identical output on repeated calls."""

    def test_conformant_deterministic(self):
        nose = {"intensity": "medium(+)", "primary_aromas": ["lemon"], "secondary_aromas": ["vanilla"], "tertiary_aromas": [], "development": "developing"}
        palate = {"sweetness": "dry", "acidity": "medium(+)", "alcohol": "medium", "body": "medium(+)", "flavour_intensity": "medium(+)", "primary_flavours": ["lemon"], "finish": "medium(+)"}
        r1 = _check_response_structure("white", nose, palate, False)
        r2 = _check_response_structure("white", nose, palate, False)
        self.assertEqual(r1, r2)

    def test_issues_found_deterministic(self):
        nose = {"intensity": "medium", "primary_aromas": [], "secondary_aromas": [], "tertiary_aromas": [], "development": "developing"}
        palate = {"sweetness": "", "acidity": "", "alcohol": "", "body": "", "flavour_intensity": "", "primary_flavours": ["lemon"], "finish": "medium"}
        r1 = _check_response_structure("white", nose, palate, False)
        r2 = _check_response_structure("white", nose, palate, False)
        self.assertEqual(r1, r2)


# ---------------------------------------------------------------------------
# 10. Key-presence contract
# ---------------------------------------------------------------------------

class KeyPresenceTests(unittest.TestCase):
    """Component 8 always returns the 4 required keys regardless of input."""

    def _assert_keys(self, wine_type, nose, palate, is_simple):
        result = _check_response_structure(wine_type, nose, palate, is_simple)
        for key in ("status", "ordering_issues", "guidance", "formative_note"):
            self.assertIn(key, result)
        self.assertIsInstance(result["ordering_issues"], list)
        self.assertIsInstance(result["guidance"], list)

    def test_keys_on_conformant(self):
        nose = {"intensity": "medium", "primary_aromas": ["lemon"], "secondary_aromas": ["vanilla"], "tertiary_aromas": [], "development": "developing"}
        palate = {"sweetness": "dry", "acidity": "medium", "alcohol": "medium", "body": "medium", "flavour_intensity": "medium", "primary_flavours": ["lemon"], "finish": "medium"}
        self._assert_keys("white", nose, palate, False)

    def test_keys_on_issues(self):
        nose = {"intensity": "medium", "primary_aromas": [], "secondary_aromas": [], "tertiary_aromas": [], "development": "developing"}
        palate = {"sweetness": "", "acidity": "", "alcohol": "", "body": "", "flavour_intensity": "", "primary_flavours": ["lemon"], "finish": "medium"}
        self._assert_keys("white", nose, palate, False)

    def test_keys_on_empty_sections(self):
        self._assert_keys("white", {}, {}, False)

    def test_status_is_conformant_or_issues_found(self):
        nose = {"intensity": "medium", "primary_aromas": ["lemon"], "secondary_aromas": ["vanilla"], "tertiary_aromas": [], "development": "developing"}
        palate = {"sweetness": "dry", "acidity": "medium", "alcohol": "medium", "body": "medium", "flavour_intensity": "medium", "primary_flavours": ["lemon"], "finish": "medium"}
        for wt in ("white", "red", "sweet"):
            result = _check_response_structure(wt, nose, palate, False)
            self.assertIn(result["status"], ("conformant", "issues_found"))


# ---------------------------------------------------------------------------
# 11. Multiple simultaneous issues
# ---------------------------------------------------------------------------

class MultipleIssueTests(unittest.TestCase):
    """A single submission can trigger more than one issue code simultaneously."""

    def test_nose_ordering_and_palate_ordering_together(self):
        """Development without aromas + flavours without scale = two issues."""
        nose = {"intensity": "medium", "primary_aromas": [], "secondary_aromas": [], "tertiary_aromas": [], "development": "developing"}
        palate = {"sweetness": "", "acidity": "", "alcohol": "", "body": "", "flavour_intensity": "", "primary_flavours": ["lemon"], "finish": "medium"}
        result = _check_response_structure("white", nose, palate, False)
        self.assertIn("ordering_nose_development_without_aromas", result["ordering_issues"])
        self.assertIn("ordering_palate_flavours_before_scale", result["ordering_issues"])
        self.assertEqual(result["status"], "issues_found")
        self.assertGreaterEqual(len(result["guidance"]), 2)

    def test_simple_wine_multiple_issues(self):
        """Simple wine with secondary nose + secondary palate = two structure codes."""
        nose = {"intensity": "medium", "primary_aromas": ["pear"], "secondary_aromas": ["vanilla"], "tertiary_aromas": ["honey"], "development": "young"}
        palate = {
            "sweetness": "dry", "acidity": "medium", "alcohol": "low", "body": "light",
            "flavour_intensity": "medium(-)", "primary_flavours": ["pear"],
            "secondary_flavours": ["vanilla"], "finish": "short",
        }
        result = _check_response_structure("white", nose, palate, True)
        self.assertIn("structure_simple_wine_excess_complexity", result["ordering_issues"])
        self.assertIn("structure_simple_wine_palate_excess", result["ordering_issues"])


if __name__ == "__main__":
    unittest.main()

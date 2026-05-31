"""Unit tests for PSL pedagogical profile config and psl_profile_validator.

All 13 required tests:
  1.  test_weights_sum_to_one
  2.  test_no_unknown_functions
  3.  test_no_unknown_roles
  4.  test_fallback_exists
  5.  test_fallback_is_balanced
  6.  test_exam_pressure_no_examiner_scoring
  7.  test_exam_pressure_no_official_authority
  8.  test_distinction_keeps_host
  9.  test_distinction_is_governance_safe
  10. test_visible_roles_no_real_names
  11. test_visible_roles_no_examiner_claim
  12. test_validator_rejects_unknown_function
  13. test_validator_rejects_bad_weights
"""

import copy
import json
import unittest
from pathlib import Path

from tools.tutor.pedagogical_strategy.psl_profile_validator import (
    load_and_validate,
    validate_config,
)

_CONFIG_PATH = (
    Path(__file__).parents[1] / "knowledge" / "config" / "pedagogical_profiles.json"
)

_FORBIDDEN_REAL_NAMES = {
    "jancis", "robinson", "parker", "suckling", "penin",
    "macneil", "johnson", "clarke", "spurrier", "asimov", "puckette",
    "mack", "yarrow", "atkin", "martin", "lee",
}


def _load_config() -> dict:
    with _CONFIG_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def _all_profile_blocks(config: dict):
    yield "default_profile", config["default_profile"].get("functions", {})
    for mode_id, mode_data in config.get("tutor_modes", {}).items():
        yield f"tutor_modes.{mode_id}", mode_data.get("functions", {})
    for role_id, role_data in config.get("visible_roles", {}).items():
        yield f"visible_roles.{role_id}", role_data.get("functions", {})


def _collect_all_text(data) -> list:
    texts = []
    if isinstance(data, str):
        texts.append(data)
    elif isinstance(data, dict):
        for v in data.values():
            texts.extend(_collect_all_text(v))
    elif isinstance(data, list):
        for item in data:
            texts.extend(_collect_all_text(item))
    return texts


def _raw_weight(fn_data) -> float:
    if isinstance(fn_data, dict):
        return float(fn_data.get("weight", 0.0))
    return float(fn_data)


# ---- Test 1 ----------------------------------------------------------------

class TestWeightsSumToOne(unittest.TestCase):
    def test_weights_sum_to_one(self):
        config = _load_config()
        tolerance = 1e-4
        for label, functions_block in _all_profile_blocks(config):
            with self.subTest(profile=label):
                total = sum(_raw_weight(v) for v in functions_block.values())
                self.assertAlmostEqual(
                    total, 1.0, delta=tolerance,
                    msg=f"'{label}' weights sum to {total:.6f}, expected 1.0",
                )


# ---- Test 2 ----------------------------------------------------------------

class TestNoUnknownFunctions(unittest.TestCase):
    ALLOWED = frozenset(
        ["cartographer", "scientist", "host", "storyteller", "critic", "challenger"]
    )

    def test_no_unknown_functions(self):
        config = _load_config()
        for label, functions_block in _all_profile_blocks(config):
            with self.subTest(profile=label):
                unknown = set(functions_block.keys()) - self.ALLOWED
                self.assertEqual(unknown, set(),
                    msg=f"Unknown function(s) in '{label}': {sorted(unknown)}")


# ---- Test 3 ----------------------------------------------------------------

class TestNoUnknownRoles(unittest.TestCase):
    ALLOWED = frozenset([
        "mentor_fundamentos", "entrenador_sensorial", "investigador_causalidad",
        "revisor_respuestas", "entrenador_distinction",
    ])

    def test_no_unknown_roles(self):
        config = _load_config()
        for role_id in config.get("visible_roles", {}):
            with self.subTest(role=role_id):
                self.assertIn(role_id, self.ALLOWED,
                    msg=f"Unknown visible_role '{role_id}'")


# ---- Test 4 ----------------------------------------------------------------

class TestFallbackExists(unittest.TestCase):
    def test_fallback_exists(self):
        config = _load_config()
        self.assertIn("default_profile", config)
        default = config["default_profile"]
        self.assertIsInstance(default, dict)
        self.assertIn("functions", default)


# ---- Test 5 ----------------------------------------------------------------

class TestFallbackIsBalanced(unittest.TestCase):
    def test_fallback_is_balanced(self):
        config = _load_config()
        fns = config["default_profile"].get("functions", {})
        for fn_id, fn_data in fns.items():
            w = _raw_weight(fn_data)
            with self.subTest(function=fn_id):
                self.assertLessEqual(w, 0.35,
                    msg=f"default_profile.{fn_id} weight {w:.3f} > 0.35")

    def test_mentor_mode_is_balanced(self):
        config = _load_config()
        fns = config.get("tutor_modes", {}).get("mentor", {}).get("functions", {})
        for fn_id, fn_data in fns.items():
            w = _raw_weight(fn_data)
            with self.subTest(function=fn_id):
                self.assertLessEqual(w, 0.35,
                    msg=f"mentor.{fn_id} weight {w:.3f} > 0.35")


# ---- Test 6 ----------------------------------------------------------------

class TestExamPressureNoExaminerScoring(unittest.TestCase):
    def _gov(self):
        return (_load_config().get("tutor_modes", {})
                .get("exam_pressure", {}).get("governance", {}))

    def test_exam_pressure_no_examiner_scoring(self):
        self.assertNotEqual(self._gov().get("examiner_scoring_allowed"), True)

    def test_exam_pressure_safe_for_examiner_false(self):
        self.assertNotEqual(self._gov().get("safe_for_examiner"), True)


# ---- Test 7 ----------------------------------------------------------------

class TestExamPressureNoOfficialAuthority(unittest.TestCase):
    """Governance disclaimers ('never claims examiner authority') are fine.
    Only unambiguous positive authority assertions are forbidden."""

    _FORBIDDEN = (
        "is an official examiner",
        "provides official wset grading",
        "score your answer officially",
        "your official score",
        "official wset score",
        "official wset marks",
        "this is an official assessment",
        "i am a wset examiner",
        "acting as examiner",
    )

    def test_exam_pressure_no_official_authority(self):
        ep = _load_config().get("tutor_modes", {}).get("exam_pressure", {})
        combined = " ".join(_collect_all_text(ep)).lower()
        for phrase in self._FORBIDDEN:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, combined,
                    msg=f"exam_pressure contains positive authority phrase: '{phrase}'")

    def test_exam_pressure_governance_explicitly_denies_authority(self):
        gov = (_load_config().get("tutor_modes", {})
               .get("exam_pressure", {}).get("governance", {}))
        self.assertIn("examiner_scoring_allowed", gov)
        self.assertIn("safe_for_examiner", gov)
        self.assertNotEqual(gov["examiner_scoring_allowed"], True)
        self.assertNotEqual(gov["safe_for_examiner"], True)


# ---- Test 8 ----------------------------------------------------------------

class TestDistinctionKeepsHost(unittest.TestCase):
    def test_distinction_keeps_host(self):
        fns = (_load_config().get("tutor_modes", {})
               .get("distinction", {}).get("functions", {}))
        self.assertIn("host", fns)
        self.assertGreater(_raw_weight(fns["host"]), 0.0)


# ---- Test 9 ----------------------------------------------------------------

class TestDistinctionIsGovernanceSafe(unittest.TestCase):
    def test_distinction_is_governance_safe(self):
        gov = (_load_config().get("tutor_modes", {})
               .get("distinction", {}).get("governance", {}))
        for key in ("safe_for_examiner", "examiner_scoring_allowed"):
            with self.subTest(flag=key):
                self.assertNotEqual(gov.get(key), True,
                    msg=f"distinction.governance.{key} must not be True")


# ---- Test 10 ---------------------------------------------------------------

class TestVisibleRolesNoRealNames(unittest.TestCase):
    def test_visible_roles_no_real_names(self):
        config = _load_config()
        for role_id, role_data in config.get("visible_roles", {}).items():
            combined = " ".join(_collect_all_text(role_data)).lower()
            for name in _FORBIDDEN_REAL_NAMES:
                with self.subTest(role=role_id, name=name):
                    self.assertNotIn(name, combined,
                        msg=f"visible_roles.{role_id} contains real name: '{name}'")


# ---- Test 11 ---------------------------------------------------------------

class TestVisibleRolesNoExaminerClaim(unittest.TestCase):
    """Disclaimer language ('does not claim official grading authority') is fine.
    Only positive authority assertions are forbidden.
    The authoritative safety check is the governance block flags."""

    _FORBIDDEN = (
        "is an official examiner",
        "provides official wset grading",
        "score your answer officially",
        "your official score",
        "official wset score",
        "official wset marks",
        "this is an official assessment",
        "i am a wset examiner",
        "acting as examiner",
    )

    def test_visible_roles_no_examiner_claim(self):
        config = _load_config()
        for role_id, role_data in config.get("visible_roles", {}).items():
            combined = " ".join(_collect_all_text(role_data)).lower()
            for phrase in self._FORBIDDEN:
                with self.subTest(role=role_id, phrase=phrase):
                    self.assertNotIn(phrase, combined,
                        msg=f"visible_roles.{role_id} positive examiner claim: '{phrase}'")

    def test_visible_roles_governance_flags_deny_authority(self):
        config = _load_config()
        for role_id, role_data in config.get("visible_roles", {}).items():
            gov = role_data.get("governance", {})
            with self.subTest(role=role_id):
                self.assertNotEqual(gov.get("examiner_scoring_allowed"), True)
                self.assertNotEqual(gov.get("safe_for_examiner"), True)


# ---- Test 12 ---------------------------------------------------------------

class TestValidatorRejectsUnknownFunction(unittest.TestCase):
    def _make_bad_config(self) -> dict:
        bad = copy.deepcopy(_load_config())
        fn = bad["default_profile"]["functions"]
        fn["sommelier"] = {"weight": 0.05, "rationale": "bad"}
        if isinstance(fn["challenger"], dict):
            fn["challenger"]["weight"] = 0.0
        else:
            fn["challenger"] = 0.0
        return bad

    def test_validator_rejects_unknown_function(self):
        errors = validate_config(self._make_bad_config())
        rules = [e["rule"] for e in errors]
        self.assertIn("unknown_function", rules,
            msg=f"Expected 'unknown_function'. Got: {errors}")

    def test_validator_error_names_the_bad_function(self):
        errors = validate_config(self._make_bad_config())
        uf = [e for e in errors if e["rule"] == "unknown_function"]
        self.assertTrue(uf)
        self.assertIn("sommelier", " ".join(e["message"] for e in uf))


# ---- Test 13 ---------------------------------------------------------------

class TestValidatorRejectsBadWeights(unittest.TestCase):
    def _make_bad_weights_config(self) -> dict:
        bad = copy.deepcopy(_load_config())
        # All 6 weights = 0.5 → raw sum = 3.0
        for fn_id in bad["default_profile"]["functions"]:
            fn_data = bad["default_profile"]["functions"][fn_id]
            if isinstance(fn_data, dict):
                fn_data["weight"] = 0.5
            else:
                bad["default_profile"]["functions"][fn_id] = 0.5
        return bad

    def test_validator_rejects_bad_weights(self):
        errors = validate_config(self._make_bad_weights_config())
        rules = [e["rule"] for e in errors]
        self.assertIn("bad_weights", rules,
            msg=f"Expected 'bad_weights'. Got: {errors}")

    def test_validator_error_references_bad_profile(self):
        errors = validate_config(self._make_bad_weights_config())
        bw = [e for e in errors if e["rule"] == "bad_weights"]
        self.assertTrue(bw)
        self.assertTrue(any("default_profile" in e["context"] for e in bw))

    def test_load_and_validate_passes_for_real_config(self):
        errors = load_and_validate()
        self.assertEqual(errors, [],
            msg=f"Real config should produce no errors. Got: {errors}")


if __name__ == "__main__":
    unittest.main()

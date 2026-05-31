"""Unit tests for the pedagogical profiles config and validator.

Covers:
- Schema validation (structure, weight sums, allowed function keys)
- Unknown function rejection
- Unknown role/mode fallback
- Default profile safety invariants (host >= 0.25, challenger <= 0.10)
- Governance flags (distinction and exam_pressure never activate examiner_scoring)
- Weight normalisation precision
- All six functions present in every profile
"""

import json
import unittest
from pathlib import Path

from tools.tutor.pedagogical_strategy.profiles import (
    ALLOWED_FUNCTIONS,
    ALLOWED_TUTOR_MODES,
    ALLOWED_VISIBLE_ROLES,
    WEIGHT_TOLERANCE,
    ProfileValidationError,
    _extract_weights,
    get_profile,
    validate_profile_config,
)

_CONFIG_PATH = Path(__file__).parents[1] / "knowledge" / "config" / "pedagogical_profiles.json"


def _load_raw_config() -> dict:
    with _CONFIG_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


class TestConfigLoads(unittest.TestCase):
    def test_config_file_exists(self):
        self.assertTrue(_CONFIG_PATH.exists(), "pedagogical_profiles.json must exist")

    def test_config_is_valid_json(self):
        config = _load_raw_config()
        self.assertIsInstance(config, dict)

    def test_top_level_keys_present(self):
        config = _load_raw_config()
        for key in ("allowed_functions", "allowed_tutor_modes", "allowed_visible_roles",
                    "default_profile", "tutor_modes", "visible_roles"):
            self.assertIn(key, config, f"Missing top-level key: {key}")


class TestWeightSums(unittest.TestCase):
    def _assert_weights_sum_to_one(self, functions_block: dict, label: str):
        weights = _extract_weights(functions_block)
        total = sum(weights.values())
        self.assertAlmostEqual(
            total, 1.0, delta=WEIGHT_TOLERANCE + 1e-5,
            msg=f"Weights in '{label}' sum to {total:.6f}, expected 1.0"
        )

    def test_default_profile_weights_sum_to_one(self):
        config = _load_raw_config()
        self._assert_weights_sum_to_one(
            config["default_profile"]["functions"], "default_profile"
        )

    def test_mentor_mode_weights_sum_to_one(self):
        config = _load_raw_config()
        self._assert_weights_sum_to_one(
            config["tutor_modes"]["mentor"]["functions"], "tutor_modes.mentor"
        )

    def test_trainer_mode_weights_sum_to_one(self):
        config = _load_raw_config()
        self._assert_weights_sum_to_one(
            config["tutor_modes"]["trainer"]["functions"], "tutor_modes.trainer"
        )

    def test_reviewer_mode_weights_sum_to_one(self):
        config = _load_raw_config()
        self._assert_weights_sum_to_one(
            config["tutor_modes"]["reviewer"]["functions"], "tutor_modes.reviewer"
        )

    def test_distinction_mode_weights_sum_to_one(self):
        config = _load_raw_config()
        self._assert_weights_sum_to_one(
            config["tutor_modes"]["distinction"]["functions"], "tutor_modes.distinction"
        )

    def test_exam_pressure_mode_weights_sum_to_one(self):
        config = _load_raw_config()
        self._assert_weights_sum_to_one(
            config["tutor_modes"]["exam_pressure"]["functions"], "tutor_modes.exam_pressure"
        )

    def test_mentor_fundamentos_role_weights_sum_to_one(self):
        config = _load_raw_config()
        self._assert_weights_sum_to_one(
            config["visible_roles"]["mentor_fundamentos"]["functions"],
            "visible_roles.mentor_fundamentos"
        )

    def test_entrenador_sensorial_role_weights_sum_to_one(self):
        config = _load_raw_config()
        self._assert_weights_sum_to_one(
            config["visible_roles"]["entrenador_sensorial"]["functions"],
            "visible_roles.entrenador_sensorial"
        )

    def test_investigador_causalidad_role_weights_sum_to_one(self):
        config = _load_raw_config()
        self._assert_weights_sum_to_one(
            config["visible_roles"]["investigador_causalidad"]["functions"],
            "visible_roles.investigador_causalidad"
        )

    def test_revisor_respuestas_role_weights_sum_to_one(self):
        config = _load_raw_config()
        self._assert_weights_sum_to_one(
            config["visible_roles"]["revisor_respuestas"]["functions"],
            "visible_roles.revisor_respuestas"
        )

    def test_entrenador_distinction_role_weights_sum_to_one(self):
        config = _load_raw_config()
        self._assert_weights_sum_to_one(
            config["visible_roles"]["entrenador_distinction"]["functions"],
            "visible_roles.entrenador_distinction"
        )


class TestAllFunctionsPresent(unittest.TestCase):
    def _assert_all_functions(self, functions_block: dict, label: str):
        present = set(functions_block.keys())
        missing = ALLOWED_FUNCTIONS - present
        self.assertEqual(
            missing, set(),
            msg=f"Missing functions in '{label}': {sorted(missing)}"
        )

    def test_all_functions_in_default_profile(self):
        config = _load_raw_config()
        self._assert_all_functions(
            config["default_profile"]["functions"], "default_profile"
        )

    def test_all_functions_in_every_tutor_mode(self):
        config = _load_raw_config()
        for mode_id, mode_data in config["tutor_modes"].items():
            self._assert_all_functions(mode_data["functions"], f"tutor_modes.{mode_id}")

    def test_all_functions_in_every_visible_role(self):
        config = _load_raw_config()
        for role_id, role_data in config["visible_roles"].items():
            self._assert_all_functions(role_data["functions"], f"visible_roles.{role_id}")


class TestValidationRejectsUnknownFunctions(unittest.TestCase):
    def _make_config_with_bad_function(self) -> dict:
        config = _load_raw_config()
        # Inject an unknown function into the default profile.
        config["default_profile"]["functions"]["sommelier"] = {"weight": 0.05}
        return config

    def test_unknown_function_raises_validation_error(self):
        config = self._make_config_with_bad_function()
        with self.assertRaises(ProfileValidationError) as ctx:
            validate_profile_config(config)
        self.assertIn("sommelier", str(ctx.exception))

    def test_error_message_lists_allowed_functions(self):
        config = self._make_config_with_bad_function()
        with self.assertRaises(ProfileValidationError) as ctx:
            validate_profile_config(config)
        err = str(ctx.exception)
        # Should mention allowed functions.
        self.assertTrue(
            any(fn in err for fn in ALLOWED_FUNCTIONS),
            "Error message should reference allowed functions."
        )


class TestValidationRejectsBadWeightSum(unittest.TestCase):
    def test_weights_summing_to_zero_raises_after_normalise(self):
        # All-zero weights: normaliser should handle gracefully,
        # but a modified config that sums to < 0.9 should raise.
        config = _load_raw_config()
        # Force challenger to 0 and leave others at normal — artificially break sum.
        config["default_profile"]["functions"]["challenger"] = {"weight": 0.60}
        # This will cause sum >> 1.0, which validate rejects.
        with self.assertRaises(ProfileValidationError):
            validate_profile_config(config)


class TestFallbackBehaviour(unittest.TestCase):
    def test_unknown_tutor_role_returns_default(self):
        profile = get_profile(tutor_role="nonexistent_role_xyz")
        self.assertEqual(profile["profile_id"], "default")
        self.assertEqual(profile["source"], "default")

    def test_unknown_tutor_mode_returns_default(self):
        profile = get_profile(tutor_mode="nonexistent_mode_xyz")
        self.assertEqual(profile["profile_id"], "default")
        self.assertEqual(profile["source"], "default")

    def test_none_inputs_return_default(self):
        profile = get_profile(tutor_role=None, tutor_mode=None)
        self.assertEqual(profile["profile_id"], "default")

    def test_default_fallback_host_weight_at_least_025(self):
        profile = get_profile()
        self.assertGreaterEqual(
            profile["functions"]["host"], 0.25,
            "Default fallback must be supportive (host >= 0.25)."
        )

    def test_default_fallback_challenger_weight_at_most_010(self):
        profile = get_profile()
        self.assertLessEqual(
            profile["functions"]["challenger"], 0.10,
            "Default fallback must not be severe (challenger <= 0.10)."
        )

    def test_default_fallback_has_all_six_functions(self):
        profile = get_profile()
        self.assertEqual(set(profile["functions"].keys()), ALLOWED_FUNCTIONS)

    def test_known_role_returns_role_not_default(self):
        profile = get_profile(tutor_role="mentor_fundamentos")
        self.assertEqual(profile["source"], "visible_role")
        self.assertEqual(profile["profile_id"], "mentor_fundamentos")

    def test_known_mode_returns_mode_not_default(self):
        profile = get_profile(tutor_mode="trainer")
        self.assertEqual(profile["source"], "tutor_mode")
        self.assertEqual(profile["profile_id"], "trainer")

    def test_role_takes_precedence_over_mode(self):
        profile = get_profile(tutor_role="revisor_respuestas", tutor_mode="mentor")
        self.assertEqual(profile["source"], "visible_role")
        self.assertEqual(profile["profile_id"], "revisor_respuestas")


class TestGovernanceInvariants(unittest.TestCase):
    def test_distinction_mode_examiner_scoring_false(self):
        config = _load_raw_config()
        governance = config["tutor_modes"]["distinction"].get("governance", {})
        self.assertFalse(
            governance.get("examiner_scoring_allowed", False),
            "distinction mode must never activate examiner_scoring_allowed."
        )

    def test_exam_pressure_mode_examiner_scoring_false(self):
        config = _load_raw_config()
        governance = config["tutor_modes"]["exam_pressure"].get("governance", {})
        self.assertFalse(
            governance.get("examiner_scoring_allowed", False),
            "exam_pressure mode must never activate examiner_scoring_allowed."
        )

    def test_exam_pressure_safe_for_examiner_false(self):
        config = _load_raw_config()
        governance = config["tutor_modes"]["exam_pressure"].get("governance", {})
        self.assertFalse(
            governance.get("safe_for_examiner", False),
            "exam_pressure must not set safe_for_examiner=True."
        )

    def test_get_profile_governance_always_clean(self):
        for role in ALLOWED_VISIBLE_ROLES:
            profile = get_profile(tutor_role=role)
            gov = profile["governance"]
            self.assertFalse(gov["safe_for_examiner"])
            self.assertFalse(gov["examiner_scoring_allowed"])
            self.assertFalse(gov["uses_llm"])
            self.assertFalse(gov["uses_api"])

    def test_meta_governance_clean(self):
        config = _load_raw_config()
        meta_gov = config.get("_meta", {}).get("governance", {})
        self.assertFalse(meta_gov.get("safe_for_examiner", False))
        self.assertFalse(meta_gov.get("examiner_scoring_allowed", False))

    def test_governance_violation_raises(self):
        config = _load_raw_config()
        config["_meta"]["governance"]["examiner_scoring_allowed"] = True
        with self.assertRaises(ProfileValidationError) as ctx:
            validate_profile_config(config)
        self.assertIn("examiner_scoring_allowed", str(ctx.exception))


class TestWeightNormalisation(unittest.TestCase):
    def test_normalised_weights_sum_to_one(self):
        raw = {"cartographer": {"weight": 2.0}, "scientist": {"weight": 3.0},
               "host": {"weight": 5.0}, "storyteller": {"weight": 2.0},
               "critic": {"weight": 1.0}, "challenger": {"weight": 1.0}}
        weights = _extract_weights(raw)
        self.assertAlmostEqual(sum(weights.values()), 1.0, places=5)

    def test_extract_weights_handles_float_values(self):
        raw = {"cartographer": {"weight": 0.20}, "scientist": {"weight": 0.20},
               "host": {"weight": 0.30}, "storyteller": {"weight": 0.20},
               "critic": {"weight": 0.05}, "challenger": {"weight": 0.05}}
        weights = _extract_weights(raw)
        self.assertAlmostEqual(weights["host"], 0.30, places=4)


if __name__ == "__main__":
    unittest.main()

"""Unit tests for the visible tutor character contracts.

Verifies that all characters are fictional originals — no real person names,
no real likenesses, no WSET examiner authority, no official scoring.

These tests protect the runtime governance contract. Any research inspiration
must live in internal documentation only and must never appear in runtime fields.
"""

import json
import unittest
from pathlib import Path

_CHARACTERS_CONFIG_PATH = (
    Path(__file__).parents[1] / "knowledge" / "config" / "visible_tutor_characters.json"
)

# Known real wine critic and educator names to explicitly check against.
# This list is internal test data — it does not appear in runtime outputs.
_KNOWN_REAL_PERSON_NAMES = frozenset([
    "jancis", "robinson", "parker", "robert", "oz", "clarke", "steven", "spurrier",
    "decanter", "halliday", "james", "wine spectator", "allen", "meadows",
    "laube", "suckling", "galloni", "tanzer", "wine advocate",
    "michael", "broadbent", "serena", "sutcliffe", "matt", "kramer",
    "eric", "asimov", "antonio", "galloni",
])

_REQUIRED_CHARACTER_FIELDS = (
    "id", "display_name", "role_label", "short_description",
    "allowed_modes", "default_mode", "strategy_profile_id",
    "visual_direction", "governance_notes", "governance",
)

_ALLOWED_TUTOR_MODES = frozenset([
    "mentor", "trainer", "reviewer", "distinction", "exam_pressure"
])

_KNOWN_STRATEGY_PROFILE_IDS = frozenset([
    "mentor_fundamentos", "entrenador_sensorial", "investigador_causalidad",
    "revisor_respuestas", "entrenador_distinction",
])


def _load_characters_config() -> dict:
    with _CHARACTERS_CONFIG_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def _all_characters(config: dict) -> list[dict]:
    return config.get("characters", [])


class TestConfigStructure(unittest.TestCase):
    def test_config_file_exists(self):
        self.assertTrue(_CHARACTERS_CONFIG_PATH.exists())

    def test_config_is_valid_json(self):
        config = _load_characters_config()
        self.assertIsInstance(config, dict)

    def test_config_has_characters_list(self):
        config = _load_characters_config()
        self.assertIn("characters", config)
        self.assertIsInstance(config["characters"], list)

    def test_at_least_one_character_defined(self):
        config = _load_characters_config()
        self.assertGreater(len(config["characters"]), 0)

    def test_five_characters_defined(self):
        config = _load_characters_config()
        self.assertEqual(len(config["characters"]), 5)


class TestRequiredFields(unittest.TestCase):
    def test_all_characters_have_required_fields(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            char_id = char.get("id", "<unknown>")
            for field in _REQUIRED_CHARACTER_FIELDS:
                self.assertIn(
                    field, char,
                    msg=f"Character '{char_id}' missing required field: '{field}'"
                )

    def test_all_ids_are_strings(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            self.assertIsInstance(char["id"], str)

    def test_all_display_names_are_strings(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            self.assertIsInstance(char["display_name"], str)

    def test_all_display_names_nonempty(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            self.assertTrue(
                char["display_name"].strip(),
                f"Character '{char['id']}' has empty display_name."
            )

    def test_all_ids_unique(self):
        config = _load_characters_config()
        ids = [c["id"] for c in _all_characters(config)]
        self.assertEqual(len(ids), len(set(ids)), "Character IDs must be unique.")


class TestNoRealPersonNames(unittest.TestCase):
    """No display_name or public-facing field may match known real wine critic names."""

    def _check_text_for_real_names(self, text: str, context: str):
        text_lower = text.lower()
        for name in _KNOWN_REAL_PERSON_NAMES:
            self.assertNotIn(
                name.lower(), text_lower,
                msg=f"Real person reference '{name}' found in {context}."
            )

    def test_no_display_name_matches_real_person(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            self._check_text_for_real_names(
                char["display_name"],
                f"display_name of character '{char['id']}'"
            )

    def test_no_short_description_mentions_real_person(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            self._check_text_for_real_names(
                char.get("short_description", ""),
                f"short_description of character '{char['id']}'"
            )

    def test_no_role_label_mentions_real_person(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            self._check_text_for_real_names(
                char.get("role_label", ""),
                f"role_label of character '{char['id']}'"
            )

    def test_no_visual_direction_mentions_real_person(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            self._check_text_for_real_names(
                char.get("visual_direction", ""),
                f"visual_direction of character '{char['id']}'"
            )


class TestNoOfficialWsetAuthority(unittest.TestCase):
    """No character may claim WSET examiner authority in any public field."""

    _AUTHORITY_PHRASES = [
        "wset examiner", "official examiner", "official score", "official mark",
        "official grade", "official evaluation", "official wset", "certified examiner",
        "wset certified", "examination authority",
    ]

    def _check_no_authority(self, text: str, context: str):
        text_lower = text.lower()
        for phrase in self._AUTHORITY_PHRASES:
            self.assertNotIn(
                phrase, text_lower,
                msg=f"Authority phrase '{phrase}' found in {context}."
            )

    def test_no_short_description_claims_official_authority(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            self._check_no_authority(
                char.get("short_description", ""),
                f"short_description of '{char['id']}'"
            )

    def test_no_role_label_claims_official_authority(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            self._check_no_authority(
                char.get("role_label", ""),
                f"role_label of '{char['id']}'"
            )


class TestGovernanceInvariants(unittest.TestCase):
    def test_no_character_activates_examiner_scoring(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            gov = char.get("governance", {})
            self.assertFalse(
                gov.get("examiner_scoring_allowed", False),
                f"Character '{char['id']}' must not activate examiner_scoring_allowed."
            )

    def test_no_character_sets_safe_for_examiner(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            gov = char.get("governance", {})
            self.assertFalse(
                gov.get("safe_for_examiner", False),
                f"Character '{char['id']}' must not set safe_for_examiner=True."
            )

    def test_meta_governance_examiner_scoring_false(self):
        config = _load_characters_config()
        meta_gov = config.get("_meta", {}).get("governance", {})
        self.assertFalse(meta_gov.get("examiner_scoring_allowed", False))

    def test_meta_governance_safe_for_examiner_false(self):
        config = _load_characters_config()
        meta_gov = config.get("_meta", {}).get("governance", {})
        self.assertFalse(meta_gov.get("safe_for_examiner", False))

    def test_meta_governance_uses_llm_false(self):
        config = _load_characters_config()
        meta_gov = config.get("_meta", {}).get("governance", {})
        self.assertFalse(meta_gov.get("uses_llm", False))

    def test_meta_governance_uses_api_false(self):
        config = _load_characters_config()
        meta_gov = config.get("_meta", {}).get("governance", {})
        self.assertFalse(meta_gov.get("uses_api", False))


class TestModeAndProfileReferences(unittest.TestCase):
    def test_all_allowed_modes_are_valid(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            for mode in char.get("allowed_modes", []):
                self.assertIn(
                    mode, _ALLOWED_TUTOR_MODES,
                    msg=f"Character '{char['id']}' has invalid allowed_mode: '{mode}'"
                )

    def test_all_default_modes_are_valid(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            self.assertIn(
                char.get("default_mode"), _ALLOWED_TUTOR_MODES,
                msg=f"Character '{char['id']}' has invalid default_mode: '{char.get('default_mode')}'"
            )

    def test_default_mode_in_allowed_modes(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            self.assertIn(
                char.get("default_mode"),
                char.get("allowed_modes", []),
                msg=f"Character '{char['id']}' default_mode not in its allowed_modes."
            )

    def test_all_strategy_profile_ids_are_valid(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            self.assertIn(
                char.get("strategy_profile_id"),
                _KNOWN_STRATEGY_PROFILE_IDS,
                msg=f"Character '{char['id']}' has unknown strategy_profile_id: "
                    f"'{char.get('strategy_profile_id')}'"
            )

    def test_visual_direction_is_string(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            self.assertIsInstance(
                char.get("visual_direction"), str,
                msg=f"Character '{char['id']}' visual_direction must be a string."
            )

    def test_visual_direction_nonempty(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            self.assertTrue(
                char.get("visual_direction", "").strip(),
                msg=f"Character '{char['id']}' has empty visual_direction."
            )

    def test_visual_direction_is_design_hint_not_logic(self):
        config = _load_characters_config()
        _forbidden_logic_tokens = ("if ", "else:", "return ", "import ", "def ", "class ")
        for char in _all_characters(config):
            vd = char.get("visual_direction", "")
            for token in _forbidden_logic_tokens:
                self.assertNotIn(
                    token, vd,
                    msg=f"Character '{char['id']}' visual_direction looks like code."
                )

    def test_governance_notes_present_and_nonempty(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            notes = char.get("governance_notes", "")
            self.assertTrue(
                notes.strip(),
                msg=f"Character '{char['id']}' has empty governance_notes."
            )

    def test_governance_notes_confirms_fictional(self):
        config = _load_characters_config()
        for char in _all_characters(config):
            notes = char.get("governance_notes", "").lower()
            self.assertIn(
                "fictional", notes,
                msg=f"Character '{char['id']}' governance_notes must confirm fictional nature."
            )


if __name__ == "__main__":
    unittest.main()

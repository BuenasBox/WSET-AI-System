"""PSL Visible Tutor Characters — full contract test suite.

Covers:
  - All 5 visible tutor roles have a character entry (test 1)
  - No display_name matches known real wine critic names (test 2)
  - No short_description mentions real persons (test 3)
  - No description claims official WSET examiner authority (test 4)
  - All 8 required fields present on every character (test 5)
  - All allowed_modes are valid tutor modes (test 6)
  - default_mode is in allowed_modes for each character (test 7)
  - strategy_profile_id maps to an existing profile in pedagogical_profiles.json (test 8)
  - No character can activate examiner_scoring_allowed (test 9)
  - character_resolver returns fallback for unknown role (test 10)
  - validate_character() returns errors for a character with real critic name (test 11)
  - avatar_stub is_avatar_implemented() always returns False (test 12)
  - avatar_stub get_avatar_stub() never raises (test 13)
  - governance_notes present and non-empty on all characters (test 14)
"""

import json
import unittest
from pathlib import Path

from tools.tutor.pedagogical_strategy.character_resolver import (
    get_character,
    list_characters,
    validate_character,
    _FALLBACK_ROLE,
    _FORBIDDEN_REAL_NAMES,
)
from tools.tutor.pedagogical_strategy.avatar_stub import (
    AvatarStub,
    get_avatar_stub,
    is_avatar_implemented,
    resolve_avatar_to_role,
    AVATAR_INTERFACE,
)

_CHARACTERS_CONFIG_PATH = (
    Path(__file__).parents[1] / "knowledge" / "config" / "visible_tutor_characters.json"
)
_PROFILES_CONFIG_PATH = (
    Path(__file__).parents[1] / "knowledge" / "config" / "pedagogical_profiles.json"
)

_EXPECTED_VISIBLE_ROLES = frozenset([
    "mentor_fundamentos",
    "entrenador_sensorial",
    "investigador_causalidad",
    "revisor_respuestas",
    "entrenador_distinction",
])

_ALLOWED_TUTOR_MODES = frozenset([
    "mentor", "trainer", "reviewer", "distinction", "exam_pressure"
])

_REQUIRED_CHARACTER_FIELDS = (
    "id", "display_name", "role_label", "short_description",
    "allowed_modes", "default_mode", "strategy_profile_id",
    "visual_direction", "governance_notes",
)

# Real critic names used for governance checks
_KNOWN_REAL_CRITIC_NAMES = frozenset([
    "jancis", "robinson", "parker", "robert", "oz", "clarke", "steven",
    "spurrier", "halliday", "james", "macneil", "johnson", "yarrow",
    "laube", "suckling", "galloni", "tanzer", "broadbent", "serena",
    "sutcliffe", "matt", "kramer", "asimov", "antonio", "peñín", "penin",
    "atkin", "martin", "puckette", "mack",
])


def _load_characters_config() -> dict:
    with _CHARACTERS_CONFIG_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def _load_profiles_config() -> dict:
    with _PROFILES_CONFIG_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def _all_characters() -> list[dict]:
    return _load_characters_config().get("characters", [])


# ---------------------------------------------------------------------------
# Test 1: All 5 visible tutor roles have a character entry
# ---------------------------------------------------------------------------

class TestAllRolesHaveCharacter(unittest.TestCase):
    """Test 1 — all 5 visible tutor roles have a character."""

    def test_all_roles_have_character(self):
        """All 5 expected visible tutor roles must have exactly one character."""
        chars = list_characters()
        profile_ids = {c["strategy_profile_id"] for c in chars}
        for role in _EXPECTED_VISIBLE_ROLES:
            self.assertIn(
                role, profile_ids,
                msg=f"Missing character for visible role '{role}'."
            )

    def test_exactly_five_characters(self):
        self.assertEqual(len(list_characters()), 5)

    def test_no_duplicate_strategy_profile_ids(self):
        chars = list_characters()
        profile_ids = [c["strategy_profile_id"] for c in chars]
        self.assertEqual(len(profile_ids), len(set(profile_ids)))


# ---------------------------------------------------------------------------
# Test 2: No display_name matches known real wine critic names
# ---------------------------------------------------------------------------

class TestNoRealCriticNamesInDisplayName(unittest.TestCase):
    """Test 2 — display_name must not match known real wine critic names."""

    def test_no_display_name_matches_real_critics(self):
        """No display_name may match or closely resemble known real wine critics."""
        for char in _all_characters():
            name_lower = char["display_name"].lower()
            for critic in _KNOWN_REAL_CRITIC_NAMES:
                self.assertNotIn(
                    critic.lower(), name_lower,
                    msg=f"Character '{char['id']}' display_name '{char['display_name']}' "
                        f"contains real critic name '{critic}'."
                )


# ---------------------------------------------------------------------------
# Test 3: No short_description mentions real persons
# ---------------------------------------------------------------------------

class TestNoRealPersonsInDescriptions(unittest.TestCase):
    """Test 3 — short_description must not mention real persons."""

    def test_no_description_mentions_real_persons(self):
        for char in _all_characters():
            desc_lower = char.get("short_description", "").lower()
            for name in _KNOWN_REAL_CRITIC_NAMES:
                self.assertNotIn(
                    name.lower(), desc_lower,
                    msg=f"Character '{char['id']}' short_description mentions "
                        f"real person '{name}'."
                )


# ---------------------------------------------------------------------------
# Test 4: No description claims official WSET examiner authority
# ---------------------------------------------------------------------------

class TestNoExaminerAuthorityInDescriptions(unittest.TestCase):
    """Test 4 — no description may claim WSET examiner authority."""

    _AUTHORITY_PHRASES = (
        "wset examiner", "official examiner", "official score", "official mark",
        "official grade", "certified examiner", "wset certified",
        "examination authority", "examiner authority", "official wset",
    )

    def test_no_examiner_authority_in_descriptions(self):
        for char in _all_characters():
            for field in ("short_description", "role_label", "display_name"):
                text_lower = char.get(field, "").lower()
                for phrase in self._AUTHORITY_PHRASES:
                    self.assertNotIn(
                        phrase, text_lower,
                        msg=f"Character '{char['id']}' field '{field}' contains "
                            f"authority phrase '{phrase}'."
                    )


# ---------------------------------------------------------------------------
# Test 5: All required fields present
# ---------------------------------------------------------------------------

class TestAllRequiredFieldsPresent(unittest.TestCase):
    """Test 5 — each character has all 8 required fields."""

    def test_all_required_fields_present(self):
        for char in _all_characters():
            char_id = char.get("id", "<unknown>")
            for field in _REQUIRED_CHARACTER_FIELDS:
                self.assertIn(
                    field, char,
                    msg=f"Character '{char_id}' is missing required field '{field}'."
                )


# ---------------------------------------------------------------------------
# Test 6: allowed_modes are valid tutor modes
# ---------------------------------------------------------------------------

class TestAllowedModesAreValid(unittest.TestCase):
    """Test 6 — all allowed_modes must be in the valid tutor modes set."""

    def test_allowed_modes_are_valid(self):
        for char in _all_characters():
            char_id = char.get("id", "<unknown>")
            for mode in char.get("allowed_modes", []):
                self.assertIn(
                    mode, _ALLOWED_TUTOR_MODES,
                    msg=f"Character '{char_id}' has invalid allowed_mode: '{mode}'."
                )

    def test_allowed_modes_is_nonempty_list(self):
        for char in _all_characters():
            modes = char.get("allowed_modes", [])
            self.assertIsInstance(modes, list)
            self.assertGreater(len(modes), 0,
                               msg=f"Character '{char['id']}' allowed_modes is empty.")


# ---------------------------------------------------------------------------
# Test 7: default_mode is in allowed_modes
# ---------------------------------------------------------------------------

class TestDefaultModeInAllowedModes(unittest.TestCase):
    """Test 7 — default_mode must be in allowed_modes for each character."""

    def test_default_mode_in_allowed_modes(self):
        for char in _all_characters():
            char_id = char.get("id", "<unknown>")
            default = char.get("default_mode")
            allowed = char.get("allowed_modes", [])
            self.assertIn(
                default, allowed,
                msg=f"Character '{char_id}' default_mode '{default}' "
                    f"is not in allowed_modes {allowed}."
            )

    def test_default_mode_is_valid_tutor_mode(self):
        for char in _all_characters():
            self.assertIn(
                char.get("default_mode"), _ALLOWED_TUTOR_MODES,
                msg=f"Character '{char['id']}' default_mode is not a valid tutor mode."
            )


# ---------------------------------------------------------------------------
# Test 8: strategy_profile_id maps to existing profile
# ---------------------------------------------------------------------------

class TestStrategyProfileIdExists(unittest.TestCase):
    """Test 8 — each strategy_profile_id maps to an existing visible_role profile."""

    def test_strategy_profile_id_exists(self):
        profiles = _load_profiles_config()
        visible_roles = set(profiles.get("visible_roles", {}).keys())
        for char in _all_characters():
            profile_id = char.get("strategy_profile_id")
            self.assertIn(
                profile_id, visible_roles,
                msg=f"Character '{char['id']}' strategy_profile_id '{profile_id}' "
                    f"does not exist in pedagogical_profiles.json visible_roles."
            )


# ---------------------------------------------------------------------------
# Test 9: No character can activate examiner scoring
# ---------------------------------------------------------------------------

class TestNoExaminerScoringActivation(unittest.TestCase):
    """Test 9 — no character config sets examiner_scoring_allowed=True."""

    def test_no_character_can_activate_examiner_scoring(self):
        for char in _all_characters():
            gov = char.get("governance", {})
            self.assertFalse(
                gov.get("examiner_scoring_allowed", False),
                msg=f"Character '{char['id']}' must not set examiner_scoring_allowed=True."
            )

    def test_no_character_sets_safe_for_examiner(self):
        for char in _all_characters():
            gov = char.get("governance", {})
            self.assertFalse(
                gov.get("safe_for_examiner", False),
                msg=f"Character '{char['id']}' must not set safe_for_examiner=True."
            )


# ---------------------------------------------------------------------------
# Test 10: character_resolver returns fallback for unknown role
# ---------------------------------------------------------------------------

class TestCharacterResolverFallback(unittest.TestCase):
    """Test 10 — unknown role returns mentor_fundamentos fallback."""

    def test_character_resolver_returns_fallback_for_unknown_role(self):
        result = get_character("nonexistent_role_xyz")
        self.assertIsInstance(result, dict)
        self.assertNotEqual(result, {})
        # Fallback must be the mentor_fundamentos character
        self.assertEqual(result.get("strategy_profile_id"), _FALLBACK_ROLE)

    def test_character_resolver_never_raises_for_unknown(self):
        try:
            result = get_character("unknown_role_that_does_not_exist")
            self.assertIsInstance(result, dict)
        except Exception as e:
            self.fail(f"get_character raised unexpectedly: {e}")

    def test_character_resolver_returns_correct_character_for_known_role(self):
        result = get_character("revisor_respuestas")
        self.assertEqual(result.get("strategy_profile_id"), "revisor_respuestas")

    def test_list_characters_returns_all_five(self):
        chars = list_characters()
        self.assertEqual(len(chars), 5)

    def test_list_characters_returns_list_of_dicts(self):
        chars = list_characters()
        self.assertIsInstance(chars, list)
        for c in chars:
            self.assertIsInstance(c, dict)


# ---------------------------------------------------------------------------
# Test 11: validate_character() returns errors for real critic name
# ---------------------------------------------------------------------------

class TestCharacterResolverValidation(unittest.TestCase):
    """Test 11 — validate_character() catches governance violations."""

    def test_character_resolver_validates_governance_real_name(self):
        """validate_character must return errors for a display_name with a real critic."""
        bad_char = {
            "id": "bad_test_char",
            "display_name": "Jancis the Tutor",
            "role_label": "Tutora",
            "short_description": "A fictional tutor.",
            "allowed_modes": ["mentor"],
            "default_mode": "mentor",
            "strategy_profile_id": "mentor_fundamentos",
            "visual_direction": "Warm, illustrated.",
            "governance_notes": "Fictional original character. No real person.",
            "governance": {
                "safe_for_examiner": False,
                "examiner_scoring_allowed": False,
            }
        }
        errors = validate_character(bad_char)
        self.assertGreater(len(errors), 0,
                           msg="Expected validation errors for real critic name, got none.")

    def test_validate_character_clean_for_valid_characters(self):
        """All actual characters in the config should pass validation."""
        for char in _all_characters():
            errors = validate_character(char)
            self.assertEqual(
                errors, [],
                msg=f"Character '{char['id']}' failed validation: {errors}"
            )

    def test_validate_character_catches_missing_governance_notes(self):
        bad_char = {
            "id": "bad_no_notes",
            "display_name": "Fictional Tutor",
            "role_label": "Tutora",
            "short_description": "A tutor.",
            "allowed_modes": ["mentor"],
            "default_mode": "mentor",
            "strategy_profile_id": "mentor_fundamentos",
            "visual_direction": "Warm.",
            "governance_notes": "",  # empty — should fail
            "governance": {
                "safe_for_examiner": False,
                "examiner_scoring_allowed": False,
            }
        }
        errors = validate_character(bad_char)
        self.assertGreater(len(errors), 0)

    def test_validate_character_catches_examiner_scoring_true(self):
        bad_char = {
            "id": "bad_scoring",
            "display_name": "Fictional Tutor",
            "role_label": "Tutora",
            "short_description": "A tutor.",
            "allowed_modes": ["mentor"],
            "default_mode": "mentor",
            "strategy_profile_id": "mentor_fundamentos",
            "visual_direction": "Warm.",
            "governance_notes": "Fictional original character.",
            "governance": {
                "safe_for_examiner": False,
                "examiner_scoring_allowed": True,  # violation
            }
        }
        errors = validate_character(bad_char)
        self.assertGreater(len(errors), 0)

    def test_validate_character_returns_list(self):
        char = _all_characters()[0]
        result = validate_character(char)
        self.assertIsInstance(result, list)


# ---------------------------------------------------------------------------
# Test 12: avatar_stub is_avatar_implemented() always returns False
# ---------------------------------------------------------------------------

class TestAvatarStubNotImplemented(unittest.TestCase):
    """Test 12 — is_avatar_implemented() always returns False."""

    def test_avatar_stub_always_returns_not_implemented(self):
        for char in _all_characters():
            result = is_avatar_implemented(char["id"])
            self.assertFalse(
                result,
                msg=f"is_avatar_implemented('{char['id']}') returned True unexpectedly."
            )

    def test_avatar_stub_unknown_id_returns_false(self):
        self.assertFalse(is_avatar_implemented("nonexistent_avatar_xyz"))

    def test_avatar_stub_empty_string_returns_false(self):
        self.assertFalse(is_avatar_implemented(""))

    def test_avatar_stub_status_field_is_not_implemented(self):
        stub = get_avatar_stub("clara_mapas")
        self.assertEqual(stub.status, "not_implemented")


# ---------------------------------------------------------------------------
# Test 13: avatar_stub get_avatar_stub() never raises
# ---------------------------------------------------------------------------

class TestAvatarStubNeverRaises(unittest.TestCase):
    """Test 13 — get_avatar_stub() never raises for any input."""

    def test_avatar_stub_never_raises_for_known_id(self):
        for char in _all_characters():
            try:
                stub = get_avatar_stub(char["id"])
                self.assertIsInstance(stub, AvatarStub)
            except Exception as e:
                self.fail(f"get_avatar_stub('{char['id']}') raised: {e}")

    def test_avatar_stub_never_raises_for_unknown_id(self):
        try:
            stub = get_avatar_stub("completely_unknown_id")
            self.assertIsInstance(stub, AvatarStub)
        except Exception as e:
            self.fail(f"get_avatar_stub('completely_unknown_id') raised: {e}")

    def test_avatar_stub_never_raises_for_empty_string(self):
        try:
            stub = get_avatar_stub("")
            self.assertIsInstance(stub, AvatarStub)
        except Exception as e:
            self.fail(f"get_avatar_stub('') raised: {e}")

    def test_avatar_stub_never_raises_for_none_like_input(self):
        try:
            stub = get_avatar_stub("None")
            self.assertIsInstance(stub, AvatarStub)
        except Exception as e:
            self.fail(f"get_avatar_stub('None') raised: {e}")

    def test_avatar_stub_character_id_is_string(self):
        stub = get_avatar_stub("test_id")
        self.assertIsInstance(stub.character_id, str)

    def test_avatar_stub_resolve_role_returns_none_for_empty_interface(self):
        # AVATAR_INTERFACE is empty at stub phase
        result = resolve_avatar_to_role("any_avatar_id")
        self.assertIsNone(result)


# ---------------------------------------------------------------------------
# Test 14: governance_notes present and non-empty on all characters
# ---------------------------------------------------------------------------

class TestGovernanceNotesPresent(unittest.TestCase):
    """Test 14 — governance_notes field exists and is non-empty for all characters."""

    def test_governance_notes_present_on_all_characters(self):
        for char in _all_characters():
            notes = char.get("governance_notes")
            self.assertIsNotNone(
                notes,
                msg=f"Character '{char['id']}' is missing governance_notes field."
            )
            self.assertTrue(
                str(notes).strip(),
                msg=f"Character '{char['id']}' has empty governance_notes."
            )

    def test_governance_notes_mentions_fictional(self):
        for char in _all_characters():
            notes = char.get("governance_notes", "").lower()
            self.assertIn(
                "fictional", notes,
                msg=f"Character '{char['id']}' governance_notes must confirm fictional nature."
            )

    def test_governance_notes_is_string(self):
        for char in _all_characters():
            self.assertIsInstance(
                char.get("governance_notes"), str,
                msg=f"Character '{char['id']}' governance_notes must be a string."
            )


if __name__ == "__main__":
    unittest.main()

"""Visible tutor character resolver.

Loads and validates the visible_tutor_characters.json contract.
Returns character configs by visible tutor role. Never raises for unknown
roles — falls back to mentor_fundamentos safely.

Governance invariants
---------------------
  safe_for_examiner = False
  examiner_scoring_allowed = False
  No real person names in display_name or short_description.
  No examiner authority claims in any public field.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

_CHARACTERS_CONFIG_PATH = (
    Path(__file__).parents[3] / "knowledge" / "config" / "visible_tutor_characters.json"
)

_FALLBACK_ROLE = "mentor_fundamentos"

# Names that must not appear in runtime-visible fields.
_FORBIDDEN_REAL_NAMES: frozenset = frozenset([
    "jancis", "robinson", "parker", "robert", "oz", "clarke", "steven",
    "spurrier", "halliday", "james", "allen", "meadows", "laube", "suckling",
    "galloni", "tanzer", "broadbent", "serena", "sutcliffe", "matt", "kramer",
    "asimov", "antonio", "peñín", "penin", "macneil", "johnson", "yarrow",
    "atkin", "martin", "puckette", "mack",
])

_AUTHORITY_PHRASES: tuple = (
    "wset examiner", "official examiner", "official score", "official mark",
    "official grade", "official evaluation", "official wset", "certified examiner",
    "wset certified", "examination authority", "examiner authority",
)


@lru_cache(maxsize=1)
def _load_characters() -> dict:
    """Load and cache the visible_tutor_characters.json config."""
    if not _CHARACTERS_CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"visible_tutor_characters.json not found at {_CHARACTERS_CONFIG_PATH}."
        )
    return json.loads(_CHARACTERS_CONFIG_PATH.read_text(encoding="utf-8"))


def _all_character_list() -> list[dict]:
    config = _load_characters()
    return config.get("characters", [])


def _character_by_role() -> dict[str, dict]:
    """Return a mapping from strategy_profile_id → character dict."""
    return {c["strategy_profile_id"]: c for c in _all_character_list()}


def get_character(tutor_role: str) -> dict:
    """Return the character config for a given visible tutor role.

    Falls back to mentor_fundamentos for unknown roles. Never raises.
    """
    by_role = _character_by_role()
    if tutor_role in by_role:
        return by_role[tutor_role]
    # Fallback
    fallback = by_role.get(_FALLBACK_ROLE)
    if fallback is not None:
        return fallback
    # Last resort: return first character if fallback role is somehow absent
    chars = _all_character_list()
    return chars[0] if chars else {}


def list_characters() -> list[dict]:
    """Return all character configs."""
    return list(_all_character_list())


def validate_character(character: dict) -> list[str]:
    """Validate a single character dict against governance rules.

    Returns a list of error strings. Empty list means valid.
    """
    errors: list[str] = []

    char_id = character.get("id", "<unknown>")

    # Required fields
    required = (
        "id", "display_name", "role_label", "short_description",
        "allowed_modes", "default_mode", "strategy_profile_id",
        "visual_direction", "governance_notes",
    )
    for field in required:
        if field not in character:
            errors.append(f"[{char_id}] Missing required field: '{field}'")

    # Check for real person names in display_name and short_description
    for field in ("display_name", "short_description", "role_label"):
        text = character.get(field, "").lower()
        for name in _FORBIDDEN_REAL_NAMES:
            if re.search(r'\b' + re.escape(name) + r'\b', text):
                errors.append(
                    f"[{char_id}] Real person name '{name}' found in field '{field}'."
                )

    # Check for examiner authority claims in description fields
    for field in ("short_description", "role_label", "display_name"):
        text = character.get(field, "").lower()
        for phrase in _AUTHORITY_PHRASES:
            if phrase in text:
                errors.append(
                    f"[{char_id}] Authority phrase '{phrase}' found in field '{field}'."
                )

    # Governance flags must not be True
    gov = character.get("governance", {})
    if gov.get("safe_for_examiner") is True:
        errors.append(f"[{char_id}] safe_for_examiner must not be True.")
    if gov.get("examiner_scoring_allowed") is True:
        errors.append(f"[{char_id}] examiner_scoring_allowed must not be True.")

    # governance_notes must be present and non-empty
    notes = character.get("governance_notes", "")
    if not notes.strip():
        errors.append(f"[{char_id}] governance_notes must be non-empty.")

    return errors

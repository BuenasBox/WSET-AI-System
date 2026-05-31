"""Pedagogical profile loader and validator."""

from __future__ import annotations
import json
from functools import lru_cache
from pathlib import Path
from typing import Any
from tools.constants import KNOWLEDGE_DIR

_PROFILES_CONFIG_PATH = KNOWLEDGE_DIR / "config" / "pedagogical_profiles.json"

WEIGHT_TOLERANCE: float = 1e-6

ALLOWED_FUNCTIONS: frozenset = frozenset(
    ["cartographer", "scientist", "host", "storyteller", "critic", "challenger"]
)
ALLOWED_TUTOR_MODES: frozenset = frozenset(
    ["mentor", "trainer", "reviewer", "distinction", "exam_pressure"]
)
ALLOWED_VISIBLE_ROLES: frozenset = frozenset([
    "mentor_fundamentos", "entrenador_sensorial", "investigador_causalidad",
    "revisor_respuestas", "entrenador_distinction",
])
_FORBIDDEN_TRUE_GOVERNANCE_KEYS = (
    "safe_for_examiner", "examiner_scoring_allowed",
    "uses_llm", "uses_api", "uses_embeddings", "uses_vector_db",
)


class ProfileValidationError(ValueError):
    """Raised when a pedagogical profile config fails validation."""


@lru_cache(maxsize=1)
def _load_profiles_config():
    if not _PROFILES_CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"pedagogical_profiles.json not found at {_PROFILES_CONFIG_PATH}."
        )
    config = json.loads(_PROFILES_CONFIG_PATH.read_text(encoding="utf-8"))
    validate_profile_config(config)
    return config


def validate_profile_config(config):
    """Validate a pedagogical profiles config dict. Raises ProfileValidationError."""
    _validate_top_level_structure(config)
    _validate_default_profile(config["default_profile"])
    for mode_id, mode_data in config.get("tutor_modes", {}).items():
        _validate_mode_entry(mode_id, mode_data)
    for role_id, role_data in config.get("visible_roles", {}).items():
        _validate_role_entry(role_id, role_data)


def get_profile(tutor_role=None, tutor_mode=None):
    """Return a profile dict with normalised function weights.

    Resolution order: visible_role -> tutor_mode -> default.
    Never raises for unknown identifiers — always returns valid profile.
    """
    config = _load_profiles_config()
    if tutor_role and tutor_role in config.get("visible_roles", {}):
        role_data = config["visible_roles"][tutor_role]
        return {
            "profile_id": tutor_role,
            "functions": _extract_weights(role_data["functions"]),
            "source": "visible_role",
            "governance": _clean_governance(),
        }
    if tutor_mode and tutor_mode in config.get("tutor_modes", {}):
        mode_data = config["tutor_modes"][tutor_mode]
        return {
            "profile_id": tutor_mode,
            "functions": _extract_weights(mode_data["functions"]),
            "source": "tutor_mode",
            "governance": _clean_governance(),
        }
    default = config["default_profile"]
    return {
        "profile_id": "default",
        "functions": _extract_weights(default["functions"]),
        "source": "default",
        "governance": _clean_governance(),
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _extract_weights(functions_block):
    weights = {}
    for fn_id, fn_data in functions_block.items():
        if isinstance(fn_data, dict):
            weights[fn_id] = float(fn_data.get("weight", 0.0))
        else:
            weights[fn_id] = float(fn_data)
    return _normalise_weights(weights)


def _normalise_weights(weights):
    total = sum(weights.values())
    if total <= 0:
        n = len(weights)
        return {k: round(1.0 / n, 6) for k in weights}
    return {k: round(v / total, 6) for k, v in weights.items()}


def _clean_governance():
    return {
        "safe_for_examiner": False, "examiner_scoring_allowed": False,
        "uses_llm": False, "uses_api": False,
        "uses_embeddings": False, "uses_vector_db": False,
    }


def _validate_weight_sum(functions_block, context):
    weights = _extract_weights(functions_block)
    total = sum(weights.values())
    if abs(total - 1.0) > WEIGHT_TOLERANCE + 1e-5:
        raise ProfileValidationError(
            f"Weights in '{context}' sum to {total:.6f}, expected 1.0."
        )


def _validate_function_keys(functions_block, context):
    unknown = set(functions_block.keys()) - ALLOWED_FUNCTIONS
    if unknown:
        raise ProfileValidationError(
            f"Unknown function(s) in '{context}': {sorted(unknown)}. "
            f"Allowed: {sorted(ALLOWED_FUNCTIONS)}."
        )
    missing = ALLOWED_FUNCTIONS - set(functions_block.keys())
    if missing:
        raise ProfileValidationError(
            f"Missing function(s) in '{context}': {sorted(missing)}."
        )


def _validate_governance_block(governance, context):
    for key in _FORBIDDEN_TRUE_GOVERNANCE_KEYS:
        if governance.get(key) is True:
            raise ProfileValidationError(
                f"Governance violation in '{context}': '{key}' must not be True."
            )


def _validate_profile_block(block, context):
    functions_block = block.get("functions")
    if not isinstance(functions_block, dict):
        raise ProfileValidationError(f"'{context}' must have a 'functions' dict.")
    _validate_function_keys(functions_block, context)
    _validate_weight_sum(functions_block, context)
    governance = block.get("governance", {})
    if isinstance(governance, dict):
        _validate_governance_block(governance, context)


def _validate_top_level_structure(config):
    for key in ("allowed_functions", "allowed_tutor_modes", "allowed_visible_roles",
                "default_profile", "tutor_modes", "visible_roles"):
        if key not in config:
            raise ProfileValidationError(f"Missing required key: '{key}'.")
    meta_governance = config.get("_meta", {}).get("governance", {})
    if isinstance(meta_governance, dict):
        _validate_governance_block(meta_governance, "_meta.governance")


def _validate_default_profile(default):
    _validate_profile_block(default, "default_profile")
    weights = _extract_weights(default["functions"])
    if weights.get("host", 0.0) < 0.25 - WEIGHT_TOLERANCE:
        raise ProfileValidationError(
            f"default_profile host weight {weights['host']:.3f} < 0.25. "
            "Fallback must be supportive."
        )
    if weights.get("challenger", 0.0) > 0.10 + WEIGHT_TOLERANCE:
        raise ProfileValidationError(
            f"default_profile challenger weight {weights['challenger']:.3f} > 0.10. "
            "Fallback must not be severe."
        )


def _validate_mode_entry(mode_id, mode_data):
    if mode_id not in ALLOWED_TUTOR_MODES:
        raise ProfileValidationError(f"Unknown tutor_mode '{mode_id}'.")
    _validate_profile_block(mode_data, f"tutor_modes.{mode_id}")


def _validate_role_entry(role_id, role_data):
    if role_id not in ALLOWED_VISIBLE_ROLES:
        raise ProfileValidationError(f"Unknown visible_role '{role_id}'.")
    _validate_profile_block(role_data, f"visible_roles.{role_id}")
    mode_ref = role_data.get("tutor_mode")
    if mode_ref and mode_ref not in ALLOWED_TUTOR_MODES:
        raise ProfileValidationError(
            f"visible_roles.{role_id}.tutor_mode '{mode_ref}' is not a valid tutor mode."
        )

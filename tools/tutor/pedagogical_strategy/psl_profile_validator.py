"""PSL profile config validator — returns structured errors list, never raises.

profiles.py raises ProfileValidationError on first failure.
This validator collects ALL errors and returns them as a list of dicts,
suitable for reporting, CI checks, and tests that need structured output.
Each error dict has keys: {"rule", "context", "message"}.

Governance invariants checked:
- All weight vectors sum to 1.0 (raw, before normalisation)
- No unknown function keys
- No unknown tutor_mode or visible_role keys
- default_profile exists and is balanced (no single function > 0.35)
- exam_pressure: examiner_scoring_allowed and safe_for_examiner not True
- distinction: host weight > 0; governance flags False
- visible roles: text contains no forbidden real names
- visible roles: text contains no positive examiner authority assertions

No LLM, no API, no embeddings, no vector DB. Pure deterministic rule checks.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.constants import KNOWLEDGE_DIR

_PROFILES_CONFIG_PATH = KNOWLEDGE_DIR / "config" / "pedagogical_profiles.json"

_ALLOWED_FUNCTIONS: frozenset = frozenset(
    ["cartographer", "scientist", "host", "storyteller", "critic", "challenger"]
)
_ALLOWED_TUTOR_MODES: frozenset = frozenset(
    ["mentor", "trainer", "reviewer", "distinction", "exam_pressure"]
)
_ALLOWED_VISIBLE_ROLES: frozenset = frozenset([
    "mentor_fundamentos", "entrenador_sensorial", "investigador_causalidad",
    "revisor_respuestas", "entrenador_distinction",
])

_FORBIDDEN_REAL_NAMES: frozenset = frozenset([
    "jancis", "robinson", "parker", "suckling", "penin",
    "macneil", "johnson", "clarke", "spurrier", "asimov", "puckette",
    "mack", "yarrow", "atkin", "martin", "lee",
])

# Only phrases that are unambiguous positive authority assertions.
# Negation forms ("never claims examiner authority") appear legitimately in
# governance disclaimers and are intentionally excluded from this list.
_EXAMINER_CLAIM_PHRASES: tuple = (
    "is an official examiner",
    "provides official wset grading",
    "provides official grading",
    "score your answer officially",
    "your official score",
    "official wset score",
    "official wset marks",
    "official band",
    "this is an official assessment",
    "i am a wset examiner",
    "acting as examiner",
)

_WEIGHT_TOLERANCE: float = 1e-4


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def load_and_validate(config_path=None):
    """Load pedagogical_profiles.json and return a list of error dicts.
    Returns an empty list if the config is valid."""
    path = config_path or _PROFILES_CONFIG_PATH
    try:
        config = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [_err("load", "file", f"Config file not found: {path}")]
    except json.JSONDecodeError as exc:
        return [_err("load", "file", f"Invalid JSON: {exc}")]
    return validate_config(config)


def validate_config(config):
    """Validate a pedagogical profiles config dict. Returns list of error dicts."""
    errors = []
    errors.extend(_check_top_level_keys(config))
    if errors:
        return errors

    errors.extend(_check_profile_block(config["default_profile"], "default_profile"))
    errors.extend(_check_fallback_balanced(config["default_profile"]))

    for mode_id, mode_data in config.get("tutor_modes", {}).items():
        errors.extend(_check_unknown_mode(mode_id))
        errors.extend(_check_profile_block(mode_data, f"tutor_modes.{mode_id}"))

    ep = config.get("tutor_modes", {}).get("exam_pressure", {})
    errors.extend(_check_exam_pressure_governance(ep))

    dist = config.get("tutor_modes", {}).get("distinction", {})
    errors.extend(_check_distinction_host(dist))
    errors.extend(_check_distinction_governance(dist))

    for role_id, role_data in config.get("visible_roles", {}).items():
        errors.extend(_check_unknown_role(role_id))
        errors.extend(_check_profile_block(role_data, f"visible_roles.{role_id}"))
        errors.extend(_check_no_real_names(role_data, f"visible_roles.{role_id}"))
        errors.extend(_check_no_examiner_claim(role_data, f"visible_roles.{role_id}"))

    return errors


# ---------------------------------------------------------------------------
# Rule checkers
# ---------------------------------------------------------------------------

def _check_top_level_keys(config):
    errors = []
    for key in ("allowed_functions", "allowed_tutor_modes", "allowed_visible_roles",
                "default_profile", "tutor_modes", "visible_roles"):
        if key not in config:
            errors.append(_err("structure", "top_level", f"Missing required key: '{key}'"))
    return errors


def _check_profile_block(block, context):
    errors = []
    functions_block = block.get("functions")
    if not isinstance(functions_block, dict):
        errors.append(_err("structure", context, "Missing or invalid 'functions' dict"))
        return errors
    errors.extend(_check_function_keys(functions_block, context))
    errors.extend(_check_weight_sum(functions_block, context))
    return errors


def _check_function_keys(functions_block, context):
    errors = []
    unknown = set(functions_block.keys()) - _ALLOWED_FUNCTIONS
    if unknown:
        errors.append(_err(
            "unknown_function", context,
            f"Unknown function(s): {sorted(unknown)}. Allowed: {sorted(_ALLOWED_FUNCTIONS)}"
        ))
    return errors


def _check_weight_sum(functions_block, context):
    """Check raw (unnormalized) weight sum must be 1.0 +/- tolerance."""
    errors = []
    raw = []
    for fn_data in functions_block.values():
        if isinstance(fn_data, dict):
            raw.append(float(fn_data.get("weight", 0.0)))
        else:
            raw.append(float(fn_data))
    total = sum(raw)
    if abs(total - 1.0) > _WEIGHT_TOLERANCE:
        errors.append(_err(
            "bad_weights", context,
            f"Weights sum to {total:.6f}, expected 1.0 (tolerance {_WEIGHT_TOLERANCE})"
        ))
    return errors


def _check_fallback_balanced(default_block):
    """No single function weight > 0.35 in the default_profile."""
    errors = []
    functions_block = default_block.get("functions")
    if not isinstance(functions_block, dict):
        return errors
    for fn, fn_data in functions_block.items():
        w = float(fn_data.get("weight", fn_data) if isinstance(fn_data, dict) else fn_data)
        if w > 0.35 + _WEIGHT_TOLERANCE:
            errors.append(_err(
                "fallback_unbalanced", "default_profile",
                f"Function '{fn}' weight {w:.3f} > 0.35 in fallback profile"
            ))
    return errors


def _check_unknown_mode(mode_id):
    if mode_id not in _ALLOWED_TUTOR_MODES:
        return [_err("unknown_mode", f"tutor_modes.{mode_id}",
                     f"Unknown tutor_mode '{mode_id}'")]
    return []


def _check_unknown_role(role_id):
    if role_id not in _ALLOWED_VISIBLE_ROLES:
        return [_err("unknown_role", f"visible_roles.{role_id}",
                     f"Unknown visible_role '{role_id}'")]
    return []


def _check_exam_pressure_governance(ep_block):
    errors = []
    gov = ep_block.get("governance", {})
    if gov.get("examiner_scoring_allowed") is True:
        errors.append(_err("exam_pressure_governance", "tutor_modes.exam_pressure",
                           "examiner_scoring_allowed must not be True"))
    if gov.get("safe_for_examiner") is True:
        errors.append(_err("exam_pressure_governance", "tutor_modes.exam_pressure",
                           "safe_for_examiner must not be True"))
    return errors


def _check_distinction_host(dist_block):
    errors = []
    fns = dist_block.get("functions")
    if not isinstance(fns, dict):
        return errors
    fn_data = fns.get("host")
    if fn_data is None:
        errors.append(_err("distinction_host_zero", "tutor_modes.distinction",
                           "distinction mode missing 'host' function"))
        return errors
    w = float(fn_data.get("weight", fn_data) if isinstance(fn_data, dict) else fn_data)
    if w <= 0.0:
        errors.append(_err("distinction_host_zero", "tutor_modes.distinction",
                           f"distinction mode host weight is {w:.3f} — must be > 0"))
    return errors


def _check_distinction_governance(dist_block):
    errors = []
    gov = dist_block.get("governance", {})
    for key in ("safe_for_examiner", "examiner_scoring_allowed"):
        if gov.get(key) is True:
            errors.append(_err("distinction_governance", "tutor_modes.distinction",
                               f"'{key}' must not be True in distinction mode"))
    return errors


def _check_no_real_names(role_data, context):
    errors = []
    combined = " ".join(_collect_text(role_data)).lower()
    for name in _FORBIDDEN_REAL_NAMES:
        if name in combined:
            errors.append(_err("real_name_in_role", context,
                               f"Forbidden real name '{name}' found in role text"))
    return errors


def _check_no_examiner_claim(role_data, context):
    errors = []
    combined = " ".join(_collect_text(role_data)).lower()
    for phrase in _EXAMINER_CLAIM_PHRASES:
        if phrase in combined:
            errors.append(_err("examiner_claim_in_role", context,
                               f"Examiner authority phrase '{phrase}' found in role text"))
    return errors


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _collect_text(data):
    texts = []
    if isinstance(data, str):
        texts.append(data)
    elif isinstance(data, dict):
        for v in data.values():
            texts.extend(_collect_text(v))
    elif isinstance(data, list):
        for item in data:
            texts.extend(_collect_text(item))
    return texts


def _err(rule, context, message):
    return {"rule": rule, "context": context, "message": message}

"""Minimal learner epistemic state helpers for local Tutor orchestration."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from tools.youtube_transcription.config import PROJECT_ROOT


NAZARETH_ROOT = PROJECT_ROOT / "knowledge" / "nazareth"
DEFAULT_LES_PATH = NAZARETH_ROOT / "epistemic_state.json"
DEFAULT_SESSION_STAGING_PATH = NAZARETH_ROOT / "session_staging.json"

DEFAULT_LES: dict[str, Any] = {
    "learner_id": "nazareth",
    "schema_version": "minimal_brain_v1",
    "current_level": "WSET_L3",
    "known_weak_areas": [],
    "recent_misconceptions": [],
    "session_count": 0,
    "governance": {
        "safe_for_examiner": False,
        "examiner_scoring_active": False,
        "embeddings_active": False,
        "vector_db_active": False,
        "cloud_services_active": False,
    },
}

DEFAULT_SESSION_STAGING: dict[str, Any] = {
    "schema_version": "minimal_brain_v1",
    "latest_session": None,
    "governance": {
        "safe_for_examiner": False,
        "examiner_scoring_active": False,
        "embeddings_active": False,
        "vector_db_active": False,
        "cloud_services_active": False,
    },
}


def ensure_learner_files(
    les_path: Path = DEFAULT_LES_PATH,
    staging_path: Path = DEFAULT_SESSION_STAGING_PATH,
) -> None:
    """Create minimal learner files when absent, preserving existing state."""
    if not les_path.exists():
        _write_json(les_path, DEFAULT_LES)
    if not staging_path.exists():
        _write_json(staging_path, DEFAULT_SESSION_STAGING)


def load_learner_state(path: Path = DEFAULT_LES_PATH) -> dict[str, Any]:
    """Load the learner epistemic state and normalize governance flags."""
    if not path.exists():
        return deepcopy(DEFAULT_LES)
    with path.open("r", encoding="utf-8") as file:
        state = json.load(file)
    if not isinstance(state, dict):
        raise ValueError(f"Learner epistemic state must be a JSON object: {path}")
    return _with_governance_defaults(state)


def build_les_context(state: dict[str, Any]) -> dict[str, Any]:
    """Return the small LES context used by Minimal Brain v1 decisions."""
    governance = _governance_false(state.get("governance", {}))
    return {
        "learner_id": state.get("learner_id", "nazareth"),
        "current_level": state.get("current_level", "WSET_L3"),
        "known_weak_areas": list(state.get("known_weak_areas", [])),
        "recent_misconceptions": list(state.get("recent_misconceptions", [])),
        "session_count": int(state.get("session_count", 0) or 0),
        "governance": governance,
    }


def write_session_staging(
    staging: dict[str, Any],
    path: Path = DEFAULT_SESSION_STAGING_PATH,
) -> Path:
    """Write the local session staging artifact."""
    staging = deepcopy(staging)
    staging["governance"] = _governance_false(staging.get("governance", {}))
    _write_json(path, staging)
    return path


def _with_governance_defaults(state: dict[str, Any]) -> dict[str, Any]:
    normalized = deepcopy(DEFAULT_LES)
    normalized.update(state)
    normalized["governance"] = _governance_false(state.get("governance", {}))
    return normalized


def _governance_false(existing: dict[str, Any]) -> dict[str, bool]:
    governance = {
        "safe_for_examiner": False,
        "examiner_scoring_active": False,
        "embeddings_active": False,
        "vector_db_active": False,
        "cloud_services_active": False,
    }
    for key in governance:
        governance[key] = False if key == "safe_for_examiner" else bool(existing.get(key, False))
    governance["examiner_scoring_active"] = False
    governance["embeddings_active"] = False
    governance["vector_db_active"] = False
    governance["cloud_services_active"] = False
    return governance


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=True)
        file.write("\n")

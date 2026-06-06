"""Traceable final resolution for the Master Bank review/inactive backlog."""

from __future__ import annotations

import copy
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tools.constants import PROJECT_ROOT


RESOLUTION_PATH = Path(
    "knowledge/question-bank/reviews/master_bank_review_inactive_resolution.json"
)


def load_resolution_payload(
    path: str | Path = RESOLUTION_PATH,
    root: str | Path = PROJECT_ROOT,
) -> dict[str, Any]:
    payload = json.loads((Path(root) / Path(path)).read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError("Master Bank resolution artifact must be an object")
    return dict(payload)


def load_resolution_index(
    path: str | Path = RESOLUTION_PATH,
    root: str | Path = PROJECT_ROOT,
) -> dict[str, dict[str, Any]]:
    payload = load_resolution_payload(path, root)
    records = payload.get("records")
    if not isinstance(records, list):
        raise ValueError("Master Bank resolution records must be a list")
    index: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, Mapping):
            raise ValueError("Every Master Bank resolution must be an object")
        source_id = str(record.get("source_question_id", "")).strip()
        if not source_id or source_id in index:
            raise ValueError("Resolution source_question_id values must be unique")
        index[source_id] = dict(record)
    return index


def apply_source_resolution(
    record: Mapping[str, Any],
    resolution: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Return a source record with only explicitly reviewed overrides applied."""
    resolved = copy.deepcopy(dict(record))
    if not resolution:
        return resolved
    overrides = resolution.get("source_overrides")
    if not isinstance(overrides, Mapping):
        return resolved
    for field, value in overrides.items():
        if value is None:
            resolved.pop(str(field), None)
        else:
            resolved[str(field)] = copy.deepcopy(value)
    return resolved


def resolution_destination(resolution: Mapping[str, Any] | None) -> str:
    if not resolution:
        return ""
    return str(resolution.get("destination", "")).strip()

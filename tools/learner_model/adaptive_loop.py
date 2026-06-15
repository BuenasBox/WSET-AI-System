"""Deterministic coordinator for the formative event -> next session loop."""

from __future__ import annotations

import copy
import json
import os
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Callable

from tools.learner_model.knowledge_tracing import normalize_pedagogical_memory
from tools.learner_model.learning_event_runtime import process_question_attempt
from tools.orchestrator.learner_state import normalize_learner_state
from tools.question_generation.full_master_bank_session_composer import (
    compose_adaptive_master_bank_session,
)
from tools.question_generation.master_bank import SAFE_GOVERNANCE


ReplaceFunction = Callable[[str | bytes | os.PathLike[str] | os.PathLike[bytes],
                            str | bytes | os.PathLike[str] | os.PathLike[bytes]], None]


def run_adaptive_learning_loop(
    *,
    attempt: Mapping[str, Any],
    item: Mapping[str, Any],
    memory: Mapping[str, Any],
    les: Mapping[str, Any],
    master_bank: Mapping[str, Any] | None = None,
    blueprint: Mapping[str, Any] | None = None,
    memory_path: str | Path | None = None,
    les_path: str | Path | None = None,
    replace_function: ReplaceFunction = os.replace,
) -> dict[str, Any]:
    """Process one attempt, persist both states, and compose the next session."""
    if (memory_path is None) != (les_path is None):
        raise ValueError("memory_path and les_path must be provided together")
    learning = process_question_attempt(
        attempt=attempt,
        item=item,
        memory=memory,
        les=les,
    )
    if memory_path is not None and les_path is not None:
        persist_learning_state_atomically(
            learning["cognitive_map"],
            learning["les"],
            memory_path=memory_path,
            les_path=les_path,
            updated_at=str(learning["formative_event"]["timestamp"]),
            replace_function=replace_function,
        )
    next_session = compose_adaptive_master_bank_session(
        learning["next_session_signals"],
        master_bank,
        learning["les"],
        blueprint=blueprint,
    )
    return {
        "schema_version": "adaptive_learning_loop_v1",
        "learning": learning,
        "next_session": next_session,
        "state_persisted": memory_path is not None,
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def persist_learning_state_atomically(
    memory: Mapping[str, Any],
    les: Mapping[str, Any],
    *,
    memory_path: str | Path,
    les_path: str | Path,
    updated_at: str,
    replace_function: ReplaceFunction = os.replace,
) -> tuple[Path, Path]:
    """Commit memory and LES as one rollback-safe filesystem transaction."""
    memory_target = Path(memory_path)
    les_target = Path(les_path)
    if memory_target.resolve() == les_target.resolve():
        raise ValueError("memory_path and les_path must be different")
    normalized_memory = normalize_pedagogical_memory(dict(memory))
    normalized_memory["updated_at"] = str(updated_at)
    normalized_les = normalize_learner_state(dict(les))
    payloads = (
        (memory_target, _json_bytes(normalized_memory)),
        (les_target, _json_bytes(normalized_les)),
    )
    temporary: dict[Path, Path] = {}
    backups: dict[Path, Path] = {}
    installed: set[Path] = set()
    try:
        for target, payload in payloads:
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary[target] = _write_temporary_file(target, payload)
        for target, _ in payloads:
            if target.exists():
                backup = _reserve_temporary_path(target, ".rollback")
                replace_function(target, backup)
                backups[target] = backup
        for target, _ in payloads:
            replace_function(temporary[target], target)
            installed.add(target)
        for backup in backups.values():
            backup.unlink(missing_ok=True)
        return memory_target, les_target
    except Exception:
        for target in installed:
            target.unlink(missing_ok=True)
        for target, backup in backups.items():
            if backup.exists():
                replace_function(backup, target)
        raise
    finally:
        for path in temporary.values():
            path.unlink(missing_ok=True)
        for path in backups.values():
            path.unlink(missing_ok=True)


def _json_bytes(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def _write_temporary_file(target: Path, payload: bytes) -> Path:
    descriptor, name = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=target.parent,
    )
    path = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        path.unlink(missing_ok=True)
        raise
    return path


def _reserve_temporary_path(target: Path, suffix: str) -> Path:
    descriptor, name = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=suffix,
        dir=target.parent,
    )
    os.close(descriptor)
    path = Path(name)
    path.unlink()
    return path

"""Minimal learner epistemic state helpers for local Tutor orchestration."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Literal, TypedDict

from tools.constants import (
    CLOUD_SERVICES_ACTIVE,
    EXAMINER_SCORING_ALLOWED,
    NAZARETH_DIR,
    SAFE_FOR_EXAMINER,
)
from tools.learner_model.knowledge_tracing import (
    DEFAULT_PEDAGOGICAL_MEMORY_PATH,
    build_memory_summary,
    ensure_pedagogical_memory,
    load_pedagogical_memory,
)


NAZARETH_ROOT = NAZARETH_DIR
DEFAULT_LES_PATH = NAZARETH_ROOT / "epistemic_state.json"
DEFAULT_SESSION_STAGING_PATH = NAZARETH_ROOT / "session_staging.json"
RA_IDS = ("RA1", "RA2", "RA3", "RA4", "RA5")
CONFIDENCE_LEVELS = ("not_recorded", "low", "medium", "high")
WEAKNESS_LEVELS = ("not_recorded", "observed", "persistent", "cleared")
RA_TRENDS = ("not_observed", "improving", "stable", "declining")
QUESTION_RESULTS = ("correct", "incorrect", "unanswered")
MAX_QUESTION_RECENT_HISTORY = 20
MAX_QUESTION_EXPOSURE_LOG = 500


class TopicSignal(TypedDict):
    topic: str
    exposure_count: int
    correct_count: int
    incorrect_count: int
    confidence_level: Literal["not_recorded", "low", "medium", "high"]
    weakness_level: Literal["not_recorded", "observed", "persistent", "cleared"]
    last_seen: str | None


class RAPerformance(TypedDict):
    correct_count: int
    incorrect_count: int


class RASignal(TypedDict):
    ra_id: Literal["RA1", "RA2", "RA3", "RA4", "RA5"]
    exposure_count: int
    performance: RAPerformance
    trend: Literal["not_observed", "improving", "stable", "declining"]
    last_seen: str | None


class MisconceptionSignal(TypedDict):
    misconception_id: str
    detection_count: int
    last_detected: str | None


class CausalChainSignal(TypedDict):
    causal_chain_id: str
    exposure_count: int
    demonstrated_count: int


class QuestionExposure(TypedDict):
    question_id: str
    timestamp: str
    mode: str
    result: Literal["correct", "incorrect", "unanswered"]


class QuestionExposureSignal(TypedDict):
    question_id: str
    exposure_count: int
    last_seen: str | None
    recent_history: list[QuestionExposure]

DEFAULT_LES: dict[str, Any] = {
    "learner_id": "nazareth",
    "schema_version": "minimal_brain_v2",
    "current_level": "WSET_L3",
    "known_weak_areas": [],
    "recent_misconceptions": [],
    "session_count": 0,
    "topic_signals": {},
    "RA_signals": {
        ra_id: {
            "ra_id": ra_id,
            "exposure_count": 0,
            "performance": {"correct_count": 0, "incorrect_count": 0},
            "trend": "not_observed",
            "last_seen": None,
        }
        for ra_id in RA_IDS
    },
    "misconception_signals": {},
    "causal_chain_signals": {},
    "question_exposure_log": [],
    "question_exposure_signals": {},
    "governance": {
        "safe_for_examiner": SAFE_FOR_EXAMINER,
        "examiner_scoring_allowed": EXAMINER_SCORING_ALLOWED,
        "examiner_scoring_active": False,
        "embeddings_active": False,
        "vector_db_active": False,
        "cloud_services_active": CLOUD_SERVICES_ACTIVE,
    },
}

DEFAULT_SESSION_STAGING: dict[str, Any] = {
    "schema_version": "minimal_brain_v2",
    "latest_session": None,
    "governance": {
        "safe_for_examiner": SAFE_FOR_EXAMINER,
        "examiner_scoring_allowed": EXAMINER_SCORING_ALLOWED,
        "examiner_scoring_active": False,
        "embeddings_active": False,
        "vector_db_active": False,
        "cloud_services_active": CLOUD_SERVICES_ACTIVE,
    },
}


def ensure_learner_files(
    les_path: Path = DEFAULT_LES_PATH,
    staging_path: Path = DEFAULT_SESSION_STAGING_PATH,
    memory_path: Path = DEFAULT_PEDAGOGICAL_MEMORY_PATH,
) -> None:
    """Create minimal learner files when absent, preserving existing state."""
    if not les_path.exists():
        _write_json(les_path, DEFAULT_LES)
    if not staging_path.exists():
        _write_json(staging_path, DEFAULT_SESSION_STAGING)
    ensure_pedagogical_memory(memory_path)


def load_learner_state(path: Path = DEFAULT_LES_PATH) -> dict[str, Any]:
    """Load the learner epistemic state and normalize additive LES contracts."""
    if not path.exists():
        return deepcopy(DEFAULT_LES)
    with path.open("r", encoding="utf-8") as file:
        state = json.load(file)
    if not isinstance(state, dict):
        raise ValueError(f"Learner epistemic state must be a JSON object: {path}")
    return _with_governance_defaults(state)


def write_learner_state(
    state: dict[str, Any],
    path: Path = DEFAULT_LES_PATH,
) -> Path:
    """Normalize and persist learner state without deriving adaptive decisions."""
    if not isinstance(state, dict):
        raise ValueError("Learner epistemic state must be a dictionary.")
    _write_json(path, _with_governance_defaults(state))
    return path


def normalize_learner_state(state: dict[str, Any]) -> dict[str, Any]:
    """Return the additive LES contract with governance pinned false."""
    if not isinstance(state, dict):
        raise ValueError("Learner epistemic state must be a dictionary.")
    return _with_governance_defaults(state)


def create_topic_signal(
    topic: str,
    *,
    exposure_count: int = 0,
    correct_count: int = 0,
    incorrect_count: int = 0,
    confidence_level: str = "not_recorded",
    weakness_level: str = "not_recorded",
    last_seen: str | None = None,
) -> TopicSignal:
    """Build one observable topic signal without calculating confidence."""
    topic_id = _required_text(topic, "topic")
    if confidence_level not in CONFIDENCE_LEVELS:
        raise ValueError(f"Unsupported confidence_level: {confidence_level}")
    if weakness_level not in WEAKNESS_LEVELS:
        raise ValueError(f"Unsupported weakness_level: {weakness_level}")
    return {
        "topic": topic_id,
        "exposure_count": _non_negative_int(exposure_count, "exposure_count"),
        "correct_count": _non_negative_int(correct_count, "correct_count"),
        "incorrect_count": _non_negative_int(incorrect_count, "incorrect_count"),
        "confidence_level": confidence_level,
        "weakness_level": weakness_level,
        "last_seen": _optional_text(last_seen, "last_seen"),
    }


def create_ra_signal(
    ra_id: str,
    *,
    exposure_count: int = 0,
    correct_count: int = 0,
    incorrect_count: int = 0,
    trend: str = "not_observed",
    last_seen: str | None = None,
) -> RASignal:
    """Build one RA1-RA5 observation record without computing trend."""
    normalized_ra_id = str(ra_id or "").strip().upper()
    if normalized_ra_id not in RA_IDS:
        raise ValueError(f"Unsupported ra_id: {ra_id}")
    if trend not in RA_TRENDS:
        raise ValueError(f"Unsupported RA trend: {trend}")
    return {
        "ra_id": normalized_ra_id,
        "exposure_count": _non_negative_int(exposure_count, "exposure_count"),
        "performance": {
            "correct_count": _non_negative_int(correct_count, "correct_count"),
            "incorrect_count": _non_negative_int(incorrect_count, "incorrect_count"),
        },
        "trend": trend,
        "last_seen": _optional_text(last_seen, "last_seen"),
    }


def create_misconception_signal(
    misconception_id: str,
    *,
    detection_count: int = 0,
    last_detected: str | None = None,
) -> MisconceptionSignal:
    """Build one persisted misconception observation."""
    normalized_id = _required_text(misconception_id, "misconception_id")
    return {
        "misconception_id": normalized_id,
        "detection_count": _non_negative_int(detection_count, "detection_count"),
        "last_detected": _optional_text(last_detected, "last_detected"),
    }


def create_causal_chain_signal(
    causal_chain_id: str,
    *,
    exposure_count: int = 0,
    demonstrated_count: int = 0,
) -> CausalChainSignal:
    """Build one persisted causal-chain observation."""
    normalized_id = _required_text(causal_chain_id, "causal_chain_id")
    return {
        "causal_chain_id": normalized_id,
        "exposure_count": _non_negative_int(exposure_count, "exposure_count"),
        "demonstrated_count": _non_negative_int(demonstrated_count, "demonstrated_count"),
    }


def create_question_exposure(
    question_id: str,
    *,
    timestamp: str,
    mode: str,
    result: str,
) -> QuestionExposure:
    """Build one question exposure entry; no selection behavior consumes it yet."""
    if result not in QUESTION_RESULTS:
        raise ValueError(f"Unsupported question result: {result}")
    return {
        "question_id": _required_text(question_id, "question_id"),
        "timestamp": _required_text(timestamp, "timestamp"),
        "mode": _required_text(mode, "mode"),
        "result": result,
    }


def append_question_exposure(
    state: dict[str, Any],
    exposure: QuestionExposure,
) -> dict[str, Any]:
    """Return a normalized copy with one validated exposure appended."""
    updated = _with_governance_defaults(state)
    entry = create_question_exposure(
        exposure.get("question_id", ""),
        timestamp=exposure.get("timestamp", ""),
        mode=exposure.get("mode", ""),
        result=exposure.get("result", ""),
    )
    updated["question_exposure_log"].append(entry)
    updated["question_exposure_log"] = updated["question_exposure_log"][
        -MAX_QUESTION_EXPOSURE_LOG:
    ]
    question_id = entry["question_id"]
    current = updated["question_exposure_signals"].get(question_id, {})
    history = list(current.get("recent_history", []))
    history.append(entry)
    updated["question_exposure_signals"][question_id] = create_question_exposure_signal(
        question_id,
        exposure_count=int(current.get("exposure_count", 0) or 0) + 1,
        last_seen=entry["timestamp"],
        recent_history=history[-MAX_QUESTION_RECENT_HISTORY:],
    )
    return updated


def create_question_exposure_signal(
    question_id: str,
    *,
    exposure_count: int = 0,
    last_seen: str | None = None,
    recent_history: list[QuestionExposure] | None = None,
) -> QuestionExposureSignal:
    """Build aggregate exposure state for one canonical question."""
    normalized_history = _normalize_question_exposure_log(recent_history or [])
    normalized_id = _required_text(question_id, "question_id")
    if any(entry["question_id"] != normalized_id for entry in normalized_history):
        raise ValueError("recent_history question_id values must match question_id.")
    return {
        "question_id": normalized_id,
        "exposure_count": _non_negative_int(exposure_count, "exposure_count"),
        "last_seen": _optional_text(last_seen, "last_seen"),
        "recent_history": normalized_history[-MAX_QUESTION_RECENT_HISTORY:],
    }


def record_session_observations(
    state: dict[str, Any],
    session: dict[str, Any],
    *,
    timestamp: str,
    results: dict[str, str] | None = None,
    topic_confidence: dict[str, str] | None = None,
    topic_weakness: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Capture session exposure, topic coverage, and RA indicators in LES."""
    updated = _with_governance_defaults(state)
    result_map = results if isinstance(results, dict) else {}
    confidence_map = topic_confidence if isinstance(topic_confidence, dict) else {}
    weakness_map = topic_weakness if isinstance(topic_weakness, dict) else {}
    mode = _required_text(session.get("mode", ""), "mode")
    items = session.get("items", [])
    if not isinstance(items, list):
        raise ValueError("session.items must be a list.")

    for item in items:
        if not isinstance(item, dict):
            continue
        question_id = _required_text(item.get("master_item_id", ""), "master_item_id")
        result = result_map.get(question_id, "unanswered")
        exposure = create_question_exposure(
            question_id,
            timestamp=timestamp,
            mode=mode,
            result=result,
        )
        updated = append_question_exposure(updated, exposure)
        curriculum = item.get("curriculum", {})
        if not isinstance(curriculum, dict):
            curriculum = {}
        topic = str(curriculum.get("topic") or "unknown").strip()
        ra_id = str(curriculum.get("ra") or "").strip().upper()
        updated["topic_signals"][topic] = _updated_topic_signal(
            updated["topic_signals"].get(topic),
            topic=topic,
            result=result,
            timestamp=timestamp,
            confidence_level=confidence_map.get(topic),
            weakness_level=weakness_map.get(topic),
        )
        if ra_id in RA_IDS:
            updated["RA_signals"][ra_id] = _updated_ra_signal(
                updated["RA_signals"].get(ra_id),
                ra_id=ra_id,
                result=result,
                timestamp=timestamp,
            )
    return updated


def build_les_context(state: dict[str, Any]) -> dict[str, Any]:
    """Return the small LES context used by Minimal Brain v1 decisions."""
    governance = _governance_false(state.get("governance", {}))
    memory_summary = build_memory_summary(load_pedagogical_memory())
    return {
        "learner_id": state.get("learner_id", "nazareth"),
        "current_level": state.get("current_level", "WSET_L3"),
        "known_weak_areas": list(state.get("known_weak_areas", [])),
        "recent_misconceptions": list(state.get("recent_misconceptions", [])),
        "session_count": int(state.get("session_count", 0) or 0),
        "pedagogical_memory": memory_summary,
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
    normalized["topic_signals"] = _normalize_signal_map(
        state.get("topic_signals"),
        create_topic_signal,
        "topic",
    )
    normalized["RA_signals"] = _normalize_ra_signals(state.get("RA_signals"))
    normalized["misconception_signals"] = _normalize_signal_map(
        state.get("misconception_signals"),
        create_misconception_signal,
        "misconception_id",
    )
    normalized["causal_chain_signals"] = _normalize_signal_map(
        state.get("causal_chain_signals"),
        create_causal_chain_signal,
        "causal_chain_id",
    )
    normalized["question_exposure_log"] = _normalize_question_exposure_log(
        state.get("question_exposure_log")
    )
    normalized["question_exposure_signals"] = _normalize_question_exposure_signals(
        state.get("question_exposure_signals")
    )
    normalized["governance"] = _governance_false(state.get("governance", {}))
    return normalized


def _governance_false(existing: dict[str, Any]) -> dict[str, bool]:
    if not isinstance(existing, dict):
        existing = {}
    governance = {
        "safe_for_examiner": SAFE_FOR_EXAMINER,
        "examiner_scoring_allowed": EXAMINER_SCORING_ALLOWED,
        "examiner_scoring_active": False,
        "embeddings_active": False,
        "vector_db_active": False,
        "cloud_services_active": CLOUD_SERVICES_ACTIVE,
    }
    for key in governance:
        governance[key] = bool(existing.get(key, False))
    governance["safe_for_examiner"] = False
    governance["examiner_scoring_allowed"] = False
    governance["examiner_scoring_active"] = False
    governance["embeddings_active"] = False
    governance["vector_db_active"] = False
    governance["cloud_services_active"] = False
    return governance


def _normalize_signal_map(
    value: Any,
    factory: Any,
    identity_field: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    normalized: dict[str, Any] = {}
    for key, signal in value.items():
        if not isinstance(signal, dict):
            continue
        identity = str(signal.get(identity_field) or key or "").strip()
        if not identity:
            continue
        try:
            kwargs = {field: field_value for field, field_value in signal.items() if field != identity_field}
            normalized[identity] = factory(identity, **kwargs)
        except (TypeError, ValueError):
            continue
    return normalized


def _normalize_ra_signals(value: Any) -> dict[str, RASignal]:
    source = value if isinstance(value, dict) else {}
    normalized: dict[str, RASignal] = {}
    for ra_id in RA_IDS:
        signal = source.get(ra_id, {})
        if not isinstance(signal, dict):
            signal = {}
        performance = signal.get("performance", {})
        if not isinstance(performance, dict):
            performance = {}
        try:
            normalized[ra_id] = create_ra_signal(
                ra_id,
                exposure_count=signal.get("exposure_count", 0),
                correct_count=performance.get("correct_count", 0),
                incorrect_count=performance.get("incorrect_count", 0),
                trend=signal.get("trend", "not_observed"),
                last_seen=signal.get("last_seen"),
            )
        except (TypeError, ValueError):
            normalized[ra_id] = create_ra_signal(ra_id)
    return normalized


def _normalize_question_exposure_log(value: Any) -> list[QuestionExposure]:
    if not isinstance(value, list):
        return []
    normalized: list[QuestionExposure] = []
    for entry in value:
        if not isinstance(entry, dict):
            continue
        try:
            normalized.append(
                create_question_exposure(
                    entry.get("question_id", ""),
                    timestamp=entry.get("timestamp", ""),
                    mode=entry.get("mode", ""),
                    result=entry.get("result", ""),
                )
            )
        except (TypeError, ValueError):
            continue
    return normalized[-MAX_QUESTION_EXPOSURE_LOG:]


def _normalize_question_exposure_signals(
    value: Any,
) -> dict[str, QuestionExposureSignal]:
    if not isinstance(value, dict):
        return {}
    normalized: dict[str, QuestionExposureSignal] = {}
    for key, signal in value.items():
        if not isinstance(signal, dict):
            continue
        question_id = str(signal.get("question_id") or key or "").strip()
        if not question_id:
            continue
        try:
            normalized[question_id] = create_question_exposure_signal(
                question_id,
                exposure_count=signal.get("exposure_count", 0),
                last_seen=signal.get("last_seen"),
                recent_history=signal.get("recent_history", []),
            )
        except (TypeError, ValueError):
            continue
    return normalized


def _updated_topic_signal(
    current: Any,
    *,
    topic: str,
    result: str,
    timestamp: str,
    confidence_level: str | None,
    weakness_level: str | None,
) -> TopicSignal:
    source = current if isinstance(current, dict) else {}
    return create_topic_signal(
        topic,
        exposure_count=int(source.get("exposure_count", 0) or 0) + 1,
        correct_count=int(source.get("correct_count", 0) or 0)
        + (1 if result == "correct" else 0),
        incorrect_count=int(source.get("incorrect_count", 0) or 0)
        + (1 if result == "incorrect" else 0),
        confidence_level=confidence_level or source.get(
            "confidence_level", "not_recorded"
        ),
        weakness_level=weakness_level or source.get(
            "weakness_level", "not_recorded"
        ),
        last_seen=timestamp,
    )


def _updated_ra_signal(
    current: Any,
    *,
    ra_id: str,
    result: str,
    timestamp: str,
) -> RASignal:
    source = current if isinstance(current, dict) else {}
    performance = source.get("performance", {})
    if not isinstance(performance, dict):
        performance = {}
    return create_ra_signal(
        ra_id,
        exposure_count=int(source.get("exposure_count", 0) or 0) + 1,
        correct_count=int(performance.get("correct_count", 0) or 0)
        + (1 if result == "correct" else 0),
        incorrect_count=int(performance.get("incorrect_count", 0) or 0)
        + (1 if result == "incorrect" else 0),
        trend=source.get("trend", "not_observed"),
        last_seen=timestamp,
    )


def _non_negative_int(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field} must be a non-negative integer.")
    return value


def _required_text(value: Any, field: str) -> str:
    normalized = str(value or "").strip()
    if not normalized:
        raise ValueError(f"{field} must be non-empty text.")
    return normalized


def _optional_text(value: Any, field: str) -> str | None:
    if value is None:
        return None
    return _required_text(value, field)


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=True)
        file.write("\n")

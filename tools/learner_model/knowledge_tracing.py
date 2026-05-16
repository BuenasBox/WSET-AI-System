"""Lightweight local knowledge tracing and pedagogical memory.

This is a deterministic Tutor-development model inspired by Bayesian Knowledge
Tracing. It does not grade, score, call APIs, use embeddings, or activate
Examiner behavior.
"""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tools.youtube_transcription.config import PROJECT_ROOT


DEFAULT_PEDAGOGICAL_MEMORY_PATH = PROJECT_ROOT / "knowledge" / "nazareth" / "pedagogical_memory.json"
MEMORY_SCHEMA_VERSION = "pedagogical_memory_v1"

DEFAULT_SKILL_STATE: dict[str, Any] = {
    "concept_id": "",
    "mastery_probability": 0.35,
    "attempts": 0,
    "successes": 0,
    "recent_failures": 0,
    "misconception_hits": 0,
    "last_seen": None,
    "confidence_trend": [],
}

DEFAULT_PEDAGOGICAL_MEMORY: dict[str, Any] = {
    "schema_version": MEMORY_SCHEMA_VERSION,
    "learner_id": "nazareth",
    "updated_at": None,
    "skills": {},
    "recurrent_misconceptions": {},
    "difficult_causal_chains": {},
    "mastered_concepts": [],
    "preferred_depth": "standard",
    "overload_patterns": [],
    "governance": {
        "safe_for_examiner": False,
        "examiner_scoring_allowed": False,
        "uses_llm": False,
        "uses_api": False,
        "uses_embeddings": False,
        "uses_vector_db": False,
        "cloud_services_active": False,
    },
}


def load_pedagogical_memory(path: Path = DEFAULT_PEDAGOGICAL_MEMORY_PATH) -> dict[str, Any]:
    """Load pedagogical memory, returning defaults if absent."""
    if not path.exists():
        return deepcopy(DEFAULT_PEDAGOGICAL_MEMORY)
    with path.open("r", encoding="utf-8") as file:
        memory = json.load(file)
    if not isinstance(memory, dict):
        raise ValueError(f"Pedagogical memory must be a JSON object: {path}")
    return normalize_pedagogical_memory(memory)


def save_pedagogical_memory(memory: dict[str, Any], path: Path = DEFAULT_PEDAGOGICAL_MEMORY_PATH) -> Path:
    """Persist local pedagogical memory with governance pinned false."""
    normalized = normalize_pedagogical_memory(memory)
    normalized["updated_at"] = datetime.now(timezone.utc).isoformat()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(normalized, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return path


def ensure_pedagogical_memory(path: Path = DEFAULT_PEDAGOGICAL_MEMORY_PATH) -> Path:
    """Create memory file if absent, preserving existing state."""
    if not path.exists():
        save_pedagogical_memory(DEFAULT_PEDAGOGICAL_MEMORY, path)
    return path


def normalize_pedagogical_memory(memory: dict[str, Any]) -> dict[str, Any]:
    """Normalize memory while preserving forward-compatible fields."""
    normalized = deepcopy(DEFAULT_PEDAGOGICAL_MEMORY)
    normalized.update(memory)
    normalized["schema_version"] = str(memory.get("schema_version") or MEMORY_SCHEMA_VERSION)
    normalized["skills"] = dict(memory.get("skills") or {})
    normalized["recurrent_misconceptions"] = dict(memory.get("recurrent_misconceptions") or {})
    normalized["difficult_causal_chains"] = dict(memory.get("difficult_causal_chains") or {})
    normalized["mastered_concepts"] = list(memory.get("mastered_concepts") or [])
    normalized["overload_patterns"] = list(memory.get("overload_patterns") or [])
    normalized["governance"] = _governance_false(memory.get("governance") or {})
    return normalized


def update_mastery(
    skill_state: dict[str, Any],
    success: bool,
    confidence: float | None = None,
    misconception_hit: bool = False,
    now: str | None = None,
) -> dict[str, Any]:
    """Update one concept using a small BKT-like mastery transition."""
    state = _normalize_skill_state(skill_state)
    mastery = float(state["mastery_probability"])
    confidence_factor = _clamp(confidence if confidence is not None else (0.75 if success else 0.35))
    learn_rate = 0.18 + confidence_factor * 0.08
    failure_penalty = 0.12 + (1 - confidence_factor) * 0.08
    if success:
        mastery = mastery + (1 - mastery) * learn_rate
        state["successes"] += 1
        state["recent_failures"] = max(0, int(state.get("recent_failures", 0)) - 1)
    else:
        mastery = mastery - mastery * failure_penalty
        state["recent_failures"] += 1
    if misconception_hit:
        mastery = mastery - mastery * 0.1
        state["misconception_hits"] += 1
    state["attempts"] += 1
    state["mastery_probability"] = round(_clamp(mastery), 3)
    state["last_seen"] = now or datetime.now(timezone.utc).isoformat()
    trend = list(state.get("confidence_trend") or [])
    trend.append(round(confidence_factor if success else -1 * (1 - confidence_factor), 3))
    state["confidence_trend"] = trend[-8:]
    return state


def decay_mastery(skill_state: dict[str, Any], days_since_seen: int = 1, decay_rate: float = 0.015) -> dict[str, Any]:
    """Apply forgetting decay without dropping below a cautious floor."""
    state = _normalize_skill_state(skill_state)
    days = max(0, int(days_since_seen or 0))
    retention = (1 - _clamp(decay_rate)) ** days
    floor = 0.05
    state["mastery_probability"] = round(max(floor, float(state["mastery_probability"]) * retention), 3)
    return state


def estimate_retention_risk(skill_state: dict[str, Any], days_since_seen: int = 0) -> float:
    """Estimate likelihood that the concept needs resurfacing."""
    state = _normalize_skill_state(skill_state)
    mastery_risk = 1 - float(state["mastery_probability"])
    failure_risk = min(0.35, int(state.get("recent_failures", 0)) * 0.1)
    misconception_risk = min(0.25, int(state.get("misconception_hits", 0)) * 0.05)
    time_risk = min(0.25, max(0, int(days_since_seen or 0)) * 0.01)
    return round(_clamp(mastery_risk * 0.55 + failure_risk + misconception_risk + time_risk), 3)


def estimate_learning_velocity(skill_state: dict[str, Any]) -> float:
    """Estimate recent learning direction from confidence trend and success rate."""
    state = _normalize_skill_state(skill_state)
    attempts = max(1, int(state.get("attempts", 0)))
    success_rate = int(state.get("successes", 0)) / attempts
    trend = [float(item) for item in state.get("confidence_trend", []) if isinstance(item, (int, float))]
    trend_signal = sum(trend[-4:]) / max(1, len(trend[-4:]))
    return round(_clamp(success_rate * 0.6 + ((trend_signal + 1) / 2) * 0.4), 3)


def update_memory_from_results(
    memory: dict[str, Any],
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    """Update persistent memory from self-eval result objects."""
    updated = normalize_pedagogical_memory(memory)
    for result in results:
        comparison = result.get("comparison") or {}
        labels = set(comparison.get("failure_labels") or [])
        success = not labels
        concept_ids = _concept_ids_from_result(result)
        misconception_hit = "misconception_unresolved" in labels or "misconception_reinforcement_risk" in labels
        confidence = _confidence_from_result(result, success)
        for concept_id in concept_ids:
            skill = dict(updated["skills"].get(concept_id) or {"concept_id": concept_id})
            updated["skills"][concept_id] = update_mastery(skill, success=success, confidence=confidence, misconception_hit=misconception_hit)
        for gap in comparison.get("likely_misconception_gaps", []) or []:
            entry = dict(updated["recurrent_misconceptions"].get(gap) or {"misconception_id": gap, "hits": 0})
            entry["hits"] = int(entry.get("hits", 0)) + 1
            entry["persistence"] = round(min(1.0, entry["hits"] / 5), 3)
            updated["recurrent_misconceptions"][gap] = entry
        for link in comparison.get("missing_causal_links", []) or []:
            entry = dict(updated["difficult_causal_chains"].get(link) or {"chain_id": link, "failures": 0})
            entry["failures"] = int(entry.get("failures", 0)) + 1
            entry["retention_risk"] = round(min(1.0, entry["failures"] / 4), 3)
            updated["difficult_causal_chains"][link] = entry
        if "weak_context_support" in labels or "shallow_reasoning" in labels:
            _append_unique(updated["overload_patterns"], "needs_more_scaffolded_context")
    updated["mastered_concepts"] = sorted(
        concept_id for concept_id, state in updated["skills"].items() if float(state.get("mastery_probability", 0)) >= 0.82
    )
    updated["preferred_depth"] = _preferred_depth(updated)
    updated["governance"] = _governance_false(updated.get("governance") or {})
    return updated


def build_memory_summary(memory: dict[str, Any]) -> dict[str, Any]:
    """Return a compact adapter summary for LES/context packages."""
    normalized = normalize_pedagogical_memory(memory)
    low_mastery = [
        {"concept_id": concept_id, "mastery_probability": state.get("mastery_probability", 0)}
        for concept_id, state in normalized["skills"].items()
        if float(state.get("mastery_probability", 0)) < 0.45
    ]
    retention_risks = [
        {"concept_id": concept_id, "retention_risk": estimate_retention_risk(state)}
        for concept_id, state in normalized["skills"].items()
        if estimate_retention_risk(state) >= 0.55
    ]
    return {
        "schema_version": normalized["schema_version"],
        "low_mastery_concepts": sorted(low_mastery, key=lambda row: row["mastery_probability"])[:5],
        "retention_risks": sorted(retention_risks, key=lambda row: row["retention_risk"], reverse=True)[:5],
        "recurrent_misconceptions": sorted(normalized["recurrent_misconceptions"].values(), key=lambda row: row.get("persistence", 0), reverse=True)[:5],
        "difficult_causal_chains": sorted(normalized["difficult_causal_chains"].values(), key=lambda row: row.get("retention_risk", 0), reverse=True)[:5],
        "mastered_concepts": normalized["mastered_concepts"][:10],
        "preferred_depth": normalized.get("preferred_depth", "standard"),
        "overload_patterns": normalized["overload_patterns"][:5],
        "governance": _governance_false(normalized.get("governance") or {}),
    }


def _normalize_skill_state(skill_state: dict[str, Any]) -> dict[str, Any]:
    state = deepcopy(DEFAULT_SKILL_STATE)
    state.update(skill_state or {})
    state["concept_id"] = str(state.get("concept_id") or "unknown_concept")
    state["mastery_probability"] = _clamp(float(state.get("mastery_probability", 0.35) or 0.35))
    state["attempts"] = int(state.get("attempts", 0) or 0)
    state["successes"] = int(state.get("successes", 0) or 0)
    state["recent_failures"] = int(state.get("recent_failures", 0) or 0)
    state["misconception_hits"] = int(state.get("misconception_hits", 0) or 0)
    state["confidence_trend"] = list(state.get("confidence_trend") or [])[-8:]
    return state


def _concept_ids_from_result(result: dict[str, Any]) -> list[str]:
    concepts = []
    for key in ("expected_topics", "expected_causal_links", "expected_keywords"):
        for value in result.get(key, []) or []:
            if value:
                concepts.append(str(value))
    if not concepts:
        concepts.append(str(result.get("question_id") or "unknown_concept"))
    return sorted(set(concepts))


def _confidence_from_result(result: dict[str, Any], success: bool) -> float:
    signals = result.get("tutor_evaluation_signals") or {}
    if signals.get("reasoning_depth_score") is not None:
        base = float(signals.get("reasoning_depth_score") or 0.5)
    else:
        base = 0.75 if success else 0.35
    return _clamp(base)


def _preferred_depth(memory: dict[str, Any]) -> str:
    high_persistence = any(float(item.get("persistence", 0)) >= 0.6 for item in memory["recurrent_misconceptions"].values())
    high_risk = any(float(item.get("retention_risk", 0)) >= 0.6 for item in memory["difficult_causal_chains"].values())
    if high_persistence or high_risk:
        return "deep"
    if len(memory["mastered_concepts"]) >= 5:
        return "minimal"
    return "standard"


def _append_unique(items: list[Any], value: Any) -> None:
    if value not in items:
        items.append(value)


def _governance_false(existing: dict[str, Any]) -> dict[str, bool]:
    return {
        "safe_for_examiner": False,
        "examiner_scoring_allowed": False,
        "uses_llm": False,
        "uses_api": False,
        "uses_embeddings": False,
        "uses_vector_db": False,
        "cloud_services_active": False,
    }


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))

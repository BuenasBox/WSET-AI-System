"""Deterministic question-attempt to cognitive-map learning event runtime.

This module updates the existing pedagogical memory and LES. It does not grade,
calculate percentages, produce pass/fail decisions, or activate examiner authority.
"""

from __future__ import annotations

import copy
import hashlib
from collections.abc import Mapping
from typing import Any

from tools.learner_model.causal_runtime import update_les_causal
from tools.learner_model.knowledge_tracing import (
    build_memory_summary,
    normalize_pedagogical_memory,
    update_mastery,
)
from tools.learner_model.misconception_runtime import process_sba_outcome
from tools.orchestrator.learner_state import (
    RA_IDS,
    record_session_observations,
)
from tools.question_generation.master_bank import SAFE_GOVERNANCE


ATTEMPT_SCHEMA_VERSION = "question_attempt_v1"
FORMATIVE_EVENT_SCHEMA_VERSION = "formative_learning_event_v1"
RUNTIME_VERSION = "cognitive_map_learning_event_runtime_v1"
CONFIDENCE_VALUES = {
    "low": 0.25,
    "medium": 0.6,
    "high": 0.85,
    "not_reported": None,
}
LEARNING_STAGES = (
    "emerging",
    "developing",
    "stabilizing",
    "ready_for_greater_challenge",
)
MAX_LEARNING_EVENTS = 500
LES_REVERSIBLE_KEYS = (
    "topic_signals",
    "RA_signals",
    "misconception_signals",
    "causal_chain_signals",
    "question_exposure_log",
    "question_exposure_signals",
    "misconception_sessions",
    "misconception_resolution",
    "causal_strength",
    "learning_event_log",
)


def create_question_attempt(
    *,
    session_id: str,
    question_id: str,
    selected_option: str,
    is_correct: bool,
    mode: str,
    timestamp: str,
    confidence: str | None = None,
    answer_changed: bool | None = None,
    response_time_band: str | None = None,
) -> dict[str, Any]:
    """Create one immutable training attempt observation."""
    selected = _required_text(selected_option, "selected_option").upper()
    if selected not in {"A", "B", "C", "D"}:
        raise ValueError("selected_option must be A, B, C, or D")
    confidence_value = str(confidence or "not_reported").strip().lower()
    if confidence_value not in CONFIDENCE_VALUES:
        raise ValueError("confidence must be low, medium, high, or not_reported")
    attempt = {
        "schema_version": ATTEMPT_SCHEMA_VERSION,
        "attempt_id": "",
        "session_id": _required_text(session_id, "session_id"),
        "question_id": _required_text(question_id, "question_id"),
        "selected_option": selected,
        "is_correct": bool(is_correct),
        "confidence": confidence_value,
        "answer_changed": bool(answer_changed) if answer_changed is not None else False,
        "response_time_band": str(response_time_band or "not_measured").strip(),
        "mode": _required_text(mode, "mode").upper(),
        "timestamp": _required_text(timestamp, "timestamp"),
    }
    attempt["attempt_id"] = "attempt_" + _stable_digest(attempt)
    return attempt


def build_diagnostic_outcome(
    attempt: Mapping[str, Any],
    item: Mapping[str, Any],
) -> dict[str, Any]:
    """Convert an attempt into the existing diagnostic_outcome_v1 contract."""
    _validate_attempt(attempt)
    curriculum = _mapping(item.get("curriculum"))
    links = _mapping(item.get("learning_links"))
    option_links = _mapping(_mapping(links.get("options")).get(attempt["selected_option"]))
    is_correct = bool(attempt["is_correct"])
    selected_role = (
        "correct"
        if is_correct
        else str(option_links.get("diagnostic_role") or "near_neighbor_confusion")
    )
    misconception_id = _optional_text(option_links.get("misconception_id"))
    causal_chain_id = _optional_text(
        option_links.get("causal_chain_id") or links.get("causal_chain_id")
    )
    confidence_alignment = _confidence_alignment(
        is_correct, str(attempt["confidence"])
    )
    timing_band = _timing_band(str(attempt["response_time_band"]))
    remediation = _remediation_route(
        is_correct=is_correct,
        misconception_id=misconception_id,
        causal_chain_id=causal_chain_id,
        topic=str(curriculum.get("topic") or "unknown"),
    )
    outcome = {
        "schema_version": "diagnostic_outcome_v1",
        "identity": {
            "outcome_id": "",
            "item_id": str(item.get("master_item_id") or attempt["question_id"]),
            "attempt_id": str(attempt["attempt_id"]),
            "outcome_version": "1.0.0",
            "generated_by": RUNTIME_VERSION,
            "training_diagnostic_only": True,
        },
        "attempt_observation": {
            "selected_option_id": attempt["selected_option"],
            "is_correct": is_correct,
            "response_time_ms": None,
            "answer_changed": bool(attempt["answer_changed"]),
            "confidence_self_report": attempt["confidence"],
            "hesitation_flag": timing_band in {"slow", "very_slow"},
        },
        "diagnostic_classification": {
            "diagnosed_error_type": _diagnosed_error_type(
                is_correct, selected_role, misconception_id
            ),
            "confidence_alignment": confidence_alignment,
        },
        "source_trace": {
            "item_source_ids": _source_ids(item, causal_chain_id),
            "selected_option_diagnostic_role": selected_role,
            "misconception_id": misconception_id,
            "causal_chain_id": causal_chain_id,
            "sat_relevance": _string_list(links.get("sat_relevance")),
            "topic": str(curriculum.get("topic") or "unknown"),
            "subtopic": str(curriculum.get("subtopic") or curriculum.get("topic") or "unknown"),
            "ra_id": str(curriculum.get("ra") or "unknown"),
        },
        "timing_interpretation": {
            "timing_band": timing_band,
            "timing_interpretation": _timing_interpretation(timing_band, is_correct),
        },
        "remediation_routing": remediation,
        "learner_state_effect_placeholders": {
            "mastery_signal": "positive_observation" if is_correct else "reinforcement_observation",
            "confidence_signal": confidence_alignment,
            "retention_signal": "continue_observation" if is_correct else "schedule_reinforcement",
            "misconception_signal": (
                "misconception_observed" if misconception_id and not is_correct else None
            ),
            "recommended_ledger_event": "formative_learning_event",
        },
        "governance": _diagnostic_governance(),
    }
    outcome["identity"]["outcome_id"] = "outcome_" + _stable_digest(outcome)
    return outcome


def build_formative_event(
    attempt: Mapping[str, Any],
    outcome: Mapping[str, Any],
    item: Mapping[str, Any],
) -> dict[str, Any]:
    """Derive the cognitive-map update directive from a diagnostic outcome."""
    trace = _mapping(outcome.get("source_trace"))
    curriculum = _mapping(item.get("curriculum"))
    is_correct = bool(attempt["is_correct"])
    confidence_signal = str(
        _mapping(outcome.get("diagnostic_classification")).get(
            "confidence_alignment", "not_reported"
        )
    )
    event = {
        "schema_version": FORMATIVE_EVENT_SCHEMA_VERSION,
        "event_id": "",
        "attempt_id": attempt["attempt_id"],
        "session_id": attempt["session_id"],
        "question_id": attempt["question_id"],
        "mode": attempt["mode"],
        "timestamp": attempt["timestamp"],
        "ra_id": str(trace.get("ra_id") or "unknown"),
        "topic": str(trace.get("topic") or "unknown"),
        "subtopic": str(trace.get("subtopic") or "unknown"),
        "difficulty": str(curriculum.get("difficulty") or "unknown"),
        "selected_distractor_role": (
            None if is_correct else trace.get("selected_option_diagnostic_role")
        ),
        "misconception_id": trace.get("misconception_id"),
        "causal_chain_id": trace.get("causal_chain_id"),
        "topic_signal_delta": 1 if is_correct else -1,
        "confidence_signal": confidence_signal,
        "reinforcement_needed": not is_correct,
        "progression_candidate": is_correct
        and confidence_signal in {"aligned", "underconfident_correct"},
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }
    event["event_id"] = "learning_event_" + _stable_digest(event)
    return event


def update_cognitive_map(
    memory: Mapping[str, Any],
    event: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Apply one formative event to pedagogical_memory_v1."""
    before = normalize_pedagogical_memory(dict(memory))
    updated = copy.deepcopy(before)
    topic = _required_text(event.get("topic"), "event.topic")
    confidence = CONFIDENCE_VALUES.get(str(event.get("confidence_signal")))
    if confidence is None:
        confidence = CONFIDENCE_VALUES.get(
            _confidence_level_from_alignment(str(event.get("confidence_signal")))
        )
    prior_skill = copy.deepcopy(updated["skills"].get(topic) or {"concept_id": topic})
    skill = update_mastery(
        prior_skill,
        success=bool(event.get("topic_signal_delta", 0) > 0),
        confidence=confidence,
        misconception_hit=bool(event.get("misconception_id") and event.get("reinforcement_needed")),
        now=str(event["timestamp"]),
    )
    skill["exposure_count"] = int(prior_skill.get("exposure_count", 0) or 0) + 1
    skill["gap_count"] = int(prior_skill.get("gap_count", 0) or 0) + (
        1 if event.get("reinforcement_needed") else 0
    )
    skill["reinforcement_priority"] = _reinforcement_priority(skill)
    skill["learning_stage"] = _learning_stage(skill)
    skill["progression_candidate"] = bool(
        event.get("progression_candidate")
        and skill["learning_stage"] in {"stabilizing", "ready_for_greater_challenge"}
    )
    updated["skills"][topic] = skill
    _update_memory_misconception(updated, event)
    _update_memory_causal_chain(updated, event)
    updated["mastered_concepts"] = sorted(
        concept_id
        for concept_id, state in updated["skills"].items()
        if float(state.get("mastery_probability", 0)) >= 0.82
    )
    events = list(updated.get("learning_events") or [])
    events.append(_event_ledger_entry(event))
    updated["learning_events"] = events[-MAX_LEARNING_EVENTS:]
    updated["governance"] = copy.deepcopy(SAFE_GOVERNANCE)
    change_set = {
        "schema_version": "cognitive_map_change_set_v1",
        "event_id": event["event_id"],
        "topic": topic,
        "before_skill": prior_skill,
        "after_skill": copy.deepcopy(skill),
        "before_learning_events": copy.deepcopy(before.get("learning_events")),
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }
    return updated, change_set


def reverse_cognitive_map_update(
    memory: Mapping[str, Any],
    change_set: Mapping[str, Any],
) -> dict[str, Any]:
    """Reverse one cognitive-map update from its explicit change set."""
    updated = copy.deepcopy(dict(memory))
    topic = _required_text(change_set.get("topic"), "change_set.topic")
    before_skill = change_set.get("before_skill")
    if isinstance(before_skill, Mapping) and set(before_skill) != {"concept_id"}:
        updated.setdefault("skills", {})[topic] = copy.deepcopy(dict(before_skill))
    else:
        updated.setdefault("skills", {}).pop(topic, None)
    before_events = change_set.get("before_learning_events")
    if before_events is None:
        updated.pop("learning_events", None)
    else:
        updated["learning_events"] = copy.deepcopy(before_events)
    return normalize_pedagogical_memory(updated)


def update_les_from_learning_event(
    les: Mapping[str, Any],
    event: Mapping[str, Any],
    item: Mapping[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    """Apply the event through existing LES exposure and runtime consumers."""
    question_id = str(item.get("master_item_id") or event["question_id"])
    result = "correct" if int(event.get("topic_signal_delta", 0)) > 0 else "incorrect"
    session = {
        "mode": event["mode"],
        "items": [copy.deepcopy(dict(item))],
    }
    updated = record_session_observations(
        dict(les),
        session,
        timestamp=str(event["timestamp"]),
        results={question_id: result},
        topic_confidence={
            str(event["topic"]): _confidence_level_from_alignment(
                str(event["confidence_signal"])
            )
        },
        topic_weakness={
            str(event["topic"]): "observed" if event["reinforcement_needed"] else "cleared"
        },
    )
    emitted: list[str] = []
    misconception_id = _optional_text(event.get("misconception_id"))
    if misconception_id:
        updated, signals = process_sba_outcome(
            updated,
            mc_id=misconception_id,
            outcome=result,
            session_id=str(event["session_id"]),
            reference_date=str(event["timestamp"]),
        )
        emitted.extend(signals)
    causal_chain_id = _optional_text(event.get("causal_chain_id"))
    if causal_chain_id:
        updated, signals = update_les_causal(
            updated,
            cc_ids_targeted=[causal_chain_id],
            chains_present=[causal_chain_id] if result == "correct" else [],
        )
        emitted.extend(signals)
    learning_log = list(updated.get("learning_event_log") or [])
    learning_log.append(_event_ledger_entry(event))
    updated["learning_event_log"] = learning_log[-MAX_LEARNING_EVENTS:]
    return updated, emitted


def build_les_change_set(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    event: Mapping[str, Any],
) -> dict[str, Any]:
    """Capture the LES fields touched by one event for deterministic reversal."""
    return {
        "schema_version": "les_learning_event_change_set_v1",
        "event_id": event["event_id"],
        "before": {
            key: copy.deepcopy(before[key]) if key in before else None
            for key in LES_REVERSIBLE_KEYS
        },
        "after": {
            key: copy.deepcopy(after[key]) if key in after else None
            for key in LES_REVERSIBLE_KEYS
        },
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def reverse_les_update(
    les: Mapping[str, Any],
    change_set: Mapping[str, Any],
) -> dict[str, Any]:
    """Reverse fields changed by one learning event without redesigning LES."""
    updated = copy.deepcopy(dict(les))
    before = _mapping(change_set.get("before"))
    for key in LES_REVERSIBLE_KEYS:
        if before.get(key) is None:
            updated.pop(key, None)
        else:
            updated[key] = copy.deepcopy(before[key])
    return updated


def build_next_session_signals(
    memory: Mapping[str, Any],
    les: Mapping[str, Any],
) -> dict[str, Any]:
    """Project composer-ready signals from both historic cognitive map and live LES."""
    summary = build_memory_summary(dict(memory))
    skills = _mapping(memory.get("skills"))

    weak_topics = [
        {
            "topic": topic,
            "priority": state.get("reinforcement_priority", "medium"),
            "stage": state.get("learning_stage", "emerging"),
        }
        for topic, state in sorted(skills.items())
        if isinstance(state, Mapping)
        and state.get("reinforcement_priority") in {"high", "urgent"}
    ]

    strong_topics = [
        {
            "topic": topic,
            "stage": state.get("learning_stage"),
            "next_challenge": _next_challenge(state),
        }
        for topic, state in sorted(skills.items())
        if isinstance(state, Mapping) and state.get("progression_candidate")
    ]

    ra_priority = _ra_reinforcement_priority(les)

    misconceptions = [
        {
            "mc_id": str(item.get("misconception_id")),
            "persistence": True,
            "resolved": False,
            "priority": "high",
        }
        for item in summary.get("recurrent_misconceptions", [])
        if item.get("misconception_id")
    ]

    causal_chains = [
        str(item.get("chain_id"))
        for item in summary.get("difficult_causal_chains", [])
        if item.get("chain_id")
    ]

    return {
        "schema_version": "next_session_learning_signals_v1",
        "weak_topic_priority": weak_topics,
        "strong_topic_progression_candidate": strong_topics,
        "RA_reinforcement_priority": ra_priority,
        "misconception_repair_candidate": misconceptions,
        "causal_chain_reinforcement_candidate": causal_chains,
        "exposure_avoidance": _exposure_avoidance(les),
        "recommended_next_mode": _recommended_mode(
            weak_topics, strong_topics, misconceptions, ra_priority
        ),
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }

def process_question_attempt(
    *,
    attempt: Mapping[str, Any],
    item: Mapping[str, Any],
    memory: Mapping[str, Any],
    les: Mapping[str, Any],
) -> dict[str, Any]:
    """Run the complete attempt -> next-session signal pipeline."""
    outcome = build_diagnostic_outcome(attempt, item)
    event = build_formative_event(attempt, outcome, item)
    updated_memory, change_set = update_cognitive_map(memory, event)
    updated_les, emitted = update_les_from_learning_event(les, event, item)
    les_change_set = build_les_change_set(les, updated_les, event)
    return {
        "attempt": copy.deepcopy(dict(attempt)),
        "diagnostic_outcome": outcome,
        "formative_event": event,
        "cognitive_map": updated_memory,
        "cognitive_map_change_set": change_set,
        "les": updated_les,
        "les_change_set": les_change_set,
        "emitted_signals": emitted,
        "next_session_signals": build_next_session_signals(updated_memory, updated_les),
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def _reinforcement_priority(skill: Mapping[str, Any]) -> str:
    failures = int(skill.get("recent_failures", 0) or 0)
    mastery = float(skill.get("mastery_probability", 0) or 0)
    if failures >= 3 or mastery < 0.25:
        return "urgent"
    if failures >= 1 or mastery < 0.45:
        return "high"
    if mastery < 0.65:
        return "medium"
    return "low"


def _learning_stage(skill: Mapping[str, Any]) -> str:
    attempts = int(skill.get("attempts", 0) or 0)
    mastery = float(skill.get("mastery_probability", 0) or 0)
    failures = int(skill.get("recent_failures", 0) or 0)
    if attempts < 3 or mastery < 0.45:
        return LEARNING_STAGES[0]
    if mastery < 0.65:
        return LEARNING_STAGES[1]
    if mastery < 0.82 or failures:
        return LEARNING_STAGES[2]
    return LEARNING_STAGES[3]


def _next_challenge(skill: Mapping[str, Any]) -> str:
    stage = str(skill.get("learning_stage") or "")
    if stage == "ready_for_greater_challenge":
        return "integration"
    return "causality_and_comparison"


def _update_memory_misconception(memory: dict[str, Any], event: Mapping[str, Any]) -> None:
    mc_id = _optional_text(event.get("misconception_id"))
    if not mc_id or not event.get("reinforcement_needed"):
        return
    entry = dict(memory["recurrent_misconceptions"].get(mc_id) or {
        "misconception_id": mc_id,
        "hits": 0,
    })
    entry["hits"] = int(entry.get("hits", 0) or 0) + 1
    entry["persistence"] = round(min(1.0, entry["hits"] / 5), 3)
    entry["last_detected"] = event["timestamp"]
    memory["recurrent_misconceptions"][mc_id] = entry


def _update_memory_causal_chain(memory: dict[str, Any], event: Mapping[str, Any]) -> None:
    chain_id = _optional_text(event.get("causal_chain_id"))
    if not chain_id or not event.get("reinforcement_needed"):
        return
    entry = dict(memory["difficult_causal_chains"].get(chain_id) or {
        "chain_id": chain_id,
        "failures": 0,
    })
    entry["failures"] = int(entry.get("failures", 0) or 0) + 1
    entry["retention_risk"] = round(min(1.0, entry["failures"] / 4), 3)
    memory["difficult_causal_chains"][chain_id] = entry


def _ra_reinforcement_priority(les: Mapping[str, Any]) -> list[dict[str, Any]]:
    priorities: list[dict[str, Any]] = []
    for ra_id, signal in sorted(_mapping(les.get("RA_signals")).items()):
        if not isinstance(signal, Mapping):
            continue
        performance = _mapping(signal.get("performance"))
        incorrect = int(performance.get("incorrect_count", 0) or 0)
        correct = int(performance.get("correct_count", 0) or 0)
        if incorrect:
            priorities.append({
                "ra_id": ra_id,
                "priority": "high" if incorrect >= correct else "medium",
            })
    return priorities


def _exposure_avoidance(les: Mapping[str, Any]) -> list[str]:
    signals = _mapping(les.get("question_exposure_signals"))
    return sorted(
        question_id
        for question_id, signal in signals.items()
        if isinstance(signal, Mapping) and int(signal.get("exposure_count", 0) or 0) >= 2
    )


def _recommended_mode(
    weak_topics: list[dict[str, Any]],
    strong_topics: list[dict[str, Any]],
    misconceptions: list[str],
    ra_priority: list[dict[str, Any]],
) -> str:
    if misconceptions or ra_priority or any(item["priority"] == "urgent" for item in weak_topics):
        return "RA_FOCUS"
    if weak_topics:
        return "QUICK_25"
    if strong_topics:
        return "STANDARD_50"
    return "EXPRESS_10"


def _remediation_route(
    *,
    is_correct: bool,
    misconception_id: str | None,
    causal_chain_id: str | None,
    topic: str,
) -> dict[str, Any]:
    if is_correct:
        return {
            "recommended_next_action": "increase_difficulty",
            "remediation_target_type": "none",
            "remediation_target_id": None,
            "feedback_priority": "low",
        }
    if misconception_id:
        return {
            "recommended_next_action": "review_misconception",
            "remediation_target_type": "misconception",
            "remediation_target_id": misconception_id,
            "feedback_priority": "high",
        }
    if causal_chain_id:
        return {
            "recommended_next_action": "review_causal_chain",
            "remediation_target_type": "causal_chain",
            "remediation_target_id": causal_chain_id,
            "feedback_priority": "high",
        }
    return {
        "recommended_next_action": "review_topic",
        "remediation_target_type": "topic",
        "remediation_target_id": topic,
        "feedback_priority": "medium",
    }


def _diagnosed_error_type(
    is_correct: bool, selected_role: str, misconception_id: str | None
) -> str:
    if is_correct:
        return "none"
    if misconception_id:
        return "misconception_reinforced"
    role_map = {
        "causal_confusion": "causal_confusion",
        "sat_confusion": "sat_confusion",
        "term_confusion": "terminology_confusion",
        "regional_confusion": "regional_confusion",
        "keyword_trap": "keyword_trap",
        "partial_reasoning": "partial_reasoning",
    }
    return role_map.get(selected_role, "knowledge_gap")


def _confidence_alignment(is_correct: bool, confidence: str) -> str:
    if confidence == "not_reported":
        return "not_reported"
    if is_correct and confidence == "low":
        return "underconfident_correct"
    if is_correct and confidence == "medium":
        return "uncertain_correct"
    if not is_correct and confidence == "high":
        return "overconfident_wrong"
    if not is_correct:
        return "uncertain_wrong"
    return "aligned"


def _confidence_level_from_alignment(alignment: str) -> str:
    if alignment in {"aligned", "overconfident_wrong"}:
        return "high"
    if alignment in {"uncertain_correct", "uncertain_wrong"}:
        return "medium"
    if alignment == "underconfident_correct":
        return "low"
    return "not_recorded"


def _timing_band(value: str) -> str:
    normalized = value.strip().lower()
    return normalized if normalized in {
        "fast", "expected", "slow", "very_slow", "not_measured"
    } else "not_measured"


def _timing_interpretation(timing_band: str, is_correct: bool) -> str:
    if timing_band == "not_measured":
        return "not_measured"
    if timing_band == "fast":
        return "fluent_recall" if is_correct else "likely_guess"
    if timing_band == "expected":
        return "deliberate_reasoning"
    if timing_band == "slow":
        return "hesitation"
    return "uncertainty_signal"


def _source_ids(item: Mapping[str, Any], causal_chain_id: str | None) -> list[str]:
    ids = [str(item.get("master_item_id") or item.get("source_question_id") or "unknown")]
    if causal_chain_id:
        ids.append(causal_chain_id)
    return ids


def _event_ledger_entry(event: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "event_id": event["event_id"],
        "attempt_id": event["attempt_id"],
        "session_id": event["session_id"],
        "question_id": event["question_id"],
        "topic": event["topic"],
        "ra_id": event["ra_id"],
        "timestamp": event["timestamp"],
        "reinforcement_needed": bool(event["reinforcement_needed"]),
        "progression_candidate": bool(event["progression_candidate"]),
    }


def _diagnostic_governance() -> dict[str, bool]:
    return {
        "safe_for_examiner": False,
        "examiner_scoring_allowed": False,
        "official_wset_score": False,
        "training_diagnostic_only": True,
        "uses_llm": False,
        "uses_api": False,
        "uses_embeddings": False,
        "uses_vector_db": False,
        "cloud_services_active": False,
    }


def _validate_attempt(attempt: Mapping[str, Any]) -> None:
    if attempt.get("schema_version") != ATTEMPT_SCHEMA_VERSION:
        raise ValueError(f"attempt schema_version must be {ATTEMPT_SCHEMA_VERSION}")
    for field in ("attempt_id", "session_id", "question_id", "mode", "timestamp"):
        _required_text(attempt.get(field), field)


def _stable_digest(value: Mapping[str, Any]) -> str:
    material = repr(_stable_value(value)).encode("utf-8")
    return hashlib.sha256(material).hexdigest()[:16]


def _stable_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return tuple((str(key), _stable_value(value[key])) for key in sorted(value))
    if isinstance(value, list):
        return tuple(_stable_value(item) for item in value)
    return value


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _string_list(value: Any) -> list[str]:
    return [str(item) for item in value] if isinstance(value, list) else []


def _required_text(value: Any, field: str) -> str:
    normalized = str(value or "").strip()
    if not normalized:
        raise ValueError(f"{field} must be non-empty text")
    return normalized


def _optional_text(value: Any) -> str | None:
    normalized = str(value or "").strip()
    return normalized or None

"""Learning Event Runtime — reconciled cognitive-map, LES, SBA, OR, and WWJ runtime.

This module is deterministic and training-diagnostic only. It does not grade,
calculate percentages, produce pass/fail decisions, or activate examiner authority.
"""

from __future__ import annotations

from pathlib import Path
import copy
from copy import deepcopy
import hashlib
from collections.abc import Mapping
from typing import Any

from tools.learner_model.causal_runtime import update_les_causal
from tools.learner_model.knowledge_tracing import (
    build_memory_summary,
    normalize_pedagogical_memory,
    update_mastery,
)
from tools.learner_model.misconception_adapter import (
    build_active_insights,
    detect_text_evidence,
)
from tools.learner_model.misconception_runtime import process_sba_outcome
from tools.learner_model.open_response_evaluator import evaluate_open_response
from tools.learner_model.wwj_remediation import get_remediation_path
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

def _build_diagnostic_outcome_from_attempt(
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

def build_diagnostic_outcome(*args: Any, **kwargs: Any) -> dict[str, Any]:
    """Build diagnostic outcome for both historic attempt/item and modern SBA calls.

    Supported contracts:
      - build_diagnostic_outcome(attempt, item)
      - build_diagnostic_outcome(outcome=..., question_id=..., mc_id=...)
    """
    if len(args) == 2 and not kwargs:
        return _build_diagnostic_outcome_from_attempt(args[0], args[1])
    if "attempt" in kwargs and "item" in kwargs:
        return _build_diagnostic_outcome_from_attempt(kwargs["attempt"], kwargs["item"])

    outcome = str(kwargs.get("outcome") or "")
    question_id = str(kwargs.get("question_id") or "")
    mc_id = _optional_text(kwargs.get("mc_id"))
    return {
        "outcome": outcome,
        "question_id": question_id,
        "mc_id": mc_id,
        "remediation_routing": _remediation_route(mc_id=mc_id, outcome=outcome),
    }

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

class _IdCandidate(dict):
    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.get("mc_id") == other or self.get("cc_id") == other
        return dict.__eq__(self, other)

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
        str(item.get("misconception_id"))
        for item in summary.get("recurrent_misconceptions", [])
        if item.get("misconception_id")
    ]

    causal_chains = [
        str(item.get("chain_id"))
        for item in summary.get("difficult_causal_chains", [])
        if item.get("chain_id")
    ]

    mc_signals = _mapping(les.get("misconception_signals"))
    mc_resolution = _mapping(les.get("misconception_resolution"))
    mc_sessions = _mapping(les.get("misconception_sessions"))

    repair_candidates: list[dict[str, Any]] = []
    for mc_id, signal in sorted(mc_signals.items()):
        if not isinstance(signal, Mapping):
            continue
        if int(signal.get("detection_count", 0) or 0) <= 0:
            continue
        resolution = _mapping(mc_resolution.get(mc_id))
        if bool(resolution.get("resolved", False)):
            continue
        sessions = _mapping(mc_sessions.get(mc_id))
        session_ids = sessions.get("session_ids", [])
        if not isinstance(session_ids, list):
            session_ids = []
        persistence = len(session_ids) > 1
        repair_candidates.append(_IdCandidate({
            "mc_id": str(mc_id),
            "persistence": persistence,
            "resolved": False,
            "priority": "high" if persistence else "standard",
        }))

    cc_signals = _mapping(les.get("causal_chain_signals"))
    causal_strength = _mapping(les.get("causal_strength"))

    reinforcement_candidates: list[dict[str, Any]] = []
    for cc_id, signal in sorted(cc_signals.items()):
        if not isinstance(signal, Mapping):
            continue
        if int(signal.get("exposure_count", 0) or 0) <= 0:
            continue
        strength = str(causal_strength.get(cc_id) or "superficial")
        reinforcement_candidates.append(_IdCandidate({
            "cc_id": str(cc_id),
            "causal_strength": strength,
            "gap_priority": "high" if strength == "superficial" else "standard",
        }))

    return {
        "schema_version": "next_session_learning_signals_v1",
        "weak_topic_priority": weak_topics,
        "strong_topic_progression_candidate": strong_topics,
        "RA_reinforcement_priority": ra_priority,

        "misconception_repair_candidate": repair_candidates,
        "causal_chain_reinforcement_candidate": reinforcement_candidates,

        "exposure_avoidance": _exposure_avoidance(les),

        "recommended_next_mode": _recommended_mode(
            weak_topics,
            strong_topics,
            repair_candidates,
            ra_priority,
        ),

        "review_topics": [],

        "modern_misconception_repair_candidate": repair_candidates,
        "modern_causal_chain_reinforcement_candidate": reinforcement_candidates,

        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }

def process_question_attempt(**kwargs: Any) -> dict[str, Any]:
    """Run an SBA attempt through the runtime.

    Supports both contracts:
      - historic: process_question_attempt(attempt=..., item=..., memory=..., les=...)
      - modern: process_question_attempt(student_answer=..., question_item=..., ...)
    """
    if "attempt" in kwargs:
        attempt = _mapping(kwargs.get("attempt"))
        item = _mapping(kwargs.get("item"))
        memory = _mapping(kwargs.get("memory"))
        les = _mapping(kwargs.get("les"))

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

    student_answer = str(kwargs.get("student_answer") or "")
    question_id = _required_text(kwargs.get("question_id"), "question_id")
    session_id = _required_text(kwargs.get("session_id"), "session_id")
    mode = _required_text(kwargs.get("mode"), "mode")
    timestamp = _required_text(kwargs.get("timestamp"), "timestamp")
    question_item = dict(_mapping(kwargs.get("question_item")))
    memory = dict(_mapping(kwargs.get("memory")))
    les = dict(_mapping(kwargs.get("les")))
    mc_id = _optional_text(kwargs.get("mc_id"))

    correct = str(question_item.get("correct_answer") or "").strip().upper()
    student = student_answer.strip().upper()
    outcome = "correct" if student == correct else "incorrect"
    if not mc_id and outcome == "incorrect":
        selected_text = _selected_option_text(question_item, student_answer)
        detection = detect_text_evidence(selected_text, source_type="sba")
        mc_id = _optional_text(detection.get("misconception_id"))

    updated_les = copy.deepcopy(les)
    all_signals: list[str] = []
    if mc_id:
        updated_les, mc_signals = process_sba_outcome(
            les,
            mc_id=mc_id,
            outcome=outcome,
            session_id=session_id,
            source_type="sba",
            item_id=question_id,
        )
        all_signals.extend(mc_signals)

    diagnostic = build_diagnostic_outcome(
        outcome=outcome,
        question_id=question_id,
        mc_id=mc_id,
    )
    les_change_set = _diff_dicts(les, updated_les)

    updated_memory = copy.deepcopy(memory)
    if mc_id and outcome == "incorrect":
        rec = updated_memory.setdefault("recurrent_misconceptions", {})
        entry = dict(rec.get(mc_id) or {"misconception_id": mc_id, "hits": 0})
        entry["hits"] = int(entry.get("hits", 0)) + 1
        entry["persistence"] = round(min(1.0, entry["hits"] / 5), 3)
        rec[mc_id] = entry
    cognitive_map_change_set = _diff_dicts(memory, updated_memory)

    next_signals = build_next_session_signals(updated_memory, updated_les)
    return {
        "attempt": {
            "question_id": question_id,
            "session_id": session_id,
            "mode": mode,
            "timestamp": timestamp,
            "student_answer": student_answer,
            "outcome": outcome,
        },
        "diagnostic_outcome": diagnostic,
        "formative_event": {
            "event_type": "sba_attempt",
            "question_id": question_id,
            "session_id": session_id,
            "timestamp": timestamp,
            "outcome": outcome,
            "emitted_signals": all_signals,
        },
        "cognitive_map": updated_memory,
        "cognitive_map_change_set": cognitive_map_change_set,
        "les": updated_les,
        "les_change_set": les_change_set,
        "emitted_signals": all_signals,
        "next_session_signals": next_signals,
        "governance": _governance(),
    }


def process_text_misconception_attempt(
    *,
    answer_text: str,
    source_type: str,
    session_id: str,
    item_id: str,
    timestamp: str,
    les: dict[str, Any],
    candidate_ids: list[str] | None = None,
    explicit_id: str | None = None,
) -> dict[str, Any]:
    """Detect and record misconception evidence for text-based learning events."""
    detection = detect_text_evidence(
        answer_text,
        explicit_id=explicit_id,
        candidate_ids=candidate_ids,
        source_type=source_type,
    )
    updated_les = deepcopy(les)
    emitted: list[str] = []
    if detection["detected"]:
        updated_les, emitted = process_sba_outcome(
            updated_les,
            mc_id=detection["misconception_id"],
            outcome="incorrect",
            session_id=session_id,
            reference_date=timestamp,
            source_type=source_type,
            item_id=item_id,
            matched_signals=detection["matched_signals"],
        )
    return {
        "detection": detection,
        "les": updated_les,
        "emitted_signals": emitted,
        "misconception_insights": build_active_insights(updated_les),
        "governance": _governance(),
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
    is_correct: bool | None = None,
    misconception_id: str | None = None,
    causal_chain_id: str | None = None,
    topic: str = "unknown",
    mc_id: str | None = None,
    outcome: str | None = None,
) -> dict[str, Any] | None:
    """Route remediation for both diagnostic_outcome_v1 and WWJ lookup contracts."""
    if outcome is not None or mc_id is not None:
        effective_mc_id = mc_id or misconception_id
        if not effective_mc_id:
            return None
        if outcome != "incorrect":
            return {
                "mc_id": effective_mc_id,
                "remediation_available": False,
                "remediation_message": "",
                "wwj_chunks": [],
                "remediation_source": "none",
            }
        path = get_remediation_path(effective_mc_id)
        return {
            "mc_id": effective_mc_id,
            "remediation_available": path["availability"] == "available",
            "remediation_message": path["remediation_message"],
            "wwj_chunks": path["wwj_chunks"],
            "remediation_source": "wwj_lookup",
        }

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


def _selected_option_text(question_item: Mapping[str, Any], student_answer: str) -> str:
    options = question_item.get("options")
    if not isinstance(options, Mapping):
        return ""
    selected = str(student_answer or "").strip()
    value = options.get(selected) or options.get(selected.upper()) or options.get(selected.lower())
    if isinstance(value, Mapping):
        return str(value.get("text") or value.get("option_text") or "")
    return str(value or "")


def _required_text(value: Any, field: str) -> str:
    normalized = str(value or "").strip()
    if not normalized:
        raise ValueError(f"{field} must be non-empty text")
    return normalized


def _optional_text(value: Any) -> str | None:
    normalized = str(value or "").strip()
    return normalized or None


# ---------------------------------------------------------------------------
# Open Response pipeline
# ---------------------------------------------------------------------------

def process_open_response_attempt(
    *,
    student_response_text: str,
    question_id: str,
    session_id: str,
    mode: str,
    timestamp: str,
    or_item: dict[str, Any],
    memory: dict[str, Any],
    les: dict[str, Any],
) -> dict[str, Any]:
    """Process one open response attempt through the full LES/cognitive-map pipeline.

    Connects evaluate_open_response() to the LES and cognitive map:

      1. Evaluates the student response via evaluate_open_response().
      2. Updates LES causal_chain_signals via update_les_causal().
      3. Updates memory.difficult_causal_chains with absent chains.
      4. Processes mc_ids_relevant as SBA-like signals (absent→incorrect, present→correct).
      5. Collects WWJ remediation chunks for each mc_id in mc_ids_relevant.
      6. Builds next_session_signals from the updated memory and LES.

    Returns a dict with the same top-level keys as process_question_attempt().
    """
    cc_ids_targeted: list[str] = list(or_item.get("causal_chain_target") or [])
    mc_ids_relevant: list[str] = list(or_item.get("mc_ids_relevant") or [])

    question_context: dict[str, Any] = {
        "cc_ids_targeted": cc_ids_targeted,
        "mc_ids_relevant": mc_ids_relevant,
        "topic": or_item.get("topic", ""),
        "ra_id": or_item.get("ra_id", ""),
    }

    # 1. Evaluate the open response
    eval_result = evaluate_open_response(student_response_text, question_context)

    chains_present: list[str] = eval_result["causal_coverage"]["chains_present"]
    chains_absent: list[str] = eval_result["causal_coverage"]["chains_absent"]

    # 2. Update LES causal signals
    updated_les, causal_signals = update_les_causal(
        les,
        cc_ids_targeted=cc_ids_targeted,
        chains_present=chains_present,
    )
    all_signals: list[str] = list(causal_signals)

    # 3. Update memory.difficult_causal_chains with absent chains
    updated_memory = deepcopy(memory)
    diff_cc = updated_memory.setdefault("difficult_causal_chains", {})
    for cc_id in chains_absent:
        entry = dict(diff_cc.get(cc_id) or {"causal_chain_id": cc_id, "hits": 0})
        entry["hits"] = int(entry.get("hits", 0)) + 1
        diff_cc[cc_id] = entry

    # 4. Record only direct misconception evidence from the learner response.
    if mc_ids_relevant:
        misconception_result = process_text_misconception_attempt(
            answer_text=student_response_text,
            source_type="open_response",
            session_id=session_id,
            item_id=question_id,
            timestamp=timestamp,
            les=updated_les,
            candidate_ids=mc_ids_relevant,
        )
        updated_les = misconception_result["les"]
        all_signals.extend(misconception_result["emitted_signals"])

    # 5. Collect WWJ remediation chunks for mc_ids_relevant
    wwj_chunks: list[str] = []
    for mc_id in mc_ids_relevant:
        path = get_remediation_path(mc_id)
        wwj_chunks.extend(path["wwj_chunks"])
    wwj_deduped = list(dict.fromkeys(wwj_chunks))

    # Include the evaluator's own wwj_chunks for any mc_ids passed in question_context
    for chunk in eval_result["remediation"]["wwj_chunks"]:
        if chunk not in wwj_deduped:
            wwj_deduped.append(chunk)

    diagnostic = {
        "profile": eval_result["profile"],
        "question_id": question_id,
        "cc_ids_targeted": cc_ids_targeted,
        "mc_ids_relevant": mc_ids_relevant,
        "chains_present": chains_present,
        "chains_absent": chains_absent,
        "reasoning_quality": eval_result["reasoning_quality"],
        "remediation": {
            "concepts_to_reinforce": eval_result["remediation"]["concepts_to_reinforce"],
            "causality_to_reinforce": eval_result["remediation"]["causality_to_reinforce"],
            "wwj_chunks": wwj_deduped,
        },
    }

    les_change_set = _diff_dicts(les, updated_les)
    cognitive_map_change_set = _diff_dicts(memory, updated_memory)
    next_signals = build_next_session_signals(updated_memory, updated_les)

    return {
        "attempt": {
            "question_id": question_id,
            "session_id": session_id,
            "mode": mode,
            "timestamp": timestamp,
            "student_response_text": student_response_text,
            "profile": eval_result["profile"],
        },
        "diagnostic_outcome": diagnostic,
        "formative_event": {
            "event_type": "open_response_attempt",
            "question_id": question_id,
            "session_id": session_id,
            "timestamp": timestamp,
            "profile": eval_result["profile"],
            "emitted_signals": all_signals,
        },
        "cognitive_map": updated_memory,
        "cognitive_map_change_set": cognitive_map_change_set,
        "les": updated_les,
        "les_change_set": les_change_set,
        "emitted_signals": all_signals,
        "next_session_signals": next_signals,
        "governance": _governance(),
    }


# ---------------------------------------------------------------------------
# Persistence helper (minimal atomicity — memory first, then LES)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Persistence helper
# ---------------------------------------------------------------------------

def persist_learning_event_result(
    result: dict[str, Any],
    *,
    memory_path: "Path | None" = None,
    les_path: "Path | None" = None,
) -> dict[str, Any]:
    """Persist the LES and memory from a process_question_attempt / process_open_response_attempt result.

    Write order: memory first, then LES. If memory write fails, LES is not written.
    If LES write fails, memory has already been written — callers should handle
    the resulting inconsistency (e.g. retry or alert).

    Args:
        result:      Output dict from process_question_attempt or process_open_response_attempt.
        memory_path: Override for pedagogical_memory path. Defaults to DEFAULT_PEDAGOGICAL_MEMORY_PATH.
        les_path:    Override for epistemic_state path. Defaults to DEFAULT_LES_PATH.

    Returns:
        Dict with keys: memory_path (str), les_path (str), success (bool).
    """
    from pathlib import Path as _Path

    from tools.learner_model.knowledge_tracing import (
        DEFAULT_PEDAGOGICAL_MEMORY_PATH,
        save_pedagogical_memory,
    )
    from tools.orchestrator.learner_state import DEFAULT_LES_PATH, write_learner_state

    mem_path = _Path(memory_path) if memory_path else DEFAULT_PEDAGOGICAL_MEMORY_PATH
    ls_path = _Path(les_path) if les_path else DEFAULT_LES_PATH

    updated_memory = result.get("cognitive_map") or {}
    updated_les = result.get("les") or {}

    save_pedagogical_memory(updated_memory, mem_path)
    write_learner_state(updated_les, ls_path)

    return {
        "memory_path": str(mem_path),
        "les_path": str(ls_path),
        "success": True,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Modern compatibility helpers
# ---------------------------------------------------------------------------

def _diff_dicts(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    """Return top-level keys that differ between old and new."""
    changed: dict[str, Any] = {}
    for key in set(old) | set(new):
        if old.get(key) != new.get(key):
            changed[key] = new.get(key)
    return changed

def _governance() -> dict[str, bool]:
    return {
        "safe_for_examiner": False,
        "examiner_scoring_allowed": False,
        "uses_llm": False,
        "uses_api": False,
        "uses_embeddings": False,
        "uses_vector_db": False,
        "cloud_services_active": False,
    }

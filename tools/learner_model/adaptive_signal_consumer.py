"""Adaptive Signal Consumer — consolidates learning signals into a structured signal dict.

Reads from:
  - next_session_signals: output of build_next_session_signals()
  - les.topic_signals, les.RA_signals
  - les.misconception_signals, les.misconception_resolution
  - les.causal_chain_signals, les.causal_strength
  - les.question_exposure_signals (question_exposure_log)
  - memory.recurrent_misconceptions
  - memory.difficult_causal_chains

Produces a structured signal dict consumed by the Adaptive Composer.

Governance invariants (permanently False):
  safe_for_examiner, examiner_scoring_allowed, uses_llm, uses_api,
  uses_embeddings, uses_vector_db, cloud_services_active.

No file I/O. No scoring. No pass/fail. No percentages.
"""

from __future__ import annotations

from typing import Any


# Ordinal reinforcement priority labels (not numeric)
_PRIORITY_URGENT = "urgent"
_PRIORITY_HIGH = "high"
_PRIORITY_STANDARD = "standard"

# How many times a question must appear before it enters avoid_repetition
_EXPOSURE_THRESHOLD = 2

# Misconception persistence threshold: seen in >1 session
_MC_PERSISTENCE_SESSION_THRESHOLD = 1

# LES confidence levels considered weak (needing reinforcement)
_WEAK_CONFIDENCE_LEVELS = {"not_recorded", "low"}


def consume_adaptive_signals(
    next_session_signals: dict[str, Any],
    les: dict[str, Any],
    memory: dict[str, Any],
) -> dict[str, Any]:
    """Consolidate learning signals into a structured adaptive signal dict.

    Args:
        next_session_signals: output of build_next_session_signals()
        les: current Learner Epistemic State dict (not mutated)
        memory: current pedagogical memory dict (not mutated)

    Returns:
        Dict with keys:
          reinforcement_targets  — topics/items needing reinforcement
          progression_targets    — topics ready for greater challenge
          review_targets         — misconceptions and causal gaps to repair
          challenge_targets      — strong topics candidate for challenge
          avoid_repetition_ids   — question_ids to avoid (excessive exposure)
          governance             — invariant governance block
    """
    topic_signals: dict[str, Any] = dict(les.get("topic_signals") or {})
    ra_signals: dict[str, Any] = dict(les.get("RA_signals") or {})
    mc_signals: dict[str, Any] = dict(les.get("misconception_signals") or {})
    mc_resolution: dict[str, Any] = dict(les.get("misconception_resolution") or {})
    mc_sessions: dict[str, Any] = dict(les.get("misconception_sessions") or {})
    cc_signals: dict[str, Any] = dict(les.get("causal_chain_signals") or {})
    causal_strength: dict[str, Any] = dict(les.get("causal_strength") or {})
    exposure_log: list[dict[str, Any]] = list(les.get("question_exposure_log") or [])

    rec_mc: dict[str, Any] = dict(memory.get("recurrent_misconceptions") or {})
    diff_cc: dict[str, Any] = dict(memory.get("difficult_causal_chains") or {})

    next_sig_repair = list(next_session_signals.get("misconception_repair_candidate") or [])
    next_sig_causal = list(next_session_signals.get("causal_chain_reinforcement_candidate") or [])

    reinforcement_targets = _build_reinforcement_targets(
        topic_signals, ra_signals, rec_mc, diff_cc
    )
    progression_targets = _build_progression_targets(topic_signals, ra_signals)
    review_targets = _build_review_targets(
        next_sig_repair, next_sig_causal, mc_signals, mc_resolution, mc_sessions, cc_signals, causal_strength
    )
    challenge_targets = _build_challenge_targets(topic_signals, ra_signals)
    avoid_repetition_ids = _build_avoid_repetition_ids(exposure_log)

    return {
        "reinforcement_targets": reinforcement_targets,
        "progression_targets": progression_targets,
        "review_targets": review_targets,
        "challenge_targets": challenge_targets,
        "avoid_repetition_ids": avoid_repetition_ids,
        "governance": _governance(),
    }


# ---------------------------------------------------------------------------
# Reinforcement targets
# ---------------------------------------------------------------------------

def _build_reinforcement_targets(
    topic_signals: dict[str, Any],
    ra_signals: dict[str, Any],
    rec_mc: dict[str, Any],
    diff_cc: dict[str, Any],
) -> list[dict[str, Any]]:
    """Topics and items that need reinforcement based on weak signals."""
    targets: list[dict[str, Any]] = []

    # Weak topics from LES topic_signals
    for topic, sig in topic_signals.items():
        if not isinstance(sig, dict):
            continue
        confidence = str(sig.get("confidence_level", "not_recorded"))
        exposure = int(sig.get("exposure_count", 0))
        incorrect = int(sig.get("incorrect_count", 0))

        if confidence in _WEAK_CONFIDENCE_LEVELS and exposure > 0:
            priority = _PRIORITY_HIGH if incorrect >= 2 else _PRIORITY_STANDARD
            targets.append({
                "type": "topic",
                "id": topic,
                "topic": topic,
                "reinforcement_priority": priority,
                "rationale": "weak_confidence_level",
            })

    # RA-level weak signals
    for ra_id, sig in ra_signals.items():
        if not isinstance(sig, dict):
            continue
        perf = sig.get("performance") or {}
        incorrect = int(perf.get("incorrect_count", 0))
        correct = int(perf.get("correct_count", 0))
        total = incorrect + correct
        if total == 0:
            continue
        if incorrect > correct:
            targets.append({
                "type": "ra",
                "id": ra_id,
                "ra_id": ra_id,
                "reinforcement_priority": _PRIORITY_URGENT if incorrect > correct * 2 else _PRIORITY_HIGH,
                "rationale": "negative_ra_performance",
            })

    # Recurrent misconceptions from memory
    for mc_id, entry in rec_mc.items():
        if not isinstance(entry, dict):
            continue
        hits = int(entry.get("hits", 0))
        if hits >= 2:
            targets.append({
                "type": "misconception",
                "id": mc_id,
                "mc_id": mc_id,
                "reinforcement_priority": _PRIORITY_URGENT if hits >= 3 else _PRIORITY_HIGH,
                "rationale": "recurrent_misconception_memory",
            })

    # Difficult causal chains from memory
    for cc_id, entry in diff_cc.items():
        if not isinstance(entry, dict):
            continue
        hits = int(entry.get("hits", 0))
        failures = int(entry.get("failures", 0))
        count = max(hits, failures)
        if count >= 1:
            targets.append({
                "type": "causal_chain",
                "id": cc_id,
                "cc_id": cc_id,
                "reinforcement_priority": _PRIORITY_HIGH if count >= 2 else _PRIORITY_STANDARD,
                "rationale": "difficult_causal_chain_memory",
            })

    return targets


# ---------------------------------------------------------------------------
# Progression targets
# ---------------------------------------------------------------------------

def _build_progression_targets(
    topic_signals: dict[str, Any],
    ra_signals: dict[str, Any],
) -> list[dict[str, Any]]:
    """Topics with strong signals that are ready for greater challenge."""
    targets: list[dict[str, Any]] = []

    for topic, sig in topic_signals.items():
        if not isinstance(sig, dict):
            continue
        confidence = str(sig.get("confidence_level", "not_recorded"))
        correct = int(sig.get("correct_count", 0))
        incorrect = int(sig.get("incorrect_count", 0))
        total = correct + incorrect
        if total == 0:
            continue

        if confidence == "high" and correct > incorrect and total >= 2:
            targets.append({
                "type": "topic",
                "id": topic,
                "topic": topic,
                "learning_stage": "ready_for_greater_challenge",
                "rationale": "high_confidence_sustained",
            })

    for ra_id, sig in ra_signals.items():
        if not isinstance(sig, dict):
            continue
        perf = sig.get("performance") or {}
        correct = int(perf.get("correct_count", 0))
        incorrect = int(perf.get("incorrect_count", 0))
        total = correct + incorrect
        if total == 0:
            continue
        trend = str(sig.get("trend", "not_observed"))
        if correct > incorrect * 2 and trend in ("improving", "stable") and total >= 3:
            targets.append({
                "type": "ra",
                "id": ra_id,
                "ra_id": ra_id,
                "learning_stage": "ready_for_greater_challenge",
                "rationale": "strong_ra_performance",
            })

    return targets


# ---------------------------------------------------------------------------
# Review targets (misconceptions + causal gaps)
# ---------------------------------------------------------------------------

def _build_review_targets(
    next_sig_repair: list[dict[str, Any]],
    next_sig_causal: list[dict[str, Any]],
    mc_signals: dict[str, Any],
    mc_resolution: dict[str, Any],
    mc_sessions: dict[str, Any],
    cc_signals: dict[str, Any],
    causal_strength: dict[str, Any],
) -> list[dict[str, Any]]:
    """Misconceptions and causal gaps that need direct repair."""
    targets: list[dict[str, Any]] = []

    # Misconception repair candidates from next_session_signals
    seen_mc: set[str] = set()
    for candidate in next_sig_repair:
        mc_id = str(candidate.get("mc_id") or "")
        if not mc_id or mc_id in seen_mc:
            continue
        seen_mc.add(mc_id)
        persistence = bool(candidate.get("persistence", False))
        resolved = bool(candidate.get("resolved", False))
        if resolved:
            continue
        priority = candidate.get("priority", _PRIORITY_STANDARD)
        targets.append({
            "type": "misconception",
            "id": mc_id,
            "mc_id": mc_id,
            "persistence": persistence,
            "resolved": resolved,
            "gap_priority": "high" if (persistence and not resolved) else "standard",
            "review_priority": priority,
            "rationale": "misconception_repair_candidate",
        })

    # Additional misconception signals from LES (not already captured)
    for mc_id, sig in mc_signals.items():
        if mc_id in seen_mc or not isinstance(sig, dict):
            continue
        detection_count = int(sig.get("detection_count", 0))
        if detection_count == 0:
            continue
        sess = mc_sessions.get(mc_id, {})
        session_ids = sess.get("session_ids", []) if isinstance(sess, dict) else []
        persistence = len(session_ids) > _MC_PERSISTENCE_SESSION_THRESHOLD
        res = mc_resolution.get(mc_id, {})
        resolved = bool(res.get("resolved", False)) if isinstance(res, dict) else False
        if resolved:
            continue
        seen_mc.add(mc_id)
        targets.append({
            "type": "misconception",
            "id": mc_id,
            "mc_id": mc_id,
            "persistence": persistence,
            "resolved": resolved,
            "gap_priority": "high" if persistence else "standard",
            "review_priority": "high" if persistence else _PRIORITY_STANDARD,
            "rationale": "les_misconception_signal",
        })

    # Causal chain reinforcement candidates
    seen_cc: set[str] = set()
    for candidate in next_sig_causal:
        cc_id = str(candidate.get("cc_id") or "")
        if not cc_id or cc_id in seen_cc:
            continue
        seen_cc.add(cc_id)
        gap_priority = str(candidate.get("gap_priority", _PRIORITY_STANDARD))
        strength = str(candidate.get("causal_strength", "superficial"))
        targets.append({
            "type": "causal_chain",
            "id": cc_id,
            "cc_id": cc_id,
            "causal_strength": strength,
            "gap_priority": gap_priority,
            "review_priority": "high" if gap_priority == "high" else _PRIORITY_STANDARD,
            "rationale": "causal_chain_reinforcement_candidate",
        })

    # Additional causal chain signals from LES
    for cc_id, sig in cc_signals.items():
        if cc_id in seen_cc or not isinstance(sig, dict):
            continue
        exposure = int(sig.get("exposure_count", 0))
        if exposure == 0:
            continue
        strength = str(causal_strength.get(cc_id, "superficial"))
        gap_priority = "high" if strength == "superficial" else "standard"
        seen_cc.add(cc_id)
        targets.append({
            "type": "causal_chain",
            "id": cc_id,
            "cc_id": cc_id,
            "causal_strength": strength,
            "gap_priority": gap_priority,
            "review_priority": "high" if gap_priority == "high" else _PRIORITY_STANDARD,
            "rationale": "les_causal_chain_signal",
        })

    return targets


# ---------------------------------------------------------------------------
# Challenge targets
# ---------------------------------------------------------------------------

def _build_challenge_targets(
    topic_signals: dict[str, Any],
    ra_signals: dict[str, Any],
) -> list[dict[str, Any]]:
    """Strong topics where distinction-level challenge is appropriate."""
    targets: list[dict[str, Any]] = []

    for topic, sig in topic_signals.items():
        if not isinstance(sig, dict):
            continue
        confidence = str(sig.get("confidence_level", "not_recorded"))
        correct = int(sig.get("correct_count", 0))
        total = correct + int(sig.get("incorrect_count", 0))
        if total < 3:
            continue
        if confidence == "high" and correct >= total * 0.8:
            targets.append({
                "type": "topic",
                "id": topic,
                "topic": topic,
                "challenge_level": "distinction",
                "rationale": "sustained_high_accuracy",
            })

    return targets


# ---------------------------------------------------------------------------
# Avoid-repetition ids
# ---------------------------------------------------------------------------

def _build_avoid_repetition_ids(exposure_log: list[dict[str, Any]]) -> list[str]:
    """Question IDs seen >= _EXPOSURE_THRESHOLD times in the log."""
    counts: dict[str, int] = {}
    for entry in exposure_log:
        if not isinstance(entry, dict):
            continue
        qid = str(entry.get("question_id") or "").strip()
        if qid:
            counts[qid] = counts.get(qid, 0) + 1
    return sorted(qid for qid, count in counts.items() if count >= _EXPOSURE_THRESHOLD)


# ---------------------------------------------------------------------------
# Governance
# ---------------------------------------------------------------------------

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

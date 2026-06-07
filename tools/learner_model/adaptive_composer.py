"""Adaptive Composer v1 — decides pedagogical priorities before Session Composer acts.

This module does NOT replace the Session Composer (tools/question_generation/sba_session_composer.py).
The Session Composer continues building valid sessions. This module produces an
adaptive_session_plan that Session Composer can receive to order its candidate pool.

The plan contains ordinal priority scores (integers, not percentages) — higher means
more pedagogically urgent for this learner at this moment.

Governance invariants (permanently False):
  safe_for_examiner, examiner_scoring_allowed, uses_llm, uses_api,
  uses_embeddings, uses_vector_db, cloud_services_active.

No file I/O. No scoring authority. No pass/fail. No WSET grade labels.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from tools.learner_model.wwj_remediation import get_remediation_path


# ---------------------------------------------------------------------------
# Session mode → target item count
# ---------------------------------------------------------------------------

SESSION_MODE_SIZES: dict[str, int] = {
    "EXPRESS_10": 10,
    "QUICK_25": 25,
    "STANDARD_50": 50,
    "FULL_DIAGNOSTIC": 50,
    "RA_FOCUS": 15,
}

# Ordinal priority scores (higher = more urgent)
_PRIORITY_MAX = 100      # misconception persisted, unresolved
_PRIORITY_URGENT = 80    # urgent reinforcement
_PRIORITY_HIGH = 60      # high reinforcement / high causal gap
_PRIORITY_STANDARD = 40  # standard reinforcement
_PRIORITY_CHALLENGE = 20 # challenge / progression upward
_PRIORITY_BASE = 10      # no special signal


def compose_adaptive_session_plan(
    session_mode: str,
    eligibility_pool: list[dict[str, Any]],
    diagnostic_blueprint: dict[str, Any],
    adaptive_signals: dict[str, Any],
) -> dict[str, Any]:
    """Build an adaptive session plan from learner signals and the eligibility pool.

    Args:
        session_mode:        One of SESSION_MODE_SIZES keys (e.g. "EXPRESS_10").
        eligibility_pool:    List of candidate question dicts from the master bank.
                             Each must have at least a "master_item_id" or "source_question_id".
        diagnostic_blueprint: Blueprint config dict (RA distribution, etc.).
                             Informational — does not override governance.
        adaptive_signals:    Output of consume_adaptive_signals().

    Returns:
        adaptive_session_plan dict with keys:
          session_mode, target_size, question_priorities,
          reinforcement_rationale, progression_rationale,
          challenge_rationale, exposure_balancing_rationale,
          remediation_paths, governance.
    """
    target_size = _resolve_mode_size(session_mode, eligibility_pool)

    reinforcement_targets = list(adaptive_signals.get("reinforcement_targets") or [])
    progression_targets = list(adaptive_signals.get("progression_targets") or [])
    review_targets = list(adaptive_signals.get("review_targets") or [])
    challenge_targets = list(adaptive_signals.get("challenge_targets") or [])
    avoid_ids = set(adaptive_signals.get("avoid_repetition_ids") or [])

    # Index signal IDs for fast lookup
    reinforcement_ids: dict[str, str] = {
        str(t.get("id") or ""): str(t.get("reinforcement_priority", "standard"))
        for t in reinforcement_targets
        if t.get("id")
    }
    progression_ids: set[str] = {
        str(t.get("id") or "") for t in progression_targets if t.get("id")
    }
    challenge_topic_ids: set[str] = {
        str(t.get("topic") or "") for t in challenge_targets if t.get("topic")
    }

    # Review: misconceptions
    review_mc: dict[str, dict[str, Any]] = {}
    review_cc: dict[str, str] = {}
    for rv in review_targets:
        if rv.get("type") == "misconception":
            mc_id = str(rv.get("mc_id") or "")
            if mc_id:
                review_mc[mc_id] = rv
        elif rv.get("type") == "causal_chain":
            cc_id = str(rv.get("cc_id") or "")
            if cc_id:
                review_cc[cc_id] = str(rv.get("gap_priority", "standard"))

    question_priorities: list[dict[str, Any]] = []
    used_topics: dict[str, int] = {}

    for item in eligibility_pool:
        qid = _item_id(item)
        curriculum = _mapping(item.get("curriculum"))
        topic = str(curriculum.get("topic") or "").strip()
        ra_id = str(curriculum.get("ra") or "").strip()
        difficulty = str(curriculum.get("difficulty") or "").strip()
        cc_ids: list[str] = _string_list(curriculum.get("expected_causal_links"))

        # Exposure control: skip items in avoid_repetition_ids
        if qid in avoid_ids:
            continue

        # Compute ordinal priority score
        score = _PRIORITY_BASE

        # Misconception repair: max priority for persistent unresolved mc_ids
        # Misconception IDs are typically in the curriculum or feedback sections
        item_mc_ids = _item_mc_ids(item)
        for mc_id in item_mc_ids:
            if mc_id in review_mc:
                rv = review_mc[mc_id]
                if rv.get("persistence") and not rv.get("resolved"):
                    score = max(score, _PRIORITY_MAX)
                else:
                    score = max(score, _PRIORITY_HIGH)

        # Causal gap reinforcement
        for cc_id in cc_ids:
            if cc_id in review_cc:
                gap_prio = review_cc[cc_id]
                score = max(score, _PRIORITY_HIGH if gap_prio == "high" else _PRIORITY_STANDARD)

        # Reinforcement: weak topics / RAs
        if topic in reinforcement_ids:
            prio = reinforcement_ids[topic]
            if prio == "urgent":
                score = max(score, _PRIORITY_URGENT)
            elif prio == "high":
                score = max(score, _PRIORITY_HIGH)
            else:
                score = max(score, _PRIORITY_STANDARD)
        if ra_id in reinforcement_ids:
            prio = reinforcement_ids[ra_id]
            if prio == "urgent":
                score = max(score, _PRIORITY_URGENT)
            elif prio == "high":
                score = max(score, _PRIORITY_HIGH)
            else:
                score = max(score, _PRIORITY_STANDARD)

        # Progression: de-emphasize basic items for strong topics
        if topic in progression_ids or ra_id in progression_ids:
            if difficulty == "foundational":
                # Reduce repetition of foundational for ready-to-progress topics
                score = max(_PRIORITY_BASE, score - 10)

        # Challenge: boost distinction-level items for strong topics
        if topic in challenge_topic_ids and difficulty == "distinction":
            score = max(score, _PRIORITY_CHALLENGE)

        # Exposure variation: penalize topics already selected twice
        topic_count = used_topics.get(topic, 0)
        if topic_count >= 2:
            score = max(_PRIORITY_BASE, score - 15)

        question_priorities.append({
            "question_id": qid,
            "priority_score": score,
            "topic": topic,
            "ra_id": ra_id,
            "difficulty": difficulty,
        })

        used_topics[topic] = topic_count + 1

    # Sort descending by priority_score, stable
    question_priorities.sort(key=lambda x: -x["priority_score"])

    # Collect WWJ remediation paths for review misconceptions
    remediation_paths = _build_remediation_paths(review_mc)

    return {
        "session_mode": session_mode,
        "target_size": target_size,
        "question_priorities": question_priorities,
        "reinforcement_rationale": _reinforcement_rationale(reinforcement_targets),
        "progression_rationale": _progression_rationale(progression_targets),
        "challenge_rationale": _challenge_rationale(challenge_targets),
        "exposure_balancing_rationale": {
            "avoided_count": sum(1 for item in eligibility_pool if _item_id(item) in avoid_ids),
            "avoid_repetition_ids": sorted(avoid_ids),
        },
        "remediation_paths": remediation_paths,
        "governance": _governance(),
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _resolve_mode_size(session_mode: str, pool: list[dict[str, Any]]) -> int:
    target = SESSION_MODE_SIZES.get(session_mode, 10)
    return min(target, len(pool))


def _item_id(item: dict[str, Any]) -> str:
    master_id = str(item.get("master_item_id") or "").strip()
    if master_id:
        return master_id
    return str(item.get("source_question_id") or item.get("question_id") or "").strip()


def _item_mc_ids(item: dict[str, Any]) -> list[str]:
    """Extract MC IDs from item feedback or curriculum sections."""
    mc_ids: list[str] = []
    feedback = item.get("feedback") or {}
    if isinstance(feedback, dict):
        for key in ("mc_id", "mc_ids"):
            value = feedback.get(key)
            if isinstance(value, str) and value.strip():
                mc_ids.append(value.strip())
            elif isinstance(value, list):
                mc_ids.extend(str(v) for v in value if str(v).strip())
    curriculum = item.get("curriculum") or {}
    if isinstance(curriculum, dict):
        for key in ("mc_id", "mc_ids"):
            value = curriculum.get(key)
            if isinstance(value, str) and value.strip():
                mc_ids.append(value.strip())
            elif isinstance(value, list):
                mc_ids.extend(str(v) for v in value if str(v).strip())
    return list(dict.fromkeys(mc_ids))


def _build_remediation_paths(review_mc: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    paths: list[dict[str, Any]] = []
    for mc_id, rv in review_mc.items():
        if rv.get("resolved"):
            continue
        path = get_remediation_path(mc_id)
        paths.append({
            "mc_id": mc_id,
            "wwj_chunks": path["wwj_chunks"],
            "availability": path["availability"],
            "remediation_message": path["remediation_message"],
        })
    return paths


def _reinforcement_rationale(targets: list[dict[str, Any]]) -> dict[str, Any]:
    urgent = [t for t in targets if t.get("reinforcement_priority") == "urgent"]
    high = [t for t in targets if t.get("reinforcement_priority") == "high"]
    return {
        "urgent_count": len(urgent),
        "high_count": len(high),
        "standard_count": len(targets) - len(urgent) - len(high),
        "target_ids": [str(t.get("id") or "") for t in targets],
    }


def _progression_rationale(targets: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "ready_for_challenge_count": len(targets),
        "target_ids": [str(t.get("id") or "") for t in targets],
    }


def _challenge_rationale(targets: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "challenge_candidate_count": len(targets),
        "target_ids": [str(t.get("topic") or t.get("id") or "") for t in targets],
    }


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(v).strip() for v in value if str(v).strip()]


def _mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


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

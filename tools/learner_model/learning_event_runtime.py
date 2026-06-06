"""Learning Event Runtime — connects SBA and OR attempts to the LES/cognitive-map pipeline.

Three integration connections closed by this module:

  1. _remediation_route() → wwj_remediation.get_remediation_path()
     WWJ chunks now enter the pipeline when an SBA distractor triggers a misconception.

  2. build_next_session_signals(memory, les) reads both memory AND live LES signals.
     Adaptive Composer sees per-node persistence and causal_strength, not just memory hits.

  3. process_open_response_attempt() connects evaluate_open_response() to LES/cognitive_map.
     OR attempts update causal_chain_signals, difficult_causal_chains, and mc signals.

Governance invariants (all permanently False):
  safe_for_examiner, examiner_scoring_allowed, uses_llm, uses_api,
  uses_embeddings, uses_vector_db, cloud_services_active.

No writes to disk — callers are responsible for persistence.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from tools.learner_model.causal_runtime import update_les_causal
from tools.learner_model.misconception_runtime import process_sba_outcome
from tools.learner_model.open_response_evaluator import evaluate_open_response
from tools.learner_model.wwj_remediation import get_remediation_path


# ---------------------------------------------------------------------------
# SBA pipeline
# ---------------------------------------------------------------------------

def process_question_attempt(
    *,
    student_answer: str,
    question_id: str,
    session_id: str,
    mode: str,
    timestamp: str,
    question_item: dict[str, Any],
    memory: dict[str, Any],
    les: dict[str, Any],
    mc_id: str | None = None,
) -> dict[str, Any]:
    """Process one SBA question attempt through the full LES/cognitive-map pipeline.

    Args:
        student_answer: The answer option chosen by the student (e.g. "B").
        question_id:    Unique question identifier.
        session_id:     Opaque session identifier for persistence tracking.
        mode:           Session mode label (e.g. "practice", "timed").
        timestamp:      ISO-8601 timestamp string.
        question_item:  SBA question dict with at least a ``correct_answer`` field.
        memory:         Current pedagogical memory dict (not mutated).
        les:            Current LES dict (not mutated).
        mc_id:          Optional MC_ID linked to the distractor the student chose.
                        Caller is responsible for the distractor → MC_ID mapping.

    Returns:
        Dict with keys: attempt, diagnostic_outcome, formative_event, cognitive_map,
        cognitive_map_change_set, les, les_change_set, emitted_signals,
        next_session_signals, governance.
    """
    correct = str(question_item.get("correct_answer") or "").strip().upper()
    student = str(student_answer or "").strip().upper()
    outcome = "correct" if student == correct else "incorrect"

    updated_les = deepcopy(les)
    all_signals: list[str] = []

    if mc_id:
        updated_les, mc_signals = process_sba_outcome(
            les,
            mc_id=mc_id,
            outcome=outcome,
            session_id=session_id,
        )
        all_signals.extend(mc_signals)

    diagnostic = build_diagnostic_outcome(
        outcome=outcome,
        question_id=question_id,
        mc_id=mc_id,
    )

    les_change_set = _diff_dicts(les, updated_les)

    updated_memory = deepcopy(memory)
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


def build_diagnostic_outcome(
    *,
    outcome: str,
    question_id: str,
    mc_id: str | None,
) -> dict[str, Any]:
    """Build the diagnostic section of an SBA attempt result."""
    return {
        "outcome": outcome,
        "question_id": question_id,
        "mc_id": mc_id,
        "remediation_routing": _remediation_route(mc_id=mc_id, outcome=outcome),
    }


def _remediation_route(*, mc_id: str | None, outcome: str) -> dict[str, Any] | None:
    """Return a WWJ remediation path when a misconception is triggered.

    Only performs the lookup when mc_id is known and the outcome is incorrect.
    Always sets remediation_source='wwj_lookup' when a lookup is attempted.
    Returns None when no mc_id is linked.
    """
    if not mc_id:
        return None
    if outcome != "incorrect":
        return {
            "mc_id": mc_id,
            "remediation_available": False,
            "remediation_message": "",
            "wwj_chunks": [],
            "remediation_source": "none",
        }
    path = get_remediation_path(mc_id)
    return {
        "mc_id": mc_id,
        "remediation_available": path["availability"] == "available",
        "remediation_message": path["remediation_message"],
        "wwj_chunks": path["wwj_chunks"],
        "remediation_source": "wwj_lookup",
    }


# ---------------------------------------------------------------------------
# Next-session signals
# ---------------------------------------------------------------------------

def build_next_session_signals(
    memory: dict[str, Any],
    les: dict[str, Any],
) -> dict[str, Any]:
    """Build next-session planning signals from both memory and live LES.

    Reads from memory:
      - recurrent_misconceptions — hit counts (pre-existing signal)
      - difficult_causal_chains  — hit counts (pre-existing signal)

    Reads from LES (new connections):
      - misconception_signals    → detection_count per mc_id
      - misconception_sessions   → session_ids for cross-session persistence
      - misconception_resolution → resolved flag per mc_id
      - causal_chain_signals     → exposure_count, demonstrated_count per cc_id
      - causal_strength          → "superficial"|"developing"|"strong" per cc_id

    Returns:
      - review_topics: topics from memory with at least one misconception hit
      - misconception_repair_candidate: [{mc_id, persistence, resolved, priority}]
        Excludes resolved misconceptions.
        priority="high" when persistence=True and resolved=False.
      - causal_chain_reinforcement_candidate: [{cc_id, causal_strength, gap_priority}]
        gap_priority="high" when strength="superficial" and exposure_count > 0.
    """
    rec_mc = dict(memory.get("recurrent_misconceptions") or {})

    review_topics = [
        mc_id for mc_id, entry in rec_mc.items()
        if isinstance(entry, dict) and int(entry.get("hits", 0)) > 0
    ]

    # --- Misconception repair candidates from LES ---
    mc_signals = dict(les.get("misconception_signals") or {})
    mc_resolution = dict(les.get("misconception_resolution") or {})
    mc_sessions = dict(les.get("misconception_sessions") or {})

    repair_candidates: list[dict[str, Any]] = []
    for mc_id, sig in mc_signals.items():
        if not isinstance(sig, dict):
            continue
        if int(sig.get("detection_count", 0)) == 0:
            continue

        sess = mc_sessions.get(mc_id, {})
        session_ids = sess.get("session_ids", []) if isinstance(sess, dict) else []
        persistence = len(session_ids) > 1

        res = mc_resolution.get(mc_id, {})
        resolved = bool(res.get("resolved", False)) if isinstance(res, dict) else False

        if resolved:
            continue

        priority = "high" if persistence else "standard"
        repair_candidates.append({
            "mc_id": mc_id,
            "persistence": persistence,
            "resolved": resolved,
            "priority": priority,
        })

    # --- Causal chain reinforcement candidates from LES ---
    cc_signals = dict(les.get("causal_chain_signals") or {})
    causal_strength = dict(les.get("causal_strength") or {})

    reinforcement_candidates: list[dict[str, Any]] = []
    for cc_id, sig in cc_signals.items():
        if not isinstance(sig, dict):
            continue
        exposure = int(sig.get("exposure_count", 0))
        if exposure == 0:
            continue
        strength = str(causal_strength.get(cc_id, "superficial"))
        gap_priority = "high" if strength == "superficial" else "standard"
        reinforcement_candidates.append({
            "cc_id": cc_id,
            "causal_strength": strength,
            "gap_priority": gap_priority,
        })

    return {
        "review_topics": review_topics,
        "misconception_repair_candidate": repair_candidates,
        "causal_chain_reinforcement_candidate": reinforcement_candidates,
    }


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

    # 4. Process mc_ids_relevant as misconception signals
    # A mc_id is treated as "incorrect" when any targeted chain is absent;
    # "correct" only when all targeted chains are present.
    any_absent = bool(chains_absent)
    all_present = not any_absent and bool(cc_ids_targeted)
    for mc_id in mc_ids_relevant:
        mc_outcome = "correct" if all_present else "incorrect"
        updated_les, mc_sigs = process_sba_outcome(
            updated_les,
            mc_id=mc_id,
            outcome=mc_outcome,
            session_id=session_id,
        )
        all_signals.extend(mc_sigs)

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
# Helpers
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

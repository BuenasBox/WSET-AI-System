"""Generate adaptive session payload for the Adaptive Session UI.

Reads:  knowledge/nazareth/epistemic_state.json
        knowledge/nazareth/pedagogical_memory.json
Calls:  build_next_session_signals → consume_adaptive_signals →
        compose_adaptive_session_plan → select_sba_session_items
Writes: frontend/session_data/session_payload.json

Governance invariants (permanently False):
  safe_for_examiner, examiner_scoring_allowed.
  training_item_only: True.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Ensure project root is on sys.path when run as a script.
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from tools.learner_model.learning_event_runtime import build_next_session_signals
from tools.learner_model.adaptive_signal_consumer import consume_adaptive_signals
from tools.learner_model.adaptive_composer import (
    compose_adaptive_session_plan,
    SESSION_MODE_SIZES,
)
from tools.question_generation.sba_session_composer import (
    load_master_bank,
    select_sba_session_items,
)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

LES_PATH = _PROJECT_ROOT / "knowledge" / "nazareth" / "epistemic_state.json"
MEMORY_PATH = _PROJECT_ROOT / "knowledge" / "nazareth" / "pedagogical_memory.json"
OUTPUT_DIR = _PROJECT_ROOT / "frontend" / "session_data"
OUTPUT_PATH = OUTPUT_DIR / "session_payload.json"

_VALID_MODES = set(SESSION_MODE_SIZES.keys())

# ---------------------------------------------------------------------------
# Governance block — never mutate these values
# ---------------------------------------------------------------------------

_GOVERNANCE: dict[str, Any] = {
    "safe_for_examiner": False,
    "examiner_scoring_allowed": False,
    "training_item_only": True,
}


# ---------------------------------------------------------------------------
# LES signal extraction
# ---------------------------------------------------------------------------


def _active_misconceptions(les: dict) -> list[str]:
    """mc_ids with at least one detection that are not yet resolved."""
    signals = les.get("misconception_signals") or {}
    resolution = les.get("misconception_resolution") or {}
    return [
        mc_id
        for mc_id, sig in signals.items()
        if isinstance(sig, dict) and int(sig.get("detection_count", 0)) > 0
        and not (resolution.get(mc_id) or {}).get("resolved", False)
    ]


def _causal_gaps(les: dict) -> list[str]:
    """cc_ids whose causal_strength is 'superficial'."""
    return [
        cc_id
        for cc_id, strength in (les.get("causal_strength") or {}).items()
        if strength == "superficial"
    ]


def _strong_topics(les: dict) -> list[str]:
    return [
        topic
        for topic, sig in (les.get("topic_signals") or {}).items()
        if isinstance(sig, dict) and sig.get("confidence_level") == "high"
    ]


def _weak_topics(les: dict) -> list[str]:
    return [
        topic
        for topic, sig in (les.get("topic_signals") or {}).items()
        if isinstance(sig, dict)
        and sig.get("confidence_level") in {"low", "not_recorded"}
    ]


# ---------------------------------------------------------------------------
# Mission briefing construction
# ---------------------------------------------------------------------------


def _infer_training_type(
    adaptive_signals: dict, les: dict
) -> str:
    """Classify the session as one of: refuerzo, diagnostico, desafio, reparacion."""
    review = adaptive_signals.get("review_targets") or []
    reinforcement = adaptive_signals.get("reinforcement_targets") or []
    progression = adaptive_signals.get("progression_targets") or []

    repair_count = sum(1 for t in review if t.get("type") == "misconception")
    if repair_count >= 2:
        return "reparacion"

    topic_signals = les.get("topic_signals") or {}
    if not topic_signals:
        return "diagnostico"

    if len(progression) > max(len(reinforcement), 1):
        return "desafio"

    return "refuerzo"


def _build_session_objective(
    strong: list[str],
    weak: list[str],
    active_mc: list[str],
    training_type: str,
) -> str:
    """Generate a short Spanish sentence describing the session focus."""
    if training_type == "diagnostico":
        return "Sesión de diagnóstico inicial — evaluando tu estado cognitivo en WSET L3."

    parts: list[str] = []

    if weak:
        topics_str = " y ".join(weak[:2])
        parts.append(f"Refuerzo de {topics_str}")

    if strong:
        strong_str = " y ".join(strong[:2])
        complement = f"ya dominas {strong_str}"
        if parts:
            parts[0] = parts[0] + f" ({complement})"
        else:
            parts.append(complement[0].upper() + complement[1:])

    if active_mc:
        n = len(active_mc)
        parts.append(
            f"corrección de {'un patrón cognitivo activo' if n == 1 else f'{n} patrones cognitivos activos'}"
        )

    if training_type == "desafio":
        parts.append("Vamos a profundidad, comparación y causalidad")
    elif training_type == "reparacion":
        parts.append("Sesión de reparación de brechas cognitivas")

    if not parts:
        return "Sesión de entrenamiento adaptativo WSET L3."

    return ". ".join(s[0].upper() + s[1:] for s in parts) + "."


# ---------------------------------------------------------------------------
# Challenge-type inference
# ---------------------------------------------------------------------------


def _infer_challenge_type(
    item: dict,
    active_mc_ids: set[str],
    causal_gap_ids: set[str],
) -> str:
    curriculum = item.get("curriculum") or {}
    mc_ids: list[str] = list(curriculum.get("mc_ids") or [])
    causal_links: list[str] = list(curriculum.get("expected_causal_links") or [])
    difficulty: str = str(curriculum.get("difficulty") or "")

    if mc_ids and set(mc_ids) & active_mc_ids:
        return "misconception_repair"

    if causal_links and causal_gap_ids:
        return "causal_chain"

    if difficulty == "distinction":
        return "challenge"

    if causal_links:
        return "reasoning"

    return "recall"


# ---------------------------------------------------------------------------
# Question list construction
# ---------------------------------------------------------------------------


def _build_feedback(item: dict) -> dict[str, Any]:
    source = item.get("source_content") or {}
    curriculum = item.get("curriculum") or {}

    explanation: str = (
        source.get("explanation")
        or source.get("rationale")
        or ""
    )
    if not explanation:
        correct_text: str = (
            source.get("correct_answer_text")
            or source.get("correct_answer")
            or ""
        )
        topic: str = curriculum.get("topic") or "el concepto"
        if correct_text:
            explanation = (
                f"La lógica correcta en {topic} apunta a este fundamento: "
                f"{correct_text}. "
                "Analiza el mecanismo causal para consolidar el razonamiento."
            )
        else:
            explanation = (
                f"Revisa los fundamentos de {topic} en tu material de referencia WSET L3."
            )

    misconception_note: str = source.get("misconception_note") or ""
    wwj_available: bool = bool(
        item.get("wwj_fragment") or item.get("wwj_remediation")
    )

    return {
        "explanation": explanation,
        "misconception_note": misconception_note,
        "wwj_available": wwj_available,
    }


def _build_questions(
    selected_items: list[dict],
    question_priorities: list[dict],
    active_mc_ids: set[str],
    causal_gap_ids: set[str],
) -> list[dict[str, Any]]:
    priority_map: dict[str, int] = {
        str(p.get("question_id") or ""): int(p.get("priority_score", 0))
        for p in question_priorities
        if p.get("question_id")
    }

    questions: list[dict[str, Any]] = []
    for item in selected_items:
        qid = str(item.get("master_item_id") or "")
        curriculum = item.get("curriculum") or {}
        source = item.get("source_content") or {}

        options: dict[str, str] = source.get("options") or {}
        correct: str = (
            source.get("correct_answer_letter")
            or source.get("correct_answer")
            or ""
        )

        questions.append(
            {
                "question_id": qid,
                "priority_score": priority_map.get(qid, 0),
                "stem": item.get("stem") or "",
                "options": options,
                "correct_answer": correct,
                "topic": curriculum.get("topic") or "",
                "ra_id": curriculum.get("ra") or "",
                "difficulty": curriculum.get("difficulty") or "",
                "challenge_type": _infer_challenge_type(
                    item, active_mc_ids, causal_gap_ids
                ),
                "feedback": _build_feedback(item),
            }
        )

    return questions


def _signals_summary(adaptive_signals: dict) -> dict[str, int]:
    reinforcement = adaptive_signals.get("reinforcement_targets") or []
    progression = adaptive_signals.get("progression_targets") or []
    review = adaptive_signals.get("review_targets") or []
    avoid = adaptive_signals.get("avoid_repetition_ids") or []

    repair_count = sum(
        1 for t in review if t.get("type") == "misconception"
    )

    return {
        "reinforcement_count": len(reinforcement),
        "progression_count": len(progression),
        "repair_count": repair_count,
        "avoidance_count": len(avoid),
    }


# ---------------------------------------------------------------------------
# Main generation function
# ---------------------------------------------------------------------------


def generate(session_mode: str = "EXPRESS_10") -> dict[str, Any]:
    """Generate and return the full adaptive session payload dict."""
    if session_mode not in _VALID_MODES:
        raise ValueError(
            f"Invalid session_mode '{session_mode}'. "
            f"Valid options: {sorted(_VALID_MODES)}"
        )

    # 1. Load learner files.
    les: dict = json.loads(LES_PATH.read_text(encoding="utf-8"))
    memory: dict = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))

    # 2. Adaptive signals pipeline.
    next_signals = build_next_session_signals(memory, les)
    adaptive_signals = consume_adaptive_signals(next_signals, les, memory)

    # 3. Load master bank and build full eligibility pool.
    master_bank = load_master_bank()
    collection_ids: set[str] = set(
        (master_bank.get("collections") or {}).get("public_lab", [])
    )
    eligibility_pool = [
        item
        for item in master_bank.get("items", [])
        if isinstance(item, dict)
        and item.get("master_item_id") in collection_ids
        and item.get("question_type") == "single_best_answer"
    ]

    # 4. Compose adaptive session plan.
    plan = compose_adaptive_session_plan(
        session_mode,
        eligibility_pool,
        {},  # diagnostic_blueprint — informational, not used for scoring
        adaptive_signals,
    )

    # 5. Select final items (priority-ordered, deduplicated).
    selected_items = select_sba_session_items(
        master_bank,
        collection="public_lab",
        question_priorities=plan["question_priorities"],
        session_size=plan["target_size"],
    )

    # 6. Build mission briefing.
    active_mc_list = _active_misconceptions(les)
    causal_gap_list = _causal_gaps(les)
    strong = _strong_topics(les)
    weak = _weak_topics(les)
    training_type = _infer_training_type(adaptive_signals, les)

    mission_briefing = {
        "strong_areas": strong,
        "weak_areas": weak,
        "active_misconceptions": active_mc_list,
        "causal_gaps": causal_gap_list,
        "session_objective": _build_session_objective(
            strong, weak, active_mc_list, training_type
        ),
        "training_type": training_type,
    }

    # 7. Build question list.
    questions = _build_questions(
        selected_items,
        plan["question_priorities"],
        set(active_mc_list),
        set(causal_gap_list),
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "session_mode": session_mode,
        "target_size": plan["target_size"],
        "mission_briefing": mission_briefing,
        "questions": questions,
        "adaptive_signals_summary": _signals_summary(adaptive_signals),
        "governance": _GOVERNANCE,
    }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate adaptive session payload for the Adaptive Session UI.\n"
            "Output: frontend/session_data/session_payload.json"
        )
    )
    parser.add_argument(
        "--mode",
        default="EXPRESS_10",
        choices=sorted(_VALID_MODES),
        metavar="MODE",
        help=f"Session mode. Options: {sorted(_VALID_MODES)} (default: EXPRESS_10)",
    )
    parser.add_argument(
        "--output",
        default=str(OUTPUT_PATH),
        help="Output file path (default: frontend/session_data/session_payload.json)",
    )
    args = parser.parse_args()

    print(f"[generate_session_payload] mode={args.mode}")
    payload = generate(args.mode)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    b = payload["mission_briefing"]
    print(f"  Written   : {out}")
    print(f"  Questions : {len(payload['questions'])} / {payload['target_size']}")
    print(f"  Training  : {b['training_type']}")
    print(f"  Weak areas: {b['weak_areas']}")
    print(f"  Misconc.  : {b['active_misconceptions']}")
    print(f"  Causal gap: {b['causal_gaps']}")
    print(f"  Governance: {payload['governance']}")


if __name__ == "__main__":
    main()

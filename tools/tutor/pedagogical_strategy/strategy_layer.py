"""Pedagogical Strategy Layer — integration facade (gated, metadata-only)."""

from __future__ import annotations
from typing import Any
from .mode_selector import select_pedagogical_strategy

ENABLE_PEDAGOGICAL_STRATEGY_LAYER: bool = False

_INERT_GOVERNANCE: dict[str, bool] = {
    "safe_for_examiner": False,
    "examiner_scoring_allowed": False,
    "uses_llm": False,
    "uses_api": False,
    "uses_embeddings": False,
    "uses_vector_db": False,
}


def build_pedagogical_strategy(
    context_package=None,
    tutor_role=None,
    tutor_mode=None,
    extra_context=None,
    learner_confidence=None,
    exam_days_remaining=None,
    learning_goal=None,
    recent_error_type=None,
    strategic_plan=None,
):
    """Build a StrategyDirective from contextual signals.

    Gate off -> {"strategy_active": False, "governance": {...}}
    Gate on  -> full StrategyDirective with function_weights, derived signals,
                traceability, and governance (all flags False).

    Convenience params (learner_confidence, exam_days_remaining, learning_goal,
    recent_error_type) are merged into extra_context; explicit extra_context wins.

    strategic_plan: optional dict from the orchestrator strategic_planner output.
    Signals from strategic_plan are advisory-only (planning_confidence > 0.1 required).

    Does NOT modify context_package. Does NOT import answer_builder/orchestrator.
    """
    if not ENABLE_PEDAGOGICAL_STRATEGY_LAYER:
        return _inert_directive()

    merged = {}
    if learner_confidence is not None:
        merged["learner_confidence"] = learner_confidence
    if exam_days_remaining is not None:
        merged["exam_days_remaining"] = exam_days_remaining
    if learning_goal is not None:
        merged["learning_goal"] = learning_goal
    if recent_error_type is not None:
        merged["recent_error_type"] = recent_error_type
    if extra_context:
        merged.update(extra_context)

    signals = _extract_signals(context_package, merged or None, strategic_plan=strategic_plan)
    directive = select_pedagogical_strategy(
        tutor_role=tutor_role,
        tutor_mode=tutor_mode,
        learner_confidence=signals.get("learner_confidence"),
        exam_days_remaining=signals.get("exam_days_remaining"),
        learning_goal=signals.get("learning_goal"),
        recent_error_type=signals.get("recent_error_type"),
    )
    directive["strategy_active"] = True
    directive["traceability"] = {
        "profile_source": directive.get("source", "unknown"),
        "rules_fired_count": len(directive.get("rules_applied", [])),
        "evidence_required": True,
        "official_scoring": False,
    }
    return directive


def is_strategy_active():
    """Return True if the strategy layer gate is enabled."""
    return ENABLE_PEDAGOGICAL_STRATEGY_LAYER


def _inert_directive():
    return {"strategy_active": False, "governance": dict(_INERT_GOVERNANCE)}


def _extract_signals(context_package, extra_context, strategic_plan=None):
    """Extract learner signals. extra_context takes precedence. Never mutates inputs.

    Connection A: reads advisory signals from strategic_plan if provided
    (planning_confidence > 0.1 required; never overwrites explicit signals).
    """
    signals = {}
    if context_package:
        les = context_package.get("learner_state_context") or {}
        memory = les.get("pedagogical_memory") or {}
        mastery = str(les.get("mastery") or les.get("current_mastery") or "").lower()
        if mastery in {"low", "beginner", "weak"}:
            signals["learner_confidence"] = "low"
        elif mastery in {"high", "advanced", "strong"}:
            signals["learner_confidence"] = "high"
        goal = memory.get("learning_goal")
        if goal:
            signals["learning_goal"] = str(goal)
    # Connection A: advisory signals from strategic_plan (never overwrite explicit signals)
    if strategic_plan and isinstance(strategic_plan, dict):
        sp_conf = float(strategic_plan.get("planning_confidence") or 0.0)
        if sp_conf > 0.1 and "learning_goal" not in signals:
            sp_diff = strategic_plan.get("difficulty_progression")
            if sp_diff == "escalate":
                signals["learning_goal"] = "distinction"
    if extra_context:
        for key in ("learner_confidence", "exam_days_remaining",
                    "learning_goal", "recent_error_type"):
            if key in extra_context and extra_context[key] is not None:
                signals[key] = extra_context[key]
    return signals

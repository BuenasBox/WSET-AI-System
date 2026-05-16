"""Deterministic adaptive scaffolding policy for the local Tutor."""

from __future__ import annotations

from typing import Any


def select_scaffolding_policy(
    mastery_probability: float | None = None,
    cognitive_load: str = "medium",
    urgency: str = "medium",
    misconception_severity: str = "medium",
) -> dict[str, Any]:
    """Select a Tutor scaffolding act without scoring or LLM calls."""
    mastery = _clamp(mastery_probability if mastery_probability is not None else 0.5)
    severity = str(misconception_severity or "medium").lower()
    load = str(cognitive_load or "medium").lower()
    urgency = str(urgency or "medium").lower()
    if severity in {"high", "critical"} or urgency == "high":
        act = "direct_correction"
    elif mastery < 0.35:
        act = "guided_explanation"
    elif load == "high":
        act = "hint"
    elif mastery >= 0.75 and urgency == "low":
        act = "compressed_reinforcement"
    else:
        act = "socratic_questioning"
    return {
        "scaffolding_act": act,
        "mastery_probability": round(mastery, 3),
        "cognitive_load": load,
        "urgency": urgency,
        "misconception_severity": severity,
        "governance": {
            "safe_for_examiner": False,
            "examiner_scoring_allowed": False,
            "uses_llm": False,
            "uses_api": False,
        },
    }


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))

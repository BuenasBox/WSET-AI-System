"""Deterministic pedagogical strategy selector."""

from __future__ import annotations
from typing import Any
from .profiles import ALLOWED_FUNCTIONS, get_profile

FUNCTION_MIN_WEIGHT: float = 0.02
HOST_MIN_WEIGHT: float = 0.08

ADJUSTMENT_RULES = [
    {
        "rule_id": "exam_imminent",
        "condition_field": "exam_days_remaining",
        "condition_op": "lte",
        "condition_value": 14,
        "deltas": {"challenger": 0.15, "critic": 0.10, "host": -0.05,
                   "storyteller": -0.10, "cartographer": -0.05, "scientist": -0.05},
        "rationale": "Exam within 14 days: maximise challenge and critical pressure.",
    },
    {
        "rule_id": "exam_approaching",
        "condition_field": "exam_days_remaining",
        "condition_op": "range_hi_exclusive",
        "condition_value": (14, 60),
        "deltas": {"scientist": 0.10, "challenger": 0.08, "storyteller": -0.10,
                   "host": -0.04, "cartographer": -0.02, "critic": -0.02},
        "rationale": "Exam within 60 days (>14): increase analytical rigour.",
    },
    {
        "rule_id": "low_confidence",
        "condition_field": "learner_confidence",
        "condition_op": "in_set",
        "condition_value": {"low", "baja"},
        "deltas": {"host": 0.15, "challenger": -0.10, "critic": -0.05,
                   "storyteller": 0.05, "scientist": -0.03, "cartographer": -0.02},
        "rationale": "Low learner confidence: prioritise support, reduce adversarial pressure.",
    },
    {
        "rule_id": "causal_gap",
        "condition_field": "recent_error_type",
        "condition_op": "eq",
        "condition_value": "causal_gap",
        "deltas": {"scientist": 0.15, "cartographer": 0.05, "storyteller": -0.10,
                   "host": -0.05, "critic": -0.03, "challenger": -0.02},
        "rationale": "Causal gap error: activate scientist for mechanism explanation.",
    },
    {
        "rule_id": "regional_confusion",
        "condition_field": "recent_error_type",
        "condition_op": "eq",
        "condition_value": "regional_confusion",
        "deltas": {"cartographer": 0.20, "scientist": 0.05, "storyteller": -0.10,
                   "host": -0.08, "critic": -0.04, "challenger": -0.03},
        "rationale": "Regional confusion: activate cartographer for conceptual geography.",
    },
    {
        "rule_id": "vague_answer",
        "condition_field": "recent_error_type",
        "condition_op": "eq",
        "condition_value": "vague_answer",
        "deltas": {"critic": 0.15, "challenger": 0.05, "storyteller": -0.10,
                   "host": -0.05, "cartographer": -0.03, "scientist": -0.02},
        "rationale": "Vague answer: activate critic for precision demands.",
    },
    {
        "rule_id": "memorization_without_reasoning",
        "condition_field": "recent_error_type",
        "condition_op": "eq",
        "condition_value": "memorization_without_reasoning",
        "deltas": {"challenger": 0.12, "scientist": 0.12, "storyteller": -0.10,
                   "host": -0.08, "cartographer": -0.03, "critic": -0.03},
        "rationale": "Memorisation without reasoning: challenge assumptions and build causal chains.",
    },
    {
        "rule_id": "distinction_goal",
        "condition_field": "learning_goal",
        "condition_op": "eq",
        "condition_value": "distinction",
        "deltas": {"scientist": 0.10, "critic": 0.10, "challenger": 0.08,
                   "storyteller": -0.15, "host": -0.08, "cartographer": -0.05},
        "rationale": "Distinction goal: maximise analytical rigour.",
    },
]


def select_pedagogical_strategy(
    tutor_role=None,
    tutor_mode=None,
    learner_confidence=None,
    exam_days_remaining=None,
    learning_goal=None,
    recent_error_type=None,
):
    """Return a deterministic StrategyDirective dict."""
    ctx = {}
    if learner_confidence is not None:
        ctx["learner_confidence"] = learner_confidence
    if exam_days_remaining is not None:
        ctx["exam_days_remaining"] = exam_days_remaining
    if learning_goal is not None:
        ctx["learning_goal"] = learning_goal
    if recent_error_type is not None:
        ctx["recent_error_type"] = recent_error_type

    profile = get_profile(tutor_role=tutor_role, tutor_mode=tutor_mode)
    weights = dict(profile["functions"])

    rules_applied = []
    for rule in ADJUSTMENT_RULES:
        if _rule_applies(rule, ctx):
            rules_applied.append(rule["rule_id"])
            for fn, delta in rule["deltas"].items():
                weights[fn] = weights.get(fn, 0.0) + delta

    weights = _clamp_and_normalise(weights)

    return {
        "profile_id": profile["profile_id"],
        "function_weights": weights,
        "feedback_intensity": _feedback_intensity(weights),
        "preferred_question_type": _preferred_question_type(weights),
        "remediation_style": _remediation_style(weights),
        "causal_depth_required": _causal_depth_required(weights),
        "emotional_support_level": _emotional_support_level(weights),
        "challenge_level": _challenge_level(weights),
        "rules_applied": rules_applied,
        "source": profile["source"],
        "governance": {
            "safe_for_examiner": False,
            "examiner_scoring_allowed": False,
            "uses_llm": False,
            "uses_api": False,
            "uses_embeddings": False,
            "uses_vector_db": False,
        },
    }


# ---------------------------------------------------------------------------
# Rule evaluation
# ---------------------------------------------------------------------------

def _rule_applies(rule, ctx):
    field = rule["condition_field"]
    op = rule["condition_op"]
    threshold = rule["condition_value"]
    value = ctx.get(field)
    if value is None:
        return False
    if op == "lte":
        try:
            return float(value) <= float(threshold)
        except (TypeError, ValueError):
            return False
    if op == "range_hi_exclusive":
        lo, hi = threshold
        try:
            fv = float(value)
            return float(lo) < fv <= float(hi)
        except (TypeError, ValueError):
            return False
    if op == "in_set":
        return str(value).lower() in {s.lower() for s in threshold}
    if op == "eq":
        return str(value).lower() == str(threshold).lower()
    return False


# ---------------------------------------------------------------------------
# Weight manipulation — floor-preserving normalisation
# ---------------------------------------------------------------------------

def _clamp_and_normalise(weights):
    """Normalise to sum=1.0 while guaranteeing per-function floor constraints.

    Uses iterative redistribution: violators are raised to their floor,
    the deficit is stolen proportionally from the highest-weight functions.
    """
    floors = {fn: (HOST_MIN_WEIGHT if fn == "host" else FUNCTION_MIN_WEIGHT)
               for fn in ALLOWED_FUNCTIONS}

    working = {fn: max(0.0, weights.get(fn, 0.0)) for fn in ALLOWED_FUNCTIONS}

    for _ in range(20):
        total = sum(working.values())
        if total <= 0:
            working = dict(floors)
            break

        norm = {fn: working[fn] / total for fn in ALLOWED_FUNCTIONS}
        violations = {fn for fn in ALLOWED_FUNCTIONS if norm[fn] < floors[fn]}

        if not violations:
            return {fn: round(norm[fn], 6) for fn in ALLOWED_FUNCTIONS}

        deficit = sum(floors[fn] - norm[fn] for fn in violations)
        above = {fn: norm[fn] for fn in ALLOWED_FUNCTIONS if fn not in violations}
        above_total = sum(above.values())

        if above_total <= 0:
            working = dict(floors)
            break

        new_working = {}
        for fn in violations:
            new_working[fn] = floors[fn]
        for fn in above:
            steal = (above[fn] / above_total) * deficit
            new_working[fn] = max(floors[fn], above[fn] - steal)
        working = new_working

    total = sum(working.values())
    if total <= 0:
        n = len(ALLOWED_FUNCTIONS)
        return {fn: round(1.0 / n, 6) for fn in ALLOWED_FUNCTIONS}
    return {fn: round(working[fn] / total, 6) for fn in ALLOWED_FUNCTIONS}


# ---------------------------------------------------------------------------
# Signal derivation
# ---------------------------------------------------------------------------

def _feedback_intensity(weights):
    combined = weights.get("critic", 0.0) + weights.get("challenger", 0.0)
    if combined >= 0.40:
        return "high"
    if combined >= 0.20:
        return "medium"
    return "low"


def _preferred_question_type(weights):
    mapping = {
        "scientist": "causal",
        "cartographer": "contextual",
        "critic": "evaluative",
        "challenger": "adversarial",
        "storyteller": "narrative",
        "host": "reflective",
    }
    dominant = max(weights, key=lambda fn: weights.get(fn, 0.0))
    return mapping.get(dominant, "causal")


def _remediation_style(weights):
    mapping = {
        "scientist": "analytical",
        "cartographer": "contextual",
        "host": "scaffolded",
        "storyteller": "narrative",
        "critic": "direct",
        "challenger": "challenge",
    }
    dominant = max(weights, key=lambda fn: weights.get(fn, 0.0))
    return mapping.get(dominant, "scaffolded")


def _causal_depth_required(weights):
    w = weights.get("scientist", 0.0)
    if w >= 0.35:
        return "deep"
    if w >= 0.20:
        return "standard"
    return "minimal"


def _emotional_support_level(weights):
    w = weights.get("host", 0.0)
    if w >= 0.25:
        return "high"
    if w >= 0.15:
        return "medium"
    return "low"


def _challenge_level(weights):
    w = weights.get("challenger", 0.0)
    if w >= 0.20:
        return "high"
    if w >= 0.10:
        return "medium"
    return "low"

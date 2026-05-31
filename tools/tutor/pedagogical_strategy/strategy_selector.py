"""Deterministic pedagogical strategy selector — ARCHIVED / LEGACY.

STATUS: Archived. This module is NOT the active selector.
Active selector: tools/tutor/pedagogical_strategy/mode_selector.py
                 (imported by strategy_layer.py as select_pedagogical_strategy)

This module was an experimental v2 rewrite with:
  - HOST_FLOOR = 0.05 (vs HOST_MIN_WEIGHT = 0.08 in mode_selector)
  - Fewer deltas per rule (simpler adjustments)
  - _round_and_correct() for rounding-drift correction
  - Different feedback_intensity scale (challenging/firm/moderate/gentle)
  - Missing causal_depth_required and challenge_level derivations

Decision (PSL baseline commit, 2026-05-31):
  Keep mode_selector.py as the single active selector. strategy_selector.py
  is preserved for reference and tested via test_psl_strategy_selector.py,
  but must NOT be imported by strategy_layer.py or any production path.

Governance invariants (immutable):
  safe_for_examiner = False, examiner_scoring_allowed = False
  No LLM, no API, no embeddings, no vector DB.
  Same inputs -> same output always.
"""

from __future__ import annotations
from .profiles import ALLOWED_FUNCTIONS, get_profile

HOST_FLOOR: float = 0.05
FUNCTION_FLOOR: float = 0.02
CHALLENGER_LOW_CONF_FLOOR: float = 0.05

_ADJUSTMENT_RULES = [
    {
        "rule_id": "exam_high_urgency",
        "condition_field": "exam_days_remaining",
        "condition_op": "lte",
        "condition_value": 14,
        "deltas": {"challenger": +0.10, "critic": +0.10, "host": -0.10, "storyteller": -0.10},
    },
    {
        "rule_id": "exam_medium_urgency",
        "condition_field": "exam_days_remaining",
        "condition_op": "range_hi_exclusive",
        "condition_value": (14, 60),
        "deltas": {"scientist": +0.08, "challenger": +0.05, "storyteller": -0.08, "host": -0.05},
    },
    {
        "rule_id": "low_confidence",
        "condition_field": "learner_confidence",
        "condition_op": "in_set",
        "condition_value": {"low", "baja"},
        "deltas": {"host": +0.12, "challenger": -0.12},
    },
    {
        "rule_id": "causal_gap",
        "condition_field": "recent_error_type",
        "condition_op": "eq",
        "condition_value": "causal_gap",
        "deltas": {"scientist": +0.10},
    },
    {
        "rule_id": "regional_confusion",
        "condition_field": "recent_error_type",
        "condition_op": "eq",
        "condition_value": "regional_confusion",
        "deltas": {"cartographer": +0.10},
    },
    {
        "rule_id": "vague_answer",
        "condition_field": "recent_error_type",
        "condition_op": "eq",
        "condition_value": "vague_answer",
        "deltas": {"critic": +0.08},
    },
    {
        "rule_id": "memorization_without_reasoning",
        "condition_field": "recent_error_type",
        "condition_op": "eq",
        "condition_value": "memorization_without_reasoning",
        "deltas": {"challenger": +0.08, "scientist": +0.05},
    },
    {
        "rule_id": "distinction_goal",
        "condition_field": "learning_goal",
        "condition_op": "eq",
        "condition_value": "distinction",
        "deltas": {"scientist": +0.08, "critic": +0.08, "challenger": +0.06},
    },
]


def select_strategy(
    tutor_role=None,
    tutor_mode=None,
    learner_confidence=None,
    exam_days_remaining=None,
    learning_goal=None,
    recent_error_type=None,
):
    """Return a deterministic StrategyDirective dict."""
    signals = {k: v for k, v in {
        "learner_confidence": learner_confidence,
        "exam_days_remaining": exam_days_remaining,
        "learning_goal": learning_goal,
        "recent_error_type": recent_error_type,
    }.items() if v is not None}

    profile = get_profile(tutor_role=tutor_role, tutor_mode=tutor_mode)
    weights = {fn: profile["functions"].get(fn, 0.0) for fn in ALLOWED_FUNCTIONS}

    rules_applied = []
    for rule in _ADJUSTMENT_RULES:
        if _rule_applies(rule, signals):
            rules_applied.append(rule["rule_id"])
            for fn, delta in rule["deltas"].items():
                weights[fn] = weights.get(fn, 0.0) + delta

    challenger_floor = (
        CHALLENGER_LOW_CONF_FLOOR if "low_confidence" in rules_applied else FUNCTION_FLOOR
    )
    weights = _normalise(weights, challenger_floor=challenger_floor)

    return {
        "profile_id": profile["profile_id"],
        "function_weights": weights,
        "feedback_intensity": _feedback_intensity(weights),
        "preferred_question_type": _preferred_question_type(weights),
        "remediation_style": _remediation_style(weights),
        "emotional_support_level": _emotional_support_level(weights),
        "rules_applied": rules_applied,
        "governance": {
            "safe_for_examiner": False,
            "examiner_scoring_allowed": False,
            "uses_llm": False,
            "uses_api": False,
            "uses_embeddings": False,
            "uses_vector_db": False,
        },
    }


def _rule_applies(rule, signals):
    field, op, threshold = rule["condition_field"], rule["condition_op"], rule["condition_value"]
    value = signals.get(field)
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


def _normalise(weights, challenger_floor=None):
    """Renormalise to sum=1.0 with per-function floor constraints.

    Floors: host >= HOST_FLOOR, challenger >= challenger_floor,
    all others >= FUNCTION_FLOOR. Iterative redistribution (20 passes max),
    then _round_and_correct to eliminate accumulated rounding drift.
    """
    if challenger_floor is None:
        challenger_floor = FUNCTION_FLOOR

    floors = {}
    for fn in ALLOWED_FUNCTIONS:
        if fn == "host":
            floors[fn] = HOST_FLOOR
        elif fn == "challenger":
            floors[fn] = challenger_floor
        else:
            floors[fn] = FUNCTION_FLOOR

    working = {fn: max(0.0, weights.get(fn, 0.0)) for fn in ALLOWED_FUNCTIONS}

    for _ in range(20):
        total = sum(working.values())
        if total <= 0:
            working = dict(floors)
            break

        norm = {fn: working[fn] / total for fn in ALLOWED_FUNCTIONS}
        violations = {fn for fn in ALLOWED_FUNCTIONS if norm[fn] < floors[fn]}

        if not violations:
            return _round_and_correct(norm)

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
        return _round_and_correct({fn: 1.0 / n for fn in ALLOWED_FUNCTIONS})
    return _round_and_correct({fn: working[fn] / total for fn in ALLOWED_FUNCTIONS})


def _round_and_correct(weights):
    """Round to 6dp, then add residual to largest weight to guarantee sum==1.0.

    round(x, 6) over 6 values accumulates up to ~3e-6 error. Adding the
    residual directly (no re-round) to the largest-weight function eliminates
    this drift deterministically while keeping output stable.
    """
    rounded = {fn: round(v, 6) for fn, v in weights.items()}
    residual = 1.0 - sum(rounded.values())
    if residual != 0.0:
        largest = max(rounded, key=rounded.__getitem__)
        rounded[largest] = rounded[largest] + residual
    return rounded


def _feedback_intensity(weights):
    combined = weights.get("critic", 0.0) + weights.get("challenger", 0.0)
    if combined > 0.50:
        return "challenging"
    if combined > 0.40:
        return "firm"
    if combined > 0.30:
        return "moderate"
    return "gentle"


def _preferred_question_type(weights):
    mapping = {
        "cartographer": "regional",
        "scientist":    "causal",
        "host":         "open",
        "storyteller":  "narrative",
        "critic":       "evaluative",
        "challenger":   "adversarial",
    }
    dominant = max(ALLOWED_FUNCTIONS, key=lambda fn: weights.get(fn, 0.0))
    return mapping.get(dominant, "causal")


def _remediation_style(weights):
    ranked = sorted(ALLOWED_FUNCTIONS, key=lambda fn: weights.get(fn, 0.0), reverse=True)
    top1 = ranked[0]
    top2 = ranked[1] if len(ranked) > 1 else None
    if top1 == "scientist":
        return "causal_chain"
    if top1 == "cartographer":
        return "comparative" if top2 in {"scientist", "critic"} else "contextual"
    if top1 == "host":
        return "narrative" if top2 == "storyteller" else "contextual"
    if top1 == "storyteller":
        return "narrative"
    if top1 == "critic":
        return "causal_chain" if top2 == "scientist" else "contextual"
    if top1 == "challenger":
        return "causal_chain" if top2 == "scientist" else "comparative"
    return "contextual"


def _emotional_support_level(weights):
    w = weights.get("host", 0.0)
    if w >= 0.25:
        return "high"
    if w >= 0.15:
        return "medium"
    return "low"

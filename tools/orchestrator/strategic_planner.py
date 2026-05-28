"""Deterministic strategic pedagogical planner for the WSET-AI-System orchestrator.

Phase 1A — Planning module in isolation.

This module reasons over learner state signals (pedagogical memory + LES) to produce
a structured planning directive. It is:

  - Deterministic:      same inputs → same output (pass reference_date for time tests)
  - Side-effect-free:   reads only from its arguments, writes nothing, no I/O
  - Governance-clean:   output never contains safe_for_examiner or examiner fields
  - Import-isolated:    imports nothing from retrieval or answer_builder
  - Cold-start safe:    produces a conservative no-op plan when data is unavailable

This module does NOT yet drive retrieval or answer rendering. It produces a
structured dict that the orchestrator can attach to the context package for
downstream inspection. Integration into run_orchestrator() is Phase 1B.

Design philosophy
-----------------
All planning decisions are explicit lookup + threshold rules over structured
learner-state signals. No heuristics are hidden in prose logic. The thresholds
below are module-level constants and can be changed without touching the algorithm.
Changing a threshold is a deliberate, auditable, testable act.

The planner MUST NOT:
  - Generate freeform text
  - Call external services
  - Use randomness
  - Introduce governance authority
  - Override safe_for_examiner or any governance flag
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


# ---------------------------------------------------------------------------
# Thresholds — module-level for testability and auditability
# ---------------------------------------------------------------------------

# memory_summary["retention_risks"] items above this → review_topics
RETENTION_RISK_THRESHOLD: float = 0.55

# memory_summary["low_mastery_concepts"] items below this → review_topics
LOW_MASTERY_THRESHOLD: float = 0.45

# memory_summary["mastered_concepts"] uses this threshold at source (build_memory_summary)
MASTERY_THRESHOLD: float = 0.82

# recurrent_misconception.persistence at or above this → misconception_focus
MISCONCEPTION_PERSISTENCE_THRESHOLD: float = 0.40

# difficult_causal_chain.retention_risk at or above this → causal_chain_focus
CAUSAL_CHAIN_RISK_THRESHOLD: float = 0.50

# Minimum mastered concepts for difficulty escalation
ESCALATE_MASTERED_MIN: int = 8

# Minimum review topics for difficulty consolidation
CONSOLIDATE_REVIEW_MIN: int = 3

# Denominator for planning_confidence normalisation
# Max useful signals ≈ 5 (retention) + 5 (low mastery) + 5 (misconceptions)
# + 5 (causal chains) + 10 (mastered) + 5 (LES weak areas × 0.3) = ~31.5
# Use 20 so confidence reaches 1.0 at a realistic data-rich state
PLANNING_CONFIDENCE_SCALE: float = 20.0

# Prefixes in known_weak_areas that encode actionable topic slugs
ACTIONABLE_WEAK_AREA_PREFIXES: tuple[str, ...] = ("causal_chain:", "fragile:")

# SAT domain keywords — any review topic containing these triggers sat_drill_needed
SAT_TOPIC_KEYWORDS: frozenset[str] = frozenset({
    "sat", "balance", "intensity", "complexity", "finish", "length", "bicl", "tasting",
})

# Valid difficulty progression values
DIFFICULTY_STABLE: str = "stable"
DIFFICULTY_CONSOLIDATE: str = "consolidate"
DIFFICULTY_ESCALATE: str = "escalate"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def run_strategic_planner(
    memory_summary: dict[str, Any] | None,
    les_context: dict[str, Any] | None,
    prepass_result: dict[str, Any] | None = None,
    reference_date: str | None = None,
) -> dict[str, Any]:
    """Return a deterministic pedagogical plan based on learner state signals.

    Arguments
    ---------
    memory_summary : dict | None
        Output of build_memory_summary() from knowledge_tracing. Contains
        pre-filtered skill signals: low_mastery_concepts, retention_risks,
        recurrent_misconceptions, difficult_causal_chains, mastered_concepts.
    les_context : dict | None
        Output of build_les_context() from learner_state. Contains
        known_weak_areas, recent_misconceptions, session_count.
    prepass_result : dict | None
        Optional output of detect_misconception() for the current query.
        If present and detected=True, the matched misconception goes first
        in misconception_focus.
    reference_date : str | None
        ISO timestamp string. If provided, used as plan_generated_at instead
        of datetime.now(). Pass this in tests for deterministic output.

    Returns
    -------
    dict with exactly these keys (governance fields are never included):
        recommended_next_topics : list[str]
        review_topics           : list[str]
        avoid_topics            : list[str]
        misconception_focus     : list[str]
        causal_chain_focus      : list[str]
        sat_drill_needed        : bool
        difficulty_progression  : str  ("stable" | "consolidate" | "escalate")
        planning_confidence     : float  (0.0 – 1.0)
        plan_generated_at       : str
        cold_start              : bool
    """
    plan_generated_at: str = reference_date or datetime.now(timezone.utc).isoformat()
    mem: dict[str, Any] = memory_summary or {}
    les: dict[str, Any] = les_context or {}

    if _is_cold_start(mem, les):
        return _cold_start_plan(plan_generated_at)

    review_topics = _compute_review_topics(mem, les)
    avoid_topics = _compute_avoid_topics(mem)
    recommended_next_topics: list[str] = []  # Phase 3: driven by WSET L3 topic sequence
    misconception_focus = _compute_misconception_focus(mem, prepass_result)
    causal_chain_focus = _compute_causal_chain_focus(mem)
    sat_drill_needed = _compute_sat_drill_needed(mem, review_topics)
    difficulty_progression = _compute_difficulty_progression(mem, review_topics)
    planning_confidence = _compute_planning_confidence(mem, les)

    return {
        "recommended_next_topics": recommended_next_topics,
        "review_topics": review_topics,
        "avoid_topics": avoid_topics,
        "misconception_focus": misconception_focus,
        "causal_chain_focus": causal_chain_focus,
        "sat_drill_needed": sat_drill_needed,
        "difficulty_progression": difficulty_progression,
        "planning_confidence": planning_confidence,
        "plan_generated_at": plan_generated_at,
        "cold_start": False,
    }


# ---------------------------------------------------------------------------
# Cold-start detection
# ---------------------------------------------------------------------------

def _is_cold_start(mem: dict[str, Any], les: dict[str, Any]) -> bool:
    """Return True when neither memory nor LES provides any usable planning signal.

    Cold-start means: the planner has no evidence to reason over. An empty
    pedagogical_memory.json combined with an empty LES is the expected state
    for a brand-new learner or after a full reset.

    Note: if the LES has known_weak_areas or recent_misconceptions, those ARE
    usable signals even when pedagogical_memory.skills is empty — which is the
    current real state of the Nazareth system (567 sessions, LES populated,
    skills not yet backfilled from self-eval).
    """
    has_memory_signal: bool = bool(
        mem.get("low_mastery_concepts")
        or mem.get("retention_risks")
        or mem.get("recurrent_misconceptions")
        or mem.get("difficult_causal_chains")
        or mem.get("mastered_concepts")
    )
    has_les_signal: bool = bool(
        les.get("known_weak_areas")
        or les.get("recent_misconceptions")
    )
    return not has_memory_signal and not has_les_signal


def _cold_start_plan(plan_generated_at: str) -> dict[str, Any]:
    """Conservative no-op plan for when no learner data is available."""
    return {
        "recommended_next_topics": [],
        "review_topics": [],
        "avoid_topics": [],
        "misconception_focus": [],
        "causal_chain_focus": [],
        "sat_drill_needed": False,
        "difficulty_progression": DIFFICULTY_STABLE,
        "planning_confidence": 0.0,
        "plan_generated_at": plan_generated_at,
        "cold_start": True,
    }


# ---------------------------------------------------------------------------
# Planning components — each is a pure function over its arguments
# ---------------------------------------------------------------------------

def _compute_review_topics(
    mem: dict[str, Any],
    les: dict[str, Any],
) -> list[str]:
    """Collect concept slugs that require review, deduplicated and ordered.

    Priority order:
      1. Retention risks (concepts fading from memory — most urgent)
      2. Low mastery concepts (concepts not yet learned)
      3. Actionable weak areas from the LES (coarser, accumulated signal)

    Items from memory_summary are already pre-filtered and sorted by
    build_memory_summary(). The planner trusts the summary as authoritative.
    """
    topics: list[str] = []
    seen: set[str] = set()

    # 1. Retention risk — pre-sorted descending by risk in memory_summary
    for item in mem.get("retention_risks") or []:
        concept_id = str(item.get("concept_id") or "").strip()
        if concept_id and concept_id not in seen:
            topics.append(concept_id)
            seen.add(concept_id)

    # 2. Low mastery — pre-sorted ascending by mastery in memory_summary
    for item in mem.get("low_mastery_concepts") or []:
        concept_id = str(item.get("concept_id") or "").strip()
        if concept_id and concept_id not in seen:
            topics.append(concept_id)
            seen.add(concept_id)

    # 3. Actionable weak areas from LES (causal_chain: and fragile: prefixes only)
    for area in les.get("known_weak_areas") or []:
        topic = _extract_weak_area_topic(area)
        if topic and topic not in seen:
            topics.append(topic)
            seen.add(topic)

    return topics


def _compute_avoid_topics(mem: dict[str, Any]) -> list[str]:
    """Return concepts with confirmed mastery — no revisiting needed."""
    return list(mem.get("mastered_concepts") or [])


def _compute_misconception_focus(
    mem: dict[str, Any],
    prepass_result: dict[str, Any] | None,
) -> list[str]:
    """Return misconception IDs to prioritise in the current session.

    The active misconception from the current query appears first (if any),
    followed by persistent misconceptions from across sessions. This ordering
    ensures that the most immediate cognitive error is addressed first.
    """
    focus: list[str] = []
    seen: set[str] = set()

    # Active misconception from the current query — always first
    if prepass_result and prepass_result.get("detected"):
        mc_id = str(prepass_result.get("matched_misconception_id") or "").strip()
        if mc_id:
            focus.append(mc_id)
            seen.add(mc_id)

    # Persistent misconceptions from across sessions (pre-sorted by persistence desc)
    for item in mem.get("recurrent_misconceptions") or []:
        persistence = float(item.get("persistence") or 0.0)
        mc_id = str(item.get("misconception_id") or "").strip()
        if persistence >= MISCONCEPTION_PERSISTENCE_THRESHOLD and mc_id and mc_id not in seen:
            focus.append(mc_id)
            seen.add(mc_id)

    return focus


def _compute_causal_chain_focus(mem: dict[str, Any]) -> list[str]:
    """Return causal chain IDs with high retention risk (pre-sorted by risk desc)."""
    focus: list[str] = []
    for item in mem.get("difficult_causal_chains") or []:
        risk = float(item.get("retention_risk") or 0.0)
        chain_id = str(item.get("chain_id") or "").strip()
        if risk >= CAUSAL_CHAIN_RISK_THRESHOLD and chain_id:
            focus.append(chain_id)
    return focus


def _compute_sat_drill_needed(
    mem: dict[str, Any],
    review_topics: list[str],
) -> bool:
    """Return True when SAT-specific weaknesses are detectable in review topics or overload patterns."""
    for topic in review_topics:
        topic_lower = topic.lower()
        if any(kw in topic_lower for kw in SAT_TOPIC_KEYWORDS):
            return True
    for pattern in mem.get("overload_patterns") or []:
        if "sat" in str(pattern).lower():
            return True
    return False


def _compute_difficulty_progression(
    mem: dict[str, Any],
    review_topics: list[str],
) -> str:
    """Classify the recommended difficulty direction.

    Logic (evaluated in priority order):
      1. consolidate — if preferred_depth is "deep" OR many review topics exist
         (the learner is not ready to advance)
      2. escalate    — if enough concepts are mastered AND no review topics exist
         (the learner is ready for harder material)
      3. stable      — default; continue at current pace
    """
    mastered: list[str] = list(mem.get("mastered_concepts") or [])
    preferred_depth: str = str(mem.get("preferred_depth") or "standard")

    if preferred_depth == "deep" or len(review_topics) >= CONSOLIDATE_REVIEW_MIN:
        return DIFFICULTY_CONSOLIDATE
    if len(mastered) >= ESCALATE_MASTERED_MIN and not review_topics:
        return DIFFICULTY_ESCALATE
    return DIFFICULTY_STABLE


def _compute_planning_confidence(
    mem: dict[str, Any],
    les: dict[str, Any],
) -> float:
    """Estimate confidence in the plan as a proxy for signal richness.

    This is NOT a learner score. It reflects how much data the planner has
    to reason over. Planning confidence = 0.0 means cold-start with no data.
    Planning confidence = 1.0 means maximum signal richness.

    LES signals contribute at 0.3× weight because they are coarser and less
    precise than pedagogical memory signals.
    """
    skill_signals: int = (
        len(mem.get("low_mastery_concepts") or [])
        + len(mem.get("retention_risks") or [])
    )
    misconception_signals: int = len(mem.get("recurrent_misconceptions") or [])
    causal_signals: int = len(mem.get("difficult_causal_chains") or [])
    mastery_signals: int = len(mem.get("mastered_concepts") or [])
    les_signals: float = min(5, len(les.get("known_weak_areas") or [])) * 0.3

    total: float = (
        skill_signals
        + misconception_signals
        + causal_signals
        + mastery_signals
        + les_signals
    )
    confidence: float = min(1.0, total / PLANNING_CONFIDENCE_SCALE)
    return round(confidence, 3)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_weak_area_topic(area: str) -> str:
    """Extract a topic slug from a known_weak_area string.

    Supported (actionable) prefixes:
        "causal_chain:X"  →  X  (a causal reasoning topic)
        "fragile:X"       →  X  (a fragile concept)

    Ignored (infrastructure, not topic slugs):
        "retrieval:X"     →  ""
        "label:X"         →  ""

    Returns empty string if the area does not encode an actionable topic.
    """
    area = str(area or "").strip()
    for prefix in ACTIONABLE_WEAK_AREA_PREFIXES:
        if area.startswith(prefix):
            topic = area[len(prefix):].strip()
            if topic:
                return topic
    return ""

# Adaptive Composer Design

**Version:** 0.1 — Pre-implementation design document
**Date:** 2026-06-07
**Status:** Design only — implementation blocked on HC_* self-eval validation
**Depends on:** `docs/PLANNER_INFLUENCE_BOUNDARY.md`, `docs/STRATEGIC_PLANNER_CONTRACT.md`

---

## 1. Purpose

The Adaptive Composer is the bridge between `strategic_planner` and `answer_builder.py`. Its job is narrow and explicit: translate planner signals into a `composition_directive` that `answer_builder.py` can consume without any knowledge of the planner's internals.

Without the Adaptive Composer, `strategic_plan` is observational only — it exists in the orchestrator result and in session staging, but has zero runtime effect. The Adaptive Composer is the first component that gives the planner controlled influence over Tutor rendering.

The Adaptive Composer does NOT:
- Access retrieval directly
- Touch LES or staging files
- Consume raw pedagogical memory (only the pre-computed strategic_plan)
- Produce content (it produces rendering hints, not prose)
- Grant grading or examiner authority
- Enable any governance-flagged behavior

---

## 2. Architecture

```
strategic_plan  ──┐
                  ├──► adaptive_composer.compose() ──► composition_directive
prepass_result  ──┘
                                                              │
                                                              ▼
                                                    context_package["composition_directive"]
                                                              │
                                                              ▼
                                                    answer_builder.py
                                                    (depth, mode, passive MC hints)
```

The Adaptive Composer is a **pure function** with no side effects. It:
- Takes `strategic_plan` (dict) and `prepass_result` (dict) as input
- Returns a `composition_directive` (dict)
- Has no imports from `retrieval`, `answer_builder`, or `learner_model`
- Has no file I/O
- Is deterministic: same inputs → same output, always

The orchestrator calls `compose()` after the strategic planner runs and injects the result into `context_package` when `ENABLE_ADAPTIVE_COMPOSER = True`. With the gate off, `context_package` is unchanged.

---

## 3. Module: `tools/orchestrator/adaptive_composer.py`

### 3.1 Feature gate

```python
ENABLE_ADAPTIVE_COMPOSER: bool = False
```

This gate must remain `False` until:
1. HC_* self-eval validation is complete (missing_keyword_support < 5)
2. Phase 3A activation criteria are met (per `PLANNER_CAUSAL_CHAIN_ACTIVATION_REVIEW.md`)
3. Snapshot regression harness confirms zero drift after AC-3 wiring
4. Explicit authorization in CLAUDE.md

### 3.2 Constants

```python
MIN_COMPOSITION_CONFIDENCE: float = 0.1
# Minimum planning_confidence for planner_active=True.
# Below this threshold, composition_directive carries planner_active=False
# and all signals revert to safe defaults. Prevents low-confidence plans
# from influencing rendering.

MAX_PASSIVE_MC: int = 2
# Maximum misconception IDs emitted in passive_misconception_reinforcement.
# Bounded to prevent reinforcement spam when many misconceptions are tracked.
# Only applies when prepass_result.detected == False.

ADAPTIVE_COMPOSER_VERSION: str = "ac_v1"
```

### 3.3 `composition_directive` schema

```python
{
    # Rendering depth hint for answer_builder._determine_explanation_depth().
    # "deep"    → force verbose explanation with full causal chain rendering
    # "concise" → brief answer, minimal elaboration
    # "standard"→ normal depth (current default behavior)
    "target_depth": "standard" | "deep" | "concise",

    # Advisory only. True when strategic_plan.sat_drill_needed == True.
    # answer_builder may choose to append a SAT mini-drill prompt.
    # Does NOT force SAT output — it is a soft hint.
    "sat_drill_hint": bool,

    # Misconception IDs to reinforce passively in the answer when the
    # prepass has NOT already detected an active misconception.
    # Empty list when prepass_result.detected == True (prepass is authoritative).
    # Bounded to MAX_PASSIVE_MC items.
    "passive_misconception_reinforcement": list[str],

    # Derived pedagogical mode for the session.
    # "remediation"   → learner needs to review/consolidate weak areas
    # "exploration"   → learner is ready for harder material
    # "reinforcement" → stable, normal session
    "session_pedagogical_mode": "exploration" | "reinforcement" | "remediation",

    # Reflects planning_confidence from strategic_plan.
    # 0.0 when planner_active == False.
    "composition_confidence": float,

    # False when planning_confidence < MIN_COMPOSITION_CONFIDENCE or
    # when strategic_plan is absent/empty. When False, all other signals
    # revert to safe defaults (standard depth, no passive MC, reinforcement mode).
    "planner_active": bool,

    # Schema version for future migration.
    "adaptive_composer_version": "ac_v1",

    # NEVER present in composition_directive:
    # safe_for_examiner, examiner_scoring_allowed, uses_llm, uses_api
}
```

### 3.4 Signal translation rules

These rules implement the CONDITIONALLY_ALLOWED signal classifications from
`docs/PLANNER_INFLUENCE_BOUNDARY.md` Section 3.

#### `target_depth` derivation

Signal sources (in priority order):

1. `misconception_focus` non-empty AND `planning_confidence >= MIN_COMPOSITION_CONFIDENCE`
   → `"deep"` (persistent misconception present; learner needs reinforced explanation)

2. `difficulty_progression == "consolidate"` AND `planning_confidence >= MIN_COMPOSITION_CONFIDENCE`
   → `"deep"` (learner needs to solidify weak areas before advancing)

3. `difficulty_progression == "escalate"` AND `planning_confidence >= MIN_COMPOSITION_CONFIDENCE`
   → `"concise"` (learner is advancing; concise answer avoids over-explaining mastered content)

4. else → `"standard"`

Rule 1 takes priority over Rule 3 — an escalating session with active misconceptions
should still get deep explanation, not concise.

#### `session_pedagogical_mode` derivation

1. `review_topics` non-empty AND `difficulty_progression == "consolidate"` → `"remediation"`
2. `difficulty_progression == "escalate"` → `"exploration"`
3. else → `"reinforcement"`

#### `passive_misconception_reinforcement` derivation

Only populated when `prepass_result.get("detected") == False`. When the prepass
has already detected an active misconception, that pathway is authoritative and
the passive list must be empty to avoid double-intervention.

Source: `strategic_plan.get("misconception_focus", [])`, sliced to `MAX_PASSIVE_MC`.

#### `sat_drill_hint` derivation

Direct passthrough: `bool(strategic_plan.get("sat_drill_needed", False))`.
Advisory only — `answer_builder.py` is not required to act on it.

#### `planner_active` derivation

```python
planning_confidence = strategic_plan.get("planning_confidence", 0.0)
planner_active = (
    bool(strategic_plan)
    and planning_confidence >= MIN_COMPOSITION_CONFIDENCE
)
```

When `planner_active == False`, all other fields revert to safe defaults:
- `target_depth = "standard"`
- `sat_drill_hint = False`
- `passive_misconception_reinforcement = []`
- `session_pedagogical_mode = "reinforcement"`
- `composition_confidence = 0.0`

### 3.5 Public interface

```python
def compose(
    strategic_plan: dict[str, Any],
    prepass_result: dict[str, Any],
) -> dict[str, Any]:
    """
    Translate strategic_plan signals into a composition_directive for answer_builder.

    Pure function. No side effects. No file I/O. No imports from retrieval or
    answer_builder. Deterministic: same inputs → same output.

    Returns a composition_directive dict. Never raises — returns safe defaults
    on any malformed input.
    """
```

The function must handle:
- `strategic_plan = {}` (cold start or disabled planner)
- `strategic_plan = None`
- `prepass_result = {}` (missing keys)
- Any unexpected key types (defensive access via `.get()`)

---

## 4. Governance constraints

The Adaptive Composer MUST satisfy all governance invariants:

| Invariant | How AC satisfies it |
|---|---|
| `safe_for_examiner = False` | Key must never appear in composition_directive |
| `examiner_scoring_allowed = False` | Key must never appear in composition_directive |
| `uses_llm = False` | No LLM calls — pure dict transformation |
| `uses_api = False` | No external calls |
| `uses_embeddings = False` | No similarity computation |
| `uses_vector_db = False` | No vector store access |
| Deterministic outputs | Same inputs → same dict, always |
| No file writes outside knowledge/ and tools/ | No file I/O at all |

Governance check in `compose()`: the returned dict must be validated before
return to assert none of the forbidden keys are present. This is a defensive
assertion, not a runtime guard — the function must be written so they can never
appear, but the check catches regressions.

---

## 5. Orchestrator wiring (Phase AC-2)

When `ENABLE_ADAPTIVE_COMPOSER = True`:

```python
# In orchestrator.py, after strategic_plan is computed:
from tools.orchestrator.adaptive_composer import compose, ENABLE_ADAPTIVE_COMPOSER

if ENABLE_ADAPTIVE_COMPOSER:
    composition_directive = compose(
        strategic_plan=strategic_plan,
        prepass_result=prepass,
    )
    context_package["composition_directive"] = composition_directive
```

When `ENABLE_ADAPTIVE_COMPOSER = False` (default), `context_package` must not
contain `"composition_directive"` at all. This ensures zero behavior change for
any downstream consumer that might inspect the package shape.

---

## 6. Answer builder wiring (Phase AC-3)

`answer_builder.py` must check for `composition_directive` defensively:

```python
# In _determine_explanation_depth() or equivalent:
directive = package.get("composition_directive") or {}
if directive.get("planner_active") and directive.get("target_depth") in ("deep", "concise", "standard"):
    # Override depth only when planner is active and depth is a known value.
    # Fall through to existing logic otherwise.
    return directive["target_depth"]
```

The existing `force_deep_explanation` path from `_pedagogical_priority_boost()`
must remain unchanged for Phase AC-3. The `composition_directive` path runs
as an additional check before the existing logic, gated on `planner_active`.

For `passive_misconception_reinforcement`: `answer_builder.py` may surface these
IDs as a supplementary note at the end of the answer (not as a forced intervention).
This is lower priority than `target_depth` wiring and can be deferred to Phase AC-4.

---

## 7. Relationship to `_pedagogical_priority_boost()`

Per `docs/STRATEGIC_PLANNER_CONTRACT.md` Section 4:

- `_pedagogical_priority_boost()` is currently a no-op at runtime (skills empty)
- The Adaptive Composer does NOT replace it in Phase AC-1 through AC-3
- Coexistence is safe: `force_deep_explanation` from the adapter and `target_depth`
  from the composer address the same rendering decision via different paths
- Priority when both are active: `composition_directive.target_depth` takes
  precedence when `planner_active=True`, since the planner has richer signal context
- Phase 4 migration: replace `_pedagogical_priority_boost()` with a thin adapter
  that reads from `strategic_plan` directly (see STRATEGIC_PLANNER_CONTRACT.md
  Section 4, Phase 3 migration sequence)

The Adaptive Composer accelerates that migration by establishing the
`composition_directive` interface that `answer_builder.py` will use in Phase 4.

---

## 8. Test plan

Target: ~44 tests across 8 classes in `tests/test_adaptive_composer.py`.

### Class 1: GovernanceTests (6 tests)

```
test_no_safe_for_examiner_key_in_directive
test_no_examiner_scoring_key_in_directive
test_no_uses_llm_key_in_directive
test_no_uses_api_key_in_directive
test_composition_version_present
test_directive_is_pure_dict_no_side_effects
```

### Class 2: PlannerActiveTests (6 tests)

```
test_planner_active_true_when_confidence_above_threshold
test_planner_active_false_when_confidence_below_threshold
test_planner_active_false_when_strategic_plan_empty
test_planner_active_false_when_strategic_plan_none
test_composition_confidence_matches_planning_confidence
test_composition_confidence_zero_when_planner_inactive
```

### Class 3: TargetDepthTests (8 tests)

```
test_depth_deep_when_misconception_focus_nonempty
test_depth_deep_when_difficulty_consolidate
test_depth_concise_when_difficulty_escalate
test_depth_standard_when_difficulty_stable
test_depth_standard_when_planner_inactive
test_depth_deep_when_misconception_and_escalate_coexist  # misconception wins
test_depth_standard_when_confidence_below_threshold
test_depth_valid_values_only  # never an unknown string
```

### Class 4: PedagogicalModeTests (6 tests)

```
test_mode_remediation_when_review_topics_and_consolidate
test_mode_exploration_when_escalate
test_mode_reinforcement_when_stable
test_mode_reinforcement_when_planner_inactive
test_mode_exploration_when_escalate_even_with_review_topics  # escalate dominates
test_mode_valid_values_only  # never an unknown string
```

### Class 5: PassiveMisconceptionTests (6 tests)

```
test_passive_mc_empty_when_prepass_detected_true
test_passive_mc_populated_when_prepass_detected_false
test_passive_mc_bounded_to_max
test_passive_mc_empty_when_misconception_focus_empty
test_passive_mc_empty_when_planner_inactive
test_passive_mc_is_list_of_strings
```

### Class 6: SatDrillHintTests (4 tests)

```
test_sat_drill_hint_true_when_plan_sat_drill_needed
test_sat_drill_hint_false_when_plan_sat_drill_not_needed
test_sat_drill_hint_false_when_planner_inactive
test_sat_drill_hint_is_bool
```

### Class 7: SafeDefaultTests (4 tests)

```
test_safe_defaults_when_plan_is_empty_dict
test_safe_defaults_when_plan_is_none
test_safe_defaults_when_confidence_zero
test_safe_defaults_match_expected_shape  # all expected keys present
```

### Class 8: DeterminismTests (4 tests)

```
test_same_inputs_produce_identical_output
test_cold_start_plan_produces_stable_defaults
test_high_confidence_plan_is_deterministic
test_compose_does_not_mutate_input_dicts
```

Total: 44 tests across 8 classes.

---

## 9. Implementation phases

### Phase AC-1 — Isolated module (unblocked after HC_* validation)

Create `tools/orchestrator/adaptive_composer.py` with:
- `ENABLE_ADAPTIVE_COMPOSER: bool = False`
- `MIN_COMPOSITION_CONFIDENCE`, `MAX_PASSIVE_MC`, `ADAPTIVE_COMPOSER_VERSION` constants
- `compose()` pure function
- All helper functions (`_derive_target_depth`, `_derive_pedagogical_mode`,
  `_derive_passive_mc`, `_safe_defaults`, `_validate_governance`)
- Zero imports from retrieval, answer_builder, learner_model, or orchestrator body

Create `tests/test_adaptive_composer.py` with all 44 tests. All 44 must pass.
Snapshot regression harness: must remain green (zero impact — gate is off).

### Phase AC-2 — Orchestrator wiring (after AC-1 green)

Wire `compose()` into `orchestrator.py` behind `ENABLE_ADAPTIVE_COMPOSER` gate.
Add `"composition_directive"` injection to `context_package` when gate is on.
Add integration tests to `tests/test_orchestrator_adaptive_composer_integration.py`
(~18 tests): verifies gate-off no-op, gate-on injection, directive shape in
context_package, governance cleanliness, no snapshot drift.

ENABLE_ADAPTIVE_COMPOSER must remain False in all committed code.

### Phase AC-3 — Answer builder wiring (after AC-2 green + explicit authorization)

Wire `composition_directive.target_depth` into `_determine_explanation_depth()`.
Wire `composition_directive.sat_drill_hint` into mini-practice prompt logic.
This is the first phase with snapshot risk — run full 25-snapshot regression
before and after. Any snapshot drift requires rollback.
Gate: `ENABLE_ADAPTIVE_COMPOSER` must still be False in committed code.
Add snapshot comparison tests to verify zero drift when gate is off.

### Phase AC-4 — Passive MC reinforcement and Phase 4 migration prep

Wire `passive_misconception_reinforcement` into answer rendering (supplementary
note only, not intervention). Annotate `_pedagogical_priority_boost()` as
`# DEPRECATED — see docs/STRATEGIC_PLANNER_CONTRACT.md Phase 4`.
Introduce `_strategic_plan_to_retrieval_hints()` stub (no behavior yet).

---

## 10. Pre-implementation checklist

Before writing any code:

- [ ] HC_* self-eval validation complete (run `python -m unittest discover -s tests -v`,
      confirm 771+ passing; run brutal self-eval, confirm missing_keyword_support < 5)
- [ ] This design document reviewed and approved (no open questions)
- [ ] `docs/PLANNER_INFLUENCE_BOUNDARY.md` re-read (signal classifications still apply)
- [ ] `docs/STRATEGIC_PLANNER_CONTRACT.md` re-read (migration path alignment)
- [ ] `ENABLE_ADAPTIVE_COMPOSER = False` confirmed as starting state
- [ ] Snapshot baseline confirmed green before first code change

---

*This document is a design record only. It does not authorize behavior changes.
All governance invariants from CLAUDE.md remain in effect. Implementation
requires explicit authorization after HC_* self-eval validation.*

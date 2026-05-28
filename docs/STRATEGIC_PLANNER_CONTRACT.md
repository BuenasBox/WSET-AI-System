# Strategic Planner Semantic Contract

**Version:** 1.0 — Phase 1B.5 (hardening, no behavior change)
**Date:** 2026-05-28
**Status:** Authoritative — supersedes any implicit assumptions in code comments

---

## Purpose

This document defines the semantic contract between the two planning-adjacent
systems that currently coexist in the orchestrator:

1. `tools/orchestrator/strategic_planner.py` — explicit planning layer
2. `_pedagogical_priority_boost()` in `tools/orchestrator/orchestrator.py` — legacy adapter

Its goals are:

- Establish a single future planning authority
- Prevent semantic divergence as both systems evolve
- Document all shared signals with explicit ownership
- Define a migration path that allows `_pedagogical_priority_boost()` to
  be retired safely without disrupting retrieval or Tutor behavior

This document does NOT authorize behavior changes. All existing logic is
preserved as-is. This is an architectural record only.

---

## 1. Authority Model

### Current state (Phase 1B)

| Concern | Current Authority | Notes |
|---|---|---|
| Pedagogical intent | `strategic_planner` (inert) | Not yet consumed |
| Retrieval prioritization | `_pedagogical_priority_boost()` (nominal) | See critical finding below |
| Answer depth | `_pedagogical_priority_boost()` via `force_deep_explanation` | Sole live consumer in answer_builder |
| Misconception intervention | `misconception_prepass.py` | Binary, authoritative |
| Retention resurfacing | `_pedagogical_priority_boost()` (lists concept IDs) | Passed to context package only |
| Session progression | No component owns this yet | Phase 2 target |
| Topic escalation | `strategic_planner` (inert) | Via `difficulty_progression` |

### Critical architectural finding

`_pedagogical_priority_boost()` is misnamed. It does NOT influence retrieval
ranking. `run_retrieval_sandbox()` accepts only `(root, query, top_k,
output_prefix)` — it never receives the boost dict. The boost is placed into
`retrieval_plan.pedagogical_priority_boost` inside the context package, where
it is consumed only by `answer_builder.py` at line 607:

```python
boost = (package.get("retrieval_plan") or {}).get("pedagogical_priority_boost") or {}
if boost.get("force_deep_explanation") and cognitive_load != "high":
    return "deep"
```

**Consequence:** `_pedagogical_priority_boost()` is currently a
**Tutor rendering hint adapter**, not a retrieval adapter. Its name
should eventually be corrected.

**Current live effect of `_pedagogical_priority_boost()`:**
Only `force_deep_explanation` has a runtime effect. All other fields
(`low_mastery_concepts`, `causal_chain_boosts`, `resurfacing_concepts`) are
written to the context package but not consumed by any downstream component.
Given that `pedagogical_memory.skills` is currently empty for Nazareth,
`force_deep_explanation` is always `False`, making the entire adapter a no-op
at runtime today.

### Recommended authority model

```
strategic_planner
    = planning authority (future)
    = owns: intent, pacing, escalation, topic selection, session goals

_pedagogical_priority_boost()
    = legacy Tutor rendering adapter (current)
    = transitional: will become a thin read-only projection of strategic_plan
    = eventual fate: replaced by a named adapter function that reads from
      strategic_plan when strategic_plan becomes authoritative (Phase 4)
```

This model is appropriate. The strategic planner is the right long-term
authority because it: (a) is deterministic and testable in isolation,
(b) has explicit thresholds, (c) has no side effects, (d) is governance-clean.
The adapter is appropriate as a transitional bridge until Tutor rendering
can be updated to consume `strategic_plan` directly.

---

## 2. Signal Ownership

The following signals are currently read by more than one component.
Each is documented with its source of truth, consumers, intended meaning,
and migration path.

---

### `low_mastery_concepts`

**Source of truth:** `knowledge_tracing.build_memory_summary()`, which reads
from `pedagogical_memory.skills`. Pre-sorted ascending by `mastery_probability`,
top 5 items only.

**Consumers:**

| Consumer | How it uses the signal |
|---|---|
| `_pedagogical_priority_boost()` | Extracts `concept_id` list → passed to context package (currently unused by downstream) |
| `strategic_planner._compute_review_topics()` | Adds concept_id to `review_topics` if not already present |
| `explanation_priority._memory_priority_boost()` | Presence (any items) → adds +0.08 priority boost |
| `explanation_priority._memory_learning_velocity()` | Count → reduces learning velocity estimate |
| `answer_builder._scaffolding_policy_for_package()` | Reads `mastery_probability` of first item → scaffolding policy |

**Intended meaning:** Concepts where the learner's current mastery estimate
falls below the low-mastery threshold (default 0.45). Ordered by urgency
(lowest mastery first).

**Threshold divergence:** `build_memory_summary()` applies the threshold at
source. `strategic_planner.LOW_MASTERY_THRESHOLD` (0.45) is documented as a
reference constant only — the planner trusts the pre-filtered list from
`build_memory_summary()` rather than re-filtering. These must remain aligned.

**Migration path:** No change required. The planner should continue trusting
the pre-filtered list. If the threshold ever changes in `knowledge_tracing.py`,
`LOW_MASTERY_THRESHOLD` in `strategic_planner.py` must be updated in the same
commit to stay in sync.

---

### `retention_risks`

**Source of truth:** `knowledge_tracing.build_memory_summary()`. Pre-sorted
descending by `retention_risk`, top 5 items only.

**Consumers:**

| Consumer | How it uses the signal |
|---|---|
| `_pedagogical_priority_boost()` | Extracts `concept_id` list as `resurfacing_concepts` → passed to context package (currently unused downstream) |
| `strategic_planner._compute_review_topics()` | Adds concept_id to `review_topics` (first priority, before low mastery) |
| `explanation_priority._memory_priority_boost()` | Presence → adds +0.06 priority boost |

**Intended meaning:** Concepts at risk of being forgotten based on recency
and mastery decay. High retention risk = needs resurfacing soon.

**Threshold divergence:** `build_memory_summary()` applies a threshold at
source before returning the list. `strategic_planner.RETENTION_RISK_THRESHOLD`
(0.55) is a documentation reference. These must remain aligned.

**Migration path:** Same as `low_mastery_concepts`. The planner trusts the
pre-filtered list; the threshold constant must track `knowledge_tracing.py`.

---

### `recurrent_misconceptions`

**Source of truth:** `pedagogical_memory.recurrent_misconceptions` (dict),
normalized and sorted by `persistence` descending, top 5 items.

**Consumers:**

| Consumer | How it uses the signal |
|---|---|
| `_pedagogical_priority_boost()` | Checks `persistence ≥ 0.60` → sets `force_deep_explanation=True` |
| `strategic_planner._compute_misconception_focus()` | Includes items where `persistence ≥ 0.40` in `misconception_focus` |
| `explanation_priority.build_explanation_priority()` | Max persistence → `misconception_persistence` score |

**Threshold divergence (active risk):**

```
_pedagogical_priority_boost()  uses  persistence ≥ 0.60  →  force_deep
strategic_planner               uses  persistence ≥ 0.40  →  misconception_focus
```

These thresholds have different semantics by design:
- The adapter's 0.60 threshold means "this misconception is so persistent
  it must force deep rendering mode" (a rendering decision).
- The planner's 0.40 threshold means "this misconception is recurring enough
  to be addressed in the session plan" (a pedagogical decision).

**This divergence is intentional and correct.** It is NOT a bug. The two
thresholds answer different questions. They must be documented separately and
must not be unified without explicit semantic analysis.

**Migration path:** When `strategic_planner` becomes authoritative (Phase 4),
`force_deep_explanation` should be derived from `strategic_plan.misconception_focus`
being non-empty. The 0.60 threshold in the adapter should be retired in favor
of the planner's 0.40 threshold, since the planner's question ("is this worth
addressing?") subsumes the adapter's question ("is this very severe?").

---

### `difficult_causal_chains`

**Source of truth:** `pedagogical_memory.difficult_causal_chains` (list),
sorted descending by `retention_risk`, top 5 items.

**Consumers:**

| Consumer | How it uses the signal |
|---|---|
| `_pedagogical_priority_boost()` | Extracts `chain_id` list as `causal_chain_boosts` → context package (currently unused downstream) |
| `strategic_planner._compute_causal_chain_focus()` | Includes chains with `retention_risk ≥ 0.50` in `causal_chain_focus` |

**Threshold divergence:** The adapter emits all chains regardless of threshold.
The planner filters by `CAUSAL_CHAIN_RISK_THRESHOLD=0.50`. The planner is
stricter. Both are currently inert (skills empty).

**Migration path:** When the planner becomes authoritative, the adapter's
`causal_chain_boosts` should be replaced by `strategic_plan.causal_chain_focus`.
The adapter's un-thresholded behavior should be retired.

---

### `preferred_depth`

**Source of truth:** `pedagogical_memory.preferred_depth` (string: `"standard"` or `"deep"`).

**Consumers:**

| Consumer | How it uses the signal |
|---|---|
| `_pedagogical_priority_boost()` | Forwarded as-is to context package |
| `strategic_planner._compute_difficulty_progression()` | `preferred_depth == "deep"` → returns `"consolidate"` |

**Semantic problem:** `preferred_depth` conflates three distinct concepts
that need to be separated. See Section 3.

---

### `known_weak_areas`

**Source of truth:** `epistemic_state.json` (LES), populated by
`les_reconciler.py` from self-eval feedback.

**Consumers:**

| Consumer | How it uses the signal |
|---|---|
| `strategic_planner._compute_review_topics()` | Extracts `causal_chain:X` and `fragile:X` prefixes → `review_topics` |
| `_pedagogical_priority_boost()` | Not consumed (not in the adapter's input path) |

**Prefix semantics:**

| Prefix | Meaning | Planner action |
|---|---|---|
| `causal_chain:X` | Learner struggled with causal chain X | Add X to review_topics |
| `fragile:X` | Concept X is mastered but fragile | Add X to review_topics |
| `retrieval:X` | Retrieval weakness in topic X | Ignored (infrastructure signal) |
| `label:X` | Recurring failure label X | Ignored (diagnostic signal) |

**Migration path:** No change needed. The planner correctly ignores
infrastructure signals. When the planner becomes authoritative, `known_weak_areas`
should be fully owned by the planner as a primary input.

---

## 3. Depth Semantics

The term `preferred_depth` currently mixes three orthogonal concepts.
This creates ambiguity as more components consume it.

### Proposed semantic separation

**`answer_depth`** — Rendering verbosity. How detailed should the Tutor's
prose response be?
- Values: `"concise"` | `"standard"` | `"deep"`
- Authority: Tutor rendering layer (`answer_builder.py`)
- Driven by: `force_deep_explanation` (adapter) or, in the future,
  `strategic_plan.difficulty_progression == "consolidate"`
- Current location: implicit output of `_determine_explanation_depth()`

**`difficulty_progression`** — Session pacing and escalation direction.
Should the current session introduce harder material, consolidate existing
material, or maintain pace?
- Values: `"escalate"` | `"stable"` | `"consolidate"`
- Authority: `strategic_planner` (owned as of Phase 1A)
- Driven by: mastered concept count, review topic count, `preferred_depth`

**`pedagogical_mode`** — Learning goal type for the session. Is the learner
exploring new territory or reinforcing prior learning?
- Values: `"exploration"` | `"reinforcement"` | `"remediation"`
- Authority: Not yet implemented — Phase 2 target
- Will be driven by: `difficulty_progression` + misconception presence +
  retention risk profile

### Current state of `preferred_depth`

`pedagogical_memory.preferred_depth` is currently a single string that
conflates all three concepts above. It is read by:

1. `_pedagogical_priority_boost()` — forwarded as-is (no effect today)
2. `strategic_planner._compute_difficulty_progression()` — `"deep"` → `"consolidate"`

**Recommended action (future, not this phase):** When
`pedagogical_memory.skills` is populated, split `preferred_depth` into the
three explicit fields above. Until then, the current behavior is safe because
the field is inert (skills empty, value is always `"standard"`).

---

## 4. Future Migration Plan

### Phase 1A (complete)
`strategic_plan` created in isolation. Pure function, no side effects,
no downstream consumers. Planning logic defined and tested.

### Phase 1B (complete)
`strategic_plan` wired into orchestrator result. Inert — not in
`context_package`, not consumed by retrieval or Tutor.
`_pedagogical_priority_boost()` unchanged and still nominally active.

### Phase 1C (next)
Persist `strategic_plan` into `session_staging.json`. The plan survives
across sessions and can be read back at the start of the next session.
This enables longitudinal continuity without any behavioral change.

**`_pedagogical_priority_boost()` status:** unchanged, no-op at runtime.

### Phase 2 — Session cognitive ledger
Introduce a session-level cognitive ledger that accumulates signals across
queries within a single session. The planner runs once per session (at start)
and can be updated mid-session as signals accumulate.

**`_pedagogical_priority_boost()` status:** still present but should be
annotated as `# DEPRECATED — will be replaced by strategic_plan adapter`.

### Phase 3 — Planner influences routing
`strategic_plan` is injected into the context package and consumed by
`answer_builder.py`. Specifically:
- `strategic_plan.misconception_focus` supplements misconception routing
- `strategic_plan.difficulty_progression` supplements `answer_depth` decisions
- `strategic_plan.review_topics` influences retrieval (for the first time)

**`_pedagogical_priority_boost()` status:** The adapter should be updated to
read from `strategic_plan` rather than raw memory signals. This is the
"projection adapter" model — the adapter becomes a thin translation layer
rather than an independent computation.

Migration sequence for this phase:
1. Add adapter function `_strategic_plan_to_retrieval_hints(strategic_plan)` that
   produces the same dict shape as `_pedagogical_priority_boost()`.
2. Run both in parallel and assert they produce equivalent output.
3. Retire `_pedagogical_priority_boost()` when parity is confirmed.

Threshold resolution at this phase:
- `force_deep_explanation`: derived from `strategic_plan.misconception_focus`
  being non-empty (threshold 0.40 wins over adapter's 0.60)
- `causal_chain_boosts`: derived from `strategic_plan.causal_chain_focus`
  (threshold 0.50 applies)

### Phase 4 — Planner becomes authoritative
`strategic_planner` is the sole source of planning decisions. All rendering
hints, routing decisions, and retrieval priorities flow from `strategic_plan`.

**`_pedagogical_priority_boost()` status:** Removed. Replaced by
`_strategic_plan_to_retrieval_hints()` introduced in Phase 3.

**`preferred_depth` in `pedagogical_memory`:** Replaced by the three explicit
fields (`answer_depth`, `difficulty_progression`, `pedagogical_mode`).

---

## 5. Proposed Regression Tests (future — do NOT implement yet)

These tests should be created at Phase 3 before any planner-to-rendering
wiring is done. They exist to catch semantic divergence before it enters
the snapshots.

### 5.1 — Semantic divergence detection
```
test_planner_and_adapter_agree_on_force_deep_when_skills_populated
    Given: memory with persistence=0.65 misconception
    Assert: adapter.force_deep_explanation == True
    Assert: strategic_plan.misconception_focus is non-empty
    (both agree — different thresholds but same direction at 0.65)

test_planner_and_adapter_diverge_at_low_persistence
    Given: memory with persistence=0.50 misconception
    Assert: adapter.force_deep_explanation == False  (0.50 < 0.60)
    Assert: "mc_id" in strategic_plan.misconception_focus  (0.50 >= 0.40)
    (divergence is expected and correct — document it, do not suppress it)
```

### 5.2 — Planner/adapter consistency after migration
```
test_strategic_plan_to_retrieval_hints_matches_legacy_adapter_shape
    Given: any populated memory_summary
    Assert: keys of _strategic_plan_to_retrieval_hints() == keys of _pedagogical_priority_boost()

test_strategic_plan_to_retrieval_hints_force_deep_matches_misconception_focus
    Given: strategic_plan.misconception_focus non-empty
    Assert: hints["force_deep_explanation"] == True
```

### 5.3 — Threshold consistency
```
test_low_mastery_threshold_matches_build_memory_summary_filter
    Assert: strategic_planner.LOW_MASTERY_THRESHOLD == knowledge_tracing._mastery_threshold

test_retention_risk_threshold_matches_build_memory_summary_filter
    Assert: strategic_planner.RETENTION_RISK_THRESHOLD matches knowledge_tracing threshold
```

### 5.4 — Governance preservation
```
test_strategic_plan_adapter_does_not_introduce_governance_fields
    Assert: "safe_for_examiner" not in _strategic_plan_to_retrieval_hints(plan)
```

---

## 6. Phase 1C Assessment

Phase 1C as currently scoped — persisting `strategic_plan` into
`session_staging.json` — is **safe to proceed unchanged.**

The persistence is additive (new key in existing file), does not alter
any retrieval or Tutor path, and requires no changes to `_pedagogical_priority_boost()`.

**Pre-condition for Phase 1C:** This contract document should be committed
before Phase 1C begins, so that the Phase 1C implementation is written with
explicit awareness of signal ownership.

**One constraint to add to Phase 1C:** The persisted plan must be written as
a snapshot only (not read back and re-used as live input to the planner).
The planner must re-derive the plan from fresh LES signals on every session.
The persisted plan is for observability and future ledger comparison only.
This prevents the plan from becoming a self-referential input.

---

*This document is an architectural record. It does not represent WSET
assessment or examiner authority. All governance invariants remain unchanged.*

# Planner Influence Boundary Contract

**Version:** 1.0 — Phase 3A.0 (governance definition, no behavior change)
**Date:** 2026-05-28
**Status:** Authoritative pre-Phase-3 governance document

---

## Purpose

This document defines the exact boundary between the strategic planner as an
*observational system* and the strategic planner as a *runtime influence*.

It must be read and acknowledged before any planner signal is permitted to
affect retrieval, Tutor rendering, routing, or any other runtime behaviour.

**No behavior changes in this document.** This is an architecture and
governance record only. All runtime behavior remains unchanged from Phase 2C.

---

## Background

Until Phase 2C, the planner operates under a strict no-influence constraint:

```
strategic_planner
    ↓
observation + persistence only
(never → retrieval, Tutor, routing)
```

Phase 3 will cross this boundary for the first time. The decision must be
deliberate, auditable, and reversible. This document governs that crossing.

**Key pre-condition identified in `STRATEGIC_PLANNER_CONTRACT.md`:**
`_pedagogical_priority_boost()` does NOT influence retrieval ranking today —
it only reaches `answer_builder.py` via `force_deep_explanation`, and even
that is inert because `pedagogical_memory.skills = {}` for Nazareth. This
means planner influence, when introduced, will be the FIRST time any
pedagogical signal reaches retrieval. The stakes of getting this right are
correspondingly high.

---

## Section 1 — Signal Classification

Each strategic planner output signal is classified for its permissibility as
a runtime influence. Classifications apply to direct influence only; all
signals remain permitted as observational/persistence artifacts.

### Legend

| Classification | Meaning |
|---|---|
| `ALLOWED` | Safe to wire into runtime with standard regression testing |
| `CONDITIONALLY_ALLOWED` | Permitted only under specific conditions (documented below) |
| `FORBIDDEN` | Must never influence runtime behavior |

---

### `review_topics` — `CONDITIONALLY_ALLOWED`

**What it is:** List of concept slugs derived from retention risks, low mastery,
and LES weak areas. Ordered by urgency.

**Permitted influence:** Retrieval query expansion only. The topic slugs may
be added as soft tokens to the query before the retrieval sandbox scores
chunks. This is additive and reversible.

**Conditions:**
1. Influence must be additive (tokens appended, not query replaced).
2. Influence must be bounded (`MAX_REVIEW_TOPIC_EXPANSION_TOKENS` constant).
3. `planning_confidence` must be above a minimum threshold before activation.
4. Snapshot regression suite must pass before and after activation.
5. A feature flag must gate the influence so it can be disabled without code change.

**Forbidden uses:** May not influence scoring weights, ranking order, forced
retrieval node selection, or Tutor rendering.

---

### `misconception_focus` — `CONDITIONALLY_ALLOWED`

**What it is:** List of misconception IDs to address in the session, ordered
by priority (active query first, then persistent).

**Permitted influence:** Soft reinforcement of misconception-related query
expansion. However, the misconception pre-pass (`detect_misconception()`)
already handles authoritative misconception routing. The planner's
`misconception_focus` is a *supplementary* signal — it must never override
or duplicate the pre-pass routing.

**Conditions:**
1. Only activatable when pre-pass returned `detected=False` (no active
   misconception) — i.e., passive reinforcement only.
2. Must not override `forced_retrieval_nodes` established by pre-pass.
3. Bounded to soft query expansion only (no forced node injection).

**Forbidden uses:** May not trigger a misconception intervention. May not
override pre-pass results. May not inject misconception nodes into
`forced_retrieval_nodes`.

---

### `causal_chain_focus` — `CONDITIONALLY_ALLOWED`

**What it is:** List of causal chain IDs with high retention risk
(`retention_risk ≥ 0.50`).

**Permitted influence:** Soft query token expansion to bias retrieval toward
those chain IDs. The retrieval sandbox already detects causal chains via
trigger keywords; the planner may gently reinforce this by adding chain-
related tokens.

**Conditions:**
1. Additive token expansion only.
2. Must not override `forced_causal_chains` produced by the retrieval sandbox.
3. Governed by `planning_confidence` threshold.

**Forbidden uses:** May not inject chain nodes as forced retrieval items. May
not replace the retrieval sandbox's own chain detection logic.

---

### `sat_drill_needed` — `CONDITIONALLY_ALLOWED`

**What it is:** Boolean derived from SAT-keyword matches in `review_topics`.

**Permitted influence:** Can provide a soft hint to the SAT reasoner that SAT
content is highly relevant for this session. However, the SAT reasoner already
detects SAT queries independently via `is_sat_query()`. The planner's hint is
advisory only.

**Conditions:**
1. The SAT reasoner must remain authoritative — it may ignore the hint.
2. The hint must not change SAT parameter scoring or quality formulation.
3. Only usable as an annotation in the context package (informational).

**Forbidden uses:** May not override SAT reasoner's own query classification.
May not change SAT observation scoring. May not inject SAT quality claims.

---

### `difficulty_progression` — `CONDITIONALLY_ALLOWED`

**What it is:** Session pacing direction: `"stable"` | `"consolidate"` |
`"escalate"`.

**Permitted influence:** Can inform Tutor explanation depth selection (via
`_determine_explanation_depth()` in `answer_builder.py`). Specifically:
`"consolidate"` may reinforce "deep" explanation mode in a way that parallels
the existing `force_deep_explanation` path.

**Conditions:**
1. Must not replace `force_deep_explanation` (the legacy adapter path); must
   work alongside it.
2. Influence must go through `answer_builder.py`'s existing depth logic — not
   a new rendering path.
3. Snapshot regression required before activation.
4. Must be reversible to current behavior by setting `difficulty_progression`
   influence weight to zero.

**Forbidden uses:** May not change Tutor source selection, retrieval results,
SAT quality claims, or governance flags.

---

### `planning_confidence` — `FORBIDDEN` (for direct influence)

**What it is:** A signal-richness proxy (0.0–1.0) indicating how much data
the planner had to reason over. It is NOT a learner quality score.

**Why forbidden:** Using `planning_confidence` as a runtime gate could create
a feedback loop: high confidence sessions influence behavior, which changes
sessions, which changes confidence. The signal is a *meta-signal about data
richness*, not a *quality assessment*. Permitting it to drive behavior would
corrupt its meaning.

**Permitted uses:** Threshold gating only — e.g., "do not activate review
topic expansion if `planning_confidence < 0.1`". Even this use must be
documented as a static threshold constant, not a dynamic policy.

---

### `cold_start` — `FORBIDDEN` (for direct influence)

**What it is:** Boolean indicating the planner had no usable signal data.

**Why forbidden:** `cold_start=True` means the plan is a conservative no-op.
Using it as a runtime signal (e.g., "skip personalization") would create a
behavioural difference between new learners and established learners that is
not driven by pedagogical intent but by data absence. The system must behave
conservatively regardless.

**Permitted uses:** Logging, ledger, and CLI reporting only.

---

### `recommended_next_topics` — `FORBIDDEN` (until Phase 3+)

**What it is:** Always empty in Phase 1–3 (requires WSET L3 topic sequence,
Phase 3 work). Even when populated, this signal must not influence runtime
until the topic sequence is validated against the exam corpus.

---

### `avoid_topics` — `FORBIDDEN` (until Phase 4)

**What it is:** List of mastered concepts.

**Why forbidden:** Suppressing retrieval of mastered concepts risks omitting
supporting material that grounds new learning. Negative retrieval exclusion
requires careful design and is a Phase 4 concern.

---

## Section 2 — Influence Target Classification

| Target | Classification | Rationale |
|---|---|---|
| **A. Retrieval query expansion** | CONDITIONALLY_ALLOWED | Additive, reversible, testable; proven pattern (SAT expansion, domain expansions) |
| **B. Retrieval scoring** | FORBIDDEN | Changes chunk ranking in ways that drift snapshots; not auditable without full re-evaluation |
| **C. Retrieval ranking override** | FORBIDDEN | Would create hidden cognitive authority; violates deterministic-first |
| **D. Tutor explanation depth** | CONDITIONALLY_ALLOWED | Existing pattern via `force_deep_explanation`; limited blast radius |
| **E. SAT reasoning** | FORBIDDEN | The SAT reasoner is self-contained and deterministic; advisory hints only permitted |
| **F. Self-eval** | FORBIDDEN | Self-eval must be independent of session-state planner; contamination risk |
| **G. LES updates** | CONDITIONALLY_ALLOWED | Only via `les_reconciler.py`; never direct write; only after self-eval pipeline |
| **H. Routing (misconception/normal)** | FORBIDDEN | Pre-pass is authoritative; planner may not override routing decisions |
| **I. Governance flags** | FORBIDDEN (absolute) | `safe_for_examiner`, `examiner_scoring_allowed` are immutable; planner has zero authority |
| **J. Forced retrieval nodes** | FORBIDDEN | Forced nodes are the pre-pass's domain; planner may not inject nodes |

---

## Section 3 — Governance Analysis

### What planner influence would violate the deterministic-first philosophy

- Any planner influence that is **not reproducible from the same LES inputs**
  violates determinism. The planner itself is deterministic; its influence
  pathways must also be deterministic.
- Influence via neural embedding similarity, LLM-generated hints, or
  stochastic expansion would violate this principle.
- Influence that depends on wall-clock time, session history not captured in
  LES, or external API calls would violate this principle.

### What planner influence would violate the governance-first philosophy

- Any influence that allows the planner to set or read `safe_for_examiner`,
  `examiner_scoring_allowed`, or any grading field.
- Any influence path where the planner output reaches a component that
  currently enforces governance flags (retrieval filter, Tutor validator) in
  a way that could accidentally elevate or bypass those flags.
- Planner-driven LES writes that modify `session_count` or `governance` blocks
  directly (bypassing `les_reconciler.py`).

### What planner influence would violate the retrieval-before-generation philosophy

- Any planner influence that causes the Tutor to generate content *about*
  topics before those topics have been retrieved from the corpus.
- Planner-driven "topic injection" into the Tutor prompt without corresponding
  retrieval evidence would violate source-first semantics.
- Planner-driven "answer length" hints that are not grounded in retrieval
  depth signals would violate this principle.

### What planner influence would violate the snapshot-tested cognition philosophy

- Any influence that changes Tutor output for the 25 frozen snapshot questions
  without a deliberate, reviewed snapshot regeneration.
- Any influence that changes the `why_retrieved` field or source rankings
  without a corresponding regression test update.
- Any influence where the blast radius cannot be measured by running
  `python -m unittest tests.test_tutor_snapshot_regression -v`.

---

## Section 4 — Risk Matrix

| Influence | Architectural Risk | Regression Risk | Governance Risk | Snapshot Risk |
|---|---|---|---|---|
| `review_topics` → query expansion | LOW | MEDIUM | LOW | MEDIUM |
| `misconception_focus` → query expansion | LOW | MEDIUM | LOW | MEDIUM |
| `causal_chain_focus` → query expansion | LOW | LOW | LOW | LOW |
| `difficulty_progression` → Tutor depth | LOW | MEDIUM | LOW | HIGH |
| `sat_drill_needed` → SAT hint | LOW | LOW | LOW | LOW |
| `review_topics` → retrieval scoring | HIGH | HIGH | MEDIUM | HIGH |
| `review_topics` → ranking override | HIGH | CRITICAL | HIGH | CRITICAL |
| Any signal → governance flags | CRITICAL | CRITICAL | CRITICAL | CRITICAL |
| Any signal → self-eval | HIGH | HIGH | HIGH | CRITICAL |
| Any signal → forced retrieval nodes | HIGH | HIGH | MEDIUM | HIGH |
| Any signal → LES direct write | HIGH | MEDIUM | HIGH | LOW |

**Risk definitions:**

- **LOW:** Isolated to a single function; reversible by removing one parameter;
  blast radius contained within a single test file.
- **MEDIUM:** Affects multiple functions or test files; requires full regression
  suite run to verify; reversible within a single PR.
- **HIGH:** Affects retrieval ranking, Tutor rendering, or snapshot outputs;
  snapshot regeneration required; regression suite may show drift.
- **CRITICAL:** Affects governance flags, examiner authority, or self-eval
  ground truth; must never be activated without explicit architectural review
  and sign-off.

---

## Section 5 — Phase 3 Entry Criteria

The following conditions must ALL be true before any planner signal may affect
runtime behavior:

### 5.1 — Existing test health (must pass, not regress)
- [ ] `python -m unittest discover -s tests -v` → 481+ passing, zero errors
- [ ] `python -m unittest tests.test_tutor_snapshot_regression -v` → 35/35 green
- [ ] `RUN_SLOW_TESTS=1 python -m unittest tests.test_golden_self_eval -v` → 7/7 green
- [ ] Brutal self-eval → zero failure labels, zero retrieval gaps, zero SAT weaknesses

### 5.2 — Planner parity tests (new, must be written before Phase 3)
- [ ] Test: `strategic_plan.review_topics` contains only concept slugs that
  exist in the WSET corpus vocabulary (no invented topics).
- [ ] Test: planner output is stable across 10 consecutive identical runs
  (determinism stress test).
- [ ] Test: planner output with `planning_confidence < 0.1` is treated as
  advisory only — the influence pathway must degrade gracefully.

### 5.3 — Influence isolation tests (new, must be written before Phase 3)
- [ ] Test: the influence pathway can be disabled by a single constant/flag
  and the system reverts to Phase 2C behavior exactly.
- [ ] Test: planner influence does not change the output when `review_topics`
  is empty (zero-signal baseline parity).
- [ ] Test: planner influence does not change governance flag values anywhere
  in the result or context package.

### 5.4 — Snapshot invariants (must be verified before and after)
- [ ] Run snapshot regression BEFORE applying any influence.
- [ ] Run snapshot regression AFTER applying any influence.
- [ ] If any snapshot changes, the change must be reviewed, justified, and
  the snapshot explicitly regenerated — never silently updated.

### 5.5 — Governance verification
- [ ] Static analysis: confirm `safe_for_examiner` and `examiner_scoring_allowed`
  never appear as mutable values anywhere in the new code path.
- [ ] Test: the new influence pathway produces `safe_for_examiner=False` in
  all outputs regardless of planner state.

---

## Section 6 — First Safe Influence

**Recommended first influence: `causal_chain_focus` → retrieval query expansion**

Rationale:

1. **Lowest snapshot risk.** Causal chain retrieval is already triggered by
   keyword matching in the retrieval sandbox. Adding chain IDs as soft query
   tokens reinforces an already-existing mechanism rather than introducing a
   new one. If a chain was going to be retrieved anyway, the expansion is a
   no-op. If the chain was borderline, the expansion gently reinforces it.

2. **Proven pattern.** The retrieval sandbox already uses `domain_expansions.json`
   and SAT observation expansion. Adding chain tokens follows the same pattern.

3. **Reversible.** Removing chain token injection reverts to current behavior
   with no other changes required.

4. **Bounded blast radius.** `causal_chain_focus` contains at most 5 items
   (pre-filtered by `build_memory_summary()`). The maximum influence is 5
   additional tokens in the query. The retrieval scoring formula is unchanged.

5. **Currently inert.** `pedagogical_memory.difficult_causal_chains` is empty
   for Nazareth (skills = {}). The influence pathway exists but fires on zero
   cases today, making snapshot drift essentially impossible in the near term.

6. **Clean governance.** Chain IDs are opaque structural identifiers. They
   carry no examiner authority, no scoring semantics, and no grading claims.

**Second choice (if causal_chain_focus is deferred):**
`review_topics` → query expansion with a `planning_confidence > 0.3` gate.
This has slightly higher snapshot risk because `known_weak_areas` is populated
for Nazareth (25 entries), meaning the influence would be live immediately.

---

## Section 7 — Prohibited Future Directions

The following directions are permanently forbidden regardless of future phases.
They may not be proposed, designed, or prototyped without first amending this
document with explicit architectural review.

### Permanently forbidden

**Planner-driven grading or scoring**
The planner may never assign, compute, suggest, or imply an exam score, pass
probability, grade, or readiness rating. The system is exam-adjacent, not an
examiner. This distinction must never erode.

**Planner-driven examiner authority**
The planner may never set `safe_for_examiner=True` or `examiner_scoring_allowed=True`.
These flags are immutable governance invariants.

**Hidden retrieval overrides**
The planner may never silently override retrieval results without a traceable,
auditable mechanism. Any planner influence on retrieval must appear in the
`retrieval_plan.pedagogical_priority_boost` or an equivalent named, inspectable field.

**Opaque ranking manipulation**
The planner may never inject priority weights directly into the scoring formula
without being expressed as a named, constant-governed parameter. Retrieval
scoring must remain fully deterministic from its explicit inputs.

**Planner-generated content**
The planner may never produce freeform text, hints, or pedagogical commentary
that is passed directly to the Tutor as if it were retrieved content. All Tutor
content must come from the corpus.

**Planner-driven LES inflation**
The planner may never write to `epistemic_state.json` directly or increment
`session_count` or mastery scores. LES writes are `les_reconciler.py`'s domain.

**Planner as self-eval judge**
The planner may never be used to evaluate the quality of Tutor answers, assign
comparator labels, or influence the self-eval scoring pipeline.

**Cross-session memory via planner**
The planner may never read prior session answers or queries from any source.
Its inputs are LES signals and the current pre-pass result — nothing else.

---

## Migration path from this document

```
Phase 3A.0 (this document)
    Boundary defined, no code changes.

Phase 3A.1 (next)
    Implement causal_chain_focus → query expansion.
    Entry criteria (Section 5) must be fully met.
    Parity and isolation tests written before implementation.
    Snapshot suite run before and after.

Phase 3B (future)
    Evaluate review_topics → query expansion.
    Requires: Phase 3A.1 green + confidence threshold analysis.

Phase 3C (future)
    Evaluate difficulty_progression → Tutor depth.
    Requires: Phase 3B green + depth semantics finalized.

Phase 4 (future)
    _pedagogical_priority_boost() retired.
    strategic_planner becomes sole planning authority.
    Full semantic contract migration complete.
```

---

*This document is an architectural governance record. It does not represent
WSET assessment or examiner evaluation authority. All governance invariants
(`safe_for_examiner=False`, `examiner_scoring_allowed=False`) remain unchanged.*

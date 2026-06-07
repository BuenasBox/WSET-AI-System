# Phase 4A.3.9.2 — Adaptive Loop Final Implementation

**Date:** 2026-06-06  
**Status:** Implemented and green

---

## Summary

This phase closes the adaptive learning loop:

```
Learning Event Runtime → LES/Memory → Next Session Signals
→ Adaptive Signal Consumer → Adaptive Composer v1
→ Session Composer (priority input) → Nueva sesión → Nuevo evento formativo
```

---

## Components Created

### `tools/learner_model/adaptive_signal_consumer.py`

Consolidates signals from multiple LES/memory sources into a structured signal dict consumed by the Adaptive Composer.

**Entry point:** `consume_adaptive_signals(next_session_signals, les, memory) -> dict`

**Output keys:**
- `reinforcement_targets` — topics/items needing reinforcement (weak confidence, negative RA performance, recurrent misconceptions, difficult causal chains)
- `progression_targets` — topics with sustained high confidence, ready for greater challenge
- `review_targets` — unresolved misconceptions and causal gaps to repair directly
- `challenge_targets` — strong topics where distinction-level items are appropriate
- `avoid_repetition_ids` — question IDs seen ≥2 times in the exposure log
- `governance` — invariant block (all False)

**Reading sources:**
- `next_session_signals` (from `build_next_session_signals`)
- `les.topic_signals`, `les.RA_signals`
- `les.misconception_signals`, `les.misconception_resolution`, `les.misconception_sessions`
- `les.causal_chain_signals`, `les.causal_strength`
- `les.question_exposure_log`
- `memory.recurrent_misconceptions`, `memory.difficult_causal_chains`

### `tools/learner_model/adaptive_composer.py`

Decides pedagogical priorities before the Session Composer acts.

**Entry point:** `compose_adaptive_session_plan(session_mode, eligibility_pool, diagnostic_blueprint, adaptive_signals) -> dict`

**Session modes defined (`SESSION_MODE_SIZES`):**

| Mode | Target Size |
|---|---|
| `EXPRESS_10` | 10 |
| `QUICK_25` | 25 |
| `STANDARD_50` | 50 |
| `FULL_DIAGNOSTIC` | 50 |
| `RA_FOCUS` | 15 |

**Output keys:**
- `session_mode` — the requested mode string
- `target_size` — min(mode_size, pool_size)
- `question_priorities` — list[dict] with `question_id`, `priority_score` (ordinal int), `topic`, `ra_id`, `difficulty`; sorted descending
- `reinforcement_rationale`, `progression_rationale`, `challenge_rationale`, `exposure_balancing_rationale`
- `remediation_paths` — WWJ remediation paths for unresolved misconceptions in review_targets
- `governance` — invariant block (all False)

**Priority score scale (ordinal, not percentage):**

| Condition | Score |
|---|---|
| Persistent unresolved misconception | 100 |
| Urgent reinforcement | 80 |
| High reinforcement / high causal gap | 60 |
| Standard reinforcement | 40 |
| Challenge / distinction for strong topic | 20 |
| Base (no signal) | 10 |

---

## Components Modified

### `tools/learner_model/learning_event_runtime.py`

Added `persist_learning_event_result()` — a persistence helper with minimal atomicity:
- Writes memory first (`save_pedagogical_memory`), then LES (`write_learner_state`)
- If memory write fails, LES is not written
- If LES write fails, memory has already been written (caller must handle inconsistency)
- Takes optional `memory_path` and `les_path` overrides for testability
- Returns `{memory_path, les_path, success}`

**No changes to existing pipeline functions** — `process_question_attempt`, `process_open_response_attempt`, `build_next_session_signals` are unchanged.

---

## Complete Adaptive Loop Flow

```
1. Student answers question (SBA or OR)
   ↓
2. process_question_attempt() / process_open_response_attempt()
   → returns: les, cognitive_map, next_session_signals, emitted_signals
   ↓
3. persist_learning_event_result() [optional caller step]
   → writes memory (first), then LES
   ↓
4. build_next_session_signals(memory, les)
   → review_topics, misconception_repair_candidate, causal_chain_reinforcement_candidate
   ↓
5. consume_adaptive_signals(next_session_signals, les, memory)
   → reinforcement_targets, progression_targets, review_targets, challenge_targets, avoid_repetition_ids
   ↓
6. compose_adaptive_session_plan(session_mode, pool, blueprint, adaptive_signals)
   → question_priorities (sorted), remediation_paths, rationales
   ↓
7. [Integration point] Session Composer orders its pool using question_priorities
   → Nueva sesión con preguntas priorizadas pedagógicamente
   ↓
8. Student answers → GOTO 1
```

---

## Pedagogical Rules Implemented

### Reinforcement rules
- Weak topic (confidence_level in `not_recorded|low`, exposure > 0) → `reinforcement_target` with priority `high` (or `urgent` if ≥2 incorrect)
- Negative RA performance (incorrect > correct) → `reinforcement_target` with priority `urgent|high`
- Recurrent misconception in memory (hits ≥ 2) → `reinforcement_target` priority `urgent|high`
- Difficult causal chain (hits ≥ 1) → `reinforcement_target` priority `high|standard`

### Progression rules
- High confidence topic (correct > incorrect, total ≥ 2) → `progression_target` with `learning_stage: ready_for_greater_challenge`
- Strong RA (correct > 2×incorrect, trend improving/stable, total ≥ 3) → `progression_target`
- Items for progression topics at foundational difficulty → score reduced by 10 (avoid basic repetition)

### Misconception repair rules
- Persistent unresolved misconception (seen in >1 session, resolved=False) → `review_target` with `gap_priority: high`
- Priority score in Adaptive Composer: 100 (maximum)
- Resolved misconceptions excluded from review_targets

### Causal gap rules
- Superficial causal chain (strength="superficial", exposure > 0) → `review_target` with `gap_priority: high`
- Items with matching `causal_chain_id` in their curriculum → priority score boosted to 60

### Exposure control rules
- Questions appearing ≥ _EXPOSURE_THRESHOLD (2) times in LES exposure log → `avoid_repetition_ids`
- Items in avoid_repetition_ids → excluded from question_priorities entirely
- Items with same topic seen twice already in pool → score reduced by 15

---

## WWJ Integration in the Adaptive Loop

When `review_targets` contains unresolved misconception entries:

1. `compose_adaptive_session_plan` calls `get_remediation_path(mc_id)` for each unresolved MC_ID
2. Includes in `adaptive_session_plan.remediation_paths`: `[{mc_id, wwj_chunks, availability, remediation_message}]`
3. Resolved misconceptions (`resolved=True`) are excluded from remediation lookups
4. WWJ does not modify question content, answer evaluation, or scoring

---

## OR Integration in the Adaptive Loop

`process_open_response_attempt()` was implemented in Phase 4A.3.9.2 (before this phase) and is fully compatible:

- Returns same top-level shape as `process_question_attempt()` (same keys)
- Updates `les.causal_chain_signals` via `update_les_causal()`
- Updates `memory.difficult_causal_chains` for absent chains
- Processes `mc_ids_relevant` as SBA-like misconception signals
- Builds `next_session_signals` from updated memory and LES
- Its output feeds directly into `consume_adaptive_signals()`

---

## Persistence State

### Current mechanism
- `write_learner_state(les, path)` — in `tools/orchestrator/learner_state.py`
- `save_pedagogical_memory(memory, path)` — in `tools/learner_model/knowledge_tracing.py`
- `persist_learning_event_result(result)` — new, in `learning_event_runtime.py` — wraps both with memory-first ordering

### Write order convention (established this phase)
`memory first → LES second`. Rationale: memory is the richer cognitive artifact. If LES write fails, memory still reflects the most recent learning event. If memory write fails, no disk state is changed.

### Atomicity
No true transactions exist. The helper provides minimal ordering guarantees. For production use, the caller should wrap `persist_learning_event_result` in a try/except and handle partial writes (e.g., retry or log for manual reconciliation).

---

## Dashboard

**Status: Omitted.** The `frontend/architecture-dashboard/system_state.json` is manually maintained and there is no automated pipeline to derive `reinforcement_target_count`, `progression_target_count`, `misconception_repair_count`, `causal_repair_count` from live LES without reading private learner artifacts. Adding static zeros would be misleading. 

**Pending integration point:** when a session summary pipeline exists that reads from ledger output (not raw LES), these four counts can be added to `system_state.json` in 4 lines.

---

## Session Composer Integration Point

`tools/question_generation/sba_session_composer.py` does NOT yet accept `question_priorities` as input. The current Session Composer:
- Takes `ra`, `topic`, `difficulty`, `session_size`, `collection` filters
- Performs its own duplicate-deferral logic via `_concept_signature`

**Planned integration:** The caller (e.g., an orchestration layer) should:
1. Call `compose_adaptive_session_plan` to get `question_priorities`
2. Sort the candidate pool by `priority_score` (descending)
3. Pass the sorted pool to `select_sba_session_items` (which already accepts a `master_bank` param)

No changes to Session Composer internals are needed — the ordering happens at the pool level before selection.

---

## Tests Added

File: `tests/test_adaptive_loop_phase4a392.py` — **59 tests** across 15 test classes.

| Test | Description |
|---|---|
| 1 | Weak topic → reinforcement_targets with high priority |
| 2 | Strong topic → progression_targets with ready_for_greater_challenge |
| 3 | Persistent unresolved misconception → review_targets with high gap_priority |
| 4 | Superficial causal chain → review_targets with high gap_priority |
| 5 | WWJ remediation_paths present when mc has availability="available" |
| 6 | avoid_repetition_ids excludes items from question_priorities |
| 7 | Adaptive Composer changes priority order vs pool order |
| 8 | Session Composer unaffected by adaptive plan; plan IDs are valid strings |
| 9 | EXPRESS_10 → target_size = 10 |
| 10 | QUICK_25 → target_size = 25 |
| 11 | STANDARD_50 → target_size = 50 |
| 12 | FULL_DIAGNOSTIC → target_size > 0 (= 50) |
| 13 | RA_FOCUS → target_size = 15 |
| 14 | process_open_response_attempt returns shape compatible with process_question_attempt |
| 15 | No output contains score, percentage, pass/fail, WSET grade labels |
| 16 | governance always safe_for_examiner=False, examiner_scoring_allowed=False |
| 17 | Public Lab collection remains 36 items (SBA export dry-run) |
| 18 | (Slow golden) Executed separately — see verification section |

---

## Verification Results

```
Suite:         1653 OK, 9 skipped
New tests:     59 (all pass)
Slow golden:   7/7 (unchanged — no retrieval/Tutor changes)
Public Lab:    36 (confirmed)
Governance:    All invariants intact
Snapshots:     35 (unchanged)
```

---

## Pending Risks

1. **Session Composer integration:** `question_priorities` from the Adaptive Composer are not yet consumed by Session Composer. The ordering step must be added at the orchestration caller level.
2. **Persistence atomicity:** True atomic writes require a transaction layer not present in this deterministic local system. The current `persist_learning_event_result` helper provides ordering guarantees only.
3. **Dashboard integration:** Adaptive signal counts not yet surfaced to dashboard — requires a ledger-based summary pipeline.
4. **RA_FOCUS size is fixed at 15:** The architecture doc specifies 10–30 configurable. The `SESSION_MODE_SIZES` dict hardcodes 15. A future enhancement should accept a `ra_focus_size` parameter.
5. **FULL_DIAGNOSTIC vs STANDARD_50 both = 50:** Currently both modes target 50 items. Differentiation (e.g., FULL_DIAGNOSTIC uses all RAs, STANDARD_50 is topic-focused) is not yet implemented in the Adaptive Composer.

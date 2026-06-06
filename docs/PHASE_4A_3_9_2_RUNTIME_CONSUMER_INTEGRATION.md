# Phase 4A.3.9.2 — Runtime Consumer Integration

**Implemented:** 2026-06-06
**Status:** Complete

---

## What this phase closed

Three integration gaps identified by direct code inspection were preventing the Learning Event Runtime from forming a closed loop between SBA/OR outcomes and the Adaptive Composer.

---

## Runtimes that existed before this phase

| Module | Purpose |
|--------|---------|
| `tools/learner_model/misconception_runtime.py` | Converts SBA distractor selections into LES misconception_signals, cross-session persistence tracking, and resolved flags |
| `tools/learner_model/causal_runtime.py` | Converts OR causal coverage into LES causal_chain_signals, demonstrated_count, and causal_strength |
| `tools/learner_model/wwj_remediation.py` | Looks up WWJ chunk IDs for a given MC_ID from the static mc_wwj_lookup.json |
| `tools/learner_model/open_response_evaluator.py` | Composes causal_runtime + wwj_remediation into a complete OR evaluation result |

All four existed as standalone modules. None were wired into a single pipeline function.

---

## The three connections that were missing

### Gap 1 — WWJ chunks never entered the SBA pipeline

`learning_event_runtime._remediation_route()` was supposed to call
`wwj_remediation.get_remediation_path()` when an SBA outcome triggered a misconception,
but the function did not exist. WWJ chunk IDs were computed by the evaluator only
for OR items; SBA wrong answers with a known `mc_id` had no remediation path.

**Fixed by:** `_remediation_route(mc_id, outcome)` in `learning_event_runtime.py`.
When `outcome="incorrect"` and `mc_id` is known, calls `get_remediation_path(mc_id)`
and returns `{remediation_available, remediation_message, wwj_chunks, remediation_source: "wwj_lookup"}`.

### Gap 2 — Next-session signals read memory only, not the LES

`build_next_session_signals(memory, les)` accepted `les` as a parameter but only
read from `memory.recurrent_misconceptions` and `memory.difficult_causal_chains`.
It never read:
- `les.misconception_signals` → per-node detection_count
- `les.misconception_sessions` → session_ids for cross-session persistence
- `les.misconception_resolution` → resolved flag per mc_id
- `les.causal_chain_signals` → exposure_count and demonstrated_count per cc_id
- `les.causal_strength` → "superficial"|"developing"|"strong" per cc_id

The Adaptive Composer therefore could not see LES-level persistence or causal strength.

**Fixed by:** `build_next_session_signals()` now reads all five LES keys and produces:
- `misconception_repair_candidate` — per-mc_id dict with `persistence`, `resolved`, `priority`
  (resolved misconceptions are excluded; persistent+unresolved → `priority="high"`)
- `causal_chain_reinforcement_candidate` — per-cc_id dict with `causal_strength`, `gap_priority`
  (superficial + exposure > 0 → `gap_priority="high"`)

### Gap 3 — No pipeline function for Open Response attempts

`open_response_evaluator.evaluate_open_response()` was standalone. Nothing connected it to:
- LES causal_chain_signals (via `update_les_causal`)
- `memory.difficult_causal_chains`
- LES misconception_signals (via `process_sba_outcome`)
- WWJ chunk collection for `mc_ids_relevant`
- next_session_signals generation

**Fixed by:** `process_open_response_attempt()` in `learning_event_runtime.py`.

---

## New file

**`tools/learner_model/learning_event_runtime.py`**

Public API:

```python
process_question_attempt(
    *, student_answer, question_id, session_id, mode, timestamp,
    question_item, memory, les, mc_id=None
) -> dict
```

```python
process_open_response_attempt(
    *, student_response_text, question_id, session_id, mode, timestamp,
    or_item, memory, les
) -> dict
```

```python
build_next_session_signals(memory, les) -> dict
```

```python
build_diagnostic_outcome(*, outcome, question_id, mc_id) -> dict
```

Both pipeline functions return the same top-level shape:
```python
{
    "attempt": {...},
    "diagnostic_outcome": {...},
    "formative_event": {...},
    "cognitive_map": {...},           # updated memory (not mutated from input)
    "cognitive_map_change_set": {...}, # top-level keys that changed
    "les": {...},                     # updated LES (not mutated from input)
    "les_change_set": {...},          # top-level keys that changed
    "emitted_signals": [...],
    "next_session_signals": {...},
    "governance": {...},
}
```

---

## SBA pipeline — end-to-end flow

```
Caller: student selects option B on question q1
  mc_id = "MC_ACIDITY_01"   (caller supplies distractor → mc_id mapping)
    │
    ▼
process_question_attempt(student_answer="B", question_item={correct_answer: "A"}, mc_id=..., ...)
    │ outcome = "incorrect"
    │
    ├─► misconception_runtime.process_sba_outcome(les, mc_id, outcome="incorrect", session_id)
    │     writes: les.misconception_signals[mc_id].detection_count++
    │     writes: les.misconception_sessions[mc_id].session_ids.append(session_id)
    │     emits:  ["misconception_triggered"]  (+ "misconception_persistent" if >1 session)
    │
    ├─► build_diagnostic_outcome()
    │     └─► _remediation_route(mc_id="MC_ACIDITY_01", outcome="incorrect")
    │             └─► wwj_remediation.get_remediation_path("MC_ACIDITY_01")
    │                   returns: {wwj_chunks: [...], availability: "available", ...}
    │
    ├─► memory.recurrent_misconceptions[mc_id].hits++
    │
    └─► build_next_session_signals(updated_memory, updated_les)
          reads les.misconception_signals   → detection_count
          reads les.misconception_sessions  → persistence
          reads les.misconception_resolution → resolved
          reads les.causal_chain_signals    → exposure/demonstrated
          reads les.causal_strength         → "superficial"|"developing"|"strong"
          returns: { misconception_repair_candidate, causal_chain_reinforcement_candidate }
```

---

## Open Response pipeline — end-to-end flow

```
Caller: student submits free-text response for OR_002
    │
    ▼
process_open_response_attempt(student_response_text, or_item, memory, les, ...)
    │ cc_ids_targeted = or_item["causal_chain_target"]  (e.g. ["CC_MLF_ACIDITY", "CC_OAK_TANNIN"])
    │ mc_ids_relevant = or_item.get("mc_ids_relevant", [])
    │
    ├─► open_response_evaluator.evaluate_open_response(response, question_context)
    │     └─► causal_runtime.detect_cc_coverage() → (chains_present, chains_absent)
    │     └─► wwj_remediation.get_remediation_path() for each mc_id_relevant
    │     returns: {profile, concept_coverage, causal_coverage, remediation, governance}
    │
    ├─► causal_runtime.update_les_causal(les, cc_ids_targeted, chains_present)
    │     writes: les.causal_chain_signals[cc_id].exposure_count++
    │     writes: les.causal_chain_signals[cc_id].demonstrated_count++ (if present)
    │     writes: les.causal_strength[cc_id] = "superficial"|"developing"|"strong"
    │     emits:  ["causal_gap_detected" | "causal_chain_demonstrated", "causal_strength_updated"]
    │
    ├─► memory.difficult_causal_chains[cc_id].hits++ (for each cc_id in chains_absent)
    │
    ├─► For each mc_id in mc_ids_relevant:
    │     mc_outcome = "correct" if all chains present, "incorrect" if any absent
    │     misconception_runtime.process_sba_outcome(updated_les, mc_id, mc_outcome, session_id)
    │
    ├─► wwj_remediation.get_remediation_path(mc_id) for each mc_id_relevant
    │     → wwj_chunks collected and deduplicated into diagnostic_outcome.remediation.wwj_chunks
    │
    └─► build_next_session_signals(updated_memory, updated_les)
```

---

## What next_session_signals now exposes (new vs before)

| Signal field | Before 4A.3.9.2 | After 4A.3.9.2 |
|---|---|---|
| `review_topics` | From memory.recurrent_misconceptions | Same (unchanged) |
| `misconception_repair_candidate` | Not present | Per-mc_id: persistence, resolved, priority |
| `causal_chain_reinforcement_candidate` | Not present | Per-cc_id: causal_strength, gap_priority |

`misconception_repair_candidate[i].persistence` — True if the mc_id has been triggered in more than one distinct session (from `les.misconception_sessions`).

`misconception_repair_candidate[i].resolved` — True if a correct answer was given after prior triggers (from `les.misconception_resolution`). Resolved misconceptions are excluded from the list.

`causal_chain_reinforcement_candidate[i].causal_strength` — Current strength from `les.causal_strength`: "superficial" | "developing" | "strong". Driven by demonstrated/exposure ratio from `causal_runtime`.

`causal_chain_reinforcement_candidate[i].gap_priority` — "high" when strength is "superficial" and exposure_count > 0 (the student has been exposed but repeatedly fails to articulate the chain).

---

## What remains pending for Adaptive Composer

- **Distractor → MC_ID mapping** — `process_question_attempt()` requires the caller to supply `mc_id` explicitly. No automated lookup from question distractor IDs to MC_IDs exists yet.
- **mc_ids_relevant in OR items** — The open_response_bank.json does not currently populate `mc_ids_relevant`; the field is reserved for future items that have explicit misconception links.
- **Adaptive Composer consumption** — `next_session_signals` is now populated with persistence and causal_strength data. The Adaptive Composer has not yet been written to consume these signals for session composition.
- **LES persistence** — Both pipeline functions return updated LES and memory dicts. The caller must call `write_learner_state()` and `save_pedagogical_memory()` to persist changes.

---

## Governance invariants

All outputs from `learning_event_runtime.py` enforce:
- `safe_for_examiner = False`
- `examiner_scoring_allowed = False`
- `uses_llm = False`
- `uses_api = False`
- `uses_embeddings = False`
- `uses_vector_db = False`
- `cloud_services_active = False`

Forbidden strings never appear in any output: `WSET_PASS`, `WSET_MERIT`, `WSET_DISTINCTION`.
No scoring labels, no percentage values, no pass/fail determinations.

---

## Test coverage added

**File:** `tests/test_learning_event_runtime_integration.py` — 44 tests across 8 classes.

| Class | Coverage |
|---|---|
| `TestWwjRemediationInSbaOutcome` | WWJ chunks for available/pending mc_ids; correct answer no chunks; no mc_id → None routing |
| `TestNextSessionSignalsReadLes` | Persistence detection from LES sessions; resolved exclusion; priority logic; causal_strength in candidates; gap_priority thresholds |
| `TestOpenResponseAttemptCallsEvaluator` | Profile classification delegation; formative event type; chains_present/absent in output |
| `TestOpenResponseLesUpdate` | causal_chain_signals updated; difficult_causal_chains updated; change_sets reflect changes |
| `TestOpenResponseWwjRemediation` | wwj_chunks for mc_ids_relevant with available mc; empty mc_ids_relevant handled |
| `TestOpenResponseMisconcepSignals` | mc_ids_relevant triggers process_sba_outcome; repair_candidate populated |
| `TestGovernanceNoForbiddenStrings` | No forbidden strings in any output; all governance flags false |
| `TestReturnShapeContract` | Both functions return identical top-level key set; no input mutation |
| `TestBuildDiagnosticOutcome` | Direct unit tests for the diagnostic builder |

---

## Verification results

```
python -m unittest discover -s tests -v
  Ran 1594 tests — OK (skipped=9)   [was 1550 before this phase]

SBA export dry-run: 36 eligible, 0 errors

Slow Golden (RUN_SLOW_TESTS=1):
  Ran 7 tests in ~31s — OK
```

Question bank counts unchanged:
- Total master bank: 616
- SBA items: 595 (36 public_lab eligible)
- OR bank: 20 items
- Governance: all flags False throughout

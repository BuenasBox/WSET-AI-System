# Phase 4A.3.8.7 — Knowledge Runtime Consumers & Open Response Evaluator

**Implemented:** 2026-06-06
**Status:** Complete

---

## What was implemented

Four new runtime consumer modules that convert static contract files into live
behavioral components integrated with the Learner Epistemic State (LES).

---

## Components and file locations

### A. Misconception Runtime Consumer
**File:** `tools/learner_model/misconception_runtime.py`

Reads `knowledge/knowledge-map/misconception_signals.json` at initialization (cached).
Exposes `process_sba_outcome(les, *, mc_id, outcome, session_id)`.

When an SBA item is answered:
- `outcome="incorrect"` + known `mc_id` → increments `detection_count` in LES
  `misconception_signals`, records session in `misconception_sessions`, emits
  `misconception_triggered` (and `misconception_persistent` if the MC has appeared
  in more than one distinct session).
- `outcome="correct"` + prior detections → marks resolved in `misconception_resolution`,
  emits `misconception_resolved`.

LES extensions (runtime-only top-level keys, persisted via `_with_governance_defaults`):
- `misconception_sessions[mc_id]` — `{session_ids: [...], first_detected: str}`
- `misconception_resolution[mc_id]` — `{first_detected, resolved, resolved_at}`

Returns `(updated_les, emitted_signals)`. Never writes to disk — caller persists.

---

### B. Causal Chain Runtime Consumer
**File:** `tools/learner_model/causal_runtime.py`

Reads `knowledge/knowledge-map/causal_chain_signals.json` and all
`knowledge/knowledge-map/causal-chains/*.json` files at initialization (cached).

Exposes:
- `get_keyword_hints(cc_id)` — returns keyword list for deterministic text matching.
  Uses `trigger_keywords` from governance/hybrid schema CC files; falls back to
  token-based derivation from the CC_ID string for legacy schema files.
- `detect_cc_coverage(student_response, cc_ids_targeted)` → `(chains_present, chains_absent)`
- `update_les_causal(les, *, cc_ids_targeted, chains_present)` → `(updated_les, emitted_signals)`

LES updates:
- `causal_chain_signals[cc_id].exposure_count` — incremented per targeted CC_ID
- `causal_chain_signals[cc_id].demonstrated_count` — incremented per articulated CC_ID
- `causal_strength[cc_id]` — `"superficial" | "developing" | "strong"` (runtime-extension key)

Emitted signals: `causal_gap_detected`, `causal_chain_demonstrated`, `causal_strength_updated`.

`causal_strength` thresholds:
- `demonstrated / exposure < 0.4` → `"superficial"`
- `0.4 ≤ ratio < 0.8` → `"developing"`
- `ratio ≥ 0.8` → `"strong"`

---

### C. WWJ Remediation Runtime
**File:** `tools/learner_model/wwj_remediation.py`

Reads `knowledge/knowledge-map/mc_wwj_lookup.json` at initialization (cached).

Exposes `get_remediation_path(mc_id) -> dict` (matches `RemediationPath` TypedDict).

Return fields:
- `mc_id` — the requested MC_ID
- `wwj_chunks` — list of verified chunk IDs from the WWJ corpus (empty if pending)
- `availability` — `"available"` | `"partial"` | `"pending"`
- `content_type` — e.g. `"theory_explanation"`, `"sat_explanation"`, or `None`
- `remediation_message` — static explanatory text (no LLM generation)

For unknown MC_IDs, returns `availability="pending"` and empty chunks.
Never calls external services. Never exposes `safe_for_examiner` in output.

---

### D. Open Response Evaluator v1
**File:** `tools/learner_model/open_response_evaluator.py`

Composes causal_runtime and wwj_remediation into a complete evaluation pipeline.

**Input:**
```python
{
  "student_response": str,
  "question_context": {
    "cc_ids_targeted": [str],   # CC_IDs the question targets
    "mc_ids_relevant": [str],   # MC_IDs relevant to this question
    "topic": str,
    "ra_id": str
  }
}
```

**Output:**
```python
{
  "profile": "FOUNDATIONAL_RESPONSE" | "DEVELOPING_RESPONSE" | "STRONG_RESPONSE",
  "concept_coverage": {"concepts_present": [...], "concepts_absent": [...]},
  "causal_coverage": {"chains_present": [...], "chains_absent": [...]},
  "reasoning_quality": "superficial" | "developing" | "strong",
  "remediation": {
    "concepts_to_reinforce": [...],
    "causality_to_reinforce": [...],
    "wwj_chunks": [...]   # chunk_ids from lookup, not invented
  },
  "governance": {
    "safe_for_examiner": False,
    "examiner_scoring_allowed": False,
    "official_wset_question": False,
    "training_item_only": True
  }
}
```

**Profile thresholds:**
- `FOUNDATIONAL_RESPONSE`: coverage_ratio < 0.50
- `DEVELOPING_RESPONSE`: 0.50 ≤ coverage_ratio < 0.80
- `STRONG_RESPONSE`: coverage_ratio ≥ 0.80

Coverage is computed as `len(chains_present) / len(cc_ids_targeted)`.
All evaluation is deterministic text matching — no LLM, no embeddings.

**Forbidden strings** (never appear in any output, constant, or comment):
`WSET_PASS`, `WSET_MERIT`, `WSET_DISTINCTION`

Internal lab-only profile constants (`_LAB_PROFILE_ACCEPTABLE`,
`_LAB_PROFILE_MERIT`, `_LAB_PROFILE_DISTINCTION`) exist as private module
constants and are never returned in default output.

---

## How components connect

```
SBA outcome (incorrect/correct)
    │
    ▼
misconception_runtime.process_sba_outcome()
    │ writes → LES misconception_signals, misconception_sessions, misconception_resolution
    │ emits  → misconception_triggered, misconception_persistent, misconception_resolved
    │
    └── if triggered → wwj_remediation.get_remediation_path(mc_id)
                           │ returns → wwj_chunks, availability, remediation_message
                           │ (caller decides whether to surface to Tutor)

Open response submitted
    │
    ▼
open_response_evaluator.evaluate_open_response()
    │ calls → causal_runtime.detect_cc_coverage()
    │ calls → wwj_remediation.get_remediation_path() for each mc_id_relevant
    │ returns → profile, coverage, remediation, governance
    │
causal_runtime.update_les_causal()
    │ writes → LES causal_chain_signals (exposure + demonstrated), causal_strength
    │ emits  → causal_gap_detected, causal_chain_demonstrated, causal_strength_updated
```

---

## Signals emitted by each consumer

| Consumer | Signal | Meaning |
|----------|--------|---------|
| Misconception Runtime | `misconception_triggered` | Student selected a distractor linked to this MC_ID |
| Misconception Runtime | `misconception_persistent` | MC_ID has appeared in > 1 distinct session |
| Misconception Runtime | `misconception_resolved` | Correct answer given after prior trigger |
| Causal Runtime | `causal_gap_detected` | Targeted CC_ID not articulated in response |
| Causal Runtime | `causal_chain_demonstrated` | Targeted CC_ID detected in response |
| Causal Runtime | `causal_strength_updated` | Strength label changed for a CC_ID |

All signals are returned as strings in a list — never written to UI or triggered
as side effects from within these modules.

---

## What was NOT implemented

- **Adaptive Composer** — pending real item data linking MC_IDs to specific SBA distractors.
  As of 2026-06-06, `sba_distractors_linked=false` for all 20 misconception nodes and all
  32 causal chain nodes in the signal files. The runtime consumers are ready; the input data
  (which distractor → which MC_ID) is not yet wired from the question bank.
- **SBA distractor → MC_ID linkage** — `process_sba_outcome` requires the caller to supply
  `mc_id` explicitly. The lookup from `distractor_id → mc_id` is not yet automated.
- **LES persistence on every outcome** — consumers return an updated LES dict; callers must
  call `write_learner_state(updated_les, les_path)` to persist. No auto-persistence.
- **Tutor-facing delivery of remediation** — `get_remediation_path` returns a path dict;
  the Tutor layer consuming it is not yet wired.

---

## Governance invariants

All four modules enforce:
- `safe_for_examiner = False` (never overridden)
- `examiner_scoring_allowed = False` (never overridden)
- No LLM, API, embeddings, vector DB, or cloud service calls
- No writes outside of the returned dict (caller controls persistence)
- `ENABLE_PEDAGOGICAL_STRATEGY_LAYER = False` — not activated

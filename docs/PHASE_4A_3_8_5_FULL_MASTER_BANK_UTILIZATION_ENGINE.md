# Phase 4A.3.8.5 - Full Master Bank Utilization Engine

## Status

Implemented as private, deterministic infrastructure.

This phase makes the canonical 616-record Master Bank available to governed
session composition without changing the 36-item public lab, frontend,
deployment, Tutor, Retrieval, Open Response Runtime, golden baseline, or
snapshots.

## Architecture

### Diagnostic Blueprint

`knowledge/diagnostic/diagnostic_blueprint.json` defines:

- RA1-RA5 distribution;
- foundational/intermediate/distinction targets;
- topic-diversity policy;
- session composition;
- deterministic fallback rules;
- governance defaults.

Modes:

| Mode | Default size |
|---|---:|
| `EXPRESS_10` | 10 |
| `QUICK_25` | 25 |
| `STANDARD_50` | 50 |
| `FULL_DIAGNOSTIC` | 100 |
| `RA_FOCUS` | 25, configurable |

`RA_FOCUS` requires an explicit RA1-RA5 target. The other modes use fixed
cross-RA distributions.

### Master Bank Eligibility

`tools/question_generation/master_bank_eligibility.py` classifies every
canonical record at runtime. It does not rewrite question content or activate
records publicly.

Primary categories:

| Category | Count | Meaning |
|---|---:|---|
| `public_lab` | 36 | Existing stable public laboratory |
| `private_practice` | 536 | Structurally usable private SBA records |
| `open_response_candidate` | 20 | Approved records; explicit opt-in only |
| `inactive` | 24 | Preserve/revision/rejected or structurally unusable |
| `adaptive_candidate` | 0 primary | Capability flag only, never activation |

`adaptive_candidate` is a secondary category on 569 records with usable RA and
difficulty metadata. It prepares a future adaptive layer but is not consumed
as an adaptive decision in this phase.

Public records also carry `private_practice`, because publication status and
private eligibility are independent. The 36-item public payload remains
unchanged.

### Session Composer v1

`tools/question_generation/full_master_bank_session_composer.py` consumes:

- the canonical Master Bank;
- the Diagnostic Blueprint;
- a LES snapshot.

Selection order is deterministic:

1. remove inactive records;
2. apply mode and RA constraints;
3. prefer questions outside recent LES history;
4. prefer lower `exposure_count`;
5. fill interleaved RA and difficulty slots;
6. apply the topic cap as a soft diversity constraint;
7. redistribute unavailable quota within the active pool;
8. report composition shortfalls explicitly.

The same bank, blueprint, LES and parameters produce the same ordered item IDs
and the same content-derived `session_id`.

Default sessions are SBA-only. `FULL_DIAGNOSTIC` and `RA_FOCUS` can include
approved Open Response candidates only when the caller explicitly passes
`include_open_response=True`. This produces descriptors only; it does not call
or modify Open Response Runtime.

The pre-existing `sba_session_composer.py` remains unchanged and continues to
serve only the 36-item `public_lab`.

## LES Tracking

`tools/orchestrator/learner_state.py` now adds:

```json
"question_exposure_signals": {
  "wset3_83": {
    "question_id": "wset3_83",
    "exposure_count": 2,
    "last_seen": "2026-06-06T12:00:00Z",
    "recent_history": []
  }
}
```

Limits:

- 20 recent entries per question;
- 500 entries in the global exposure log.

`record_session_observations()` captures:

- question exposure count, last seen and recent history;
- topic exposure;
- topic correct/incorrect observations;
- explicit topic confidence;
- explicit topic weakness;
- RA1-RA5 exposure;
- RA correct/incorrect performance indicators.

Confidence, weakness and RA trend are not inferred automatically. No official
score, grade, percentage, pass/fail, proficiency equivalence, or examiner
authority is produced.

## Dashboard Integration Data

`tools/dashboard/master_bank_utilization_data.py` is a pure projection. It
returns:

- total bank size;
- active private pool;
- eligibility counts;
- current session composition;
- RA coverage and performance indicators;
- topic coverage, confidence and weakness;
- question exposure and repetition statistics.

It does not read private LES files itself, modify frontend files, or deploy.
The caller must supply the LES snapshot explicitly.

## Data Reality and Fallback

The canonical bank currently contains:

- 602 `intermediate`;
- 10 `distinction`;
- 4 `foundational`.

Therefore, larger blueprint modes cannot meet their intended difficulty
distribution exactly. The composer does not relabel items or manufacture
difficulty. It preserves RA coverage, redistributes unavailable slots, and
emits `difficulty_shortfall:*` warnings.

This is the main residual data risk. It is metadata scarcity, not a composer
failure.

## Governance Boundary

All new payloads enforce:

```json
{
  "safe_for_examiner": false,
  "examiner_scoring_allowed": false,
  "uses_llm": false,
  "uses_api": false,
  "uses_embeddings": false,
  "uses_vector_db": false,
  "cloud_services_active": false
}
```

No public activation, UI integration, deployment, recommendation engine, or
adaptive progression is included.

## Verification

Executed commands:

```powershell
python -m unittest discover -s tests -v
python -m tools.question_generation.export_static_demo_questions --dry-run
$env:RUN_SLOW_TESTS=1; python -m unittest tests.test_golden_self_eval -v
```

Focused coverage is in:

- `tests/test_full_master_bank_utilization_engine.py`
- `tests/test_learner_state_foundation.py`

The final command results and commit are reported in the implementation
handoff for this phase.

Results:

- full suite: 1522 tests, 9 skipped, 0 failures;
- SBA export dry run: 36 eligible items, 0 validation errors;
- Slow Golden: 7/7 OK;
- Tutor snapshots: 25/25 unchanged.

During the gate, Slow Golden exposed a pre-existing comparator mismatch:
official WSET chunks were marked `shallow_retrieval` unless their metadata
contained the legacy literal `high` or `golden`. The comparator now treats
official WSET source chunks as curated priority support. Retrieval, Tutor and
the golden baseline were not changed. A focused regression test covers this
case.

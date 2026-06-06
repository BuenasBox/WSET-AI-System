# Phase 4A.3.8.3 - Learner State Foundation

## Status

Implemented as inactive infrastructure.

This phase extends the local Learner Epistemic State (LES) with deterministic
storage contracts required by future adaptive learning work. It does not add an
Adaptive Engine, alter question selection, influence Tutor or Retrieval, expose
a frontend, or activate any runtime behavior.

## Compatibility Boundary

The extension is additive and retains:

```json
"schema_version": "minimal_brain_v2"
```

Existing LES documents load with defaults for all new fields. Existing unknown
fields are preserved. `build_les_context()` intentionally does not expose the
new signal containers, so current Tutor, Retrieval, planner, and orchestrator
behavior remains unchanged.

## Top-Level LES Extension

```json
{
  "topic_signals": {},
  "RA_signals": {
    "RA1": {},
    "RA2": {},
    "RA3": {},
    "RA4": {},
    "RA5": {}
  },
  "misconception_signals": {},
  "causal_chain_signals": {},
  "question_exposure_log": []
}
```

All counters are non-negative integers. Timestamps are persisted strings. This
layer validates structure only; it does not interpret timestamp chronology.

## Topic Signal Contract

```json
{
  "topic": "cool_climate",
  "exposure_count": 3,
  "correct_count": 2,
  "incorrect_count": 1,
  "confidence_level": "medium",
  "last_seen": "2026-06-06T12:00:00Z"
}
```

Allowed `confidence_level` values:

- `not_recorded`
- `low`
- `medium`
- `high`

Confidence is an explicitly supplied observation. The foundation does not
derive it from correct or incorrect counts.

## RA Signal Contract

One record always exists for each of `RA1` through `RA5`.

```json
{
  "ra_id": "RA1",
  "exposure_count": 4,
  "performance": {
    "correct_count": 3,
    "incorrect_count": 1
  },
  "trend": "stable",
  "last_seen": "2026-06-06T12:00:00Z"
}
```

Allowed `trend` values:

- `not_observed`
- `improving`
- `stable`
- `declining`

Trend is persisted only when supplied by an authorized future producer. This
phase does not calculate it. Performance consists only of observable response
counts and is not an official or unofficial WSET result.

## Misconception Signal Contract

```json
{
  "misconception_id": "MC_ACIDITY_01",
  "detection_count": 2,
  "last_detected": "2026-06-06T12:00:00Z"
}
```

The foundation stores detections. It does not detect misconceptions, infer
severity, schedule interventions, or alter the existing misconception pre-pass.

## Causal Chain Signal Contract

```json
{
  "causal_chain_id": "CC_COOL_CLIMATE_ACIDITY",
  "exposure_count": 4,
  "demonstrated_count": 1
}
```

`demonstrated_count` records an externally supplied observation. This layer
does not evaluate causal reasoning or infer understanding.

## Question Exposure Contract

```json
{
  "question_id": "Q_RA1_001",
  "timestamp": "2026-06-06T12:00:00Z",
  "mode": "diagnostic_sba",
  "result": "incorrect"
}
```

Allowed `result` values:

- `correct`
- `incorrect`
- `unanswered`

Entries are append-only at the contract helper level and preserve insertion
order. No repetition control, deduplication, ranking, recency weighting, or
adaptive question selection is implemented.

## Persistence API

`tools/orchestrator/learner_state.py` provides:

- `load_learner_state()`
- `write_learner_state()`
- `create_topic_signal()`
- `create_ra_signal()`
- `create_misconception_signal()`
- `create_causal_chain_signal()`
- `create_question_exposure()`
- `append_question_exposure()`

Writes normalize the new containers, preserve the input object, use local JSON,
and enforce governance defaults. Invalid optional signal entries are ignored
during deserialization; legacy LES fields remain available.

## Governance

Every load and write enforces:

```json
{
  "safe_for_examiner": false,
  "examiner_scoring_allowed": false,
  "examiner_scoring_active": false,
  "embeddings_active": false,
  "vector_db_active": false,
  "cloud_services_active": false
}
```

The foundation contracts contain no grade, percentage, pass/fail, official
scoring, or proficiency field. `correct` and `incorrect` are question outcome
observations only and do not confer WSET assessment authority.

## Explicit Non-Goals

- No Adaptive Engine.
- No question selection changes.
- No global ranking.
- No confidence or trend calculation.
- No misconception inference.
- No causal reasoning evaluation.
- No Tutor, Retrieval, Self-Eval, Golden, Dashboard, or frontend changes.
- No publication or deployment.

## Verification

Coverage is in `tests/test_learner_state_foundation.py` and includes legacy
schema compatibility, constructor contracts, serialization, deserialization,
LES persistence, question exposure persistence, Tutor-context isolation, and
governance enforcement.

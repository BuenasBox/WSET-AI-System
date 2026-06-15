# Phase 4A.3.9.2 - Adaptive Loop Finalization

> **STATUS: CANONICAL**
>
> **LAST RECONCILED: 2026-06-06**

## Status

Implemented as deterministic private learning infrastructure.

## Objective

Close the formative loop:

```text
Formative Event
  -> Next Session Signals
  -> Adaptive Composer
  -> New Session
  -> New Formative Event
```

## Implementation

`tools/question_generation/full_master_bank_session_composer.py` now provides
`compose_adaptive_master_bank_session()`.

It consumes:

- recommended next mode;
- RA reinforcement priority;
- weak-topic priority;
- strong-topic progression candidates;
- misconception repair candidates;
- causal-chain reinforcement candidates;
- exposure avoidance.

The existing `compose_master_bank_session()` remains the base implementation.
Without `next_session_signals`, its response shape and selection behavior remain
unchanged.

`tools/learner_model/adaptive_loop.py` provides:

- `run_adaptive_learning_loop()`;
- `persist_learning_state_atomically()`.

The coordinator processes one attempt, persists cognitive memory and LES as a
rollback-safe pair, and composes the next session from the resulting signals.

## Persistence Contract

Both JSON payloads are normalized and written to temporary files first.
Existing destinations are moved to rollback files, then both new files are
installed. If either installation fails, both original files are restored.

This is coordinated filesystem atomicity with deterministic rollback. It does
not claim multi-process database transaction semantics.

## Preserved Boundaries

- Existing modes remain `EXPRESS_10`, `QUICK_25`, `STANDARD_50`,
  `FULL_DIAGNOSTIC`, and `RA_FOCUS`.
- Master Bank eligibility and suitability classification are unchanged.
- Open Response Evaluator is unchanged.
- Open Response activation remains off.
- Tutor, Retrieval, Self-Eval, golden fixtures, snapshots, dashboard assets,
  and frontend assets are unchanged.
- Adaptive signals may reorder eligible candidates but cannot add an ineligible
  item to a session.
- Unsafe governance flags fail closed.

## Learning Links

The current Master Bank has no `learning_links` records. Topic, RA, difficulty,
and exposure signals are therefore the active adaptive inputs today.

Misconception and causal-chain ranking support is implemented and remains inert
until reviewed links are added under
`docs/LEARNING_LINKS_CONTRACT.md`.

## Tests

`tests/test_adaptive_loop_finalization.py` covers:

- unchanged base-composer behavior;
- mode and RA signal consumption;
- weak-topic prioritization;
- exposure avoidance;
- linked misconception targeting;
- unsafe-governance rejection;
- successful coordinated persistence;
- rollback after second-file installation failure;
- end-to-end event-to-next-session behavior.

Verification result:

```text
Full suite: 1643 tests, 9 skipped, 0 failures
SBA export dry-run: 36 eligible, 0 validation errors
Slow Golden: 7/7 OK
```

## Deferred

- Population and human review of real Master Bank `learning_links`.
- Connection of the private coordinator to a learner-facing session surface.
- `SYSTEM_CAPABILITIES_MATRIX.md`, after remaining runtime reconciliation.

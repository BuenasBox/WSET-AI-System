# Phase 4A.3.9.0 - Cognitive Map Learning Event Runtime

## Status

Implemented as deterministic, private learning infrastructure.

The runtime converts each SBA interaction into a traceable formative event,
updates the existing cognitive map and LES, and produces signals for a future
adaptive composer. It does not create a mark, percentage, pass/fail result,
exam-readiness claim, or examiner authority.

## Existing Components Reused

- `pedagogical_memory_v1` and `knowledge_tracing.py` remain the cognitive map.
- `minimal_brain_v2` remains the LES schema.
- `diagnostic_outcome_v1` remains the diagnostic outcome contract.
- `record_session_observations()` remains the exposure/topic/RA adapter.
- `misconception_runtime.py` remains the misconception consumer.
- `causal_runtime.py` remains the causal-chain consumer.
- Master Bank curriculum and optional `learning_links` supply item metadata.
- Session modes remain `EXPRESS_10`, `QUICK_25`, `STANDARD_50`,
  `FULL_DIAGNOSTIC`, and `RA_FOCUS`.

No second cognitive map or replacement LES was created.

## New Runtime

`tools/learner_model/learning_event_runtime.py` implements:

1. `create_question_attempt()`
2. `build_diagnostic_outcome()`
3. `build_formative_event()`
4. `update_cognitive_map()`
5. `update_les_from_learning_event()`
6. `build_next_session_signals()`
7. `process_question_attempt()`
8. `reverse_cognitive_map_update()` and `reverse_les_update()`

All functions are deterministic when given the same explicit timestamp and
inputs. They return new dictionaries and do not mutate their inputs.

## Attempt Flow

```text
Question Attempt
  -> diagnostic_outcome_v1
  -> formative_learning_event_v1
  -> pedagogical_memory_v1 update
  -> minimal_brain_v2 LES update
  -> next_session_learning_signals_v1
```

The attempt records session/question identity, selected option, correctness,
optional confidence, answer change, response-time band, mode, and timestamp.
It contains no assessment result beyond the observed correctness boolean.

## Diagnostic Outcome

The runtime preserves the existing schema instead of extending it
incompatibly. It maps:

- RA, topic and subtopic into `source_trace`;
- selected distractor role, misconception and causal-chain IDs when supplied;
- confidence alignment into `diagnostic_classification`;
- reinforcement/progression direction into the existing remediation and
  learner-state placeholder fields.

Difficulty and explicit learning deltas belong to the separate formative
event, because `diagnostic_outcome_v1` rejects unknown properties.

## Cognitive Map Update

The existing topic skill record receives additive runtime metadata:

- `exposure_count`
- `gap_count`
- `reinforcement_priority`
- `learning_stage`
- `progression_candidate`

Stages are evidence descriptions only:

- `emerging`
- `developing`
- `stabilizing`
- `ready_for_greater_challenge`

Incorrect observations increase reinforcement priority and gap evidence.
Repeated strong observations can make a topic a progression candidate for
causality, comparison, or integration. Existing mastery probability behavior
is reused from `update_mastery()`.

The cognitive map also receives a bounded append-only `learning_events` log.
Each update returns a `cognitive_map_change_set_v1` containing the prior and
new topic skill records. `reverse_cognitive_map_update()` applies that record
to restore the prior topic state and event log.

## LES Adapter

LES remains `minimal_brain_v2`. The adapter reuses:

- question exposure log and aggregate exposure signals;
- topic observations;
- RA observations;
- misconception detection/session persistence;
- causal-chain exposure/demonstration state.

A bounded `learning_event_log` is added as a forward-compatible top-level
extension. Existing LES normalization preserves unknown top-level fields, and
Tutor context continues to exclude all new learning-event fields.

`les_learning_event_change_set_v1` captures the prior and resulting values of
the LES containers touched by an event. `reverse_les_update()` restores those
containers exactly.

`misconception_runtime.process_sba_outcome()` now accepts an optional
`reference_date`; existing callers remain compatible, while tests and batch
runtimes can be reproducible.

## Next Session Signals

The runtime emits, but does not consume:

- `weak_topic_priority`
- `strong_topic_progression_candidate`
- `RA_reinforcement_priority`
- `misconception_repair_candidate`
- `causal_chain_reinforcement_candidate`
- `exposure_avoidance`
- `recommended_next_mode`

This is a projection for a later adaptive composer. It does not alter the
current Session Composer.

## Boundaries

This phase does not modify Tutor, Retrieval, Self-Eval, golden fixtures,
snapshots, dashboard frontend, SBA frontend, Open Response frontend, or the
Open Response evaluator. It does not deploy or activate Open Response.

The Master Bank currently lacks complete distractor-to-misconception and
item-to-causal-chain links. The runtime consumes optional `learning_links`
when present and otherwise records topic/RA evidence without inventing IDs.

## Tests

`tests/test_learning_event_runtime.py` covers:

- attempt to outcome;
- outcome to formative event;
- cognitive-map and LES updates;
- weak-topic reinforcement;
- strong-topic progression;
- schema compatibility;
- append-only trace logs;
- deterministic reproduction;
- governance and prohibited-field absence;
- unchanged public lab and Open Response evaluator files.

## Pending Work

- Populate governed Master Bank `learning_links` for real SBA distractors.
- Let the Session Composer consume next-session signals in a separate phase.
- Add future Open Response attempts through the same formative event contract
  without activating the current Open Response surface.
- Define a persistence coordinator for atomic memory/LES writes.

## Verification

Executed:

```powershell
python -m unittest discover -s tests -v
python -m tools.question_generation.export_static_demo_questions --dry-run
$env:RUN_SLOW_TESTS='1'; python -m unittest tests.test_golden_self_eval -v
```

Results:

- full suite: 1627 tests, 9 skipped, 0 failures;
- focused learning-event runtime: 25/25;
- SBA export: 36 eligible items, 0 validation errors;
- Slow Golden: 7/7;
- snapshots: unchanged;
- public and Open Response frontend files: unchanged.

The integrated branch used for this phase classifies 506 records in the SBA
operational pool and 21 in the Open Response candidate pool. Those executable
counts differ from the 589/27 planning context supplied for the phase. The
runtime does not encode either count and remains compatible with later
eligibility-data reconciliation.

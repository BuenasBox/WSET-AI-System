# Phase 4A.3.5 - Diagnostic Outcome Model

Date: 2026-05-31

Status: Authoritative diagnostic outcome model for future diagnostic
single-best-answer attempts. This phase defines model and schema only. It does
not authorize question generation, generated banks, attempt persistence,
learner-state writes, session-ledger writes, PSL changes, retrieval changes,
frontend changes, snapshots, or scoring authority.

References:

- `docs/DIAGNOSTIC_SBA_GOVERNANCE_CONTRACT.md`
- `docs/DIAGNOSTIC_SBA_ITEM_SCHEMA.md`
- `knowledge/enrichment/diagnostic_outcome.schema.json`

## 1. Purpose

The Diagnostic Outcome Model defines what the system may learn from a learner's
future attempt on a diagnostic single-best-answer item.

It answers:

- What did the learner select?
- Was the selected option correct?
- What diagnostic role did that option carry?
- Was the response fast, slow, hesitant, or changed?
- Was confidence aligned or misaligned?
- What misconception, causal chain, SAT skill, topic, or subtopic should be
  remediated?
- What learner-state update should be suggested later?

This model is the bridge between:

```text
SBA Item
  -> Attempt
  -> Diagnostic Outcome
  -> Future Learner Model
  -> Remediation
  -> Tutor Persona Engine
```

The model is diagnostic, not official. It may support training feedback and
future learner-state suggestions, but it must never produce official marks,
examiner judgments, grade predictions, or certification claims.

## 2. Non-Goals

This phase must not:

- Generate questions.
- Create a question bank.
- Generate distractors.
- Persist attempts.
- Modify learner state.
- Modify session ledger.
- Modify PSL or Tutor Persona files.
- Modify retrieval.
- Modify frontend.
- Modify snapshots.
- Activate official scoring authority.

## 3. Canonical Outcome Structure

Every diagnostic outcome must contain:

- `schema_version`
- `identity`
- `attempt_observation`
- `diagnostic_classification`
- `source_trace`
- `timing_interpretation`
- `remediation_routing`
- `learner_state_effect_placeholders`
- `governance`

Unknown fields are rejected by the schema. Future evolution should use
`outcome_version` and `schema_version`.

## 4. Identity

Required fields:

- `outcome_id`
- `item_id`
- `attempt_id`
- `outcome_version`
- `generated_by`
- `training_diagnostic_only`

`training_diagnostic_only` must be `true`.

## 5. Attempt Observation

Required fields:

- `selected_option_id`
- `is_correct`
- `response_time_ms`
- `answer_changed`
- `confidence_self_report`
- `hesitation_flag`

`selected_option_id` must be one of `A`, `B`, `C`, or `D`.

`confidence_self_report` may be `low`, `medium`, `high`, or `not_reported`.
Response time may be `null` when not measured.

## 6. Diagnostic Classification

Required fields:

- `diagnosed_error_type`
- `confidence_alignment`

Allowed `diagnosed_error_type` values:

- `none`
- `knowledge_gap`
- `causal_confusion`
- `sat_confusion`
- `terminology_confusion`
- `process_confusion`
- `regional_confusion`
- `misconception_reinforced`
- `partial_reasoning`
- `keyword_trap`
- `guessing_behavior`
- `confidence_mismatch`

Allowed `confidence_alignment` values:

- `aligned`
- `overconfident_wrong`
- `underconfident_correct`
- `uncertain_correct`
- `uncertain_wrong`
- `not_reported`

These classifications are diagnostic signals. They are not official scoring,
official marking, pass/fail judgments, or certification evidence.

## 7. Source Trace

Required fields:

- `item_source_ids`
- `selected_option_diagnostic_role`
- `misconception_id`
- `causal_chain_id`
- `sat_relevance`
- `topic`
- `subtopic`
- `ra_id`

`item_source_ids` must be a non-empty list. Optional trace IDs may be `null`
when not applicable. `sat_relevance` is a list and may be empty.

The selected option diagnostic role must describe why that option matters
diagnostically, such as `correct`, `misconception`, `partial_reasoning`,
`keyword_trap`, `causal_confusion`, or `sat_confusion`.

## 8. Timing Interpretation

Required fields:

- `timing_band`
- `timing_interpretation`

Allowed `timing_band` values:

- `fast`
- `expected`
- `slow`
- `very_slow`
- `not_measured`

Allowed `timing_interpretation` values:

- `fluent_recall`
- `deliberate_reasoning`
- `hesitation`
- `likely_guess`
- `uncertainty_signal`
- `not_measured`

Timing is a training diagnostic. It must not be interpreted as an official
performance mark.

## 9. Remediation Routing

Required fields:

- `recommended_next_action`
- `remediation_target_type`
- `remediation_target_id`
- `feedback_priority`

Allowed `recommended_next_action` values:

- `continue`
- `review_topic`
- `review_causal_chain`
- `review_misconception`
- `review_sat_skill`
- `repeat_similar_item`
- `reduce_difficulty`
- `increase_difficulty`
- `switch_to_explanation`
- `schedule_review`

Allowed `remediation_target_type` values:

- `topic`
- `subtopic`
- `causal_chain`
- `misconception`
- `sat_skill`
- `source_chunk`
- `none`

Allowed `feedback_priority` values:

- `low`
- `medium`
- `high`
- `urgent`

`remediation_target_id` may be `null` when the target type is `none`.

## 10. Learner-State Effect Placeholders

This model does not update learner state.

It reserves descriptive fields only:

- `mastery_signal`
- `confidence_signal`
- `retention_signal`
- `misconception_signal`
- `recommended_ledger_event`

These fields may describe a later suggested update, but they must not contain
authoritative scores, official marks, pass/fail claims, or direct write
instructions. Future learner-state updates require a separate phase.

## 11. Governance

Every outcome must include:

```json
{
  "safe_for_examiner": false,
  "examiner_scoring_allowed": false,
  "official_wset_score": false,
  "training_diagnostic_only": true,
  "uses_llm": false,
  "uses_api": false,
  "uses_embeddings": false,
  "uses_vector_db": false,
  "cloud_services_active": false
}
```

No future diagnostic outcome may override these values.

## 12. Forbidden Outputs

The Diagnostic Outcome Model explicitly forbids:

- Official marks.
- Official score.
- Pass/fail certification.
- Examiner judgment.
- Grade prediction.
- Official WSET result.
- Certification readiness claim.

Allowed outputs:

- Diagnostic signal.
- Training feedback.
- Remediation route.
- Learner-state suggestion.
- Readiness-supporting evidence, but not official readiness certification.

## 13. Text Safety

The schema rejects obvious official-authority wording in descriptive fields,
including:

- `official mark`
- `official score`
- `examiner judgment`
- `grade prediction`
- `official WSET result`
- `certified pass`
- `certification readiness`
- `guaranteed pass`

This is a conservative schema-level guard. Phase 4A.4+ validators may add
deeper text scanning if diagnostic outcome text expands.

## 14. Validation Covered In Phase 4A.3.5

The schema and focused tests cover:

- Required identity.
- Required attempt observation.
- Valid selected option IDs.
- Valid diagnostic classification values.
- Valid confidence alignment.
- Valid timing band.
- Valid remediation action and target type.
- Safe governance constants.
- Rejection of extra official scoring/pass-fail fields.
- Rejection of obvious certification/official-scoring wording.
- Learner-state effect fields as placeholders only.

## 15. Next Phase

The next recommended phase is Phase 4A.4: Deterministic SBA Template
Generator, only after the diagnostic outcome model remains stable.

The generator must emit items that pass Phase 4A.2 schema checks and Phase
4A.3 validation, and future attempt handling must emit outcomes compatible
with this model.

# Phase 4A.2 - Diagnostic SBA Item Schema

Date: 2026-05-31

Status: Authoritative schema contract for future diagnostic
single-best-answer items. This document defines structure only. It does not
authorize question generation, generated banks, retrieval changes, planner
changes, PSL changes, frontend changes, or knowledge-corpus edits.

References:

- `docs/DIAGNOSTIC_SBA_GOVERNANCE_CONTRACT.md`
- `knowledge/enrichment/diagnostic_sba_item.schema.json`

## 1. Purpose

The Diagnostic SBA item schema defines the canonical structure that every
future training-only diagnostic single-best-answer item must satisfy before it
can enter a generated bank.

The schema supports:

- Deterministic generation.
- Source grounding.
- RA, topic, and subtopic segmentation.
- Misconception diagnosis.
- Distractor analysis.
- Remediation routing.
- Future learner analytics.

This is not a quiz-bank schema for generic multiple choice. It is a diagnostic
training schema. Every option must carry diagnostic metadata so that a selected
wrong answer can tell the system something useful about the learner's likely
gap.

## 2. Canonical File

The machine-readable JSON Schema lives at:

```text
knowledge/enrichment/diagnostic_sba_item.schema.json
```

The schema uses JSON Schema Draft 2020-12.

## 3. Top-Level Structure

Every item must contain these top-level sections:

- `schema_version`
- `identity`
- `curriculum`
- `question`
- `options`
- `source_support`
- `feedback`
- `governance`
- `attempt_analytics_placeholders`

The schema is closed at the top level: unknown top-level fields are rejected.
Future schema evolution should use `item_version` and `schema_version`, not
ad hoc fields.

## 4. Identity

Required fields:

- `item_id`: Stable deterministic identifier for the item.
- `item_version`: Version string for item revisions.
- `created_by`: Component or phase that created the item.
- `generation_method`: Must identify a non-LLM method such as
  `manual_schema_fixture` or `deterministic_template`.
- `training_item_only`: Must be `true`.

Identity fields must never imply official WSET authorship or examiner status.

## 5. Curriculum

Required fields:

- `ra_id`: WSET result area or assessment-objective grouping.
- `topic`: Main topic.
- `subtopic`: More precise topic segment.
- `difficulty`: Controlled difficulty label.
- `learning_objective`: Human-readable learning objective.

Allowed difficulty labels:

- `foundational`
- `intermediate`
- `advanced`
- `distinction`

The item must be source-grounded at this curriculum level. Broad RA presence is
not enough; `topic` and `subtopic` must be present.

## 6. Question

Required fields:

- `stem`: The question stem.
- `question_type`: Must be `single_best_answer`.
- `expected_reasoning_type`: Controlled reasoning label.

Allowed reasoning labels:

- `definition`
- `cause_effect`
- `process`
- `sat_reasoning`
- `misconception_correction`
- `regional_comparison`
- `vocabulary`
- `diagnostic_review`

The stem must be training-only, paraphrased, and supported by source material.
It must not imitate official WSET wording.

## 7. Options

The item must contain exactly four options:

- `A`
- `B`
- `C`
- `D`

Each option must include:

- `option_id`
- `option_text`
- `is_correct`
- `diagnostic_role`

Exactly one option must have `is_correct = true`.

Allowed diagnostic roles:

- `correct`
- `misconception`
- `partial_reasoning`
- `keyword_trap`
- `causal_confusion`
- `sat_confusion`
- `near_neighbor_confusion`
- `scope_error`
- `regional_confusion`
- `term_confusion`
- `unsupported_inference`

The correct option must use `diagnostic_role = "correct"`. Distractors must
use a non-`correct` role. Phase 4A.2 records this as a schema convention; Phase
4A.3 should enforce cross-field semantic validation in code.

## 8. Misconception Support

Every option may include:

- `misconception_id`
- `misconception_description`

These fields are optional because not every diagnostic distractor corresponds
to a known misconception node. When a misconception node exists, the distractor
should link to it.

If `diagnostic_role = "misconception"`, Phase 4A.3 should require a
`misconception_id` unless an explicit exception is documented.

## 9. Source Support

Source support is mandatory.

Required fields:

- `source_ids`
- `source_chunks`
- `support_rationale`

`source_ids` and `source_chunks` must both be non-empty arrays. The support
rationale must explain why the cited sources support the item, the correct
answer, and the diagnostic contrast.

Allowed source types for future support records remain limited to lightweight
repo-local artifacts:

- JSON
- JSONL
- Markdown
- Python configs/tests/snapshots
- Already extracted chunks

The schema intentionally does not allow an item with empty source support.
Unsupported items must fail validation.

## 10. Feedback Support

Required fields:

- `correct_rationale`
- `why_other_options_are_wrong`
- `remediation_recommendation`

`why_other_options_are_wrong` must contain entries for all four options. The
correct option entry may briefly state that it is correct and point to the
correct rationale; the three distractor entries must explain the diagnostic
error.

`remediation_recommendation` must be training-only and must not claim official
examiner authority.

## 11. Governance

Every item must include governance metadata:

```json
{
  "safe_for_examiner": false,
  "examiner_scoring_allowed": false,
  "official_wset_question": false,
  "training_item_only": true
}
```

The machine schema also reserves these governance fields:

- `uses_llm = false`
- `uses_api = false`
- `uses_embeddings = false`
- `uses_vector_db = false`
- `cloud_services_active = false`

These additional fields are required by the JSON Schema to keep Phase 4A.2
aligned with the Phase 4A.1 governance contract.

## 12. Attempt Analytics Placeholders

The item reserves future attempt analytics fields but does not implement
analytics.

Reserved fields:

- `response_time`
- `confidence`
- `answer_changed`
- `diagnosed_error_type`
- `hesitation`
- `recommended_next_action`

These fields must be present as nullable placeholders. Future attempt records
may populate them, but the item schema itself does not analyze learner
behavior.

Attempt analytics must never create official scoring authority.

## 13. Tiny Illustrative Example

This example is structural only. It is not a generated bank item and should not
be treated as production content.

```json
{
  "schema_version": "diagnostic_sba_item_v1",
  "identity": {
    "item_id": "diag_sba_example_001",
    "item_version": "1.0.0",
    "created_by": "phase_4a2_schema_doc",
    "generation_method": "manual_schema_fixture",
    "training_item_only": true
  },
  "curriculum": {
    "ra_id": "RA1",
    "topic": "viticulture",
    "subtopic": "climate_and_acidity",
    "difficulty": "foundational",
    "learning_objective": "Identify a source-grounded cause-effect relationship."
  },
  "question": {
    "stem": "Which option best describes the relationship being tested?",
    "question_type": "single_best_answer",
    "expected_reasoning_type": "cause_effect"
  },
  "options": {
    "A": {
      "option_id": "A",
      "option_text": "Correct source-grounded relationship.",
      "is_correct": true,
      "diagnostic_role": "correct"
    },
    "B": {
      "option_id": "B",
      "option_text": "Plausible misconception.",
      "is_correct": false,
      "diagnostic_role": "misconception",
      "misconception_id": "MC_EXAMPLE",
      "misconception_description": "Example misconception placeholder."
    },
    "C": {
      "option_id": "C",
      "option_text": "Partial reasoning.",
      "is_correct": false,
      "diagnostic_role": "partial_reasoning"
    },
    "D": {
      "option_id": "D",
      "option_text": "Keyword trap.",
      "is_correct": false,
      "diagnostic_role": "keyword_trap"
    }
  },
  "source_support": {
    "source_ids": ["CC_EXAMPLE"],
    "source_chunks": ["chunk_example_001"],
    "support_rationale": "The cited source supports the correct relationship and diagnostic contrast."
  },
  "feedback": {
    "correct_rationale": "The correct option follows the cited source support.",
    "why_other_options_are_wrong": {
      "A": "This is the correct answer.",
      "B": "This reflects the linked misconception.",
      "C": "This is incomplete reasoning.",
      "D": "This matches words but not the relationship."
    },
    "remediation_recommendation": "Review the linked source and retry a related training item."
  },
  "governance": {
    "safe_for_examiner": false,
    "examiner_scoring_allowed": false,
    "official_wset_question": false,
    "training_item_only": true,
    "uses_llm": false,
    "uses_api": false,
    "uses_embeddings": false,
    "uses_vector_db": false,
    "cloud_services_active": false
  },
  "attempt_analytics_placeholders": {
    "response_time": null,
    "confidence": null,
    "answer_changed": null,
    "diagnosed_error_type": null,
    "hesitation": null,
    "recommended_next_action": null
  }
}
```

## 14. Validation Covered In Phase 4A.2

The schema and focused tests cover:

- Required top-level sections.
- Required nested fields.
- Exactly four options.
- Exactly one correct option.
- Missing source support rejection.
- Unsafe governance flag rejection.
- Basic enum constraints.
- Non-empty strings and non-empty source arrays.

## 15. Deferred To Phase 4A.3

Phase 4A.3 should implement a dedicated Diagnostic SBA Validator that performs
semantic checks beyond JSON Schema, including:

- Correct option must use `diagnostic_role = "correct"`.
- Distractors must not use `diagnostic_role = "correct"`.
- Duplicate option text detection after normalization.
- Near-duplicate option detection after canonical-term and alias normalization.
- Official wording leakage detection.
- Examiner-authority phrase detection.
- Unsupported rationale detection.
- `misconception` role requires `misconception_id` unless explicitly waived.
- Every cited source ID exists in allowed repo-local source material.
- Remediation recommendation maps to a valid tutor-side action.

## 16. Next Phase

The next recommended phase is Phase 4A.3: Diagnostic SBA Validator.

The validator must exist before any generator or generated bank exists.

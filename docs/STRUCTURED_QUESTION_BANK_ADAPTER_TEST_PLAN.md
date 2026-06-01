# Structured Question Bank Adapter Test Plan

Phase: 4A.3.7.2

Status: test-plan and contract-test phase only. This document does not
implement adapter code, migrate questions, generate questions, modify the
structured question bank, or create a converted bank.

Source bank:

- `knowledge/question-bank/structured/wset3_questions.json`

Target future output:

- `diagnostic_sba_item_v1`

Related documents:

- `docs/STRUCTURED_QUESTION_BANK_COMPATIBILITY_AUDIT.md`
- `docs/STRUCTURED_QUESTION_BANK_ADAPTER_CONTRACT.md`
- `docs/DIAGNOSTIC_SBA_ITEM_SCHEMA.md`
- `knowledge/enrichment/diagnostic_sba_item.schema.json`
- `tools/question_generation/diagnostic_sba_validator.py`

## 1. Purpose

The adapter test plan defines what must be true before any structured question
bank adapter can be implemented.

The future adapter must prove that it can classify, map, enrich, and validate
existing structured questions without:

- mutating the source bank;
- bulk-converting unsafe records;
- forcing open-response prompts into SBA;
- inventing source support;
- inventing diagnostic roles;
- upgrading governance safety;
- creating official scoring authority.

The tests in this phase are contract-style and use small in-memory fixtures
only. They intentionally do not import or create production adapter code.

## 2. Test Scope

The future adapter test suite should cover:

- clean SBA candidate classification;
- missing options;
- empty options;
- duplicate option text;
- invalid correct answer letter;
- `short_answer` preservation;
- unsafe governance;
- direct field mapping expectations;
- lineage preservation;
- required enrichment fields;
- no mutation;
- no bulk conversion;
- compatibility with the diagnostic SBA validator after enrichment.

## 3. Out Of Scope

This phase must not test:

- generated question quality;
- real question-bank migration;
- bulk conversion;
- parser behavior;
- retrieval behavior;
- knowledge-map matching;
- official Markdown parsing;
- Wine With Jimmy chunk mapping;
- frontend behavior;
- PSL behavior.

## 4. Fixture Strategy

Contract tests should use tiny in-memory dictionaries that mimic the current
structured bank shape:

- `question_id`
- `question_text`
- `question_type`
- `expected_topics`
- `expected_causal_links`
- `expected_keywords`
- `expected_reasoning_type`
- `difficulty`
- `source_type`
- `safe_for_examiner`
- `options`
- `correct_answer_letter`
- `correct_answer_text`

The tests should not read `knowledge/question-bank/structured/wset3_questions.json`.
The production bank was already audited in Phase 4A.3.7; this phase locks the
adapter contract, not the live bank metrics.

## 5. Classification Expectations

Future adapter classification must be deterministic.

Required categories:

- `adapter_ready_clean_pilot`
- `requires_source_grounding`
- `requires_option_diagnostics`
- `preserve_for_open_response`
- `reject_or_defer`

Classification must fail closed. A record with invalid structure or unsafe
governance must not be silently mapped into a candidate item.

## 6. Clean SBA Candidate Test

A clean candidate must have:

- `question_type == "theory"`;
- exact A-D options;
- all option texts non-empty;
- no duplicate option text after normalization;
- valid A-D `correct_answer_letter`;
- non-empty `correct_answer_text`;
- correct answer text matching the selected option;
- `expected_topics` present;
- `expected_reasoning_type` present;
- `safe_for_examiner = false`.

Expected classification:

- `adapter_ready_clean_pilot`

The test must also verify that the item still requires enrichment before it can
be a valid diagnostic SBA item.

## 7. Rejection And Deferral Tests

The following records must classify as `reject_or_defer`:

- missing `options`;
- missing A-D keys;
- empty option text;
- duplicate option text after normalization;
- invalid `correct_answer_letter`;
- missing `correct_answer_text`;
- mismatched `correct_answer_text`;
- `safe_for_examiner = true`.

Rejected or deferred records must retain deterministic reasons.

## 8. Open-Response Preservation Test

Records with `question_type == "short_answer"` must classify as:

- `preserve_for_open_response`

They must not be converted into A-D SBA form. Their expected topics,
keywords, causal links, and difficulty should be preserved as future
open-response rubric hints only.

## 9. Field Mapping Expectations

The future adapter must map direct fields as follows:

| Source field | Target expectation |
| --- | --- |
| `question_id` | preserved as `source_question_id` lineage and deterministic item ID seed |
| `question_text` | `question.stem` |
| `question_type` | candidate eligibility only; output question type must be diagnostic SBA compatible |
| `difficulty` | `curriculum.difficulty` |
| `expected_topics` | candidate curriculum hints |
| `expected_causal_links` | candidate causal-chain hints |
| `expected_keywords` | candidate matching and diagnostic hints |
| `source_type` | lineage/provenance, not sufficient source support |
| `safe_for_examiner` | `governance.safe_for_examiner = false` |
| `options.A-D` | `options.A-D.option_text` |
| `correct_answer_letter` | exactly one `is_correct = true` |
| `correct_answer_text` | answer verification and feedback hint only |

Mapping tests must confirm that direct mapping alone creates a draft, not a
validated item.

## 10. Lineage Tests

Every adapted draft or candidate must preserve:

- `source_bank_path`;
- `source_question_id`;
- `source_question_type`;
- `source_source_type`;
- `adapter_version`;
- `adapted_at`;
- `transformation_notes`.

Lineage should also carry classification and deferral reasons when applicable.

## 11. Required Enrichment Tests

Tests must assert that direct mapping leaves these required enrichment gaps:

- `source_support`;
- `support_rationale`;
- per-option `diagnostic_role`;
- `misconception_id` when applicable;
- `causal_chain_id` when applicable;
- SAT relevance when applicable;
- `correct_rationale`;
- `why_other_options_are_wrong`;
- `remediation_recommendation`;
- `attempt_analytics_placeholders`;
- full governance constants.

No adapter output may be treated as valid until these fields are present and
validated.

## 12. No Mutation And No Bulk Conversion

The future adapter must:

- avoid mutating input dictionaries;
- avoid mutating nested `options`;
- return deterministic errors;
- process one record at a time by default;
- require explicit approval for any future batch output;
- never overwrite the source bank.

Contract tests should deep-copy input fixtures before classification or mapping
and assert equality after the operation.

## 13. Future Validator Compatibility

After enrichment, a candidate must pass:

- the diagnostic SBA JSON Schema;
- `validate_diagnostic_sba_item(item)`;
- governance validation;
- source support validation;
- option diagnostics validation.

Current implementation note:

- `knowledge/enrichment/diagnostic_sba_item.schema.json` requires
  `question.question_type = "diagnostic_single_best_answer"`.
- `tools/question_generation/diagnostic_sba_validator.py` currently requires
  `question.question_type = "single_best_answer"`.

This mismatch must be resolved before adapter implementation can claim full
schema-plus-validator compatibility. Phase 4A.3.7.2 does not change either
file.

## 14. Contract Test File

This phase adds:

- `tests/test_structured_question_bank_adapter_contract.py`

The tests are intentionally in-memory and adapter-free. They define expected
contract behavior so a future production adapter can be implemented against the
same cases.

## 15. Recommended Next Phase

Phase 4A.3.7.3 - Adapter Skeleton.

The next phase should create a minimal production module with no migration and
no file writes. It should satisfy the contract tests before adding any real
question-bank reads.

# Structured Question Bank Adapter Contract

Phase: 4A.3.7.1

Status: contract-only. This document does not implement an adapter, migrate
questions, generate diagnostic items, modify the structured question bank, or
authorize runtime use.

Primary source bank:

- `knowledge/question-bank/structured/wset3_questions.json`

Target diagnostic schema:

- `docs/DIAGNOSTIC_SBA_ITEM_SCHEMA.md`
- `knowledge/enrichment/diagnostic_sba_item.schema.json`

Related governance contract:

- `docs/DIAGNOSTIC_SBA_GOVERNANCE_CONTRACT.md`

## 1. Purpose

The Structured Question Bank Adapter is not a generator.

Its future role is to transform or enrich existing structured question-bank
records into `diagnostic_sba_item_v1` candidates while preserving original
lineage, source provenance, governance restrictions, and diagnostic intent.

The adapter must not invent new question content. It may only map existing
fields, attach validated repo-local enrichment, and produce adapter outputs
that still have to pass schema and validator checks before any runtime or bank
use.

The adapter exists because the current structured question bank is strategically
valuable but not directly compatible with the diagnostic SBA architecture:

- 616 total structured records.
- 595 `theory` records.
- 21 `short_answer` / open-response records.
- 591 basic SBA-compatible records.
- 525 strict records with non-empty A-D options and one valid answer.
- 520 clean pilot candidates after excluding duplicate option text.
- 0 records directly compatible with `diagnostic_sba_item_v1`.

## 2. Non-Goals

This contract does not authorize:

- Adapter implementation.
- Converted item creation.
- Generated question creation.
- Question-bank mutation.
- Bulk migration.
- Retrieval changes.
- Knowledge-map changes.
- PSL changes.
- Frontend changes.
- Runtime practice-session changes.

Future implementation must be approved in a separate phase.

## 3. Input Format

The current structured bank records use these fields:

| Field | Current meaning |
| --- | --- |
| `question_id` | Existing stable identifier in the structured bank. |
| `question_text` | Question stem or prompt text. |
| `question_type` | Existing item type, currently mainly `theory` with some `short_answer`. |
| `expected_topics` | Topic hints or expected knowledge areas. |
| `expected_causal_links` | Causal-chain hints or expected causal relations. |
| `expected_keywords` | Keyword hints for expected answer coverage or matching. |
| `expected_reasoning_type` | Current reasoning label, such as `theory_foundation` or `cause_effect`. |
| `difficulty` | Current difficulty label. |
| `source_type` | Existing source/provenance label, often workbook or structured-bank provenance. |
| `safe_for_examiner` | Existing governance flag; all audited records are `false`. |
| `options` | A-D option object when present. |
| `correct_answer_letter` | Existing answer key. Valid SBA values are A, B, C, or D. |
| `correct_answer_text` | Existing correct answer text. |

Input records must be treated as immutable. The adapter must read them as
source records and produce separate adapted candidates.

## 4. Output Format

The adapter target is `diagnostic_sba_item_v1`.

Every adapted candidate must use the canonical top-level structure:

- `schema_version`
- `identity`
- `curriculum`
- `question`
- `options`
- `source_support`
- `feedback`
- `governance`
- `attempt_analytics_placeholders`

An adapted candidate is not valid merely because it has this shape. It must
also pass the diagnostic SBA schema, deterministic validator, governance checks,
source-support checks, and option-diagnostics checks.

## 5. Field Mapping Rules

The future adapter must use deterministic field mapping.

| Source field | Target field | Policy |
| --- | --- | --- |
| `question_id` | `identity.source_question_id` and item ID seed | Preserve exactly as lineage. Generate adapter item IDs deterministically with a prefix, not by overwriting the original ID. |
| `question_text` | `question.stem` | Preserve as candidate stem unless a later approved enrichment phase records an explicit paraphrase. Never silently rewrite. |
| `question_type` | `question.question_type` | Existing `theory` can map only to `diagnostic_single_best_answer` after SBA eligibility checks. Existing `short_answer` must be preserved for open-response, not forced into SBA. |
| `expected_reasoning_type` | `question.expected_reasoning_type` | Map directly only when compatible with the schema enum. Otherwise map through an approved deterministic table and record the mapping note. |
| `difficulty` | `curriculum.difficulty` | Map if it is one of the allowed diagnostic labels. Unknown values must fail or require enrichment. |
| `expected_topics` | `curriculum.ra_id`, `curriculum.topic`, `curriculum.subtopic`, `curriculum.learning_objective` candidates | Use only as hints. Must be resolved into explicit curriculum fields before validation. |
| `expected_causal_links` | candidate `causal_chain_id` / diagnostic enrichment metadata | Use as hints for knowledge-map matching. Do not invent causal-chain IDs. |
| `expected_keywords` | source matching hints, diagnostic hints, remediation hints | Use as hints only. Keywords are not source support by themselves. |
| `source_type` | lineage metadata and candidate `source_support.source_ids` hint | Preserve as provenance. It does not satisfy mandatory source support alone. |
| `safe_for_examiner` | `governance.safe_for_examiner` | Preserve false. If true ever appears, fail closed unless a future governance contract explicitly handles it. |
| `options.A-D` | `options.A-D.option_text` | Map only when A-D keys exist and option text is non-empty. Add `option_id`, `is_correct`, and `diagnostic_role` through deterministic enrichment. |
| `correct_answer_letter` | `options.<letter>.is_correct` | Exactly one A-D option must become true. Invalid answer letters reject or defer the item. |
| `correct_answer_text` | answer verification and feedback hint | Must match the selected option or be resolved before adaptation. It is not a rationale. |

## 6. Required Enrichment

The following fields cannot be mapped directly from the current structured
bank and must be enriched before a candidate can become valid:

- `source_support.source_ids`
- `source_support.source_chunks`
- `source_support.support_rationale`
- per-option `diagnostic_role`
- optional but preferred per-option `misconception_id`
- optional but preferred per-option `misconception_description`
- candidate `causal_chain_id` where supported by a known node
- SAT relevance where deterministically supported
- `feedback.correct_rationale`
- `feedback.why_other_options_are_wrong`
- `feedback.remediation_recommendation`
- full governance constants
- `attempt_analytics_placeholders`

Enrichment must be traceable. A candidate with unsupported rationale,
unsupported source support, or invented diagnostic metadata must fail
validation.

## 7. Allowed Enrichment Sources

Future enrichment may use only repo-local lightweight sources:

- Official WSET Markdown for grounding only, not wording imitation.
- Wine With Jimmy chunks for pedagogical explanation and remediation support.
- Knowledge-map causal chains.
- Knowledge-map misconceptions.
- Knowledge-map concepts and relationships.
- Canonical dictionary assets.
- SAT aliases and SAT resources.
- Existing `expected_topics`.
- Existing `expected_keywords`.
- Existing `expected_causal_links`.
- Already extracted chunks and JSON/JSONL inventories.

The adapter must not depend on Excel, Word, PDF, OCR, external websites,
external APIs, runtime LLM generation, embeddings, vector databases, or cloud
services.

## 8. Forbidden Behaviors

The adapter must not:

- Modify `knowledge/question-bank/structured/wset3_questions.json`.
- Overwrite source records.
- Create generated questions.
- Create a bulk converted bank without separate approval.
- Change original question text silently.
- Invent source support.
- Invent missing WSET authority.
- Mark anything `safe_for_examiner = true`.
- Set `examiner_scoring_allowed = true`.
- Set `official_wset_question = true`.
- Assign official marks or examiner scores.
- Produce pass, fail, certification, or guaranteed outcome claims.
- Treat `source_type` as sufficient source support.
- Treat keyword overlap as sufficient rationale.
- Force `short_answer` items into SBA form.
- Hide invalid answer keys or duplicate options.

Failures must be explicit and deterministic.

## 9. Candidate Categories

Every source record should be classified before adaptation.

### 9.1 `adapter_ready_clean_pilot`

Use this category for records that satisfy all structural pilot conditions:

- `question_type == "theory"`.
- Exact A-D options present.
- All A-D options non-empty.
- No duplicate option text after normalization.
- Valid A-D `correct_answer_letter`.
- Non-empty `correct_answer_text`.
- Correct answer text matches the selected option.
- `expected_topics` present.
- `expected_reasoning_type` present.
- `safe_for_examiner = false`.
- No obvious official-authority wording.

This category still requires enrichment before validation.

### 9.2 `requires_source_grounding`

Use this category when the item is structurally usable but lacks validated
source support from allowed repo-local sources.

These items must not become valid diagnostic SBA items until source support,
support rationale, and curriculum grounding are attached.

### 9.3 `requires_option_diagnostics`

Use this category when the item has valid option shape and answer key but
options lack diagnostic roles, misconception links, or clear wrong-option
rationales.

These items must not enter a diagnostic bank until option metadata is complete.

### 9.4 `preserve_for_open_response`

Use this category for `short_answer`, open-response, development, and free-text
prompts.

These records are valuable but must be routed to a future open-response schema
instead of being compressed into A-D form.

### 9.5 `reject_or_defer`

Use this category for records with:

- missing or invalid answer letters;
- empty options;
- duplicate options that cannot be resolved safely;
- unsupported source claims;
- official wording risk requiring manual review;
- ambiguous or multiple plausible answers;
- any unsafe governance signal.

Rejected or deferred records must retain lineage and rejection reasons.

## 10. Safety Policy

Adapter outputs are training-only candidates. They are not official questions,
not examiner materials, and not scoring artifacts.

Every output candidate must preserve these governance values:

```json
{
  "safe_for_examiner": false,
  "examiner_scoring_allowed": false,
  "official_wset_question": false,
  "training_item_only": true,
  "uses_llm": false,
  "uses_api": false,
  "uses_embeddings": false,
  "uses_vector_db": false,
  "cloud_services_active": false
}
```

The adapter must never upgrade safety. It can only preserve safe-false
governance, add missing false constants, or fail closed.

Official WSET Markdown may ground a fact, but adapted wording must not imitate
protected official phrasing. If a source item appears too close to official
wording, it must be marked for manual review, not converted automatically.

## 11. Lineage Policy

Every adapted candidate must preserve lineage fields.

Required lineage metadata:

- `source_bank_path`
- `source_question_id`
- `source_question_type`
- `source_source_type`
- `adapter_version`
- `adapted_at`
- `transformation_notes`

Recommended additional lineage metadata:

- `source_question_hash`
- `source_options_hash`
- `source_expected_topics`
- `source_expected_keywords`
- `source_expected_causal_links`
- `classification_category`
- `rejection_or_deferral_reasons`
- `manual_review_required`

Lineage may be stored inside an approved future identity/provenance extension.
If the current diagnostic schema does not allow additional fields, the adapter
must not bypass the schema; instead, a future schema extension or sidecar audit
record must be approved first.

## 12. Validation Pipeline

Future adapted items must pass this minimum pipeline:

1. Source-record structural classification.
2. Adapter eligibility filter.
3. Deterministic field mapping.
4. Source-support enrichment.
5. Option diagnostic enrichment.
6. Governance constant application.
7. Diagnostic SBA JSON Schema validation.
8. `validate_diagnostic_sba_item(item)` validation.
9. Source support validation.
10. Option diagnostics validation.
11. Official wording and authority-language scan.
12. Lineage completeness check.

An item that fails any step must not enter a validated diagnostic bank.

## 13. Pilot Strategy

The first adapter pilot should be small and reviewable.

Recommended pilot size:

- 20-50 items maximum.

Pilot subset criteria:

- Clean A-D options.
- No duplicate option text after normalization.
- Valid A-D correct answer letter.
- Non-empty correct answer text.
- Correct answer text matches the selected option.
- `question_type == "theory"`.
- `expected_topics` present.
- `expected_reasoning_type` present.
- Source support can be attached from approved repo-local sources.
- Distractors can be assigned meaningful diagnostic roles.
- Low official wording risk after scan and review.
- `source_type` acceptable as provenance, not as sole support.
- Remediation route exists.

Recommended pilot exclusions:

- `short_answer`.
- true/false rows represented through `Verdadero` or `Falso`.
- records with empty option values.
- records with duplicate option text.
- records that require rewriting to become coherent.
- records without source support.
- records that look like official-question wording.

The pilot must optimize for clean validation and auditability, not count.

## 14. Open-Response Preservation Policy

The 21 `short_answer` records must not be forced into diagnostic SBA form.

Preservation rules:

- Keep original prompts as open-response candidates.
- Preserve `question_id`, `question_text`, `expected_topics`,
  `expected_causal_links`, `expected_keywords`, `expected_reasoning_type`,
  `difficulty`, `source_type`, and `safe_for_examiner`.
- Route them to a future open-response schema and evaluator contract.
- Use existing keywords and causal links as future rubric hints, not as
  automatic grading authority.
- Apply the same governance restrictions: no official scoring, no certification
  claims, no examiner authority.

Future open-response work should define separate structures for rubric support,
model answers, expected reasoning, misconception detection, and remediation.

## 15. Adapter Output States

A future adapter should distinguish these states:

| State | Meaning |
| --- | --- |
| `classified_only` | Source record was read and categorized, but no adapted item was created. |
| `mapped_draft` | Direct field mapping exists, but enrichment is incomplete. |
| `enriched_candidate` | Source support, diagnostics, feedback, and governance were attached. |
| `validated_item` | Candidate passed schema and validator checks. |
| `deferred` | Record is valuable but cannot be safely adapted yet. |
| `rejected` | Record fails a hard safety or structural rule. |

Only `validated_item` outputs may be considered for a future pilot diagnostic
bank, and only after a separate migration phase authorizes file creation.

## 16. Future Implementation Boundaries

When implementation is approved, the adapter should be read-only by default.

Future implementation requirements:

- no file writes unless explicit output path is supplied;
- dry-run mode by default;
- deterministic ordering by source `question_id`;
- deterministic error ordering;
- no mutation of input records;
- no external dependencies unless separately approved;
- no network access;
- no LLM calls;
- no embeddings or vector DB calls;
- no import-time side effects.

## 17. Recommended Next Phase

Phase 4A.3.7.2 - Structured Question Bank Adapter Test Plan.

The next phase should define read-only tests and expected counts before any
adapter implementation exists. The test plan should lock:

- total source count;
- count by `question_type`;
- strict candidate count;
- clean pilot candidate count;
- short-answer preservation count;
- invalid answer-letter count;
- empty-option count;
- duplicate-option count;
- governance expectations;
- no-write guarantees.

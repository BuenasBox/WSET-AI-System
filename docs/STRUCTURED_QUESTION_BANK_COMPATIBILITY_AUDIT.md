# Structured Question Bank Compatibility Audit

Phase: 4A.3.7

Status: audit-only. No question-bank records were modified, migrated, generated, parsed, or converted.

## Scope

Primary file audited:

- `knowledge/question-bank/structured/wset3_questions.json`

Compared against:

- `docs/DIAGNOSTIC_SBA_GOVERNANCE_CONTRACT.md`
- `docs/DIAGNOSTIC_SBA_ITEM_SCHEMA.md`
- `knowledge/enrichment/diagnostic_sba_item.schema.json`
- `tools/question_generation/diagnostic_sba_validator.py`
- `docs/DIAGNOSTIC_OUTCOME_MODEL.md`
- `knowledge/enrichment/diagnostic_outcome.schema.json`

This audit evaluates compatibility only. It does not authorize bulk conversion.

## 1. Current Bank Counts

| Metric | Count |
| --- | ---: |
| Total records | 616 |
| `theory` | 595 |
| `short_answer` | 21 |
| Records with `options` object | 616 |
| Records with exact A-D option keys | 616 |
| Records with non-empty A-D options | 525 |
| Records with valid A-D `correct_answer_letter` | 591 |
| Records with non-empty `correct_answer_text` | 596 |
| Records with exactly one answer by valid letter | 591 |
| Basic SBA candidates: A-D keys + valid answer letter | 591 |
| Strict SBA candidates: non-empty A-D + valid letter + correct text | 525 |
| Strict `theory` candidates | 524 |
| Strict `short_answer` candidates | 1 |
| Clean pilot candidates after excluding duplicate options | 520 |

Difficulty distribution:

| Difficulty | Count |
| --- | ---: |
| `intermediate` | 601 |
| `distinction` | 10 |
| `foundational` | 5 |

Reasoning type distribution:

| Reasoning type | Count |
| --- | ---: |
| `theory_foundation` | 596 |
| `cause_effect` | 20 |

Governance:

- All 616 records have `safe_for_examiner = false`.
- No obvious official-authority wording was found using a conservative scan for phrases such as "official WSET question", "examiner mark", "certified result", "guaranteed pass", and "WSET official".

## 2. SBA Compatibility Estimate

The bank is partially compatible with the future Diagnostic SBA architecture, but not schema-compatible as-is.

Compatibility bands:

| Band | Count | Meaning |
| --- | ---: | --- |
| Direct diagnostic SBA-ready | 0 | No records have full `diagnostic_sba_item_v1` structure, source support, option diagnostic roles, feedback block, or full governance block. |
| Strict migration candidates | 525 | Have non-empty A-D options, valid correct answer letter, and correct answer text. |
| Clean pilot candidates | 520 | Strict `theory` records with non-empty unique option text. |
| Basic migration candidates | 591 | Have A-D keys and a valid A-D answer letter, but may include empty or duplicate option text. |
| Preserve for open-response | 21 | `short_answer` records should not be forced into SBA without separate open-response design. |
| Needs repair before consideration | 91 | Records with one or more empty A-D option values. |
| Invalid for current SBA migration | 25 | Records without valid A-D answer letter. |

The practical pilot pool should be the 520 clean `theory` records, further reduced by topic/source/manual review criteria.

## 3. Existing Field Mapping

| Existing field | Diagnostic SBA target | Compatibility |
| --- | --- | --- |
| `question_id` | `identity.item_id` | Usable with deterministic prefix/versioning. |
| `question_text` | `question.stem` | Usable only after wording and source-support review. |
| `question_type` | `question.question_type` | Not directly compatible. Must become `single_best_answer`. Existing `theory` is too broad. |
| `expected_reasoning_type` | `question.expected_reasoning_type` | Partial. Existing `theory_foundation` is not an allowed schema value; `cause_effect` maps directly. |
| `difficulty` | `curriculum.difficulty` | Partial. `foundational`, `intermediate`, `distinction` are allowed; no `advanced` present. |
| `expected_topics` | `curriculum.ra_id`, `topic`, `subtopic` | Partial. Needs deterministic parsing/enrichment. |
| `expected_causal_links` | source/diagnostic metadata; possible `causal_chain_id` extension | Useful enrichment input, not a schema field as-is. |
| `expected_keywords` | source support, rationale, remediation hints | Useful enrichment input, not a schema field as-is. |
| `source_type` | `source_support.source_ids` or provenance metadata | Partial. It identifies source workbook/sheet/provenance, not source chunks. |
| `safe_for_examiner` | `governance.safe_for_examiner` | Compatible for this one flag; all are false. |
| `options.A-D` | `options.A-D.option_text` | Partial. Need `option_id`, `is_correct`, `diagnostic_role`, optional misconception metadata. |
| `correct_answer_letter` | `options.<letter>.is_correct = true` | Usable when A-D. Invalid for 25 records. |
| `correct_answer_text` | `feedback.correct_rationale` support / answer verification | Partial. It is answer text, not a rationale. |

## 4. Missing Required Diagnostic Fields

Every existing record is missing the diagnostic item top-level structure:

- `schema_version`
- `identity`
- `curriculum`
- `question`
- `source_support`
- `feedback`
- `governance` full block
- `attempt_analytics_placeholders`

Every existing option is missing:

- `option_id`
- `is_correct`
- `diagnostic_role`
- optional `misconception_id`
- optional `misconception_description`

Every item is missing mandatory source support:

- `source_ids`
- `source_chunks`
- `support_rationale`

Every item is missing mandatory feedback support:

- `correct_rationale`
- `why_other_options_are_wrong`
- `remediation_recommendation`

Every item is missing full governance fields required by the new contract:

- `examiner_scoring_allowed = false`
- `official_wset_question = false`
- `training_item_only = true`
- `uses_llm = false`
- `uses_api = false`
- `uses_embeddings = false`
- `uses_vector_db = false`
- `cloud_services_active = false`

## 5. Enrichment Required

Required before migration:

1. Source support
   - Map each item to repo-local official chunks, official Markdown, knowledge-map nodes, or pedagogical chunks.
   - Add item-level `source_support`.
   - Avoid using `source_type` alone as source support.

2. Curriculum segmentation
   - Derive `ra_id`, `topic`, `subtopic`, and `learning_objective`.
   - Existing `expected_topics` is a useful hint but not enough.

3. Diagnostic option roles
   - Assign `correct` to the correct option.
   - Assign distractor roles such as `misconception`, `partial_reasoning`, `keyword_trap`, `causal_confusion`, `regional_confusion`, or `term_confusion`.

4. Misconception linking
   - Link distractors to `misconception_id` where a knowledge-map misconception exists.
   - Do not invent misconception IDs.

5. Causal-chain linkage
   - Use `expected_causal_links` and knowledge-map causal chains as enrichment hints.
   - Store linkage as metadata only after schema/contract approval if not present in `diagnostic_sba_item_v1`.

6. SAT relevance
   - Identify SAT items using `expected_topics`, keywords, and source support.
   - Do not infer SAT relevance solely from wine terms.

7. Feedback rationales
   - Write `correct_rationale`.
   - Explain why each distractor is wrong.
   - Add remediation recommendation.

8. Attempt analytics placeholders
   - Add null placeholders for response time, confidence, answer changes, diagnosed error type, hesitation, and recommended next action.

## 6. Safety Risks

| Risk | Status | Notes |
| --- | --- | --- |
| Official wording risk | Medium | `source_type` references WSET3 bancos and imported workbook names. No obvious official-authority phrases found, but source provenance alone does not prove wording safety. |
| Missing source support | High | No item has mandatory diagnostic `source_support`. |
| Ambiguous/duplicate options | Medium | 95 records have duplicate option text by normalized comparison; 91 have empty option values. Many are likely true/false or open-answer structures, not SBA. |
| Unsafe governance | Low/Medium | Existing `safe_for_examiner=false` is good, but full governance block is missing everywhere. |
| Answer mismatch | Low among strict candidates | For records with A-D option, valid letter, and answer text, no exact option-vs-answer-text mismatch was found. |
| Unsupported rationale | High | Existing bank has answers/keywords, not source-grounded rationales. |
| Short-answer loss | High if bulk converted | 21 `short_answer` records should be preserved for open-response phases. |
| Schema overconfidence | High | A-D presence does not imply diagnostic readiness. |

Invalid answer-letter details:

- 20 records have empty `correct_answer_letter`.
- 3 records use `Falso`.
- 2 records use `Verdadero`.

The `Verdadero`/`Falso` records are not directly compatible with A-D SBA unless deliberately transformed and validated.

## 7. Short-Answer / Open-Response Preservation

The 21 `short_answer` records should be preserved for a later open-response schema. They include one legacy structured item and 20 open/development-style prompts.

Observed open-response source types include:

- `WSET3_RA1_Banco_Preguntas_TOTAL.xlsx | Abiertas`
- `WSET3_RA1_Banco_Preguntas_Bloque2.xlsx | Preguntas_Abiertas`
- `WSET3_RA1_Banco_Preguntas_Bloque8.xlsx | Desarrollo`
- `structured_question_bank`

Preservation rules:

- Do not bulk-convert short-answer prompts into SBA.
- Tag them later for open-response evaluation.
- Preserve `expected_topics`, `expected_causal_links`, and `expected_keywords` as rubric/evaluation hints.
- Add governance boundaries before runtime use.

## 8. Recommended Pilot Subset Criteria

A safe first pilot migration should use a tiny subset, not the full 520 clean candidate pool.

Recommended pilot item criteria:

- `question_type == "theory"`
- exact A-D options present
- all A-D option texts non-empty
- no duplicate option texts after normalization
- valid `correct_answer_letter` in A-D
- non-empty `correct_answer_text`
- answer text exactly matches the selected option text
- `safe_for_examiner == false`
- no official-authority wording
- `expected_topics` present and mappable to RA/topic/subtopic
- source support can be attached from official chunks, knowledge-map nodes, or Wine With Jimmy chunks
- distractors can be assigned clear diagnostic roles
- at least one remediation path exists

Recommended exclusions for pilot:

- `short_answer`
- true/false rows represented as `Verdadero`/`Falso`
- rows with empty option values
- rows with duplicate option values
- rows whose source support cannot be found
- rows requiring extensive rewriting
- rows that look official-question-like after manual review

Suggested pilot size:

- 10-25 items across 2-4 high-confidence topics.

Good early topic families:

- cause/effect viticulture and winemaking
- MLF, oak, acidity, tannin, botrytis, cool/warm climate
- topics already supported by knowledge-map concepts, misconceptions, and causal chains

## 9. Migration Strategy

Recommended sequence:

1. Create a compatibility adapter contract.
   - Define deterministic mapping from current bank fields to diagnostic draft fields.
   - Do not write migrated items yet.

2. Build read-only compatibility tests.
   - Lock current counts and risk metrics.
   - Ensure future migration does not accidentally include open-response items.

3. Select pilot candidates.
   - Use strict criteria.
   - Manual review for wording and source support.

4. Enrich pilot candidates.
   - Add source support, diagnostic roles, rationales, remediation, full governance, and attempt placeholders.

5. Validate with existing `validate_diagnostic_sba_item`.
   - No item enters any generated bank unless validator passes.

6. Preserve short-answer records.
   - Route to future open-response schema rather than forcing conversion.

7. Avoid bulk conversion.
   - Bulk conversion should wait until manifest reconciliation, source support mapping, and pilot validation are stable.

## 10. Compatibility Verdict

The structured question bank is strategically valuable and should be the first source for a controlled SBA migration pilot. It is not directly compatible with `diagnostic_sba_item_v1`.

The key reason is not option shape. The bank already has many A-D structures. The blockers are diagnostic architecture requirements:

- item-level source support
- diagnostic distractor metadata
- misconception/causal-chain linkage
- source-grounded rationales
- remediation recommendations
- full governance block
- attempt analytics placeholders

The safest next step is an adapter contract and read-only compatibility test phase before any item migration.

## 11. Recommended Next Phase

Phase 4A.3.7.1 - Structured Question Bank Adapter Contract.

This should define, without writing migrated items:

- field mapping rules
- exclusion rules
- pilot candidate filters
- source support requirements
- diagnostic enrichment requirements
- validation gates
- open-response preservation rules

# Question Bank Markdown Inventory

Phase: 4A.3.6 - Markdown inventory and ingestion plan

Status: documentation-only checkpoint. No questions were generated, converted, parsed, or moved.

## Scope

This inventory covers repo-local lightweight artifacts only. The scan focused on Markdown files, with related JSON/Python/test references considered only for context. Excel, Word, PDF, OCR, external websites, APIs, embeddings, vector databases, and LLM generation are out of scope.

Authoritative upstream contracts:

- `docs/DIAGNOSTIC_SBA_GOVERNANCE_CONTRACT.md`
- `docs/DIAGNOSTIC_SBA_ITEM_SCHEMA.md`
- `docs/DIAGNOSTIC_OUTCOME_MODEL.md`
- `knowledge/enrichment/diagnostic_sba_item.schema.json`
- `knowledge/enrichment/diagnostic_outcome.schema.json`
- `tools/question_generation/diagnostic_sba_validator.py`

## Inventory Method

Repo scan commands used:

- `rg --files -g "*.md"`
- targeted `rg` searches for question-bearing language in Markdown files
- targeted reads of candidate Wine With Jimmy, retrieval sandbox, and self-evaluation Markdown files

Summary:

- Total Markdown files located: 159
- Official WSET study-guide Markdown files: 52
- Wine With Jimmy cleaned transcript Markdown files: 30
- Markdown files under `knowledge/question-bank/`: 0

The existing canonical structured question bank is not Markdown:

- `knowledge/question-bank/structured/wset3_questions.json`

That JSON file may be relevant to future ingestion phases, but this phase does not inspect or transform it as Markdown source material.

## Task A - Markdown Source Classification

### SBA Question Source

Confirmed direct SBA-style Markdown source:

- `knowledge/wine-with-jimmy/clean/WSET_Level_3_Mock_Theory_Exam_Questions_Part_1_of_4_with_Jimmy_Smith_D.clean.md`

This file contains 10 multiple-choice questions in transcript form, followed by one short-written-answer question. It is not already structured as diagnostic SBA JSON.

### Short-Answer Question Source

Confirmed short-answer/open-response Markdown sources:

- `knowledge/wine-with-jimmy/clean/Viticulture_Exam_Prep_WSET_Level_3_Sample_Questions.clean.md`
- `knowledge/wine-with-jimmy/clean/Master_Winemaking_for_WSET_Level_3_Exam_Clarification_Techniques_Explained.clean.md`
- `knowledge/wine-with-jimmy/clean/Mastering_Sweet_Wine_Production_for_Level_3_Exams_Wine_with_Jimmy.clean.md`
- `knowledge/wine-with-jimmy/clean/WSET_L3_Understanding_Growing_Environment_Problems_Short_Written_Question_Part_1.clean.md`
- `knowledge/wine-with-jimmy/clean/WSET_Level_3_Wines_-_Understanding_Aromatics_With_Working_Written_Questio.clean.md`
- `knowledge/wine-with-jimmy/clean/0LRBstQgK0I__Understanding_Southern_France_for_WSET_Level_3_Wines_Part_1_-_Climate_Grapegrowing_&_Grape_Varieties.clean.md`

These are pedagogical transcripts with question and answer discussion embedded in prose.

### Open-Response Question Source

The short-answer files above should also be treated as future open-response sources. They contain mark-bearing written-answer patterns and answer-structure explanations that do not naturally fit four-option SBA without loss of learning value.

### Mock/Sample Question Source

Mock/sample question-bearing files:

- `knowledge/wine-with-jimmy/clean/WSET_Level_3_Mock_Theory_Exam_Questions_Part_1_of_4_with_Jimmy_Smith_D.clean.md`
- `knowledge/wine-with-jimmy/clean/Viticulture_Exam_Prep_WSET_Level_3_Sample_Questions.clean.md`
- `knowledge/wine-with-jimmy/clean/Master_Winemaking_for_WSET_Level_3_Exam_Clarification_Techniques_Explained.clean.md`
- `knowledge/wine-with-jimmy/clean/Mastering_Sweet_Wine_Production_for_Level_3_Exams_Wine_with_Jimmy.clean.md`

These are not official WSET questions. They are third-party pedagogical examples and must retain `safe_for_examiner=false`.

### Official/Reference Knowledge Source

Official/reference Markdown sources:

- `knowledge/official-wset/study-guide/wset_markdown/**/*.md`
- `knowledge/official-wset/study-guide/official_wset_chunks_report.md`

These should be used for source grounding only, not wording imitation.

### Mixed

Mixed diagnostic/reporting artifacts:

- `knowledge/self-eval/self_eval_summary.md`
- `knowledge/self-eval/before_vs_after_self_eval.md`
- `knowledge/self-eval/causal_chain_impact_report.md`
- `knowledge/retrieval-sandbox/*.md`
- `prompts/tutor-agent.md`
- `prompts/examiner-agent.md`

These contain evaluation, retrieval, answer-structure, prompt, or system-behavior information. They are useful for design constraints but should not be converted into diagnostic SBA items.

### Not Relevant

Most project, architecture, governance, roadmap, dashboard, deployment, and setup Markdown files are not question-bearing. They should remain outside question ingestion.

Examples:

- `README.md`
- `CLAUDE.md`
- `AGENTS.md`
- `docs/DIAGNOSTIC_SBA_GOVERNANCE_CONTRACT.md`
- `docs/DIAGNOSTIC_SBA_ITEM_SCHEMA.md`
- `docs/DIAGNOSTIC_OUTCOME_MODEL.md`
- `docs/STRATEGIC_PLANNER_CONTRACT.md`
- `docs/PLANNER_INFLUENCE_BOUNDARY.md`
- `frontend/architecture-dashboard/README.md`

## Task B - Question-Bearing Markdown Inventory

| Path | Approx. question count | Question type | Answers included | Rationales included | Explicit source support | RA/topic/subtopic mapping | Diagnostic metadata | Maps to `diagnostic_sba_item_v1` | Maps later to open-response | Enrichment required |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `knowledge/wine-with-jimmy/clean/WSET_Level_3_Mock_Theory_Exam_Questions_Part_1_of_4_with_Jimmy_Smith_D.clean.md` | 10 SBA-style MCQ + 1 short written | Mixed: SBA-style, short answer, mock | Yes, embedded in transcript | Yes, embedded but noisy | No item-level source support | No explicit RA/subtopic fields | No | Yes, with heavy enrichment | Yes | Segment items, reconstruct A-D options, normalize answer keys, add source chunks, add RA/topic/subtopic, add diagnostic roles, remove authority language, validate no wording leakage |
| `knowledge/wine-with-jimmy/clean/Viticulture_Exam_Prep_WSET_Level_3_Sample_Questions.clean.md` | 1 multi-part short-answer sample | Short answer/open response | Yes | Yes | No item-level source support | Topic implied: viticulture/weather/rainfall | No | Not directly | Yes | Preserve as open-response; optionally derive SBA later from grounded concepts, not from wording |
| `knowledge/wine-with-jimmy/clean/Master_Winemaking_for_WSET_Level_3_Exam_Clarification_Techniques_Explained.clean.md` | 1 multi-part short-answer sample | Short answer/open response | Yes | Yes | No item-level source support | Topic implied: winemaking/clarification | No | Not directly | Yes | Preserve for open-response; could support later deterministic distractors after source grounding |
| `knowledge/wine-with-jimmy/clean/Mastering_Sweet_Wine_Production_for_Level_3_Exams_Wine_with_Jimmy.clean.md` | 1 multi-part short-answer sample | Short answer/open response | Yes | Yes | No item-level source support | Topic implied: sweet wine production | No | Not directly | Yes | Preserve for open-response; source-map before any SBA derivation |
| `knowledge/wine-with-jimmy/clean/WSET_L3_Understanding_Growing_Environment_Problems_Short_Written_Question_Part_1.clean.md` | 2 short-answer examples | Short answer/open response | Yes | Yes | No item-level source support | Topic implied: growing environment problems | No | Not directly | Yes | Preserve; derive future remediation patterns for frost/freeze concepts |
| `knowledge/wine-with-jimmy/clean/WSET_Level_3_Wines_-_Understanding_Aromatics_With_Working_Written_Questio.clean.md` | 1 short-answer example | Short answer/open response | Yes | Yes | No item-level source support | Topic implied: aromatic varieties/winemaking | No | Not directly | Yes | Preserve; useful for causal reasoning and remediation, not direct SBA conversion |
| `knowledge/wine-with-jimmy/clean/0LRBstQgK0I__Understanding_Southern_France_for_WSET_Level_3_Wines_Part_1_-_Climate_Grapegrowing_&_Grape_Varieties.clean.md` | 3 short-answer prompts | Short answer/open response | Yes | Yes | No item-level source support | Topic implied: Southern France/climate/winds | No | Not directly | Yes | Preserve; source-map to official markdown before reuse |

Notes:

- The only file with clear SBA-style material is the mock theory transcript.
- None of the Markdown question-bearing files are already safe to load as canonical diagnostic SBA items.
- None contain diagnostic distractor roles, `misconception_id`, item-level governance metadata, or source chunks aligned to the current schema.

## Task C - Reference Markdown Inventory

| Path group | Topic coverage | Usefulness for source support | Usefulness for future generation | Wording leakage risk | Recommended use |
| --- | --- | --- | --- | --- | --- |
| `knowledge/official-wset/study-guide/wset_markdown/**/*.md` | Official WSET study-guide coverage across Level 3 topics | High | High for grounding only | High | Use for `source_support`, RA/topic mapping, and concept verification. Do not imitate phrasing. Do not create official-looking items. |
| `knowledge/official-wset/study-guide/official_wset_chunks_report.md` | Chunking/report metadata | Medium | Medium | Medium | Use to understand chunk quality and coverage. Do not convert into items. |
| `knowledge/wine-with-jimmy/clean/*.md` | Pedagogical transcripts across WSET L3 theory, SAT, regions, viticulture, winemaking, exam strategy | Medium | Medium | Medium | Use as pedagogical support and possible source candidates after cleaning and mapping. Keep `source_trust_tier=pedagogical`. |
| `knowledge/retrieval-sandbox/*.md` | Retrieval run outputs and retrieved excerpts | Low to medium | Low | Medium | Use for retrieval diagnostics only. Do not convert to question items. |
| `knowledge/self-eval/*.md` | Tutor self-evaluation outcomes and reports | Low | Low | Low | Use for model evaluation context only. Do not convert to question items. |
| `knowledge/map/**/*.md` and `knowledge/knowledge-map/**/*.md` | Knowledge map documentation/placeholders | Low | Low | Low | Use as architecture context only. |

Reference Markdown must support source-grounded generation by concept, not by copied wording. Any future converter must separate "source grounding" from "question wording."

## Task D - Conversion Readiness

### Ready For Pilot Conversion

None.

No Markdown file currently satisfies the diagnostic SBA schema without enrichment. The closest source has options and answers embedded in noisy transcript prose, not structured item fields.

### Convertible With Enrichment

- `knowledge/wine-with-jimmy/clean/WSET_Level_3_Mock_Theory_Exam_Questions_Part_1_of_4_with_Jimmy_Smith_D.clean.md`

Required enrichment:

- deterministic segmentation into 10 SBA-style items
- option reconstruction into A/B/C/D
- correct answer extraction
- duplicate/empty option checks
- RA/topic/subtopic mapping
- item-level source support from official/reference Markdown
- diagnostic roles for distractors
- `misconception_id` where available
- governance metadata enforced by validator
- wording-leakage review

### Preserve But Do Not Convert Yet

- `knowledge/wine-with-jimmy/clean/Viticulture_Exam_Prep_WSET_Level_3_Sample_Questions.clean.md`
- `knowledge/wine-with-jimmy/clean/Master_Winemaking_for_WSET_Level_3_Exam_Clarification_Techniques_Explained.clean.md`
- `knowledge/wine-with-jimmy/clean/Mastering_Sweet_Wine_Production_for_Level_3_Exams_Wine_with_Jimmy.clean.md`
- `knowledge/wine-with-jimmy/clean/WSET_L3_Understanding_Growing_Environment_Problems_Short_Written_Question_Part_1.clean.md`
- `knowledge/wine-with-jimmy/clean/WSET_Level_3_Wines_-_Understanding_Aromatics_With_Working_Written_Questio.clean.md`
- `knowledge/wine-with-jimmy/clean/0LRBstQgK0I__Understanding_Southern_France_for_WSET_Level_3_Wines_Part_1_-_Climate_Grapegrowing_&_Grape_Varieties.clean.md`
- `knowledge/retrieval-sandbox/*.md`
- `knowledge/self-eval/*.md`

These materials are better preserved for open-response schema design, remediation design, and answer-structure modeling.

### Unsafe / Ambiguous / Official Wording Risk

- `knowledge/official-wset/study-guide/wset_markdown/**/*.md`
- Any retrieved official excerpts inside `knowledge/retrieval-sandbox/*.md`
- Any transcript text that claims examiner authority, marks, guarantees, pass/fail outcomes, or official WSET status

These may support grounding and validation, but must not be copied into question stems/options/rationales.

## Task E - Open-Response Preservation

Short-answer/open-response Markdown should be preserved for future open-response evaluator phases. Do not force it into four-option SBA when the learning value depends on causality, sequencing, explanation quality, or mark allocation.

Future tags should include:

- `source_path`
- `source_trust_tier`
- `question_type`
- `preserve_for_open_response=true`
- `not_sba_reason`
- `candidate_prompt_text`
- `candidate_model_answer`
- `topic`
- `subtopic`
- `ra_id`
- `expected_reasoning_type`
- `rubric_hint`
- `source_support`
- `official_wording_risk`
- `safe_for_examiner=false`
- `examiner_scoring_allowed=false`
- `training_item_only=true`

Open-response candidates should not receive official marks. They may include training rubrics, reasoning expectations, and diagnostic feedback boundaries later.

## Task F - Future Ingestion Architecture

Proposed modules only; do not implement in this phase:

- `tools/question_generation/markdown_question_inventory.py`
- `tools/question_generation/markdown_sba_parser.py`
- `tools/question_generation/markdown_open_response_parser.py`
- `tools/question_generation/markdown_reference_mapper.py`
- `tools/question_generation/question_bank_ingestion_plan.py`

Recommended responsibilities:

- `markdown_question_inventory.py`: locate and classify Markdown sources deterministically.
- `markdown_sba_parser.py`: parse only files explicitly approved as SBA-style candidates.
- `markdown_open_response_parser.py`: preserve short-answer/open-response materials without converting them to SBA.
- `markdown_reference_mapper.py`: map candidate items to official/reference source chunks.
- `question_bank_ingestion_plan.py`: produce a machine-readable plan, not generated items.

All modules must be standard-library only unless a later phase explicitly approves dependencies.

## Task G - Proposed Destination Structure

Proposed destination structure only; do not create in this phase:

- `knowledge/question-bank/diagnostic_sba/source_inventory.json`
- `knowledge/question-bank/diagnostic_sba/converted/`
- `knowledge/question-bank/diagnostic_sba/rejected/`
- `knowledge/question-bank/diagnostic_sba/manual_review/`
- `knowledge/question-bank/open_response/source_inventory.json`
- `knowledge/question-bank/open_response/candidates/`
- `knowledge/question-bank/reference_grounding/`
- `knowledge/question-bank/ingestion_reports/`

The first machine-readable inventory should be generated only after a parser contract exists.

## Task H - Safe Conversion Roadmap

Recommended next phases:

1. 4A.3.7 - Markdown Question Inventory Report
   - Create deterministic inventory script and JSON report.
   - No conversion.

2. 4A.3.8 - Markdown SBA Parser Contract
   - Define parser input/output behavior.
   - Define approved source allowlist and rejection categories.
   - No generated bank.

3. 4A.3.9 - Small SBA Pilot Conversion
   - Convert a tiny manually reviewed subset from the mock theory transcript.
   - Require validator pass.
   - Require source support from reference Markdown.

4. 4A.4 - Deterministic SBA Template Generator
   - Proceed only after validator, parser contract, and pilot conversion are stable.

5. 4B - Open Response Question Schema
   - Preserve and model short-answer/open-response sources without forcing them into SBA.

## Governance Boundaries

Any future ingestion must preserve:

- `safe_for_examiner=false`
- `examiner_scoring_allowed=false`
- `official_wset_question=false`
- `training_item_only=true`
- `uses_llm=false`
- `uses_api=false`
- `uses_embeddings=false`
- `uses_vector_db=false`
- `cloud_services_active=false`

Forbidden conversion outcomes:

- official WSET questions
- official WSET marks
- examiner authority
- pass/fail certification claims
- protected wording imitation
- unsupported rationales
- generated content without source support

## Key Risks

1. No Markdown question file is schema-ready.

2. The best SBA candidate is a noisy auto-caption transcript. It will require human-reviewed segmentation or a very conservative deterministic parser.

3. Official/reference Markdown is valuable for grounding but dangerous as wording source. Future generation must paraphrase from grounded concepts and cite source chunks.

4. Short-answer material carries more pedagogical value as open-response training than as forced SBA conversion.

5. Transcript files contain tutor/exam strategy language, references to marks, and instructor authority. A future ingestion flow must strip or neutralize authority language before item creation.

6. The repo already contains structured JSON question material, but this phase intentionally did not ingest it because the requested scope is Markdown inventory.

## Recommendation

Proceed next with Phase 4A.3.7: Markdown Question Inventory Report.

That phase should create a deterministic inventory script and a machine-readable source inventory, but still avoid generation, conversion, and parser implementation beyond classification.

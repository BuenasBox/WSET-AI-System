# Phase 4A.0 - Single Best Answer Feasibility Audit

Date: 2026-05-29

Scope: audit-only feasibility review for deterministic, source-grounded WSET Level 3 single-best-answer training item generation.

This review intentionally used only lightweight repository artifacts: `.json`, `.jsonl`, `.md`, `.py`, tests, snapshots, configs, and text/json chunks already extracted. It did not read Excel, Word, PDF, PPT, OCR, external websites, APIs, embeddings, vector stores, or runtime LLM output.

## Verdict

Single-best-answer generation is viable now for a constrained first implementation, provided it is limited to training items, source-grounded rationales, deterministic templates, and strict governance validation.

The repo already has enough lightweight material to begin without Excel, PDF, or Word. The safest first generated items are cause/effect, vineyard factor, winemaking process, SAT-reasoning, misconception-correction, and vocabulary/definition questions. It is not yet ready for broad official-exam-like regional detail or questions that require inferred official marking intent.

## 1. Available Materials

| Source | Format | Approx. count | Usefulness for single-best-answer generation | Governance risk |
|---|---:|---:|---|---|
| `knowledge/question-bank/structured/wset3_questions.json` | JSON | 616 questions; 595 `theory`, 21 `short_answer`; 525 with A-D options; 20 open items without correct letter | High. Strong schema precedent for options, correct answer letter/text, expected topics, causal links, keywords, reasoning type, difficulty, and training-bank metadata. Useful as calibration, not as generation source by itself. | Medium. Existing items are training-bank material, but generator must avoid treating them as official WSET questions or copying protected wording. |
| `knowledge/question-bank/structured/_archive/wset3_questions.generated.json` | JSON | 616 archived questions | Low. Archived duplicate/obsolete bank should not be a generation source. | Medium. Useful only as historical artifact; avoid reading it in production generation to prevent duplicate or stale items. |
| `knowledge/self-eval/sample_questions.json` | JSON | 5 sample questions | Medium. Provides compact examples of expected fields and tutor/evaluator pathways. | Low. Small calibration set, not enough as a generation corpus. |
| `knowledge/self-eval/question_expectations.json` | JSON | 9 expectation templates | Medium. Useful for expected topics, causal links, keyword expectations, and deterministic evaluation behavior. | Low. Expectations are pedagogical metadata, not official scoring. |
| `knowledge/self-eval/self_eval_results.jsonl` and summaries | JSONL/MD | existing attempt/result history | Low/Medium. Can reveal stable weaknesses and answer patterns, but should not be a factual source. | Medium. Learner/output artifacts may contain noisy or model-generated text; use only for diagnostics. |
| `knowledge/knowledge-map/causal-chains/*.json` | JSON | 32 causal-chain nodes | High. Excellent basis for cause -> mechanism -> effect questions, correct rationales, causal distractors, SAT reasoning prompts, and source-grounding queries. | Low/Medium. Nodes are marked tutor-safe but not examiner-safe; generated items must remain training-only. |
| `knowledge/knowledge-map/misconceptions/*.json` | JSON | 20 misconception nodes | High. Strong source for plausible-but-wrong distractors and misconception-correction questions. | Low/Medium. Needs validator to ensure distractors are wrong but plausible, not ambiguous. |
| `knowledge/knowledge-map/concepts/*.json` | JSON | 8 concept nodes | High for early scope. Useful for definitions, related causal chains, related regions/grapes, and distinction insights. | Low/Medium. Limited coverage; not enough for broad syllabus generation. |
| `knowledge/knowledge-map/relationships/*.json` | JSON | 10 relationship nodes | Medium. Helpful for relationship-style items and graph consistency checks. | Low. Coverage is narrow. |
| `knowledge/knowledge-map/topics`, `regions`, `grape-varieties`, `tasting` | README/placeholders | no structured nodes found beyond README/.gitkeep | Low. Indicates planned taxonomy areas but not enough structured material yet. | Low. Main risk is overclaiming coverage. |
| `knowledge/knowledge-map/manifests/schemas/*.json` and manifest | JSON/MD | 5 schemas plus manifest | Medium. Useful for validator design and future graph-driven item provenance. | Low. Architecture metadata only. |
| `knowledge/enrichment/wset_master_dictionary/consolidated/canonical_terms_master.jsonl` | JSONL | 424 canonical terms | High. Strong term normalization, aliases, categories, RA/source hints, and safe-for-tutor flags. Useful for vocabulary items, option normalization, and detecting duplicate/near-duplicate options. | Medium. Entries reference official source documents in metadata; generator must not reproduce official wording or imply examiner authority. |
| `knowledge/enrichment/wset_master_dictionary/master_terms.jsonl` | JSONL | 680 raw terms | Medium. Broader but less consolidated. Useful as secondary normalization input. | Medium. Prefer consolidated canonical file for first implementation. |
| `knowledge/config/domain_expansions.json` | JSON | 3 SAT expansion keys; 18 domain expansion keys | Medium. Useful for synonym coverage, topic expansion, and option similarity controls. | Low. Expansion config is not factual authority. |
| `knowledge/config/sat_observation_aliases.json` | JSON | 10 SAT parameters | High for tasting/SAT items. Provides deterministic aliases for acidity, tannin, sweetness, body, finish, intensity, complexity, balance, condition, and development. | Medium. SAT items can become examiner-like; require training-only governance and no official scoring claims. |
| `knowledge/config/retrieval_config.json` | JSON | scoring weights/config | Medium. Useful for source-grounding thresholds and audit metadata, not item facts. | Low. Do not treat retrieval score as truth. |
| `knowledge/config/explanation_priority_config.json` | JSON | priority config | Low/Medium. Useful for rationale style priorities. | Low. Not a factual source. |
| `knowledge/official-wset/study-guide/official-chunks/official_wset_chunks.jsonl` | JSONL | 52 chunks | High for source support if used carefully. Provides already-extracted text chunks with trust tier, source type, safe-for-tutor, safe-for-examiner, and review metadata. | High. Official-source wording leakage is the primary risk. Use for grounding and validation, not direct question wording. |
| `knowledge/official-wset/study-guide/wset_markdown/**/*.md` | MD | 52 markdown files | High for source support, section coverage, and topic grounding. | High. Same official wording risk; generated questions must paraphrase via deterministic templates and be training-only. |
| `knowledge/official-wset/study-guide/artifacts/study_guide_learning_objectives.jsonl` | JSONL | 38 lines | High. Good source for RA/learning-outcome alignment. | Medium/High. Requires human verification notes in related artifacts; do not overstate official authority. |
| `knowledge/official-wset/study-guide/artifacts/study_guide_topic_hierarchy.json` | JSON | RA1-RA5, approx. 30 chapter entries | High. Useful for learning-outcome/topic placement. | Medium/High. Artifact has human-review warning; use as draft taxonomy until verified. |
| `knowledge/wine-with-jimmy/chunk-ready/*.jsonl` | JSONL | 30 files; 333 chunks | High for tutor-style source support, worked explanations, SAT discussion, and exam strategy context. | Medium. Pedagogical third-party transcript material; noisy transcription and outro/intro chunks must be filtered. |
| `knowledge/wine-with-jimmy/manual-import/reports/golden_tutor_chunk_candidates.jsonl` | JSONL | 166 candidates | Medium/High. Useful for selecting high-pedagogical-value chunks and avoiding low-quality source support. | Medium. Candidate status is not human approval. |
| `knowledge/wine-with-jimmy/manual-import/reports/` | JSON/JSONL/MD | 30 report files | Medium. Useful for chunk quality diagnostics and manual-import provenance. | Low/Medium. Metadata/reporting, not primary factual authority. |
| `knowledge/wine-with-jimmy/clean/` | JSON/MD | 30 cleaned text artifacts | Medium. Useful as source text if chunk-ready material is insufficient. | Medium. Use chunk-ready first because it has richer metadata. |
| `knowledge/wine-with-jimmy/metadata/` | JSON | 377 metadata files | Low/Medium. Useful for provenance and source labels, not question content. | Low. Metadata only. |
| `tests/test_question_bank_converter.py` | Python tests | 333 lines | High for schema and loader compatibility. Encodes expectations around question-bank conversion, open-question preservation, and `load_questions()`. | Low. Test behavior, not content authority. |
| `tools/self_eval/question_runner.py` and `tools/self_eval/answer_comparator.py` | Python | live self-eval loading/comparison logic | Medium. Useful to keep generated item schema compatible with current training/evaluation paths. | Low. No generator should grant examiner authority. |
| `tests/fixtures/tutor_snapshots/` | JSON fixtures | 25 snapshot entries; 20 theory and 5 short_answer | Medium. Useful for stable tutor answer patterns, governance language, and regression behavior. | Low/Medium. Snapshots are outputs/fixtures, not factual sources. |

## 2. Positive Findings

- The structured bank already contains a practical single-answer shape: question text, options, `correct_answer_letter`, `correct_answer_text`, expected topics, expected causal links, expected keywords, reasoning type, difficulty, source type, and examiner-safety metadata.
- Causal-chain nodes are rich enough for deterministic cause -> mechanism -> effect questions. They include trigger keywords, steps, linked misconceptions, linked topics, examples, SAT relevance, distinction notes, and governance metadata.
- Misconception nodes are directly useful for distractors: each includes the misconception, why it is wrong, corrected understanding, related topics/concepts, severity/frequency, and detection signals.
- SAT alias config can support deterministic tasting-structure questions and normalize learner-facing terms in English and Spanish.
- The canonical dictionary can normalize terms, detect aliases, enforce term/category consistency, and prevent duplicate or near-duplicate option wording.
- Official extracted chunks and markdown provide source grounding without needing to read PDF files in this phase. They also carry governance fields such as `safe_for_examiner`, `official_grading_authority`, and `requires_human_review`.
- Wine With Jimmy chunk-ready JSONL gives tutor-style explanations, SAT examples, and exam-strategy context already converted to text/jsonl. It can supplement official-source support when marked pedagogical rather than official authority.
- Existing tests already encode many constraints that a future generator should respect: deterministic loading, preservation of open questions, governance-safe tutor snapshots, retrieval behavior, and self-eval expectations.

## 3. Negative Findings / Gaps

- There is no implemented single-best-answer generator, item validator, distractor builder, or audit CLI yet.
- There is no dedicated generated-item schema or schema version for `single_best_answer`; the current bank uses `theory` and `short_answer` question types even when many items behave like multiple choice.
- RA and learning-outcome mapping exists but is not uniformly attached to every item at the level needed for reliable generation by RA/topic/difficulty.
- Structured topic, region, grape-variety, wine-law, and tasting map directories are mostly placeholders. Broad regional generation would therefore lean heavily on chunks/dictionary rather than a governed graph.
- Difficulty labels in the current bank are heavily skewed: 601 `intermediate`, 10 `distinction`, 5 `foundational`. This is too coarse for calibrated generation without a difficulty contract.
- Existing source support is not uniformly explicit at item level. Future generated items need `source_support` with chunk IDs or node IDs, not just inferred topics.
- Official extracted material is useful but risky: the generator must not copy official wording, create official-looking items, or imply WSET examiner authority.
- Distractor strategy is not yet formalized. Misconceptions are strong, but templates must distinguish plausible wrong options from ambiguous partially-correct options.
- Some chunk corpora include intros, outros, promotional content, repair reports, and exam-strategy text. Source-grounding filters must exclude non-content chunks for factual item generation.
- There is no human-calibrated generated single-best-answer pilot bank yet.

## 4. Viable Question Types

| Question type | Viability | Required source material | Risks |
|---|---|---|---|
| Cause/effect mechanism questions | HIGH | Causal-chain nodes, concept nodes, official chunks for support | Distractors may become partially correct if causal scope is too broad. |
| Vineyard factor questions | HIGH | RA1 causal chains, concepts, official chunks, Wine With Jimmy viticulture chunks | Current structured region/topic graph is narrow; keep early scope to general factors. |
| Winemaking process questions | HIGH | Causal chains for MLF, oak, lees, maceration, whole bunch, sulphites; concept nodes | Need careful option wording so "best answer" is uniquely best. |
| SAT quality reasoning questions | HIGH/MEDIUM | SAT aliases, SAT quality causal chains, tasting snapshots, official chunks | Must avoid official scoring claims and examiner authority. |
| Misconception correction questions | HIGH | Misconception nodes plus corrected understanding | Some misconceptions are nuanced; distractors must not punish valid exceptions. |
| Vocabulary/definition questions | MEDIUM/HIGH | Canonical dictionary, concept nodes, official extracted chunks | Definition wording must be paraphrased and source-grounded. |
| Regional style questions | MEDIUM | Official extracted chunks, canonical dictionary, topic hierarchy, Wine With Jimmy chunks | Structured region graph is not populated; source coverage and RA mapping must be checked per item. |
| Grape-variety characteristic questions | MEDIUM | Canonical dictionary, official chunks, Wine With Jimmy chunks | Grape-variety map is a placeholder; avoid unsupported broad claims. |
| Wine law/appellation questions | MEDIUM/LOW | Official extracted chunks, dictionary categories, topic hierarchy | High risk of exact official wording and stale legal detail. Needs stronger validators. |
| Exam-strategy questions | LOW/MEDIUM | Wine With Jimmy exam-strategy chunks, snapshots | Useful for tutoring, but not a core WSET content bank and may be opinionated. |

## 5. Non-Viable Question Types Yet

- Official-exam-like questions that imitate protected WSET phrasing or layout.
- Questions that require exact official marking intent or examiner authority.
- Highly specific regional law/appellation questions without direct, item-level source support.
- Obscure regional detail where only dictionary presence exists but no explanatory source chunk supports the correct answer.
- Ambiguous style-comparison questions where multiple options could be true depending on region, producer, vintage, or winemaking choice.
- Questions that require current legal/regulatory updates unless the source support is explicitly current and traceable.
- Open-response or essay evaluation items; those belong to a later LLM-judge/open-response phase, not Phase 4A.

## 6. Proposed Item Schema

Future generated items should use an explicit `single_best_answer` type rather than overloading `theory`.

```json
{
  "id": "",
  "question_type": "single_best_answer",
  "question": "",
  "options": {
    "A": "",
    "B": "",
    "C": "",
    "D": ""
  },
  "correct_answer": "",
  "correct_answer_letter": "",
  "rationale": "",
  "learning_outcome": "",
  "assessment_objective": "",
  "topic": "",
  "subtopic": "",
  "difficulty": "",
  "source_support": [
    {
      "source_id": "",
      "source_path": "",
      "source_type": "",
      "trust_tier": "",
      "supports": "question|correct_answer|rationale|distractor"
    }
  ],
  "causal_chain_id": "",
  "misconception_ids": [],
  "sat_relevance": [],
  "distractor_strategy": "",
  "governance": {
    "safe_for_examiner": false,
    "official_wset_question": false,
    "training_item_only": true
  }
}
```

Recommended additions before implementation:

- `schema_version`: e.g. `single_best_answer_v1`.
- `generation_method`: e.g. `deterministic_template`.
- `source_quote_policy`: e.g. `no_verbatim_official_wording`.
- `validation_status`: e.g. `draft`, `validated`, `human_review_required`.
- `language`: e.g. `es` or `en`.

## 7. Proposed Generator Architecture

Do not implement yet. Recommended module layout:

```text
tools/question_generation/
  __init__.py
  item_schema.py
  item_validator.py
  source_grounding.py
  distractor_builder.py
  causal_chain_templates.py
  misconception_templates.py
  sat_templates.py
  single_best_answer_generator.py
  generation_audit.py
```

Responsibilities:

- `item_schema.py`: dataclass/typed-dict schema and JSON serialization.
- `item_validator.py`: deterministic validation gates.
- `source_grounding.py`: select and verify lightweight source support from graph nodes, chunks, and dictionary entries.
- `distractor_builder.py`: build plausible wrong options from misconceptions, sibling terms, and controlled contrast sets.
- `causal_chain_templates.py`: generate cause/mechanism/effect item stems and rationales.
- `misconception_templates.py`: generate misconception-correction items.
- `sat_templates.py`: generate SAT observation/quality reasoning items.
- `single_best_answer_generator.py`: orchestrate templates without LLMs, embeddings, or external services.
- `generation_audit.py`: produce deterministic reports; no hidden generation side effects.

## 8. Required Validators

Generation should not be allowed until validators exist for:

- exactly 4 options: A, B, C, D
- exactly 1 correct answer
- `correct_answer_letter` matches `correct_answer`
- no duplicate options after normalization
- no near-duplicate options after canonical-term/alias normalization
- all options grammatically compatible with the stem
- distractors plausible but wrong
- no ambiguous partially-correct distractor unless the stem explicitly asks for "best"
- rationale required
- source support required for question, correct answer, and rationale
- source support must use allowed lightweight artifacts only
- no official wording leakage from extracted WSET text
- no claim that the item is an official WSET question
- `governance.safe_for_examiner` must remain false
- `governance.official_wset_question` must remain false
- `governance.training_item_only` must remain true
- RA/learning outcome required
- topic and subtopic required
- difficulty required and must use controlled labels
- if `causal_chain_id` is present, the chain must exist
- if `misconception_ids` are present, each misconception must exist
- if SAT relevance is present, SAT parameter/level must exist in `sat_observation_aliases.json`
- no generated item may depend on binary files, OCR, external websites, APIs, LLMs, embeddings, or vector DBs
- deterministic output order and stable IDs
- generated bank must be idempotent

## 9. Implementation Roadmap

### 4A.1 Governance Contract

Define a formal generation contract: training-only, deterministic-first, source-grounded, no official WSET question claim, no examiner authority, no official scoring, no runtime LLM.

### 4A.2 Item Schema

Add `single_best_answer_v1` schema with explicit governance fields, source support, rationale, and validation status.

### 4A.3 Validator

Implement validators before any generated bank exists. Tests should cover option count, uniqueness, source support, governance flags, official wording leakage checks, idempotence, and deterministic IDs.

### 4A.4 Deterministic Template Generator

Start with a tiny template set for causal-chain and concept-definition items. No distractor creativity yet; use controlled inputs only.

### 4A.5 Distractor Builder

Add misconception-driven distractors and canonical-dictionary contrast distractors with ambiguity checks.

### 4A.6 Small Generated Pilot Bank

Generate a small pilot, e.g. 20-40 items, limited to RA1 causal-chain, concept, and misconception items. Require audit report and human review before expanding.

### 4A.7 Audit/Report CLI

Add a deterministic CLI that reports generated item counts by RA, topic, difficulty, source type, causal chain, misconception, SAT relevance, and validation status.

## 10. Final Recommendation

Single-best-answer generation is viable now, but only as a controlled training-item generator behind validators and governance constraints.

Generate safely first:

- RA1 cause/effect items from causal-chain nodes.
- Concept-definition items from concept nodes plus canonical dictionary support.
- Misconception-correction items using misconception nodes.
- SAT reasoning items limited to alias-supported parameters and source-grounded rationales.

Postpone:

- broad regional/appellation detail,
- official-exam-like items,
- exact marking-intent questions,
- highly nuanced style comparisons,
- any item type that lacks direct source support.

Safest first implementation task:

Start with Phase 4A.1, the governance contract, followed immediately by Phase 4A.2 schema and Phase 4A.3 validator. The generator should not exist until the validator can reject unsafe or unsupported items.

The repo has enough lightweight material to start without Excel/PDF/Word. The strongest initial source stack is:

1. causal-chain JSON nodes,
2. misconception JSON nodes,
3. concept JSON nodes,
4. canonical dictionary JSONL,
5. SAT alias/config JSON,
6. official extracted chunks/markdown used only for support and never copied as official question wording,
7. Wine With Jimmy chunk-ready JSONL as pedagogical support where appropriate.


# Phase 4A.1 - Diagnostic Single-Best-Answer Governance Contract

Date: 2026-05-31

Status: Governance contract only. No generator, schema code, generated question
bank, runtime route, frontend, retrieval change, or knowledge-file change is
authorized by this document.

Reference: `docs/SINGLE_BEST_ANSWER_FEASIBILITY_AUDIT.md`

## 1. Purpose

The Diagnostic Single-Best-Answer Engine is not a basic quiz system.

It is a deterministic, source-grounded diagnostic training system for WSET
Level 3 study. Its purpose is to produce and analyze training-only
single-best-answer practice items that help the system identify what the
learner understands, what misconception may be active, and what remediation
should happen next.

The future engine is designed to support:

- RA, topic, and subtopic segmentation.
- Misconception diagnosis.
- Distractor interpretation.
- Response-time analysis.
- Confidence and hesitation signals.
- Remediation routing.
- Future progress tracking.

The engine must remain tutor-side, training-only, and diagnostic. It must not
become an examiner, grading, certification, or official WSET-question system.

## 2. Phase Isolation

Phase 4A.1 is docs-only.

This phase may create this governance contract and nothing else. It must not:

- implement generator code;
- implement schema code;
- implement validators;
- create generated questions;
- modify question banks;
- modify knowledge files;
- modify retrieval code;
- modify Tutor rendering code;
- modify PSL or Tutor Persona files;
- modify frontend files;
- modify snapshots.

Future phases may implement the components defined here only after their own
explicit phase instruction.

## 3. Permitted Source Materials

The future engine may use only lightweight repo-local materials:

- JSON files.
- JSONL files.
- Markdown files.
- Python configs, tests, and snapshots.
- Already extracted text or chunk artifacts.

The future engine must not use:

- Excel files.
- Word files.
- PDF files.
- OCR.
- External APIs.
- External websites.
- Runtime LLM generation.
- Embeddings.
- Vector databases.
- Cloud services.

Official extracted WSET material may be used only as source support and
validation evidence. It must not be copied into official-looking questions or
used to imitate protected wording.

## 4. Allowed Outputs

The future engine may output:

- Training questions.
- Training answer keys.
- Diagnostic feedback.
- Source-grounded rationales.
- Misconception-linked distractors.
- Remediation recommendations.
- Readiness indicators for internal training.

Readiness indicators are internal tutor diagnostics. They may indicate training
coverage, topic stability, recurring error patterns, confidence trends, or
recommended next actions. They are not official scores or pass/fail judgments.

## 5. Forbidden Outputs

The future engine must never output or imply:

- Official WSET questions.
- Official WSET marks.
- Examiner authority.
- Pass, fail, certification, or qualification claims.
- Protected wording imitation.
- Generated content without source support.
- Official grading bands.
- Official examiner verdicts.
- Claims that a generated item predicts official exam performance.
- Claims that a learner is ready or not ready in an official WSET sense.

Terms such as "diagnostic", "training", "practice", "internal readiness",
and "recommended remediation" are permitted. Terms that imply official
assessment authority are forbidden.

## 6. Governance Flags

Every generated diagnostic item, generated answer key, generation audit record,
and attempt-analysis record must preserve these governance values:

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

No future phase may permit the SBA engine to override these values. If any
input artifact contains contradictory governance fields, generation must fail
closed or mark the item as invalid before it can enter a generated bank.

## 7. Source Grounding Rules

Every future diagnostic item must include source grounding before it can be
validated.

Minimum required grounding:

- `source_support`.
- RA.
- Topic.
- Subtopic.
- Rationale.
- Correct answer justification.
- Distractor rationale or diagnostic role for every distractor.

Source support must be item-level, not merely corpus-level. It must identify
which repo-local source supports the question, the correct answer, the
rationale, and any distractor when applicable.

Allowed source support may include:

- causal-chain node IDs;
- misconception node IDs;
- concept node IDs;
- canonical dictionary term IDs or source rows;
- already extracted chunk IDs;
- already extracted markdown paths;
- SAT alias/config entries;
- existing test or snapshot references used only for format and governance
  calibration.

Source support must not be treated as official examiner authority. Retrieval
score, dictionary presence, or historical self-eval occurrence is not enough
by itself to prove factual correctness.

## 8. Diagnostic Distractor Rules

Distractors are diagnostic instruments, not filler.

Every distractor must be:

- Plausible but wrong.
- Linked to a diagnostic role when possible.
- Linked to a `misconception_id` when possible.
- Grounded in a documented contrast, misconception, sibling term, or common
  error pattern.
- Written so that the correct answer remains uniquely best.

Distractors must not be:

- Random.
- Trick-only.
- Ambiguous.
- Partially correct in a way that competes with the correct answer.
- Based solely on lexical similarity.
- Based on unsupported regional or legal detail.
- Punitive or designed to embarrass the learner.

Permitted diagnostic roles include:

- `misconception_match`.
- `near_neighbor_confusion`.
- `causal_gap`.
- `term_confusion`.
- `scope_error`.
- `sat_parameter_confusion`.
- `regional_confusion`.
- `overgeneralization`.
- `unsupported_inference`.

If no diagnostic role can be assigned, the distractor must still have a
plain-language rationale explaining why it is plausible and why it is wrong.

## 9. Attempt Analytics Boundaries

The future system may analyze:

- Selected option.
- Correctness.
- Response time.
- Changed answer.
- Hesitation.
- Confidence self-report.
- Diagnosed error type.
- Unknown terms.
- Recommended next action.

The future system must not use attempt analytics to claim official scoring
authority. Attempt analytics may support remediation routing, progress
tracking, and internal readiness indicators only.

Response time and hesitation are diagnostic signals, not moral or ability
judgments. A slow correct answer may indicate uncertainty, cognitive load, or
developing mastery. A fast incorrect answer may indicate overconfidence or a
strong misconception. These interpretations must remain probabilistic training
signals, not official conclusions.

## 10. Future Schema Requirements

This section defines minimum future schema requirements. It does not implement
schema code.

### 10.1 Diagnostic Item

Every diagnostic item must include at minimum:

- `id`.
- `schema_version`.
- `question_type`: must be `single_best_answer`.
- `language`.
- `question`.
- `options`.
- `correct_answer_letter`.
- `correct_answer`.
- `rationale`.
- `correct_answer_justification`.
- `ra`.
- `topic`.
- `subtopic`.
- `difficulty`.
- `reasoning_type`.
- `diagnostic_focus`.
- `source_support`.
- `governance`.
- `validation_status`.
- `generation_method`.

Recommended optional fields:

- `causal_chain_id`.
- `misconception_ids`.
- `sat_relevance`.
- `canonical_terms`.
- `estimated_time_seconds`.
- `remediation_targets`.

### 10.2 Option Metadata

Each option must include at minimum:

- `letter`.
- `text`.
- `is_correct`.
- `diagnostic_role`.
- `rationale`.
- `source_support`.

Distractor options should include when available:

- `misconception_id`.
- `confused_term`.
- `confused_topic`.
- `error_type`.

Exactly one option must have `is_correct = true`.

### 10.3 Source Support

Each source-support record must include at minimum:

- `source_id`.
- `source_path`.
- `source_type`.
- `trust_tier`.
- `supports`: one of `question`, `correct_answer`, `rationale`,
  `distractor`, `diagnostic_role`, or `remediation`.
- `source_governance`.

Recommended optional fields:

- `chunk_id`.
- `node_id`.
- `term_id`.
- `ra`.
- `topic`.
- `human_review_required`.

### 10.4 Governance Metadata

Every item and generated bank must include governance metadata with:

- `safe_for_examiner = false`.
- `examiner_scoring_allowed = false`.
- `official_wset_question = false`.
- `training_item_only = true`.
- `uses_llm = false`.
- `uses_api = false`.
- `uses_embeddings = false`.
- `uses_vector_db = false`.
- `cloud_services_active = false`.
- `source_quote_policy = "no_verbatim_official_wording"`.
- `official_authority_claimed = false`.

### 10.5 Attempt Analytics

Every future attempt record must include at minimum:

- `attempt_id`.
- `item_id`.
- `selected_option`.
- `is_correct`.
- `response_time_ms`.
- `changed_answer`.
- `confidence_self_report`.
- `hesitation_signal`.
- `diagnosed_error_type`.
- `unknown_terms`.
- `recommended_next_action`.
- `governance`.

Attempt records must not include official marks, pass/fail decisions, official
grade bands, or examiner verdicts.

## 11. Validation Requirements Before Generation

Generation must not be allowed until validators exist for at least the
following conditions:

- Exactly 4 options.
- Exactly 1 correct answer.
- `correct_answer_letter` matches the correct option.
- No duplicate options after normalization.
- No near-duplicate options after canonical-term and alias normalization.
- No empty required fields.
- Source support present.
- Source support present for question, correct answer, and rationale.
- Distractor rationale or diagnostic role present for every distractor.
- RA present.
- Topic present.
- Subtopic present.
- Governance fields safe.
- `safe_for_examiner` is false.
- `examiner_scoring_allowed` is false.
- `official_wset_question` is false.
- `training_item_only` is true.
- No official wording leakage.
- No examiner authority.
- No unsupported rationale.
- No unsupported correct answer.
- No ambiguous distractor.
- No distractor that is only a trick.
- No dependence on Excel, Word, PDF, OCR, external websites, APIs, runtime
  LLMs, embeddings, vector databases, or cloud services.
- Deterministic stable IDs.
- Deterministic output ordering.

Validators must fail closed. An invalid item must not enter a generated bank
as validated training content.

## 12. Remediation Routing Boundaries

The future engine may recommend remediation actions such as:

- Review a causal-chain node.
- Review a misconception correction.
- Practice a related SAT parameter.
- Revisit a canonical term.
- Try a second item on the same RA/topic.
- Route to a tutor explanation path.

Remediation recommendations must be traceable to the item, option selected,
diagnostic role, and source support. They must not bypass the existing Tutor
governance model or claim official examination authority.

## 13. Audit Requirements

Every future generated bank must include an audit report with:

- Item count.
- Count by RA.
- Count by topic and subtopic.
- Count by difficulty.
- Count by reasoning type.
- Count by source type.
- Count by causal chain.
- Count by misconception.
- Count by SAT relevance.
- Validation status counts.
- Governance flag summary.
- Unsupported or human-review-required item list.

Audit reports must be deterministic and read-only. They must not generate new
items as a side effect.

## 14. Phase Roadmap

Recommended next phases:

### 4A.2 Diagnostic SBA Item Schema

Define the explicit schema for diagnostic items, option metadata, source
support, governance metadata, and attempt analytics. No generator yet.

### 4A.3 Item Validator

Implement validators before any generated bank exists. Validators must enforce
option structure, source support, uniqueness, governance, no official wording
leakage, no examiner authority, and unsupported-rationale rejection.

### 4A.4 Deterministic Template Generator

Add a minimal deterministic generator for tightly scoped item types, starting
with causal-chain, concept-definition, and misconception-correction templates.

### 4A.5 Distractor Builder

Add diagnostic distractor construction from misconception nodes, sibling terms,
canonical dictionary contrasts, and controlled error roles.

### 4A.6 Pilot Generated Bank

Generate a small pilot bank only after validators exist. Recommended scope:
20-40 items, limited to source-supported RA/topic coverage, with audit report
and human-review status.

### 4A.7 Attempt Analyzer

Implement attempt analytics for selected option, correctness, response time,
changed answer, hesitation, confidence self-report, diagnosed error type,
unknown terms, and recommended next action.

### 4A.8 Practice-Session Backend

Connect validated diagnostic items and attempt analytics into a training-only
practice session backend. This must remain separate from official scoring and
must preserve all governance flags.

## 15. Non-Goals For Phase 4A

Phase 4A must not implement:

- Official exam simulation with WSET authority.
- Official mark allocation.
- Pass/fail certification decisions.
- Open-response judging.
- LLM-based item generation.
- Embedding-based similarity generation.
- Vector database retrieval.
- Frontend persona/avatar features.
- PSL integration.

## 16. Final Decision

Diagnostic single-best-answer generation may proceed only as a controlled,
training-only, source-grounded, deterministic system behind validators.

The next safe step is Phase 4A.2: define the Diagnostic SBA item schema. The
generator must not exist until the schema and validator can reject unsafe,
ambiguous, unsupported, or authority-leaking items.

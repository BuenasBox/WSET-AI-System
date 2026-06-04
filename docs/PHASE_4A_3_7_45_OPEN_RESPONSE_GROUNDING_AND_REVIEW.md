# Phase 4A.3.7.45 Open Response Grounding & Review Records

## Summary

Phase 4A.3.7.45 adds a derived, non-activated open-response review layer. It does not modify the raw structured question bank, Diagnostic SBA payload, cockpit, Tutor, Retrieval, Self-Eval, Golden baselines, snapshots, or frontend.

Artifacts added:

- `knowledge/question-bank/open_response/normalized/diagnostic_open_response_candidates.json`
- `knowledge/question-bank/open_response/reviews/open_response_review_records.json`

Pipeline hardening added:

- `review_status`: `approved`, `requires_revision`, `rejected`
- `activation_status`: always `inactive`
- chunk-level `corpus_support.evidence_chunks`
- approval gates for RA, corpus support, SBA residue removal, governance flags, and absence of official scoring fields

## Review Counts

| Status | Count | IDs |
|---|---:|---|
| approved | 20 | 798-817 |
| requires_revision | 0 | none |
| rejected | 1 | 18 |

All approved items remain inactive and are approved only for internal open-response structural review.

## Candidate Outcomes

| ID | Status | RA | Topic | Subtopic | Corpus support |
|---|---|---|---|---|---|
| 18 | rejected | unknown | sulfitos | SO2 | missing |
| 798 | approved | RA1 | sostenibilidad | precio | supported |
| 799 | approved | RA1 | fermentacion malolactica | vino blanco | supported |
| 800 | approved | RA1 | altitud | clima | supported |
| 801 | approved | RA1 | orientacion | pendiente | supported |
| 802 | approved | RA1 | oxidacion | vino blanco | supported |
| 803 | approved | RA1 | levaduras | fermentacion | supported |
| 804 | approved | RA1 | suelo | drenaje | supported |
| 805 | approved | RA1 | roble | roble americano | supported |
| 806 | approved | RA1 | manejo del dosel | tecnicas de vinedo | supported |
| 807 | approved | RA1 | decisiones humanas | clima extremo | supported |
| 808 | approved | RA1 | densidad de plantacion | competencia | supported |
| 809 | approved | RA1 | levaduras seleccionadas | levaduras autoctonas | supported |
| 810 | approved | RA1 | estres hidrico | calidad | supported |
| 811 | approved | RA1 | latitud | altitud | supported |
| 812 | approved | RA1 | estres hidrico | calidad | supported |
| 813 | approved | RA1 | levaduras autoctonas | riesgo enologico | supported |
| 814 | approved | RA1 | poda de invierno | rendimiento | supported |
| 815 | approved | RA1 | acero inoxidable | fermentacion | supported |
| 816 | approved | RA1 | maceracion prolongada | vino tinto | supported |
| 817 | approved | RA1 | suelo | arena | supported |

## What Was Normalized

- Source `short_answer` records are converted into `diagnostic_open_response` candidates.
- SBA residue is removed from the derived candidate layer:
  - `options`
  - `option_a` / `option_b` / `option_c` / `option_d`
  - `correct_answer`
  - `correct_answer_letter`
  - `correct_answer_text`
  - `distractors`
- Minimal metadata is present for each candidate:
  - `source_question_id`
  - `RA`
  - `topic`
  - `subtopic`
  - `difficulty`
  - `expected_concepts`
  - `optional_causal_chain`
  - `corpus_support`
  - `review_status`
  - `activation_status`
- `activation_status` remains `inactive` for every candidate.

## Grounding

Grounding is deterministic and local. It uses available official WSET chunks from:

- `knowledge/official-wset/study-guide/official-chunks/official_wset_chunks.jsonl`

The grounding layer records only chunk/document references and matched support terms. It does not quote official text, generate model answers, or claim examiner authority.

Evidence rules:

- A candidate is `supported` only when at least one eligible chunk has at least three matched support terms.
- Index and repair-report chunks are excluded from approval evidence.
- If no eligible evidence is found, `corpus_support.status` is `missing`.
- Missing corpus support blocks `approved`.

Unsupported:

- ID 18 has `corpus_support.status = missing`.

## ID 18 Decision

ID 18 is rejected from the open-response candidate set for this phase.

Reasons:

- `RA` is missing.
- Causal metadata is missing.
- Corpus chunk support is missing.
- The raw source record is structurally anomalous: it is typed `short_answer` but retains populated SBA options and `correct_answer_letter`.

The raw bank was not modified.

## Governance

The review layer remains training-only:

- `safe_for_examiner = false`
- `examiner_scoring_allowed = false`
- `official_wset_question = false`
- `training_item_only = true`
- `uses_llm = false`
- `uses_api = false`
- `uses_embeddings = false`
- `uses_vector_db = false`
- `cloud_services_active = false`

Any official scoring, marks, grade, pass/fail, or examiner-authority field is rejected by validation.

## Risks

- Grounding is term-level chunk support, not a human semantic ruling that the chunk fully supports every nuance in the stem.
- Some approved candidates are broad conceptual questions; they still need human review before any learner-facing use.
- No model answers or canonical rubrics have been created.
- No cockpit activation exists, and this phase should not be interpreted as release readiness.

## Remaining Gaps

- Human semantic review of each approved candidate.
- More precise RA/topic/subtopic taxonomy alignment.
- Better chunk ranking for broad RA1 questions where multiple official chunks match.
- Optional causal-chain mapping to existing knowledge-map causal IDs.
- Canonical formative answer expectations that remain non-scoring and non-examiner.

## Recommended Next Phase

Phase 4A.3.7.46 should add human-review resolution and semantic audit fixtures for the 20 approved internal candidates:

- verify each chunk evidence link,
- decide whether each causal expectation is acceptable,
- map optional causal chains to knowledge-map IDs where available,
- keep `activation_status = inactive`,
- continue to block ID 18 until the source anomaly is resolved or explicitly discarded.

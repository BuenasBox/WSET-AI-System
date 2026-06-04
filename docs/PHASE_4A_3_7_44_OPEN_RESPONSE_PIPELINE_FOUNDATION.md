# Phase 4A.3.7.44 Open Response Pipeline Foundation

## Implemented

- Added `knowledge/enrichment/diagnostic_open_response.schema.json` as the internal contract for training-only open response practice items.
- Added `tools/question_generation/open_response_pipeline.py`, a deterministic local module for:
  - detecting open response records,
  - normalizing structured records into `diagnostic_open_response` candidates,
  - validating governance-safe candidate shape,
  - producing formative feedback from concept coverage and causal-link presence.
- Added `tests/test_open_response_pipeline.py` with 23 tests covering schema, governance, adapter behavior, deterministic output, missing concept detection, partial concept detection, and causal-link feedback.
- Added `docs/OPEN_RESPONSE_QUESTION_INVENTORY.md` with the first inventory of open response candidates in the structured question bank.

## Contract Shape

The candidate contract uses these fields:

- `source_question_id`
- `question_type: diagnostic_open_response`
- `stem`
- `RA`
- `topic`
- `subtopic`
- `difficulty`
- `expected_concepts`
- `optional_causal_chain`
- `corpus_support`
- `feedback_rubric`
- `governance_flags`

The feedback vocabulary is deliberately formative:

- `concept_coverage`
- `feedback_level`
- `formative_feedback`
- `needs_review`
- `present_concepts`
- `missing_concepts`
- `partial_concepts`
- `revision_suggestion`

## Not Implemented

- No cockpit integration.
- No frontend exposure.
- No official evaluation.
- No examiner authority.
- No equivalence claim with WSET assessment.
- No generated model-answer bank beyond source-derived concept support.
- No retrieval or Tutor integration.
- No write-back to learner state.
- No LLM, API, embedding, vector database, or cloud path.

## Inventory Findings

- Total structured questions inspected: 616.
- Open response candidates detected: 21.
- Candidate type detected: `short_answer`.
- IDs detected: 18, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817.
- 20 of 21 candidates have RA coverage.
- 20 of 21 candidates have at least one expected causal link.
- All 21 candidates have expected keyword/concept support.

## Risks

- The source records still carry `options` objects, so open response candidates need human review before any learner-facing release.
- Candidate 18 is structurally anomalous: it is typed `short_answer`, lacks RA and causal-link metadata, and still has a populated answer-letter field from SBA-style data.
- Corpus support is currently metadata-level only. It identifies source type and support terms but does not yet cite explicit chunks.
- The formative evaluator is intentionally shallow. It can detect concept presence and weak causal wording, but it cannot judge nuance, completeness, or source-grounded reasoning depth.

## Gaps

- Canonical RA/topic/subtopic mapping should be normalized against the project taxonomy.
- Explicit corpus chunk support should be attached before activation.
- Feedback templates need domain-specific phrasing for different question families.
- Human review records for open response candidates do not exist yet.
- The evaluator should eventually distinguish concept mention from concept use in a valid explanation.

## Recommended Next Phase

Phase 4A.3.7.45 should add an enrichment-and-review layer for open response candidates:

- canonicalize RA/topic/subtopic,
- attach source chunk support,
- create human review records,
- generate safe study-guide model responses,
- keep cockpit/frontend activation off until reviewed candidates pass governance validation.

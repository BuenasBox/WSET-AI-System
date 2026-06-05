# Phase 4A.3.7.48 Open Response Remediation Batch 1

Phase: 4A.3.7.48
Scope: semantic remediation for open-response source IDs 804, 817, 807, 809
Activation: inactive; no open-response item activated or published

## Source Review Used

This remediation used `docs/OPEN_RESPONSE_SEMANTIC_REVIEW_BATCH_1.md` as the review source. No new audit pass was performed.

## Files Changed

- `knowledge/question-bank/structured/wset3_questions.json`
- `knowledge/question-bank/open_response/normalized/diagnostic_open_response_candidates.json`

`knowledge/question-bank/open_response/reviews/open_response_review_records.json` was regenerated and remains unchanged because all four remediated candidates still satisfy the structural review gate with `review_status: approved` and `activation_status: inactive`.

## Changes Applied

| source_question_id | Before | After | Final review_status |
|---|---|---|---|
| 804 | Broad soil-type/style/quality prompt. Expected concepts included several soil types and quality language. | Narrowed to soil drainage -> vine vigour -> wine style. Removed broad soil-type requirements and direct quality framing. | approved |
| 817 | Asked for sand, clay, and gravel in one item, with uneven support and overlap with 804. | Reframed as a comparative sand/clay water-availability and vigour item. Removed gravel and heat-retention requirements. | approved |
| 807 | Broad extreme-climate compensation prompt with drought, frost, hail, harvest, selection, and quality maintenance. | Narrowed to irrigation and canopy management reducing drought/heat effects on grape ripening. Removed frost, hail, harvest selection, and direct quality-maintenance expectations. | approved |
| 809 | Framed selected vs indigenous yeast around premium wine, risking unsupported premium/quality assumptions. | Reframed as a fermentation tradeoff: control, consistency, potential complexity, and risk. Removed premium and direct quality requirements. | approved |

## Grounding Changes

- Q804 grounding now emphasizes soil, drainage, water, yield/concentration, ripening, and style. Broad terms such as clay, gravel, sand, nutrients, and quality were removed from the expected concept set.
- Q817 grounding now focuses on sand, clay, drainage, water retention, vigour, concentration, ripening, and style. Gravel and heat-retention terms were removed.
- Q807 grounding now focuses on irrigation, water stress, drought/heat, canopy management, exposure, ripening, and balance. Frost, hail, harvest selection, and broad climate-extreme terms were removed.
- Q809 grounding now uses winemaking/fermentation chunks more directly by adding broad yeast/aroma terms and removing premium/quality terms.

## Causal-Chain Mapping

| source_question_id | Mapping |
|---|---|
| 804 | `CC_SOIL_DRAINAGE_VINE_VIGOUR` supports the narrowed drainage -> vigour path. The schema stores the native formative chain as `suelo -> drenaje -> vigor`. |
| 817 | `CC_SOIL_DRAINAGE_VINE_VIGOUR` supports the sandy/well-drained soil portion of the comparison. Clay/water-retention remains conceptually expected but is not mapped to a separate knowledge-map chain. |
| 807 | Unmapped. No existing causal-chain node covers irrigation/canopy management for drought or heat effects on ripening. |
| 809 | Unmapped. No existing causal-chain node covers selected versus indigenous yeast tradeoffs. |

## Feedback-Rubric Impact

The candidate schema still requires the fixed formative rubric contract:

- `concept_coverage: expected_concept_presence`
- `causal_link: formative_causal_link_presence`
- `formative_feedback: training_guidance_only`
- `needs_review: derived_from_missing_or_partial_concepts`

The remediation improves rubric behavior by narrowing stems, removing over-broad or unsupported expected concepts, and aligning the first causal link with the intended formative causal check. No score, mark, grade, pass/fail, or examiner judgement was introduced.

## Remaining Risks

- Q804 and Q817 still both cover soil and vigour. They are now differentiated, but should not both be activated without a future sequencing decision.
- Q817 maps only the drainage side cleanly to `CC_SOIL_DRAINAGE_VINE_VIGOUR`; clay/water retention remains supported as expected concepts but lacks a dedicated causal-chain node.
- Q807 remains distinction-level and still allows more than one valid explanatory route within irrigation/canopy management.
- Q809 remains partly dependent on selected/cultured versus indigenous/ambient yeast equivalence. The official corpus supports ambient/cultured yeast tradeoffs, but no dedicated knowledge-map causal chain exists yet.

## Questions Requiring Revision

None in this batch after remediation. All four remain approved for internal inactive open-response use only.

## Verification

Completed verification:

```powershell
python -m unittest discover -s tests -v
python -m tools.question_generation.export_static_demo_questions --dry-run
```

Results:

- Unit suite: 1397 tests run, OK, 9 skipped.
- SBA dry-run: `eligible_item_count: 36`.
- SBA dry-run validation: `validation_errors: 0`.

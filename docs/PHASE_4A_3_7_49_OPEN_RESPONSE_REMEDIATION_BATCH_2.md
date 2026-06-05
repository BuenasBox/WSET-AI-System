# Phase 4A.3.7.49 Open Response Remediation Batch 2

Phase: 4A.3.7.49
Scope: semantic remediation for open-response source IDs 810, 812, 798, 805
Activation: inactive; no open-response item activated or published

## Source Review Used

This remediation used the existing human review packet, existing review records, and normalized candidates. No new audit pass or review report was created.

## Files Changed

- `knowledge/question-bank/structured/wset3_questions.json`
- `knowledge/question-bank/open_response/normalized/diagnostic_open_response_candidates.json`

`knowledge/question-bank/open_response/reviews/open_response_review_records.json` remains unchanged because all four candidates still satisfy the internal structural review gate with `review_status: approved` and `activation_status: inactive`.

## Changes Applied

| source_question_id | Before | After | Final review_status |
|---|---|---|---|
| 810 | Framed moderate water stress around high-quality vineyards and price impact, with automatic quality/value implications. | Reframed as yield reduction, berry concentration, and potential cost/price influence. Removed direct quality/value and phenolics requirements. | approved |
| 812 | Simpler water-stress item still used broad quality wording. | Reframed around moderate, non-excessive water stress affecting vigour, berry size, and concentration. Removed direct quality and phenolics requirements. | approved |
| 798 | Sustainability item included broad commercial perception/value language. | Reframed around certified/organic sustainable practices, production cost, and commercial differentiation. Removed broad value requirement. | approved |
| 805 | Oak item implied generic quality perception and included cost/quality concepts. | Reframed as an American/French oak comparison focused on aromas, tannin, integration, structure, and complexity. Removed cost and direct quality requirements. | approved |

## Grounding Changes

- Q810 grounding now focuses on water stress, berry size, concentration, yield, cost, price, ripening, and sugar.
- Q812 grounding now focuses on moderate water stress, vigour, vegetative growth, berry size, concentration, ripening, yield, and sugar.
- Q798 grounding now focuses on sustainable/organic/biodynamic practices, certification, cost, labour, yield, price, market perception, and differentiation.
- Q805 grounding now focuses on oak type, vanilla/coconut/spice/toast aromas, tannin, integration, structure, complexity, and new oak.

## Causal-Chain Mapping

| source_question_id | Mapping |
|---|---|
| 810 | Unmapped. No existing knowledge-map chain covers moderate water stress -> berry concentration -> yield/cost/price. |
| 812 | Unmapped. No existing knowledge-map chain covers moderate water stress -> vigour/berry size -> concentration. |
| 798 | Unmapped. No existing knowledge-map chain covers sustainability/certification -> production cost -> price or market differentiation. |
| 805 | `CC_OAK_FLAVOUR` supports the oak type/toast/aroma profile path. `CC_OAK_TANNIN` supports the new oak/tannin/structure path. The schema stores the native formative chain as `roble americano -> vainilla -> perfil`. |

## Remaining Risks

- Q810 and Q812 still both cover moderate water stress. They are now differentiated by level and outcome: Q810 is yield/cost/price; Q812 is vigour/berry/concentration.
- Q810 price influence remains potential and should not be treated as automatic.
- Q798 still depends on commercial differentiation language; this is bounded to market perception and cost/price support from existing chunks.
- Q805 maps cleanly to oak flavour and tannin chains, but French/American differences should remain style-dependent rather than universal.

## Recommendations

- Keep all four inactive until a future private activation decision.
- If future sequencing is added, avoid presenting Q810 and Q812 in the same short diagnostic set.
- Keep Q805 as the causal-chain-positive item in this batch.
- Leave Q798, Q810, and Q812 unmapped unless new reviewed knowledge-map nodes are added.

## Verification

Completed verification:

```powershell
python -m unittest tests.test_open_response_grounding_review tests.test_open_response_pipeline -v
python -m unittest discover -s tests -v
python -m tools.question_generation.export_static_demo_questions --dry-run
```

Results:

- Targeted open-response tests: 34 tests run, OK.
- Unit suite: 1397 tests run, OK, 9 skipped.
- SBA dry-run: `eligible_item_count: 36`.
- SBA dry-run validation: `validation_errors: 0`.

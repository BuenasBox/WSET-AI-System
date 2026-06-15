# SBA Enrichment Batch 6 Report

## Result

- Previous enriched count: **260**
- New enriched count: **285**
- Delta: **+25**
- Remaining fallback: **293**
- Generated micro-drills: **218**
- Matcher v2 changed: **no**

## Items Added

`wset3_8`, `wset3_34`, `wset3_44`, `wset3_55`, `wset3_69`,
`wset3_77`, `wset3_79`, `wset3_96`, `wset3_116`, `wset3_122`,
`wset3_200`, `wset3_225`, `wset3_233`, `wset3_249`, `wset3_253`,
`wset3_274`, `wset3_284`, `wset3_292`, `wset3_302`, `wset3_328`,
`wset3_357`, `wset3_366`, `wset3_394`, `wset3_420`, `wset3_439`.

## Domains Covered

- Tokaji Aszu production and noble-rot concentration
- Indigenous yeast expression and fermentation variability
- Tannin, protein, fat and acid food-pairing mechanisms
- TCA and volatile-acidity faults
- Madeira estufagem
- Vintage Champagne and sparkling autolysis
- Traditional-method versus tank-method production
- Warm-climate ripeness and acid loss
- Priorat low yields and concentration
- Barolo structure and extended ageing
- Maritime fog and altitude-driven freshness
- Carbonic maceration
- Red-wine ageability
- Steep-slope solar exposure
- Bordeaux blending under vintage variation
- Mosel slope and orientation

## Nodes Created

- `HC_TOKAJI_ASZU_BERRY_ADDITION`
- `HC_INDIGENOUS_YEAST_COMPLEXITY_VARIABILITY`
- `HC_VINTAGE_CHAMPAGNE_EXTENDED_AGEING`
- `HC_PRIORAT_LICORELLA_LOW_YIELD_CONCENTRATION`
- `HC_BORDEAUX_BLEND_VINTAGE_VARIATION`

## Nodes Extended

No existing node was broadened. Twenty promotions reuse established nodes
whose mechanisms directly explain the keyed answer.

## Rejected Items

- `wset3_89`: rejected by the identification-stem guard (`¿Qué indica...?`);
  the guard was not weakened despite the underlying volatile-acidity mechanism.
- Pure definitions such as riddling, prise de mousse and liqueur d'expedition:
  rejected as trivia-only for this batch.
- Regional and variety identification questions: rejected.
- Soil claims implying a direct mineral taste or universal acidity effect:
  rejected as oversimplified.
- Negative-polarity items and deliberately false keyed answers: rejected.
- Items with questionable keyed mechanisms, including soil depth as a frost
  cause and night harvesting as creating acidity: rejected.

## Caveats Added

All 25 items include Spanish `Matiz:` text and provenance-level caveats.
They bound fermentation risk, regional variability, food interactions,
fault diagnosis, vintage comparisons, soil interpretation, ageing outcomes
and the limits of climate or altitude as single-cause explanations.

## Tests Run

Passed:

- Batch 6 promotion tests: **6/6**
- Strong-signal and false-positive regression tests: **9/9**
- Determinism tests: **1/1**
- Spanish and enrichment-integrity tests: **7/7**
- HC node schema/governance and manifest tests: **47/47**
- Post-regeneration Batch 6 verification: **6/6**
- Post-regeneration integrity, false-positive and Spanish tests: **13/13**

Timed out:

- No new Batch 6 focused command timed out.
- The known `tests.test_sba_enrichment_expansion` timeout from Batch 5 was not
  rerun; all focused payload and governance contracts passed.

## Artifacts

- `knowledge/question-bank/enrichment/sba_enrichment_v1.json` regenerated
  with 285 enriched items and 218 micro-drills.
- `docs/ENRICHMENT_BATCH1_SAMPLE.md` regenerated.
- Frontend and production payload mirrors were not touched.

## Files Changed

- `tools/question_generation/sba_enrichment_deriver.py`
- `tests/test_sba_enrichment_batch6.py`
- Five new `HC_*` causal node files
- `knowledge/question-bank/enrichment/sba_enrichment_v1.json`
- `docs/ENRICHMENT_BATCH1_SAMPLE.md`
- This report

## Delivery

- Implementation commit: `161f361`
- Implementation push: **success**, `origin/main`
- Report commit: recorded in the subsequent documentation commit
- Production touched: **no**
- Frontend touched: **no**
- Governance flags changed: **no**
- LLM/API/embedding/vector DB/cloud usage added: **no**

This is formative enrichment only. It does not represent official WSET
assessment or examiner scoring.

# SBA Enrichment Batch 7 Report

## Result

- Previous enriched count: **285**
- New enriched count: **310**
- Delta: **+25**
- Remaining fallback: **268**
- Generated micro-drills: **239**
- Matcher v2 changed: **no**

## Items Added

`wset3_229`, `wset3_231`, `wset3_246`, `wset3_255`, `wset3_259`,
`wset3_281`, `wset3_283`, `wset3_285`, `wset3_288`, `wset3_305`,
`wset3_320`, `wset3_359`, `wset3_368`, `wset3_369`, `wset3_375`,
`wset3_376`, `wset3_399`, `wset3_403`, `wset3_441`, `wset3_463`,
`wset3_465`, `wset3_471`, `wset3_503`, `wset3_721`, `wset3_734`.

## Domains Covered

- Warm, cool, maritime and continental climate effects
- Altitude and diurnal temperature range
- Priorat low-yield slopes and concentration
- Carbonic maceration
- Barolo maceration and red-wine ageability
- Compost and soil organic matter
- Stainless-steel inert vessels
- Yeast strain and fermentation aromas
- High-acid wine and salty-food balance
- Bottle storage and oxidation control

## Nodes Created

- `HC_COMPOST_SOIL_ORGANIC_MATTER`
- `HC_STAINLESS_INERT_VESSEL`
- `HC_YEAST_STRAIN_AROMA_PROFILE`

## Nodes Extended

No existing node was broadened. Existing climate, altitude, food-pairing,
carbonic-maceration, storage and ageability nodes were reused with
item-specific Spanish caveats.

## Rejected Items

- Pure regional, variety and terminology identification: rejected.
- Negative-polarity and deliberately false keyed answers: rejected.
- `wset3_515`: open truncated-conical vessels do not by themselves establish
  malolactic fermentation as the single best answer.
- `wset3_520`: lees ageing does not safely support the keyed protein-stability
  claim without conflating it with bentonite fining.
- `wset3_429`: deep soil was not accepted as a general direct cause of spring
  frost risk.
- `wset3_454`: flowering rain was not enriched as dilution; poor fruit set is
  the stronger direct mechanism.
- `wset3_468`: night harvesting preserves freshness rather than creating or
  increasing acidity.
- Soil-to-minerality and universal limestone-to-acidity claims: rejected.

## Caveats Added

Every promoted item includes Spanish `Matiz:` text and provenance-level
`learner_caveat`. Caveats constrain regional comparisons, climate
generalizations, soil interpretation, fermentation causality, ageing
outcomes, food pairing and storage claims.

## Tests Run

Passed:

- Batch 7 promotion tests: **6/6**
- Strong-signal and false-positive regression tests: **9/9**
- Determinism tests: **1/1**
- Spanish and enrichment-integrity tests: **7/7**
- HC node schema/governance and manifest tests: **47/47**
- Post-regeneration Batch 7 verification: **6/6**
- Post-regeneration integrity, false-positive and Spanish tests: **13/13**

Timed out:

- No Batch 7 focused command timed out.
- The known `tests.test_sba_enrichment_expansion` timeout from Batch 5 was not
  rerun; focused payload, determinism and governance contracts passed.

## Artifacts

- `knowledge/question-bank/enrichment/sba_enrichment_v1.json` regenerated
  with 310 enriched items and 239 micro-drills.
- `docs/ENRICHMENT_BATCH1_SAMPLE.md` regenerated.
- Frontend and production payload mirrors were not touched.

## Files Changed

- `tools/question_generation/sba_enrichment_deriver.py`
- `tests/test_sba_enrichment_batch7.py`
- Three new `HC_*` causal node files
- `knowledge/question-bank/enrichment/sba_enrichment_v1.json`
- `docs/ENRICHMENT_BATCH1_SAMPLE.md`
- This report

## Delivery

- Implementation commit: `dbbd215`
- Implementation push: **success**, `origin/main`
- Report commit: recorded in the subsequent documentation commit
- Production touched: **no**
- Frontend touched: **no**
- Governance flags changed: **no**
- LLM/API/embedding/vector DB/cloud usage added: **no**

This is formative enrichment only. It does not represent official WSET
assessment or examiner scoring.

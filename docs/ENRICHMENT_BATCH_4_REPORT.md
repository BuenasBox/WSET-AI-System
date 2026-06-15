# SBA Enrichment Batch 4 Report

## Result

- Previous enriched count: **210**
- New enriched count: **235**
- Delta: **+25**
- Remaining fallback: **343**
- Batch policy: deterministic manual-review promotion layered after matcher v2
- Matcher v2 changed: **no**

## Items Added

`wset3_11`, `wset3_65`, `wset3_104`, `wset3_113`, `wset3_208`,
`wset3_210`, `wset3_219`, `wset3_230`, `wset3_251`, `wset3_266`,
`wset3_282`, `wset3_321`, `wset3_339`, `wset3_341`, `wset3_345`,
`wset3_401`, `wset3_421`, `wset3_460`, `wset3_466`, `wset3_499`,
`wset3_514`, `wset3_669`, `wset3_673`, `wset3_740`, `wset3_850`.

## Domains Covered

- Cool, continental, maritime and altitude climate mechanisms
- Oxidation and oxidative maturation
- Madeira heat maturation
- Sparkling base-wine acidity
- Biological ageing under flor
- Moscato d'Asti fermentation arrest
- Appassimento grape drying
- Oak maturation, lignin/vanillin and oak-origin style
- Selected-yeast fermentation control
- SO2 microbial inhibition
- Canopy management
- Natural cork and gradual bottle evolution

## Nodes Created

- `HC_MADEIRA_HEAT_OXIDATIVE_AGEING`
- `HC_MOSCATO_ASTI_FERMENTATION_ARREST`
- `HC_APPASSIMENTO_GRAPE_DRYING_CONCENTRATION`
- `HC_OAK_LIGNIN_VANILLIN`
- `HC_FRENCH_AMERICAN_OAK_STYLE`
- `HC_NATURAL_CORK_SLOW_OXYGEN`

## Nodes Extended

No existing node was broadened specifically for the 25 manual promotions.

The commit also carries forward the already validated 205-to-210 baseline
extensions in `HC_YIELD_CONCENTRATION`, `HC_DRIP_IRRIGATION_PRECISION`,
`HC_FLOWERING_RAIN_FRUIT_SET`, `HC_RED_FERMENTATION_EXTRACTION`, and
`HC_CANOPY_VIGOUR_EXPOSURE`.

## Rejected Items

- Regional or variety identification items: rejected as trivia-only.
- Negative-polarity items `wset3_771` through related INCORRECTA items:
  rejected because the keyed answer is false by design.
- `wset3_454`: rejected because "dilution" does not safely explain rain
  during flowering; poor fruit set is the stronger causal mechanism.
- `wset3_458`: rejected because the keyed early-harvest answer does not
  safely explain increased polyphenol concentration.
- `wset3_468`: rejected because night harvesting preserves existing acidity
  and freshness rather than creating or increasing acidity.
- `wset3_485`: rejected because limestone does not universally cause high
  acidity without site, climate and water context.
- `wset3_515`: rejected because open truncated-conical vessels do not by
  themselves justify malolactic fermentation as the single best answer.
- `wset3_520`: rejected because lees contact and protein stability require
  more qualification than the item provides.
- `wset3_849`: rejected because the keyed claim of perfect hermeticity and
  zero bottle variation is absolute and unsafe.

## Caveats Added

Every promoted item has a Spanish learner-facing `Matiz:` and provenance-level
`learner_caveat`. Caveats bound climate generalizations, regional variation,
oak tendencies, closure variability, SO2 limitations, fermentation
dependencies and the difference between preservation and creation of acidity.

## Tests Run

Passed:

- `python -m unittest tests.test_sba_enrichment_batch4 -v` — 8/8
- `python -m unittest tests.test_sba_enrichment_deriver.StrongSignalContractTests tests.test_sba_enrichment_deriver.FalsePositiveRegressionTests -v` — 9/9
- `python -m unittest tests.test_sba_enrichment_deriver.DeterminismTests -v` — 1/1
- `python -m unittest tests.test_sba_enrichment_deriver.SpanishOutputTests tests.test_sba_enrichment_deriver.EnrichmentIntegrityTests -v` — 7/7
- `python -m unittest tests.test_heuristic_causal_nodes tests.test_knowledge_map_manifest_contract -v` — 47/47
- Post-regeneration batch verification — 8/8
- Post-regeneration integrity and false-positive verification — 11/11

Timed out:

- `python -m unittest discover -s tests -v` — exceeded 600 seconds; no
  focused failure was observed before timeout. Per batch policy, this did not
  block the batch after all focused contracts passed.

## Artifacts

- `knowledge/question-bank/enrichment/sba_enrichment_v1.json` regenerated
  with 235 enriched items and 179 micro-drills.
- `docs/ENRICHMENT_BATCH1_SAMPLE.md` regenerated.
- Frontend or production payload mirrors were not regenerated because the
  batch explicitly prohibits touching the frontend repository.

## Files Changed

- `tools/question_generation/sba_enrichment_deriver.py`
- `tests/test_sba_enrichment_batch4.py`
- `tests/test_sba_enrichment_deriver.py`
- `tests/test_sba_enrichment_expansion.py`
- Six new `HC_*` causal node files
- Five carried-forward baseline `HC_*` node extensions
- `knowledge/question-bank/enrichment/sba_enrichment_v1.json`
- `docs/ENRICHMENT_BATCH1_SAMPLE.md`
- This report

## Delivery

- Implementation commit: `7159b79`
- Implementation push: **success**, `origin/main`
- Production touched: **no**
- Frontend touched: **no**
- Governance flags changed: **no**
- LLM/API/embedding/vector DB/cloud usage added: **no**

This is formative enrichment only. It does not represent official WSET
assessment or examiner scoring.

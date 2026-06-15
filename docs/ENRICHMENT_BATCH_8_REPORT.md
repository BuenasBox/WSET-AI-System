# SBA Enrichment Batch 8 Report

## Result

- Previous enriched count: **310**
- New enriched count: **360**
- Delta: **+50**
- Remaining fallback: **218**
- Generated micro-drills: **276**
- Matcher v2 changed: **no**

## Items Added

`wset3_63`, `wset3_97`, `wset3_105`, `wset3_121`, `wset3_211`,
`wset3_213`, `wset3_235`, `wset3_237`, `wset3_250`, `wset3_256`,
`wset3_260`, `wset3_267`, `wset3_268`, `wset3_272`, `wset3_276`,
`wset3_280`, `wset3_290`, `wset3_293`, `wset3_295`, `wset3_299`,
`wset3_307`, `wset3_313`, `wset3_314`, `wset3_324`, `wset3_327`,
`wset3_332`, `wset3_337`, `wset3_343`, `wset3_348`, `wset3_374`,
`wset3_383`, `wset3_395`, `wset3_412`, `wset3_419`, `wset3_423`,
`wset3_425`, `wset3_456`, `wset3_508`, `wset3_512`, `wset3_517`,
`wset3_657`, `wset3_712`, `wset3_728`, `wset3_729`, `wset3_730`,
`wset3_735`, `wset3_822`, `wset3_827`, `wset3_833`, `wset3_851`.

## Domains Covered

- Traditional-method sparkling production and pressure
- Fortification timing, oxidative Sherry and Pedro Ximenez sweetness
- Service temperature, glassware and professional protocol
- Food pairing with cheese and umami
- Climate, water stress, soil drainage and variety cycle
- Regional style mechanisms with explicit caveats
- Terraces, appellation hierarchy and vineyard specificity
- Harvest sugar measurement
- SO2 sensitivity and microbial inhibition
- Appellation rules, export positioning and price formation
- Sulfite allergen labelling and bag-in-box packaging

## Nodes Created

- `HC_ALSACE_VARIETAL_LABEL_DRY_CLIMATE`
- `HC_APPELLATION_RULES_ORIGIN_VALUE`
- `HC_BAG_IN_BOX_COLLAPSIBLE_OXYGEN`
- `HC_BRAND_CONSISTENCY_EXPORT_SUCCESS`
- `HC_BURGUNDY_SITE_HIERARCHY_CONCENTRATION`
- `HC_COONAWARRA_TERRA_ROSSA_MODERATION`
- `HC_DOURO_TERRACES_SLOPE_ACCESS`
- `HC_HARVEST_BRIX_RIPENESS_DECISION`
- `HC_NEGOCIANT_BLEND_MATURATION_ROLE`
- `HC_SERVICE_TEMPERATURE_GLASS_PROTOCOL`
- `HC_SULFITE_ALLERGEN_LABEL_THRESHOLD`
- `HC_TULIP_GLASS_AROMA_CONCENTRATION`

## Nodes Extended

No existing HC node was broadened. Existing mechanisms were reused only where
they directly explained the keyed answer, with item-specific Spanish caveats.

## Rejected Items

- Negative-polarity and deliberately false keyed answers.
- Pure region, variety, label and terminology identification.
- Health-advice items, which are outside the enrichment mechanism scope.
- `wset3_90`: replaced because the food interaction required a weaker
  generalization than the accepted Palo Cortado mechanism.
- `wset3_515`, `wset3_520`, `wset3_429`, `wset3_454`, `wset3_458` and
  `wset3_468`: retained as fallback because their keyed causal claims remain
  weak, incorrect or oversimplified.
- Soil-to-minerality claims without a bounded physical mechanism.

## Caveats Added

Every item includes Spanish `Matiz:` text and provenance-level caveats.
Caveats constrain regional generalizations, soil interpretation, service
choices, legal categories, market value, ageing outcomes and production-style
variation.

## Tests Run

Passed:

- Batch 8 promotion tests: **6/6**
- Strong-signal and false-positive regression tests: **9/9**
- Determinism tests: **1/1**
- Spanish and enrichment-integrity tests: **7/7**
- HC node schema/governance and manifest tests: **47/47**
- Post-regeneration Batch 8 verification: **6/6**
- Post-regeneration integrity, false-positive and Spanish tests: **13/13**

Timed out:

- No Batch 8 focused command timed out.
- The known legacy expansion-suite timeout was not rerun; all required focused
  payload, governance and regression contracts passed.

## Artifacts

- Sidecar regenerated with 360 enriched items and 276 micro-drills.
- Sample enrichment report regenerated.
- Frontend payload files were not staged, committed or pushed.

## Delivery

- Implementation commit: `0de432e`
- Implementation push: **success**, `origin/main`
- Production touched: **no**
- Frontend touched by this batch: **no**
- Governance flags changed: **no**
- LLM/API/embedding/vector DB/cloud usage added: **no**

This is formative enrichment only. It does not represent official WSET
assessment or examiner scoring.

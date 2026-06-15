# SBA Enrichment Final Closeout Report

## Final Result

- Starting count: **310 enriched SBA**
- Final count: **360 enriched SBA**
- Total delta: **+50**
- Total SBA bank: **578**
- Remaining fallback: **218**
- Final enrichment percentage: **62.28%**
- Final micro-drill count: **276**
- Final phase: `P.8-batch8-manual-review`
- Matcher v2 changed: **no**

## Safe Coverage Limit

The requested 450 target cannot be reached under the locked precision-first
contracts. After Batch 8, the 218 fallback items classify as:

- **112 identification stems**
- **24 negative-polarity stems**
- **4 definitional stems**
- **78 other reviewable stems**

The 140 blocked items cannot be promoted without weakening existing guards.
Manual review of the remaining 78 found that fewer than 50 retain
medium-high causal confidence. Most are trivia, legal or label recall,
regional identification written in an alternate form, weak style
generalizations, or questions with questionable keyed mechanisms.

The final count therefore stops at 360 under the explicit stopping rule:
remaining items are mostly trivia/identification or cannot support a complete
safe batch without quality dropping.

## Nodes Created

Twelve nodes were created during the final closeout:

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

Including Batches 5-7, the expansion from 210 to 360 created **29 new HC
nodes**.

## Nodes Extended

No existing node was broadened during final closeout. Existing nodes were
reused only when their established mechanism directly explained the keyed
answer. Matcher thresholds, trigger handling, stoplists and guards remained
unchanged.

## Domains Covered

- Sparkling second fermentation, pressure and lees development
- Fortification timing, oxidative ageing and dried-grape sweetness
- Wine service temperature, glassware and protocol
- Food pairing with cheese, protein, fat and umami
- Climate moderation, altitude, solar exposure and water stress
- Soil drainage and bounded site-specific soil mechanisms
- Harvest Brix and variety growth-cycle timing
- Terraces and steep-slope cultivation
- Regional style mechanisms with explicit caveats
- Appellation rules, hierarchy, origin protection and typicity
- Negociant blending and maturation
- Brand consistency, distribution, reputation and price
- Sulfite labelling and bag-in-box packaging

## Rejected Domains And Reasons

- Pure regional, grape, category and terminology identification: trivia-only.
- Negative-polarity questions: keyed answer is false by design.
- Definitions and label hierarchy recall: no causal explanation of the answer.
- Health-advice questions: outside the enrichment mechanism scope.
- Limestone or minerality claims: rejected when they implied direct flavour
  transfer or universal acidity.
- Regional profiles: rejected where the keyed answer was too broad,
  inconsistent or unsupported by one bounded mechanism.
- Viticulture questions with weak keys: deep soil as frost cause, early harvest
  as increased polyphenol concentration, night harvest as increased acidity,
  and flowering rain as dilution.
- Winemaking questions with weak keys: open truncated-conical vessels as a
  cause of malolactic fermentation and lees ageing as protein stabilization.
- Commercial or regulatory recall: rejected when the answer merely named an
  organization, channel, legal equivalent or classification.
- Absolute closure claims: rejected where screwcap was described as perfectly
  hermetic and eliminating all bottle variation.

## Tests Run

Passed:

- Batch 8 exact promotion contract: **6/6**
- Strong-signal and false-positive regression tests: **9/9**
- Determinism tests: **1/1**
- Spanish and enrichment-integrity tests: **7/7**
- HC node schema/governance and knowledge-map manifest tests: **47/47**
- Post-regeneration Batch 8 verification: **6/6**
- Post-regeneration integrity, false-positive and Spanish tests: **13/13**
- Structured enrichment contract and behavior tests: **28/28**
- Final deterministic file comparison: `derive() == sidecar`
- Final payload audit: 360 records, 276 drills, unique item IDs

Timed out:

- No final-closeout focused command timed out.
- The legacy `tests.test_sba_enrichment_expansion` suite timed out during Batch
  5 and was documented there. It was not rerun because focused payload,
  governance, determinism and regression contracts passed after every later
  batch.

## Files Changed

- `tools/question_generation/sba_enrichment_deriver.py`
- `tests/test_sba_enrichment_batch8.py`
- Twelve new `knowledge/knowledge-map/causal-chains/HC_*.json` files
- `knowledge/question-bank/enrichment/sba_enrichment_v1.json`
- `docs/ENRICHMENT_BATCH1_SAMPLE.md`
- `docs/ENRICHMENT_BATCH_8_REPORT.md`
- `docs/superpowers/plans/2026-06-15-sba-enrichment-final-closeout.md`
- This final closeout report

## Commits And Push

- Batch 8 implementation: `0de432e`
- Batch 8 report: `33cf748`
- Final closeout report: recorded in the final documentation commit
- Push status: **success**, `origin/main`
- Production touched: **no**
- Frontend touched by enrichment work: **no**
- Governance flags changed: **no**
- LLM/API/embedding/vector DB/cloud usage added: **no**

## Frontend Sync Recommendation

Perform a separate, explicitly scoped frontend synchronization using
`knowledge/question-bank/enrichment/sba_enrichment_v1.json` as the source of
truth after the existing local frontend modifications are reviewed. Do not
merge or overwrite those local frontend changes as part of enrichment
closeout. The sync should verify the 360 enriched IDs, 276 micro-drills,
Spanish learner-facing text and unchanged governance before any production
deployment.

This is formative enrichment only. It does not represent official WSET
assessment or examiner scoring.

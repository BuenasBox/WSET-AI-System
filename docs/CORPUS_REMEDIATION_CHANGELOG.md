# Corpus Remediation Changelog

Phase 4A.3.7.33

## Summary

| Item set | Count |
|---|---:|
| Items processed | 524 |
| Original DISTRACTOR_CONFLICT inventory | 181 |
| Original conflicts remaining | 12 |
| New review signals | 2 |
| Total after-state DISTRACTOR_CONFLICT | 14 |
| AUTO_FIXED original conflicts | 169 |
| HUMAN_REVIEW total | 10 |
| DISCARD recommendations total | 4 |
| PARTIAL → STRONG audit promotions | 6 |

## Field-Level Changes Recorded

No question bank fields were modified. The changed fields below refer to the remediated audit dataset.

| Item | Field modified | Before | After | Evidence / reason |
|---|---|---|---|---|
| Q1 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-1_43_sherry.md` |
| Q1 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q2 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q3 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-2_44_port.md` |
| Q3 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q5 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-1_43_sherry.md`; conflict evidence `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-1_43_sherry.md` |
| Q5 | remediation_status | pending | HUMAN_REVIEW | A: Crianza biológica bajo flor; `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-1_43_sherry.md`; conflict evidence `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-1_43_sherry.md` |
| Q9 | grounding | PARTIAL | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q9 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q10 | grounding | PARTIAL | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q10 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q11 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md` |
| Q11 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q12 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md` |
| Q12 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q13 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md` |
| Q13 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q14 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-3_6_vineyard_management.md` |
| Q14 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q15 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q16 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md` |
| Q16 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q17 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-4_7_common_elements_in_winemaking_and_maturation.md`; conflict evidence `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-4_7_common_elements_in_winemaking_and_maturation.md` |
| Q17 | remediation_status | pending | HUMAN_REVIEW | C: Estimular la fermentación maloláctica; `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-4_7_common_elements_in_winemaking_and_maturation.md`; conflict evidence `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-4_7_common_elements_in_winemaking_and_maturation.md` |
| Q19 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q20 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q21 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q22 | grounding | WEAK | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q23 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q25 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q29 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_7_section_4_sparkling_wines_of_the_world/7-1_41_sparkling_wine_production.md` |
| Q29 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q30 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_7_section_4_sparkling_wines_of_the_world/7-1_41_sparkling_wine_production.md` |
| Q32 | grounding | WEAK | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q34 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q36 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q38 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q40 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q41 | grounding | PARTIAL | WEAK | `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-2_44_port.md` |
| Q41 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q43 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_4_section_1_wine_and_the_consumer/4-1_1_the_systematic_approach_to_tasting_wine.md` |
| Q45 | grounding | PARTIAL | WEAK | `knowledge/official-wset/study-guide/wset_markdown/seccion_4_section_1_wine_and_the_consumer/4-1_1_the_systematic_approach_to_tasting_wine.md` |
| Q52 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q59 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q62 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_4_section_1_wine_and_the_consumer/4-1_1_the_systematic_approach_to_tasting_wine.md` |
| Q79 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q83 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q91 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q93 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_4_section_1_wine_and_the_consumer/4-1_1_the_systematic_approach_to_tasting_wine.md` |
| Q94 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q95 | grounding | PARTIAL | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q95 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q97 | grounding | PARTIAL | WEAK | `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-1_43_sherry.md` |
| Q97 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q99 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q100 | grounding | PARTIAL | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q100 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q101 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-8_11_wine_and_the_law.md` |
| Q105 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q107 | grounding | PARTIAL | STRONG | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-4_7_common_elements_in_winemaking_and_maturation.md` |
| Q111 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q113 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q114 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q115 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q116 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q121 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q124 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_7_section_4_sparkling_wines_of_the_world/7-1_41_sparkling_wine_production.md` |
| Q126 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q127 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_4_section_1_wine_and_the_consumer/4-1_1_the_systematic_approach_to_tasting_wine.md` |
| Q128 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_4_section_1_wine_and_the_consumer/4-1_1_the_systematic_approach_to_tasting_wine.md` |
| Q201 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_7_section_4_sparkling_wines_of_the_world/7-1_41_sparkling_wine_production.md` |
| Q203 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_4_section_1_wine_and_the_consumer/4-1_1_the_systematic_approach_to_tasting_wine.md` |
| Q203 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q204 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q206 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q207 | grounding | PARTIAL | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q207 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q210 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q211 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q214 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_7_section_4_sparkling_wines_of_the_world/7-1_41_sparkling_wine_production.md` |
| Q216 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q217 | grounding | PARTIAL | WEAK | `knowledge/official-wset/study-guide/wset_markdown/seccion_7_section_4_sparkling_wines_of_the_world/7-1_41_sparkling_wine_production.md` |
| Q218 | grounding | PARTIAL | NOT_FOUND | `knowledge/official-wset/study-guide/wset_markdown/seccion_7_section_4_sparkling_wines_of_the_world/7-2_42_sparkling_wines_of_the_world.md` |
| Q218 | distractor_conflict | False | True | Wrong option has official-corpus support in a passage that also matches item context. |
| Q218 | remediation_status | pending | DISCARD | B: Champagne usa el método Charmat; `knowledge/official-wset/study-guide/wset_markdown/seccion_7_section_4_sparkling_wines_of_the_world/7-2_42_sparkling_wines_of_the_world.md` |
| Q223 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q226 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q227 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q229 | grounding | NOT_FOUND | STRONG | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md` |
| Q230 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q232 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q236 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q237 | grounding | PARTIAL | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q237 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q238 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q239 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q240 | grounding | PARTIAL | STRONG | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-4_7_common_elements_in_winemaking_and_maturation.md` |
| Q241 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q243 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q244 | grounding | WEAK | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q244 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q245 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q247 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md` |
| Q247 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q248 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q249 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md` |
| Q250 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md` |
| Q252 | remediation_status | pending | HUMAN_REVIEW | B: Syrah; `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md`; conflict evidence `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md` |
| Q254 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-22_33_california.md` |
| Q254 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q257 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q258 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q263 | remediation_status | pending | HUMAN_REVIEW | C: Syrah; `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-19_30_spain.md`; conflict evidence `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md` |
| Q264 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q268 | grounding | PARTIAL | STRONG | `knowledge/official-wset/study-guide/wset_markdown/seccion_4_section_1_wine_and_the_consumer/4-1_1_the_systematic_approach_to_tasting_wine.md` |
| Q268 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q270 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q272 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-3_14_the_dordogne_and_south_west_france.md` |
| Q272 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q273 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q277 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q278 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q279 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q281 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q286 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q287 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q288 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q289 | grounding | WEAK | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q291 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q293 | grounding | WEAK | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q294 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q296 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q298 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q301 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q303 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-22_33_california.md` |
| Q303 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q305 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q306 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q308 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q309 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q312 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q317 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q325 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q328 | distractor_conflict | False | True | Wrong option has official-corpus support in a passage that also matches item context. |
| Q328 | remediation_status | pending | HUMAN_REVIEW | C: Fermentación maloláctica completa; `knowledge/official-wset/study-guide/wset_markdown/seccion_4_section_1_wine_and_the_consumer/4-1_1_the_systematic_approach_to_tasting_wine.md`; conflict evidence `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-4_7_common_elements_in_winemaking_and_maturation.md` |
| Q330 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q333 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_4_section_1_wine_and_the_consumer/4-1_1_the_systematic_approach_to_tasting_wine.md` |
| Q337 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q338 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q343 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q344 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q345 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q348 | grounding | PARTIAL | WEAK | `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-2_13_bordeaux.md` |
| Q350 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q352 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q353 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q354 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q356 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q360 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q361 | remediation_status | pending | HUMAN_REVIEW | B: Santa Barbara; `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-22_33_california.md`; conflict evidence `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-22_33_california.md` |
| Q362 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q363 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q364 | grounding | WEAK | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q367 | grounding | PARTIAL | STRONG | `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-2_13_bordeaux.md` |
| Q368 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q370 | remediation_status | pending | DISCARD | A: Barossa Valley; `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-28_39_australia.md` |
| Q371 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q373 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q374 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q376 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md` |
| Q376 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q378 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q379 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q381 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q382 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q383 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q384 | grounding | WEAK | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q386 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_4_section_1_wine_and_the_consumer/4-1_1_the_systematic_approach_to_tasting_wine.md` |
| Q387 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q388 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md` |
| Q394 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q395 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q396 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md` |
| Q397 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q398 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q400 | grounding | STRONG | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q400 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q402 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q403 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md` |
| Q403 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q404 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q405 | remediation_status | pending | HUMAN_REVIEW | D: Gran Reserva; `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-19_30_spain.md`; conflict evidence `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-19_30_spain.md` |
| Q406 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q407 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q409 | remediation_status | pending | HUMAN_REVIEW | A: Barossa Valley; `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md`; conflict evidence `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-28_39_australia.md` |
| Q410 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q411 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q414 | remediation_status | pending | HUMAN_REVIEW | D: Walker Bay; `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md`; conflict evidence `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-27_38_south_africa.md` |
| Q416 | remediation_status | pending | HUMAN_REVIEW | A: Syrah; `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md`; conflict evidence `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md` |
| Q417 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q418 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q420 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q421 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q422 | grounding | PARTIAL | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q422 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q424 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q426 | grounding | STRONG | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q428 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q429 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q430 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_4_section_1_wine_and_the_consumer/4-1_1_the_systematic_approach_to_tasting_wine.md` |
| Q430 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q432 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q433 | grounding | PARTIAL | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q433 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q435 | grounding | PARTIAL | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q435 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q437 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q438 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q439 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q440 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q441 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q442 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q451 | grounding | STRONG | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q452 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q455 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q459 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q460 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q461 | grounding | PARTIAL | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q461 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q464 | grounding | PARTIAL | STRONG | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md` |
| Q464 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q465 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q466 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q469 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q471 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q474 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q475 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q478 | grounding | PARTIAL | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q478 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q479 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q483 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q484 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q485 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_4_section_1_wine_and_the_consumer/4-1_1_the_systematic_approach_to_tasting_wine.md` |
| Q485 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q486 | grounding | PARTIAL | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q486 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q489 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q490 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q491 | grounding | PARTIAL | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q491 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q492 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q493 | grounding | PARTIAL | STRONG | `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-2_13_bordeaux.md` |
| Q494 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q495 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md` |
| Q495 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q497 | grounding | PARTIAL | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q497 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q498 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q499 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q503 | grounding | PARTIAL | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q503 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q506 | grounding | PARTIAL | WEAK | `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-19_30_spain.md` |
| Q508 | grounding | WEAK | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q509 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q510 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q512 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q513 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q515 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q516 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q518 | grounding | STRONG | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q518 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q519 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q520 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q659 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q660 | grounding | PARTIAL | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q660 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q661 | remediation_status | pending | DISCARD | A: Chardonnay; `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md`; conflict evidence `knowledge/official-wset/study-guide/wset_markdown/seccion_7_section_4_sparkling_wines_of_the_world/7-2_42_sparkling_wines_of_the_world.md` |
| Q662 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q663 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q664 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q665 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q666 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q667 | grounding | PARTIAL | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q667 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q689 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q690 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q691 | grounding | PARTIAL | WEAK | `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-27_38_south_africa.md` |
| Q691 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q692 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q693 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q694 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q695 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q696 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q697 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q698 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q699 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q700 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q728 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q730 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q735 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q736 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q738 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_4_section_1_wine_and_the_consumer/4-1_1_the_systematic_approach_to_tasting_wine.md` |
| Q823 | grounding | PARTIAL | NOT_FOUND | `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-20_31_portugal.md` |
| Q823 | remediation_status | pending | DISCARD | D: IGP; `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-20_31_portugal.md` |
| Q825 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q828 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |
| Q834 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q835 | grounding | PARTIAL | NOT_FOUND | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q835 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q836 | grounding | STRONG | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/repair_report_wine_and_the_law.md` |
| Q836 | distractor_conflict | True | False | Original conflict removed by official-corpus-only, context-bound distractor validation; no question text changed. |
| Q837 | grounding | NOT_FOUND | PARTIAL | `knowledge/official-wset/study-guide/wset_markdown/seccion_4_section_1_wine_and_the_consumer/4-1_1_the_systematic_approach_to_tasting_wine.md` |
| Q842 | grounding | PARTIAL | NOT_FOUND | No actionable conflict after official-corpus-only pass. |

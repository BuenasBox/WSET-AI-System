# Corpus-Grounded Remediation Report

Phase 4A.3.7.33 — Corpus-grounded remediation program

## Scope

This pass remediates the evidence-audit layer, not the question bank. It restricts documentary evidence to the official converted WSET Markdown corpus under `knowledge/official-wset/study-guide/wset_markdown/`, excludes non-substantive index/front-matter files, and applies context-bound distractor validation.

No governance, Tutor, retrieval, self-eval, frontend, contracts, activation, publication, answer keys, stems, options, or bank records were modified.

## Before / After Metrics

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| STRONG | 57 | 41 | -16 |
| PARTIAL | 256 | 219 | -37 |
| WEAK | 10 | 9 | -1 |
| NOT_FOUND | 201 | 255 | +54 |
| DISTRACTOR_CONFLICT, original inventory only | 181 | 12 | -169 |
| DISTRACTOR_CONFLICT, total after-state | 181 | 14 | -167 |

The STRONG count decreased under the remediated audit because the prior pass allowed local self-eval artifacts and other non-official Markdown. This pass intentionally favors corpus purity over optimistic promotion.

## Original 181 Conflict Inventory Classification

| Classification | Count |
|---|---:|
| menor | 170 |
| moderado | 8 |
| severo | 3 |

## Remediation Outcomes For Original 181

| Outcome | Count | Meaning |
|---|---:|---|
| AUTO_FIXED | 169 | Conflict removed by official-corpus-only, context-bound validation; no bank edit. |
| HUMAN_REVIEW | 9 | Official evidence still creates plausible ambiguity; editorial decision required. |
| DISCARD | 3 | High-risk item from the original inventory: weak/no correct grounding with a supported wrong option. |

## New Review Signals

These were not in the original 181 conflict set but surfaced under the official-corpus/context-bound pass. They are not counted as AUTO_FIXED debt reduction.

| Item | Status | Problematic distractor | Evidence file |
|---|---|---|---|
| Q218 | DISCARD | B: Champagne usa el método Charmat | `knowledge/official-wset/study-guide/wset_markdown/seccion_7_section_4_sparkling_wines_of_the_world/7-2_42_sparkling_wines_of_the_world.md` |
| Q328 | HUMAN_REVIEW | C: Fermentación maloláctica completa | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-4_7_common_elements_in_winemaking_and_maturation.md` |

## Questions Promoted In Audit Dataset

Promotion here means the remediated evidence dataset changed from PARTIAL to STRONG using official-corpus passages. It does not activate the item and does not bypass human review.

| Item | RA | Evidence file | Matched terms |
|---|---|---|---|
| Q107 | RA3 | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-4_7_common_elements_in_winemaking_and_maturation.md` | fermentation, fermenting, malolactic fermentation |
| Q240 | RA3 | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-4_7_common_elements_in_winemaking_and_maturation.md` | fermentation, fermenting, malolactic fermentation |
| Q268 | RA2 | `knowledge/official-wset/study-guide/wset_markdown/seccion_4_section_1_wine_and_the_consumer/4-1_1_the_systematic_approach_to_tasting_wine.md` | tannin, tannins, acidity |
| Q367 | RA3 | `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-2_13_bordeaux.md` | spring frosts, spring frost, frost |
| Q464 | RA2 | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md` | tannin, tannins, Reduce |
| Q493 | RA1 | `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-2_13_bordeaux.md` | frost, spring frosts, spring frost |

## Discard Recommendations

| Item | RA | Source | Current grounding | Problematic distractor | Evidence file |
|---|---|---|---|---|---|
| Q218 | RA3 | new review signal | NOT_FOUND | B: Champagne usa el método Charmat | `knowledge/official-wset/study-guide/wset_markdown/seccion_7_section_4_sparkling_wines_of_the_world/7-2_42_sparkling_wines_of_the_world.md` |
| Q370 | RA2 | original inventory | NOT_FOUND | A: Barossa Valley | `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-28_39_australia.md` |
| Q661 | RA3 | original inventory | PARTIAL | A: Chardonnay | `knowledge/official-wset/study-guide/wset_markdown/seccion_7_section_4_sparkling_wines_of_the_world/7-2_42_sparkling_wines_of_the_world.md` |
| Q823 | RA5 | original inventory | NOT_FOUND | D: IGP | `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-20_31_portugal.md` |

## Remaining Human Review Queue

| Item | Severity | Source | RA | Problematic distractor | Evidence file |
|---|---|---|---|---|---|
| Q5 | moderado | original inventory | UNKNOWN | A: Crianza biológica bajo flor | `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-1_43_sherry.md` |
| Q17 | moderado | original inventory | UNKNOWN | C: Estimular la fermentación maloláctica | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-4_7_common_elements_in_winemaking_and_maturation.md` |
| Q252 | moderado | original inventory | RA2 | B: Syrah | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md` |
| Q263 | moderado | original inventory | RA2 | C: Syrah | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md` |
| Q328 | moderado | new review signal | RA2 | C: Fermentación maloláctica completa | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-4_7_common_elements_in_winemaking_and_maturation.md` |
| Q361 | menor | original inventory | RA2 | B: Santa Barbara | `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-22_33_california.md` |
| Q405 | moderado | original inventory | RA2 | D: Gran Reserva | `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-19_30_spain.md` |
| Q409 | moderado | original inventory | RA2 | A: Barossa Valley | `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-28_39_australia.md` |
| Q414 | moderado | original inventory | RA2 | D: Walker Bay | `knowledge/official-wset/study-guide/wset_markdown/seccion_6_section_3_still_wines_of_the_world/6-27_38_south_africa.md` |
| Q416 | moderado | original inventory | RA2 | A: Syrah | `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md` |

## Dataset Changes

No question-bank dataset changes were applied. The updated evidence dataset is `docs/CORPUS_REMEDIATION_DATASET.json`; it records item-level before/after grounding, conflict status, severity, evidence passage, cause, and remediation status for all 524 processed SBA items.

## Traceability Notes

- Every AUTO_FIXED item has `dataset_change_applied: false`; the fix is to the audit interpretation, not the bank.
- Remaining HUMAN_REVIEW and DISCARD items include the problematic distractor, evidence file, excerpt, and matched terms in the dataset.
- The stricter official-only corpus boundary explains the increase in NOT_FOUND and the decrease in STRONG. Those are not regressions in the bank; they are removal of unsupported evidence sources.

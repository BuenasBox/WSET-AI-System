# Gold Bank Activation Readiness

Phase 4A.3.7.33A - Gold Bank Activation Readiness

Status: documentary readiness analysis only. This document does not activate questions, publish a payload, modify questions, modify distractors, modify the dynamic exporter, touch frontend visual code, or change Tutor, Retrieval, Self-Eval, or governance behavior.

## Executive Decision

The current 18 active/elegible private Diagnostic SBA items are **not** the best 18 candidates available.

They are a historically eligible static-demo set with useful topic variety, but they do not meet the stricter Gold Bank evidence threshold. Only 2 of the 18 active items are Gold candidates, and both are Gold-A: Q2 and Q83. The remaining 16 active items are not Gold under the official-corpus-grounded classification from `docs/CORPUS_GROUNDED_GOLD_BANK.md`.

Activation recommendation: **do not activate globally and do not expand blindly to 24**. The next phase should be a controlled candidate replacement/expansion plan based on Gold-A first, then tightly reviewed Gold-B where coverage requires it.

## Evidence Base

Inputs reviewed:

| Artifact | Use |
|---|---|
| `docs/CORPUS_GROUNDED_GOLD_BANK.md` | Gold-A/B/C ranking and Gold rationale. |
| `docs/CORPUS_REMEDIATION_DATASET.json` | Official-only grounding state and conflict state. |
| `docs/DIAGNOSTIC_SBA_PHASE_4A_3_7_35_CANONICAL_BASELINE.md` | Canonical 18 active/elegible source IDs. |
| `frontend/diagnostic-sba/preguntas.json` | Current active payload metadata for RA/topic/subtopic/difficulty. |
| `knowledge/question-bank/structured/wset3_questions.json` | Correct answer position and source-bank metadata only. |

Current baseline from the Gold Bank:

| Metric | Count |
|---|---:|
| Valid SBA items | 524 |
| STRONG official-corpus items | 41 |
| Gold-A | 15 |
| Gold-B | 20 |
| Gold-C | 6 |
| Active/elegible private items | 18 |
| Active items that are Gold-A | 2 |
| Active items that are Gold-B | 0 |
| Active items that are Gold-C | 0 |
| Active items that are not Gold | 16 |

## Active vs Gold Comparison

### Active Set

Current active/elegible source IDs:

```text
Q2, Q4, Q5, Q12, Q15, Q17, Q20, Q30, Q44, Q50, Q78, Q83, Q87, Q108, Q247, Q253, Q386, Q510
```

| Active item | RA | Topic | Subtopic | Difficulty | Grounding | Conflict | Gold status |
|---|---|---|---|---|---|---|---|
| Q2 | RA4 | fortified_wines | port_fortification_fermentation | intermediate | STRONG | false | Gold-A rank 1 |
| Q4 | RA4 | fortified_wines | sherry_solera_fractional_blending | foundational | PARTIAL | false | Not Gold |
| Q5 | RA4 | fortified_wines | oloroso_amontillado_ageing_contrast | distinction | PARTIAL | true | Not Gold |
| Q12 | RA1 | viticulture | spring_frost_topography | intermediate | PARTIAL | false | Not Gold |
| Q15 | RA5 | price_factors | production_cost_mechanisation | intermediate | NOT_FOUND | false | Not Gold |
| Q17 | RA1 | winemaking | destemming_tannin_extraction | intermediate | PARTIAL | true | Not Gold |
| Q20 | RA1 | winemaking | extraction_and_body | intermediate | NOT_FOUND | false | Not Gold |
| Q30 | RA3 | sparkling_wines | traditional_method_autolysis | intermediate | PARTIAL | false | Not Gold |
| Q44 | RA1 | wine_and_food | tannin_salt_fat_pairing | intermediate | PARTIAL | false | Not Gold |
| Q50 | RA1 | storage_and_service | long_term_storage_conditions | intermediate | NOT_FOUND | false | Not Gold |
| Q78 | RA1 | storage_and_service | cork_horizontal_storage | intermediate | NOT_FOUND | false | Not Gold |
| Q83 | RA1 | quality_factors | ageability_structure_balance | intermediate | STRONG | false | Gold-A rank 2 |
| Q87 | RA1 | storage_and_service | old_wine_decanting_sediment | intermediate | NOT_FOUND | false | Not Gold |
| Q108 | RA3 | sparkling_wines | charmat_primary_aroma_retention | intermediate | NOT_FOUND | false | Not Gold |
| Q247 | RA2 | still_wines | mosel_cool_climate_acidity | intermediate | PARTIAL | false | Not Gold |
| Q253 | RA2 | still_wines | barolo_nebbiolo_tannin_ageing | intermediate | PARTIAL | false | Not Gold |
| Q386 | RA2 | still_wines | mosel_pfalz_riesling_comparison | intermediate | PARTIAL | false | Not Gold |
| Q510 | RA1 | viticulture | noble_rot_humid_morning_mist | intermediate | NOT_FOUND | false | Not Gold |

### Cross-Set Overlap

| Comparison set | Active overlap |
|---|---|
| Top 12 Gold-A | Q2, Q83 |
| Top 24 Gold | Q2, Q83 |
| Top 36 Gold | Q2, Q83 |

This means every Top 12, Top 24, and Top 36 Gold candidate other than Q2 and Q83 is currently inactive.

## Groups A-E

### Group A - Active Items That Are Gold-A

| Item | Gold rank | RA | Topic signal | Readiness note |
|---|---:|---|---|---|
| Q2 | 1 | RA4 | Port fortification | Keep. Strong mechanism support and clean conflict state. |
| Q83 | 2 | RA1 | Ageability and structure | Keep. Strong diagnostic signal around acidity, tannin, balance, and ageability. |

### Group B - Active Items That Are Gold-B

None.

### Group C - Active Items That Are Gold-C

None.

### Group D - Gold-A Items That Are Not Active

| Item | Gold rank | RA | Topic signal |
|---|---:|---|---|
| Q105 | 3 | RA4 | Sherry oxidative complexity |
| Q228 | 4 | RA2 | Chianti Classico |
| Q258 | 5 | RA2 | Uco Valley altitude/coolness |
| Q265 | 6 | RA2 | Central Otago Pinot Noir |
| Q287 | 7 | RA2 | Barolo structure |
| Q309 | 8 | RA2 | Tokaj botrytis |
| Q356 | 9 | RA2 | Sta. Rita Hills / coastal Pinot Noir |
| Q424 | 10 | RA2 | Barossa Valley Shiraz |
| Q659 | 11 | RA3 | Brut Nature / no dosage |
| Q834 | 12 | RA5 | German Pradikat label hierarchy |
| Q269 | 13 | RA2 | Vinho Verde |
| Q438 | 14 | RA2 | Willamette Valley Pinot Noir |
| Q498 | 15 | RA2 | Canopy management / fungal disease |

### Group E - Gold-B Items That Are Not Active

| Item | Gold rank | RA | Topic signal |
|---|---:|---|---|
| Q107 | 16 | RA3 | Prise de mousse |
| Q206 | 17 | RA4 | Port varieties |
| Q216 | 18 | RA3 | Cremant de Loire / Chenin Blanc |
| Q230 | 19 | RA1 | Continental-climate red structure |
| Q232 | 20 | RA2 | Pinot Noir terroir sensitivity |
| Q240 | 21 | RA3 | Charmat / Prosecco |
| Q268 | 22 | RA2 | Nebbiolo young style |
| Q270 | 23 | RA2 | Chinon / Cabernet Franc |
| Q277 | 24 | RA2 | Oregon Pinot Noir |
| Q301 | 25 | RA2 | Chile / Cabernet Sauvignon |
| Q308 | 26 | RA2 | Marlborough Sauvignon Blanc |
| Q325 | 27 | RA2 | Loire Sauvignon Blanc |
| Q395 | 28 | RA2 | Maipo Cabernet Sauvignon profile |
| Q402 | 29 | RA2 | Douro / Touriga Nacional |
| Q421 | 30 | RA2 | Ribera del Duero climate effect |
| Q440 | 31 | RA1 | Chablis / avoiding MLF |
| Q441 | 32 | RA2 | Medoc red structure |
| Q464 | 33 | RA2 | Destemming and green tannin |
| Q493 | 34 | RA1 | Late harvest frost exposure |
| Q515 | 35 | RA1 | Open vats / malolactic fermentation |

## Quality of the Active Set

### Are The 18 Active Items The Best 18 Available?

No.

The best 18 available under the current Gold Bank ranking would be:

```text
Q2, Q83, Q105, Q228, Q258, Q265, Q287, Q309, Q356, Q424, Q659, Q834, Q269, Q438, Q498, Q107, Q206, Q216
```

That set consists of 15 Gold-A items plus the top 3 Gold-B items. The current active set contains only Q2 and Q83 from that ranked group.

### How Many Should Remain?

Strict Gold-readiness answer: **2 should remain as Gold-aligned candidates**.

Private-lab continuity answer: the other 16 can remain only as current static-demo private items until replaced or promoted, but they should not be represented as Gold candidates and should not be used as the basis for expansion.

### How Many Should Be Replaced?

For a best-18 Gold-aligned lab set: **16 should be replaced**.

The replacement should not be implemented in this phase. This is a readiness finding only.

### Expected Gain From Replacement

Replacing the 16 non-Gold active items with ranked Gold candidates would produce these gains:

| Dimension | Current active 18 | Gold-aligned 18 candidate set | Gain |
|---|---:|---:|---|
| STRONG official grounding | 2 | 18 | +16 STRONG items |
| PARTIAL items | 9 | 0 | Removes 9 weakly grounded active items |
| NOT_FOUND items | 7 | 0 | Removes 7 unsupported active items |
| Active conflict items | 2 | 0 | Removes Q5 and Q17 conflict risk |
| Gold-A items | 2 | 15 | +13 Gold-A items |
| Gold-B items | 0 | 3 | Adds only the top reviewed Gold-B items |
| Non-Gold items | 16 | 0 | Removes non-Gold activation debt |

The tradeoff is coverage: the current active set has broader service/storage/food-pairing representation, but much of that breadth is not corpus-grounded enough. A Gold-aligned set has stronger evidence, but it is RA2-heavy and still weak in service/storage/price.

## Coverage of the 18 Active Items

### RA Coverage

| RA | Active count | Assessment |
|---|---:|---|
| RA1 | 9 | Overcovered numerically, but many are PARTIAL or NOT_FOUND. |
| RA2 | 3 | Undercovered for WSET L3 still-wine regional diagnosis. |
| RA3 | 2 | Undercovered; both active RA3 items are not Gold. |
| RA4 | 3 | Reasonable count, but only Q2 is Gold-A; Q5 has conflict. |
| RA5 | 1 | Undercovered and unsupported; Q15 is NOT_FOUND. |

### Topic Coverage

| Topic | Active count | Assessment |
|---|---:|---|
| fortified_wines | 3 | Present, but only Port fortification Q2 is Gold-A; Q5 has conflict. |
| viticulture | 2 | Useful causal topics, but Q12 is PARTIAL and Q510 is NOT_FOUND. |
| winemaking | 2 | Present, but Q17 has conflict and Q20 is NOT_FOUND. |
| sparkling_wines | 2 | Present, but Q30 is PARTIAL and Q108 is NOT_FOUND. |
| wine_and_food | 1 | Valuable diagnostic gap-filler, but only PARTIAL. |
| storage_and_service | 3 | Overrepresented relative to evidence; all three are NOT_FOUND. |
| quality_factors | 1 | Strong: Q83 is Gold-A. |
| still_wines | 3 | Underrepresented relative to WSET L3 scope; all three are PARTIAL. |
| price_factors | 1 | Valuable RA5/price signal, but NOT_FOUND. |

### Subtopic Coverage

Overcovered or fragile subtopics:

| Subtopic cluster | Items | Readiness issue |
|---|---|---|
| Storage/service handling | Q50, Q78, Q87 | All NOT_FOUND; coverage exists but is not Gold-ready. |
| Fortified Sherry/Port basics | Q2, Q4, Q5 | Q2 is strong; Q4 is PARTIAL; Q5 has conflict. |
| RA1 handling/winemaking basics | Q17, Q20, Q44 | One conflict, one NOT_FOUND, one PARTIAL. |

Undercovers and vacuums:

| Gap | Evidence |
|---|---|
| RA2 regional still wines | Only Q247, Q253, Q386 active; all are PARTIAL, while many inactive Gold-A RA2 items exist. |
| RA3 Gold-ready sparkling | No active Gold RA3 item; Q659 is inactive Gold-A. |
| RA5 Gold-ready label/law/category | Active Q15 is NOT_FOUND; inactive Q834 is the only Gold-A RA5 item. |
| Service/storage Gold readiness | Active breadth exists, but no active service/storage item is Gold. |
| Price/commercial reasoning | Active Q15 is NOT_FOUND; no Gold-A price item currently exists. |

### Difficulty Coverage

| Difficulty | Active count | Assessment |
|---|---:|---|
| foundational | 1 | Thin entry-level coverage. |
| intermediate | 16 | Dominant; not a meaningful cognitive spread. |
| distinction | 1 | Thin advanced coverage, and the one distinction item Q5 has conflict. |

Difficulty is not reliable enough yet as an activation selector. It should be treated as descriptive metadata, not a readiness guarantee.

## Suggested Replacements

No replacements are authorized in this phase. The following is a planning recommendation only.

### Strict Best-18 Gold Candidate Set

Keep:

```text
Q2, Q83
```

Replace the 16 non-Gold active items with:

```text
Q105, Q228, Q258, Q265, Q287, Q309, Q356, Q424, Q659, Q834, Q269, Q438, Q498, Q107, Q206, Q216
```

Rationale: this preserves all 15 Gold-A candidates and uses only the top 3 Gold-B items to reach 18.

### Coverage-Aware Variant

If the lab requires better RA1/RA3/RA4 balance, the first Gold-B candidates to evaluate are:

| Candidate | Why |
|---|---|
| Q107 | RA3 sparkling production term; needs term-specific source confirmation. |
| Q206 | RA4 fortified/Port variety coverage; needs RA/topic normalization. |
| Q216 | RA3 Cremant/Chenin coverage; needs source-specificity review. |
| Q230 | RA1 structure/climate reasoning; useful if RA1 coverage drops too far after replacement. |
| Q240 | RA3 Charmat/Prosecco; useful replacement for active Q108 if method-specific support is tightened. |

## Path to 24

### Scenario Conservador: 18 -> 24

Goal: minimum risk. Do not grow by appending six items to the current active 18. First replace the non-Gold debt.

Recommended documentary candidate set: Top 24 Gold.

```text
Q2, Q83, Q105, Q228, Q258, Q265, Q287, Q309, Q356, Q424, Q659, Q834,
Q269, Q438, Q498, Q107, Q206, Q216, Q230, Q232, Q240, Q268, Q270, Q277
```

Expected profile:

| Class | Count |
|---|---:|
| Gold-A | 15 |
| Gold-B | 9 |
| Gold-C | 0 |

Readiness condition before activation: the 9 Gold-B items need source-specific review notes resolved or explicitly accepted as low-risk training-only items.

### Scenario Balanceado: 24 -> 36

Goal: better topical spread and stronger regional coverage, while still excluding Gold-C from activation.

Recommended documentary candidate set: Top 36 Gold, with a hard review gate on ranks 25-35 and no automatic activation of rank 36.

```text
Top 24 Gold plus Q301, Q308, Q325, Q395, Q402, Q421, Q440, Q441, Q464, Q493, Q515
```

Q21 is rank 36 but Gold-C. It should remain out of any activation set unless reviewed and repaired in a later non-documentary phase.

Expected profile if Q21 is excluded:

| Class | Count |
|---|---:|
| Gold-A | 15 |
| Gold-B | 20 |
| Gold-C | 0 |
| Candidate count | 35 |

To reach exactly 36 without Gold-C, the project needs one more promoted PARTIAL or a newly hardened STRONG item. This is a useful constraint: the bank supports a strong 24 more readily than a clean 36.

### Scenario Ambicioso: 36 -> 50

Goal: broad lab coverage only if the Gold Bank grows beyond the current 41 STRONG items.

Current evidence does **not** support a clean 50-item Gold activation path. The full STRONG set contains only 41 items, and six of those are Gold-C. A 50-item activation set would necessarily include either Gold-C items, PARTIAL items, or newly promoted candidates.

Minimum prerequisites for a 50-item path:

| Requirement | Reason |
|---|---|
| Promote at least 15-20 PARTIAL candidates through source-specific evidence hardening | Needed to avoid Gold-C and NOT_FOUND debt. |
| Prioritize RA5, service/storage, food pairing, price, and RA3 method topics | Current Gold Bank is RA2-heavy and weak in consumer/service domains. |
| Resolve conflict/HUMAN_REVIEW queue before inclusion | Conflict items should not enter a private diagnostic lab unchanged. |
| Re-run official-only corpus verification | A 50-item set cannot be inferred from the current 41 STRONG baseline. |

Recommendation: do not plan a 50-item activation until after at least one PARTIAL-promotion cycle.

## Option Shuffle Readiness

No option shuffle is authorized in this phase.

### Does The Dataset Permit Safe Shuffle?

Conditionally, yes, but not yet as an activation step.

The data model has enough stable identifiers to support future shuffle if the implementation preserves:

| Field / concept | Must be preserved |
|---|---|
| `source_question_id` | Primary source traceability back to structured bank and audit records. |
| `item_id` / `draft_id` / `review_id` | Draft/review lineage and static-demo eligibility traceability. |
| Original `option_id` A/B/C/D | Needed to preserve diagnostic role and answer-key lineage after display order changes. |
| Correct option mapping | Must remain internal/outcome-only and must not leak into pre-submit payload. |
| Option diagnostics | Must follow original option identity, not display position. |
| Export metadata | Must record whether display order was canonical or shuffled. |

### Are There Dependencies On A/B/C/D Order?

Yes, there are practical dependencies today:

| Dependency | Risk |
|---|---|
| Structured bank stores `correct_answer_letter` as A/B/C/D | Shuffle must translate original answer letter to displayed order internally. |
| Payload options are emitted in sorted A/B/C/D order | Frontend currently treats displayed index as the selected option position. |
| Tests assert no correct answer leakage in render payload and outcome-only answer key availability | Shuffle must preserve the render/outcome separation. |
| Correct answer distribution analysis depends on original letters | Shuffle would invalidate position-bias metrics unless original and display positions are stored separately. |
| Gold-C Q111 has duplicate option text | Duplicate option text can make option identity ambiguous; such items must not be shuffled into activation unchanged. |

### Shuffle Readiness Conclusion

The dataset is structurally close to shuffle-ready, but the activation path should first define an explicit immutable `original_option_id` and separate it from `display_option_id` or display index. Option shuffle should be tested as a dedicated phase after Gold candidate selection, not bundled into expansion.

## Risks

| Risk | Assessment |
|---|---|
| Active/elegible may be mistaken for Gold-ready | High. Sixteen active items are not Gold. |
| Expanding current 18 to 24 by appending Gold items | High. This would preserve existing grounding debt and make the lab look broader without improving its core evidence quality. |
| RA2 dominance in Gold Bank | Medium. The strongest Gold candidates are heavily RA2/regional. |
| Service/storage/food/price gaps | High. Current active set covers these areas, but mostly without STRONG support. |
| Gold-B source specificity | Medium. Many Gold-B items need tighter source-specific evidence before activation. |
| Gold-C accidental inclusion | High. Gold-C should remain excluded from activation until reviewed/repaired. |
| Option-position bias | Medium. Gold sets remain B/C-heavy; shuffle may help later but requires traceability work. |
| Governance drift | Low if this remains documentary. No examiner authority or official scoring is introduced here. |

Governance invariants remain unchanged:

```text
safe_for_examiner = False
examiner_scoring_allowed = False
uses_llm = False
uses_api = False
uses_embeddings = False
uses_vector_db = False
cloud_services_active = False
```

## Recommendation For Next Phase

Recommended next phase: **Phase 4A.3.7.34 - Controlled Gold-A Expansion to 24 Candidate Plan**.

Scope should remain controlled:

1. Do not append six items to the current 18.
2. Define a replacement-first activation candidate set using Q2 and Q83 plus inactive Gold-A items.
3. Decide whether the phase target is strict best-18 replacement or a Top-24 Gold candidate set.
4. Resolve or explicitly accept the review notes for Gold-B ranks 16-24 before any 24-item activation.
5. Keep Gold-C excluded.
6. Keep option shuffle as a separate readiness/implementation phase after candidate selection.

Bottom line: the project now has enough evidence to stop expanding blindly. A 24-item private Diagnostic SBA lab is plausible, but it should be built from the Gold Bank ranking, not from the current active set plus additions.

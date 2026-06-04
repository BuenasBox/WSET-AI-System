# Active Set Reconciliation Plan

Phase 4A.3.7.33B - Active Set Reconciliation Plan

Status: planning artifact only. This document does not replace, activate, deactivate, publish, edit, shuffle, or export any Diagnostic SBA question. It does not modify questions, distractors, payloads, exporter behavior, Tutor, Retrieval, Self-Eval, or governance.

## Executive Decision

The current active/elegible 18-item private set should not be expanded as-is. It should first be reconciled against the Corpus-Grounded Gold Bank.

Only two current active items are Gold-A:

```text
Q2, Q83
```

The controlled replacement plan is therefore replacement-first:

1. Keep Q2 and Q83.
2. Remove the 16 non-Gold active items from the future Gold-aligned active candidate set.
3. Fill the 18-item target with the remaining top Gold-A items plus the top three Gold-B items.
4. Expand to 24 only after the 18-item set is Gold-aligned.
5. Treat 24 to 36 as a reviewed expansion, because rank 36 is Gold-C and should not become an activation item unchanged.

## Evidence Base

Inputs reviewed:

| Artifact | Use |
|---|---|
| `docs/CORPUS_GROUNDED_GOLD_BANK.md` | Gold-A/B/C ranking, coverage, replacement rationale. |
| `docs/GOLD_BANK_ACTIVATION_READINESS.md` | Active-vs-Gold overlap and readiness constraints. |
| `docs/DIAGNOSTIC_SBA_PHASE_4A_3_7_35_CANONICAL_BASELINE.md` | Canonical 18 active/elegible source IDs. |
| `frontend/diagnostic-sba/preguntas.json` | Current render payload shape and active metadata. |
| `tools/question_generation/static_demo_exporter.py` | Exporter ordering and A-D option validation constraints. |
| `docs/STATIC_DEMO_EXPORT_CONTRACT.md` | Render/outcome separation and audit-trail requirements. |
| `docs/DIAGNOSTIC_SBA_COCKPIT_CONTRACT.md` | Frontend dependency on option IDs and outcome payloads. |

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

## Current Active Ranking

This is a reconciliation ranking, not a learner-facing order. It ranks the 18 current active/elegible items by Gold alignment, grounding state, conflict state, and future promotion value.

| Reconciliation rank | Active item | RA | Topic / subtopic | Classification | Motive |
|---:|---|---|---|---|---|
| 1 | Q2 | RA4 | fortified_wines / port_fortification_fermentation | Gold-A rank 1 - keep | STRONG official support, clean conflict state, clear mechanism question, already active/elegible. |
| 2 | Q83 | RA1 | quality_factors / ageability_structure_balance | Gold-A rank 2 - keep | STRONG support and strong diagnostic signal around acidity, tannin, balance, and ageability. |
| 3 | Q247 | RA2 | still_wines / mosel_cool_climate_acidity | Not Gold - high-priority PARTIAL promotion candidate | Valuable Mosel/cool-climate/acidity coverage, but currently PARTIAL rather than STRONG. |
| 4 | Q253 | RA2 | still_wines / barolo_nebbiolo_tannin_ageing | Not Gold - high-priority PARTIAL promotion candidate | Valuable Barolo/Nebbiolo/ageing coverage, but currently PARTIAL rather than STRONG. |
| 5 | Q386 | RA2 | still_wines / mosel_pfalz_riesling_comparison | Not Gold - high-priority PARTIAL promotion candidate | Useful regional comparison signal, but currently PARTIAL rather than STRONG. |
| 6 | Q30 | RA3 | sparkling_wines / traditional_method_autolysis | Not Gold - PARTIAL promotion candidate | Useful sparkling-method/autolysis coverage, but not Gold-ready under official-only grounding. |
| 7 | Q44 | RA1 | wine_and_food / tannin_salt_fat_pairing | Not Gold - PARTIAL promotion candidate | Fills food-pairing/service-adjacent gap, but only PARTIAL support. |
| 8 | Q12 | RA1 | viticulture / spring_frost_topography | Not Gold - PARTIAL | Useful causal viticulture topic, but no longer STRONG after remediation. |
| 9 | Q4 | RA4 | fortified_wines / sherry_solera_fractional_blending | Not Gold - PARTIAL | Useful fortified-wine topic, but not STRONG enough for Gold alignment. |
| 10 | Q5 | RA4 | fortified_wines / oloroso_amontillado_ageing_contrast | Not Gold - PARTIAL with conflict | Topic is valuable, but after-state conflict/HUMAN_REVIEW makes it unsuitable for Gold unchanged. |
| 11 | Q17 | RA1 | winemaking / destemming_tannin_extraction | Not Gold - PARTIAL with conflict | Winemaking topic is useful, but conflict/HUMAN_REVIEW blocks Gold alignment unchanged. |
| 12 | Q510 | RA1 | viticulture / noble_rot_humid_morning_mist | Not Gold - NOT_FOUND | Noble-rot coverage is valuable, but current official-only support is absent. |
| 13 | Q108 | RA3 | sparkling_wines / charmat_primary_aroma_retention | Not Gold - NOT_FOUND | Charmat coverage is useful, but current official-only support is absent. |
| 14 | Q15 | RA5 | price_factors / production_cost_mechanisation | Not Gold - NOT_FOUND | RA5/price signal is valuable, but current official-only support is absent. |
| 15 | Q50 | RA1 | storage_and_service / long_term_storage_conditions | Not Gold - NOT_FOUND | Storage coverage exists but is not corpus-grounded enough. |
| 16 | Q78 | RA1 | storage_and_service / cork_horizontal_storage | Not Gold - NOT_FOUND | Storage coverage exists but is not corpus-grounded enough. |
| 17 | Q87 | RA1 | storage_and_service / old_wine_decanting_sediment | Not Gold - NOT_FOUND | Service/storage handling exists but is not corpus-grounded enough. |
| 18 | Q20 | RA1 | winemaking / extraction_and_body | Not Gold - NOT_FOUND | Winemaking topic exists, but official-only support is absent. |

Set-level conclusion: Q2 and Q83 remain. The other 16 should be treated as replacement debt for a Gold-aligned active set, not as the base for expansion.

## Gold-A Candidates

### Top 12 Gold-A

| Rank | Item | RA | Topic signal | Coverage contribution | Why superior to non-Gold active items |
|---:|---|---|---|---|---|
| 1 | Q2 | RA4 | Port fortification | Fortified-wine mechanism and fermentation interruption. | Already active, STRONG, clean, mechanism-based. |
| 2 | Q83 | RA1 | Ageability and structure | Quality reasoning through acidity, tannin, balance, longevity. | Already active, STRONG, diagnostic, clean. |
| 3 | Q105 | RA4 | Sherry oxidative complexity | Fortified-wine style discrimination beyond Port. | STRONG support and cleaner than active Q4/Q5. |
| 4 | Q228 | RA2 | Chianti Classico | Italy regional still-wine coverage. | Region-specific support, cleaner than active PARTIAL RA2 items. |
| 5 | Q258 | RA2 | Uco Valley altitude/coolness | Argentina altitude/climate-to-style reasoning. | STRONG region-specific support and useful South America coverage. |
| 6 | Q265 | RA2 | Central Otago Pinot Noir | New Zealand regional/style coverage. | STRONG region-specific support; inactive active set lacks Gold RA2. |
| 7 | Q287 | RA2 | Barolo structure | Nebbiolo/Barolo style and structure. | STRONG style profile; cleaner alternative to active Q253 until Q253 is hardened. |
| 8 | Q309 | RA2 | Tokaj botrytis | Sweet-wine causal bridge: botrytis to style. | STRONG botrytis support; cleaner than active Q510 NOT_FOUND. |
| 9 | Q356 | RA2 | Sta. Rita Hills coastal Pinot Noir | California coastal climate/style coverage. | STRONG regional support; expands beyond current PARTIAL RA2. |
| 10 | Q424 | RA2 | Barossa Valley Shiraz | Australia regional style coverage. | STRONG regional support and clean distractor state. |
| 11 | Q659 | RA3 | Brut Nature / no dosage | Sparkling label/dosage terminology. | Only Gold-A sparkling candidate; cleaner than active Q30/Q108. |
| 12 | Q834 | RA5 | German Pradikat label hierarchy | RA5 label/category hierarchy. | Only STRONG RA5 Gold-A candidate; replaces unsupported active RA5 Q15. |

### Gold-A Outside The Active Set

| Item | Gold rank | RA | Coverage contribution | Why superior |
|---|---:|---|---|---|
| Q105 | 3 | RA4 | Sherry oxidative complexity. | STRONG and clean, while active Sherry-adjacent Q4 is PARTIAL and Q5 has conflict. |
| Q228 | 4 | RA2 | Chianti Classico. | STRONG region-specific still-wine coverage. |
| Q258 | 5 | RA2 | Uco Valley altitude/coolness. | STRONG climate/regional reasoning; fills South America. |
| Q265 | 6 | RA2 | Central Otago Pinot Noir. | STRONG New Zealand coverage. |
| Q287 | 7 | RA2 | Barolo structure. | STRONG Barolo-style signal, cleaner than active Q253 until source hardening. |
| Q309 | 8 | RA2 | Tokaj botrytis. | STRONG sweet-wine causal signal, cleaner than active Q510. |
| Q356 | 9 | RA2 | Sta. Rita Hills / coastal Pinot Noir. | STRONG California regional support. |
| Q424 | 10 | RA2 | Barossa Valley Shiraz. | STRONG Australia regional support. |
| Q659 | 11 | RA3 | Brut Nature / no dosage. | Only Gold-A RA3 candidate; clean sparkling terminology. |
| Q834 | 12 | RA5 | German Pradikat label hierarchy. | Only Gold-A RA5 candidate; essential label/category coverage. |
| Q269 | 13 | RA2 | Vinho Verde. | Clean Portugal region/style item. |
| Q438 | 14 | RA2 | Willamette Valley Pinot Noir. | Clean Oregon regional support and useful D-position answer. |
| Q498 | 15 | RA2 | Canopy management / fungal disease. | Strong viticulture-practice support and causal reasoning seed. |

These 13 inactive Gold-A items are superior because they are STRONG, clean, and already classified Gold-A. They replace PARTIAL, NOT_FOUND, and conflict-bearing active items with official-corpus-grounded candidates.

## Replacement Candidates

### Optimized 18-Item Candidate Set

The best 18 available under the current Gold Bank ranking are:

```text
Q2, Q83, Q105, Q228, Q258, Q265, Q287, Q309, Q356, Q424,
Q659, Q834, Q269, Q438, Q498, Q107, Q206, Q216
```

Composition:

| Class | Count | Items |
|---|---:|---|
| Gold-A | 15 | Q2, Q83, Q105, Q228, Q258, Q265, Q287, Q309, Q356, Q424, Q659, Q834, Q269, Q438, Q498 |
| Gold-B | 3 | Q107, Q206, Q216 |
| Gold-C | 0 | None |
| Non-Gold | 0 | None |

Replacement action for a future activation phase:

| Keep from active | Remove from active candidate set | Add as replacements |
|---|---|---|
| Q2, Q83 | Q4, Q5, Q12, Q15, Q17, Q20, Q30, Q44, Q50, Q78, Q87, Q108, Q247, Q253, Q386, Q510 | Q105, Q228, Q258, Q265, Q287, Q309, Q356, Q424, Q659, Q834, Q269, Q438, Q498, Q107, Q206, Q216 |

This replacement is set-level, not one-to-one by topic. A strict one-to-one topical replacement would preserve unsupported service/storage/price breadth, which is precisely the current readiness problem.

## Transition Plan

### Stage 1 - 18 Current Active Items To Optimized 18

Goal: remove non-Gold activation debt before any expansion.

Future candidate set:

```text
Q2, Q83,
Q105, Q228, Q258, Q265, Q287, Q309, Q356, Q424, Q659, Q834, Q269, Q438, Q498,
Q107, Q206, Q216
```

Prerequisites before execution in a later phase:

| Requirement | Reason |
|---|---|
| Confirm Q107 source specificity for `prise de mousse`. | Gold-B item; strong support but term-specific confirmation should be tightened. |
| Normalize Q206 RA/topic mapping. | Gold-B item; fortified/Port variety coverage but mapping needs review. |
| Confirm Q216 Cremant-specific source support. | Gold-B item; current note says support is not tightly Cremant-specific. |
| Keep Q4, Q5, Q12, Q17, Q30, Q44, Q247, Q253, Q386 in a promotion backlog, not active Gold set. | These retain pedagogical value but are not Gold-ready today. |
| Exclude all NOT_FOUND active items from Gold-aligned activation. | They create unsupported authority risk. |

Expected gain:

| Dimension | Current active 18 | Optimized 18 | Change |
|---|---:|---:|---|
| STRONG official grounding | 2 | 18 | +16 |
| Gold-A | 2 | 15 | +13 |
| Gold-B | 0 | 3 | +3 |
| Non-Gold | 16 | 0 | -16 |
| Conflict-bearing active items | 2 | 0 | -2 |
| NOT_FOUND active items | 7 | 0 | -7 |

### Stage 2 - Optimized 18 To 24

Goal: expand only after the base 18 is Gold-aligned.

Add Gold ranks 19-24:

```text
Q230, Q232, Q240, Q268, Q270, Q277
```

Resulting 24-item candidate set:

```text
Q2, Q83, Q105, Q228, Q258, Q265, Q287, Q309, Q356, Q424, Q659, Q834,
Q269, Q438, Q498, Q107, Q206, Q216,
Q230, Q232, Q240, Q268, Q270, Q277
```

Composition:

| Class | Count |
|---|---:|
| Gold-A | 15 |
| Gold-B | 9 |
| Gold-C | 0 |
| Non-Gold | 0 |

Review gates:

| Item | Gate |
|---|---|
| Q230 | Confirm climate/structure support is source-specific enough, not only SAT-generic. |
| Q232 | Accept or tighten generic Pinot Noir/terroir support. |
| Q240 | Confirm Charmat/Prosecco method-specific support. |
| Q268 | Tie Nebbiolo young-style support to source text. |
| Q270 | Confirm Chinon/Cabernet Franc support beyond grape-generic evidence. |
| Q277 | Confirm Oregon-specific support. |

### Stage 3 - 24 To 36

Goal: broaden coverage while avoiding accidental Gold-C activation.

Add Gold-B ranks 25-35:

```text
Q301, Q308, Q325, Q395, Q402, Q421, Q440, Q441, Q464, Q493, Q515
```

Rank 36 in the current Gold Bank is:

```text
Q21
```

Q21 is Gold-C. It may be listed as the documentary rank-36 Gold candidate, but it should not enter an activation set unchanged. Therefore the exact 24-to-36 plan has two tracks:

| Track | Candidate count | Items | Status |
|---|---:|---|---|
| Documentary Top-36 Gold ranking | 36 | Top 24 plus Q301, Q308, Q325, Q395, Q402, Q421, Q440, Q441, Q464, Q493, Q515, Q21 | Exact ranking continuity; Q21 is blocked by Gold-C status. |
| Activation-safe expansion | 35 until hardening produces one more candidate | Top 24 plus Q301, Q308, Q325, Q395, Q402, Q421, Q440, Q441, Q464, Q493, Q515 | Excludes Gold-C; requires one promoted PARTIAL or repaired Gold-C before exactly 36 activable items. |

Preferred 36th-slot remediation path:

| Priority | Candidate | Current state | Why |
|---:|---|---|---|
| 1 | Q247 | PARTIAL active private item | Mosel/cool-climate/acidity; high-value RA2 causal coverage. |
| 2 | Q253 | PARTIAL active private item | Barolo/Nebbiolo ageing; high-value style coverage. |
| 3 | Q386 | PARTIAL active private item | Mosel vs Pfalz comparison; useful diagnostic contrast. |
| 4 | Q852 | PARTIAL promotion priority | Magnum ageing/storage; helps RA5 storage gap. |
| 5 | Q44 | PARTIAL active private item | Food-pairing/service gap coverage. |

Recommendation: do not force Q21 into an activation set simply to reach 36. Either keep Stage 3 as a 35-item activation-safe set pending hardening, or run a separate source-specific hardening phase to promote one PARTIAL item before exact activation to 36.

## Pedagogical Risk

### Loss Of Coverage

| Area lost from current active set | Active items affected | Risk |
|---|---|---|
| Storage and service handling | Q50, Q78, Q87 | High topical loss, but all three are NOT_FOUND and therefore unsafe as Gold evidence. |
| Food pairing | Q44 | Medium loss; valuable topic but only PARTIAL. Preserve in promotion backlog. |
| Price factors | Q15 | Medium loss; RA5 price signal disappears until a better-supported RA5 item is hardened. |
| Traditional method autolysis / Charmat | Q30, Q108 | Medium loss; replaced partly by Q659 and later Q107/Q240, but method-depth remains review-gated. |
| Spring frost / destemming / extraction | Q12, Q17, Q20 | Medium loss; causal RA1/winemaking breadth drops, but Q17 has conflict and Q20 is NOT_FOUND. |
| Mosel/Barolo/Mosel-Pfalz active familiarity | Q247, Q253, Q386 | Medium loss; these are high-priority promotion candidates, but not Gold-ready today. |

### Gain Of Coverage

| Area gained | Items |
|---|---|
| Strong RA2 regional still-wine coverage | Q228, Q258, Q265, Q287, Q356, Q424, Q269, Q438 |
| Strong fortified-wine breadth | Q2, Q105, later Q206 |
| Gold-A sparkling terminology | Q659 |
| Gold-A RA5 label/category hierarchy | Q834 |
| Sweet-wine / botrytis causal bridge | Q309 |
| Viticulture practice / disease pressure seed | Q498 |
| Better answer-position spread at 18 than current C-heavy legacy patterns | Q206 and Q216 add A-position correct answers; Q438 and Q834 add D-position coverage. |

### Diagnostic Gain

| Diagnostic dimension | Expected effect |
|---|---|
| Official grounding | Major gain: optimized 18 are all STRONG. |
| Conflict reduction | Major gain: Q5 and Q17 leave the activation candidate set. |
| Unsupported authority risk | Major gain: NOT_FOUND active items are removed. |
| Regional discrimination | Major gain: more RA2 region/style items with STRONG support. |
| Causal reasoning | Mixed: stronger evidence, but some current causal service/storage topics are lost until PARTIAL promotion. |
| Misconception precision | Gain where distractors are clean; loss where current topic-specific traps are removed but not yet replaced. |

### RA1-RA5 Impact

| RA | Current active 18 | Optimized 18 | Impact |
|---|---:|---:|---|
| RA1 | 9 | 1 | Large numerical drop. Pedagogically acceptable only because most current RA1 items are PARTIAL/NOT_FOUND/conflict; needs PARTIAL hardening next. |
| RA2 | 3 | 10 | Large gain. Better aligns with WSET L3 regional still-wine diagnosis, but risks RA2 dominance. |
| RA3 | 2 | 3 | Small gain and better grounding; Q659 is Gold-A, Q107/Q216 are Gold-B review-gated. |
| RA4 | 3 | 3 | Same count, much cleaner: Q2/Q105 plus Q206 instead of Q4/Q5 debt. |
| RA5 | 1 | 1 | Same count, but Q834 replaces unsupported Q15. RA5 remains undercovered outside label hierarchy. |

Stage 2 improves RA1/RA3 slightly through Q230 and Q240. Stage 3 adds more RA1 through Q440, Q493, and Q515, but those are Gold-B review-gated. Service/storage/food/price remains the main pedagogical gap until PARTIAL promotion work is done.

## Option Shuffle Dependency Check

No option shuffle is authorized here.

### Current Dependencies On A/B/C/D Order

| Dependency | Current state | Shuffle implication |
|---|---|---|
| Render payload options | `items[].options` is emitted as a four-entry list ordered A, B, C, D. | Shuffle would break current exporter validation unless validation is changed deliberately. |
| Exporter validation | `static_demo_exporter.py` rejects render options not ordered A-D. | Current exporter is not shuffle-ready without a separate implementation phase. |
| Outcome payload | `outcomes_by_item_id[*].correct_option_id` stores the correct A/B/C/D option ID. | Shuffle must remap displayed option ID to original option identity after submit. |
| Option diagnostics | `option_diagnostics` are keyed by original A/B/C/D. | Diagnostics must follow original option identity, not display position. |
| Frontend attempt handling | Cockpit records `selected_option_id` as A/B/C/D and validates it against option IDs. | Future shuffle must distinguish selected display ID from original option ID. |
| Audit trail | `source_question_id`, `item_id`, `draft_id`, and `review_id` are stable. | These are sufficient for question-level traceability after shuffle. |
| Duplicate option text | Gold-C Q111 has duplicate option text and is already blocked. | Duplicate text items must not be shuffled into activation unchanged because identity could become ambiguous to reviewers. |

### Technical Limitation

There is no blocker in the data model that makes shuffle impossible, but the current exporter/frontend contract is fixed-order A-D. A later shuffle phase must add an explicit identity split:

| Required concept | Purpose |
|---|---|
| `original_option_id` | Stable source identity: A/B/C/D from the draft/review/outcome metadata. |
| `display_option_id` or display index | Learner-facing temporary position after shuffle. |
| Correct-answer remap | Compares learner display choice to original correct option after submit. |
| Diagnostic remap | Maps selected display option back to original diagnostic role. |
| Export metadata flag | Records canonical vs shuffled display mode for audit. |

### Shuffle Readiness Conclusion

Option shuffle can be applied later without breaking traceability if the implementation preserves original option identity and render/outcome separation. It should not be bundled with active-set reconciliation, because reconciliation already changes the candidate set and should remain independently auditable.

## Risks

| Risk | Level | Mitigation |
|---|---|---|
| Expanding current 18 without replacement | High | Replacement-first plan; do not append Gold candidates to non-Gold active debt. |
| RA1/service/storage/food/price coverage loss | High | Preserve Q44, Q247, Q253, Q386, Q852, Q837, Q824, Q820, Q30 as promotion backlog. |
| RA2 dominance after Gold alignment | Medium | Accept for 18/24 because evidence is strongest there; correct through PARTIAL hardening later. |
| Gold-B source specificity | Medium | Require item-level review gates before activation, especially ranks 16-35. |
| Gold-C accidental activation | High | Exclude Q21 and all Gold-C items from activation unless repaired/reclassified later. |
| Option-position bias | Medium | Defer shuffle to a dedicated traceability-preserving implementation phase. |
| Governance drift | Low | Keep documentary-only status; do not introduce examiner scoring or official authority. |

## Recommendation For Next Phase

Recommended next phase: Phase 4A.3.7.34 - Controlled Active Set Replacement Plan Execution Readiness.

Scope should remain non-public and controlled:

1. Choose whether Stage 1 targets the strict optimized 18 or prepares Stage 1 plus Stage 2 together.
2. Perform review-note hardening for Gold-B Q107, Q206, and Q216 before any replacement execution.
3. Keep Q2 and Q83.
4. Replace the other 16 active items only in a later explicit activation/export phase.
5. Keep option shuffle separate until original/display option identity is implemented and tested.
6. Start a PARTIAL promotion plan for service/storage/food/price and RA1 gaps before attempting an activation-safe exact 36.

Bottom line: the exact Gold-aligned 18 is available now as a candidate plan. A clean 24-item candidate set is plausible after Gold-B review gates. A clean 36-item activation set is not yet fully available without either accepting Gold-C Q21 as blocked documentary rank 36 or promoting one additional PARTIAL item through source-specific hardening.

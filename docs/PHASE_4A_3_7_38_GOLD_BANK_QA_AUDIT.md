# Phase 4A.3.7.38 - Gold Bank 36-Item QA Audit

Status: documentation-only QA audit.

Scope: only the 36 active private diagnostic SBA items exported in `frontend/diagnostic-sba/preguntas.json`.

Out of scope: no question-bank edits, no draft/review edits, no payload regeneration, no exporter changes, no visual frontend changes, no Tutor/Retrieval/Self-Eval/Golden/Snapshot changes.

This audit treats the active set as a private diagnostic training bank. It is not an exam, not official WSET scoring, and not safe for examiner authority.

## Decision Criteria

| Decision | Criteria |
|---|---|
| PASS | Exact 36-item active set; no structural/export errors; no active conflict/discard/human-review blocker; acceptable diagnostic coverage; warnings are minor. |
| PASS_WITH_WARNINGS | Exact 36-item active set and export-valid, but material warnings remain around coverage balance, redundancy, position bias, source-specificity, or metadata exposure. |
| BLOCKED | Missing/extra/duplicate active IDs, unsafe governance flag, invalid options, invalid answer key in source diagnostics, active discard/human-review blocker, or exporter validation failure. |

Final decision: **PASS_WITH_WARNINGS**.

Rationale: the active set is exactly the expected 36 IDs, exporter dry-run reports 36 eligible items and 0 validation errors, all active items are STRONG after corpus remediation with no after-state distractor conflict, and governance remains safe. Warnings remain: the visual payload omits `correct_option_id` and option diagnostics by design/implementation, the set is heavily RA2/intermediate-weighted, correct-answer position C is overrepresented, there are conceptual near-duplicates, and Q21 is the single documented Gold-C inclusion.

## Composition Verification

Expected active IDs:

`Q2, Q21, Q83, Q105, Q107, Q206, Q216, Q228, Q230, Q232, Q240, Q258, Q265, Q268, Q269, Q270, Q277, Q287, Q301, Q308, Q309, Q325, Q356, Q395, Q402, Q421, Q424, Q438, Q440, Q441, Q464, Q493, Q498, Q515, Q659, Q834`

Observed active IDs in `frontend/diagnostic-sba/preguntas.json`: exact match, same order.

| Check | Result |
|---|---|
| Active item count | PASS - 36 |
| IDs correct | PASS |
| Duplicate source IDs | PASS - none |
| `question_type` canonical | PASS - all `single_best_answer` |
| Options A-D complete | PASS - all 36 have A, B, C, D |
| Active visual payload governance | PASS - `training_item_only=true`, `official_wset_question=false`, `safe_for_examiner=false`, `examiner_scoring_allowed=false`, `static_demo_only=true` |
| Draft governance | PASS - all reviewed drafts keep `uses_llm=false`, `uses_api=false`, `uses_embeddings=false`, `uses_vector_db=false`, `cloud_services_active=false` |
| Source diagnostics | PASS - approved drafts contain one valid correct option and A-D option diagnostics |
| Visual payload answer key exposure | WARNING - `frontend/diagnostic-sba/preguntas.json` does not expose `correct_option_id` |
| Visual payload diagnostics exposure | WARNING - `frontend/diagnostic-sba/preguntas.json` does not expose `option_diagnostics` |

Interpretation: the private source diagnostics are complete in the approved diagnostic drafts/reviews, and the exporter validates successfully. The active frontend payload itself is display-oriented and omits answer-key/diagnostic internals. That is not a runtime blocker for the current exporter contract, but it should be treated as a contract clarity warning if future QA expects the active payload to be self-contained.

## Coverage Table

| ID | RA | Topic | Subtopic | Difficulty | Correct |
|---|---|---|---|---|---|
| Q2 | RA4 | fortified_wines | port_fortification_fermentation | intermediate | C |
| Q21 | RA3 | sparkling_wines | cremant_de_loire_chenin_blanc | intermediate | C |
| Q83 | RA1 | quality_factors | ageability_structure_balance | intermediate | B |
| Q105 | RA4 | fortified_wines | sherry_oxidative_complexity | intermediate | B |
| Q107 | RA3 | sparkling_wines | prise_de_mousse | intermediate | C |
| Q206 | RA4 | fortified_wines | port_varieties | intermediate | A |
| Q216 | RA3 | sparkling_wines | cremant_de_loire_chenin_blanc | intermediate | A |
| Q228 | RA2 | still_wines | chianti_classico | intermediate | B |
| Q230 | RA1 | quality_factors | continental_climate_red_structure | intermediate | A |
| Q232 | RA2 | still_wines | pinot_noir_terroir_sensitivity | intermediate | D |
| Q240 | RA3 | sparkling_wines | charmat_prosecco | intermediate | B |
| Q258 | RA2 | still_wines | uco_valley_altitude_coolness | intermediate | B |
| Q265 | RA2 | still_wines | central_otago_pinot_noir | intermediate | C |
| Q268 | RA2 | still_wines | nebbiolo_young_style | intermediate | B |
| Q269 | RA2 | still_wines | vinho_verde | intermediate | C |
| Q270 | RA2 | still_wines | chinon_cabernet_franc | intermediate | C |
| Q277 | RA2 | still_wines | oregon_pinot_noir | intermediate | C |
| Q287 | RA2 | still_wines | barolo_structure | intermediate | B |
| Q301 | RA2 | still_wines | chile_cabernet_sauvignon | intermediate | C |
| Q308 | RA2 | still_wines | marlborough_sauvignon_blanc | intermediate | C |
| Q309 | RA2 | still_wines | tokaj_botrytis | intermediate | C |
| Q325 | RA2 | still_wines | loire_sauvignon_blanc | intermediate | C |
| Q356 | RA2 | still_wines | sta_rita_hills_coastal_pinot_noir | intermediate | C |
| Q395 | RA2 | still_wines | maipo_cabernet_sauvignon_profile | intermediate | B |
| Q402 | RA2 | still_wines | douro_touriga_nacional | intermediate | C |
| Q421 | RA2 | still_wines | ribera_del_duero_climate_effect | intermediate | C |
| Q424 | RA2 | still_wines | barossa_valley_shiraz | intermediate | B |
| Q438 | RA2 | still_wines | willamette_valley_pinot_noir | intermediate | D |
| Q440 | RA1 | winemaking | chablis_avoiding_mlf | intermediate | C |
| Q441 | RA2 | still_wines | medoc_red_structure | intermediate | B |
| Q464 | RA2 | winemaking | destemming_green_tannin | intermediate | A |
| Q493 | RA1 | viticulture | late_harvest_frost_exposure | intermediate | B |
| Q498 | RA2 | viticulture | canopy_management_fungal_disease | intermediate | B |
| Q515 | RA1 | winemaking | open_vats_malolactic_fermentation | intermediate | A |
| Q659 | RA3 | sparkling_wines | brut_nature_no_dosage | intermediate | B |
| Q834 | RA5 | label_law | german_pradikat_label_hierarchy | intermediate | D |

## Coverage Distribution

| RA | Count | Audit note |
|---|---:|---|
| RA1 | 5 | Useful process/quality coverage, but not broad enough to stand alone. |
| RA2 | 22 | Dominant area; appropriate for still-wine-heavy diagnostic exploration, but overconcentrated. |
| RA3 | 5 | Adequate sparkling signal; includes one near-duplicate pair. |
| RA4 | 3 | Minimal fortified coverage; coherent but narrow. |
| RA5 | 1 | Only one label/law item; useful but underrepresented. |

| Topic | Count |
|---|---:|
| still_wines | 20 |
| sparkling_wines | 5 |
| fortified_wines | 3 |
| winemaking | 3 |
| quality_factors | 2 |
| viticulture | 2 |
| label_law | 1 |

| Difficulty | Count |
|---|---:|
| intermediate | 36 |

Difficulty assessment: acceptable for a private diagnostic lab focused on mid-level WSET L3 recognition and causal reasoning. It is not balanced enough for exam simulation because there are no explicit easy/hard bands and no official scoring calibration.

## Correct Answer Distribution

| Correct option | Count | Share |
|---|---:|---:|
| A | 5 | 13.9% |
| B | 13 | 36.1% |
| C | 15 | 41.7% |
| D | 3 | 8.3% |

Assessment: positional bias is material. C and B together account for 77.8% of correct answers, while D appears only 3 times. This does not block a private diagnostic lab, but it should be the next implementation phase before broader private publication. Do not manually rewrite answer keys; use controlled option shuffle with deterministic preservation of diagnostics.

## Diagnostic Quality By Item

| ID | Quality | Note |
|---|---|---|
| Q2 | Alta | Clear mechanism: fortification stops Port fermentation; distractors separate ageing/drying from fortification. |
| Q21 | Baja | Gold-C exception; concept overlaps Q216 and distractors are broad grape-name distractors with limited diagnostic depth. |
| Q83 | Alta | Strong ageability construct: acidity, tannin, balance; good causal and diagnostic value. |
| Q105 | Alta | Clean oxidative Sherry style discrimination; low ambiguity among styles. |
| Q107 | Media | Useful sparkling process term; source-specificity warning remains for term-level support. |
| Q206 | Media | Correct Port variety signal; distractors plausible enough, but RA/topic normalization warning remains. |
| Q216 | Media | Same Cremant/Chenin target as Q21 with cleaner phrasing; still redundant. |
| Q228 | Alta | Region/style association with coherent Italian regional distractors. |
| Q230 | Media | Good structure reasoning, but "clima continental" framing is broad and can overgeneralize. |
| Q232 | Media | Useful Pinot/terroir diagnostic, but stem is broad and generic rather than region-specific. |
| Q240 | Media | Good method contrast; term/method support should remain source-tightened. |
| Q258 | Alta | Clear altitude/coolness regional signal; useful South America coverage. |
| Q265 | Alta | Strong Central Otago/Pinot association; distractors remain plausible within New Zealand. |
| Q268 | Media | Good Nebbiolo structural profile, but source support is more SAT/style-generic. |
| Q269 | Alta | Clean Vinho Verde recognition; distractors are coherent Portuguese alternatives. |
| Q270 | Media | Correct Chinon/Cabernet Franc association; generic grape evidence warning remains. |
| Q277 | Media | Good Oregon/Pinot signal; overlaps with broader Pinot cluster. |
| Q287 | Alta | Strong Barolo structure profile; distractors clearly test style misunderstanding. |
| Q301 | Media | Correct Chile/Cabernet signal; largely recall-based and needs Chile-specific source tightness. |
| Q308 | Media | Correct Marlborough/Sauvignon Blanc signal; straightforward recall with modest distractor diagnostics. |
| Q309 | Alta | Strong Tokaj/botrytis causal bridge; useful sweet-wine diagnostic signal. |
| Q325 | Media | Correct Loire/Sauvignon Blanc association; recall-heavy and overlaps grape-region association pattern. |
| Q356 | Alta | Clear coastal California Pinot regional signal; distractors are credible California alternatives. |
| Q395 | Media | Good Maipo Cabernet profile, but overlaps Chile/Cabernet cluster and SAT-structure support. |
| Q402 | Media | Useful Douro/Touriga association; overlaps Q206 Touriga/Port family. |
| Q421 | Media | Good climate-to-structure causal item; overlaps continental/high-acidity/tannin mechanism. |
| Q424 | Alta | Clean Barossa/Shiraz regional signal with coherent Australian distractors. |
| Q438 | Alta | Strong Willamette/Pinot profile; good D-position balance, but part of Pinot cluster. |
| Q440 | Media | Useful Chablis/MLF process question; source narrowing warning remains. |
| Q441 | Media | Good Medoc structure signal; somewhat generic high-acidity/tannin profile. |
| Q464 | Media | Useful causal winemaking item; RA normalization warning remains because content is winemaking. |
| Q493 | Media | Good harvest-risk signal; needs source-context caution from Gold Bank note. |
| Q498 | Alta | Strong viticulture disease/canopy management causal item; useful non-region diagnostic signal. |
| Q515 | Baja | Potential over-inference: open truncated vats to malolactic fermentation link is less clean than other items. |
| Q659 | Alta | Clean label terminology for dosage; good sparkling balance and low ambiguity. |
| Q834 | Alta | Strong RA5 label hierarchy item; clear ordered alternatives. |

Quality distribution:

| Quality | Count |
|---|---:|
| Alta | 15 |
| Media | 19 |
| Baja | 2 |

Interpretation: quality is adequate for a private diagnostic bank. The two Baja items do not create a blocker because they are bounded to training use, but Q21 and Q515 should be first in any future adjustment pass.

## Redundancy Audit

| Pattern | Items | Severity | Note |
|---|---|---|---|
| Cremant de Loire / Chenin Blanc duplicate | Q21, Q216 | High | Same subtopic and same correct concept; Q21 is weaker and Gold-C. |
| Pinot Noir regional cluster | Q232, Q258, Q265, Q277, Q356, Q438 | Medium | Useful region spread, but repeated Pinot recognition can inflate apparent mastery. |
| Cabernet Sauvignon Chile/Maipo cluster | Q301, Q395 | Medium | Q301 tests planted variety; Q395 tests profile. Related but not exact duplicate. |
| Touriga/Port/Douro cluster | Q206, Q402, Q2 | Medium | Q2 mechanism is distinct; Q206/Q402 both reinforce Touriga/Douro-family knowledge. |
| High acidity/tannin/structure mechanism | Q83, Q230, Q268, Q287, Q421, Q441 | Medium | Useful WSET L3 reasoning pattern, but repeated mechanism may overweight structural red-wine reasoning. |
| Sparkling fermentation/method terminology | Q107, Q240, Q659 | Low | Distinct terms: prise de mousse, Charmat, dosage label. |
| Fungal/disease/late-harvest risk | Q493, Q498 | Low | Distinct risk mechanisms: frost exposure vs canopy/fungal pressure. |

No exact duplicate stems were found. The main redundancy risk is conceptual weighting, not repeated text.

## Conflict And Support Cross-Check

Artifacts checked:

- `docs/CORPUS_REMEDIATION_DATASET.json`
- `docs/CORPUS_REMEDIATION_REPORT.md`
- `docs/CORPUS_GROUNDED_GOLD_BANK.md`

Dataset result for the 36 active items:

| Signal | Active count |
|---|---:|
| `after_grounding=STRONG` | 36 |
| `after_distractor_conflict=true` | 0 |
| `remediation_status=AUTO_FIXED` | 30 |
| `remediation_status=NO_ACTION` | 6 |
| Active item in report discard recommendations | 0 |
| Active item in remaining human-review queue | 0 |
| Active item with WEAK/PARTIAL after-state support | 0 |

Gold Bank classification result:

| Gold class | Active count | Items |
|---|---:|---|
| Gold-A | 15 | Q2, Q83, Q105, Q228, Q258, Q265, Q287, Q309, Q356, Q424, Q659, Q834, Q269, Q438, Q498 |
| Gold-B | 20 | Q107, Q206, Q216, Q230, Q232, Q240, Q268, Q270, Q277, Q301, Q308, Q325, Q395, Q402, Q421, Q440, Q441, Q464, Q493, Q515 |
| Gold-C | 1 | Q21 |

Remnant warnings from `CORPUS_GROUNDED_GOLD_BANK.md`:

| Item | Warning |
|---|---|
| Q21 | Gold-C exception; source specificity and distractor strength require significant future review. |
| Q107 | Term-specific source confirmation should be tightened. |
| Q206 | RA/topic mapping should be normalized before broader activation. |
| Q216 | Cremant-specific source review should be tightened. |
| Q230 | Climate framing is source-generic. |
| Q232 | Support is grape/SAT generic rather than region-specific. |
| Q240 | Method-specific passage review should be tightened. |
| Q268 | Nebbiolo source tie should be tightened. |
| Q270 | Grape evidence is generic. |
| Q277 | Oregon-specific support should be tightened. |
| Q301 | Chile-specific support should be tightened. |
| Q308 | Marlborough-specific support should be tightened. |
| Q325 | Loire-specific support should be tightened. |
| Q395 | Support is SAT-structure heavy. |
| Q402 | Douro-specific support should be checked. |
| Q421 | Support is SAT-generic. |
| Q440 | Source support should be narrowed. |
| Q441 | Support is SAT-generic. |
| Q464 | RA should be normalized toward winemaking/RA1 or RA3 before broader activation. |
| Q493 | Matched file context should be reviewed. |
| Q515 | Vessel-to-fermentation link may be over-inferred. |

No active item carries a current discard recommendation, human-review queue blocker, weak support, partial support, or current distractor conflict in the remediation dataset.

## Difficulty Distribution

All 36 items are `intermediate`.

Assessment for private diagnostic lab: acceptable. The bank is coherent for a controlled mid-level diagnostic exercise and avoids false exam calibration.

Assessment for publication/private broader use: warning. Without easy/hard spread, learner outcomes may reflect mid-band recognition rather than calibrated mastery progression. Keep "no official scoring" and "training only" language intact.

## Warnings

1. The visual active payload omits `correct_option_id` and `option_diagnostics`; the approved diagnostic drafts retain them and exporter validation passes. Clarify whether future QA requires a self-contained private diagnostic payload or a display-only frontend payload.
2. RA2 dominates the bank with 22/36 items. This is acceptable for still-wine diagnostic emphasis but not balanced curriculum coverage.
3. All items are intermediate. This supports a focused lab but not a calibrated adaptive ladder.
4. Correct answer positions are skewed: C=15, B=13, A=5, D=3. Deterministic option shuffle should be the next implementation phase.
5. Q21 is the only Gold-C item and should remain explicitly documented as a rank-36 exception.
6. Q21/Q216 are near-duplicates. Keep only one in a future quality-adjustment pass if expansion candidates are available.
7. Q515 has the clearest residual semantic risk due to possible over-inference.

## Final Decision

**PASS_WITH_WARNINGS**

The active 36-item Gold Bank is suitable for a private diagnostic lab under current governance constraints. It should not be represented as an exam, official scoring instrument, or examiner-safe bank.

Recommended next phase: **option shuffle first**, then targeted item adjustment.

Priority order:

1. Implement deterministic option shuffle while preserving answer keys, diagnostics, and governance.
2. Replace or revise Q21 if a stronger non-duplicative candidate is available.
3. Re-check Q515 source specificity or replace it with a cleaner winemaking causal item.
4. Expand RA1/RA3/RA4/RA5 coverage before any broader private publication.
5. Add difficulty bands only after the answer-position bias and Gold-C exception are resolved.

## Verification

Command:

```powershell
python -m tools.question_generation.export_static_demo_questions --dry-run
```

Result:

```text
eligible_item_count: 36
validation_errors: 0
```

Command:

```powershell
python -m unittest discover -s tests -v
```

Result:

```text
Ran 1352 tests in 11.047s
OK (skipped=9)
```

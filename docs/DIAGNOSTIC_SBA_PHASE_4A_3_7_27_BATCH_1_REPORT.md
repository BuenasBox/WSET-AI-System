# Diagnostic SBA Phase 4A.3.7.27 Batch 1 Report

Date: 2026-06-03

Status: approved for private Diagnostic SBA expansion only.

Known unrelated blocker retained:
`KNOWN_BLOCKER_SLOW_GOLDEN_TUTOR_RETRIEVAL_2026_06_03`.

## Scope

This phase expanded the private Diagnostic SBA dataset only. It did not modify
Tutor, retrieval, self-eval golden baselines, Tutor snapshots, backend/API
runtime, embeddings, cloud services, official scoring, or examiner authority.

The static Diagnostic SBA payload was regenerated with the existing export CLI.
No cockpit HTML or visual behavior was changed.

## Dataset Result

- Draft records: 14 total.
- Review records: 14 total.
- Eligible private static-demo items: 12.
- Historical excluded items retained: `1`, `13`.
- Canonical question type: `diagnostic_single_best_answer`.

Eligible item IDs:

`2, 12, 15, 17, 20, 30, 44, 50, 83, 108, 247, 253`

## Items Added

| source_question_id | topic | subtopic | dificultad | razón de selección | señal diagnóstica aportada | riesgo pedagógico | revisión necesaria |
|---|---|---|---|---|---|---|---|
| `15` | `price_factors` | `production_cost_mechanisation` | intermediate | Adds absent price-factor coverage. | Separates human production-cost decisions from natural site factors. | Low: may be read as simplistic pricing if context is ignored. | Confirm mechanisation is framed as cost input, not quality or official price claim. |
| `20` | `winemaking` | `extraction_and_body` | intermediate | Adds applied extraction/body reasoning. | Links extraction level to structure/body rather than generic winemaking terms. | Low: body can be multifactorial. | Confirm wording stays focused on the most direct variable in this option set. |
| `30` | `sparkling_wines` | `traditional_method_autolysis` | intermediate | Adds sparkling and autolysis coverage. | Diagnoses recognition of lees/autolytic aroma markers. | Low: distractors are broad cross-style transfers. | Confirm distractors stay plausible enough for diagnostic use. |
| `44` | `wine_and_food` | `tannin_salt_fat_pairing` | intermediate | Adds service/food, tasting, and common-error coverage. | Tests tannin perception and the tannin/sweetness/spice confusion cluster. | Medium: food-pairing statements can be overgeneralized. | Confirm pairing wording remains bounded and training-only. |
| `50` | `storage_and_service` | `long_term_storage_conditions` | intermediate | Adds storage and service coverage. | Diagnoses heat/light/position storage errors. | Low: factual and structurally clear. | Confirm no official service-standard claim is implied. |
| `83` | `quality_factors` | `ageability_structure_balance` | intermediate | Adds quality-factor and ageability coverage. | Tests structure/balance reasoning and the error that any wine improves with age. | Medium: ageability can be mistaken for automatic quality. | Confirm feedback emphasizes structural preconditions, not quality absolutism. |
| `108` | `sparkling_wines` | `charmat_primary_aroma_retention` | intermediate | Adds second sparkling method contrast with an A answer. | Distinguishes tank-method freshness from traditional-method lees complexity. | Low: possible method-quality hierarchy if phrased poorly. | Confirm the item does not imply Charmat is better/worse than traditional method. |
| `247` | `still_wines` | `mosel_cool_climate_acidity` | intermediate | Adds still-wine regional and acidity mechanism coverage. | Applies cool-climate acidity reasoning to Mosel. | Low: acidity must not be framed as automatic quality. | Confirm regional shorthand remains accurate and source-grounded. |
| `253` | `still_wines` | `barolo_nebbiolo_tannin_ageing` | intermediate | Adds major still-wine regional structure coverage. | Connects Nebbiolo/Barolo, tannin, and ageing potential. | Low: appellation recognition must not imply official authority. | Confirm distractors remain broad diagnostic contrasts. |

## Items Discarded Or Retained For Revision

No new batch-1 candidate was added and then rejected after structural review.
The batch intentionally stopped at 9 additions because these candidates were
the strongest fit for missing diagnostic coverage and answer-position balance.

Historical retained exclusions:

- `1` remains `requires_revision`: wording-safety and misconception-linkage
  review still needed.
- `13` remains `requires_revision`: single-best-answer ambiguity around soil
  drainage remains too high.

## Coverage Achieved

The 12 eligible items cover the requested diagnostic areas as follows:

| Target area | Covered by |
|---|---|
| viticultura | `12` |
| vinificación | `17`, `20` |
| vinos tranquilos | `247`, `253` |
| espumosos | `30`, `108` |
| fortificados | `2` |
| almacenamiento y servicio | `44`, `50` |
| cata | `20`, `44`, `83`, `247`, `253` |
| factores de calidad | `83` |
| factores de precio | `15` |
| regiones principales | `247`, `253` |
| errores frecuentes de estudiantes | `44`, `83`, `247` |
| razonamiento causal aplicado | `12`, `17`, `20`, `30`, `83`, `247`, `253` |

Health report distributions:

```json
{
  "topic_distribution": {
    "fortified_wines": 1,
    "price_factors": 1,
    "quality_factors": 1,
    "sparkling_wines": 2,
    "still_wines": 2,
    "storage_and_service": 1,
    "viticulture": 1,
    "wine_and_food": 1,
    "winemaking": 2
  },
  "subtopic_coverage": "12 present, 0 missing",
  "difficulty_coverage": "12 present, 0 missing"
}
```

## Difficulty Distribution

```json
{
  "intermediate": 12
}
```

Risk: the first expanded eligible set is concentrated in `intermediate`.
This was not artificially altered because the selected source-bank candidates
are all tagged intermediate or were already normalized to intermediate in the
existing private drafts. Future expansion should deliberately add foundational,
advanced, and distinction items after human review.

## Correct Answer Distribution

```json
{
  "A": 3,
  "B": 3,
  "C": 4,
  "D": 2
}
```

This removes the previous C concentration without rewriting correct answers
artificially.

## Governance Status

- `safe_for_examiner`: false for all draft/review/export records.
- `examiner_scoring_allowed`: false for all draft/review/export records.
- `official_wset_question`: false for all draft/review/export records.
- `training_item_only`: true for all draft/review/export records.
- `uses_llm`: false.
- `uses_api`: false.
- `uses_embeddings`: false.
- `uses_vector_db`: false.
- `cloud_services_active`: false.
- `validation_errors`: 0.
- `governance_violations`: [].

No official scoring, pass/fail, certification, examiner, or public publication
claim was introduced.

## Commands Executed

```powershell
python -m tools.question_generation.export_static_demo_questions --write
python -m unittest tests.test_first_5_enrichment_drafts tests.test_first_5_human_review_records tests.test_static_demo_exporter tests.test_static_demo_export_dry_run tests.test_static_demo_export_file tests.test_diagnostic_sba_validator tests.test_diagnostic_sba_schema tests.test_human_review_resolution -v
python -m tools.question_generation.export_static_demo_questions --dry-run
python -m tools.question_generation.export_static_demo_questions --health-report
python -m unittest discover -s tests -v
```

Focal test result:

```text
Ran 146 tests
OK
```

Full unittest result:

```text
Ran 1349 tests
OK (skipped=9)
```

Dry-run result:

```text
eligible_item_count: 12
source_question_ids: 2, 12, 15, 17, 20, 30, 44, 50, 83, 108, 247, 253
validation_errors: 0
```

Health result:

```json
{
  "eligible_item_count": 12,
  "validation_error_count": 0,
  "validation_errors": [],
  "governance_violations": []
}
```

## Remaining Risks

- Difficulty distribution is concentrated in `intermediate`.
- Source support remains draft/human-review scoped and must not be treated as
  public or production authorization.
- Items `1` and `13` still require revision and should not be silently
  promoted.
- The unrelated slow golden Tutor/retrieval blocker remains unresolved and
  must not be reclassified by this SBA-only phase.

## Recommendation

Approve Phase 4A.3.7.27 as a private Diagnostic SBA expansion batch.

Next phase should add a small second batch focused on:

- foundational and distinction difficulty spread;
- more fortified coverage beyond Port;
- more storage/service edge cases;
- one or two region-comparison items with stronger source support;
- explicit review of historical items `1` and `13` without forcing promotion.

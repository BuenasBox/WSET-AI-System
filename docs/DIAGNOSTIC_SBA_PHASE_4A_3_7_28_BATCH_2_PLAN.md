# Diagnostic SBA Phase 4A.3.7.28 Batch 2 Plan

Date: 2026-06-03

Status: planning gate only. No Batch 2 migration implemented.

Known unrelated blocker retained:
`KNOWN_BLOCKER_SLOW_GOLDEN_TUTOR_RETRIEVAL_2026_06_03`.

## Scope

This phase audits the private Diagnostic SBA dataset and prepares a controlled
Batch 2 shortlist. It does not modify Tutor, retrieval, self-eval, golden
baselines, Tutor snapshots, cockpit HTML/visual behavior, backend/API runtime,
LLM paths, embeddings, cloud services, dependencies, official scoring, examiner
authority, or public publication state.

The current private payload remains the Phase 4A.3.7.27 output.

## Current Dataset Audit

Source files audited:

- `knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json`
- `knowledge/question-bank/diagnostic_sba/reviews/first_5_human_review_records.json`
- `knowledge/question-bank/structured/wset3_questions.json`
- `docs/DIAGNOSTIC_SBA_PHASE_4A_3_7_27_BATCH_1_REPORT.md`

Current private Diagnostic SBA state:

- Draft records: 14.
- Review records: 14.
- Eligible private static-demo items: 12.
- Required-revision records: `1`, `13`.
- Validation errors: 0.
- Governance violations: [].

Eligible source IDs:

`2, 12, 15, 17, 20, 30, 44, 50, 83, 108, 247, 253`

Topic distribution:

```json
{
  "fortified_wines": 1,
  "price_factors": 1,
  "quality_factors": 1,
  "sparkling_wines": 2,
  "still_wines": 2,
  "storage_and_service": 1,
  "viticulture": 1,
  "wine_and_food": 1,
  "winemaking": 2
}
```

Subtopic distribution:

```json
{
  "ageability_structure_balance": 1,
  "barolo_nebbiolo_tannin_ageing": 1,
  "charmat_primary_aroma_retention": 1,
  "destemming_tannin_extraction": 1,
  "extraction_and_body": 1,
  "long_term_storage_conditions": 1,
  "mosel_cool_climate_acidity": 1,
  "port_fortification_fermentation": 1,
  "production_cost_mechanisation": 1,
  "spring_frost_topography": 1,
  "tannin_salt_fat_pairing": 1,
  "traditional_method_autolysis": 1
}
```

Difficulty distribution:

```json
{
  "intermediate": 12
}
```

Correct-answer distribution:

```json
{
  "A": 3,
  "B": 3,
  "C": 4,
  "D": 2
}
```

Health-report risks:

- `difficulty distribution concentrated in one value`
- `missing_or_weak_fields`: []
- `validation_error_count`: 0
- `governance_violations`: []

## Coverage Gaps

Priority gaps confirmed:

- Foundational: only one unused foundational SBA candidate with A-D options was
  found after excluding already drafted IDs: `4`.
- Advanced: no unused `advanced` SBA candidates with A-D options were found in
  the current structured bank. This should not be backfilled by relabeling
  intermediate items.
- Distinction: one strong unused distinction candidate was found: `5`.
- Fortified beyond Port: current eligible coverage has only `2`
  (`port_fortification_fermentation`). Batch 2 should add Sherry/Jerez and
  Madeira coverage before adding more Port.
- Storage/service edge cases: current eligible coverage has only `50`
  (`long_term_storage_conditions`) plus food-pairing item `44`. Batch 2 should
  add decanting/sediment, cork orientation, and/or service-temperature effects.
- Region-comparison: current regional items are Mosel and Barolo recognition
  items. Batch 2 can add one or two comparison items, but only with explicit
  source support because comparison stems are easy to overstate.
- Historical items `1` and `13` remain excluded and should not be promoted in
  Batch 2 without a dedicated revision phase.

## Candidate Audit Table

| source_question_id | topic | subtopic | difficulty | correct_answer_letter | reason for selection | expected diagnostic signal | probable source support | pedagogical risk | human review needed | decision |
|---|---|---|---|---|---|---|---|---|---|---|
| `4` | fortified_wines | sherry_solera_fractional_blending | foundational | C | Only strong unused foundational candidate; adds Sherry/Jerez beyond Port. | Separates solera/criaderas consistency logic from generic barrel-ageing or forced oxygenation. | `cc_fractional_blending_consistency.json`; Sherry official markdown. | Low-medium: avoid implying solera is only a term-recognition fact. | Confirm source grounding and feedback link to fractional blending/consistency. | recommend |
| `5` | fortified_wines | oloroso_amontillado_ageing_contrast | distinction | C | Strong distinction candidate; adds Sherry ageing contrast beyond item `1`. | Tests biological vs oxidative ageing and flor-loss/no-flor logic. | Sherry official markdown; `cc_flor_biological_ageing.json`; possibly local solera/fortified support. | Medium: option C must be bounded to Oloroso in the option set; avoid overbroad Sherry claims. | Confirm Amontillado vs Oloroso contrast and wording safety. | recommend |
| `95` | fortified_wines | madeira_heating_controlled_process | intermediate | D | Adds Madeira and gives a D answer without changing correctness. | Recognizes Madeira as the fortified style associated with controlled heating. | Fortified Muscats/Madeira official area if present in extracted support; structured bank only if official Madeira grounding is weak. | Medium: question is more recognition than causal diagnosis. | Confirm source support for Madeira heating before drafting. | hold |
| `96` | fortified_wines | madeira_estufagem | intermediate | B | Better diagnostic Madeira candidate than `95`; tests production process rather than style label. | Distinguishes estufagem heating from oxidative ageing, cold maturation, and flor ageing. | Madeira/fortified official support if available; current official extraction must be checked carefully. | Medium: support may be thinner in current extracted markdown than for Sherry/Port. | Confirm estufagem grounding and avoid unsupported process detail. | recommend |
| `100` | fortified_wines | madeira_style_names | intermediate | B | Adds Madeira style-name coverage. | Recognizes Sercial/Verdelho/Bual/Malmsey as Madeira styles. | Official Madeira support likely required; structured bank alone is insufficient for promotion. | Medium-high: mostly recall, weak diagnostic depth. | Confirm source support and decide whether it adds enough value beyond `96`. | hold |
| `78` | storage_and_service | cork_horizontal_storage | intermediate | B | Adds storage edge case not covered by `50`: cork orientation and oxidation risk. | Connects horizontal storage, cork moisture, air ingress, and oxidation. | Storage/service official markdown lines on side storage and cork drying. | Low: factual and source-grounded if feedback stays bounded. | Confirm no universal claim for non-cork closures. | recommend |
| `87` | storage_and_service | old_wine_decanting_sediment | intermediate | C | Adds service edge case: decanting old wine with sediment. | Distinguishes careful sediment separation from agitation or rapid pouring. | Storage/service official markdown on heavy deposit and careful decanting. | Low: clear diagnostic contrast. | Confirm feedback distinguishes sediment removal from unnecessary aeration. | recommend |
| `713` | storage_and_service | low_service_temperature_structured_red | intermediate | A | Adds service-temperature perception edge case. | Tests how too-low temperature can emphasize tannin and reduce aroma expression. | Storage/service official markdown on service temperatures and sensory effects. | Medium: source wording may not directly map to tannin emphasis. | Confirm exact source support before drafting. | hold |
| `734` | storage_and_service | white_wine_oxidation_storage_closure | intermediate | A | Adds oxidation/storage/closure edge case. | Connects stable temperature and closure choice with oxidation risk. | Storage/service official markdown plus closure/TCA support may be split. | Medium-high: screwcap claim may overstate oxidation prevention. | Requires strict source check; likely needs wording change before draft. | hold |
| `51` | storage_and_service | glassware_cleaning_aroma_contamination | intermediate | A | Adds service hygiene edge case. | Diagnoses aromatic contamination from perfumed detergent. | Storage/service official markdown on clean glasses, if sufficient. | Medium: may be too practical/low-level unless tied to aroma assessment. | Confirm support and diagnostic value. | hold |
| `386` | still_wines | mosel_pfalz_riesling_comparison | intermediate | C | Strongest region-comparison candidate found in one country/chapter area. | Compares Mosel and Pfalz Riesling through residual sugar/alcohol/body/acidity logic. | Germany official markdown likely covers Mosel and Pfalz in the same chapter. | Medium: comparison must avoid absolute style claims. | Confirm both regional profiles and bounded feedback. | recommend |
| `392` | still_wines | marlborough_loire_sauvignon_comparison | intermediate | C | Useful second comparison candidate if source support is strong enough. | Tests New Zealand vs Loire Sauvignon Blanc style contrast. | New Zealand and Loire official markdown; source support spans chapters. | Medium-high: "more tropical, greater freshness" may be too broad or imprecise. | Confirm source support across both regions; possibly rewrite wording in later phase. | hold |
| `24` | sparkling_wines | cava_champagne_multi_vintage_contrast | intermediate | C | Region/method comparison candidate with sparkling coverage. | Tests Champagne blending allowance vs distractor method errors. | Sparkling production and regional official markdown. | Medium: "Champagne permits multi-vintage blends" may be true but the distractors are uneven. | Confirm whether it is diagnostic enough after Batch 1 sparkling additions. | hold |
| `13` | viticulture | soil_texture_drainage | intermediate | C | Historical requires-revision item; could address viticulture gap if repaired. | Would test soil texture, drainage, water retention, and vine vigor. | `CC_SOIL_DRAINAGE_VINE_VIGOUR.json`; growing-environment official markdown. | High: current option set leaves single-best ambiguity. | Dedicated revision pass required. | hold |
| `1` | fortified_wines | sherry_flor_biological_ageing | distinction | C | Historical requires-revision item; strong topic but not yet wording-safe. | Would test flor oxygen protection and biological-ageing character. | `cc_flor_biological_ageing.json`; Sherry official markdown. | Medium: wording-safety and misconception-linkage signoff missing. | Dedicated revision pass required. | hold |

## Recommended Batch 2 Shortlist

Recommended for the next implementation phase, subject to human-review drafting:

| source_question_id | role in Batch 2 |
|---|---|
| `4` | Adds foundational difficulty and Sherry/Jerez solera coverage. |
| `5` | Adds distinction difficulty and Sherry biological/oxidative contrast. |
| `78` | Adds storage-service cork/orientation/oxidation edge case. |
| `87` | Adds storage-service decanting/sediment edge case. |
| `96` | Adds Madeira production coverage beyond Port. |
| `386` | Adds a region-comparison item with likely strong Germany source support. |

Optional stretch candidate:

| source_question_id | condition |
|---|---|
| `392` | Add only if a source-support check confirms the Marlborough/Loire comparison is precise and bounded. Otherwise keep out of Batch 2. |

This shortlist intentionally remains small. It targets missing difficulty spread
and coverage gaps without migrating a large set from the structured bank.

## Hold / Reject List

Hold:

- `95`: useful Madeira answer-position candidate, but weaker diagnostically than
  `96` because it tests style recognition more than process reasoning.
- `100`: useful Madeira recall item, but lower diagnostic value than `96`.
- `713`: potentially useful service-temperature item, but needs direct support
  for the tannin/aroma wording.
- `734`: closure/storage wording may overstate screwcap as an oxidation-control
  answer; requires source and wording review.
- `51`: practical service item; hold until glassware-cleaning support and
  diagnostic value are confirmed.
- `392`: potentially valuable comparison item; hold unless source support is
  strong across both Marlborough and Loire.
- `24`: plausible sparkling comparison item; hold because Batch 1 already added
  two sparkling items and the distractor set may be less diagnostic.
- `1`: historical requires-revision item; do not promote in Batch 2 planning.
- `13`: historical requires-revision item; do not promote in Batch 2 planning.

Reject for Batch 2:

- Any candidate selected only because it has four options and a correct answer
  letter.
- Any `intermediate` candidate relabeled as `advanced` or `distinction` to fill
  difficulty coverage.
- Any candidate whose answer key would need to be changed for answer-position
  balance.
- Any public, examiner, official-scoring, production-bank, or cockpit-facing
  migration.

## Historical Item Review

### source_question_id `1`

Current status: `requires_revision`.

Reason it remains excluded:

- Review did not record wording-safety signoff.
- Misconception linkage is unresolved.
- The draft itself asks for confirmation that wording is sufficiently
  paraphrased from local support.

Correctability assessment:

- Seems corrigible. The core answer is pedagogically useful and source support
  is plausible through flor/biological-ageing support and Sherry source areas.
- It should not be promoted in Batch 2 because it needs a focused review record,
  not silent inclusion.

Possible minimal correction:

- Keep the original correct answer letter and option set.
- Add explicit wording-safety signoff after checking the support text.
- Decide whether misconception linkage remains unattached or receives a bounded
  oxygen/oxidative-ageing confusion link.
- Tighten feedback to say "best answer in this option set" and avoid implying
  a full account of all flor effects.

Decision: hold.

### source_question_id `13`

Current status: `requires_revision`.

Reason it remains excluded:

- Correct-answer check is not signed off.
- Distractor logic is not signed off.
- Rationale quality is not signed off.
- Wording safety is not signed off.
- Review flags ambiguity around sandy structure as the single best answer.
- Clay and organic matter distractors need sharper rationale.

Correctability assessment:

- Possibly corrigible, but risk is higher than item `1`.
- The likely fix requires changing the stem or option wording to target
  drainage rate explicitly. That is beyond a planning gate and should not be
  bundled into a general Batch 2 migration.

Possible minimal correction:

- Reframe the stem toward drainage rate/permeability rather than "element of
  soil" generally.
- Preserve the original correct answer only if the revised stem makes sandy
  structure clearly the best answer.
- Strengthen the distractor rationales: clay as water retention/poor drainage,
  limestone as composition rather than texture, organic matter as water/nutrient
  influence rather than direct drainage answer.

Decision: hold.

## Risk Assessment

Primary risks for Batch 2:

- Difficulty coverage cannot be fully solved from the current structured bank:
  there are no unused `advanced` A-D SBA candidates found in the audit.
- Adding `4` and `5` improves difficulty spread but adds more C answers. This is
  acceptable only if quality and support remain stronger than answer-position
  balance concerns.
- Madeira support must be checked carefully. The current official extraction has
  clear fortified materials, but Batch 2 should not assume every Madeira detail
  is sufficiently grounded without direct source confirmation.
- Region-comparison items are prone to overgeneralization. `386` is preferable
  because Mosel/Pfalz can likely be checked in one Germany source area; `392`
  spans Loire and New Zealand and should stay optional.
- Historical items `1` and `13` are tempting because they address gaps, but both
  must remain excluded until explicit revision records exist.

Mitigations:

- Keep Batch 2 small.
- Draft only from the recommended shortlist.
- Preserve source question IDs and correct answer letters.
- Require source-support notes and human-review records before eligibility.
- Run the SBA focal suite and full suite if data files are changed.

## Governance Status

This planning gate introduced:

- no public publication;
- no cockpit visual changes;
- no Tutor/retrieval/self-eval/golden/snapshot changes;
- no backend/API/LLM runtime;
- no embeddings;
- no vector database;
- no cloud services;
- no new dependencies;
- no official scoring;
- no examiner authority.

Required governance state remains:

```python
safe_for_examiner = False
examiner_scoring_allowed = False
uses_llm = False
uses_api = False
uses_embeddings = False
uses_vector_db = False
cloud_services_active = False
```

## Commands Executed

```powershell
git status --short
rg --files
Get-Content -Path docs/DIAGNOSTIC_SBA_PHASE_4A_3_7_27_BATCH_1_REPORT.md
Get-Content -Path knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json
Get-Content -Path knowledge/question-bank/diagnostic_sba/reviews/first_5_human_review_records.json
Get-Content -Path knowledge/question-bank/structured/wset3_questions.json
Get-Content -Path tools/question_generation/export_static_demo_questions.py
Get-Content -Path tools/question_generation/static_demo_exporter.py
Get-Content -Path tools/question_generation/diagnostic_sba_validator.py
rg -n "Batch 2|4A.3.7.28|source_question_id|question_id" docs tools knowledge/question-bank -g "*.md" -g "*.py" -g "*.json"
python - <<'PY'
# Inline JSON audit: draft/review/eligible counts, distributions, requires_revision IDs.
PY
python - <<'PY'
# Inline structured-bank audit: candidate scans by fortified, storage/service,
# region-comparison terms, and available foundational/advanced/distinction items.
PY
python - <<'PY'
# Inline candidate detail dump for source IDs:
# 1, 4, 5, 13, 24, 51, 58, 78, 87, 95, 96, 100, 386, 392, 713, 734.
PY
rg -n "solera|criaderas|Oloroso|Amontillado|Madeira|Malmsey|Sercial|Verdelho|Bual|estuf|decant|sediment|storage|serve|service|temperature|horizontal|Marlborough|Loire|Pfalz|Mosel|Sancerre|Pouilly|TCA|screwcap|cork|bag-in-box|magnum|Sherry|Jerez|flor|oxidative" knowledge/official-wset/study-guide/wset_markdown knowledge/knowledge-map -g "*.md" -g "*.json"
python -m tools.question_generation.export_static_demo_questions --dry-run
python -m tools.question_generation.export_static_demo_questions --health-report
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

## Recommendation For Next Implementation Phase

Approve Phase 4A.3.7.28 as a planning-only gate.

Recommended next phase:

`Phase 4A.3.7.29 — Diagnostic SBA Expansion Batch 2 Controlled Drafts`

Implementation scope should be limited to creating draft/review records for
the recommended shortlist only:

`4, 5, 78, 87, 96, 386`

Do not include `1` or `13` in the Batch 2 implementation unless a separate
explicit historical-revision phase is opened first.

# Diagnostic SBA Phase 4A.3.7.29 Batch 2 Report

Date: 2026-06-03

Status: completed as controlled private Diagnostic SBA expansion.

## Scope

Phase 4A.3.7.29 expanded the private Diagnostic SBA dataset from 12 to 18
eligible items. It did not activate the full structured bank.

Changed artifacts:

- `knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json`
- `knowledge/question-bank/diagnostic_sba/reviews/first_5_human_review_records.json`
- `frontend/diagnostic-sba/preguntas.json`

The frontend change is payload-only via the existing narrow static-demo
exporter. No cockpit HTML, visual layout, backend/API, Tutor, retrieval,
self-eval, golden baseline, snapshots, LLM, embeddings, cloud service, or
dependency changes were made.

## Items Added

| source_question_id | topic | subtopic | difficulty | correct_option_id | reason for inclusion | pedagogical risk | review applied |
|---|---|---|---|---|---|---|---|
| `4` | fortified_wines | sherry_solera_fractional_blending | foundational | C | Adds the only strong unused foundational candidate and Sherry/Jerez solera coverage beyond Port. | Low: can become term-recognition if not linked to fractional blending and consistency. | Source support, single-best answer, distractor plausibility, metadata, answer-position impact, wording safety, governance. |
| `5` | fortified_wines | oloroso_amontillado_ageing_contrast | distinction | C | Adds the only strong distinction candidate and tests biological versus oxidative Sherry ageing. | Medium: Oloroso/Amontillado contrast can be overgeneralized. Feedback is bounded to the option set. | Source support, single-best answer, distractor plausibility, contrast framing, metadata, answer-position impact, wording safety, governance. |
| `78` | storage_and_service | cork_horizontal_storage | intermediate | B | Adds cork orientation and oxidation-risk reasoning not covered by the long-term storage item alone. | Low: bounded to natural cork closures. | Source support, single-best answer, distractor plausibility, closure scope, metadata, answer-position impact, wording safety, governance. |
| `87` | storage_and_service | old_wine_decanting_sediment | intermediate | C | Adds old-wine decanting and sediment-management signal. | Low: feedback separates sediment removal from broad aeration claims. | Source support, single-best answer, distractor plausibility, causal-chain linkage, metadata, answer-position impact, wording safety, governance. |
| `386` | still_wines | mosel_pfalz_riesling_comparison | intermediate | C | Adds bounded Germany region-comparison signal beyond Mosel recognition. | Medium: regional comparisons can overstate style. Feedback is bounded to the option set. | Source support, single-best answer, distractor plausibility, comparison wording, metadata, answer-position impact, wording safety, governance. |
| `510` | viticulture | noble_rot_humid_morning_mist | intermediate | D | Adds noble-rot causal reasoning, a common-student-error misconception link, and a D answer for balance. | Medium: noble rot must remain conditional, not broad humidity benefit. Feedback contrasts noble rot with grey rot. | Source support, single-best answer, distractor plausibility, misconception linkage, metadata, answer-position impact, wording safety, governance. |

## Deferred Candidates

| source_question_id | decision | reason |
|---|---|---|
| `96` | Deferred | Madeira `estufagem` is diagnostically useful, but the current official extraction did not provide direct Madeira/estufagem support. Structured-bank support alone was not enough for promotion. |
| `95` | Deferred | Adds a D answer and Madeira recognition, but weaker diagnostic depth than `96` and no direct Madeira support was found in the extracted official source area. |
| `100` | Deferred | Madeira style-name recall; useful later only after direct source support and stronger diagnostic rationale. |
| `392` | Deferred | Marlborough/Loire comparison remains too broad across chapters and risks overgeneralizing Sauvignon Blanc style. |
| `713` | Deferred | Service-temperature source support exists for cold reds tasting thin/harsh, but the candidate wording about tannin emphasis and aroma reduction needs tighter source alignment. |
| `734` | Deferred | Screwcap/storage wording may overstate oxidation prevention and mixes closure and storage variables. |
| `51` | Deferred | Glassware-cleaning item is practical but lower diagnostic priority for this batch. |
| `24` | Deferred | Sparkling comparison candidate is plausible, but Batch 1 already has two sparkling items and the distractor set is less diagnostic. |
| `1` | Deferred | Historical requires-revision item. Needs a dedicated revision/signoff phase. |
| `13` | Deferred | Historical requires-revision item. Soil-texture option set remains more ambiguous than acceptable for silent promotion. |

## Coverage Before And After

Before:

```json
{
  "eligible_item_count": 12,
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
  "difficulty_distribution": {
    "intermediate": 12
  },
  "correct_option_distribution": {
    "A": 3,
    "B": 3,
    "C": 4,
    "D": 2
  }
}
```

After:

```json
{
  "eligible_item_count": 18,
  "topic_distribution": {
    "fortified_wines": 3,
    "price_factors": 1,
    "quality_factors": 1,
    "sparkling_wines": 2,
    "still_wines": 3,
    "storage_and_service": 3,
    "viticulture": 2,
    "wine_and_food": 1,
    "winemaking": 2
  },
  "difficulty_distribution": {
    "distinction": 1,
    "foundational": 1,
    "intermediate": 16
  },
  "correct_option_distribution": {
    "A": 3,
    "B": 4,
    "C": 8,
    "D": 3
  }
}
```

## Health Report

Dry-run summary:

```text
eligible_item_count: 18
source_question_ids: 2, 4, 5, 12, 15, 17, 20, 30, 44, 50, 78, 83, 87, 108, 247, 253, 386, 510
validation_errors: 0
```

Health status:

```json
{
  "eligible_item_count": 18,
  "bias_risks": [],
  "missing_or_weak_fields": [],
  "validation_error_count": 0,
  "validation_errors": [],
  "governance_violations": []
}
```

## Governance Status

Governance remains safe:

```python
safe_for_examiner = False
examiner_scoring_allowed = False
uses_llm = False
uses_api = False
uses_embeddings = False
uses_vector_db = False
cloud_services_active = False
```

No item is an official WSET question. No official scoring, examiner authority,
certification readiness, pass/fail claim, backend runtime, API path, LLM path,
embedding path, vector DB path, cloud path, or new dependency was introduced.

## Commands Executed

```powershell
git status --short
Get-Content -Path docs/DIAGNOSTIC_SBA_PHASE_4A_3_7_28_BATCH_2_PLAN.md
rg --files
Get-Content -Path knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json
Get-Content -Path knowledge/question-bank/diagnostic_sba/reviews/first_5_human_review_records.json
Get-Content -Path tools/question_generation/diagnostic_sba_validator.py
Get-Content -Path tools/question_generation/static_demo_exporter.py
Get-Content -Path tools/question_generation/export_static_demo_questions.py
Get-Content -Path tools/question_generation/human_review_resolution.py
Select-String -Path tests/test_first_5_enrichment_drafts.py,tests/test_first_5_human_review_records.py,tests/test_diagnostic_sba_validator.py,tests/test_static_demo_exporter.py,tests/test_static_demo_export_dry_run.py -Pattern "source_question_id|eligible_item_count|review_status|approved_for_static_demo|12|14"
Select-String -Path knowledge/official-wset/study-guide/wset_markdown/**/*.md,knowledge/knowledge-map/causal-chains/cc_noble_rot_concentration.json,knowledge/knowledge-map/misconceptions/mc_botrytis_01.json -Pattern "noble rot|Botrytis|mist|humid|fog|sun|Tokaj|Sauternes" -Context 1,2
Select-String -Path knowledge/official-wset/study-guide/wset_markdown/seccion_4_section_1_wine_and_the_consumer/4-3_3_storage_and_service_of_wine.md -Pattern "temperature|cold|cool|aroma|red|tannin|structured|serve|service" -Context 2,3
python -m json.tool knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json
python -m json.tool knowledge/question-bank/diagnostic_sba/reviews/first_5_human_review_records.json
python -m tools.question_generation.export_static_demo_questions --dry-run
python -m tools.question_generation.export_static_demo_questions --health-report
python -m unittest tests.test_diagnostic_sba_schema tests.test_diagnostic_sba_validator tests.test_first_5_enrichment_drafts tests.test_first_5_human_review_records tests.test_static_demo_exporter tests.test_static_demo_export_dry_run tests.test_static_demo_export_file tests.test_diagnostic_sba_cockpit_json_loader tests.test_diagnostic_sba_loader_failure_recovery_qa -v
python -m tools.question_generation.export_static_demo_questions --write
python -m unittest tests.test_diagnostic_sba_schema tests.test_diagnostic_sba_validator tests.test_first_5_enrichment_drafts tests.test_first_5_human_review_records tests.test_static_demo_exporter tests.test_static_demo_export_dry_run tests.test_static_demo_export_file tests.test_diagnostic_sba_cockpit_json_loader tests.test_diagnostic_sba_loader_failure_recovery_qa -v
python -m unittest discover -s tests -v
git restore knowledge/nazareth/self_eval_feedback.json knowledge/retrieval-sandbox/orchestrator_context_retrieval_debug.csv
git diff --stat
```

## Test Results

- JSON validation: OK.
- Dry-run export: OK, 18 eligible, 0 validation errors.
- Health report: OK, no SBA blockers.
- SBA/export focal suite: 159 tests OK.
- Full suite: 1349 tests OK, 9 skipped.

The first focal run failed because `frontend/diagnostic-sba/preguntas.json`
still contained the previous 12-item payload while the dry-run generated 18.
The file was then updated with the existing narrow exporter, and the suite
passed. No cockpit HTML or visual behavior was changed.

## Remaining Risks

- Correct-answer distribution still leans toward C: 8 of 18 items.
- Madeira remains uncovered because direct local source support was not found
for `96`, `95`, or `100`.
- Advanced difficulty remains unavailable in the mapped A-D candidate set.
- Regional-comparison items remain higher-risk and should stay sparse.
- Historical items `1` and `13` remain excluded until a dedicated revision
phase resolves wording and ambiguity.

## Recommendation For Batch 3

Do not activate the full bank.

Batch 3 should remain controlled and should target only candidates that improve
clear deficits:

- Madeira only after direct source support is available or source extraction is
confirmed.
- One or two A/D-answer candidates only if they have real diagnostic signal.
- No relabeling intermediate items as advanced.
- No historical `1` or `13` promotion without a separate revision record.
- Keep total active private items at or below 24 until a human review pass
confirms distractor quality and coverage balance.

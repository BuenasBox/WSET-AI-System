# Phase 4A.3.7.35 Diagnostic SBA Canonical Baseline

## Base chosen

Canonical base: `origin/main` at `6e4669f`.

Rationale: this line contains the newer dynamic Diagnostic SBA exporter and the recent audit surface. The detached `fb80f0f` line was used only as a data/doc source for the private Batch 2 baseline.

## Imported from `fb80f0f`

- Private Diagnostic SBA draft/review source data needed to recover the 18 eligible private items.
- Batch 1 and Batch 2 phase documentation:
  - `docs/DIAGNOSTIC_SBA_PHASE_4A_3_7_27_BATCH_1_REPORT.md`
  - `docs/DIAGNOSTIC_SBA_PHASE_4A_3_7_27_GATE_STATUS.md`
  - `docs/DIAGNOSTIC_SBA_PHASE_4A_3_7_28_BATCH_2_PLAN.md`
  - `docs/DIAGNOSTIC_SBA_PHASE_4A_3_7_29_BATCH_2_REPORT.md`

The `fb80f0f` fixed exporter was not imported.

## Imported from `origin/codex/phase-4a3-7-33-remediation-artifacts`

- `docs/CORPUS_REMEDIATION_REPORT.md`
- `docs/CORPUS_REMEDIATION_CHANGELOG.md`
- `docs/CORPUS_REMEDIATION_DATASET.json`
- `tests/test_structured_question_bank_adapter.py`, because its skeleton question-type expectation still applies to the current adapter behavior.

## Discarded or not carried forward

- The fixed exporter from `fb80f0f`; the active exporter remains the dynamic scanner from `origin/main`.
- The separate `batch_2_enrichment_drafts.json` and `batch_2_human_review_records.json` files from `origin/main`; they conflicted with the consolidated private baseline by duplicating source IDs and reducing deterministic eligibility under duplicate-review handling.
- The `--health-report` CLI mode from `fb80f0f`; it was not present on `origin/main` and was not restored in this phase.
- No Gold Bank activation, option shuffle, Tutor/retrieval/self-eval changes, governance changes, or new pedagogical questions were introduced.

## Final active/elegible count

- Source draft records: 20
- Source review records: 20
- Eligible static-demo items: 18
- Active payload items in `frontend/diagnostic-sba/preguntas.json`: 18
- Excluded source IDs: `1`, `13`
- Active/elegible source IDs: `2, 4, 5, 12, 15, 17, 20, 30, 44, 50, 78, 83, 87, 108, 247, 253, 386, 510`

## Active exporter

Active exporter: `tools/question_generation/export_static_demo_questions.py`.

Status: dynamic exporter preserved. It scans `knowledge/question-bank/diagnostic_sba/drafts/` and `knowledge/question-bank/diagnostic_sba/reviews/` for `*_drafts.json` and `*_review_records.json`.

The dry-run result is:

```text
eligible_item_count: 18
validation_errors: 0
```

## Corpus remediation status

The remediation report, changelog, and dataset from Phase 4A.3.7.33 are present in `docs/`. They are integrated as documentation/data artifacts only; no Tutor, retrieval, self-eval, golden baseline, snapshot, governance, or production-bank behavior was changed.

## Tests executed

- `python -m tools.question_generation.export_static_demo_questions --dry-run`
- `python -m unittest discover -s tests -v`

## Remaining risks

- The historical file names `first_5_enrichment_drafts.json` and `first_5_human_review_records.json` now contain the reconciled 20-record private baseline. Tests document this canonical interpretation, but the names remain legacy.
- The static demo payload is larger than the old 3-item active payload; frontend behavior was not manually browser-tested in this phase.
- Gold Bank planning remains blocked until this canonical line is reviewed and accepted.

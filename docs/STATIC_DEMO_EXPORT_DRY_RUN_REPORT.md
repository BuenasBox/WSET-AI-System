# Static Demo Export Dry Run Report

Phase: 4A.3.7.15

Status: dry run only. This report records an in-memory export payload build and
validation. It does not create `frontend/diagnostic-sba/preguntas.json`, modify
frontend files, create a production bank, approve additional drafts, or generate
questions.

## Input Files Used

- `knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json`
- `knowledge/question-bank/diagnostic_sba/reviews/first_5_human_review_records.json`
- Exporter: `tools/question_generation/static_demo_exporter.py`

## Dry Run Method

The dry run builds the static demo export payload in memory with:

```python
build_static_demo_export_payload(drafts, reviews)
```

The result is validated with:

```python
validate_static_demo_export_payload(payload)
```

No output file is written.

## Eligible IDs

The dry run selected exactly three items:

- `2`
- `12`
- `17`

These are the only first-five drafts with:

- `review_status = approved_for_static_demo`;
- `approval_scope = static_demo_only`;
- valid review records;
- validator-valid drafts;
- safe draft governance;
- safe review governance confirmation.

## Excluded IDs And Reasons

- `1` - excluded because the review status is `requires_revision`.
- `13` - excluded because the review status is `requires_revision`.

Excluded drafts are not included as hidden, disabled, or future frontend
entries.

## Payload Shape Summary

The dry-run payload uses Option A from the static demo export contract:

- top-level `export_version = static_demo_export_v0`;
- top-level `static_demo_only = true`;
- `items[]` contains pre-submit render data only;
- `outcomes_by_item_id{}` contains separated post-submit demo outcome data;
- `export_metadata{}` records lineage and dry-run status.

The render payload preserves:

- `item_id`;
- `source_question_id`;
- `draft_id`;
- `review_id`;
- `approval_scope`;
- RA/topic/subtopic/difficulty/learning-objective fields where present;
- stem;
- A-D option text only;
- static-demo governance fields.

The outcome payload preserves post-submit-only data such as:

- `correct_option_id`;
- option diagnostics;
- feedback;
- misconception linkage;
- causal-chain linkage;
- SAT relevance;
- remediation data.

## Leakage Checks

Pre-submit `items[]` was checked for absence of:

- `correct_option_id`;
- `is_correct`;
- `diagnostic_role`;
- `diagnostic_note`;
- `misconception_id`;
- feedback/rationales;
- why-other-options rationales;
- remediation details;
- causal-chain diagnosis details.

Result: no pre-submit correctness, diagnostic-role, rationale, or remediation
leakage was found.

## Governance Checks

Every selected render item confirms:

```json
{
  "training_item_only": true,
  "official_wset_question": false,
  "safe_for_examiner": false,
  "examiner_scoring_allowed": false,
  "static_demo_only": true
}
```

The dry-run payload does not contain production approval, official scoring,
pass/fail, certification-readiness, or examiner-authority language.

## Validation Result

`validate_static_demo_export_payload(payload)` returned no errors.

The payload order is deterministic:

```text
2, 12, 17
```

## Frontend Readiness

The in-memory payload is structurally ready for the next phase to write a
static demo file, subject to that phase explicitly authorizing
`frontend/diagnostic-sba/preguntas.json`.

The current phase does not modify the cockpit prototype. The frontend still has
no external JSON export file.

## No Export Confirmation

Confirmed for this dry run:

- `frontend/diagnostic-sba/preguntas.json` was not created.
- `knowledge/question-bank/diagnostic_sba/preguntas.json` was not created.
- No frontend file was modified.
- No draft file was modified.
- No review file was modified.
- No production bank was created.

## Next Recommended Phase

Phase 4A.3.7.16 - Static Demo Export File.

# Human Review Resolution Contract

Phase: 4A.3.7.10

Status: contract/test-first only. This document does not resolve drafts,
approve items, create approved items, create `preguntas.json`, publish to
frontend, or promote anything to production.

Current draft source:

- `knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json`

Current draft IDs:

- `1`
- `2`
- `12`
- `13`
- `17`

All five Phase 4A.3.7.9 drafts are validator-valid but remain:

- `enrichment_status = defer_for_human_review`
- `human_review.required = true`

## 1. Purpose

The human review resolution layer defines how a reviewer may resolve draft
diagnostic SBA items and, if safe, promote them only to limited non-production
status.

Validator-valid is not the same as approved. A draft can pass structural and
governance validation while still needing human review for source credibility,
wording safety, distractor logic, diagnostic value, and remediation quality.

This contract keeps the promotion path additive and auditable:

- the original draft remains unchanged;
- every decision is recorded in a separate review record;
- no item may become production or official assessment material;
- governance stays training-only and examiner-unsafe.

## 2. Review Statuses

Allowed `review_status` values:

### `pending_human_review`

The draft has not been resolved. It remains blocked from export, pilot use, and
frontend use.

### `approved_for_static_demo`

The draft may later be exported to a static frontend demo only, after a
separate phase explicitly creates that export. It remains training-only,
non-production, non-official, and not suitable for scoring.

### `approved_for_training_pilot`

The draft may later be included in a local/internal training pilot, after a
separate phase explicitly creates pilot output. This is broader than a static
demo but still not production and not examiner scoring.

### `requires_revision`

The draft has potential, but reviewer found issues that must be fixed in a
new additive draft or revision record before approval.

### `rejected`

The draft is not safe or useful enough to proceed. Reasons must be recorded.

### `preserve_only`

The draft or source question should be retained for historical, open-response,
or reference purposes, but should not proceed as a diagnostic SBA item.

## 3. Promotion Rules

A draft may move from `defer_for_human_review` to
`approved_for_static_demo` only if all conditions are true:

- `validate_diagnostic_sba_item(draft)` returns no errors.
- Source support is credible and repo-local.
- No official wording imitation risk remains.
- No examiner authority is present or implied.
- No unsupported rationale remains.
- All option diagnostics are plausible.
- Correct answer support is clear.
- Remediation is grounded.
- Governance flags are safe.
- Reviewer signs off in a review record.

A draft may move to `approved_for_training_pilot` only after satisfying all
static-demo requirements plus any additional pilot-specific checks defined in a
future phase.

A draft may not move to production in this phase.

Forbidden direct transitions:

- draft to production
- draft to official exam use
- draft to examiner scoring
- draft to certification readiness
- draft to frontend export without an additive export phase

## 4. Reviewer Checklist

Every review record must include a checklist with explicit boolean values for:

- `source_support_checked`
- `correct_answer_checked`
- `distractor_logic_checked`
- `diagnostic_roles_checked`
- `misconception_links_checked`
- `causal_chain_links_checked`
- `sat_relevance_checked`
- `rationale_quality_checked`
- `remediation_quality_checked`
- `wording_safety_checked`
- `governance_flags_checked`

Approval statuses require every checklist field to be `true`.

Rejected, revision, preserve-only, and pending records may contain failed
checklist items, but they must record issues or notes explaining the decision.

## 5. Review Record Schema

Every review result must be represented as an additive review record.

Required fields:

- `review_id`
- `source_question_id`
- `draft_id`
- `reviewer`
- `reviewed_at`
- `review_status`
- `risk_before`
- `risk_after`
- `checklist`
- `issues_found`
- `required_changes`
- `approval_scope`
- `governance_confirmation`
- `notes`

Recommended deterministic ID pattern:

```text
review_<source_question_id>_<YYYYMMDD>_<sequence>
```

`reviewed_at` should use an ISO-8601 timestamp when implementation exists.

## 6. Approval Scope

Allowed `approval_scope` values:

- `static_demo_only`
- `local_training_pilot`
- `internal_review_only`

Forbidden scopes:

- `production`
- `official_exam`
- `examiner_scoring`
- `certification_readiness`

Status/scope compatibility:

| Review status | Allowed scopes |
| --- | --- |
| `pending_human_review` | `internal_review_only` |
| `approved_for_static_demo` | `static_demo_only` |
| `approved_for_training_pilot` | `local_training_pilot` |
| `requires_revision` | `internal_review_only` |
| `rejected` | `internal_review_only` |
| `preserve_only` | `internal_review_only` |

## 7. Governance Confirmation

Every review record must confirm:

```json
{
  "safe_for_examiner": false,
  "examiner_scoring_allowed": false,
  "official_wset_question": false,
  "training_item_only": true,
  "uses_llm": false,
  "uses_api": false,
  "uses_embeddings": false,
  "uses_vector_db": false,
  "cloud_services_active": false
}
```

The review record must never upgrade a draft to examiner-safe, official, or
scoring-authorized status.

## 8. Output Policy

Even if a draft is approved, item output remains:

- training-only;
- `safe_for_examiner = false`;
- `examiner_scoring_allowed = false`;
- `official_wset_question = false`;
- non-production unless a future phase creates a limited output.

Approval does not create a question bank. Approval does not create runtime
availability. Approval does not create examiner authority.

## 9. Frontend Policy

Only `approved_for_static_demo` items may later be exported to:

```text
frontend/diagnostic-sba/preguntas.json
```

That export is forbidden in this phase.

If a later phase exports static demo items, the frontend must still display:

```text
PROTOTIPO · ENTRENAMIENTO · NO EVALUACIÓN OFICIAL WSET
```

No frontend may hide or soften the training-only boundary.

## 10. Audit Trail

No draft may be promoted without a review record.

Audit rules:

- Original draft remains unchanged.
- Review result is additive.
- Multiple review records may exist over time.
- Later reviews must not delete earlier decisions.
- A review record must include issues found, required changes, and notes even
  when approval is granted.
- Promotion must be traceable by `source_question_id` and `draft_id`.

## 11. Rejection And Preserve-Only Policy

Reject or preserve if any of these remain unresolved:

- weak source support;
- official wording risk;
- misleading rationale;
- ambiguous correct answer;
- unsupported diagnostic role;
- unsupported remediation;
- governance uncertainty;
- official/examiner/certification implication;
- item is better suited for open-response or reference-only use.

`preserve_only` should be preferred over `rejected` when the artifact remains
useful as source evidence, future open-response material, or audit history.

## 12. Test Contract Expectations

Contract tests should use in-memory review records only and verify:

- valid review record schema accepted;
- missing reviewer fails;
- missing checklist fails;
- official/examiner scope rejected;
- production scope rejected;
- `approved_for_static_demo` requires all checklist items true;
- rejected review may have failed checklist;
- governance confirmation required;
- approval does not mutate draft;
- approval remains training-only;
- review status enum enforced;
- approval scope enum enforced.

## 13. Next Phase

Phase 4A.3.7.11 - Human Review Record Skeleton.

The next phase should implement pure helpers for review-record validation and
additive review-record construction. It should not approve drafts, export
frontend data, or create production items.

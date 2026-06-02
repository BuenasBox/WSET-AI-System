# Static Demo Export Contract

Phase: 4A.3.7.13

Status: contract-first only. This document does not create `preguntas.json`,
modify the frontend, create a production bank, approve additional drafts, or
export any diagnostic SBA item.

Future export target:

```text
frontend/diagnostic-sba/preguntas.json
```

That file is forbidden in this phase.

## 1. Purpose

The static demo export is only for the isolated diagnostic SBA cockpit
prototype.

It is:

- a local static demo artifact;
- training-only;
- non-production;
- non-official;
- separate from the live tutoring, retrieval, learner-state, and self-eval
  systems.

It is not:

- a live backend;
- an official WSET question bank;
- an official WSET scoring system;
- a certification-readiness signal;
- an examiner-authorized assessment;
- a learner-state update path.

## 2. Export Eligibility

An item may be exported only when every condition is true:

- the source draft is validator-valid;
- the draft has exactly one matching human-review record;
- the review record validates with `validate_review_record()`;
- `review_status = approved_for_static_demo`;
- `approval_scope = static_demo_only`;
- draft governance is safe;
- review governance confirmation is safe;
- no official wording risk remains;
- no examiner authority, official score, pass/fail, or certification-readiness
  language is present.

The current Phase 4A.3.7.12 review outcomes make only drafts `2`, `12`, and
`17` eligible in principle. Eligibility still must be revalidated by the future
exporter at export time.

## 3. Exclusion Rules

The future exporter must exclude any item with:

- `review_status = requires_revision`;
- `review_status = rejected`;
- `review_status = preserve_only`;
- missing review record;
- invalid review record;
- unsafe draft governance;
- unsafe review governance confirmation;
- official wording risk;
- failed draft validator;
- forbidden scope such as `production`, `official_exam`,
  `examiner_scoring`, or `certification_readiness`.

Excluded items must not appear in the static demo output, even as disabled or
hidden frontend entries.

## 4. Output Shape

The frontend pre-submit payload must not expose:

- `is_correct`;
- `correct_option_id`;
- `diagnostic_role`;
- correct rationale;
- why other options are wrong;
- misconception diagnosis;
- causal-chain diagnosis;
- remediation conclusion.

Those fields belong only to a post-submit outcome payload, or to a hidden local
demo outcome map that is clearly separated from pre-submit render data.

### Recommended Format: Option A, Split Payloads

Option A is the required recommendation for the next phase because it makes
pre-submit leakage easier to test.

```json
{
  "export_version": "static_demo_export_v0",
  "exported_at": "2026-06-02T00:00:00Z",
  "disclaimer": "PROTOTIPO · ENTRENAMIENTO · NO EVALUACIÓN OFICIAL WSET",
  "items": [
    {
      "item_id": "draft_diag_sba_structured_2",
      "source_question_id": "2",
      "draft_id": "draft_diag_sba_structured_2",
      "review_id": "review_2_20260602_001",
      "approval_scope": "static_demo_only",
      "static_demo_only": true,
      "training_item_only": true,
      "official_wset_question": false,
      "safe_for_examiner": false,
      "examiner_scoring_allowed": false,
      "question": {
        "stem": "...",
        "question_type": "single_best_answer"
      },
      "options": [
        {"option_id": "A", "option_text": "..."},
        {"option_id": "B", "option_text": "..."},
        {"option_id": "C", "option_text": "..."},
        {"option_id": "D", "option_text": "..."}
      ]
    }
  ],
  "outcomes_by_item_id": {
    "draft_diag_sba_structured_2": {
      "correct_option_id": "C",
      "feedback": {
        "correct_rationale": "...",
        "why_other_options_are_wrong": {},
        "remediation_recommendation": "..."
      },
      "diagnostic_metadata": {}
    }
  }
}
```

`items[]` is the only payload the frontend may use before a learner submits an
answer. `outcomes_by_item_id` may be consulted only after submit in the static
demo.

### Allowed Alternative: Option B, Single Local Demo Payload

Option B is allowed only if the separation remains explicit:

```json
{
  "render_payload": {},
  "demo_outcome_payload": {}
}
```

The future exporter must still prove that `render_payload` has no correctness,
diagnostic-role, causal-chain, misconception, rationale, or remediation
leakage.

## 5. Required Governance Fields

Every exported item must include:

```json
{
  "training_item_only": true,
  "official_wset_question": false,
  "safe_for_examiner": false,
  "examiner_scoring_allowed": false,
  "static_demo_only": true
}
```

The export must not add or imply production status.

## 6. Frontend Policy

The frontend must:

- render only pre-submit data before answer confirmation;
- reveal outcome data only after submit;
- display this disclaimer:

```text
PROTOTIPO · ENTRENAMIENTO · NO EVALUACIÓN OFICIAL WSET
```

The frontend must never claim:

- LES update;
- official score;
- pass/fail;
- certification readiness;
- examiner authority.

## 7. Audit Trail

Each exported item must preserve:

- `source_question_id`;
- `draft_id`;
- `review_id`;
- `approval_scope`;
- `exported_at`;
- `export_version`.

Ordering must be deterministic, sorted by numeric `source_question_id` when
possible.

## 8. Future Exporter Validation Requirements

The future exporter must validate:

- every exported item has an approved review;
- no excluded review status is exported;
- no pre-submit leakage of correct answer appears;
- no pre-submit leakage of diagnostic roles appears;
- outcome payload is separated from render payload;
- no unsafe governance appears;
- ordering is deterministic;
- drafts and review records are not mutated;
- `frontend/diagnostic-sba/preguntas.json` is created only in the explicit
  exporter phase.

## 9. Current Phase Boundary

Phase 4A.3.7.13 creates this contract and contract tests only.

It does not:

- create `frontend/diagnostic-sba/preguntas.json`;
- modify frontend files;
- create an export script;
- create a production bank;
- approve additional drafts;
- modify existing drafts;
- modify existing review records;
- generate questions.

## 10. Next Phase

Phase 4A.3.7.14 - Static Demo Exporter Skeleton.

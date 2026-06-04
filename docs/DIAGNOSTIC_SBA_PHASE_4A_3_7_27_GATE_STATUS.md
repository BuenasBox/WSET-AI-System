# Diagnostic SBA Phase 4A.3.7.27 Gate Status

Date: 2026-06-03

## Closed SBA Commit

Phase 4A.3.7.26 is closed at:

`f78f78572e79295e471d930408971a61ebf7a98e`

Commit subject:

`test(diagnostic-sba): canonicalize contract and add expansion readiness gate`

The commit scope is Diagnostic SBA contract/export/frontend/test documentation:

- `question_type` canonicalized to `diagnostic_single_best_answer`
- legacy `single_best_answer` explicitly rejected
- schema, validator, exporter, drafts, fixtures, frontend static payload, tests, and docs aligned
- export validation and health report checks hardened

The commit did not touch `tools/self_eval`, `tools/tutor`, or `tools/retrieval`.

## Worktree Hygiene

Initial gate hygiene found one pending runtime/debug artifact:

`knowledge/retrieval-sandbox/orchestrator_context_retrieval_debug.csv`

The diff was limited to retrieval debug ranking output for the question "How does cool climate affect acidity?". It was classified as runtime/debug output, unrelated to Diagnostic SBA, and restored with `git restore`.

After the slow self-eval triage run, additional generated self-eval runtime files appeared under `knowledge/self-eval/`, `knowledge/nazareth/self_eval_feedback.json`, and the same retrieval debug CSV. These were also restored. No SBA commit content was reverted.

Current hygiene decision: worktree must be clean before Phase 4A.3.7.27 starts.

## Verification Evidence

Previously recorded Phase 4A.3.7.26 verification:

- SBA/export focal suite: 184 OK
- full suite: 1339 OK, 9 skipped
- export dry-run: `eligible_item_count` 3, `validation_errors` 0
- health report: `validation_error_count` 0, `governance_violations` []

Slow golden command run during this gate:

```powershell
$env:RUN_SLOW_TESTS=1; python -m unittest tests.test_golden_self_eval -v
```

Result:

- 7 tests run
- 3 OK
- 4 failed

Passing checks:

- `test_governance_flags_unchanged`
- `test_no_retrieval_gaps`
- `test_no_sat_weaknesses`

Failing checks:

- `test_no_failure_labels`
- `test_no_new_retrieval_weaknesses`
- `test_known_retrieval_weakness_not_worse`
- `test_no_new_missing_causal_chains`

Live metrics from the failed run:

- `failure_labels`: `{"shallow_retrieval": 13, "shallow_reasoning": 12, "missing_causal_link": 1}`
- `retrieval_weaknesses`: `missing_keyword_support` increased from golden 5 to live 17
- new retrieval weakness types: `shallow_retrieval`, `missing_causal_link_support`
- new missing causal chain: `cause -> mechanism -> effect`

Affected generated attempt ids:

`1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 15, 16, 19, 20, 21, 22, 23, 24, 25`

## Failure Classification

Classification: separate Tutor/retrieval self-eval gate blocker, not a Diagnostic SBA blocker by code ownership.

Evidence:

- The failing slow test runs `tools.self_eval.question_runner.run_self_eval(limit=25)` and compares live Tutor/retrieval/comparator output to `knowledge/self-eval/golden_brutal_output.json`.
- The golden baseline is strictness `hard` and expects no failure labels plus only 5 `missing_keyword_support` weaknesses.
- The live run produces Tutor/retrieval diagnostic labels across theory questions, not Diagnostic SBA export/validation labels.
- The closed SBA commit did not modify `tools/self_eval`, `tools/tutor`, `tools/retrieval`, or `knowledge/self-eval/golden_brutal_output.json`.
- Governance, retrieval-gap, and SAT-specific slow golden checks still pass.

Not classified as:

- Diagnostic SBA regression
- export contract regression
- frontend static payload regression
- governance regression
- SAT regression

Open classification requiring a separate phase:

- whether the slow golden baseline is obsolete
- whether the comparator strictness is now misaligned with the current Tutor/retrieval state
- whether this is a real Tutor/retrieval regression introduced before Phase 4A.3.7.26
- whether runtime learner/self-eval state contributes to the live metrics

No golden baseline was regenerated, no snapshots were updated, and no Tutor/retrieval behavior was modified in this gate.

Known blocker ID:

`KNOWN_BLOCKER_SLOW_GOLDEN_TUTOR_RETRIEVAL_2026_06_03`

Owning gate policy:

`docs/GOVERNANCE_DOMAIN_GATES.md`

## Gate Decision

Decision: Phase 4A.3.7.27 is unblocked only for private Diagnostic SBA dataset expansion.

Reason: the red slow golden condition is classified as an unrelated
Tutor/retrieval/self-eval known blocker under the domain-gate policy. It remains
blocking for Tutor/retrieval and for publication paths that depend on integrated
Tutor/retrieval quality, but it does not block private Diagnostic SBA expansion
when SBA/global gates are green and no Tutor/retrieval files or behavior are
changed.

## Conditions To Unblock

Phase 4A.3.7.27 private Diagnostic SBA expansion may begin only when all of the
following are true:

- SBA/export focal suite is green;
- full `python -m unittest discover -s tests -v` suite is green;
- `python -m tools.question_generation.export_static_demo_questions --dry-run`
  reports `validation_errors: 0`;
- `python -m tools.question_generation.export_static_demo_questions --health-report`
  reports `validation_error_count: 0` and no governance violations;
- worktree is clean;
- no Tutor/retrieval/self-eval/golden/snapshot files or behavior are changed;
- the slow golden failure remains documented as
  `KNOWN_BLOCKER_SLOW_GOLDEN_TUTOR_RETRIEVAL_2026_06_03`.

Tutor/retrieval remains blocked until one of the following is explicitly
completed and documented:

1. Slow golden is made green through an authorized Tutor/retrieval/self-eval remediation phase without changing Diagnostic SBA data.
2. The slow golden baseline is formally declared obsolete and replaced through an explicitly authorized baseline regeneration phase.
3. A separate governance decision changes the Tutor/retrieval slow golden contract.

Until the Tutor/retrieval blocker is resolved:

- do not modify Tutor/retrieval logic as part of SBA expansion
- do not regenerate golden baselines or snapshots without explicit authorization
- do not claim Tutor/retrieval slow golden health
- do not use this decision as public publication readiness

Allowed continuation scope:

- private Diagnostic SBA dataset expansion only;
- validator/export/health-report hardening directly related to Diagnostic SBA;
- documentation of SBA readiness and known blockers.

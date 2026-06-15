# Roadmap Phase 4A

> **STATUS: HISTORICAL**
>
> **DO NOT USE AS CURRENT PROJECT STATE**
>
> Current pending work is recorded in [PROJECT_STATE_RECONCILIATION.md](PROJECT_STATE_RECONCILIATION.md).

Date: 2026-06-01

Phase 4A is the diagnostic single-best-answer and structured question-bank workstream. It is governance-first: contracts, schemas, validators, fixtures, and review gates come before any connected runtime.

## Status Summary

- COMPLETE phases: 21
- IN PROGRESS: Phase META.1 - project bootstrap package
- NEXT: Phase 4A.3.7.11 - implement human review resolution

## Phase List

| Phase | Status | Description |
|---|---|---|
| 4A.0 | COMPLETE | Audited whether single-best-answer generation is feasible under deterministic, source-grounded, non-examiner governance constraints. |
| 4A.1 | COMPLETE | Defined the Diagnostic SBA governance contract and permanent authority boundaries. |
| 4A.2 | COMPLETE | Added the Diagnostic SBA item schema for training-only single-best-answer items. |
| 4A.3 | COMPLETE | Added the deterministic Diagnostic SBA item validator. |
| 4A.3.5 | COMPLETE | Added the diagnostic outcome model schema for attempt interpretation. |
| 4A.3.6 | COMPLETE | Inventoried Markdown question-bank sources for structured conversion and enrichment planning. |
| 4A.3.6.5 | COMPLETE | Audited knowledge assets and cognitive inventory counts. |
| 4A.3.6.6 | COMPLETE | Audited knowledge-map manifest reconciliation requirements. |
| 4A.3.6.7 | COMPLETE | Defined the knowledge-map manifest regeneration contract. |
| 4A.3.6.8 | COMPLETE | Added contract tests for knowledge-map manifest regeneration. |
| 4A.3.7 | COMPLETE | Audited structured question-bank compatibility for diagnostic SBA enrichment. |
| 4A.3.7.1 | COMPLETE | Defined the structured question-bank adapter contract. |
| 4A.3.7.2 | COMPLETE | Added structured question-bank adapter contract tests. |
| 4A.3.7.3 | COMPLETE | Added the structured question-bank adapter skeleton. |
| 4A.3.7.4 | COMPLETE | Validated the structured adapter against pilot source items. |
| 4A.3.7.5 | COMPLETE | Defined the pilot enrichment contract. |
| 4A.3.7.6 | COMPLETE | Added the structured question-bank enrichment skeleton. |
| 4A.3.7.7 | COMPLETE | Added diagnostic SBA enrichment fixtures. |
| 4A.3.7.8 | COMPLETE | Validated the first five pilot enrichment candidates. |
| 4A.3.7.9 | COMPLETE | Added the first five diagnostic SBA enrichment drafts. |
| 4A.3.7.10 | COMPLETE | Added human review resolution contract tests. |
| META.1 | IN PROGRESS | Create permanent bootstrap documentation for future agents and human contributors. |
| 4A.3.7.11 | NEXT | Implement the human review resolution flow described by the contract tests and governance document. |

## Current Exit Criteria For NEXT

Phase 4A.3.7.11 should not be considered complete until:

- human review resolution is implemented deterministically
- generated/enriched drafts remain training-only
- unsafe governance fields fail closed
- approved/rejected/revision-required states are explicit
- no learner-state, retrieval, Tutor, or frontend runtime behavior changes unless explicitly authorized
- `python -m unittest discover -s tests -v` is green in a permission-clean local environment

## Verification Notes

The most recent attempted full test run on 2026-06-01 was blocked by local permission errors, not test assertion failures. Before using a new test count as canonical, resolve local write/rename permissions for:

- `knowledge/config/domain_expansions.json`
- `knowledge/retrieval-sandbox/orchestrator_context_retrieval.json`

The latest known green status before this bootstrap phase remains the dashboard/audit baseline: 1,107 tests and 35 snapshots.

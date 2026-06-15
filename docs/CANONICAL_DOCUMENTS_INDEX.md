# Canonical Documents Index

> **STATUS: CANONICAL**
>
> **LAST RECONCILED: 2026-06-06**

This is the entry point for current project documentation. Documents not listed
here may remain useful as design history, audit evidence, contracts, or phase
records, but they must not override executable evidence or the current-state
reconciliation.

Precedence:

1. Code, versioned data, tests, and Git history.
2. [Project State Reconciliation](PROJECT_STATE_RECONCILIATION.md).
3. The canonical component documents listed below.
4. Historical reports, audits, plans, and roadmaps.

## Current State

- [Project State Reconciliation](PROJECT_STATE_RECONCILIATION.md) - canonical
  repository state, operational counts, verification baseline, and pending work.

## Project Governance

- [Diagnostic SBA Governance Contract](DIAGNOSTIC_SBA_GOVERNANCE_CONTRACT.md) -
  training-only authority boundary for diagnostic SBA.
- [Open Response Lab Contract](OPEN_RESPONSE_LAB_CONTRACT.md) - private,
  formative Open Response boundary; public activation remains off.
- [Strategic Planner Contract](STRATEGIC_PLANNER_CONTRACT.md) - planner signal
  ownership and authority boundaries.
- [Planner Influence Boundary](PLANNER_INFLUENCE_BOUNDARY.md) - allowed and
  forbidden planner influence directions.

The immutable runtime flags remain defined and enforced in
`tools/constants.py`. No documentation may authorize examiner scoring, LLMs,
APIs, embeddings, vector databases, or cloud services in the active cognitive
loop.

## Master Bank

- [Master Bank Review and Inactive Resolution](PHASE_4A_3_8_5_7_MASTER_BANK_REVIEW_INACTIVE_RESOLUTION.md) -
  canonical resolution of the review and inactive eligibility backlog.
- [Master Bank Eligibility and Suitability Integration](PHASE_4A_3_8_5_6_MASTER_BANK_ELIGIBILITY_SUITABILITY_INTEGRATION.md) -
  operational eligibility integration.
- [Full Master Bank Utilization Engine](PHASE_4A_3_8_5_FULL_MASTER_BANK_UTILIZATION_ENGINE.md) -
  deterministic private session composition architecture.

Current reconciled counts are 616 Master Bank records, 589 operational SBA
records, and 27 Open Response candidates.

## Open Response

- [Runtime Consumers and Open Response Evaluator](PHASE_4A_3_8_7_RUNTIME_CONSUMERS.md) -
  implemented misconception, causal-chain, WWJ remediation, and evaluator
  runtimes.
- [Open Response Lab Contract](OPEN_RESPONSE_LAB_CONTRACT.md) - activation and
  governance boundary.

The evaluator exists as private deterministic infrastructure. The Open Response
frontend and public activation remain off.

## Learning Runtime

- [Cognitive Map Learning Event Runtime](PHASE_4A_3_9_0_COGNITIVE_MAP_LEARNING_EVENT_RUNTIME.md) -
  current attempt-to-event, cognitive-map, LES, and next-session signal flow.
- [Adaptive Loop Finalization](PHASE_4A_3_9_2_ADAPTIVE_LOOP_FINALIZATION.md) -
  signal consumption, coordinated persistence, and next-session composition.
- [Learning Links Contract](LEARNING_LINKS_CONTRACT.md) - governed item-level
  links for misconception and causal-chain targeting.

## Dashboard

- [Frontend Source of Truth Reconciliation](FRONTEND_SOURCE_OF_TRUTH_RECONCILIATION.md) -
  production repository, deployment source, operational domain, and frontend
  path ownership.

Production is published from `BuenasBox/epistemiclab-dashboard` on `main`.
`WSET-AI-System/origin/gh-pages` is historical unless explicitly reactivated.

## Frontend

- Canonical development source: `frontend/architecture-dashboard/`.
- Active Diagnostic SBA editing source: `frontend/diagnostic-sba/`.
- Experimental surfaces are not production evidence.

See [Frontend Source of Truth Reconciliation](FRONTEND_SOURCE_OF_TRUTH_RECONCILIATION.md)
for the promotion path and production boundary.

## Roadmap

There is no standalone canonical roadmap at this reconciliation point. Use the
`Pendientes reales` section of
[Project State Reconciliation](PROJECT_STATE_RECONCILIATION.md) for current
next-work boundaries. Older roadmap documents are historical planning records.

## Historical Entry Points

The following files are retained for project history and must not be used as
current-state authorities:

- [Project Current State](PROJECT_CURRENT_STATE.md)
- [Codex Bootstrap Context](CODEX_BOOTSTRAP_CONTEXT.md)
- [Roadmap Phase 4A](ROADMAP_PHASE_4A.md)
- [Legacy Documentation Index](INDEX.md)
- [Deployment Domain Plan](DEPLOYMENT_DOMAIN.md)

No historical document is deleted by documentation canonicalization.

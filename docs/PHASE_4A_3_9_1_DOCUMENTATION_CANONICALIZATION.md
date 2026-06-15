# Phase 4A.3.9.1 - Documentation Canonicalization

> **STATUS: CANONICAL**
>
> **LAST RECONCILED: 2026-06-06**

## Scope

Documentation-only maintenance phase. No code, tests, knowledge data, runtime
behavior, frontend assets, deployment configuration, or governance flags were
changed.

## Changes

- Marked five current-state and component documents as canonical.
- Marked five superseded state, bootstrap, roadmap, index, and deployment
  documents as historical.
- Added `docs/CANONICAL_DOCUMENTS_INDEX.md` as the current documentation entry
  point.
- Preserved all historical documents and their original content.

## Canonical Documents

- `PROJECT_STATE_RECONCILIATION.md`
- `PHASE_4A_3_9_0_COGNITIVE_MAP_LEARNING_EVENT_RUNTIME.md`
- `PHASE_4A_3_8_7_RUNTIME_CONSUMERS.md`
- `PHASE_4A_3_8_5_7_MASTER_BANK_REVIEW_INACTIVE_RESOLUTION.md`
- `FRONTEND_SOURCE_OF_TRUTH_RECONCILIATION.md`
- `CANONICAL_DOCUMENTS_INDEX.md`

## Historical Documents

- `PROJECT_CURRENT_STATE.md`
- `CODEX_BOOTSTRAP_CONTEXT.md`
- `ROADMAP_PHASE_4A.md`
- `INDEX.md`
- `DEPLOYMENT_DOMAIN.md`

## Deferred

`docs/SYSTEM_CAPABILITIES_MATRIX.md` is intentionally deferred until the
remaining pedagogical runtime work is reconciled. Creating it earlier would
risk turning an incomplete capability snapshot into a new source of drift.

## Verification

This phase requires documentation checks only:

- all designated canonical files contain the canonical header;
- all designated historical files contain the historical warning;
- all links in the canonical index resolve to repository files;
- no files outside `docs/` are modified by this phase.

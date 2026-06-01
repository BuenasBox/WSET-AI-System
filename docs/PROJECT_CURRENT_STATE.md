# Project Current State

Date: 2026-06-01

## Project Identity

WSET-AI-System is a deterministic, local, governance-constrained WSET Level 3 tutoring architecture.

It is retrieval-first and neuro-symbolic: source retrieval, learner-state signals, misconception objects, SAT reasoning, causal-chain structures, and governance checks come before answer rendering.

The system is a tutor, not an examiner. It may support training, diagnosis, remediation, and internal readiness signals, but it must not claim official WSET scoring authority, examiner authority, certification readiness, or pass/fail judgment.

## Architectural Principles

Immutable governance principles:

- `safe_for_examiner = false`
- `examiner_scoring_allowed = false`
- no LLM runtime dependency
- no API runtime dependency
- no embeddings
- no vector DB
- no cloud dependency in the active loop

Active loop:

- deterministic retrieval over local assets
- deterministic misconception pre-pass
- deterministic SAT observation and quality reasoning
- deterministic causal-chain matching and rendering
- deterministic Tutor answer construction
- local session staging and telemetry only

## Current Knowledge Assets

Current repository scan:

- Total knowledge files: 2,211
- Knowledge JSON files: 1,276
- Knowledge Markdown files: 712
- Knowledge JSONL files: 38
- Knowledge TXT files: 67

Question bank:

- Structured WSET3 questions: 616
- Theory questions: 595
- Short-answer questions: 21
- Basic SBA candidates recorded by dashboard state: 591
- Strict SBA candidates recorded by dashboard state: 525
- Clean pilot SBA candidates recorded by dashboard state: 520
- Diagnostic SBA draft bank files: 1

Knowledge map:

- Total knowledge-map files: 100
- Causal-chain JSON nodes: 32
- Misconception JSON nodes: 20
- Concept JSON nodes: 8
- Relationship JSON nodes: 10
- Service JSON nodes: 2
- Tasting JSON nodes: 2
- Topic JSON nodes: 2
- Wine-law JSON nodes: 2
- Manifests and schemas: 8 files

Official WSET extracted corpus:

- Official WSET files: 84
- Official WSET Markdown files: 53
- Official chunk artifact: `knowledge/official-wset/study-guide/official-chunks/official_wset_chunks.jsonl`

Wine With Jimmy corpus:

- Wine With Jimmy related files: 689
- Clean Markdown transcripts: 30
- Raw JSON transcript files: 41
- Metadata JSON files: 377
- Chunk-ready JSONL files: 30
- Golden tutor candidate artifact: `knowledge/wine-with-jimmy/manual-import/reports/golden_tutor_chunk_candidates.jsonl`

## Current Test Status

Latest known green project status from repository memory and dashboard audit:

- Tests: 1,107 passing/skipped at the Phase 4A frontend/state audit point.
- Tutor snapshots: 35 green.
- Golden self-eval baseline: no failure labels, no retrieval gaps, no SAT weaknesses.
- Governance status: no LLM dependency, no vector DB dependency, no cloud runtime dependency, no examiner authority.

Verification attempt on 2026-06-01:

- `python -m unittest discover -s tests -v` discovered and ran 1,186 tests.
- Result: 1,175 passed, 8 skipped, 3 errors.
- Errors were local filesystem permission errors, not assertion failures:
  - rename blocked for `knowledge/config/domain_expansions.json`
  - writes blocked for `knowledge/retrieval-sandbox/orchestrator_context_retrieval.json`
- Treat this as a local permission issue to resolve before using the run as the new green baseline.

## Current Frontend Status

Architecture dashboard:

- Source of truth: `frontend/architecture-dashboard/`
- Public deployment repo: `epistemiclab-dashboard`
- Live URL recorded in audit: `https://epistemiclab.dpdns.org`
- Current dashboard state file is stale relative to HEAD and should be regenerated after Phase META.1.

Diagnostic SBA cockpit:

- Static prototype exists at `frontend/diagnostic-sba/index.html`.
- Frontend/backend contract exists at `docs/DIAGNOSTIC_SBA_COCKPIT_CONTRACT.md`.
- The cockpit is currently a prototype only: no backend connection, no Supabase, no LES writes, no retrieval changes, no cognitive runtime changes.
- The frontend must render backend diagnostic outcomes in future phases; it must not invent correctness, misconception diagnosis, confidence alignment, timing band, or remediation conclusions.

## Current Diagnostic SBA Status

Completed Phase 4A work:

- 4A.0: Single-best-answer generation feasibility audit.
- 4A.1: Diagnostic SBA governance contract.
- 4A.2: Diagnostic SBA item schema.
- 4A.3: Diagnostic SBA item validator.
- 4A.3.5: Diagnostic outcome model schema.
- 4A.3.6: Markdown question-bank inventory.
- 4A.3.6.5: Knowledge asset and cognitive inventory audit.
- 4A.3.6.6: Knowledge-map manifest reconciliation audit.
- 4A.3.6.7: Knowledge-map manifest regeneration contract.
- 4A.3.6.8: Knowledge-map manifest regeneration contract tests.
- 4A.3.7: Structured question-bank compatibility audit.
- 4A.3.7.1: Structured question-bank adapter contract.
- 4A.3.7.2: Structured question-bank adapter contract tests.
- 4A.3.7.3: Structured question-bank adapter skeleton.
- 4A.3.7.4: Pilot adapter validation.
- 4A.3.7.5: Pilot enrichment contract.
- 4A.3.7.6: Structured question-bank enrichment skeleton.
- 4A.3.7.7: Diagnostic SBA enrichment fixtures.
- 4A.3.7.8: First five pilot enrichment candidates validated.
- 4A.3.7.9: First five diagnostic SBA enrichment drafts.
- 4A.3.7.10: Human review resolution contract tests.

Current phase:

- META.1: Project bootstrap context package.

## Current Risks

- The latest full test run is blocked by local Windows/OneDrive permission errors; resolve file rename/write permissions before treating 1,186 tests as a new green baseline.
- Dashboard state is stale relative to HEAD and should be regenerated and synced to the public dashboard repo.
- Diagnostic SBA remains contract/prototype oriented; it is not yet a connected backend runtime.
- Human review resolution is not yet implemented beyond contract tests.
- Planner causal-chain influence remains intentionally gated off until stronger evidence shows value beyond organic retrieval.
- Machine-local cognitive artifacts under `knowledge/nazareth/`, `knowledge/self-eval/reports/`, `knowledge/self-eval/attempts/`, `knowledge/retrieval-sandbox/`, and `*.jsonl` runtime traces must not be committed unless explicitly versioned config/baseline files.

## Current Next Phase

Next recommended implementation phase:

- Phase 4A.3.7.11: Implement the human review resolution flow defined by `docs/HUMAN_REVIEW_RESOLUTION_CONTRACT.md`.

Before implementation, read:

- `CLAUDE.md`
- `docs/PROJECT_CURRENT_STATE.md`
- `docs/ROADMAP_PHASE_4A.md`
- `docs/HUMAN_REVIEW_RESOLUTION_CONTRACT.md`

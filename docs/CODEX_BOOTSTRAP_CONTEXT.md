# Codex Bootstrap Context

> **STATUS: HISTORICAL**
>
> **DO NOT USE AS CURRENT PROJECT STATE**
>
> Start with [CANONICAL_DOCUMENTS_INDEX.md](CANONICAL_DOCUMENTS_INDEX.md).

This file is written for a future coding agent or human contributor who has no access to historical chats.

## What This Project Is

WSET-AI-System is a deterministic, local, governance-constrained WSET Level 3 tutoring system.

It is a retrieval-first, neuro-symbolic tutoring substrate. It combines local source retrieval, structured learner state, misconception objects, causal-chain reasoning, SAT reasoning, diagnostic question-bank tooling, and deterministic Tutor rendering.

It is designed for training and remediation. It is a tutor, not an examiner.

## What It Is Not

This project is not:

- an official WSET examiner
- an official scoring system
- a certification predictor
- a generative-first chatbot
- an LLM runtime application
- an embeddings or vector-search system
- a cloud runtime system
- a frontend-first product

Do not add hidden inference services, API calls, embeddings, vector databases, cloud services, official scoring language, or examiner authority.

## Governance Rules

These invariants are immutable:

```text
safe_for_examiner = false
examiner_scoring_allowed = false
uses_llm = false
uses_api = false
uses_embeddings = false
uses_vector_db = false
cloud_services_active = false
```

Rules:

- Never set `safe_for_examiner` to true.
- Never set `examiner_scoring_allowed` to true.
- Never imply official WSET scoring, examiner judgment, certification, pass/fail, or official readiness.
- Fail closed if any input artifact contains contradictory governance flags.
- Keep outputs deterministic and reproducible.
- Do not introduce runtime dependencies on external services.

## Architecture Rules

Core flow:

1. Orchestrator loads or creates learner state.
2. Misconception pre-pass checks query signals.
3. Retrieval sandbox performs deterministic local retrieval.
4. Causal-chain and SAT structures are threaded into context.
5. Tutor answer builder renders deterministic markdown.
6. Session staging and telemetry are written locally.

Rules:

- Do not import `tools.orchestrator` from leaf modules.
- Do not refactor behavior-dense Tutor code without snapshot protection.
- Keep planner influence behind explicit gates unless a phase authorizes activation.
- Keep strategic planner outputs observable before making them influential.
- Keep local cognitive artifacts out of public deployment and commits unless they are explicit baselines/config.

## Retrieval Rules

Active engine:

- `tools/retrieval/tutor_retrieval_sandbox.py`

Retrieval is deterministic and local. It loads local chunks, official extracted chunks, golden tutor chunks, dictionary terms, and knowledge-map nodes.

Rules:

- Query hints such as `causal_chain:<id>` must be parsed before lexical scoring.
- Planner causal-chain injection must remain gated unless a later phase explicitly activates it.
- Do not add embeddings, vector DBs, web search, cloud retrieval, or LLM reranking.
- Preserve source diversity and governance filtering.
- Preserve no-op behavior for hint-free queries unless a phase intentionally changes it and snapshots verify the change.

## Question Bank Rules

Current structured source:

- `knowledge/question-bank/structured/wset3_questions.json`

Current count:

- 616 structured questions
- 595 theory questions
- 21 short-answer questions

Rules:

- Do not commit binary question-bank sources such as XLSX, PDF, DOCX, or PPTX.
- Use deterministic converters only.
- Protect open questions: do not export hidden correct answers or explanations for open/free-response items unless the phase explicitly authorizes a training artifact.
- Generated or enriched SBA items must be training-only, source-grounded, and governance-clean.
- Every diagnostic SBA item must contain exactly four options and exactly one correct option.
- Every diagnostic distractor must have diagnostic metadata.

## Diagnostic SBA Rules

Diagnostic SBA is a training diagnostic system, not an exam simulator.

Authoritative contracts:

- `docs/DIAGNOSTIC_SBA_GOVERNANCE_CONTRACT.md`
- `docs/DIAGNOSTIC_SBA_ITEM_SCHEMA.md`
- `docs/DIAGNOSTIC_OUTCOME_MODEL.md`
- `docs/DIAGNOSTIC_SBA_COCKPIT_CONTRACT.md`
- `docs/HUMAN_REVIEW_RESOLUTION_CONTRACT.md`

Rules:

- Items must be training-only and not official WSET questions.
- Items must be paraphrased and source-grounded.
- Outcomes must not contain pass/fail, marks, examiner scoring, or official readiness claims.
- Human review is required for enriched drafts until the resolution flow validates otherwise.
- The frontend must not derive correctness, misconception diagnosis, timing band, confidence alignment, or remediation conclusions.

## Frontend Rules

Current frontend surfaces:

- `frontend/architecture-dashboard/`
- `frontend/diagnostic-sba/`

Rules:

- Frontend is not allowed to become the cognitive authority.
- Diagnostic SBA cockpit must render backend-provided diagnostic outcomes, not invent them.
- No frontend may expose learner-state files, local cognitive artifacts, self-eval attempts, retrieval-sandbox reports, or private machine-local traces.
- Dashboard state updates in the private repo must be manually synced to the separate public dashboard repo when appropriate.
- Keep all governance disclaimers visible where diagnostic behavior appears.

## Known Active Workstreams

- Phase META.1: permanent project bootstrap package.
- Phase 4A.3.7.x: structured question-bank enrichment toward diagnostic SBA items.
- Human review resolution for the first five diagnostic SBA enrichment drafts.
- Diagnostic SBA cockpit migration path from static prototype to connected local backend.
- Architecture dashboard state refresh and public dashboard sync.
- Planner causal-chain influence remains experimental and gated off.

## How To Determine Next Phase

1. Read `CLAUDE.md`.
2. Read `docs/PROJECT_CURRENT_STATE.md`.
3. Read `docs/ROADMAP_PHASE_4A.md`.
4. Check `git log --oneline -30` for the latest phase commit.
5. Check `git status --short` and do not overwrite unrelated local changes.
6. If the latest phase is `4A.3.7.10`, the next recommended implementation phase is `4A.3.7.11`: implement human review resolution.
7. If newer phase docs exist, trust the newest committed contract plus current tests over this bootstrap file.

## Mandatory Files To Read First

Read these before changing code:

- `CLAUDE.md`
- `docs/PROJECT_CURRENT_STATE.md`
- `docs/ROADMAP_PHASE_4A.md`

For Diagnostic SBA work, also read:

- `docs/DIAGNOSTIC_SBA_GOVERNANCE_CONTRACT.md`
- `docs/DIAGNOSTIC_SBA_ITEM_SCHEMA.md`
- `docs/DIAGNOSTIC_OUTCOME_MODEL.md`
- `docs/DIAGNOSTIC_SBA_COCKPIT_CONTRACT.md`
- `docs/HUMAN_REVIEW_RESOLUTION_CONTRACT.md`

For planner/retrieval influence work, also read:

- `docs/STRATEGIC_PLANNER_CONTRACT.md`
- `docs/PLANNER_INFLUENCE_BOUNDARY.md`
- `docs/PLANNER_CAUSAL_CHAIN_ACTIVATION_REVIEW.md`

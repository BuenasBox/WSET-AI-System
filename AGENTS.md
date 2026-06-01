# AGENTS.md — WSET-AI-System Project Memory

This file is loaded automatically by Codex at the start of every session.
It is the authoritative project context for Codex + Codex collaboration.

---

## PROJECT IDENTITY

WSET-AI-System is a deterministic, local, governance-constrained WSET Level 3 tutoring architecture. It is currently best described as a rule-based neuro-symbolic ITS/RAG substrate, not a generative-first tutor.

Core philosophy: retrieval and structured cognition first; generation only after source, governance, learner-state, misconception, and causal-chain constraints are explicit.

It intentionally avoids: autonomous examiner authority, official scoring, hidden LLM calls, embeddings, vector databases, cloud services, frontend exposure, and untraceable answer drift.

Deterministic retrieval-first was chosen because the system is exam-adjacent and source-governed. The main risk is not lack of fluency — it is unsupported authority, grading overclaim, calibration drift, and untestable changes in cognitive behavior. Retrieval-first makes answer construction inspectable, snapshot-testable, and governance-enforceable.

---

## GOVERNANCE INVARIANTS (IMMUTABLE)

```
safe_for_examiner = False          # never set to True
examiner_scoring_allowed = False   # never set to True
uses_llm = False
uses_api = False
uses_embeddings = False
uses_vector_db = False
cloud_services_active = False
```

Enforcement: `tools/constants.py`. Checked in retrieval filters, Tutor validation, self-eval, LES write-back, SAT reasoner tests, and snapshot tests. Any truthy violation must fail safe.

Do NOT import `tools.orchestrator` from leaf modules.
Do NOT call any external services, LLMs, APIs, embeddings, or vector DB.
Do NOT write to files outside `knowledge/` and `tools/`.
This system is deterministic. All outputs must be reproducible.

---

## CURRENT ARCHITECTURE

### Retrieval layer
`tools/retrieval/tutor_retrieval_sandbox.py` — active deterministic retrieval engine. Loads Wine With Jimmy chunks, official WSET extracted chunks, golden tutor chunks, consolidated dictionary terms, and knowledge-map nodes. Performs query classification, domain expansion, SAT observation expansion, scoring, source diversity selection, governance filtering, and matched causal-chain extraction. Config: `knowledge/config/domain_expansions.json`, `knowledge/config/retrieval_config.json`. Official chunk creation: `tools/retrieval/official_wset_chunks.py`.

### Tutor layer
`tools/tutor/answer_builder.py` — renders deterministic Tutor markdown from context packages. Handles normal answers, misconception interventions, source notes, heading/disclaimer registries, causal-chain rendering, SAT quality section injection, mini-practice prompts, and governance validation. SAT support: `tools/tutor/sat_reasoner.py`. Explanation depth/scaffolding: `tools/tutor/explanation_priority.py`, `tools/tutor/scaffolding_policy.py`, `knowledge/config/explanation_priority_config.json`.

### Orchestrator
`tools/orchestrator/orchestrator.py` — local cognitive loop: ensure learner files → load LES → run misconception pre-pass → route to `misconception_prepass` or `normal_tutor` → run retrieval → build retrieved context → thread matched causal chains into `forced_causal_chains` → write context packages → stage session. Currently a router, not a full strategic planner. Protocol typing: `tools/orchestrator/protocols.py`.

### Strategic planner (Phase 1A — isolated)
`tools/orchestrator/strategic_planner.py` — deterministic pedagogical planning module. Pure function over learner state signals (memory_summary + les_context + optional prepass_result). Returns structured plan dict: `recommended_next_topics`, `review_topics`, `avoid_topics`, `misconception_focus`, `causal_chain_focus`, `sat_drill_needed`, `difficulty_progression`, `planning_confidence`, `plan_generated_at`, `cold_start`. Zero imports from retrieval or answer_builder. Zero side effects. All thresholds are module-level constants. Phase 1B will wire it into `run_orchestrator()`.

### Learner / epistemic state
`tools/orchestrator/learner_state.py` — LES defaults and session staging.
`tools/orchestrator/les_reconciler.py` — reconciles self-eval feedback into LES.
`tools/learner_model/knowledge_tracing.py` — mastery, retention risk, learning velocity, recurring misconceptions.
Active files: `knowledge/nazareth/epistemic_state.json`, `session_staging.json`, `pedagogical_memory.json`.

### Misconception handling
`tools/orchestrator/misconception_prepass.py` — loads 20 misconception nodes from `knowledge/knowledge-map/misconceptions/`, scores detection signals and `detection_keywords`, applies explanatory-query guards, returns deterministic intervention directives. Misconceptions are cognitive objects, not retrieval snippets.

### SAT reasoning layer
`tools/tutor/sat_reasoner.py` — deterministic SAT query detection, observation extraction, quality hypothesis scoring, exclusion rules, WSET-register quality formulation. Alias data: `knowledge/config/sat_observation_aliases.json`. SAT causal nodes: `CC_SAT_QUALITY_HIGH.json`, `CC_SAT_QUALITY_MEDIUM.json`.

### Causal-chain system
32 JSON nodes in `knowledge/knowledge-map/causal-chains/`. Retrieval detects via trigger keywords and step text → passes full safe nodes into `forced_causal_chains`. Tutor renders CAUSA/MECANISMO/EFECTO/FORMULACIÓN DE EXAMEN blocks via `_render_causal_chain()` and `_select_best_causal_chain()`. Causal chains are typed reasoning structures, not retrieved prose.

### Self-eval harness
`tools/self_eval/question_runner.py` — runs questions through orchestrator → retrieval → Tutor → comparator → reporter.
`tools/self_eval/answer_comparator.py` — deterministic diagnostic labels and SAT strength labels.
`tools/self_eval/evaluation_reporter.py` — writes summaries, feedback, pedagogical memory, and LES reconciliation.

### Snapshot regression harness
`tests/test_tutor_snapshot_regression.py` — 25 frozen Tutor outputs under `tests/fixtures/tutor_snapshots/`. Asserts exact answer snapshots, fixture integrity, idempotency, governance flags, disclaimers, headings, absence of `safe_for_examiner=True`.

### Structured question bank
Questions loaded from `knowledge/question-bank/structured/` → raw XLSX if available → `knowledge/self-eval/sample_questions.json`. Expectation templates: `knowledge/self-eval/question_expectations.json`. Current structured file: `knowledge/question-bank/structured/wset3_questions.json`. Binary files (XLSX, PDF, etc.) are blocked by `.gitignore`; use markitdown to convert docs before committing.

---

## CURRENT TESTING STATUS

- Test count: **507** via `python -m unittest discover -s tests -v` (500 regular + 7 slow, skipped by default)
- All 507 pass locally. (`pytest` not installed in active venv — use `python -m unittest`)
- Slow golden baseline: `RUN_SLOW_TESTS=1 python -m unittest tests.test_golden_self_eval -v` → 7/7 OK
- Brutal self-eval: 25 questions, no failure labels, no retrieval gaps, no SAT weaknesses.
- Known retrieval weakness: `missing_keyword_support` count = 5 (frozen in golden baseline).
- Snapshots: green for all 25 fixtures.

---

## ACTIVE REMEDIATION PLAN — WHERE WE ARE

Plan document: `docs/backend_stability_remediation_plan.md`
Workflow: Codex plans/reviews/writes prompts → Codex implements → Codex verifies → commit only when green.

### ALL BATCHES COMPLETE ✅

**Batch A — R1-C** (question runner config extraction) ✅
- `knowledge/self-eval/sample_questions.json`, `question_expectations.json` extracted
- `tests/test_question_runner_expectations.py` added
- Result: 236 → 238 tests

**Batch B — R1-A, R1-B, R1-D + R2-A, R2-B, R2-C** ✅
- `SAT_EVALUATION_TERMS` in `tools/constants.py`; `tokenize_term()` added
- `knowledge/config/retrieval_config.json`, `explanation_priority_config.json` created
- `tools/orchestrator/protocols.py` — typed protocol interfaces
- `evaluation_reporter.py` — explicit `ImportError` for `les_reconciler`
- `tests/test_retrieval_config.py`, `test_constants.py` added
- Result: 238 tests

**Batch C — R3-A (data-driven topic dispatch) + R3-B (score helpers)** ✅
- `knowledge/answer_patterns.json` (41 entries, bilingual, sentinel `__no_cross_language_pattern__`)
- `answer_builder.py`: all 5 dispatch functions data-driven (`_normal_direct_answer`, `_cause_effect_line`, `_exam_line`, `_mini_practice`, `_official_idea_from_text`)
- `score_chunk_for_query()` decomposed into 5 named helpers: `_score_lexical_overlap`, `_score_term_and_concept_matches`, `_score_boost_signals`, `_aggregate_chunk_score`, `_build_score_breakdown`. Orchestrator body ≤20 lines of logic.
- `tests/test_answer_patterns_schema.py` added (8 schema tests)
- Result: 238 → 246 tests

**Batch D — R4-A, R4-B, R4-C** ✅
- `tests/test_regression_r4a.py` — 9 regression tests (Tokaji + forced_causal_chains)
- `knowledge/self-eval/golden_brutal_output.json` — frozen CI baseline
- `tests/test_golden_self_eval.py` — 7 slow golden tests (guard: `RUN_SLOW_TESTS=1`)
- Result: 246 → 262 tests (255 regular + 7 slow)

**Batch E — R3-B score component tests** ✅
- `tests/test_score_components.py` — 36 unit tests for all 5 `score_chunk_for_query` helpers in isolation
- Fixed fixture bug: `matched_terms` in query_analysis must be `[{"canonical_term": ..., "category": ...}]`, not strings
- Result: 262 → 298 tests (291 regular + 7 slow)

**Batch F — Phase 1A strategic planner (isolated)** ✅
- `tools/orchestrator/strategic_planner.py` — new deterministic planning module (side-effect-free, governance-clean, cold-start safe, import-isolated)
- `tests/test_strategic_planner.py` — 49 tests across 10 classes; covers all 15 required tests + edge cases
- `_pedagogical_priority_boost()` in orchestrator preserved unchanged
- Result: 298 → 347 tests (340 regular + 7 slow)

**Batch G — Phase 1B orchestrator integration** ✅
- `tools/orchestrator/orchestrator.py` — planner wired in after LES construction; `strategic_plan` key added to result; planner NOT injected into `context_package` (zero retrieval/Tutor impact)
- `tests/test_orchestrator_strategic_planner_integration.py` — 22 integration tests across 7 classes (all required tests); verifies plan is observable, inert, governance-clean, and deterministic end-to-end
- Zero snapshot drift (35/35 snapshots unchanged)
- Result: 347 → 369 tests (362 regular + 7 slow)

**Phase 1B.5 — Semantic contract hardening** ✅
- `docs/STRATEGIC_PLANNER_CONTRACT.md` — authority model, signal ownership, depth semantics, migration path for `strategic_planner` vs `_pedagogical_priority_boost()`. Key finding: `_pedagogical_priority_boost()` does NOT influence retrieval (retrieval sandbox never receives it); it only affects Tutor rendering via `force_deep_explanation`. Adapter is fully inert at runtime today (skills={}). No code changes.

**Phase 3A.0 — Planner influence boundary contract** ✅
- `docs/PLANNER_INFLUENCE_BOUNDARY.md` — pre-Phase-3 governance document; classifies all planner signals (ALLOWED/CONDITIONALLY_ALLOWED/FORBIDDEN); classifies all influence targets; governance analysis; risk matrix; Phase 3 entry criteria (Section 5); identifies `causal_chain_focus → query expansion` as the first safe influence; permanently forbidden directions. No code changes.

**Phase 3A.2 — Retrieval compatibility for planner query hints** ✅
- `tools/retrieval/tutor_retrieval_sandbox.py` — added `_HINT_TOKEN_RE`, `_MAX_HINT_IDS = 3`, `_parse_planner_query_hints()` helper; wired into `run_retrieval_sandbox()` before `classify_query()` so `causal_chain:<id>` tokens never reach lexical scoring; `clean_query` and `planner_hint_chain_ids` added to run output; strict no-op for hint-free queries
- `tests/test_retrieval_planner_query_hints.py` — 38 tests across 13 classes; covers all 12 required tests; verifies single/multi-hint parsing, order preservation, malformed token rejection, deduplication, bounding, clean query integrity, governance cleanliness, no lexical noise (negative control included), no-op for normal queries, snapshot invariance, flag invariant
- Audit confirmed: CC_SAT_QUALITY_HIGH would inject `sat`, `quality`, `high`, `cc` into query_tokens as noise — parsing eliminates this
- Zero behavior change for hint-free queries; zero snapshot drift
- Result: 546 → 584 tests (576 passing + 8 skipped)

**Phase 3A.3 — Controlled causal-chain hint injection experiment** ✅
- `tools/retrieval/tutor_retrieval_sandbox.py` — added retrieval-local `ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION = False` gate and `_inject_planner_causal_chain_hints()` helper; parsed `planner_hint_chain_ids` can be converted into native lightweight `matched_causal_chains` only when the gate is explicitly enabled; default runtime remains unchanged
- `tests/test_retrieval_planner_causal_chain_injection.py` — 16 tests; verifies gate-off no-op, empty/unknown ID no-op, valid ID injection, multi-ID order preservation, deduplication, organic match preservation, no mutation, native shape, governance cleanliness, no full causal-chain prose, no scoring weight changes, default snapshot invariance, and reuse of existing `causal_chain_match_score`
- No new scoring weights; no ranking override; no Tutor changes; no governance fields; no snapshot drift
- Result: 584 → 600 tests (592 passing + 8 skipped)

**Phase 3A.8 — Planner causal-chain activation readiness review** ✅
- `docs/PLANNER_CAUSAL_CHAIN_ACTIVATION_REVIEW.md` — decision review covering evidence from 3A.4 A/B comparison, 3A.5 score deltas, 3A.6 adversarial negatives, and 3A.7 semantic compatibility hardening
- Recommendation: keep experimental behind gates; do not activate globally
- `ENABLE_PLANNER_QUERY_EXPANSION = False` and `ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION = False` remain required defaults
- Rationale: semantic compatibility mitigates known adversarial failures, but incremental value after gating is not yet strong enough because many compatible positives are already matched organically
- Activation criteria documented: larger representative fixtures, organic-miss positive wins, wrong-hint score delta below threshold, no ranking corruption, unchanged snapshots, governance-clean outputs, and explicit rollback plan
- Result: 660 tests (652 passing + 8 skipped), 35 snapshots green

**Question bank converter** ✅
- `tools/question_bank/convert_xlsx_to_json.py` — Excel → JSON converter; reads structured question XLSX, normalises columns, protects `Abierta` questions (strips `correct_answer` / `explanation` fields before export), writes `knowledge/question-bank/structured/wset3_questions.json`; governance-clean; no LLM/API calls
- `tools/question_bank/__init__.py` — package init
- `requirements.txt` — declares `openpyxl` dependency
- `tests/test_question_bank_converter.py` — 39 tests across N classes; covers column normalisation, Abierta protection, round-trip JSON schema, governance cleanliness, file-write invariants
- Result: 507 → 546 tests (539 regular + 7 slow)

**Phase 3A.1 — Planner query expansion gate** ✅
- `tools/orchestrator/orchestrator.py` — added `ENABLE_PLANNER_QUERY_EXPANSION = False`, `MAX_PLANNER_CHAIN_HINTS = 3`, `_apply_planner_query_hints()` helper; wired before `run_retrieval_sandbox()` call; gate is a deterministic no-op with flag off; only `causal_chain_focus` IDs used when flag on; all other planner signals explicitly ignored; expansion bounded to 3 compact tokens (`causal_chain:<id>`); no governance fields, no prose
- `tests/test_planner_query_expansion_gate.py` — 26 tests across 8 classes; covers all 15 required tests; verifies flag-off no-op, missing-plan guard, empty-chain guard, signal isolation (review_topics/misconception_focus/difficulty_progression/planning_confidence), bounding, determinism, governance cleanliness, prose safety, and end-to-end orchestrator invariants
- Zero behavior change with flag off; zero snapshot drift
- Result: 481 → 507 tests (500 regular + 7 slow)

**Batch K — Phase 2C ledger summary CLI** ✅
- `tools/orchestrator/ledger_summary.py` — extended with CLI block: `load_ledger_file()`, `format_report()`, `_cli()`, `DEFAULT_LEDGER_PATH`; `python -m tools.orchestrator.ledger_summary --ledger <path>` prints formatted report; `--json` outputs raw summary JSON; `--top-n N` overrides display limit; read-only, no file writes
- `tests/test_ledger_summary_cli.py` — 27 tests across 10 classes covering all 10 required tests; verifies read-only invariants (ledger, LES, staging unchanged), error handling, JSON mode, governance cleanliness
- Result: 454 → 481 tests (474 regular + 7 slow)

**Batch J — Phase 2B ledger summary layer** ✅
- `tools/orchestrator/ledger_summary.py` — pure function `summarize_ledger(ledger) -> dict`; computes top_review_topics, top_misconceptions, top_causal_chains, sat_drill_rate, cold_start_rate, difficulty_distribution + pct, route_distribution, average_planning_confidence; TOP_N=10 cap; ties broken alphabetically; no side effects; no file I/O; governance-clean; no grading fields
- `tests/test_ledger_summary.py` — 42 tests across 14 classes covering all 14 required tests
- No changes to planner, retrieval, Tutor, or orchestrator (summary is pure reporting)
- Result: 412 → 454 tests (447 regular + 7 slow)

**Batch I — Phase 2A session cognitive ledger** ✅
- `tools/orchestrator/session_ledger.py` — new write-only telemetry module; `append_to_ledger()` records structured signals (route, review_topics, misconceptions_triggered, causal_chains_seen, sat_drill_needed, difficulty_progression, planning_confidence, cold_start); bounded to last 100 sessions; governance-clean; no raw queries/answers/chunks
- `tools/orchestrator/orchestrator.py` — ledger appended after staging write; ledger_path derived from `les_path.parent` so tests automatically use temp dirs
- `tests/test_session_ledger.py` — 26 tests across 10 classes covering all 14 required tests
- Result: 386 → 412 tests (405 regular + 7 slow)

**Batch H — Phase 1C strategic plan persistence** ✅
- `tools/orchestrator/orchestrator.py` — `staging` dict extended with top-level `"strategic_plan"` key (write-only observation snapshot; never read back by planner)
- `tests/test_strategic_plan_persistence.py` — 17 tests across 7 classes; verifies top-level persistence, JSON round-trip, cold-start/warm-start correctness, governance cleanliness, no-readback guarantee, and planner determinism regardless of staging contents
- Result: 369 → 386 tests (379 regular + 7 slow)

### Pending tasks

**None from remediation plan.** All items in `docs/backend_stability_remediation_plan.md` are complete or deferred.

**Next phases:**
- **Phase 3A activation readiness** — Keep causal-chain planner influence gated OFF until additional evidence shows value beyond organic retrieval without adversarial regressions.
- **Phase 3B** — WSET L3 topic sequence to populate `recommended_next_topics`.

**Semantic contract:** `docs/STRATEGIC_PLANNER_CONTRACT.md` — defines authority model, signal ownership, depth semantics, and migration path between `strategic_planner` and `_pedagogical_priority_boost()`. Read before touching either component.

---

## VERIFICATION GATE PROTOCOL

After every code change:
```
python -m unittest discover -s tests -v   → must stay at 660+ passing/skipped
brutal self-eval                          → must stay {}
```
Slow golden suite (only when touching self-eval pipeline):
```
$env:RUN_SLOW_TESTS=1; python -m unittest tests.test_golden_self_eval -v
```
Any regression = rollback that sub-step before proceeding.

---

## DOCUMENTATION CONVENTION

**No binary documents in the repository.** Convert to Markdown first:
```bash
markitdown source.pdf > output.md
markitdown source.docx > docs/output.md
```
Blocked by `.gitignore`: `*.pdf`, `*.doc`, `*.docx`, `*.xls`, `*.xlsx`, `*.ppt`, `*.pptx`, `*.odt`, `*.ods`, `*.odp`.

---

## COGNITIVE ARTIFACT PROTECTION

The following are **machine-local cognitive objects** and must NEVER be committed or deployed to Vercel/GitHub public. Risks: cognitive leakage, operational drift, false authority, learner-data exposure.

| Path | What it is | Risk |
|------|-----------|------|
| `knowledge/nazareth/` | Live LES, session staging, pedagogical memory | Learner state exposure |
| `knowledge/self-eval/reports/` | Dynamic self-eval run outputs | Drift / false authority |
| `knowledge/self-eval/attempts/` | Per-question attempt artifacts | Operational noise |
| `knowledge/retrieval-sandbox/` | Derived retrieval outputs | Contamination |
| `*.jsonl` | Pipeline stream outputs | Machine-local traces |
| `.Codex/` | Agent tooling state | Tooling leakage |
| `.vercel/` | Vercel deployment cache | CI contamination |

**What IS intentionally versioned in `knowledge/self-eval/`:**
- `sample_questions.json` — config, not runtime output
- `question_expectations.json` — config, not runtime output
- `golden_brutal_output.json` — intentional CI baseline (future R4-C)

**Regression harness is protected:** `tests/fixtures/tutor_snapshots/` has explicit `!`-negations in `.gitignore` as a safety net. This must never be excluded.

---

## WHAT NOT TO TOUCH

- Do not refactor `answer_builder.py` behavior-dense code without snapshots
- Do not set any governance flag to True
- Do not add LLM, API, embeddings, vector DB, or cloud paths
- Do not expose anything to a frontend yet
- Do not add official grading authority to any module
- Do not alter snapshot outputs without explicit regression intent
- Do not run R3-B before R1-B is confirmed complete (it is — `retrieval_config.json` exists)

---

## REPO STATUS (as of last session)

Latest commits (session 2026-05-29):
- `feat(phase-3a2): parse planner causal-chain query hints safely` ← next commit
- `feat(question-bank): add Excel→JSON converter; protect Abierta questions; declare openpyxl` ← Commit 2 (this session)
- `feat(phase-3a1): wire planner query expansion gate; add gate tests` ← Commit 1 (this session)
- `docs(phase-3a0): add PLANNER_INFLUENCE_BOUNDARY.md; governance contract`
- `feat(phase-2c): add ledger summary CLI; complete observability loop`
- `feat(phase-2b): add ledger summary layer; pure reporting function`
- `feat(phase-2a): add session cognitive ledger; write-only telemetry`
- `feat(phase-1c): persist strategic_plan to session_staging; add persistence tests`
- `docs(phase-1b5): add STRATEGIC_PLANNER_CONTRACT.md; semantic contract hardening`
- `feat(phase-1b): wire strategic_planner into orchestrator; add integration tests`
- `feat(phase-1a): add strategic_planner module and tests in isolation`

Dirty worktree (not committed — runtime / local only):
- `knowledge/nazareth/epistemic_state.json`, `session_staging.json` — modified locally (machine-local cognitive objects, never commit)
- `knowledge/self-eval/attempts/` — runtime self-eval outputs (gitignored)

---

*This file is a development planning document. It does not represent WSET assessment or examiner evaluation.*

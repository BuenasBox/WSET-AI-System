# CLAUDE_PROJECT_STATUS.md

> **Authority**: Derived from repository state as of commit `f092b5955` (2026-06-06T01:24:19Z).  
> **Purpose**: Cold-start orientation for any AI agent joining this project.  
> **Rule**: Trust this file only if no newer commit in `docs/` contradicts it. If in doubt, re-derive from the repo.

---

## Repository Identity

| Field | Value |
|---|---|
| Repo | `BuenasBox/WSET-AI-System` |
| Branch | `main` |
| HEAD commit | `f092b5955f053005847425d75831120439b338d9` |
| HEAD message | `Merge PR #3: canonical Master Bank infrastructure` |
| HEAD date | 2026-06-06T01:24:19Z |
| Merged PRs | PR #2 (Open Response Lab), PR #3 (Master Bank) |
| No active unmerged branches | confirmed at time of writing |

---

## Governance Invariants (NEVER modify without explicit authorization)

```
safe_for_examiner = false                    # always, all layers
examiner_scoring_allowed = false             # always, all layers
official_wset_question = false               # always
training_item_only = true                    # always
ENABLE_PEDAGOGICAL_STRATEGY_LAYER = False    # do NOT activate without user authorization
```

All frontend components must display: `PROTOTIPO ESTÁTICO · ENTRENAMIENTO · NO EVALUACIÓN OFICIAL WSET`

---

## Work Stream Status

### 1. Tutor / PSL (Pedagogical Strategy Layer)
**Status: ✅ COMPLETED**

- 8 Python modules in `tools/tutor/pedagogical_strategy/`: `strategy_selector.py`, `strategy_layer.py`, `mode_selector.py`, `profiles.py`, `psl_profile_validator.py`, `character_resolver.py`, `avatar_stub.py`, `__init__.py`
- `tools/tutor/`: `answer_builder.py` (51KB), `explanation_priority.py`, `sat_reasoner.py`, `scaffolding_policy.py`
- 5 tutor modes: mentor, trainer, reviewer, distinction, exam_pressure
- 5 fictional characters: Astrid, Andrey, María, Arturo, Fernanda (governance-safe, no real persons)
- 6 PSL functions: cartographer, scientist, host, storyteller, critic, challenger
- 8+ test files covering PSL (test_psl_*, test_pedagogical_*)
- Gate: `ENABLE_PEDAGOGICAL_STRATEGY_LAYER = False` — **gated by design, not a bug**
- Blocker: None. Activation is a deliberate governance decision.
- Risk: PSL functions are deterministic logic only. No LLM, no roleplay, no real-person imitation.

---

### 2. Retrieval
**Status: 🔄 IN PROGRESS**

- `tools/retrieval/official_wset_chunks.py` (7KB) — lexical chunk retrieval from official WSET corpus
- `tools/retrieval/tutor_retrieval_sandbox.py` (60KB) — large sandbox implementation
- `knowledge/retrieval-sandbox/` — sandbox data directory exists
- `knowledge/official-wset/` — corpus directory exists
- Tests: `test_official_corpus_retrieval.py`, `test_planner_query_expansion_gate.py`, `test_golden_tutor_chunks.py`
- **Blocker**: Retrieval not yet wired into runtime tutor pipeline
- **Gap**: Planner integration with question composition not fully operational
- Risk: No vector DB, no embeddings (by design). Lexical only.

---

### 3. Governance
**Status: ✅ COMPLETED**

- Schema enforcement: `knowledge/enrichment/diagnostic_sba_item.schema.json` — `question_type: "diagnostic_single_best_answer"` (canonical)
- Validator: `tools/question_generation/diagnostic_sba_validator.py` — canonical, enforces all invariants
- Docs: `DIAGNOSTIC_SBA_GOVERNANCE_CONTRACT.md`, `AGENT_BOUNDARIES.md`, `DATA_GOVERNANCE.md`, `EXAMINER_CALIBRATION_RULES.md`
- Frontend: disclaimer banner required and present in v2.2
- Tests: `test_diagnostic_sba_schema.py`, `test_diagnostic_sba_validator.py`, governance checks in all major test files
- Risk: `AI_CONTRACT.md` and `ARCHITECTURE.md` exist but are **empty (0 bytes)** — need to be populated

---

### 4. Diagnostic SBA
**Status: 🔄 IN PROGRESS**

| Metric | Value | Source |
|---|---|---|
| Structured bank | ~616 records | `knowledge/question-bank/structured/wset3_questions.json` (486KB) |
| Gold Bank | ~36 items | PHASE_4A_3_7_37-38-39 reports |
| Master Bank | EXISTS | `knowledge/question-bank/master_bank/master_bank.json` (1.2MB) — merged PR #3 |
| Active/published | **UNCERTAIN** | `frontend/diagnostic-sba/preguntas.json` — last known: 3 items; may have changed after PR #3 |
| Exporter | EXISTS | `tools/question_generation/export_static_demo_questions.py` + `static_demo_exporter.py` |
| Option Shuffle | REPORTED | `PHASE_4A_3_7_40_OPTION_SHUFFLE_REPORT.md` exists — frontend implementation status **unconfirmed** |
| SBA cockpit | v2.2 deployed | `frontend/diagnostic-sba-v2.2/index.html` |
| Deployed cockpit | ⚠️ UNCERTAIN | `frontend/architecture-dashboard/diagnostic-sba/index.html` — was hardcoded mock; status after PR #3 unknown |

- C-option bias: 56.5% of structured bank has correct answer = C (documented)
- SBA purity: micro_drill items enforced as type `micro_sba` only (v2.2)
- 7-stage cognitive flow implemented in cockpit
- **Critical gap**: Verify deployed cockpit reads live `preguntas.json` vs. hardcoded mock

---

### 5. Gold Bank
**Status: ✅ COMPLETED**

- Phase 4A.3.7.37: Gold Bank Implementation — done
- Phase 4A.3.7.38: Gold Bank QA Audit — done
- Phase 4A.3.7.39: Targeted QA Remediation — done
- Corpus grounding: `FULL_BANK_CORPUS_VERIFICATION.json` (801KB) — 524 items: 57 STRONG / 256 PARTIAL / 10 WEAK / 201 NOT_FOUND
- Tier-1 (10 items): 9 STRONG, 1 PARTIAL (Q17)
- Human review: batch_1 + batch_2 approved

---

### 6. Master Bank
**Status: ✅ COMPLETED (merged 2026-06-06)**

- `knowledge/question-bank/master_bank/master_bank.json` — 1.2MB, canonical data file
- `knowledge/question-bank/master_bank/master_bank.schema.json` — 4.3KB, JSON schema
- `tools/question_generation/master_bank.py` — 18KB, importer/validator/accessor
- `tools/question_generation/sba_session_composer.py` — 5.5KB, session composition
- `tests/test_master_bank.py` — integrity tests
- **This was the central blocker for Governed Generation. It is now resolved.**

---

### 7. Open Response
**Status: 🔄 IN PROGRESS**

| Component | Status | File |
|---|---|---|
| Pipeline | ✅ EXISTS | `tools/question_generation/open_response_pipeline.py` (31KB) |
| Session Engine | ✅ EXISTS | `tools/question_generation/open_response_session_engine.py` (7KB) |
| Runtime (private) | ✅ EXISTS | `tools/question_generation/open_response_lab_runtime.py` (9KB) |
| Frontend Lab | ✅ EXISTS | `frontend/open-response-lab/` directory |
| Normalized candidates | ✅ EXISTS | `knowledge/question-bank/open_response/normalized/diagnostic_open_response_candidates.json` (78KB) |
| Review records | ✅ EXISTS | `knowledge/question-bank/open_response/reviews/open_response_review_records.json` (24KB) |
| Semantic review | ✅ DONE | `OPEN_RESPONSE_SEMANTIC_REVIEW_BATCH_1.md` |
| Phases | ✅ 44–49 done | Foundation, grounding, remediation batches 1+2, private lab runtime |
| Operational rubrics | ❌ MISSING | No rubrics file exists for examiner-style scoring |
| Feedback templates | ❌ MISSING | No structured feedback template files |
| Remediation maps | ❌ MISSING | No remediation map documents |
| Active count | **UNKNOWN** | No published active set confirmed |

- `docs(open-response): add semantic review and readiness assessment` — last commit in this area
- Tests: `test_open_response_pipeline.py`, `test_open_response_session_engine.py`, `test_open_response_lab_runtime_mvp.py`, `test_open_response_grounding_review.py`

---

### 8. Adaptive Architecture
**Status: ❌ NOT STARTED**

- No adaptive runtime component exists that modifies question selection based on learner performance in real-time
- `tools/learner_model/` directory exists (empty or minimal)
- `test_learner_knowledge_tracing.py` exists but tests static model, not live adaptation
- Blocker: Requires Master Bank (now done) + Session Composer (now done) + Open Response rubrics

---

### 9. Governed Generation
**Status: ❌ NOT STARTED**

Prerequisites audit:

| Prerequisite | Status |
|---|---|
| Master Bank schema | ✅ EXISTS |
| Master Bank data | ✅ EXISTS |
| Corpus grounding verification | ✅ DONE (full bank) |
| Validator with generation_source field | UNCLEAR — needs verification |
| Generation contract document | NOT FOUND in docs listing |
| 5-gate generation pipeline | NOT IMPLEMENTED |
| Human review gate for generated items | NOT IMPLEMENTED |
| Corpus citation requirement enforcement | PARTIAL |

- `docs/SBA_MASTER_BANK_AND_GOVERNED_GENERATION_ROADMAP.md` — strategy document exists
- Actual generation pipeline: not yet built

---

### 10. Dashboard
**Status: 🔄 IN PROGRESS**

- Architecture dashboard deployed at `epistemiclab.dpdns.org`
- `frontend/architecture-dashboard/` — directory exists
- `docs/DASHBOARD_LAB_LINK_CONTRACT.md` — lab link contract documented
- Tests: `test_dashboard_lab_link_contract.py`, `test_dashboard_lab_link_implementation.py`, `test_dashboard_state_updater.py`
- **Known gap**: Deployed `index.html` under architecture-dashboard/diagnostic-sba was last known to be hardcoded mock. Status after PR #3 unconfirmed.
- `frontend/diagnostic-sba-v2.2/index.html` (latest version) — exists in repo

---

### 11. Knowledge Layer
**Status: ✅ COMPLETED (core)**

- `knowledge/official-wset/` — WSET official Markdown corpus (used for grounding)
- `knowledge/question-bank/structured/wset3_questions.json` — 486KB, ~616 records
- `knowledge/answer_patterns.json` — 45KB
- `knowledge/knowledge-map/` — knowledge map directory
- `knowledge/calibration/` — calibration data
- `knowledge/benchmark-wines/` + `knowledge/benchmark-answers/` — benchmark sets
- `knowledge/nazareth/` — learner data (Nazareth)
- Enrichment schema: `knowledge/enrichment/diagnostic_sba_item.schema.json`
- **Gap**: Coverage metrics not computed. No automated coverage report.
- **Gap**: Knowledge asset registry architecture not designed.

---

## Tests

**Confirmed test files: 48+ (partial listing)**

Test areas identified:
- PSL: `test_psl_*` (4 files), `test_pedagogical_*` (3 files), `test_adaptive_pedagogical_reasoning.py`
- SBA: `test_diagnostic_sba_*` (4 files)
- Open Response: `test_open_response_*` (4 files)
- Master Bank: `test_master_bank.py`
- Retrieval: `test_official_corpus_retrieval.py`, `test_planner_query_expansion_gate.py`, `test_golden_tutor_chunks.py`
- Orchestrator: `test_orchestrator_strategic_planner_integration.py`, `test_minimal_brain_orchestrator.py`
- Dashboard: `test_dashboard_*` (3 files)
- Ledger: `test_ledger_summary.py`, `test_ledger_summary_cli.py`
- Self-eval: `test_golden_self_eval.py`
- Milestone: `test_milestone_1_3.py`

Last known test run result: **1,363 passing** (from prior execution review, pre-PR #3). Current count unknown — `test_master_bank.py` was added in PR #3.

---

## Deployments

| Asset | Status | URL / Location |
|---|---|---|
| Architecture dashboard | ✅ PUBLIC | `epistemiclab.dpdns.org` |
| Diagnostic SBA cockpit | ✅ PUBLIC (via dashboard) | `epistemiclab.dpdns.org/diagnostic-sba/` |
| SBA v2.2 source | PRIVATE | `frontend/diagnostic-sba-v2.2/index.html` |
| Open Response Lab | PRIVATE | `frontend/open-response-lab/` |
| Raw GitHub download | AVAILABLE | `https://raw.githubusercontent.com/BuenasBox/WSET-AI-System/main/frontend/diagnostic-sba-v2.2/index.html` |

---

## Hallazgos Críticos

1. **master_bank.json now exists** — PR #3 merged 2026-06-06. The central blocker for Governed Generation is resolved. The execution review in `SBA_MASTER_BANK_EXECUTION_REVIEW.md` is NOW STALE on this point.
2. **Deployed cockpit JSON loader status unconfirmed** — Was hardcoded mock. May still be. Must verify before claiming cockpit reads live data.
3. **preguntas.json count is uncertain** — Last known: 3 items. PR #3 added session composer and static exporter. The file may have been re-exported with more items, or may still be 3.
4. **Open Response missing rubrics/templates/maps** — Pipeline and engine exist but scoring rubrics, feedback templates, and remediation maps are not present. These are required before Open Response can be used pedagogically.
5. **AI_CONTRACT.md and ARCHITECTURE.md are empty** — Both 0 bytes. Placeholder files that were never populated.
6. **Option shuffle: report exists, implementation unconfirmed** — `PHASE_4A_3_7_40_OPTION_SHUFFLE_REPORT.md` exists but whether the shuffle is live in the frontend is unconfirmed.

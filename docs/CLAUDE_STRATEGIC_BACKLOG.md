# CLAUDE_STRATEGIC_BACKLOG.md

> **Authority**: Derived from repository state as of commit `f092b5955` (2026-06-06T01:24:19Z).  
> **Purpose**: Prioritized work queue for Claude sessions. Read this before starting any implementation work.  
> **Rule**: Items are ordered by strategic impact. Do not reorder without evidence from repo state.

---

## Legend

| Symbol | Meaning |
|---|---|
| 🔴 P1 | Critical — blocks learner-facing functionality |
| 🟠 P2 | High — needed for completeness of active work streams |
| 🟡 P3 | Medium — important but not blocking anything deployed |
| 🟢 P4 | Low — future capability, no current dependency |

---

## Backlog

### 🔴 P1-A — Verify and Fix Deployed Cockpit JSON Loader

| Field | Value |
|---|---|
| Phase | Immediate fix |
| Description | `frontend/architecture-dashboard/diagnostic-sba/index.html` was a hardcoded v2.2 mock as of the prior execution review. Must verify if PR #3 or Codex updated it to read `preguntas.json` live. If still hardcoded, reconnect it. |
| Dependencies | Knowledge of cockpit contract (`DIAGNOSTIC_SBA_COCKPIT_CONTRACT.md`), `frontend/diagnostic-sba/preguntas.json` |
| Expected Deliverable | Confirmed live JSON loader in deployed cockpit. Updated `FRONTEND_STATE_AUDIT.md` with current status. |
| Claude work | Read `frontend/architecture-dashboard/diagnostic-sba/index.html`. Check for fetch/XHR to preguntas.json. Compare with `frontend/diagnostic-sba-v2.2/index.html`. |

---

### 🔴 P1-B — Audit and Re-export preguntas.json

| Field | Value |
|---|---|
| Phase | Immediate |
| Description | `frontend/diagnostic-sba/preguntas.json` last confirmed: 3 items (Q2, Q12, Q17). With PR #3 merging `static_demo_exporter.py` and `sba_session_composer.py`, the eligible item count may have changed. Verify actual count, run exporter if needed. |
| Dependencies | `master_bank.json` (now exists), `static_demo_exporter.py`, `export_static_demo_questions.py` |
| Expected Deliverable | `preguntas.json` with all Gold Bank items that pass governance gates (expected: ~9–36 depending on export criteria). |
| Claude work | Read `preguntas.json`. Count items. Read exporter to understand criteria. Write Codex prompt if re-export is needed. |

---

### 🔴 P1-C — Open Response: Operational Rubrics

| Field | Value |
|---|---|
| Phase | 4A.3.7.50 (next after phase 49) |
| Description | Open Response pipeline, session engine, and runtime exist. Missing: deterministic scoring rubrics that define what constitutes an acceptable vs. exemplary answer for each question type. Without rubrics, the feedback loop is undefined. |
| Dependencies | `diagnostic_open_response_candidates.json` (78KB, normalized candidates), `open_response_review_records.json` (24KB) |
| Expected Deliverables | `docs/OPEN_RESPONSE_OPERATIONAL_RUBRICS.md` — rubric spec per question type. `knowledge/question-bank/open_response/rubrics/` directory with at least 1 rubric file. |
| Claude work | Design rubric schema (deterministic, no LLM scoring). Define thresholds. Write first rubric for most common OR question type. |

---

### 🟠 P2-A — Open Response: Feedback Templates

| Field | Value |
|---|---|
| Phase | 4A.3.7.51 |
| Description | After rubrics are defined, structured feedback templates must be created so the tutor can return pedagogically useful feedback to learners on open response answers. Templates must be deterministic (no LLM generation). |
| Dependencies | P1-C (rubrics) |
| Expected Deliverables | `knowledge/question-bank/open_response/feedback_templates/` with templates per rubric category. `docs/OPEN_RESPONSE_FEEDBACK_TEMPLATE_SPEC.md`. |
| Claude work | Design template format. Write templates for each rubric outcome. |

---

### 🟠 P2-B — Open Response: Remediation Maps

| Field | Value |
|---|---|
| Phase | 4A.3.7.52 |
| Description | Given a learner's open response error pattern, remediation maps define which SBA questions, knowledge chunks, or explanations to surface next. Connects OR feedback to SBA session composer. |
| Dependencies | P2-A (feedback templates), `master_bank.json` |
| Expected Deliverables | `knowledge/question-bank/open_response/remediation_maps/` directory. `docs/OPEN_RESPONSE_REMEDIATION_MAP_SPEC.md`. |
| Claude work | Design remediation map schema. Write maps for first 3 error categories. |

---

### 🟠 P2-C — Knowledge Utilization & Coverage Audit

| Field | Value |
|---|---|
| Phase | 4A.3.7.53 |
| Description | The full bank corpus verification (`FULL_BANK_CORPUS_VERIFICATION.json`) shows 201 NOT_FOUND items and 181 DISTRACTOR_CONFLICT flags. A coverage audit would identify which WSET topics have adequate question coverage and which have gaps. |
| Dependencies | `FULL_BANK_CORPUS_VERIFICATION_SUMMARY.md`, `master_bank.json`, `knowledge/knowledge-map/` |
| Expected Deliverables | `docs/KNOWLEDGE_COVERAGE_AUDIT.md` — topic → item count matrix. List of under-covered topics. Priority list for new question generation. |
| Claude work | Read corpus verification summary. Cross-reference with knowledge map. Produce gap analysis. |

---

### 🟠 P2-D — Verify Option Shuffle Implementation

| Field | Value |
|---|---|
| Phase | Verification |
| Description | `PHASE_4A_3_7_40_OPTION_SHUFFLE_REPORT.md` documents option shuffle design. Whether this was implemented in the frontend is unconfirmed. The C=56.5% positional bias in the structured bank is a known issue. |
| Dependencies | `frontend/diagnostic-sba-v2.2/index.html`, `PHASE_4A_3_7_40_OPTION_SHUFFLE_REPORT.md` |
| Expected Deliverable | Confirmed status in `FRONTEND_STATE_AUDIT.md`. If not implemented, Codex prompt to add shuffle using `correct_answer_text` field. |
| Claude work | Read the shuffle report. Grep for shuffle logic in v2.2 index.html. |

---

### 🟡 P3-A — Knowledge Coverage Metrics

| Field | Value |
|---|---|
| Phase | 4A.3.7.54 |
| Description | After the coverage audit (P2-C), implement automated coverage metrics that can be run as a CI check. Reports: % of knowledge map topics covered by ≥3 Gold Bank items. |
| Dependencies | P2-C (coverage audit), `knowledge/knowledge-map/`, `master_bank.json` |
| Expected Deliverables | `tools/question_bank/coverage_metrics.py`. `docs/KNOWLEDGE_COVERAGE_METRICS_CONTRACT.md`. |
| Claude work | Design metric schema. Write script. Add test. |

---

### 🟡 P3-B — Governed Generation Readiness Audit

| Field | Value |
|---|---|
| Phase | 4A.3.7.55 |
| Description | Master Bank now exists. Assess which of the 8 generation prerequisites are now met and what remains before the first governed generation cycle can run. |
| Dependencies | `master_bank.json` (done), `master_bank.schema.json`, `SBA_MASTER_BANK_AND_GOVERNED_GENERATION_ROADMAP.md` |
| Expected Deliverables | `docs/GOVERNED_GENERATION_READINESS_AUDIT.md` — checklist of 8 prerequisites with current status. Specific gaps documented. |
| Claude work | Read roadmap. Check each prerequisite against repo state. Document gaps. |

---

### 🟡 P3-C — Populate AI_CONTRACT.md and ARCHITECTURE.md

| Field | Value |
|---|---|
| Phase | Documentation |
| Description | Both files are 0 bytes. `AI_CONTRACT.md` should encode governance invariants as a binding contract. `ARCHITECTURE.md` should describe the current system architecture for cold-start orientation. |
| Dependencies | `AGENT_BOUNDARIES.md` (51KB), `DIAGNOSTIC_SBA_GOVERNANCE_CONTRACT.md`, current repo state |
| Expected Deliverables | Non-empty `AI_CONTRACT.md` and `ARCHITECTURE.md`. |
| Claude work | Synthesize from existing governance docs. Write concise, authoritative versions. |

---

### 🟡 P3-D — Knowledge Asset Registry Architecture

| Field | Value |
|---|---|
| Phase | 4A.3.7.56 |
| Description | Design a registry that catalogs all knowledge assets (corpus chunks, question items, rubrics, templates) with their coverage, grounding status, and pedagogical tags. Foundation for adaptive architecture. |
| Dependencies | P3-A (coverage metrics), `knowledge/knowledge-map/`, `master_bank.json` |
| Expected Deliverables | `docs/KNOWLEDGE_ASSET_REGISTRY_ARCHITECTURE.md` — schema design. `knowledge/knowledge-map/registry_schema.json`. |
| Claude work | Design registry schema. Map existing assets to registry format. |

---

### 🟢 P4-A — Adaptive Architecture Design

| Field | Value |
|---|---|
| Phase | Future |
| Description | Design how the system will adapt question selection to individual learner performance in real-time. Requires learner model, session history, and master bank integration. |
| Dependencies | P3-D (registry), P2-B (remediation maps), `tools/learner_model/` |
| Expected Deliverables | `docs/ADAPTIVE_ARCHITECTURE_DESIGN.md`. |

---

### 🟢 P4-B — Governed Generation Implementation

| Field | Value |
|---|---|
| Phase | Future |
| Description | Implement the 5-gate governed generation pipeline from the master bank roadmap. Generate new SBA items with full corpus citation requirements and human review gating. |
| Dependencies | P3-B (readiness audit), all prerequisites from roadmap |
| Expected Deliverables | `tools/question_generation/governed_generation_pipeline.py`. First generated batch with citations. |

---

## Codex vs. Claude Boundary

| Work Type | Owner |
|---|---|
| Python implementation (scripts, pipelines, validators) | Codex |
| Test writing | Codex |
| HTML/JS frontend implementation | Codex |
| Schema design and documentation | Claude |
| Rubric design and content | Claude |
| Architectural decisions | Claude |
| Human review of question content | Human |
| Governance decisions | Human |

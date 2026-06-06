# CLAUDE_NEXT_PHASES.md

> **Authority**: Derived from repository state as of commit `f092b5955` (2026-06-06T01:24:19Z).  
> **Purpose**: Claude-only work queue. Describes what Claude (not Codex, not human) should do next.  
> **Rule**: Work in NOW before NEXT. Do not start LATER until NEXT is done.

---

## Priority Order Validation

You proposed this order:

```
1. Knowledge Utilization & Coverage Audit
2. Open Response Operational Rubrics
3. Open Response Feedback Templates
4. Open Response Remediation Maps
5. Governed Generation Readiness
6. Knowledge Coverage Metrics
7. Knowledge Asset Registry Architecture
```

**Assessment after repo audit:**

The order is logically sound but has two corrections:

1. **Items 1–2 should be reordered**: Open Response Operational Rubrics should come BEFORE the Knowledge Coverage Audit. The rubrics unblock the OR feedback loop (a deployed feature with users). The coverage audit is strategic research. Deployed feature > research.

2. **Two items are missing from the list**: (A) Fix the deployed cockpit JSON loader (critical bug, takes ~30 min) and (B) verify option shuffle implementation — both should precede content work.

**Recommended order:**

```
[NOW]   Fix deployed cockpit JSON loader (if still hardcoded)
[NOW]   Verify option shuffle in frontend
[NOW]   Open Response Operational Rubrics
[NEXT]  Open Response Feedback Templates
[NEXT]  Open Response Remediation Maps
[NEXT]  Knowledge Utilization & Coverage Audit
[LATER] Knowledge Coverage Metrics
[LATER] Governed Generation Readiness Audit
[LATER] Knowledge Asset Registry Architecture
[FUTURE] Adaptive Architecture Design
```

---

## NOW (Current Sprint)

Do these before starting any new content work.

### NOW-1: Verify Deployed Cockpit JSON Loader

**What**: Read `frontend/architecture-dashboard/diagnostic-sba/index.html`. Determine whether it fetches `preguntas.json` dynamically or renders hardcoded data.

**How**:
```
1. mcp__github__get_file_contents: frontend/architecture-dashboard/diagnostic-sba/index.html
2. Search for: fetch(, XMLHttpRequest, preguntas.json, hardcoded
3. Compare with frontend/diagnostic-sba-v2.2/index.html (latest version)
4. Document finding in FRONTEND_STATE_AUDIT.md
```

**If hardcoded**: Write Codex prompt to reconnect JSON loader using v2.2 pattern.  
**If live**: Confirm and move on.  
**Deliverable**: Updated `FRONTEND_STATE_AUDIT.md` line confirming status.

---

### NOW-2: Audit preguntas.json Count

**What**: Determine how many items are currently in `frontend/diagnostic-sba/preguntas.json` and whether they reflect all eligible Gold Bank items.

**How**:
```
1. Read preguntas.json (note: file is ~201KB, read carefully)
2. Count items
3. Compare with master_bank.json eligible active items
4. If count < eligible, write Codex prompt to re-run exporter
```

**Deliverable**: Known count. Codex prompt if re-export needed.

---

### NOW-3: Verify Option Shuffle Status

**What**: Determine if option shuffle was implemented in `frontend/diagnostic-sba-v2.2/index.html`.

**How**:
```
1. Read PHASE_4A_3_7_40_OPTION_SHUFFLE_REPORT.md
2. Read frontend/diagnostic-sba-v2.2/index.html — search for shuffle, Fisher-Yates, correct_answer_text
3. Document status
```

**If not implemented**: Write Codex prompt to implement shuffle using `correct_answer_text` field (not `correct_answer` position).  
**Deliverable**: Confirmed status. Codex prompt if needed.

---

### NOW-4: Open Response Operational Rubrics

**What**: Design and write the first operational rubrics for Open Response scoring.

**Why now**: The pipeline, session engine, and runtime exist (phases 44–52 done). The missing rubrics are the gap between "infrastructure built" and "pedagogically usable."

**How**:
```
1. Read knowledge/question-bank/open_response/normalized/diagnostic_open_response_candidates.json
   — identify the most common question types
2. Read knowledge/question-bank/open_response/reviews/open_response_review_records.json
   — understand what human reviewers approved
3. Read docs/OPEN_RESPONSE_SEMANTIC_REVIEW_BATCH_1.md
   — understand quality expectations
4. Design a deterministic rubric schema (no LLM scoring)
5. Write rubrics for the top 3 question types
```

**Schema requirements**:
- Deterministic: each criterion is a rule, not a judgment
- Governance-safe: no examiner_scoring_allowed = true ever
- Levels: insufficient / partial / adequate / strong
- Each level has explicit criteria (keywords, structure, coverage)

**Deliverables**:
- `docs/OPEN_RESPONSE_OPERATIONAL_RUBRICS.md` — rubric spec and schema
- `knowledge/question-bank/open_response/rubrics/rubric_schema.json` — JSON schema
- `knowledge/question-bank/open_response/rubrics/rubric_batch_1.json` — first 3 rubrics

---

## NEXT (After NOW is complete)

### NEXT-1: Open Response Feedback Templates

**What**: Write structured feedback templates keyed to rubric outcomes.

**Dependencies**: NOW-4 (rubrics) must be done first.

**How**:
```
1. For each rubric level (insufficient/partial/adequate/strong)
   → define a feedback message template
   → include: what was correct, what was missing, what to review next
2. Templates must reference specific knowledge assets (corpus chunks, topics)
3. No freeform LLM generation — all templates are deterministic
```

**Deliverables**:
- `knowledge/question-bank/open_response/feedback_templates/` directory
- `docs/OPEN_RESPONSE_FEEDBACK_TEMPLATE_SPEC.md`

---

### NEXT-2: Open Response Remediation Maps

**What**: Map rubric failure modes to remediation actions (which SBA questions, which knowledge chunks to surface).

**Dependencies**: NEXT-1 (feedback templates), `master_bank.json`.

**How**:
```
1. For each rubric failure category, define:
   → 2–3 SBA questions from master_bank that address the gap
   → 1–2 knowledge corpus references
   → recommended session type (drill / review / exam_pressure)
2. Link to sba_session_composer.py session type parameters
```

**Deliverables**:
- `knowledge/question-bank/open_response/remediation_maps/` directory
- `docs/OPEN_RESPONSE_REMEDIATION_MAP_SPEC.md`

---

### NEXT-3: Knowledge Utilization & Coverage Audit

**What**: Analyze which WSET topics are well-covered vs. under-covered in the master bank.

**How**:
```
1. Read docs/FULL_BANK_CORPUS_VERIFICATION_SUMMARY.md
   — 201 NOT_FOUND items, 181 DISTRACTOR_CONFLICT flags identified
2. Read knowledge/knowledge-map/ contents
3. Cross-reference: which topics have ≥3 strong-grounded items vs. <3?
4. Produce a topic → coverage tier table
5. Identify priority topics for new question development
```

**Deliverables**:
- `docs/KNOWLEDGE_COVERAGE_AUDIT.md` — topic matrix, coverage gaps, priority list

---

## LATER (After NEXT is complete)

### LATER-1: Knowledge Coverage Metrics (automated)

**What**: Turn the coverage audit into a runnable script and test.

**Dependencies**: NEXT-3 (audit).  
**Deliverable**: `tools/question_bank/coverage_metrics.py` + test.

---

### LATER-2: Governed Generation Readiness Audit

**What**: Assess all 8 prerequisites from `SBA_MASTER_BANK_AND_GOVERNED_GENERATION_ROADMAP.md` against current repo state.

**Note**: master_bank.json now exists. Prerequisites 1–2 are met. Assess the remaining 6.  
**Deliverable**: `docs/GOVERNED_GENERATION_READINESS_AUDIT.md`.

---

### LATER-3: Knowledge Asset Registry Architecture

**What**: Design a registry schema for all knowledge assets with coverage, grounding, and pedagogical metadata.

**Dependencies**: LATER-1 (metrics), LATER-2 (generation readiness).  
**Deliverable**: `docs/KNOWLEDGE_ASSET_REGISTRY_ARCHITECTURE.md` + `knowledge/knowledge-map/registry_schema.json`.

---

## FUTURE (No immediate dependency)

### FUTURE-1: Adaptive Architecture Design
Design real-time learner adaptation using session history + master bank. **No code yet.**

### FUTURE-2: Governed Generation — First Cycle
Implement the 5-gate generation pipeline from the roadmap. Requires LATER-2 prerequisites all green.

### FUTURE-3: PSL Activation
Activate `ENABLE_PEDAGOGICAL_STRATEGY_LAYER = True` only after explicit user authorization and full regression test run.

---

## How to Resume a Session After Context Reset

1. Read `CLAUDE_PROJECT_STATUS.md` — understand what exists
2. Read `CLAUDE_STRATEGIC_BACKLOG.md` — understand the queue
3. Read this file — find the first incomplete NOW item
4. Check `git log --oneline -10` via GitHub MCP to verify no new commits changed the state
5. Start work on the first incomplete NOW item

**Do not** rely on conversational memory. **Do not** re-derive status from scratch unless these docs are more than 5 commits stale.

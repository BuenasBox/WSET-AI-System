# Dashboard State Updater — Skill

## When to run

Run this skill after every completed phase or batch of work, when asked by the user.
Never run autonomously or on a schedule. Always confirm with the user before writing.

Trigger phrases:
- "update the dashboard"
- "the phase is complete, update the state"
- "refresh the dashboard state"

---

## What this skill does

1. Reads repo evidence (git log, AGENTS.md, docs/)
2. Derives updated values for `system_state.json`
3. Optionally applies them via the updater script
4. Prints a diff summary for user review
5. The user then commits and pushes manually

---

## Files to read (allowed)

| File / Path | Purpose |
|---|---|
| `git log --oneline` | Latest phase, latest commit hash, latest event |
| `AGENTS.md` | Test count, snapshot count, phase history |
| `docs/` | Phase docs, contract docs, audit docs |
| `frontend/architecture-dashboard/system_state.json` | Current state baseline |
| `knowledge/question-bank/structured/wset3_questions.json` | Question counts |
| `knowledge/knowledge-map/` (non-learner) | Graph node counts |
| `knowledge/config/` | Config asset counts |

---

## Files NEVER to read

| Path | Reason |
|---|---|
| `knowledge/nazareth/` | Private learner state |
| `knowledge/self-eval/attempts/` | Runtime self-eval outputs |
| `knowledge/self-eval/reports/` | Dynamic run reports |
| `knowledge/retrieval-sandbox/` | Derived retrieval outputs |
| `.env`, `.env.*` | Secrets |
| `*.jsonl` | Pipeline stream outputs |

---

## How to update system_state.json

### Option A — Use the script (preferred)

```powershell
# Preview changes only:
python tools/dashboard/update_architecture_dashboard_state.py --dry-run

# Apply changes:
python tools/dashboard/update_architecture_dashboard_state.py --write
```

### Option B — Manual update by Codex

When the user provides explicit values, Codex edits system_state.json directly.
Always show the full diff before writing.

---

## Fields and their sources

| Field | Source |
|---|---|
| `current_phase` | User confirmation or AGENTS.md |
| `latest_phase` | Most recent phase tag in git log |
| `latest_event` | Most recent commit message |
| `latest_commit` | git rev-parse --short HEAD |
| `tests` | AGENTS.md "Test count" line |
| `snapshots` | AGENTS.md snapshot count |
| `maturity` | User-confirmed estimate |
| `phases_completed` | Merged git log phase tags |
| `governance_status.*` | Always 0 / false — immutable |
| `knowledge_assets_count` | Knowledge audit doc or user value |
| `structured_question_count` | Question bank JSON or user value |
| `sba_*_candidates` | SBA audit report or user value |

---

## Governance constraints (never override)

```
governance_violations: 0
llm_dependency: 0
vector_db_dependency: 0
cloud_runtime_dependency: 0
official_examiner_authority: false
```

---

## Verification after writing

```powershell
git diff frontend/architecture-dashboard/system_state.json
git status  # must show only dashboard files changed
python -c "import json; json.load(open('frontend/architecture-dashboard/system_state.json'))"
```

---

## Commit dashboard update

```powershell
git add frontend/architecture-dashboard/system_state.json
git commit -m "chore(dashboard): update system_state to Phase <X>"
git push
```

---

## Deploy to gh-pages (subtree)

```powershell
git subtree push --prefix frontend/architecture-dashboard origin gh-pages
```

If history divergence:
```powershell
git push origin `git subtree split --prefix frontend/architecture-dashboard main`:gh-pages --force
```

---

## What NOT to do

- Do NOT modify backend runtime (tools/retrieval, tools/tutor, tools/orchestrator)
- Do NOT modify knowledge/ files
- Do NOT set governance flags to True
- Do NOT deploy or commit automatically
- Do NOT read private learner state files (knowledge/nazareth/)

# Frontend State Audit

Date: 2026-06-01

Status: Read-only audit. No backend changes. No schema changes. No deployment.

Scope:
- `frontend/architecture-dashboard/` — architecture dashboard
- `frontend/diagnostic-sba/` — SBA cockpit prototype
- `docs/DIAGNOSTIC_SBA_COCKPIT_CONTRACT.md` — frontend/backend contract
- `tools/dashboard/update_architecture_dashboard_state.py` — updater script

---

## 1. Architecture Dashboard Audit

### 1.1 Deployment status

| Item | Status |
|---|---|
| Live URL | `https://epistemiclab.dpdns.org` — confirmed live |
| Repo serving Pages | `github.com/BuenasBox/epistemiclab-dashboard` (public, separate repo) |
| Source branch | `main`, folder `/ (root)` |
| DNS | Cloudflare CNAME `epistemiclab.dpdns.org → buenasbox.github.io` — active |
| HTTPS | Enabled via GitHub Pages |
| robots.txt | Present, all crawlers denied ✓ |
| .nojekyll | Present ✓ |
| CNAME file | `epistemiclab.dpdns.org` ✓ |

### 1.2 Dual-repo structure

The dashboard exists in two locations:

| Location | Purpose |
|---|---|
| `WSET-AI-System/frontend/architecture-dashboard/` | Source of truth, tracked in private repo |
| `epistemiclab-dashboard/` (`C:\Users\esand\OneDrive\Documents\`) | Public deployment repo, separate git |

The `epistemiclab-dashboard/` directory has its own `.git/` and pushes to the
public GitHub Pages repo. The `WSET-AI-System` main repo tracks the same files
under `frontend/architecture-dashboard/` as ordinary files (not a submodule).

**Maintenance rule:** When `system_state.json` or `index.html` change in the
main repo, they must be manually synced to `epistemiclab-dashboard/` and pushed.
The updater script (`tools/dashboard/update_architecture_dashboard_state.py`)
writes only to the main repo path; the operator is responsible for the sync and push.

### 1.3 Stale content in system_state.json

`frontend/architecture-dashboard/system_state.json` was last updated for
Phase 4A.3.7. Multiple fields are now stale.

| Field | Current value in JSON | Actual current value | Severity |
|---|---|---|---|
| `tests` | 660 | **1107** (confirmed by test run 2026-06-01) | HIGH |
| `latest_phase` | `Phase 4A.3.7` | `Phase 4A.3.7.3` (adapter skeleton committed) | MEDIUM |
| `latest_commit` | `5481624` | `6a17a26` | MEDIUM |
| `latest_event` | "Structured Question Bank Compatibility Audit completed" | Adapter skeleton added | MEDIUM |
| `current_recommendation` | "Structured Question Bank Adapter Contract or Diagnostic SBA Cockpit Prototype" | Both complete; next is adapter implementation | MEDIUM |
| `diagnostic_sba_status` | `"pending"` | Prototype committed; contract written — should be `"prototype"` | MEDIUM |
| `in_progress_phase` | `""` | `"Phase 4A.3.7.4"` (if Codex is active) | LOW |

**Action required:** Run `python tools/dashboard/update_architecture_dashboard_state.py --write`
and manually update the fields the script cannot derive (test count from actual run,
diagnostic_sba_status). Then sync to `epistemiclab-dashboard/` and push.

### 1.4 Stale content in index.html (hardcoded fallback values)

The dashboard `index.html` has hardcoded fallback values in the `STATE` object
used when `fetch('./system_state.json')` fails. These are currently stale:

```javascript
var STATE = {
  maturity: 41,          // json shows 50
  tests: 660,            // actual 1107
  latest_phase: 'Phase 4A',  // should be Phase 4A.3.7.3
  latest_commit: '5481624',  // stale
  ...
```

Since the live site fetches `system_state.json` successfully, these fallbacks
are not normally visible. However, they will appear if the JSON fetch fails.
Updating these to match `system_state.json` after each system_state update
is recommended but non-blocking.

### 1.5 Dormant sectors — stale content

The "SECTORES DORMIDOS" section in `index.html` shows:

| Sector | Label in HTML | Actual status |
|---|---|---|
| SECTOR 8-A | "Despliegue Controlado · epistemiclab.dpdns.org · **Hibernando**" | **ACTIVE** — site is live at epistemiclab.dpdns.org |

The footer also reads: `"DNS reservado vía Cloudflare"` but DNS is active
and the site is fully deployed.

These are content accuracy issues. They do not affect functionality or governance.

### 1.6 Subsystems table — missing entries

The "SUBSISTEMAS ACTIVOS" table in `index.html` was authored at Phase 3A.
Several modules added since then are absent:

| Missing subsystem | Module | Phase added |
|---|---|---|
| Banco de Preguntas Estructurado | `tools/question_bank/` | Question bank converter |
| Esquema SBA Diagnóstico | `knowledge/enrichment/diagnostic_sba_item.schema.json` | Phase 4A.2 |
| Modelo de Outcome Diagnóstico | `knowledge/enrichment/diagnostic_outcome.schema.json` | Phase 4A.3.5 |
| Adaptador Banco de Preguntas | `tools/structured_question_bank/structured_question_bank_adapter.py` | Phase 4A.3.7.3 |

These absences are a documentation gap, not a functional risk.

### 1.7 Evolution replay — stale sequence

The `EVOLUTION_REPLAY` array in `index.html` ends at "Fase 3A · Compuertas de
Influencia del Planner". Phases 4A.0 through 4A.3.7.3 are not represented.
The replay animation therefore shows only 7 of ~22 completed phases.

This is a display accuracy issue. The animation still works correctly for what
it shows. No functional risk.

### 1.8 CRLF/LF line ending drift

`git status` reports `frontend/architecture-dashboard/CNAME` and
`frontend/architecture-dashboard/robots.txt` as modified. Diff confirms
this is a CRLF/LF normalization artifact — no content change. The files
on disk have CRLF endings; git expects LF. A `.gitattributes` rule or a
normalizing commit would resolve this.

### 1.9 Dashboard governance assessment

| Check | Status |
|---|---|
| noindex/nofollow meta tags | ✓ present in index.html |
| robots.txt — all crawlers denied | ✓ present |
| No external dependencies | ✓ confirmed |
| No API calls | ✓ confirmed |
| No tracking | ✓ confirmed |
| Governance flags displayed | ✓ (safe_for_examiner, uses_llm, etc.) |
| No official WSET authority claim | ✓ footer disclaimer present |
| No score/grade display | ✓ |

**Dashboard governance: CLEAN.**

---

## 2. Diagnostic SBA Prototype Audit

### 2.1 Blocker verification (post-fix)

| Blocker | Fix applied | Verified |
|---|---|---|
| B1 — Misconception shown on correct answer | `ds-misc` hidden via `display:none` when `isOk`. Reset in `loadQ()`. Section excluded from stagger reveal array. | ✓ |
| B2 — No visible disclaimer | `proto-badge` in header: "PROTOTIPO · ENTRENAMIENTO · NO EVALUACIÓN OFICIAL WSET" | ✓ |

### 2.2 Quality check

| Item | Status |
|---|---|
| Confidence button labels | ✓ Fixed: INSEG / POCO / NEUTRO / SEGURO / MUY SEG |
| "LES Actualizado" claim | ✓ Removed. Now: "Señales Registradas Localmente" |
| Correct answer distribution | ✓ Q1=B · Q2=C · Q3=B · Q4=A |
| Keyboard shortcuts A/B/C/D + Enter | ✓ Functional |
| Mobile scroll-to-diagnostic | ✓ Present (`scrollIntoView` after confirm) |
| Timer color states | ✓ blue → amber (30s) → red (60s) |
| Mastery label qualifier | ✓ "Señal de Maestría · Entrenamiento" |
| governance fields in mock data | ✓ `training_item_only: true`, `safe_for_examiner: false` per question |
| diagnostic_role per option | ✓ `dr` field present on each option |

### 2.3 Contract alignment check

Reference: `docs/DIAGNOSTIC_SBA_COCKPIT_CONTRACT.md`

**Item payload (Section 3.1) vs prototype mock data (`QS` array):**

| Contract field | Prototype mock | Alignment |
|---|---|---|
| `schema_version` | `schema_version` ✓ | Aligned |
| `item_id` | `id` | Key mismatch — expected in Phase 3 migration |
| `curriculum.ra_id` | `ra_id` (flat) | Wrapper absent — expected Phase 1 deviation |
| `curriculum.subtopic` | `subtopic` (flat) | Wrapper absent — expected Phase 1 deviation |
| `curriculum.difficulty` | `dificultad` (Spanish, non-schema enum) | Uses INTERMEDIO/AVANZADO not intermediate/advanced |
| `question.stem` | `stem` (flat) | Wrapper absent — expected Phase 1 deviation |
| `question.expected_reasoning_type` | `expected_reasoning_type` (flat) | Wrapper absent — expected Phase 1 deviation |
| `options[].option_id` | `opts[].id` | Key mismatch — expected Phase 3 migration |
| `options[].option_text` | `opts[].txt` | Key mismatch — expected Phase 3 migration |
| `options[].diagnostic_role` | `opts[].dr` (abbreviated) | Key mismatch — expected Phase 3 migration |
| `governance.*` | `governance.*` ✓ | Aligned |
| Pre-submission strip of `is_correct` | NOT applied — `correcta` embedded | Expected Phase 1 deviation; documented in contract §3.3 |

All deviations are **expected Phase 1 static-prototype deviations** documented
in contract Section 2.2 and the migration plan (Section 10). None are bugs.

**Attempt payload (Section 4.1):**

The prototype captures all required fields but does not build or send the
attempt payload. State object holds: `S.sel`, `S.tFinal` (seconds not ms),
`S.hesit`, `S.conf` (1–5 not low/medium/high). These must be transformed
at Phase 3 migration:

| Schema field | Prototype captures | Transform needed |
|---|---|---|
| `selected_option_id` | `S.sel` ✓ | None |
| `response_time_ms` | `S.tFinal` (seconds) | Multiply by 1000 |
| `answer_changed` | `S.hesit > 0` ✓ | `Boolean(S.hesit > 0)` |
| `hesitation_count` | `S.hesit` ✓ | None |
| `confidence_self_report` | `S.conf` (1–5) | Map via `mapConfidence()` (Section 8.4) |
| `attempt_id` | Not generated | Add at Phase 3 |
| `session_id` | Not generated | Add at Phase 3 |

**Diagnostic outcome (Section 5.1):**

The prototype approximates the outcome using embedded `q.diag.*` fields.
The `display.*` block from the contract does not exist yet — its content is
hand-coded inline in `showDiag()`. Correct at Phase 1; must be replaced at
Phase 3.

**Governance gate (Section 7.3):**

The `safe_for_examiner` and `training_diagnostic_only` runtime checks defined
in the contract are NOT yet implemented in the prototype. They are required
before Phase 3. Prototype is Phase 1 — acceptable.

### 2.4 No backend assumptions check

| Check | Status |
|---|---|
| No HTTP fetch calls | ✓ — no `fetch()`, no `XMLHttpRequest` |
| No API keys, tokens, or credentials | ✓ |
| No Supabase imports | ✓ |
| No external script tags | ✓ |
| No CDN dependencies | ✓ (font fallback chain is local-first) |
| No hidden scoring authority | ✓ |
| Comment documents planned fetch path | ✓ ("En producción: reemplazar con fetch('./preguntas.json')") |

**Prototype governance: CLEAN.**

### 2.5 Prototype functional coverage

Verified interaction paths:

- ✓ Question loads, timer starts
- ✓ Keyboard A/B/C/D selects option
- ✓ Changing selection increments hesitation counter
- ✓ Confidence selector optional, confirm enabled without it
- ✓ Enter confirms answer
- ✓ Options lock: correct = green, selected-wrong = red, others fade
- ✓ Misconception panel hidden when answer is correct
- ✓ Misconception panel visible when answer is wrong
- ✓ Causal chain collapsed by default, expandable
- ✓ Stagger reveal sequence correct (veredicto → distractor → misc? → causal → SAT → remed → next)
- ✓ Next question advances session
- ✓ Session complete overlay shows without "LES Actualizado"
- ✓ Reset restores state cleanly

---

## 3. Deployment Status

| Artifact | Deployment path | Live URL | Status |
|---|---|---|---|
| Architecture dashboard | `epistemiclab-dashboard` repo → GitHub Pages → `epistemiclab.dpdns.org` | https://epistemiclab.dpdns.org | ✓ LIVE |
| Diagnostic SBA prototype | Local file only, not deployed | `frontend/diagnostic-sba/index.html` | LOCAL ONLY |
| `system_state.json` (deployed) | Synced to `epistemiclab-dashboard/` + pushed | Part of live dashboard | STALE (tests=660, should be 1107) |

### Deployment sync gap

The `system_state.json` in the main `WSET-AI-System` repo was updated via
the state updater (commit `90692e4`) to show tests=660. Since then, the
adapter tests added 447 more (total now 1107). The deployed dashboard is
visually incorrect on the test count.

---

## 4. Governance Status

| Artifact | Governance | Risk level |
|---|---|---|
| Architecture dashboard | noindex/nofollow enforced, no external deps, no authority claims | LOW |
| SBA prototype | training_item_only=true in mock data, disclaimer visible, no LES claim | LOW |
| system_state.json | No sensitive data, no learner state, no LES path | LOW |
| Contract document | Design-only, no implementation, governance boundaries explicit | NONE |
| Updater script | Read-only from safe paths, writes only to dashboard directory | LOW |

No governance violations detected across any frontend artifact.

---

## 5. Contract Alignment Summary

`docs/DIAGNOSTIC_SBA_COCKPIT_CONTRACT.md` defines 4 migration phases.

| Phase | Contract section | Prototype compliance | Gap |
|---|---|---|---|
| Phase 1 — Static prototype | §10.1 | ✓ Complete | None — Phase 1 is the current state |
| Phase 2 — preguntas.json | §10.2 | Not yet started | Requires ≥5 validated items from adapter |
| Phase 3 — HTTP endpoint | §10.3 | Not yet started | Requires Phase 4A.7 Attempt Analyzer |
| Phase 4 — Supabase persistence | §10.4 | Not yet started | Separate decision required |

---

## 6. Unresolved Frontend Risks

**RISK 1 — system_state.json stale (HIGH)**
Tests show 1107 but deployed dashboard shows 660. The state updater script
exists but has not been run since the adapter tests were added. This is
the most visible discrepancy: the dashboard claims 660 verified tests when
1107 pass. Fix: run the updater, manually correct the test count field,
sync to `epistemiclab-dashboard/` and push.

**RISK 2 — Dormant sector 8-A incorrect (MEDIUM)**
`index.html` labels "Despliegue Controlado · epistemiclab.dpdns.org" as
"Hibernando". The site is live. This is a content accuracy issue, not a
governance risk. Fix: requires an `index.html` edit (change "Hibernando"
to "ACTIVO" for SECTOR 8-A, update footer DNS note).

**RISK 3 — EVOLUTION_REPLAY stops at Phase 3A (LOW)**
The animated evolution replay in the dashboard only shows 7 phases. Phases
4A.0–4A.3.7.3 are not represented. Cosmetic issue, no functional impact.

**RISK 4 — Phase 2 cockpit migration blocked (MEDIUM)**
The contract's Phase 2 (preguntas.json) requires at least 5 validated items
from the adapter output. The adapter skeleton (Phase 4A.3.7.3) exists but
the adapter is not yet functional. Until the adapter can output
schema-validated items, Phase 2 migration cannot proceed.

**RISK 5 — Prototype answer_changed capture mismatch (LOW)**
The prototype captures `hesitation_count` as an int. The outcome schema
requires `answer_changed` as a boolean. The transform is trivial
(`hesitation_count > 0`) but it has not been implemented yet because no
attempt payload is sent in Phase 1. Must be implemented before Phase 3.

**RISK 6 — Governance gate not yet implemented in prototype (LOW)**
Contract Section 7.3 defines a runtime governance check:
`if (outcome.governance.safe_for_examiner === true) → showError()`.
This check is absent from the current prototype. Acceptable for Phase 1
(no backend response to validate). Required before Phase 3.

**RISK 7 — difficulty enum mismatch (LOW)**
Prototype uses `INTERMEDIO / AVANZADO` (Spanish, uppercase) where the
item schema specifies `intermediate / advanced` (English, lowercase).
No functional impact in Phase 1. Must be normalized at Phase 2 when
items are loaded from validated JSON.

---

## 7. Readiness Assessment

### READY NOW

| Artifact | Condition |
|---|---|
| Architecture dashboard at `epistemiclab.dpdns.org` | Live. DNS active. Governance clean. |
| SBA prototype as local static file | No blockers. Opens in any browser. |
| Frontend/backend contract | Written, committed, signed off. |
| Dashboard updater script | Functional. Awaiting next run. |

### READY AFTER system_state.json UPDATE (immediate — before next session)

| Artifact | Blocked by |
|---|---|
| Deployed dashboard showing accurate test count | Run updater + sync + push |
| Sector 8-A showing ACTIVO | index.html edit + sync + push |
| Footer DNS note updated | index.html edit + sync + push |

### READY AFTER ADAPTER OUTPUT (Phase 4A.3.7.4+)

| Artifact | Blocked by |
|---|---|
| `preguntas.json` (cockpit Phase 2) | Adapter must output ≥5 schema-validated items |
| `diagnostic_compatible_count` > 0 in system_state | Adapter must produce validated items |
| Cockpit `fetch('./preguntas.json')` migration | Phase 2 items must exist |

### READY AFTER ATTEMPT ANALYZER (Phase 4A.7)

| Artifact | Blocked by |
|---|---|
| Cockpit Phase 3 (HTTP endpoint) | Analyzer must compute `diagnostic_outcome_v1` |
| Governance gate implementation | Backend endpoint must exist to validate against |
| Actual `response_time_ms` payload | Attempt POST endpoint must exist |
| `confidence_alignment` display | Backend classification required |

### READY AFTER LES INTEGRATION (Phase 4B+)

| Artifact | Blocked by |
|---|---|
| Session persistence across reloads | Backend session model |
| Cross-session mastery signal | LES write-back |
| "Señales enviadas al LES" confirmed message | Backend LES integration |

---

## 8. Recommended Next Frontend Phase

**Only one recommendation.**

### Phase 2 Cockpit Migration — `preguntas.json`

This is the highest-value next frontend step after Codex completes Phase 4A.3.7.3.

**Prerequisite:** Phase 4A.3.7.4 — the adapter must be able to output at
least 5 schema-validated `diagnostic_sba_item_v1` items.

**Frontend work (minimal, low risk):**

1. Create `frontend/diagnostic-sba/preguntas.json` populated with validated
   items from the adapter output.
2. Replace the embedded `var QS = [...]` block in `index.html` with:
   ```javascript
   fetch('./preguntas.json')
     .then(function(r) { return r.json(); })
     .then(function(d) { QS = d.questions; loadQ(0); })
     .catch(function() { showError('No se pudo cargar las preguntas.'); });
   ```
3. Add LOADING and ERROR states to the UI state machine.
4. Normalize the `difficulty` enum from Spanish to schema-aligned English
   (INTERMEDIO → intermediate, AVANZADO → advanced).
5. Normalize option key names: `id` → `option_id`, `txt` → `option_text`.

**Why this and not Phase 3:**
Phase 3 (HTTP endpoint) requires Phase 4A.7 Attempt Analyzer, which is a
significant backend implementation. Phase 2 only requires the adapter to
output JSON — a much smaller dependency. Phase 2 also validates that the
item schema format is correct before introducing HTTP complexity.

**Why this and not dashboard updates:**
Dashboard updates (test count, sector 8-A, etc.) are maintenance tasks, not
a frontend phase. They should happen before Phase 2 begins but are not
"the next frontend phase."

**Dependency:** Phase 4A.3.7.4 must complete and produce validated items
before Phase 2 can start. If Phase 4A.3.7.4 is what Codex is working on,
Phase 2 is the direct successor.

---

## 9. Frontend Health Summary

| Dimension | Score | Notes |
|---|---|---|
| Dashboard deployment | GREEN | Live at epistemiclab.dpdns.org |
| Dashboard content accuracy | AMBER | Test count stale (660 vs 1107), sector 8-A label incorrect |
| Dashboard governance | GREEN | No violations |
| Cockpit prototype correctness | GREEN | Blockers fixed, governance clean |
| Cockpit contract alignment | GREEN | Phase 1 deviations are expected and documented |
| Cockpit readiness for Phase 2 | AMBER | Blocked on adapter output |
| Frontend risks | LOW | 7 risks identified, all manageable, none blocking |

---

*This audit does not authorize any backend, schema, retrieval, or LES changes.
Frontend changes limited to `frontend/` and `docs/`. Governance invariants
in `docs/DIAGNOSTIC_SBA_GOVERNANCE_CONTRACT.md` remain in force.*

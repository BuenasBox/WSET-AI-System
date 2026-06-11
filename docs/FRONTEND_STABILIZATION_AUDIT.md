# FRONTEND STABILIZATION AUDIT — Phase Z.2

**Date:** 2026-06-10
**Scope:** Production frontend at epistemiclab.dpdns.org (repo `epistemiclab-dashboard`, commit `b0c2b69`, main = origin/main)
**Method:** Runtime verification, not static analysis. The deployed code was served locally and driven with a real headless Chromium (puppeteer-core + CDP). Every finding below was reproduced with real clicks, real navigation, real mode changes, real sessions. Console/page errors were captured for every interaction. Question IDs and error texts are verbatim runtime output.

**Status legend:** 🔴 BROKEN (learner blocked) · 🟠 PLACEBO (visible but no real behavior) · 🟡 DEGRADED (works with defects) · 🟢 WORKING

---

## 0. Executive summary

| Experience | Verdict |
|---|---|
| Adaptive Session — SBA modes (Express/Estándar/Mock 50) | 🔴 All 3 blocked by a JS crash; even past the crash, zero answer options render (second crash-level defect) |
| Adaptive Session — SAT modes (Sprint/Practice/Mock) | 🟢 Work end-to-end, incl. 30-min timer |
| Diagnostic SBA | 🔴 Session can never advance past question 1 (infinite stage loop) |
| Open Response Lab | 🔴 100% non-functional — every render crashes; no question ever displays |
| Full Simulation | 🟢 SBA/OR/SAT phases all render and advance |
| Global navigation (header) | 🔴 Unclickable on 3 of 4 experiences (covered by fixed governance banner) |
| Mentor system | 🟠 Cosmetic — all 3 mentors emit identical placeholder text |
| Feedback panels (Cadena causal/Trampas/Misconception/SAT) | 🟠 Always "—" — source fields are 0/523 populated in the deployed bank |
| Pressure mode | 🟢 Real behavior (timers 45s vs 90/120s) |
| RA filters | N/A — no RA selector control exists in production; mock RA blueprint internally correct |

**Root-cause pattern:** Phase Y.0 deployed a regenerated 523-item bank (`preguntas_data.js`, `session_bank.js`) and a regenerated ORL payload whose schemas do not match what the page renderers were written against. Most breakage is contract drift between data generators and UI code, plus one CSS stacking bug.

**Separate finding (local machine, not production):** the local worktree at `C:\Dev\epistemiclab-dashboard` had all four experience HTML files truncated mid-token (e.g. `adaptive-session/index.html` ended at `onclick="fin`). Production (origin/main) was unaffected. The worktree was restored to HEAD before this audit. Cause unknown — likely an interrupted local write. Re-check file integrity before any future deploy.

---

## ISSUE #1 — Adaptive Session blocked at "MISIÓN DE ENTRENAMIENTO" — 🔴 CRITICAL — CONFIRMED

- **URL:** `/adaptive-session/`
- **Control:** Mode buttons Express·10, Estándar·25, Mock Theory Part 1·50 → INICIAR MISIÓN
- **Expected:** Selecting a mode shows the briefing with a start button; session begins.
- **Actual (runtime):** All 3 SBA modes throw and the start button is never rendered. Captured page error, identical for `express_10`, `standard_25`, `mock_theory_50`:
  `TypeError: Cannot read properties of undefined (reading 'toUpperCase')`
  DOM state after click: `startBtn: []`, `meta: null` — briefing cards and objective render, then nothing.
- **Root cause:** `buildSBA()` (index.html ~line 1356) constructs `mission_briefing` **without** `training_type`. `renderScreen0()` (line 968–969) executes `b.training_type.toUpperCase()` *before* appending the INICIAR MISIÓN button (line 973). The exception aborts rendering exactly between the objective block and the button — which is why the learner sees Áreas fuertes/débiles/Misconceptions/Brechas causales/Objetivo but cannot continue.
- **Second blocker behind the first:** with `training_type` patched in at runtime, INICIAR MISIÓN appears and screen-1 loads the stem — but **0 option buttons** render (`#options-wrap` empty, CONFIRMAR hidden). Cause: `renderQuestion()` (line 1038) reads `q.options[letter]` expecting an **object keyed A–D**; `buildSBA()` (line 1363) emits an **array** of `{label,text}`. `array['A']` → undefined → every option skipped.
- **Third defect behind that:** `renderFeedback()` expects `q.feedback.explanation` (object); `buildSBA()` (line 1366) emits the **string** `'Repasa el concepto relacionado con esta pregunta.'` → explanation panel would render empty even if options worked.
- **SAT modes:** 🟢 verified working — sat_sprint (Vino 1 de 1 → Finalizar → "Práctica SAT completada"), sat_practice (1 de 2 → Siguiente → Finalizar), sat_mock (timer rendered and counting, 2 wines, completes). Zero page errors.
- **"Mi Progreso":** 🟢 toggles and renders cold-start message correctly.
- **Proposed fix (minimal, no new features):**
  1. Add `training_type: 'refuerzo'` (or derived value) to `mission_briefing` in `buildSBA()` — or make `renderScreen0()` null-safe.
  2. In `buildSBA()`, emit `options` as `{A:..., B:..., C:..., D:...}` to match the renderer (or adapt the renderer; pick one contract).
  3. Emit `feedback` as `{explanation: ...}` shape.
  4. Add regression: a headless test that clicks each of the 6 modes and asserts question 1 renders ≥2 options with no page errors.

---

## ISSUE #2 — Global navigation broken — 🔴 CRITICAL — CONFIRMED (root cause: overlay stacking, not hrefs)

- **URLs:** `/diagnostic-sba/`, `/adaptive-session/`, `/open-response-lab/` (header + footer navs); `/full-simulation/` is 🟢.
- **Expected:** SBA Cockpit / Adaptive Session / Open Response Lab / Simulacro links navigate.
- **Actual (runtime):** All `href`s are correct (`/diagnostic-sba/`, `/adaptive-session/`, `/open-response-lab/`, `/full-simulation/`). But hit-testing (`document.elementFromPoint` at each link center) shows clicks never reach the links:
  - Header nav on diagnostic-sba, adaptive-session, open-response-lab: intercepted by **`.gov-banner`** (the fixed governance banner, `position:fixed; top:0; z-index:1000`). The nav is the first in-flow element at `top:0, height:47px`, fully underneath the banner. Real click test: clicking "Adaptive Session" from diagnostic-sba → **navigation timeout, URL unchanged**.
  - Footer nav on diagnostic-sba: intercepted by **`#mode-overlay`** (fullscreen mode selector overlay) while it is active.
  - Footer nav on adaptive-session: intercepted by **`.adp-ol`** overlay (label `adp-slabel`) while active.
  - Net effect: on the landing state of diagnostic-sba and adaptive-session, and at all times on open-response-lab's single nav, **no navigation control is clickable at all**.
  - `/full-simulation/`: nav sits at `top:55px` (page has banner offset) — all 4 links clickable. This is the reference implementation.
- **Hub (`/` index.html):** contains exactly **1** link (`./diagnostic-sba/`); Adaptive Session, ORL and Simulacro are unreachable from the hub.
- **Proposed fix:** add top padding/margin (≈30px, as full-simulation does) so the nav clears the fixed banner on the other 3 pages; render overlays *below* nav or give the nav `position:relative; z-index:1100` above overlays; add the 3 missing links to the hub. Verify with the same elementFromPoint probe.

---

## ISSUE #3 — Diagnostic SBA question repetition — 🔴 CRITICAL — CONFIRMED (stage-machine loop, not queue duplication)

- **URL:** `/diagnostic-sba/`
- **Expected:** REVELAR → "Continuar → Micro-entrenamiento SBA" → drill → next question.
- **Actual (runtime, real IDs):** Session `quick_drill` = `[wset3_78, …]`. Answered q1 (`wset3_78`), reached REVELAR, clicked "Continuar → Micro-entrenamiento SBA" → **returned to LEER of the same question**: `{stage:'read', questionIndex:0, qid:'wset3_78', counter:'Pregunta 1 de 5'}`. Repeated the full cycle a second time → again `{questionIndex:0, qid:'wset3_78'}`. **The learner can never reach question 2 in any mode.**
- **Root cause:** `renderTrain()` (line ~1956): `const drill=q.micro_drill||null; if(!drill){goToRead();return;}` — and `micro_drill` is populated for **0/523** items in the deployed bank. The only "Siguiente pregunta →" button in the whole flow lives inside `renderTrain()`, so when the drill is absent the stage machine bounces back to `read` of the same question. The reported "same question appears repeatedly" is this loop.
- **Queue generation itself is 🟢:** no duplicate `id`/`source_question_id` in the bank (523 unique); fresh-first rotation verified — two consecutive quick_drill sessions had **zero ID overlap** (`wset3_483, wset3_478, wset3_51, wset3_54, wset3_510` vs `wset3_224, wset3_105, wset3_232, wset3_24, wset3_246`); localStorage recents save/load works.
- **Proposed fix:** in `renderTrain()`, when `micro_drill` is absent, skip the TRAIN stage and advance: render a pass-through with "Siguiente pregunta →" (`nextQuestion()`) instead of `goToRead()`. One-line behavioral change; add regression test asserting questionIndex increments across the full stage cycle.

---

## ISSUE #4 — Mentor system static — 🟠 PLACEBO — CONFIRMED

- **URL:** `/diagnostic-sba/` (selector `#mentorMode`), `/adaptive-session/` (mentor hint on wrong answers)
- **Expected:** Entrenador Técnico / Mentor Guía / Revisor Estricto materially change feedback.
- **Actual (runtime):** Switching mentor changes **only the panel title**. Captured with all three values on the same question:
  - Mentor Guía → "Repasa el concepto relacionado con esta pregunta."
  - Revisor Estricto → "Repasa el concepto relacionado con esta pregunta."
  - Entrenador Técnico → "Repasa el concepto relacionado con esta pregunta."
- **Root cause:** line 1844: `const _fbm=q.feedback_by_mode||{}; const feedback=_fbm[STATE.mentorMode]||_fbm.mentor||'Repasa el concepto…'` — and `feedback_by_mode` is populated for **0/523** deployed items, so the fallback always wins. The mentor selector has no data to differentiate on.
- **Mentor challenge repetition:** the CONTRASTE stage challenge is `q.cross_exam_challenge || '¿Tu razonamiento cubre causa, mecanismo y efecto?'` (line 1766); `cross_exam_challenge` = **0/523** → the same sentence for every question. Verified on `wset3_*` q1 and q2: identical string.
- **Adaptive mentor hint:** single static English hint (`DISTINCTION_COACH.mentor_hints.MCQ_strategy.hint`, "For MCQ, eliminate clearly wrong options first…") shown on every wrong answer — static AND untranslated.
- **Proposed fix (per sprint rule "wire correctly or remove"):** since the data does not exist, either (a) generate `feedback_by_mode`/`cross_exam_challenge` into the bank export pipeline (data work, not UI), or (b) hide the mentor selector and the static challenge until data ships. Interim minimum: derive mode-differentiated text from existing fields (topic + RA) so the selector isn't a placebo, and translate the MCQ hint.

---

## ISSUE #5 — Empty SBA feedback panels — 🟠 PLACEBO — CONFIRMED, cause (B): data never reaches runtime

- **URL:** `/diagnostic-sba/` REVELAR stage
- **Runtime capture:** Cadena Causal nodes = `["—","—","—"]`; Trampas de distractor = "—"; Misconception frecuente = "—"; Relevancia SAT = "—".
- **Population rates in deployed `preguntas_data.js` (523 items):**

| Field | Populated | Rate |
|---|---|---|
| `causal_chain` | 0/523 | 0% |
| `distractor_traps` | 0/523 | 0% |
| `misconception` | 0/523 | 0% |
| `cross_exam_challenge` | 0/523 | 0% |
| `sat_relevance` | 0/523 | 0% |
| `feedback_by_mode` | 0/523 | 0% |
| `micro_drill` | 0/523 | 0% |

  Item schema actually shipped: `id, source_question_id, topic, ra, difficulty, text, options, correct_index, correct_letter, keywords, gold, governance`. The legacy `preguntas.json` (36 items) also lacks all 7 fields. The renderers were written for a richer schema that has never existed in production.
- **Cause classification:** (B) — data never reaches runtime because it doesn't exist in any deployed bank. The renderer is fine.
- **Proposed fix:** hide each panel when its field is empty (`if (!q.causal_chain) skip block`), so the REVELAR screen shows only real content. Re-enable per-panel automatically when the bank export starts including the fields. No placebo "—" panels.

---

## ISSUE #6 — Revisor Estricto placeholder — 🟠 CONFIRMED (same root as #4/#5)

- The text "Repasa el concepto relacionado con esta pregunta." is the hard fallback at line 1844, reached for 100% of items because `feedback_by_mode` is 0/523. The identical string is also **hardcoded as the feedback for every question** in adaptive `buildSBA()` (line 1366).
- **Proposed fix:** same as #4. At minimum, replace the universal fallback with question-specific deterministic text assembled from fields that DO exist (`topic`, `ra`, `keywords`, correct option text) — e.g. "Tema: maridaje · RA2 · La opción correcta se apoya en: <keywords>". No generic placeholder.

---

## ISSUE #7 — RA filters — VERDICT: control does not exist; internal blueprint 🟢

- **Finding:** there is **no learner-facing RA selector** in any deployed experience. The only `<select>` in diagnostic-sba is `#mentorMode`; adaptive-session has zero selects. RA1–RA5 appear only as static text in the Mock Theory mode description.
- **Internal RA blueprint (runtime evidence):** `loadMode('mock_theory_1')` → 50 questions, distribution `{RA1:8, RA2:28, RA3:5, RA4:5, RA5:4}` — exact match to spec. Sample IDs: `wset3_325, wset3_824, wset3_502, wset3_261, wset3_339, wset3_421`. Adaptive `buildSBA('mock_theory_50')` → identical distribution `{RA1:8, RA2:28, RA3:5, RA4:5, RA5:4}`.
- **Conclusion:** the reported "RA selectors may not affect question selection" refers to a control that isn't in production. Nothing to fix at runtime; if an RA filter is desired it is new scope (excluded from this sprint). Document its absence.

---

## ISSUE #8 — Pressure mode — 🟢 REAL BEHAVIOR — CONFIRMED

- **URL:** `/diagnostic-sba/`, toggle "Presión".
- **Runtime evidence:** Pressure ON → LEER timer total = **45 s**; OFF → **90 s** (read) — captured from live timer state. Code also sets CONFIRMAR stage 45 s vs 120 s. Badge updates (⬤ Activado/Desactivado) and the prepare-stage metadata reflects state.
- **Verdict:** not cosmetic. No fix needed. (Optional polish: surface the time budget on the toggle so the effect is visible before entering a question.)

---

## ISSUE #9 — Open Response Lab broken — 🔴 CRITICAL — CONFIRMED

- **URL:** `/open-response-lab/`
- **Actual (runtime):** stem = `""` (empty), topic/RA never set, only the textarea (static HTML) visible. Page error on load, repeated on every interaction:
  `TypeError: Cannot read properties of undefined (reading 'item_ids')` (×2 on initial load).
- **Root cause:** session-key contract drift. UI state defaults/buttons use keys `short_practice | standard_practice | extended_practice | mock_theory_2`. The deployed `lab_payload.js` `sessions` object contains only `short | standard | long` (sizes 3/5/10). `currentSession()` → `payload.sessions['short_practice']` → `undefined` → `currentItem()` line 381 throws before any DOM update. **Every** render call dies, so every control on the page is dead.
- **Proposed fix:** regenerate `lab_payload.js` with the four UI session keys (the payload generator in WSET-AI-System owns this contract — note `tools/frontend/patch_dashboard_html.py` already references `mock_theory_2`), or map keys in `loadState()/startSession()` with a validation fallback: if `payload.sessions[name]` is missing, fall back to the first available session and log. Add a boot-time contract assert (keys ⊆ payload.sessions) that renders a visible error instead of dying silently.

---

## ISSUE #10 — ORL session mode buttons — 🔴 CONFIRMED (same root as #9)

- **Runtime evidence:** all four buttons fire their click handlers (events attach; `startSession()` runs) but each render crashes with the same `item_ids` TypeError; `aria-pressed` remains on `short_practice` for all four because `render()` dies before updating it. Buttons *appear* inactive; they are actually wired but the payload kills them.
- **Fix:** same as #9. After the key fix, verify each button regenerates a session with mode-specific size and `aria-pressed` moves.

---

## ISSUE #11 — ORL session counts wrong — 🔴 CONFIRMED

- **Runtime evidence:** "Pregunta 1 de 3" is **hardcoded static markup** (index.html line 258). Because `render()` always crashes (#9), the text is never updated — the learner sees "1 de 3" regardless of mode. Additionally, even with keys fixed, payload sizes are `short:3, standard:5, long:10` while the UI advertises `1 / 2 / 4 / 4` — the regenerated payload also drifted from the approved mode sizes.
- **Fix:** correct the payload sessions to the configured sizes (1/2/4/4 per CLAUDE.md mode spec) when regenerating; replace static placeholder with an em-dash or loading state so a stale count can never display.

---

## ISSUE #12 — Spanish localization — 🟡 CONFIRMED (mixed-language UI)

Learner-visible English strings captured at runtime:

| Page | English strings |
|---|---|
| All 4 navs | "SBA Cockpit", "Adaptive Session", "Open Response Lab" |
| diagnostic-sba | "Quick Drill", "Express", "Mock Theory · Parte 1" |
| adaptive-session | "Mock Theory Part 1", "SAT Sprint", "SAT Practice", "SAT Mock Exam" |
| open-response-lab | "Short Practice", "Standard Practice", "Extended Practice", "Mock Theory Part 2" (mode buttons + `labelForSession()` labels) |
| adaptive (feedback) | Mentor hint shown to learner is fully English: "For MCQ, eliminate clearly wrong options first. …" |
| coach_data.js | All `DISTINCTION_COACH` hints/`common_errors` are English; they surface in learner-facing coach panels (adaptive SAT finish, ORL coach, full-sim) |

- **Proposed fix:** single localization pass: nav labels (e.g. "Cabina SBA · Sesión Adaptativa · Laboratorio de Respuesta Abierta · Simulacro"), mode buttons ("Práctica corta · 1", etc.), and translate `coach_data.js` learner-facing strings (keys/structure unchanged so LI logic is untouched). Keep technical governance strings as-is.

---

## ISSUE #13 — Control inventory

URLs abbreviated: SBA=`/diagnostic-sba/`, ADP=`/adaptive-session/`, ORL=`/open-response-lab/`, SIM=`/full-simulation/`, HUB=`/`.

| Control | Page | Visible | Working | Status | Evidence |
|---|---|---|---|---|---|
| Mode: Quick Drill 5 / Express 10 / Estándar 25 / Mock 50 | SBA | ✔ | Partially | 🟡 | Sessions generate w/ correct sizes & RA blueprint; flow then dead-ends at q1 (Issue #3) |
| Stage flow PREPARAR→LEER→CONFIRMAR→CONTRASTE→REVELAR | SBA | ✔ | ✔ | 🟢 | Walked end-to-end, no errors |
| TRAIN stage → next question | SBA | ✔ | ✘ | 🔴 | Loops to same question (`wset3_78` twice) — Issue #3 |
| Mentor selector (3 modes) | SBA | ✔ | ✘ | 🟠 | Title changes, body identical — Issue #4 |
| Pressure toggle | SBA | ✔ | ✔ | 🟢 | 45 s vs 90/120 s timers — Issue #8 |
| Confidence buttons (4) + reasoning microtags (4) | SBA | ✔ | ✔ | 🟢 | Enable commit; overconfidence banner logic present |
| Commit / Confirmo / Cambiar respuesta / hardLock | SBA | ✔ | ✔ | 🟢 | All advance stages correctly |
| Feedback panels ×4 (causal/trampas/misconception/SAT) | SBA | ✔ | ✘ | 🟠 | Always "—", 0/523 data — Issue #5 |
| Cross-exam challenge text | SBA | ✔ | ✘ | 🟠 | Static for all questions — Issue #4 |
| Restart / mapa cognitivo | SBA | ✔ | unreachable | 🔴 | Behind the Issue #3 loop; cannot be reached by a learner |
| Mode: Express/Estándar/Mock 50 | ADP | ✔ | ✘ | 🔴 | TypeError, no start button — Issue #1 |
| INICIAR MISIÓN | ADP | ✘ (never renders) | ✘ | 🔴 | Issue #1 |
| SBA question options | ADP | ✘ (0 options) | ✘ | 🔴 | options array/object mismatch — Issue #1 |
| Mode: SAT Sprint/Practice/Mock | ADP | ✔ | ✔ | 🟢 | All complete end-to-end |
| SAT timer (mock) | ADP | ✔ | ✔ | 🟢 | Counts down, color shift logic present |
| Siguiente → / Finalizar ✓ (SAT) | ADP | ✔ | ✔ | 🟢 | Wine 1→2→completion verified |
| Mi Progreso toggle | ADP | ✔ | ✔ | 🟢 | Renders cold-start analysis panel |
| Mentor hint (wrong answer) | ADP | ✔ | static | 🟠 | Single English hint — Issues #4/#12 |
| Session mode buttons ×4 | ORL | ✔ | ✘ | 🔴 | Handlers fire, render crashes — Issues #9/#10 |
| Question stem/topic/RA display | ORL | ✘ | ✘ | 🔴 | Never populated — Issue #9 |
| Enviar/Siguiente/Finalizar/Reiniciar | ORL | ✔ | ✘ | 🔴 | All call `render()` → same crash |
| Question counter | ORL | ✔ | ✘ | 🔴 | Static "1 de 3" — Issue #11 |
| Iniciar Simulacro | SIM | ✔ | ✔ | 🟢 | Starts Part 1, timer 75:00 |
| SBA phase (50q) options/confirm/next | SIM | ✔ | ✔ | 🟢 | Q1→Q2 advance verified |
| OR phase (4 items) | SIM | ✔ | ✔ | 🟢 | Real stems render (graceful fallback around ORL payload drift) |
| SAT phase (2 wines) | SIM | ✔ | ✔ | 🟢 | Wine + textarea render |
| Header nav links ×4 | SBA, ADP, ORL | ✔ | ✘ | 🔴 | Covered by gov-banner; click test timed out — Issue #2 |
| Header nav links ×4 | SIM | ✔ | ✔ | 🟢 | elementFromPoint clean |
| Footer nav links ×4 | SBA, ADP | ✔ | ✘ while overlay active | 🔴 | Covered by mode overlays — Issue #2 |
| Hub links to experiences | HUB | partial | ✘ | 🔴 | Only 1 of 4 experiences linked |
| REPRODUCIR EVOLUCIÓN | HUB | ✔ | untested | — | Dashboard-internal, not learner-facing |

---

## Fix plan (proposed order, after approval)

1. **ORL payload contract** (#9/#10/#11) — regenerate `lab_payload.js` with UI session keys + approved sizes; add boot assert. Unblocks an entire experience with a data-only change.
2. **Adaptive buildSBA contract** (#1) — `training_type`, options object shape, feedback object shape. Unblocks 3 modes.
3. **SBA TRAIN loop** (#3) — pass-through to `nextQuestion()` when no `micro_drill`. One-line. Unblocks all SBA sessions.
4. **Nav stacking** (#2) — banner offset on 3 pages + overlay z-order + hub links.
5. **Placebo removal** (#4/#5/#6) — hide empty panels; question-specific fallback feedback; hide or data-back the mentor selector.
6. **Localization pass** (#12).
7. **Regression harness** — keep the headless click-through scripts (mode start, stage advance, nav hit-test, ORL render) as a pre-deploy gate so "exists visually but doesn't work" can't ship again.

Each step: implement → re-run the runtime probes above → only then commit. Both repos pushed only after all gates green, per sprint protocol.

---

*Formative training audit document. No WSET assessment or examiner authority. safe_for_examiner: false.*

## FIX LOG — Phase Z.2 stabilization sprint (2026-06-10, post-approval)

All fixes verified by the headless regression gate (`tools/frontend/regression_gate/gate.mjs`) — real clicks in headless Chromium against the deploy candidate. Final run: **G1–G8 ALL GREEN**.

1. **ORL payload contract (#9/#10/#11)** — `lab_payload.js` sessions rekeyed to `short_practice/standard_practice/extended_practice/mock_theory_2` with approved sizes 1/2/4/4 (existing items + evaluation data preserved; mock approximates official with 3×RA1 + 1×RA5). `validSessionName()` boot guard added; static counter placeholder neutralized. Evidence: 4 modes render correct counts; full 4-question walk + finish + restart; 0 page errors. *Note: `tools/frontend/generate_production_payloads.py` emits the right keys but omits `evaluation_by_item_id` — reconcile before next regeneration.*
2. **Adaptive buildSBA contract (#1)** — `training_type` added to mission_briefing (refuerzo/diagnostico); `renderScreen0` made null-safe; options emitted as A–D object; feedback emitted as `{explanation}`. Evidence: 3 SBA modes show INICIAR MISIÓN (10/25/50 retos); 10-question walk, 10 unique IDs, 4 options each, debrief renders.
3. **SBA TRAIN loop (#3)** — `renderTrain`/`submitDrill` without `micro_drill` now advance via `nextQuestion()`; reveal button label adapts (Siguiente pregunta → / Ver Mapa Cognitivo →). Evidence: q1→q5→map, 5 unique IDs, 5 attempts recorded.
4. **Nav stacking (#2)** — header navs offset below the fixed gov-banner (sba: `margin-top:34px`; adaptive: `calc(var(--gov-h)+4px)`); `.global-nav` z-index 600 above overlays (500); overlays given `padding-top:96px; overflow-y:auto` to avoid nav/card collision; hub now links all 4 experiences; stale "119" corrected to 523. Evidence: 0 blocked links by hit-test; 4/4 real click navigations + hub click.
5. **Placebo removal (#4/#5/#6)** — empty panels (Cadena causal, Trampas, Misconception, Relevancia SAT) hidden unless populated; mentor selector hidden until `feedback_by_mode` ships (placebo); static cross-stage challenge hidden unless per-item; static English MCQ mentor hint removed; universal fallback replaced by deterministic per-question guidance (correct option + topic + RA) in both SBA and Adaptive. Evidence: 0 "—" panels; guidance text differs per question ID.
6. **Localization (#12)** — nav labels (Cabina SBA / Sesión Adaptativa / Respuesta Abierta / Simulacro), mode buttons, ORL h1 + session labels, challenge badge, and all learner-facing `coach_data.js` strings (command verbs, mentor hints, quality principle) translated to Spanish. Evidence: G8 scan finds 0 English labels. *Note: `coach_data.js` is generated by `distinction_coach_exporter.py` — translation must be ported to the exporter source before regeneration.*

**Infrastructure finding:** during the sprint, files edited on the host were intermittently clamped to their pre-edit byte length when read from the execution environment — the same mid-token truncation found in the original worktree. All final files were written atomically and G1 (integrity gate) now guards against deploying a truncated file.

Full Simulation re-verified post-fix: SBA options render, OR phase picks up the restored `mock_theory_2` session (4 items), SAT phase renders. 0 page errors.

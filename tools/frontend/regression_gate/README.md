# regression_gate — Headless pre-deploy gate (Phase Z.2)

Runtime regression gate for the epistemiclab-dashboard production frontend.
Born from `docs/FRONTEND_STABILIZATION_AUDIT.md`: a feature that exists visually
but does not work is incomplete. This gate executes REAL clicks in headless
Chromium against the deploy candidate. **Run before every dashboard push.**

## Usage
```bash
npm install            # puppeteer-core + @sparticuz/chromium (or set CHROME_PATH)
DASHBOARD_ROOT=C:/Dev/epistemiclab-dashboard node gate.mjs
# subset: GATES=G5,G6 node gate.mjs
```

## Gates
| Gate | Verifies |
|---|---|
| G1 | File integrity: `</html>` present, every inline script parses (guards against the truncation corruption found 2026-06-10) |
| G2 | ORL: 4 modes render correct counts (1/2/4/4), full session walk, finish, restart |
| G3 | Adaptive SBA: 3 modes reach INICIAR MISIÓN; 10-question walk, unique IDs, options render, debrief |
| G4 | Adaptive SAT: 3 modes render wine + textarea |
| G5 | Diagnostic SBA: quick_drill advances q1→q5→map (no TRAIN loop, no repetition) |
| G6 | Navigation: all nav links pass elementFromPoint hit-test + real click navigates; hub has 4 lab cards |
| G7 | No placebo: no "—" panels, question-specific guidance, mentor selector hidden while data-less |
| G8 | Localization: no English learner-facing mode/nav labels |

Exit code 0 = green. Any FAIL = do not deploy.

Governance: formative tooling only; no LLM/API/cloud calls; safe_for_examiner=False.

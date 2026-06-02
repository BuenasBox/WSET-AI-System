# Static Demo Cockpit Manual QA

Phase: 4A.3.7.18

Date: 2026-06-02

Status: passed after one minimal blocker fix.

## Scope

Inspected:

- `frontend/diagnostic-sba/index.html`
- `frontend/diagnostic-sba/preguntas.json`
- `tests/test_diagnostic_sba_cockpit_json_loader.py`
- `tests/test_static_demo_export_file.py`

This QA pass did not modify the exporter, question bank drafts, review records,
schemas, retrieval, PSL, knowledge-map, backend code, or static export payload.

## Preview Method

Use a local static server:

```bash
python -m http.server 8000 -d frontend/diagnostic-sba
```

Then open:

```text
http://localhost:8000/
```

Directly opening `frontend/diagnostic-sba/index.html` from disk may fail to
load `./preguntas.json` because browser `file://` behavior commonly blocks or
changes local fetch semantics. That is expected browser behavior for this static
demo and is not a product bug.

## QA Summary

| Area | Result | Notes |
|---|---:|---|
| A. Load behavior | PASS | Cockpit references `./preguntas.json`, shows loading copy, validates payload, and has a graceful error state. |
| B. Question flow | PASS | First question renders from `items[]`; options render; one option can be selected; confidence is required before commit; confirm/commit path exists. |
| C. Outcome flow | PASS | Correct answer, diagnostic roles, rationales, and remediation are read only after submit from `outcomes_by_item_id[item_id]`. |
| D. Session flow | PASS | Exported items are ordered `2 -> 12 -> 17`; next action advances through all three; session summary appears after the third item. |
| E. Governance | PASS | Visible disclaimer is present; static demo/training-only language is used; no official scoring, pass/fail, certification readiness, or examiner authority claims were found. |
| F. SBA-only | PASS | Four-option single-answer interaction only; no fill blanks, drag/drop, typing task, multi-select, ordering, or tag-select interaction. |
| G. Browser limitations | PASS | Local server preview is required/recommended for reliable `fetch('./preguntas.json')`; direct file open may fail as expected. |

## Detailed Checklist

### A. Load Behavior

- PASS: Opens with loading state: `Cargando preguntas desde ./preguntas.json...`.
- PASS: Loads `preguntas.json` through `fetch(DATA_URL)`.
- PASS: Handles fetch or validation failure with error copy:
  `ERROR · No se cargó preguntas.json · Sin diagnóstico parcial`.
- PASS: Local HTTP probe confirmed the page and JSON are served from
  `http://localhost:8000/`.

### B. Question Flow

- PASS: First question renders from `payload.items[0]`.
- PASS: Exactly four options render per item.
- PASS: Selection is single-answer only through A-D option IDs.
- PASS: Confidence controls appear after option selection.
- PASS: Confidence is required before commit. A blocker was found here and fixed
  by keeping confirm disabled until a confidence value is selected.
- PASS: Confirm/commit path locks the item and transitions to outcome reveal.
- PASS: Cross-examination panel appears after confirmation.
- PASS: Reveal appears only after confirmation.

### C. Outcome Flow

- PASS: `loadQ()` does not access `OUTCOMES_BY_ITEM_ID`.
- PASS: `correct_option_id` is accessed first in `confirmAnswer()`.
- PASS: Feedback comes from `outcomes_by_item_id[item_id]`.
- PASS: No outcome data is visible before submit in the render path.

### D. Session Flow

- PASS: Static export contains exactly three items.
- PASS: Item order is deterministic: `2`, `12`, `17`.
- PASS: Items `1` and `13` are absent from the exported demo.
- PASS: The next button advances through the three items.
- PASS: Session completion overlay appears after the third item.
- PASS: Cognitive map sections remain present: distractor/fundamento,
  misconception when applicable, causal chain, SAT signal, remediation, and next
  action.

### E. Governance

- PASS: Visible header disclaimer:
  `PROTOTIPO ESTÁTICO · ENTRENAMIENTO · NO EVALUACIÓN OFICIAL WSET`.
- PASS: Payload governance is safe for all three exported items:
  `training_item_only=true`, `official_wset_question=false`,
  `safe_for_examiner=false`, `examiner_scoring_allowed=false`,
  `static_demo_only=true`.
- PASS: No official score claim found.
- PASS: No pass/fail assessment claim found. The UI uses answer-level
  correct/incorrect feedback only after submit.
- PASS: No examiner authority claim found.
- PASS: No certification-readiness claim found.
- PASS: No LES update claim found.

### F. SBA-Only Interaction

- PASS: The cockpit renders A-D options only.
- PASS: One selected answer is tracked in `S.sel`.
- PASS: No fill-in-the-blank task found.
- PASS: No drag/drop task found.
- PASS: No typing/open-response task found.
- PASS: No multi-select task found.
- PASS: No ordering task found.
- PASS: No tag-select task found.

## Blockers Found

One blocker was found:

- Confidence was captured but not required before commit.

Fix applied:

- The confirm button now remains disabled until the learner selects a confidence
  value.
- Click and Enter commit paths now guard against missing confidence.
- A regression assertion was added to
  `tests/test_diagnostic_sba_cockpit_json_loader.py`.

## Final QA Result

PASS.

The static demo cockpit is ready for publication-readiness review as a static,
training-only, non-official diagnostic SBA prototype.

## Next Recommended Phase

Phase 4A.3.7.19 - Static Demo Publication Readiness.

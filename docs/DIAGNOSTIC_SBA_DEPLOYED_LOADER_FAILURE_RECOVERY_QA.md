# Phase 4A.3.7.23 - Diagnostic SBA v2.2 Deployed Loader Failure/Recovery QA

Date: 2026-06-03

Status: deployed QA not approved; local loader failure/recovery QA passed.

## Scope

This phase validates the Diagnostic SBA static JSON loader without modifying:

- `frontend/diagnostic-sba/preguntas.json`;
- the Diagnostic SBA cockpit design;
- governance flags;
- scoring or examiner authority;
- backend, API, LLM, embeddings, vector database, or cloud behavior.

The controlled failure scenarios use only:

- `tests/fixtures/diagnostic_sba/loader_failure_recovery_server.py`;
- an in-memory copy of the current `preguntas.json` payload;
- the current local cockpit HTML;
- a local HTTP server used only for QA.

The fixture server is not a product backend and must never be deployed.

## Approval Criteria

The deployed loader may be approved only when:

1. `/diagnostic-sba/` contains the current loader and calls `fetch(DATA_URL)`.
2. `/diagnostic-sba/preguntas.json` loads with items `2`, `12`, and `17`.
3. No embedded mock question bank is active.
4. Every controlled failure shows the private-lab error state.
5. Submit is unavailable during failure.
6. No question, option, or partial diagnosis remains visible during failure.
7. Reload after payload restoration returns the cockpit to a functional state.
8. The training, non-official, and no-examiner-authority badge remains visible.

## Deployed Environment Evidence

Checked URLs:

```text
https://epistemiclab.dpdns.org/diagnostic-sba/
https://epistemiclab.dpdns.org/diagnostic-sba/preguntas.json
```

Observed:

- Both URLs returned HTTP `200`.
- The deployed `preguntas.json` returned `static_demo_export_v0` with 3 items:
  `2`, `12`, and `17`.
- The deployed cockpit HTML did not contain `var DATA_URL = './preguntas.json';`.
- The deployed cockpit HTML did not contain `fetch(DATA_URL)`.
- The deployed cockpit HTML contained an embedded question bank.
- Browser inspection showed a 4-question experience rather than the 3-item
  `preguntas.json` payload.

Result: the deployed cockpit is not the loader-enabled cockpit validated in
Phase 4A.3.7.22. Deployed loader QA is blocked until the current static
`frontend/diagnostic-sba/index.html` is published with `preguntas.json`.

## Controlled Local Scenarios

Run the test-only fixture server:

```powershell
python -m tests.fixtures.diagnostic_sba.loader_failure_recovery_server --port 18766
```

Scenario URLs:

```text
http://127.0.0.1:18766/scenario/valid/diagnostic-sba/
http://127.0.0.1:18766/scenario/missing/diagnostic-sba/
http://127.0.0.1:18766/scenario/forbidden/diagnostic-sba/
http://127.0.0.1:18766/scenario/server_error/diagnostic-sba/
http://127.0.0.1:18766/scenario/corrupt_json/diagnostic-sba/
http://127.0.0.1:18766/scenario/invalid_structure/diagnostic-sba/
http://127.0.0.1:18766/scenario/missing_options/diagnostic-sba/
http://127.0.0.1:18766/scenario/missing_outcome/diagnostic-sba/
http://127.0.0.1:18766/scenario/inconsistent_outcome/diagnostic-sba/
http://127.0.0.1:18766/scenario/recovery/diagnostic-sba/
```

Expected fail-closed state for every failure:

- error text includes `Laboratorio privado`;
- options container is empty;
- confirm/submit control is hidden or unavailable;
- no diagnostic result is shown;
- no mock or fallback questions are activated;
- governance badge remains visible.

The `recovery` scenario returns an invalid payload on its first request and the
valid payload on the next request. A browser reload must restore the functional
3-item cockpit without any additional manual change.

## Browser QA Evidence

| Scenario | Observed result |
|---|---|
| Valid payload | `1/3`, four A-D options visible, no diagnostic result, submit initially disabled |
| Missing file / HTTP 404 | `0/0`, zero options, submit hidden, no diagnostic result, private-lab error |
| HTTP 403 | `0/0`, zero options, submit hidden, no diagnostic result, private-lab error |
| HTTP 500 | `0/0`, zero options, submit hidden, no diagnostic result, private-lab error |
| Corrupt JSON | `0/0`, zero options, submit hidden, no diagnostic result, private-lab error |
| Valid JSON, invalid structure | `0/0`, zero options, submit hidden, no diagnostic result, private-lab error |
| Incomplete A-D options | `0/0`, zero options, submit hidden, no diagnostic result, private-lab error |
| Missing matching outcome | `0/0`, zero options, submit hidden, no diagnostic result, private-lab error |
| Inconsistent outcome item ID | `0/0`, zero options, submit hidden, no diagnostic result, private-lab error |
| Recovery after restoration | First load failed closed; one reload restored `1/3` with four A-D options |

Every observed state preserved:

```text
LABORATORIO PRIVADO · PROTOTIPO ESTÁTICO · ENTRENAMIENTO ·
NO EVALUACIÓN OFICIAL WSET · SIN AUTORIDAD EXAMINADORA
```

## Test Commands

```powershell
python -m unittest tests.test_diagnostic_sba_loader_failure_recovery_qa -v
python -m unittest tests.test_diagnostic_sba_cockpit_json_loader -v
python -m unittest discover -s tests -v
python -m tools.question_generation.export_static_demo_questions --dry-run
```

## Result

Local loader failure/recovery QA: passed.

Deployed loader failure/recovery QA: not approved because the deployed cockpit
still uses an embedded question bank and does not fetch `preguntas.json`.

## Next Recommended Phase

Phase 4A.3.7.24 - Publish Loader-Enabled Diagnostic SBA Cockpit and Repeat
Deployed Failure/Recovery QA.

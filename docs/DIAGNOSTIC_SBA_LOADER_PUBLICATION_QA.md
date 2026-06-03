# Phase 4A.3.7.24 - Loader-Enabled Diagnostic SBA Cockpit Publication QA

Date: 2026-06-03

Status: deploy-approved.

## Objective

Publish the canonical loader-enabled Diagnostic SBA cockpit and confirm that
the live private lab uses `preguntas.json` as its only active question source.

## Root Cause

The public deployment repository contained a copy of
`frontend/diagnostic-sba-v2.2/index.html`, which used an embedded
`QUESTIONS` array. The canonical loader-enabled file is
`frontend/diagnostic-sba/index.html`.

The public `diagnostic-sba/preguntas.json` was already correct and contained
the expected `static_demo_export_v0` payload. The publication error affected
only `diagnostic-sba/index.html`.

## Minimal Publication Change

Only this public deployment file was replaced:

```text
epistemiclab-dashboard/diagnostic-sba/index.html
```

No change was made to:

- `diagnostic-sba/preguntas.json`;
- governance flags;
- scoring or examiner authority;
- backend, API, LLM, embeddings, vector database, or cloud behavior.

## Commits

Source repository:

```text
de67548 test(phase-4a3.7.23): verify loader failure recovery
```

Public deployment repository:

```text
3c0e2f9 fix: publish loader-enabled diagnostic SBA cockpit
```

## Live Evidence

Checked URLs:

```text
https://epistemiclab.dpdns.org/diagnostic-sba/
https://epistemiclab.dpdns.org/diagnostic-sba/preguntas.json
```

Observed:

- both URLs returned HTTP `200`;
- the live HTML contains `var DATA_URL = './preguntas.json';`;
- the live HTML contains `fetch(DATA_URL)`;
- the live HTML does not contain `const QUESTIONS`;
- the live HTML does not contain an embedded `var QS = [{...}]` question bank;
- the live JSON has `export_version = static_demo_export_v0`;
- the live JSON has 3 items with source question IDs `2`, `12`, and `17`;
- browser rendering showed `1/3`, four A-D options, and the private-lab
  governance badge.

The source and public repository copies of `index.html` had identical SHA-256
hashes after publication. The source and public repository copies of
`preguntas.json` also had identical SHA-256 hashes before and after the public
index replacement.

## Failure/Recovery QA

Production failure simulation was not performed because changing the live JSON
or route would modify the production static deployment. The deployed HTML is
byte-identical to the canonical loader that passed the controlled local
failure/recovery scenarios in Phase 4A.3.7.23:

- HTTP 404, 403, and 500;
- corrupt JSON;
- valid JSON with invalid structure;
- incomplete A-D options;
- missing outcome;
- inconsistent outcome;
- recovery after restoring valid JSON.

This establishes behavior parity without touching the production payload.

## Verification Commands

```powershell
python -m unittest tests.test_diagnostic_sba_cockpit_json_loader tests.test_diagnostic_sba_loader_failure_recovery_qa -v
python -m unittest discover -s tests -v
python -m tools.question_generation.export_static_demo_questions --dry-run
git diff --check
```

## Result

Phase 4A.3.7.24 is deploy-approved. The live cockpit now uses
`preguntas.json` as its only active question source, and the deployment
misalignment recorded in Phase 4A.3.7.23 is resolved.

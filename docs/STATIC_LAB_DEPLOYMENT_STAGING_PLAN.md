# Static Lab Deployment Staging Plan

Phase: 4A.3.7.20.5

Status: planning and static validation only. This phase does not copy files,
modify the dashboard, modify the Diagnostic SBA Lab, deploy `gh-pages`, or
publish anything.

## 1. Purpose

This plan defines how to stage the static Diagnostic SBA Lab under the existing
EpistemicLab dashboard deployment after the dashboard lab-link gate is satisfied.

Final intended URL:

```text
https://epistemiclab.dpdns.org/diagnostic-sba/
```

Current gate:

- Claude visual/SBA-purity review must be accepted.
- Explicit authorization must be given before modifying the dashboard.
- No deployment may occur in this planning phase.

## 2. Current Sources

Current published dashboard root:

```text
frontend/architecture-dashboard/
```

Current static lab source:

```text
frontend/diagnostic-sba/
```

The lab source currently contains:

```text
frontend/diagnostic-sba/index.html
frontend/diagnostic-sba/preguntas.json
```

## 3. Desired Deployed Tree

The desired static deployment tree is:

```text
/
  index.html
  system_state.json
  robots.txt
  CNAME
  .nojekyll
  diagnostic-sba/
    index.html
    preguntas.json
```

The deployed `/diagnostic-sba/` route must serve the static cockpit, and
`/diagnostic-sba/preguntas.json` must load as the cockpit data file.

## 4. Staging Options

### Option A - Copy Lab Into Dashboard Folder

Approach:

Copy:

```text
frontend/diagnostic-sba/
```

into:

```text
frontend/architecture-dashboard/diagnostic-sba/
```

before using the current subtree publish flow.

Benefits:

- simplest immediate path;
- works with the current `git subtree push --prefix frontend/architecture-dashboard`
  deployment model;
- easy to inspect before deployment.

Risks:

- duplicates lab files in the repository;
- can drift from the source lab unless every update is copied carefully;
- makes the dashboard folder both source and release artifact.

### Option B - Release Assembly Directory

Approach:

Create a future release assembly script that builds a temporary static
deployment directory from explicit source files:

```text
frontend/architecture-dashboard/*       -> temp deployment root
frontend/diagnostic-sba/index.html      -> temp deployment root/diagnostic-sba/index.html
frontend/diagnostic-sba/preguntas.json  -> temp deployment root/diagnostic-sba/preguntas.json
```

The release assembly output can then be reviewed and published from a known
clean static tree.

Benefits:

- cleanest long-term staging model;
- avoids duplicating the lab source in the dashboard folder;
- makes included/excluded files explicit;
- reduces risk of accidentally publishing docs, tests, source-bank files,
  knowledge corpus files, tools, learner state, or private memory files;
- supports a pre-deploy manifest and checksum review in later phases.

Risks:

- requires a future script/assembly phase;
- needs an adjusted deployment command or a temporary branch/tree workflow;
- slightly more setup than direct copy.

### Option C - Change Repository Layout

Approach:

Move dashboard and lab into a new shared deployment source tree.

Benefits:

- could make deployment structure obvious.

Risks:

- broad repo layout change;
- unnecessary for the current static lab;
- higher chance of breaking existing dashboard publication assumptions;
- outside the current phase scope.

## 5. Recommended Approach

Recommend Option B for the clean long-term path: create a future release
assembly step that builds a temporary static deployment directory from explicit
allowed files.

If a near-term manual deployment is authorized before an assembly script exists,
Option A is acceptable as a simple interim path, but only after:

- visual/SBA-purity review is accepted;
- the dashboard link implementation phase is authorized;
- copied lab files are verified against the source files;
- the copied deployment tree is inspected before any `gh-pages` update.

Do not use Option C for this workstream.

## 6. Files That Must Be Included

The staged deployment must include:

- dashboard `index.html`;
- dashboard `system_state.json`;
- dashboard `robots.txt`;
- `CNAME`;
- `.nojekyll`;
- `diagnostic-sba/index.html`;
- `diagnostic-sba/preguntas.json`.

If any required file is missing, deployment must stop.

## 7. Files That Must Not Be Included

The staged deployment must not include:

- knowledge corpus;
- diagnostic SBA drafts/reviews;
- tests;
- docs;
- source-bank files;
- Python tools;
- hidden local artifacts;
- learner state;
- research docs;
- private memory files;
- `knowledge/nazareth/`;
- `knowledge/self-eval/reports/`;
- `knowledge/self-eval/attempts/`;
- `knowledge/retrieval-sandbox/`;
- `.codex/` or `.claude/`;
- `.vercel/`;
- runtime `*.jsonl` traces;
- exporter scripts;
- schemas;
- local worktree metadata.

The deployment should contain only static frontend assets needed by the private
dashboard and the private Diagnostic SBA Lab.

## 8. Privacy Requirements

The staged deployment must preserve:

- `robots.txt` disallow all;
- dashboard page meta `noindex,nofollow`;
- lab page meta `noindex,nofollow`;
- no sitemap;
- no analytics;
- no tracking;
- no public external links;
- no backend;
- no API;
- no Supabase;
- no login;
- no learner data persistence.

Recommended robots rule:

```text
User-agent: *
Disallow: /
```

## 9. Future Deployment Commands

Documented for future use only. Do not run these commands in this phase.

Current known method:

```bash
git subtree push --prefix frontend/architecture-dashboard origin gh-pages
```

Fallback method:

```bash
git push origin `git subtree split --prefix frontend/architecture-dashboard main`:gh-pages --force
```

Important:

- These commands assume the deployment tree already contains
  `diagnostic-sba/index.html` and `diagnostic-sba/preguntas.json`.
- If Option B is implemented, the command may need to target the assembled
  release tree or a release branch rather than the raw dashboard source folder.
- No command should run until the implementation phase explicitly authorizes
  dashboard modification and deployment.

## 10. Pre-Deploy Checks

Before any future deployment:

1. Confirm the dashboard loads from the staged root.
2. Confirm `/diagnostic-sba/` loads from the staged root.
3. Confirm `/diagnostic-sba/preguntas.json` loads from the staged root.
4. Confirm no 404 for the lab route.
5. Confirm dashboard `noindex,nofollow` metadata is present.
6. Confirm lab `noindex,nofollow` metadata is present.
7. Confirm `robots.txt` disallows all.
8. Confirm no sitemap exists or references `/diagnostic-sba/`.
9. Confirm no analytics or tracking scripts exist.
10. Confirm no external calls were introduced.
11. Confirm no backend/API/Supabase references exist.
12. Confirm no learner-state writes or persistence are introduced.
13. Confirm no knowledge corpus, docs, tests, tools, drafts/reviews, or private
    local artifacts are present in the staged deployment tree.
14. Confirm the lab still contains item IDs `2`, `12`, and `17` only.

## 11. Post-Deploy Checks

After any future authorized deployment:

1. Open:

```text
https://epistemiclab.dpdns.org/
```

2. Open:

```text
https://epistemiclab.dpdns.org/diagnostic-sba/
```

3. Open:

```text
https://epistemiclab.dpdns.org/diagnostic-sba/preguntas.json
```

4. Verify the dashboard link points to `/diagnostic-sba/` or
   `diagnostic-sba/`.
5. Verify the lab session completes through item order `2 -> 12 -> 17`.
6. Verify the browser console has no blocking errors.
7. Verify no indexing metadata was introduced.
8. Verify `robots.txt` still disallows all.
9. Verify there are no official score, pass/fail, examiner authority,
   certification-readiness, backend persistence, analytics, or learner-state
   claims.

## 12. Phase Boundary

This phase creates only:

- `docs/STATIC_LAB_DEPLOYMENT_STAGING_PLAN.md`;
- optional static inspection tests.

This phase must not:

- modify `frontend/architecture-dashboard/index.html`;
- copy diagnostic SBA files;
- deploy;
- modify `gh-pages`;
- modify `CNAME` or `robots.txt`;
- modify `frontend/diagnostic-sba/index.html`;
- modify `frontend/diagnostic-sba/preguntas.json`;
- add analytics, login, backend, API, or Supabase;
- touch question bank, exporter, retrieval, PSL, or knowledge-map files.

## 13. Next Recommended Phase

Phase 4A.3.7.21 - Dashboard Lab Link Implementation, only after
visual/SBA-purity review and explicit authorization.

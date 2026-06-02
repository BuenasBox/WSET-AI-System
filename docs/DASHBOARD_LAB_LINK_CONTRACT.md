# Dashboard Lab Link Contract

Phase: 4A.3.7.20

Status: contract only. This phase does not modify the architecture dashboard,
does not modify the diagnostic SBA cockpit, and does not publish or deploy the
lab.

## 1. Purpose

This contract defines how the private EpistemicLab architecture dashboard may
link to the static Diagnostic SBA Lab in a future implementation phase.

The intended lab URL is:

```text
/diagnostic-sba/
```

The dashboard link label should be one of:

```text
Diagnostic SBA Lab
Laboratorio Diagnóstico SBA
```

## 2. Dashboard Role

The existing architecture dashboard remains the private EpistemicLab landing
page.

The dashboard must continue to frame the project as:

- private;
- local/static unless a later phase authorizes otherwise;
- governance-constrained;
- training-oriented;
- not an official WSET assessment surface.

The Diagnostic SBA Lab link must not replace the architecture dashboard as the
landing page and must not be presented as a primary public product CTA.

## 3. Lab Link Purpose

The new dashboard link gives private access to:

```text
/diagnostic-sba/
```

The link exists so internal reviewers can open the static diagnostic SBA
cockpit from the dashboard context.

The link must be framed as:

- laboratory;
- static demo;
- training-only / entrenamiento;
- no official WSET evaluation / no evaluacion oficial WSET;
- no examiner authority;
- no learner persistence.

Recommended governance wording for the dashboard link or card:

```text
Laboratorio privado · Entrenamiento · No evaluación oficial WSET
```

An ASCII-safe equivalent is also acceptable:

```text
Laboratorio privado · Entrenamiento · No evaluacion oficial WSET
```

## 4. Publication Structure

Recommended static deployment structure:

```text
/
  index.html                  # architecture dashboard
  system_state.json
  robots.txt
  CNAME
  diagnostic-sba/
    index.html
    preguntas.json
```

Required deployment files:

- architecture dashboard files;
- `diagnostic-sba/index.html`;
- `diagnostic-sba/preguntas.json`.

Do not deploy knowledge corpus files, draft files, review records, exporter
scripts, schemas, learner-state files, self-eval reports, retrieval artifacts,
source-bank files, or local machine traces.

## 5. Link Behavior

The dashboard link must use a relative path:

```html
href="./diagnostic-sba/"
```

or:

```html
href="diagnostic-sba/"
```

The link must not:

- hard-code local filesystem paths;
- use absolute Windows paths;
- use `file://` URLs;
- depend on localhost;
- point to an external public domain;
- point to a backend, API, or Supabase route.

## 6. Visual Placement

The link should be visible but clearly marked as lab/private.

Allowed placements:

- a new `Labs` section;
- a small button/card in the architecture dashboard;
- a subdued private-lab entry near other internal project surfaces.

Forbidden placement:

- primary public CTA;
- marketing hero button;
- official exam call-to-action;
- production app launch button.

The link/card should be visually secondary to the dashboard landing-page
purpose.

## 7. Noindex And Privacy Requirements

The dashboard deployment must preserve:

- dashboard-level noindex/nofollow;
- lab-level noindex/nofollow if present;
- `robots.txt` disallow;
- no sitemap;
- no analytics;
- no tracking;
- no public navigation from external domains;
- no login;
- no backend;
- no API usage;
- no Supabase;
- no learner data persistence.

Recommended robots rule:

```text
User-agent: *
Disallow: /
```

The dashboard link implementation must not add sitemap entries or SEO metadata
for `/diagnostic-sba/`.

## 8. Governance Label

The dashboard link/card must include private lab governance wording such as:

```text
Laboratorio privado · Entrenamiento · No evaluación oficial WSET
```

or:

```text
Private lab · Training-only · No official WSET evaluation
```

The label must not imply production use, official assessment authority, or
learner-state persistence.

## 9. Forbidden Link/Card Claims

The dashboard link/card must not say or imply:

- official exam;
- official WSET score;
- pass/fail;
- certification readiness;
- examiner simulation;
- examiner scoring;
- examiner authority;
- production app;
- public launch;
- official WSET question source;
- LES updated;
- learner record saved.

## 10. Deployment Gate

The dashboard lab link may be implemented only after all of the following are
true:

1. This contract exists and is committed.
2. Current cockpit manual QA is green.
3. Visual/SBA-purity review is accepted.
4. Explicit authorization to modify the architecture dashboard is given.
5. The implementation phase confirms no backend, API, Supabase, analytics,
   login, or learner persistence is being added.

Until those gates are satisfied, no dashboard HTML should be modified.

## 11. Future Implementation Acceptance Criteria

The future dashboard-link implementation should verify:

- the dashboard still loads as the private landing page;
- the lab link points to `./diagnostic-sba/` or `diagnostic-sba/`;
- the link label is `Diagnostic SBA Lab` or `Laboratorio Diagnóstico SBA`;
- the link/card includes private training-only governance wording;
- the lab path includes `diagnostic-sba/index.html` and
  `diagnostic-sba/preguntas.json`;
- no external dependencies, analytics, backend calls, API calls, or Supabase
  references are introduced;
- no forbidden official/examiner/production/certification claims are present;
- noindex/nofollow and robots disallow remain in place.

## 12. Current Phase Boundary

This phase creates only:

- `docs/DASHBOARD_LAB_LINK_CONTRACT.md`;
- optional static contract tests.

This phase must not:

- modify `frontend/architecture-dashboard/index.html`;
- modify `frontend/diagnostic-sba/index.html`;
- modify `frontend/diagnostic-sba/preguntas.json`;
- deploy `gh-pages`;
- change `CNAME` or `robots.txt`;
- add analytics;
- add login;
- add backend/API/Supabase;
- touch question bank, exporter, retrieval, PSL, or knowledge-map files.

## 13. Next Recommended Phase

Phase 4A.3.7.21 - Dashboard Lab Link Implementation.

# Static Demo Publication Readiness

Phase: 4A.3.7.19

Date: 2026-06-02

Status: ready for private lab publication planning; not published in this
phase.

## Scope

This document evaluates whether the static Diagnostic SBA Lab is ready to be
published inside the private EpistemicLab dashboard deployment.

This phase does not:

- deploy the lab;
- modify `gh-pages`;
- modify the architecture dashboard;
- modify the cockpit;
- modify `preguntas.json`;
- modify the exporter;
- add backend, API, Supabase, login, analytics, or learner persistence.

## Readiness Verdict

The Diagnostic SBA cockpit is ready for private lab publication planning, with
publication deferred until the next dashboard-link contract and final visual
review are accepted.

The current cockpit is suitable as:

- a private lab;
- a static demo;
- a training-only diagnostic SBA prototype;
- a non-official WSET-adjacent learning tool;
- a no-backend, no-persistence, no-tracking static page.

It is not ready for:

- production users;
- public launch;
- SEO/indexing;
- official claims;
- official WSET question-source claims;
- examiner scoring;
- certification-readiness claims;
- backend persistence;
- LES writes;
- user accounts;
- analytics/tracking;
- public navigation from external domains.

## Current Evidence

Phase 4A.3.7.18 manual QA passed after one minimal blocker fix.

Confirmed state:

- `frontend/diagnostic-sba/index.html` loads `./preguntas.json`.
- `frontend/diagnostic-sba/preguntas.json` exists.
- Exported item IDs are `2`, `12`, and `17`.
- Loading and error states exist.
- Confidence is required before commit.
- Interactions are SBA-only.
- Pre-submit rendering uses only `items[]`.
- Post-submit outcome data is read only after confirmation from
  `outcomes_by_item_id[item_id]`.
- No backend, API, Supabase, external dependencies, or runtime learner-state
  writes were added.
- Governance disclaimer remains visible.

## Readiness Questions

### Is The Diagnostic SBA Cockpit Ready For Private Lab Publication?

Yes, with one boundary: it is ready for private lab publication planning, not
for immediate publication in this phase.

Publication should wait for:

- the dashboard lab-link contract;
- final visual/SBA-purity review acceptance;
- a manual test of the exact deployed URL after the lab is linked.

### Should It Be Linked From The Architecture Dashboard?

Yes, but only after the dashboard link contract is approved.

Recommended integration:

- keep the architecture dashboard as the landing page;
- add one private lab button/link labelled `Diagnostic SBA Lab`;
- link to `/diagnostic-sba/`;
- keep noindex/nofollow and private-lab language visible;
- do not add marketing copy, SEO metadata, analytics, login, or public product
  claims.

### What Is The Safest URL Structure?

Recommended URL:

```text
https://epistemiclab.dpdns.org/diagnostic-sba/
```

Rationale:

- keeps the lab under the same private static deployment;
- avoids a separate public domain or external navigation path;
- keeps assets local to the static deployment;
- gives the cockpit a stable relative JSON path:
  `/diagnostic-sba/preguntas.json`.

### What Files Must Be Included In Deployment?

Required files:

```text
frontend/diagnostic-sba/index.html
frontend/diagnostic-sba/preguntas.json
```

No knowledge corpus files, draft files, review records, exporter scripts,
schemas, learner-state files, self-eval reports, retrieval artifacts, or local
machine traces should be included in the public static deployment.

### Should It Remain Noindex/Private?

Yes.

The lab should remain private, noindex, nofollow, and absent from sitemaps.
It should be shared by direct private link only.

### What Robots/Meta Rules Are Required?

The cockpit page should keep:

```html
<meta name="robots" content="noindex,nofollow,noarchive,nosnippet,noimageindex">
<meta name="googlebot" content="noindex,nofollow">
```

The static deployment should also use a `robots.txt` rule equivalent to:

```text
User-agent: *
Disallow: /
```

Publication should not add a sitemap entry for `/diagnostic-sba/`.

### What Governance Disclaimer Must Remain Visible?

The visible cockpit disclaimer must remain:

```text
PROTOTIPO ESTATICO · ENTRENAMIENTO · NO EVALUACION OFICIAL WSET
```

The current UI uses the accented display text:

```text
PROTOTIPO ESTÁTICO · ENTRENAMIENTO · NO EVALUACIÓN OFICIAL WSET
```

That visible language is acceptable and should not be removed or softened.

## Security And Privacy Requirements

Publication readiness requires:

- keep `noindex,nofollow`;
- keep `robots.txt` disallow;
- no sitemap;
- no public navigation from external domains;
- no analytics or tracking;
- no backend;
- no API;
- no Supabase;
- no learner data persistence;
- no login yet;
- no source maps or sensitive build artifacts;
- no knowledge corpus exposure;
- no source bank exposure;
- no draft/review export beyond the static demo payload;
- only static frontend assets needed by the lab.

## Architecture Requirements

The published lab must be described as:

- private lab;
- static demo;
- training-only;
- no official WSET authority;
- no examiner scoring;
- no official score;
- no pass/fail;
- no certification readiness;
- no LES persistence;
- no runtime learner-model writes.

The lab must not become the cognitive authority. It should continue to render
the already separated static demo payload:

- `items[]` before submit;
- `outcomes_by_item_id{}` only after submit.

## Publication Options

### Option A - Publish Only `/diagnostic-sba/`

Description:

Deploy the lab path and share the direct private link without linking from the
architecture dashboard.

Pros:

- smallest dashboard change footprint;
- reduces accidental discovery from dashboard navigation;
- useful for very narrow reviewer access.

Cons:

- less discoverable for intended internal dashboard users;
- creates an undocumented lab entry point;
- easier for dashboard and lab deployment states to drift.

### Option B - Add A Private Dashboard Button

Description:

Keep the architecture dashboard as the landing page and add a private
`Diagnostic SBA Lab` button linking to `/diagnostic-sba/`.

Pros:

- cleanest private-lab user flow;
- keeps the lab framed by the architecture dashboard context;
- makes governance and deployment state easier to review together;
- matches current project direction.

Cons:

- requires a dashboard-link phase;
- should wait for final visual/SBA-purity review;
- must preserve noindex/private rules.

### Option C - Keep Local Preview Only

Description:

Do not publish. Continue using:

```bash
python -m http.server 8000 -d frontend/diagnostic-sba
```

Pros:

- lowest exposure risk;
- no dashboard change;
- no deployment coordination.

Cons:

- blocks private stakeholder review in the deployed lab context;
- does not test the intended static deployment URL;
- delays integration with EpistemicLab dashboard navigation.

## Recommendation

Recommend Option B: add a private architecture-dashboard button linking to:

```text
/diagnostic-sba/
```

Condition:

Do this only after the Phase 4A.3.7.20 dashboard lab-link contract is accepted
and the final visual/SBA-purity review is complete.

Do not publish in this phase.

## Recommended Publication Sequence

1. Keep the architecture dashboard as the landing page.
2. Define the dashboard lab-link contract.
3. Add a private button/link labelled `Diagnostic SBA Lab`.
4. Ensure `noindex,nofollow` metadata remains in the lab page.
5. Ensure deployment-level `robots.txt` disallows indexing.
6. Include only:
   - `frontend/diagnostic-sba/index.html`
   - `frontend/diagnostic-sba/preguntas.json`
7. Deploy dashboard and lab together only after final visual review.
8. Manually test:
   - `https://epistemiclab.dpdns.org/`
   - `https://epistemiclab.dpdns.org/diagnostic-sba/`
   - `https://epistemiclab.dpdns.org/diagnostic-sba/preguntas.json`
9. Confirm all three item IDs appear in session order: `2`, `12`, `17`.
10. Confirm no direct or indirect official scoring, pass/fail, examiner,
    certification-readiness, analytics, backend, or persistence claim appears.

## Blockers

No blockers remain for publication-readiness planning.

Publication itself is still blocked pending:

- Phase 4A.3.7.20 dashboard lab-link contract;
- final visual/SBA-purity review acceptance;
- explicit deployment authorization.

## Final Assessment

The static Diagnostic SBA Lab is ready to be considered for private dashboard
publication under `/diagnostic-sba/`.

It should remain private, noindex, static, training-only, non-official, and
free of backend/persistence/analytics until a later phase explicitly authorizes
those changes.

## Next Recommended Phase

Phase 4A.3.7.20 - Dashboard Lab Link Contract.

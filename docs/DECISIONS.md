# Decisions

## 2026-05-28 — Reserve Temporary Domain For Future Frontend Testing

**Decision:** Track `epistemiclab.dpdns.org` as the temporary domain plan in
`docs/DEPLOYMENT_DOMAIN.md` without enabling frontend implementation or web
deployment.

**Rationale:** The project may need a temporary public URL during the future
frontend phase, but the current system remains backend/governance focused. A
documented domain plan avoids mixing infrastructure preparation with premature
deployment.

**Constraints:**

- No frontend work is started by this decision.
- No backend API is exposed by this decision.
- No GitHub Pages, Vercel, Netlify, or other deployment is activated by this
  decision.
- DNS provider API keys are operational secrets and must not be committed.

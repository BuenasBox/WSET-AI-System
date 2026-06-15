# SECURITY AUDIT REPORT — EpistemicLab
**Date**: 2026-06-15  
**Scope**: PHASE S.1 (Read-Only Audit) | Frontend + Backend + Production  
**Status**: Complete | Evidence-based, no code modifications  

---

## EXECUTIVE SUMMARY

EpistemicLab consists of two public GitHub repositories serving a production deployment at `epistemiclab.dpdns.org`. The audit reveals significant **intellectual property (IP) exposure** and **content corpus exposure**, with **no critical authentication breaches** at present, but substantial risks to proprietary assets if the platform gains wider visibility.

| Category | Count | Status |
|----------|-------|--------|
| **CRITICAL Issues** | 0 | No active security breaches |
| **HIGH Issues** | 5 | IP/content exposure (intentional public repos) |
| **MEDIUM Issues** | 7 | Configuration & data exposure |
| **LOW Issues** | 4 | Non-blocking findings |

---

## PART 1: GITHUB EXPOSURE AUDIT

### Repository Visibility

**Frontend**: `https://github.com/BuenasBox/epistemiclab-dashboard`
- Public repository ✓
- 140 tracked files
- 3 main deployable directories (diagnostic-sba, adaptive-session, open-response-lab, full-simulation)
- 22 documentation files in `/docs/`
- Branch: `main` | Last commit: 3258eab (docs: i18n Spanish localization)

**Backend**: `https://github.com/BuenasBox/WSET-AI-System.git`
- Public repository ✓
- 2,145 tracked files
- 215 documentation files in `/docs/`
- Complete knowledge-base (causal chains, misconceptions, enrichment)
- Branch: `main` | Last commit: 6c124ae (Cerrado etapa producción)

### Critical IP Assets Exposed

**Frontend Exposure** (`epistemiclab-dashboard`):
1. **Question Bank — 578 SBA items** | File: `diagnostic-sba/preguntas_data.js`
   - Severity: **HIGH** — Complete curriculum visible, searchable, indexed
   - Includes: question text, correct answers, options, causal chain explanations, feedback profiles
   - Format: `window.PREGUNTAS_BANK` (client-side JavaScript)
   - Governance: Correctly flagged as `safe_for_examiner=false`, formative only

2. **Open Response Corpus — 106 items** | File: `open-response-lab/lab_payload.js`
   - Severity: **HIGH** — Complete OR bank exposed
   - Includes: item_id, feedback profiles, expected concepts, causal-chain targets
   - Coverage: All 106 OR items (OR_001 to OR_106)

3. **Adaptive Session Bank — 578 SBA + 6 SAT prompts** | File: `adaptive-session/session_bank.js`
   - Severity: **HIGH** — 6 SAT wine prompts exposed (complete wine structure)
   - Includes: SAT_P01 through SAT_P06 with full observation patterns

4. **Coaching & Mentor Profiles** | File: `adaptive-session/coach_data.js`, `adaptive-session/learner_intelligence.js`
   - Severity: **HIGH** — Complete mentor profiles, learner intelligence taxonomy, coaching decisions
   - Includes: pedagogical profiles, strategy patterns, misconception triggers

5. **Access Control & Authentication Design** | Files: `shared/access-control.js`, `shared/auth-provider.js`, `shared/access-code-store.js`
   - Severity: **MEDIUM** — Access policy matrix visible, plan requirements, privilege levels

**Backend Exposure** (`WSET-AI-System-push`):
1. **Knowledge Map & Causal Chains** | Directory: `knowledge/knowledge-map/`
   - Severity: **HIGH** — 14 causal-chain nodes (8 official CC_* + 6 heuristic HC_*)
   - Includes: mechanism explanations, pedagogical rationale, exam formulation guidance
   - Files: `knowledge/knowledge-map/causal-chains/`, `knowledge/knowledge-map/misconceptions/`

2. **Enrichment Data** | File: `knowledge/question-bank/enrichment/sba_enrichment_v1.json`
   - Severity: **HIGH** — 205 enriched items with causal structure
   - Includes: detailed explanation patterns, feedback templates, micro-drill design

3. **Misconception Framework** | Directory: `knowledge/knowledge-map/misconceptions/`
   - Severity: **HIGH** — 20 misconception nodes with detection patterns and interventions
   - Includes: learner-model assumptions, pedagogical intervention strategies

4. **Configuration & Retrieval Rules** | Files: `knowledge/config/*.json`
   - Severity: **MEDIUM** — Domain expansions, retrieval scoring, explanation priority, pedagogical profiles
   - Includes: algorithmic scoring details, retrieval depth tuning, pedagogical sequencing

5. **215 Documentation Files**
   - Severity: **MEDIUM** — Complete architecture, design decisions, phase history, roadmap
   - Files: `docs/*.md` (system design, performance analysis, pedagogical strategy, phase planning)

---

## PART 2: FRONTEND EXPOSURE AUDIT

### Deployed Assets Analysis

| File | Type | Content | Public Access | Governance |
|------|------|---------|---|---|
| `preguntas_data.js` | Data | 578 SBA + answers + causal chains + feedback | ✓ Direct | `safe_for_examiner=false` ✓ |
| `lab_payload.js` | Data | 106 OR items + feedback profiles + causal targets | ✓ Direct | `safe_for_examiner=false` ✓ |
| `session_bank.js` | Data | 578 SBA + 6 SAT wines + session modes | ✓ Direct | `safe_for_examiner=false` ✓ |
| `coach_data.js` | Data | Mentor profiles, coaching strategies, learner models | ✓ Direct | Governance flags present |
| `learner_intelligence.js` | Data | Learner taxonomy, intelligence profiles, decision logic | ✓ Direct | Not verified |
| `access-control.js` | Logic | Access policy matrix, privilege levels, plan requirements | ✓ Direct | Internal visibility |
| `auth-provider.js` | Logic | Authentication contract, session management | ✓ Direct | Implementation detail |
| `supabase-config.js` | API | Supabase URL and publishable key retrieval | ✓ API endpoint | Standard practice |

### API Exposure

**Endpoint**: `api/supabase-config.js`
- Exposes: `SUPABASE_URL` + `SUPABASE_PUBLISHABLE_KEY`
- Purpose: Client-side auth initialization
- Risk: **LOW** — Publishable keys are designed for client-side exposure
- Caching: `public, max-age=300` (5 min cache)

**Endpoint**: `/login/`, `/profile/`, `/admin/`, `/upgrade/`
- All routes accessible from public GitHub repo
- Implementation details exposed (mock profiles, access logic, upgrade flow)

### Data Files

| File | Purpose | Exposure | Items | Sensitivity |
|------|---------|----------|-------|---|
| `preguntas.json` | Static fallback SBA | Direct | 18 (subset) | HIGH |
| `.vercel/repo.json` | Vercel deployment metadata | Tracked in git | Project ID, Org ID | MEDIUM |

---

## PART 3: SUPABASE EXPOSURE AUDIT

### Configuration Files

**File**: `supabase/config.toml`
- Tracked in git ✓
- Contents: Local development configuration (port 54321, schema config, DB setup)
- **No credentials** — Uses `.env.local` for secrets (not tracked)

**File**: `.env.local` (Local only)
- **Status**: Not committed to git ✓
- **Contents**: 
  - `SUPABASE_PUBLISHABLE_KEY` (designed for client use)
  - `SUPABASE_URL` (production database endpoint)
  - `VERCEL_OIDC_TOKEN` (JWT for Vercel deployments)
- **Risk**: If accidentally committed = authentication bypass

### Remote Supabase Considerations

**Known**: Production Supabase instance at `hylknjjhmxsuuwbsslkr.supabase.co`
- Project from `.env.local`: `https://hylknjjhmxsuuwbsslkr.supabase.co`
- RLS (Row-Level Security): **Status unknown** (requires cloud audit)
- Admin access: **Status unknown** (requires cloud audit)
- RPCs: Partially documented in frontend code (`ACCESS.3` migration pending)

---

## PART 4: AUTHENTICATION & ACCESS CONTROL

### Current System

**Auth Methods**:
1. **Supabase Auth** (Primary) — Email-based authentication
2. **Mock Profiles** (Dev/Test) — 5 profiles (visitor, demo, premium, full_access, admin)
3. **Access Codes** — Redemption flow for plan upgrades

**Plans & Access Levels**:
```
┌─ public (sba_quick_drill)
├─ demo (sba_express, open_response_short)
├─ premium (adaptive_express, sat_sprint, sat_practice)
└─ full_access (sba_mock_theory, adaptive_mock_theory, sat_mock, full_simulation)
```

**Session Storage**: LocalStorage + sessionStorage
- Keys: `wset_session_v1`, `wset_access_audit_v1`
- Serialized: Access state, auth status, plan info, permissions

### Security Findings

| Item | Finding | Risk | Status |
|------|---------|------|--------|
| Password reset flow | Implemented in `auth-provider.js` | Depends on Supabase RLS | **Unknown** |
| Admin privilege escalation | Mock admin profile in dev | Test code visible in prod | **MEDIUM** |
| Session hijacking | localStorage-based | XSS could compromise session | **Requires HTTPS** |
| Plan upgrade codes | Client-side validation only | Should validate on backend | **MEDIUM** |
| Supabase RLS | Not visible in frontend code | Must assume properly configured | **Requires audit** |

---

## PART 5: CONTENT PROTECTION

### What Can Be Downloaded

**From Frontend** (via browser):
- ✓ All 578 SBA items (preguntas_data.js)
- ✓ All 106 OR items (lab_payload.js)
- ✓ All 6 SAT wine prompts (session_bank.js)
- ✓ All coaching/mentor strategies (coach_data.js)
- ✓ All access control rules (access-control.js)
- ✓ Complete authentication logic (auth-provider.js)

**From Backend** (GitHub):
- ✓ All knowledge-map nodes (14 causal chains)
- ✓ All misconceptions (20 nodes)
- ✓ All enrichment data (205 items)
- ✓ All configuration files (domain expansions, retrieval rules, etc.)
- ✓ 215 documentation files (system design, roadmap, pedagogical strategy)

**Protection**: None — All assets are public JavaScript and JSON files, downloadable in seconds with standard `wget` or browser DevTools.

---

## PART 6: PUBLIC SURFACE ANALYSIS

### robots.txt

**Status**: ✓ Present and restrictive
```
User-agent: *
Disallow: /

# AI Crawlers explicitly blocked
User-agent: GPTBot, ChatGPT-User, anthropic-ai, Claude-Web, etc.
Disallow: /
```

**Analysis**:
- Correctly blocks all crawlers
- Explicitly blocks AI/LLM bots (GPTBot, anthropic-ai, Claude-Web, etc.)
- **No sitemap**: Intentional (prevents discovery)

### sitemap.xml

**Status**: ✗ Not present ✓ (Good practice)

### Source Maps

**Status**: ✓ None served to clients
- 1,097 .map files found in `node_modules/` (never deployed)
- No source maps in production assets
- Frontend code obfuscation: **Not confirmed** (minification status unknown)

### Debug Routes & Code

**Status**: ✓ Clean
- No `console.log()` calls in production code
- No `debugger` statements
- No debug routes or exposed endpoints
- Admin panel: Requires authentication (mock or Supabase)

### Documentation Exposure

**Frontend docs**: 22 files
- `/docs/ACCESS_*.md` — Access system design
- `/docs/SYSTEM_STATE_AUDIT.md` — Current deployment status
- `/docs/Y1_EXECUTION_REPORT.md` — Project phases and milestones
- `/docs/OR_106_INTEGRATION_REPORT.md` — Open Response implementation

**Backend docs**: 215 files
- `/docs/ARCHITECTURE.md` — Complete system design
- `/docs/ROADMAP_*.md` — Future phases and planning
- `/docs/PEDAGOGICAL_*.md` — Teaching strategy (exported)
- `/docs/CORPUS_GROUNDED_GOLD_BANK.md` — Question classification and quality tiers
- `/docs/DIAGNOSTIC_SBA_*.md` — Diagnostic system design and status

---

## PART 7: GITHUB-SPECIFIC RISKS

### Repository Settings (Observed)

| Setting | Observed | Risk |
|---------|----------|------|
| Visibility | Public | Intentional |
| Forks | Unknown | Could spread IP |
| Issue tracking | Active (implied) | Design details exposed |
| Pull requests | Public | Development history visible |
| Wiki | Unknown | Could document internals |
| Discussions | Unknown | Could expose design intent |

### Commit History Exposure

**Backend** (`WSET-AI-System-push`):
- Recent commits show phase progression: "Phase 4A", "SAT validator", "Adaptive loop"
- Commits reveal: Misconception closure, causal-chain injection, pedagogical strategy
- History enables: Reverse-engineering of design evolution

**Frontend** (`epistemiclab-dashboard`):
- Recent commits: "Full Simulation", "Mentor System", "Open Response Expansion"
- Tags/branches: Could reveal upcoming features

### Risk: Forks & Redistribution

Both repos are forkable without restriction. Fork counter (if visible) shows distribution potential.

---

## PART 8: INTELLECTUAL PROPERTY INVENTORY

### Proprietary Assets Exposed

| Asset | Scope | Files | Status |
|-------|-------|-------|--------|
| **Question Bank** | 578 SBA + 106 OR | preguntas_data.js, lab_payload.js | Public JS |
| **Causal Chains** | 14 nodes (official + heuristic) | knowledge/knowledge-map/causal-chains/ | Public JSON |
| **Misconceptions** | 20 cognitive models | knowledge/knowledge-map/misconceptions/ | Public JSON |
| **Enrichment** | 205 items (35.5% coverage) | knowledge/question-bank/enrichment/ | Public JSON |
| **Mentor System** | Coaching profiles, decision logic | coach_data.js | Public JS |
| **Learner Intelligence** | Taxonomy, profiles | learner_intelligence.js | Public JS |
| **Pedagogical Strategy** | Sequencing, priority rules | knowledge/config/, docs/ | Public JSON + docs |
| **SAT Framework** | Wine structure, scales, aliases | knowledge/sat-framework/ | Public JSON |
| **System Architecture** | 215 design docs | docs/*.md | Public Markdown |

**Total Scope**: ~700+ items + 400+ enrichment assets + 14 causal chains + 20 misconceptions + complete system design

---

## PART 9: VULNERABILITY SURFACE

### Known Vulnerabilities

| Type | Component | Finding | Severity |
|------|-----------|---------|----------|
| **Privilege Escalation** | Mock admin profile | Visible in prod code | MEDIUM |
| **XSS** | Session storage (localStorage) | Depends on HTTPS + SameSite | **Requires Verification** |
| **CSRF** | Access code redemption | Frontend validates; backend unknown | **Requires Verification** |
| **Replay Attack** | Session tokens | localStorage-based; no timestamp validation visible | **Requires Verification** |
| **Supabase RLS Bypass** | Data access control | RLS configuration not visible | **Requires Cloud Audit** |
| **API Rate Limiting** | Supabase config API | No rate limiting visible | **Requires Verification** |
| **Plan Forgery** | Plan validation | Client-side only; backend validation unknown | **Requires Verification** |

---

## PART 10: RISK CLASSIFICATION SUMMARY

### CRITICAL (Active Breaches)
- **Count**: 0 ✓

### HIGH (IP Exposure)
1. **Complete SBA question bank exposed** (578 items + answers + explanations)
2. **Complete OR corpus exposed** (106 items)
3. **Complete causal-chain framework exposed** (14 nodes + pedagogical rationale)
4. **Complete misconception system exposed** (20 nodes + detection + intervention)
5. **Complete mentoring & coaching system exposed** (profiles, decision logic, learner models)

### MEDIUM (Configuration & Auth)
1. **215 documentation files expose system design & roadmap**
2. **Supabase configuration tracked** (no secrets, but structure visible)
3. **Vercel deployment metadata exposed** (repo.json with project/org IDs)
4. **Admin functionality visible** (mock profiles in production code)
5. **Access control matrix exposed** (privilege levels, plan requirements)
6. **Session management via localStorage** (depends on HTTPS + XSS protection)
7. **Learner intelligence taxonomy exposed** (decision patterns visible)

### LOW (Best Practices)
1. **No source maps served** ✓ (Good)
2. **robots.txt restrictive** ✓ (Good)
3. **No obvious debug code** ✓ (Good)
4. **No sensitive env vars in code** ✓ (Good)
5. **Note**: .env.local exists locally with Vercel OIDC token (low-risk, not committed)

---

## PART 11: BUSINESS IMPACT ASSESSMENT

### If This IP Becomes Widely Visible

| Scenario | Impact | Timeline |
|----------|--------|----------|
| **Competitor builds clone** | Loss of differentiation, reduced market value | Weeks |
| **Mass distribution of question bank** | Exam security compromised if used as official | Days |
| **Causal-chain system reverse-engineered** | Competitive pedagogical advantage lost | Weeks |
| **Misconception models published** | Research contribution claimed by others | Months |
| **Mentoring system copied** | SaaS business model threatened | Weeks |

### Protection Strategy

**Current**: Relies on repos being "low-visibility" (GitHub stars = ~0, no marketing)
**Risk**: SEO growth, AI training data crawls, or media coverage → sudden visibility

---

## SUMMARY TABLE

| Category | Finding | Severity | Fixable Now | Notes |
|----------|---------|----------|-------------|-------|
| GitHub Visibility | Both repos public | HIGH | Yes (Private recommended) | IP exposure |
| Question Bank | 578 SBA + 106 OR public | HIGH | Yes (Move to private) | Core product |
| Causal Chains | 14 nodes exposed | HIGH | Yes (Move to private) | Pedagogical IP |
| Documentation | 215+ files expose design | HIGH | Yes (Thin out public docs) | Roadmap visible |
| Source Maps | Not served ✓ | — | Already good | — |
| robots.txt | Restrictive ✓ | — | Already good | — |
| Debug Code | None ✓ | — | Already good | — |
| Supabase Secrets | Not committed ✓ | — | Already good | — |
| Auth System | RLS unknown | MEDIUM | Requires audit | Supabase cloud |
| Admin Access | Mock visible in code | MEDIUM | Yes (Remove dev code) | Low-risk but visible |

---

## NEXT STEPS

**Phase S.2** (Safe Hardening) will address:
1. Remove source maps from deployment
2. Improve security headers (CSP, X-Frame-Options, etc.)
3. Remove debug routes and mock profiles
4. Strengthen robots.txt and add security.txt
5. Move sensitive documentation off public repos
6. Review Supabase RLS (cloud audit)
7. Implement rate limiting

**Phase S.3** (Strategic Decisions):
- Decide whether to make repos private
- Plan knowledge-asset migration strategy
- Define public-vs-private documentation split

---

## AUDIT CHECKLIST

- [x] GitHub visibility audit
- [x] Frontend data exposure analysis
- [x] Backend IP inventory
- [x] API/endpoint exposure
- [x] Authentication architecture review
- [x] Configuration file analysis
- [x] Documentation scope assessment
- [x] Source maps & debug code check
- [x] robots.txt & SEO analysis
- [x] Secret/credential check

**Audit completed**: 2026-06-15 | **No modifications made** (Phase S.1 = read-only)

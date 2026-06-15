# SECURITY RISK MATRIX — EpistemicLab
**Date**: 2026-06-15 | **Scope**: S.1 Audit findings → Risk quantification  
**Format**: CVSS-inspired 5×5 matrix + remediation priority

---

## RISK MATRIX (5×5)

### Axes
- **Likelihood** (1=rare, 5=very likely)
- **Impact** (1=low, 5=critical)
- **Score** = Likelihood × Impact (Max = 25, Red ≥ 15, Orange ≥ 9, Yellow ≥ 5, Green < 5)

---

## RISK ENTRIES

### R1: Complete SBA Question Bank Exposure
**Asset**: 578 SBA items (preguntas_data.js, session_bank.js)  
**Exposure**: Public JavaScript, downloadable in seconds  
**Threat Model**: Competitor clones, mass distribution, exam security compromise

| Factor | Rating | Justification |
|--------|--------|---|
| **Likelihood** | 4 | High visibility (public GitHub) once platform grows; no blocking crawlers |
| **Impact** | 5 | Core product, exam-adjacent; if used as official WSET, catastrophic |
| **Score** | **20** | **CRITICAL** 🔴 |
| **Detectability** | High | Can verify via simple `wget preguntas_data.js` |
| **Exploitability** | Trivial | No authentication required, open API |

**Remediation**:
- Move to private backend API
- Authenticate requests with auth token
- Serve per-user subset only
- **Priority**: P0 (Urgent)

---

### R2: Causal-Chain Framework Exposure
**Asset**: 14 causal-chain nodes (8 CC_* official + 6 HC_* heuristic)  
**Exposure**: Public JSON in knowledge-map directory  
**Threat Model**: Pedagogical IP theft, reverse-engineering, competitive research publication

| Factor | Rating | Justification |
|--------|--------|---|
| **Likelihood** | 3 | Moderate; visible to academics/competitors who find repo |
| **Impact** | 5 | Unique pedagogical architecture; high R&D value; paper-worthy |
| **Score** | **15** | **CRITICAL** 🔴 |
| **Detectability** | High | Findable via GitHub search for "causal chain wine" |
| **Exploitability** | Medium | Requires understanding to reimplement, but all info present |

**Remediation**:
- Move to private backend
- Serve only matched chains to authenticated users
- Document as proprietary IP in LICENSE
- **Priority**: P0 (Urgent)

---

### R3: Misconception System Exposure
**Asset**: 20 misconception nodes + detection logic + intervention strategies  
**Exposure**: Public JSON in knowledge-map/misconceptions directory  
**Threat Model**: Pedagogical pattern theft, competitive system development

| Factor | Rating | Justification |
|--------|--------|---|
| **Likelihood** | 3 | Visible to domain experts; niche but valuable audience |
| **Impact** | 4 | Learner-model IP; significant R&D value but less critical than causal chains |
| **Score** | **12** | **HIGH** 🟠 |
| **Detectability** | High | Findable via GitHub search |
| **Exploitability** | Medium | Requires pedagogical expertise to reuse |

**Remediation**:
- Move to private backend (only inject detected misconceptions to users)
- Keep detection offline
- **Priority**: P1 (Important)

---

### R4: Mentoring & Coaching System Exposure
**Asset**: Mentor profiles, decision logic, learner intelligence taxonomy  
**Exposure**: Public JavaScript (coach_data.js, learner_intelligence.js)  
**Threat Model**: System cloning, copyrighted content theft

| Factor | Rating | Justification |
|--------|--------|---|
| **Likelihood** | 3 | Visible but requires technical understanding to exploit |
| **Impact** | 4 | Valuable IP but less exam-critical than question bank |
| **Score** | **12** | **HIGH** 🟠 |
| **Detectability** | High | Direct download via browser |
| **Exploitability** | Medium | Logic visible; implementation straightforward |

**Remediation**:
- Move coach_data to private API
- Serve per-session mentor profiles only
- Obfuscate decision logic
- **Priority**: P1 (Important)

---

### R5: System Architecture & Roadmap Exposure
**Asset**: 215 documentation files (system design, pedagogical strategy, roadmap)  
**Exposure**: Public Markdown in docs/ directory  
**Threat Model**: Competitor intelligence, product strategy analysis, feature roadmap leakage

| Factor | Rating | Justification |
|--------|--------|---|
| **Likelihood** | 3 | Visible to motivated competitors; not indexed but findable |
| **Impact** | 4 | Roadmap and strategy valuable; less critical than product IP |
| **Score** | **12** | **HIGH** 🟠 |
| **Detectability** | High | GitHub search, direct browse |
| **Exploitability** | Medium | Documentation clear but requires understanding context |

**Remediation**:
- Remove roadmap docs from public repo
- Keep only architecture overview
- Move detailed design docs to private wiki
- **Priority**: P1 (Important)

---

### R6: Open Response Corpus Exposure
**Asset**: 106 OR items (lab_payload.js)  
**Exposure**: Public JavaScript with feedback profiles and causal targets  
**Threat Model**: Exam compromise, cloning

| Factor | Rating | Justification |
|--------|--------|---|
| **Likelihood** | 3 | Smaller scope than SBA; still public |
| **Impact** | 4 | Exam-adjacent; less critical than 578 SBA items |
| **Score** | **12** | **HIGH** 🟠 |
| **Detectability** | High | Direct access |
| **Exploitability** | Trivial | Plain text, fully exposed |

**Remediation**:
- Move to private API
- Authenticate with auth token
- **Priority**: P1 (Important)

---

### R7: SAT Wine Framework Exposure
**Asset**: 6 SAT wine prompts (session_bank.js)  
**Exposure**: Public JavaScript  
**Threat Model**: Exam-adjacent; research value

| Factor | Rating | Justification |
|--------|--------|---|
| **Likelihood** | 2 | Small scope (only 6 wines); niche audience |
| **Impact** | 4 | Exam-adjacent; educational research value |
| **Score** | **8** | **MEDIUM** 🟡 |
| **Detectability** | High | Direct access |
| **Exploitability** | Trivial | Plain data |

**Remediation**:
- Move to private API
- Keep governance flags (`safe_for_examiner=false`)
- **Priority**: P2 (Moderate)

---

### R8: Supabase Configuration Exposure
**Asset**: supabase/config.toml (public schema config)  
**Exposure**: Git tracked, public repo  
**Threat Model**: Reconnaissance for Supabase instance, endpoint mapping

| Factor | Rating | Justification |
|--------|--------|---|
| **Likelihood** | 2 | Dev config; no credentials; limited value |
| **Impact** | 3 | Could reveal Supabase instance structure |
| **Score** | **6** | **MEDIUM** 🟡 |
| **Detectability** | High | Direct file access |
| **Exploitability** | Medium | Requires Supabase knowledge |

**Remediation**:
- Move to .env (not tracked)
- Document in wiki
- **Priority**: P2 (Moderate)

---

### R9: Vercel Deployment Metadata Exposure
**Asset**: .vercel/repo.json (project/org IDs)  
**Exposure**: Git tracked, public repo  
**Threat Model**: Account takeover, project compromise

| Factor | Rating | Justification |
|--------|--------|---|
| **Likelihood** | 1 | Requires Vercel access; IDs alone insufficient |
| **Impact** | 3 | Could aid targeted Vercel account compromise |
| **Score** | **3** | **LOW** 🟢 |
| **Detectability** | High | Direct file |
| **Exploitability** | Low | IDs alone don't grant access |

**Remediation**:
- Move .vercel to .gitignore (safe if no secrets present)
- **Priority**: P3 (Low)

---

### R10: Admin Functionality Visible in Prod Code
**Asset**: Mock admin profile in login.js (production code)  
**Exposure**: Public JavaScript  
**Threat Model**: Privilege escalation via local dev bypass

| Factor | Rating | Justification |
|--------|--------|---|
| **Likelihood** | 2 | Requires bypassing Supabase auth; limited vector |
| **Impact** | 3 | Admin access would be significant |
| **Score** | **6** | **MEDIUM** 🟡 |
| **Detectability** | High | Direct code inspection |
| **Exploitability** | Low | Supabase auth still required |

**Remediation**:
- Remove mock profiles from production build
- Keep in dev environment only
- Use feature flags
- **Priority**: P2 (Moderate)

---

### R11: Session Hijacking via localStorage
**Asset**: Session data in localStorage (access_session_v1, wset_session_v1)  
**Exposure**: JavaScript accessible to XSS attacks  
**Threat Model**: Account hijacking, learner data theft

| Factor | Rating | Justification |
|--------|--------|---|
| **Likelihood** | 2 | Requires XSS or network MITM; HTTPS helps |
| **Impact** | 4 | Could compromise learner account + data |
| **Score** | **8** | **MEDIUM** 🟡 |
| **Detectability** | Medium | Requires XSS vulnerability |
| **Exploitability** | Medium | Depends on XSS + no SameSite flags |

**Remediation**:
- Use HttpOnly cookies for sensitive tokens
- Implement CSP (Content Security Policy)
- Add SameSite=Strict flags
- **Priority**: P2 (Moderate)

---

### R12: Supabase RLS Unknown Configuration
**Asset**: Row-Level Security policies (not visible in repo)  
**Exposure**: Cloud-side; unknown  
**Threat Model**: Unauthorized data access, lateral movement

| Factor | Rating | Justification |
|--------|--------|---|
| **Likelihood** | 2 | Unknown; assume defaults (risky) |
| **Impact** | 5 | Could expose learner data, user accounts |
| **Score** | **10** | **HIGH** 🟠 |
| **Detectability** | Low | Requires cloud audit |
| **Exploitability** | Medium | If RLS weak, easy to bypass |

**Remediation**:
- Audit Supabase RLS policies
- Document row-level rules
- Implement least-privilege access
- **Priority**: P1 (Important)

---

### R13: Plan Validation Client-Side Only
**Asset**: Access control logic (evaluateModeAccess in access-control.js)  
**Exposure**: Public JavaScript  
**Threat Model**: Privilege escalation, free access to premium features

| Factor | Rating | Justification |
|--------|--------|---|
| **Likelihood** | 4 | Trivial to bypass (localStorage edit) |
| **Impact** | 3 | Could access premium features without payment |
| **Score** | **12** | **HIGH** 🟠 |
| **Detectability** | Medium | Browser DevTools required |
| **Exploitability** | Trivial | Simple localStorage hack |

**Remediation**:
- Validate plan on backend (Supabase RPC)
- Use auth token, not localStorage
- Implement server-side plan verification
- **Priority**: P0 (Urgent)

---

### R14: API Rate Limiting Unknown
**Asset**: Supabase APIs (auth, data, RPC)  
**Exposure**: Cloud-side; unknown  
**Threat Model**: DoS, brute force, account enumeration

| Factor | Rating | Justification |
|--------|--------|---|
| **Likelihood** | 3 | Common attack vector |
| **Impact** | 3 | Could disrupt service; learner data at risk |
| **Score** | **9** | **HIGH** 🟠 |
| **Detectability** | Low | Requires load testing |
| **Exploitability** | Medium | Standard DoS techniques |

**Remediation**:
- Verify Supabase rate limiting is enabled
- Implement client-side throttling
- Monitor API logs for anomalies
- **Priority**: P1 (Important)

---

## RISK RANKING (by Score × Priority)

| Rank | ID | Issue | Score | Priority | Action |
|------|----|----|-------|----------|--------|
| 1 | R1 | SBA question bank exposure | 20 | P0 | Move to private API |
| 2 | R2 | Causal-chain framework | 15 | P0 | Move to private backend |
| 3 | R13 | Plan validation client-side | 12 | P0 | Backend validation |
| 4 | R3 | Misconceptions exposure | 12 | P1 | Move to private API |
| 5 | R4 | Mentoring system exposure | 12 | P1 | Move to private API |
| 6 | R5 | Roadmap & design docs | 12 | P1 | Remove from public repo |
| 7 | R6 | OR corpus exposure | 12 | P1 | Move to private API |
| 8 | R12 | Supabase RLS unknown | 10 | P1 | Cloud audit + document |
| 9 | R14 | API rate limiting unknown | 9 | P1 | Verify + implement |
| 10 | R7 | SAT wine exposure | 8 | P2 | Move to private API |
| 11 | R11 | Session hijacking risk | 8 | P2 | HttpOnly cookies + CSP |
| 12 | R8 | Supabase config exposure | 6 | P2 | Move to .env |
| 13 | R10 | Admin mock visible | 6 | P2 | Remove from prod build |
| 14 | R9 | Vercel metadata exposure | 3 | P3 | Move to .gitignore |

---

## HEAT MAP

```
Impact
  5 │ R1(20) R2(15)                 
  4 │ R3(12) R4(12) R5(12) R6(12)   R12(10)
  3 │ R7(8)  R8(6)  R10(6) R13(12)  R14(9)
  2 │ R11(8) R9(3)                  
  1 │                                
    └─────────────────────────────
      1    2    3    4    5
           Likelihood
```

**Legend**:
- 🔴 **CRITICAL** (Score ≥ 15): R1, R2
- 🟠 **HIGH** (Score 9-14): R3, R4, R5, R6, R12, R13, R14
- 🟡 **MEDIUM** (Score 5-8): R7, R8, R10, R11
- 🟢 **LOW** (Score < 5): R9

---

## REMEDIATION ROADMAP

### Phase S.2 (Safe Hardening) — P0/P1 Items Only
- [ ] Move SBA bank to private API (R1)
- [ ] Move causal-chain framework to private API (R2)
- [ ] Implement backend plan validation (R13)
- [ ] Move OR corpus to private API (R6)
- [ ] Audit & document Supabase RLS (R12)
- [ ] Verify API rate limiting (R14)
- [ ] Move misconceptions to private (R3)
- [ ] Move mentoring system to private (R4)
- [ ] Remove roadmap docs (R5)

### Phase S.3 (Strategic Decisions) — P2 Items
- [ ] Implement HttpOnly cookies (R11)
- [ ] Move Supabase config (R8)
- [ ] Remove mock admin from prod (R10)

### Phase S.4 (Long-term) — Architectural
- [ ] Make backend repo private
- [ ] Make frontend repo private (or thin public)
- [ ] Implement unified content API
- [ ] Document security.txt and .well-known/security.json

---

## COMPLIANCE & AUDIT

| Criterion | Status | Notes |
|-----------|--------|-------|
| GDPR Readiness | Unknown | Requires Supabase audit |
| Data Retention Policy | Unknown | Learner data retention unknown |
| Encryption in Transit | Assumed ✓ | HTTPS required on production domain |
| Encryption at Rest | Unknown | Supabase cloud config unknown |
| Access Logging | Unknown | Supabase logs not visible |
| Backup Strategy | Unknown | Supabase backup config unknown |
| Incident Response | Unknown | No documented plan |
| Penetration Testing | None | Recommended before public launch |

---

**Risk Matrix completed**: 2026-06-15 | **Audit findings quantified**  
**Next phase**: S.2 (Safe Hardening implementation)

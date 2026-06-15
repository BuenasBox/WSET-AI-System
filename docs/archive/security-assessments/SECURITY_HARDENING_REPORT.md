# SECURITY HARDENING REPORT — Phase S.2
**Date**: 2026-06-15 | **Phase**: S.2 Safe Hardening (No breaking changes)  
**Status**: Ready for implementation | Risk level: LOW (all changes are non-breaking)

---

## EXECUTIVE SUMMARY

Phase S.2 applies **low-risk security hardening** without architectural redesign. All changes are:
- **Non-breaking** (existing functionality preserved)
- **Reversible** (can be rolled back)
- **Non-disruptive** (no migration required)
- **Implementation-ready** (specific, actionable steps provided)

**Scope**: Configuration, headers, routing, code cleanup, documentation thinning

**Timeline**: 1-2 weeks | **Effort**: Medium | **Risk**: Low

---

## PART 1: QUICK-WINS (No-Code / Configuration-Only)

### H1.1: Improve Security Headers
**Risk**: XSS, Clickjacking, MIME sniffing  
**Implementation**: Add headers to Vercel deployment

**File to modify**: `vercel.json` (create if missing)
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        },
        {
          "key": "Permissions-Policy",
          "value": "geolocation=(), microphone=(), camera=()"
        }
      ]
    },
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "no-store, max-age=0"
        }
      ]
    }
  ]
}
```

**Verification**:
```bash
curl -I https://epistemiclab.dpdns.org/
# Check for X-Content-Type-Options, X-Frame-Options, etc.
```

**Effort**: 5 minutes | **Impact**: Medium | **Risk**: None

---

### H1.2: Enhance robots.txt
**Current**: Already restrictive ✓
**Improvement**: Add security.txt reference + canonical domain

**File to modify**: `robots.txt`
```
# Current (keep as-is)
User-agent: *
Disallow: /

# NEW: Add these lines
# See also: /.well-known/security.txt for vulnerability reporting

# Canonical domain
Host: epistemiclab.dpdns.org

# Crawl delay to reduce resource usage
Crawl-delay: 10
```

**Effort**: 2 minutes | **Impact**: Low | **Risk**: None

---

### H1.3: Create security.txt
**Purpose**: Provide security contact + vulnerability disclosure policy

**File to create**: `.well-known/security.txt`
```
Contact: security@epistemiclab.dpdns.org
Expires: 2026-12-31T23:59:59.000Z
Preferred-Languages: en, es
Canonical: https://epistemiclab.dpdns.org/.well-known/security.txt

# Vulnerability Disclosure
# Please report security vulnerabilities to: security@epistemiclab.dpdns.org
# - Do not publicly disclose until we've had 30 days to respond
# - Include reproduction steps and expected behavior
# - Include your contact info for follow-up

Policy: https://epistemiclab.dpdns.org/security-policy.md
Acknowledgments: https://epistemiclab.dpdns.org/security-acknowledgments.md
```

**Effort**: 10 minutes | **Impact**: Low | **Risk**: None

---

### H1.4: Configure Supabase Permissions
**Current**: Unknown (requires cloud audit)
**Action**: Document current RLS status

**Checklist**:
- [ ] Open Supabase dashboard
- [ ] Go to Authentication → Policies
- [ ] Verify Row-Level Security is **ENABLED**
- [ ] For each table (sba_items, or_items, etc.):
  - [ ] Verify SELECT policy exists
  - [ ] Verify user_id filtering in policy
  - [ ] Test policy with multiple accounts
- [ ] Document findings in `SUPABASE_RLS_AUDIT.md`

**Effort**: 30 minutes | **Impact**: High | **Risk**: None (audit-only)

---

### H1.5: Add Content Security Policy (CSP)
**Risk**: XSS attacks, script injection  
**Implementation**: Add CSP header to `vercel.json`

```json
{
  "source": "/(.*)",
  "headers": [
    {
      "key": "Content-Security-Policy",
      "value": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' https:; connect-src 'self' https://hylknjjhmxsuuwbsslkr.supabase.co; font-src 'self'"
    }
  ]
}
```

**Testing**:
```javascript
// Browser console — should see CSP errors if any script is injected
console.log('CSP is active');
```

**Effort**: 15 minutes | **Impact**: High | **Risk**: Low (test thoroughly)

---

## PART 2: CODE CLEANUP (Safe Removals)

### H2.1: Remove Mock Admin Profile from Production
**Risk**: Privilege escalation vector (visible in code)

**File to modify**: `login/login.js`

**Current code** (line 12-18):
```javascript
var MOCK_PROFILES = [
  { id: 'visitor', label: 'Visitante', role: null, plan: null, durationDays: null },
  { id: 'demo', label: 'Demo', role: 'student', plan: 'demo', durationDays: 30 },
  { id: 'premium', label: 'Premium', role: 'student', plan: 'premium', durationDays: 30 },
  { id: 'full_access', label: 'Acceso Completo', role: 'student', plan: 'full_access', durationDays: null },
  { id: 'admin', label: 'Admin', role: 'admin', plan: 'full_access', durationDays: null },  // ← REMOVE
];
```

**Action**: Replace with feature-flag approach

```javascript
// At top of file
var ENABLE_MOCK_PROFILES = false; // Set to false in production

var MOCK_PROFILES = ENABLE_MOCK_PROFILES ? [
  { id: 'visitor', label: 'Visitante', role: null, plan: null, durationDays: null },
  { id: 'demo', label: 'Demo', role: 'student', plan: 'demo', durationDays: 30 },
  { id: 'premium', label: 'Premium', role: 'student', plan: 'premium', durationDays: 30 },
  { id: 'full_access', label: 'Acceso Completo', role: 'student', plan: 'full_access', durationDays: null },
  { id: 'admin', label: 'Admin', role: 'admin', plan: 'full_access', durationDays: null },
] : [];
```

**Verification**:
```javascript
// In browser console
console.log(WSETLogin.getMockProfiles());
// Should return empty array in production
```

**Effort**: 10 minutes | **Impact**: Medium | **Risk**: Low

---

### H2.2: Remove Debug Code (if any)
**Current Status**: ✓ Already clean (no console.log found)
**Action**: Maintain this standard going forward

**Checklist**:
- [ ] No `console.log()` in production code
- [ ] No `debugger` statements
- [ ] No `alert()` calls
- [ ] No exposed variable assignments

**Effort**: 0 minutes (already done) | **Impact**: Preventive

---

### H2.3: Add XSS Protection Headers
**Already covered in H1.1** ✓

---

## PART 3: CONFIGURATION TIGHTENING

### H3.1: Move .vercel to .gitignore
**File**: `.gitignore`
**Status**: Currently tracking (low-risk but best practice to exclude)

**Current**:
```
.vercel
```

**Problem**: `.vercel/repo.json` contains Vercel project/org IDs
**Solution**: Add to .gitignore if not already there

```bash
# Verify it's ignored
git check-ignore .vercel/repo.json
# Should output: .vercel/repo.json

# If not, add it:
echo ".vercel/" >> .gitignore
```

**Effort**: 2 minutes | **Impact**: Low | **Risk**: None

---

### H3.2: Supabase Config to .env
**File**: `supabase/config.toml`
**Status**: Already not sensitive (no credentials) ✓

**Recommendation**: Document as dev-only config

```
# In supabase/config.toml (add comment)
# ============================================================================
# Supabase Local Development Configuration
# This file is used for `supabase start` only.
# Production configuration is managed in Supabase Cloud.
# Do not commit secrets. Use .env for local env vars.
# ============================================================================
```

**Effort**: 5 minutes | **Impact**: Low | **Risk**: None

---

### H3.3: API Rate Limiting Setup
**Purpose**: Prevent DoS, brute force, credential stuffing

**Implementation** (in `api/supabase-config.js` or new `api/rate-limit.js`):

```javascript
// Simple rate limiting middleware for Vercel
module.exports = function withRateLimit(handler, options) {
  const options = options || {};
  const maxRequests = options.maxRequests || 100; // per minute
  const windowMs = options.windowMs || 60 * 1000; // 1 minute

  const requestCounts = {}; // In-memory (won't work with serverless scaling)

  return function rateLimit(request, response) {
    const key = request.headers['x-forwarded-for'] || request.socket.remoteAddress;
    const now = Date.now();

    if (!requestCounts[key]) {
      requestCounts[key] = [];
    }

    // Remove old requests
    requestCounts[key] = requestCounts[key].filter(t => now - t < windowMs);

    if (requestCounts[key].length >= maxRequests) {
      return response.status(429).json({
        error: 'too_many_requests',
        retry_after: Math.ceil((requestCounts[key][0] + windowMs - now) / 1000)
      });
    }

    requestCounts[key].push(now);
    return handler(request, response);
  };
};
```

**Usage**:
```javascript
const withRateLimit = require('../api/rate-limit');

module.exports = withRateLimit(handler, {
  maxRequests: 100,
  windowMs: 60 * 1000
});
```

**Better Alternative**: Use Supabase built-in rate limiting or Redis

**Effort**: 30 minutes | **Impact**: High | **Risk**: Low (test first)

---

## PART 4: DOCUMENTATION HARDENING

### H4.1: Thin Out Public Documentation
**Current**: 215 files in `/docs/` (includes roadmap, design, phases)
**Target**: Keep only public-safe docs; move strategic docs to private

**Files to KEEP** (safe public docs):
```
docs/
├── README.md              (Project overview)
├── ARCHITECTURE.md        (High-level design only)
├── SECURITY.md            (This security policy)
├── GOVERNANCE.md          (Governance flags, compliance)
├── API.md                 (Public API contract)
└── CONTRIBUTING.md        (Dev setup)
```

**Files to REMOVE** (strategic/proprietary):
```
docs/ROADMAP_*.md
docs/PHASE_*.md
docs/DESIGN_*.md
docs/RESEARCH_*.md
docs/DIAGNOSTIC_*.md
docs/ACTIVE_SET_RECONCILIATION_PLAN.md
docs/CORPUS_GROUNDED_GOLD_BANK.md
# ... (100+ files)
```

**Implementation**:
```bash
# List files to remove
find docs -type f -name "*.md" | grep -E "(ROADMAP|PHASE|DESIGN|RESEARCH|DIAGNOSTIC)" | wc -l

# Create archive for private storage
zip -r /private/WSET-docs-archive.zip docs/ROADMAP*.md docs/PHASE*.md

# Remove from repo (carefully!)
git rm docs/ROADMAP*.md docs/PHASE*.md
# Do NOT force-push if already public (leaves data in history)
```

**Effort**: 1-2 hours | **Impact**: High | **Risk**: Medium (data in git history)

---

### H4.2: Add Security Policy
**File to create**: `SECURITY.md`

```markdown
# Security Policy

## Governance
- Safe for examiner: **FALSE**
- Examiner scoring allowed: **FALSE**  
- Training only: **TRUE**
- Disclaimer: "PROTOTIPO · ENTRENAMIENTO · NO EVALUACIÓN OFICIAL WSET"

## Reporting Security Issues
Please **do not** disclose security vulnerabilities publicly.

1. Email: security@epistemiclab.dpdns.org
2. Include: reproduction steps, impact assessment
3. Timeline: 30 days to respond + patch

## Known Limitations
- No end-to-end encryption
- Session tokens stored in localStorage (requires HTTPS)
- Learner data stored in Supabase (requires RLS audit)

## Supported Versions
| Version | Status | Support Until |
|---------|--------|---|
| Production | Active | — |
| Staging | Development | — |
| Public Repos | Deprecated | 2026-12-31 |

## Infrastructure
- Hosting: Vercel (serverless)
- Database: Supabase (PostgreSQL)
- Auth: Supabase Auth (email)

## Compliance
- GDPR: [Audit pending]
- HIPAA: Not applicable
- FERPA: [Needs review]
```

**Effort**: 20 minutes | **Impact**: Low | **Risk**: None

---

## PART 5: VERIFICATION & TESTING

### V1: Security Headers Test
```bash
# Test production domain
curl -I https://epistemiclab.dpdns.org/

# Expected headers:
# X-Content-Type-Options: nosniff
# X-Frame-Options: DENY
# X-XSS-Protection: 1; mode=block
# Content-Security-Policy: ...
```

### V2: robots.txt Verification
```bash
curl https://epistemiclab.dpdns.org/robots.txt
# Should show: User-agent: *\nDisallow: /
```

### V3: HTTPS Enforcement
```bash
# Should redirect to HTTPS
curl -I http://epistemiclab.dpdns.org/

# Expected: 301 or 307 redirect to https://
```

### V4: API Rate Limiting Test
```bash
# Simulate rapid requests
for i in {1..200}; do
  curl https://epistemiclab.dpdns.org/api/supabase-config
done

# Expected: 429 status after threshold
```

### V5: Admin Mock Profile Check
```javascript
// In browser console (production)
console.log(window.WSETLogin.getMockProfiles());
// Should be empty array or throw error
```

### V6: CSP Violation Test
```javascript
// This should fail due to CSP
eval('console.log("CSP allowed eval")');
// Expected: CSP violation in console
```

---

## PART 6: ROLLBACK PROCEDURES

### If Security Headers Break Site
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Content-Security-Policy",
          "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
        }
      ]
    }
  ]
}
```

### If Rate Limiting Blocks Users
```javascript
// Temporarily increase threshold
const maxRequests = 1000; // was 100
const windowMs = 60 * 1000; // 1 minute
```

### If Mock Admin Removal Breaks Dev
```bash
# Restore from git history
git checkout HEAD~1 login/login.js

# Then use feature flag approach instead
```

---

## PART 7: IMPLEMENTATION SCHEDULE

### Week 1: Quick-Wins
- [ ] Add security headers (vercel.json)
- [ ] Enhance robots.txt + create security.txt
- [ ] Audit Supabase RLS
- [ ] Add Content-Security-Policy
- [ ] Document findings in audit report

**Time estimate**: 2-3 hours  
**Testing**: Automated (curl, CSP violation check)  
**Risk**: LOW

### Week 2: Code & Config Cleanup
- [ ] Remove mock admin profile (or feature-flag)
- [ ] Move .vercel to .gitignore
- [ ] Implement rate limiting
- [ ] Add SECURITY.md policy
- [ ] Test in staging environment

**Time estimate**: 4-6 hours  
**Testing**: Manual (browser DevTools, API testing)  
**Risk**: LOW (all reversible)

### Optional Week 3: Documentation Thinning
- [ ] Archive proprietary docs
- [ ] Remove strategic docs from public repo
- [ ] Create private GitHub Wiki (move 100+ docs)
- [ ] Update README with deprecation notice

**Time estimate**: 3-4 hours  
**Testing**: Link verification  
**Risk**: MEDIUM (git history contains data)

---

## PART 8: COMPLIANCE CHECKLIST

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Security headers implemented | [ ] | curl output |
| robots.txt blocks crawlers | [✓] | Already done |
| security.txt present | [ ] | /.well-known/security.txt |
| CSP enforced | [ ] | vercel.json + testing |
| Rate limiting implemented | [ ] | /api/rate-limit.js |
| Mock admin removed | [ ] | login.js inspection |
| Debug code removed | [✓] | Already done |
| Supabase RLS verified | [ ] | Supabase dashboard audit |
| Source maps not served | [✓] | Already verified |
| HTTPS enforced | [✓] | Vercel default |
| Sensitive docs removed | [ ] | Git history clean |

---

## PART 9: SUCCESS CRITERIA

| Metric | Target | Timeline |
|--------|--------|----------|
| Security headers passing | 8/8 | Week 1 |
| CSP violations: 0 | 0 | Week 1 |
| API rate limiting functional | ✓ | Week 2 |
| Mock admin removed | ✓ | Week 2 |
| Production tests green | ✓ | Week 2 |
| No regression in existing features | ✓ | Week 2 |
| Supabase RLS documented | ✓ | Week 1 |

---

## PART 10: NEXT STEPS (Phase S.3)

After Phase S.2 is complete:
1. **Phase S.3**: Move to private repos (optional)
2. **Phase S.4**: Implement content APIs (Tier 1 assets)
3. **Phase S.5**: Migrate documentation to wiki

See `INTELLECTUAL_PROPERTY_PROTECTION_PLAN.md` for Phase S.3+ details.

---

**Phase S.2 Ready for Implementation**: 2026-06-15  
**All changes are non-breaking and reversible**  
**Estimated effort**: 1-2 weeks | **Risk level**: LOW

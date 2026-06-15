# COMMERCIALIZATION SECURITY REPORT — Phase S.2B
**Date**: 2026-06-15 | **Focus**: Revenue protection, IP theft prevention, SaaS abuse mitigation  
**Scope**: Content extraction, subscription bypass, account sharing, automated scraping  

---

## EXECUTIVE SUMMARY

EpistemicLab is **revenue-critical but commercially vulnerable**. Current architecture embeds all content in public JavaScript files, relies on client-side plan validation, has no device/session controls, and lacks abuse detection mechanisms.

**Risk Assessment**:
- 🔴 **CRITICAL**: Content embedding (578 SBA + 106 OR items trivially downloadable)
- 🔴 **CRITICAL**: Plan validation is client-side only (privilege escalation trivial)
- 🟠 **HIGH**: No account sharing detection (one account = unlimited users)
- 🟠 **HIGH**: No automated scraping protection
- 🟠 **HIGH**: No concurrent session/device limits
- 🟡 **MEDIUM**: Trial abuse possible (unlimited free accounts)
- 🟡 **MEDIUM**: Access code redemption has no rate limiting

**Revenue Impact**: If these vulnerabilities are exploited, estimated **40-60% revenue leakage** before any monetization begins.

**Good News**: All risks are addressable through non-breaking changes to Phase S.2 and parallel implementation of Phase S.4 (content API).

---

## PART 1: CONTENT EXTRACTION VULNERABILITY ASSESSMENT

### Attack Surface 1: SBA Question Bank (578 items)

**Current Exposure**:
- **File**: `diagnostic-sba/preguntas_data.js`
- **Format**: `window.PREGUNTAS_BANK = { items: [...] }`
- **Content**: Full questions, correct answers, causal chains, feedback
- **Access**: Zero authentication, public HTTP/S, embedded in page source

**Extraction Methods** (Trivial difficulty):

| Method | Time | Skill | Detection |
|--------|------|-------|-----------|
| Browser DevTools → Copy source | 30 sec | None | None |
| `curl preguntas_data.js` | 1 min | Basic | None |
| Open in text editor | 30 sec | None | None |
| JavaScript `fetch()` | 2 min | Basic | None |
| Python `requests.get()` | 1 min | Basic | None |
| Browser extension | 5 min | Medium | Possible |

**Use Cases for Stolen Content**:
1. **Competitor clones platform** → Same questions, same curriculum
2. **Third-party aggregator** → Copies to Quizlet, AnkiWeb, StudyBlue, etc.
3. **Content reseller** → Repackages as "Wine Study Guide"
4. **Leaked to candidates** → Exam security compromised
5. **AI training data** → Training data for wine-AI competitors

**Business Impact**: 
- **Immediate**: Curriculum IP loses differentiation
- **Medium-term**: Competitors undercut pricing (no R&D cost)
- **Long-term**: Exam security compromised if leaked to candidates

**Mitigation**: Move to private API (Phase S.4), serve per-user subset, rate limit by subscription tier

---

### Attack Surface 2: Open Response Corpus (106 items)

**Current Exposure**:
- **File**: `open-response-lab/lab_payload.js`
- **Format**: `window.OPEN_RESPONSE_LAB_PAYLOAD = { evaluation_by_item_id: {...} }`
- **Content**: Item IDs, expected concepts, causal-chain targets, feedback profiles
- **Access**: Zero authentication, public HTTP/S

**Extraction Risk**: **IDENTICAL to SBA** (same vulnerability, smaller corpus)

**Mitigation**: Move to private API (Phase S.4)

---

### Attack Surface 3: SAT Wine Prompts (6 items)

**Current Exposure**:
- **File**: `adaptive-session/session_bank.js`
- **Format**: Embedded in session mode definitions
- **Content**: Wine structure, observation patterns, evaluation criteria
- **Access**: Zero authentication, public HTTP/S

**Extraction Risk**: **MEDIUM** (smaller corpus, high exam-relevance)

**Unique Threat**: SAT wines are practice-adjacent; if leaked to actual candidates, exam security = 0

**Mitigation**: Move to private API (Phase S.4), refresh wines annually

---

### Attack Surface 4: Coaching Data (Mentor Profiles)

**Current Exposure**:
- **File**: `adaptive-session/coach_data.js`
- **Format**: Mentor profiles, coaching strategies, learner intelligence
- **Content**: Coaching decision logic, pedagogical approach, personality profiles
- **Access**: Zero authentication, public HTTP/S

**Extraction Risk**: **MEDIUM-HIGH** (proprietary coaching framework)

**Use Cases**:
1. Competitor rebuilds coaching system (reverse-engineering)
2. Academic researchers publish coaching patterns
3. Third-party tutors adopt same strategies

**Mitigation**: Move coaching injection to backend RPC; serve only matched profiles

---

## PART 2: INTELLECTUAL PROPERTY EXTRACTION ASSESSMENT

### IP Asset 1: Causal-Chain Framework (14 nodes)

**Current Exposure**:
- **Location**: `knowledge/knowledge-map/causal-chains/*.json` (public repo)
- **Format**: JSON with causa → mecanismo → efecto → formulación_examen
- **Content**: Complete pedagogical reasoning for 14 core wine concepts
- **Access**: Git clone (trivial), GitHub search (findable)

**IP Value**: **VERY HIGH**
- Represents ~2 years of pedagogical R&D
- Unique teaching methodology
- Patent-worthy (pedagogical approach)
- Publishable research (academic value)

**Theft Scenarios**:
1. **Academic publication** → Researcher publishes "Teaching Wine Through Causal Chains"
2. **Competitor adoption** → WSET competitor reimplements causal-chain approach
3. **Content licensing** → Third party licenses to other tutoring platforms
4. **AI training** → OpenAI/Anthropic trains on causal-chain patterns

**Mitigation**: Keep nodes in private backend; inject only matched chains to authenticated users

---

### IP Asset 2: Misconception Models (20 nodes)

**Current Exposure**:
- **Location**: `knowledge/knowledge-map/misconceptions/*.json` (public repo)
- **Format**: Misconception + detection keywords + intervention strategy
- **Content**: Learner cognitive models for wine education
- **Access**: Git clone (trivial)

**IP Value**: **HIGH**
- Represents learner modeling research
- Unique misconception taxonomy (wine-specific)
- Applicable to other domains (transferable)

**Theft Scenarios**:
1. **Learner modeling vendor** → Adopts misconception framework
2. **Academic research** → Papers on wine education misconceptions
3. **Competitor system** → Reuses detection + intervention logic

**Mitigation**: Keep nodes in private backend; serve only detected misconceptions

---

### IP Asset 3: Mentoring & Coaching System

**Current Exposure**:
- **Location**: `coach_data.js`, `learner_intelligence.js` (public)
- **Content**: Mentor profiles, coaching decision trees, personality models
- **Access**: Direct file download (trivial)

**IP Value**: **MEDIUM-HIGH**
- Unique adaptive coaching approach
- Non-obvious coaching decision logic
- Transferable to other subjects

**Theft Scenarios**:
1. **Competitor rebuilds coaching** → Reverse-engineering visible logic
2. **Third-party coaching platform** → Adopts same patterns
3. **Tutor marketplace** → Coaches use same strategies (harder to differentiate)

**Mitigation**: Move coaching injection to backend; obfuscate decision trees

---

### IP Asset 4: Evaluator Framework

**Current Exposure**:
- **Location**: `knowledge/distinction-patterns/`, `knowledge/evaluator-framework/` (semi-public)
- **Content**: Mark allocation rules, quality reasoning patterns, readiness reasoning
- **Access**: Backend repo (less exposed than frontend)

**IP Value**: **MEDIUM**
- SAT-specific evaluation criteria
- Quality reasoning patterns (exam-grading relevant)

**Theft Scenarios**:
1. **Exam coaching services** → Use patterns to teach to SAT
2. **Mark prediction models** → Predict SAT scores with evaluator rules
3. **Competitor tutoring** → Reuse quality reasoning

**Mitigation**: Keep evaluator framework private; expose only through Tutor API

---

## PART 3: COMMERCIAL ABUSE VULNERABILITY ASSESSMENT

### Abuse 1: Account Sharing (Unlimited Users Per Account)

**Current State**: ✅ **VULNERABLE**
- No device fingerprinting
- No concurrent session limits
- No geo-location tracking
- No IP-based session control
- Family sharing not possible (but not prevented)

**Exploit Scenario**:
```
1. User A purchases "full_access" account ($X/month)
2. User A shares credentials with 5 study groups (5-50 users total)
3. Platform sees 1 paying user, actually 50 users
4. Revenue impact: 50 users, 1 subscription = 49 free rides
```

**Risk Quantification**:
- **Likely**: 20-30% of users will share with study groups (normal behavior)
- **Revenue impact**: 20-50% of subscription revenue lost to sharing

**Detection Methods**: Browser fingerprinting, IP geolocation, session anomaly detection

**Mitigation**: Implement device controls + concurrent session limits (Phase S.2B.1)

---

### Abuse 2: Trial Account Abuse

**Current State**: ✅ **VULNERABLE**
- `demo` plan allows access to Diagnostic SBA + Open Response Lab
- No rate limiting on account creation
- No payment method required for demo
- No email verification (likely)
- No trial duration enforcement

**Exploit Scenario**:
```
1. Attacker creates 100 demo accounts (5 min, scripted)
2. Each account gets Diagnostic SBA + OR Lab access
3. Combined: ~550+ practice items available for free (no payment)
4. 100 accounts × 2 experiences = complete curriculum for free
```

**Risk Quantification**:
- **Likely**: 5-15% of users will create multiple accounts
- **Revenue impact**: 10-30% of conversion to premium lost

**Detection Methods**: Email domain analysis, IP rate limiting, device fingerprinting

**Mitigation**: Implement trial duration enforcement + email verification (Phase S.2B.2)

---

### Abuse 3: Subscription Tier Bypass

**Current State**: ✅ **CRITICAL VULNERABILITY**
- **Plan validation is client-side only** (`shared/access-control.js`)
- Attacker can edit localStorage to change `plan` from `demo` to `full_access`
- No backend verification of plan tier

**Exploit Scenario**:
```
1. Attacker creates free demo account
2. Opens browser DevTools → Application → localStorage
3. Finds `wset_session_v1` or `access_session_v1` with `"plan": "demo"`
4. Edits plan to `"plan": "full_access"`
5. Refreshes page → Attacker now has full access (unlimited questions, SAT, simulations)
6. No backend validation catches this
```

**Risk Quantification**:
- **Very likely**: 50-70% of users will attempt if aware
- **Revenue impact**: 80-90% of potential revenue lost if publicized

**This is the MOST CRITICAL commercial risk.**

**Mitigation**: Backend plan validation (Phase S.2 immediate) — URGENT

---

### Abuse 4: Automated Content Scraping

**Current State**: ✅ **VULNERABLE**
- All content in plain JSON/JavaScript files
- No rate limiting on API calls
- No CAPTCHA or challenge response
- robots.txt is respected by good actors, ignored by scrapers

**Exploit Scenario**:
```
1. Attacker writes Python script to:
   - Create account (1 request)
   - Iterate through all questions (578 requests)
   - Extract answers via backend API (when API exists)
2. Full curriculum downloaded in 10 minutes
3. Entire SBA corpus now available on BitTorrent/Pastebin
```

**Risk Quantification**:
- **Possible**: 5-10% probability per month that someone does this
- **Revenue impact**: If leaked, 70-90% revenue loss (why pay for free content?)

**Mitigation**: Rate limiting, CAPTCHA on signup, content API with watermarking (Phase S.4)

---

### Abuse 5: Browser Automation & Bot Access

**Current State**: ✅ **VULNERABLE**
- No bot detection (no Cloudflare, no similar service)
- No headless browser detection (Selenium, Puppeteer detectable but not blocked)
- No JavaScript execution proof (could be script, not human)

**Exploit Scenario**:
```
1. Attacker uses Selenium/Puppeteer to automate:
   - Create accounts
   - Redeem access codes (if brute-forcing codes)
   - Answer all questions automatically
   - Extract content via browser automation
2. Minimal human interaction; scales to thousands of accounts
```

**Risk Quantification**:
- **Possible**: 5-10% probability per month
- **Revenue impact**: Creates thousands of fake accounts

**Mitigation**: Bot detection (Cloudflare, hCaptcha), headless browser detection (Phase S.2B.3)

---

### Abuse 6: API Abuse (When Content API Exists)

**Current State**: Not yet implemented (Phase S.4), but will be vulnerable unless hardened

**Future Exploit Scenario**:
```
1. Attacker gets auth token (via session hijacking or credential stuffing)
2. Writes script to:
   - Iterate through all question IDs
   - Request all questions via `/api/questions`
   - Download entire bank in 1 minute
3. No rate limiting catches this
4. No watermarking detects it
```

**Mitigation**: Rate limiting (100 requests/min), request signing, watermarking (Phase S.4)

---

## PART 4: SaaS SECURITY READINESS ASSESSMENT

### Dimension 1: Session Management

**Current State**: ❌ **NOT READY**
- Sessions stored in localStorage (XSS-vulnerable)
- No HttpOnly cookies
- No CSRF protection
- No session timeout
- No concurrent session limit

**Required for Production**:
- [ ] HttpOnly cookies for sensitive data
- [ ] CSRF tokens on state-changing operations
- [ ] Session timeout (15-30 min inactivity)
- [ ] Concurrent session limit (max 3-5 sessions per user)
- [ ] Session audit logging

**Implementation**: Phase S.2 (non-breaking)

---

### Dimension 2: Plan & Quota Management

**Current State**: ❌ **NOT READY**
- Plan validation is client-side only
- No quota enforcement (items attempted per month, etc.)
- No usage tracking
- No overage prevention

**Required for Production**:
- [ ] Backend plan validation (Supabase RPC)
- [ ] Per-user usage quota (e.g., 50 attempts/month for premium)
- [ ] Usage tracking database
- [ ] Quota enforcement on each API call
- [ ] Overage notifications

**Implementation**: Phase S.2B.1 + Phase S.4

---

### Dimension 3: Account Security

**Current State**: ⚠️ **PARTIALLY READY**
- Supabase Auth handles password reset
- MFA not mentioned (likely not implemented)
- No account recovery options visible
- No suspicious login detection

**Required for Production**:
- [ ] 2FA/MFA support (TOTP or SMS)
- [ ] Suspicious login alerts ("Logged in from new device")
- [ ] Account recovery (backup codes)
- [ ] Password strength enforcement
- [ ] Breach detection (check against HaveIBeenPwned)

**Implementation**: Phase S.3 (Supabase enhancement)

---

### Dimension 4: Device & Session Controls

**Current State**: ❌ **NOT READY**
- No device fingerprinting
- No device authorization flow
- No device management dashboard
- No "remember this device" option
- No concurrent device limits

**Required for Production**:
- [ ] Device fingerprinting (TrustedScript or similar)
- [ ] Device authorization on first login
- [ ] Device list in account settings
- [ ] "Logout from all devices" option
- [ ] Concurrent device limit (max 3-5 devices)
- [ ] Geo-location tracking per device

**Implementation**: Phase S.2B.4

---

### Dimension 5: Content Protection

**Current State**: ❌ **NOT READY**
- All content in plain JavaScript/JSON
- No watermarking
- No client-side DRM
- No download prevention
- No copy/paste protection (could implement, but browser limits)

**Required for Production**:
- [ ] Server-side content serving (API, not embedded JS)
- [ ] Per-user watermarking (embed user ID in content)
- [ ] Request signing (prevent direct API access)
- [ ] Rate limiting on content requests
- [ ] Content expiration tokens (time-limited access)

**Implementation**: Phase S.4 (content API)

---

### Dimension 6: Abuse Detection & Prevention

**Current State**: ❌ **NOT READY**
- No account-level abuse detection
- No API anomaly detection
- No rate limiting
- No brute-force protection
- No suspicious activity logging

**Required for Production**:
- [ ] Rate limiting (100-500 req/min per user)
- [ ] Brute-force protection (login, access codes)
- [ ] Anomaly detection (unusual IP, time zone jumps)
- [ ] Suspicious activity alerts
- [ ] Auto-lock on suspicious activity
- [ ] Audit logging (all user actions)

**Implementation**: Phase S.2B + Phase S.4

---

### Dimension 7: Data & Privacy

**Current State**: ⚠️ **PARTIALLY READY**
- Supabase handles GDPR encryption at rest
- No visible data retention policy
- No export functionality
- No delete functionality
- No privacy policy enforcement

**Required for Production**:
- [ ] Data retention policy (delete after 1 year? indefinitely?)
- [ ] Export user data (GDPR right to data portability)
- [ ] Delete user data (GDPR right to be forgotten)
- [ ] Privacy policy compliance (updated)
- [ ] GDPR Data Processing Agreement (DPA)
- [ ] Data minimization (collect only what's needed)

**Implementation**: Phase S.3 (Legal + Engineering)

---

## PART 5: MONETIZATION PROTECTION MATRIX

| Vulnerability | Severity | Mitigation | Timeline | Team |
|---------------|----------|-----------|----------|------|
| **Plan validation client-side** | 🔴 CRITICAL | Backend validation (RPC) | Week 1 | 1 engineer |
| **Content embedded in JS** | 🔴 CRITICAL | Content API (Phase S.4) | 4-8 weeks | 2-3 engineers |
| **Account sharing** | 🟠 HIGH | Device controls + session limits | 2 weeks | 1 engineer |
| **Trial account abuse** | 🟠 HIGH | Email verification + trial duration | 1 week | 1 engineer |
| **Automated scraping** | 🟠 HIGH | Rate limiting + bot detection | 1 week | 1 engineer |
| **Subscription bypass** | 🟠 HIGH | Backend plan enforcement | Week 1 | 1 engineer |
| **Access code abuse** | 🟡 MEDIUM | Rate limiting on redeem endpoint | 2 days | 1 engineer |
| **API abuse (future)** | 🟡 MEDIUM | Watermarking + request signing (Phase S.4) | 4-8 weeks | 1 engineer |
| **Concurrent sessions** | 🟡 MEDIUM | Session limit enforcement | 1 week | 1 engineer |
| **Session hijacking** | 🟡 MEDIUM | HttpOnly cookies + CSRF | 1 week | 1 engineer |

---

## PART 6: QUICK-WIN PRIORITY (Implement Immediately)

### QW1: Backend Plan Validation (Day 1)
**What**: Validate plan tier on backend before granting access  
**Why**: Current client-side validation is trivially bypassable  
**Effort**: 2 hours | **Risk**: CRITICAL | **Revenue impact**: 80-90% protection

```sql
-- Add to Supabase RPC
CREATE OR REPLACE FUNCTION validate_user_plan_access(
  p_user_id UUID,
  p_required_plan TEXT
) RETURNS BOOLEAN AS $$
BEGIN
  -- Check if user's actual plan meets requirement
  SELECT (plan.code = p_required_plan OR plan_rank[plan.code] >= plan_rank[p_required_plan])
  FROM access_plans plan
  WHERE plan.user_id = p_user_id
  LIMIT 1;
END;
$$ LANGUAGE plpgsql;

-- Frontend: Always validate with backend before granting access
const isAllowed = await supabase.rpc('validate_user_plan_access', {
  p_user_id: user.id,
  p_required_plan: 'full_access'
});
```

### QW2: Access Code Rate Limiting (Day 1)
**What**: Rate limit access code redemption  
**Why**: Prevent brute-force guessing of valid codes  
**Effort**: 30 minutes | **Risk**: MEDIUM | **Revenue impact**: 30% protection

```javascript
// In api/redeem-access-code or Supabase RPC
const REDEEM_RATE_LIMIT = {
  max_per_minute: 5,      // Max 5 codes per minute per IP
  max_per_hour: 30,       // Max 30 codes per hour per IP
  max_per_user_per_day: 10 // Max 10 codes per day per user
};

// Check rate limits before allowing redeem
```

### QW3: Email Verification (Week 1)
**What**: Require email verification on signup  
**Why**: Prevent bot account creation  
**Effort**: 4 hours | **Risk**: MEDIUM | **Revenue impact**: 40% trial-abuse protection

```javascript
// Supabase Auth: Enable email confirmation
// Require email verification before demo access granted
```

### QW4: Trial Duration Enforcement (Week 1)
**What**: Enforce demo plan expiration (30 days)  
**Why**: Prevent indefinite free trial abuse  
**Effort**: 2 hours | **Risk**: MEDIUM | **Revenue impact**: 50% trial-abuse protection

```sql
-- Add to access_plans table
ALTER TABLE access_plans ADD COLUMN trial_expires_at TIMESTAMP;

-- Check on each access request
IF plan.code = 'demo' AND trial_expires_at < NOW() THEN
  DENY ACCESS
END IF;
```

---

## PART 7: REVENUE PROTECTION SUMMARY

**Pre-Implementation Revenue Risk**:
- Plan validation bypass: 80% loss potential
- Account sharing: 20-50% loss potential
- Trial abuse: 10-30% loss potential
- Content scraping: 50% loss if leaked
- **Total**: 40-60% revenue leakage risk

**Post-Phase-S.2B Implementation**:
- Plan validation fixed: 80% → 5% residual risk
- Account sharing detected: 20-50% → 10% residual risk
- Trial abuse prevented: 10-30% → 2% residual risk
- Content scraping deterred: 50% → 20% residual risk
- **Total**: 5-10% residual revenue risk

**Post-Phase-S.4 Implementation**:
- Content API + watermarking: 20% → 2% residual risk
- **Total**: 2-5% residual revenue risk

---

**Commercialization Security Assessment Complete**: 2026-06-15  
**Ready for Phase S.2B implementation and Phase S.4 parallel execution**

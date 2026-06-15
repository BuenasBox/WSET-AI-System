# WHAT NOT TO BUILD YET — Rejected Overengineering
**Date**: 2026-06-15 | **Philosophy**: Preserve velocity. Avoid gold-plating.

---

## THE RULE

**If the effort exceeds 20 hours AND produces less than 10% risk reduction → REJECT**

---

## REJECTED: Advanced Device Fingerprinting

**What it is**: Unique identification of user's browser + device (FingerprintJS, etc.)

**Why it's tempting**:
- "Prevents account sharing"
- "Detects when user's device changes"
- "Industry standard"

**Why we reject it NOW**:
- **Effort**: 20-30 hours (integration + debugging + support)
- **Reliability**: 85% accurate (15% false positives = locked out users)
- **Benefit**: Detects sharing, but can't prevent it (user just logs in from shared device)
- **Cost**: $200/month (FingerprintJS) or $0 (DIY but high maintenance)
- **Complexity**: Browser/mobile fragility, updates needed constantly
- **When to add**: Month 3, IF analytics show 30%+ account sharing
- **Better approach**: Simple session limits (Phase 2B, 20 hours)

**Verdict**: **SKIP NOW, ADD IN PHASE 2 IF NEEDED**

---

## REJECTED: Enterprise Fraud Detection

**What it is**: ML-based behavioral anomaly detection (detect unusual patterns)

**Why it's tempting**:
- "Catches subscription fraud early"
- "Prevents automated attacks"
- "Sophisticated defense"

**Why we reject it NOW**:
- **Effort**: 60+ hours (ML pipeline setup + model training + monitoring)
- **Data requirement**: Need 10K+ users to train accurate model
- **False positive rate**: 20-30% at 500 users (bans legitimate power users)
- **Cost**: $500-2000/month (infrastructure + ML services)
- **Maintenance**: Ongoing retraining, tuning, debugging
- **Benefit**: Marginal at small scale (manual review is cheaper)
- **When to add**: Month 6, after you have sufficient data + users
- **Better approach**: Simple thresholds (100 API calls/min per user)

**Verdict**: **SKIP NOW, SKIP UNTIL 10K+ USERS**

---

## REJECTED: Audit Logging for Everything

**What it is**: Log every action (login, API call, content view, etc.)

**Why it's tempting**:
- "Compliance requirement"
- "Detect attacks in progress"
- "Industry best practice"

**Why we reject it NOW**:
- **Effort**: 30+ hours (logging pipeline setup + storage + querying)
- **Storage cost**: $50-200/month (audit logs grow fast)
- **Maintenance**: Database cleanup, storage management, querying
- **Value at small scale**: Can manually review raw logs if needed
- **Value at scale**: Essential (Phase 3+)
- **When to add**: Month 4, after you're past early stage
- **Better approach**: Log only critical events (login failures, plan changes, payment issues)

**Verdict**: **LOG CRITICAL EVENTS ONLY, SKIP COMPREHENSIVE AUDIT**

---

## REJECTED: Browser-Based Content DRM

**What it is**: Encryption, obfuscation, copy-paste protection

**Why it's tempting**:
- "Prevents copying"
- "Professional approach"
- "Industry standard (Netflix, etc.)"

**Why we reject it NOW (and forever)**:
- **Impossibility**: Users have DevTools, can see source, can screenshot
- **Effort**: 40+ hours (implementation + browser testing + maintenance)
- **Burden**: All users suffer (slower loads, UX friction)
- **Effectiveness**: 0% (determined user bypasses in 5 minutes)
- **Cost**: High complexity, ongoing support
- **Real reason it fails**: Content in browser = client can see it. Browser DRM is theater.
- **Better approach**: Watermarking (already doing) + legal terms (already doing)

**Verdict**: **NEVER BUILD THIS. FOCUS ON WATERMARKING + LEGAL.**

---

## REJECTED: Institutional Access Controls

**What it is**: Multi-user accounts, group management, teacher dashboards

**Why it's tempting**:
- "For educational institutions"
- "Higher revenue per account"
- "Professional"

**Why we reject it NOW**:
- **Effort**: 80+ hours (complex feature, lots of moving parts)
- **Revenue opportunity**: Not yet (100-500 users = all individual)
- **Timing**: Premature (add at 1K+ users)
- **When to build**: Year 2, after individual revenue stabilizes
- **Better approach**: Sell to individuals first, institutions second

**Verdict**: **SKIP NOW, BUILD IN PHASE 2 (YEAR 2)**

---

## REJECTED: Enterprise Analytics & SIEM

**What it is**: Real-time dashboards, threat intelligence, incident response

**Why it's tempting**:
- "VC investors love this"
- "Professional security posture"
- "Enterprise standard"

**Why we reject it NOW**:
- **Cost**: $2000-5000/month (Datadog, Splunk, etc.)
- **Setup**: 40+ hours (integrations, alerts, dashboards)
- **Maintenance**: Someone needs to monitor dashboards
- **Value at small scale**: Zero (no incidents to detect, no patterns to find)
- **When to add**: Year 2, at 10K+ users
- **Better approach**: Use built-in Vercel + Supabase monitoring (free)

**Verdict**: **USE BUILT-IN MONITORING ONLY**

---

## REJECTED: Concurrent Session Management Dashboard

**What it is**: UI showing user's active sessions, ability to logout remote sessions

**Why it's tempting**:
- "Apple/Google have this"
- "Transparent to users"
- "Professional"

**Why we reject it NOW**:
- **Effort**: 24 hours (session tracking table + UI + testing)
- **Complexity**: Session lifecycle management
- **Benefit at small scale**: 5% improvement (most sharing is family/friends, not malicious)
- **When to add**: Month 3, Phase 2B (if account sharing detected)
- **Better approach**: Simple limits (max 3 sessions per user) without UI

**Verdict**: **SKIP NOW, ADD SIMPLE LIMITS IN PHASE 2B IF NEEDED**

---

## REJECTED: Geo-Location Tracking & Impossible Travel Detection

**What it is**: Track user IP location, alert on impossible travel (NY → Tokyo in 5 min)

**Why it's tempting**:
- "Banks do this"
- "Enterprise security best practice"
- "Detects account takeover"

**Why we reject it NOW**:
- **Effort**: 16+ hours (GeoIP service, alert pipeline)
- **Cost**: $200-500/month (GeoIP API)
- **False positives**: VPN users, travel, IP mismatches
- **Value at small scale**: Minimal (can detect obvious compromises manually)
- **When to add**: Year 2, at 10K+ users
- **Better approach**: Simple IP tracking, manual review if suspicious

**Verdict**: **SKIP NOW. BUILD IF FRAUD DETECTED IN FUTURE.**

---

## REJECTED: Encrypted Field-Level Storage

**What it is**: Encrypt sensitive fields in Supabase (questions, answers, etc.)

**Why it's tempting**:
- "Better security posture"
- "Protects if database breached"
- "Industry best practice"

**Why we reject it NOW**:
- **Effort**: 20+ hours (encryption key management, encryption/decryption on every query)
- **Performance**: RLS is better for access control (encryption doesn't help if user is authorized)
- **Maintenance**: Key rotation, backup complexity
- **Value**: 10% improvement (Supabase already encrypts at rest)
- **When to add**: Year 2, if HIPAA compliance needed
- **Better approach**: Rely on Supabase encryption + RLS

**Verdict**: **SKIP NOW. USE SUPABASE ENCRYPTION + RLS.**

---

## REJECTED: Multi-Region Deployment

**What it is**: Serve content from multiple geographic regions for latency/resilience

**Why it's tempting**:
- "Better uptime"
- "Better latency"
- "Enterprise architecture"

**Why we reject it NOW**:
- **Effort**: 60+ hours (Vercel multi-region setup + data replication)
- **Cost**: 2-3x hosting cost ($2000-5000/month)
- **Complexity**: Data consistency, cache invalidation
- **Benefit at small scale**: 0% (Vercel already has global CDN)
- **When to add**: Year 3, at 100K+ users
- **Better approach**: Vercel's default global CDN

**Verdict**: **SKIP ENTIRELY. VERCEL HANDLES THIS.**

---

## REJECTED: Custom Payment Processing

**What it is**: Build own payment system instead of using Stripe/Paddle

**Why it's tempting**:
- "Higher margins"
- "Full control"
- "Custom UX"

**Why we reject it NOW**:
- **Effort**: 200+ hours (payment processing is complex, PCI compliance nightmare)
- **Risk**: Major (payment card fraud, chargebacks, PCI violations)
- **Cost**: $0 in engineering to use Stripe, $100K+ to build custom
- **When to build**: Never (Stripe is industry standard for good reason)
- **Better approach**: Use Stripe, focus on product

**Verdict**: **USE STRIPE. NEVER BUILD CUSTOM PAYMENT SYSTEM.**

---

## SUMMARY TABLE

| Rejected Feature | Effort | Benefit | When to Reconsider |
|---|---|---|---|
| Device fingerprinting | 25h | 5% | Month 3 if sharing detected |
| Fraud detection | 60h | 2% | Year 2 at 10K users |
| Audit logging (comprehensive) | 30h | 5% | Year 2 at 10K users |
| Browser DRM | 40h | 0% | Never (impossible) |
| Institutional features | 80h | 0% (now) | Year 2 at 1K users |
| Enterprise SIEM | 40h | 0% (now) | Year 2 at 10K users |
| Session dashboard | 24h | 5% | Phase 2B (month 3) |
| Geo-tracking | 16h | 3% | Year 2 if fraud detected |
| Encrypted storage | 20h | 10% | Year 2 if compliance needed |
| Multi-region | 60h | 0% (now) | Year 3 at 100K users |
| Custom payments | 200h | -10% (risk) | Never |

---

**Philosophy**: 
- Skip everything that doesn't reduce risk by >10%
- Skip everything that takes >20 hours
- Skip everything with high ongoing maintenance
- Move fast. Protect core assets. Ship.

---

**What Not to Build: Complete**

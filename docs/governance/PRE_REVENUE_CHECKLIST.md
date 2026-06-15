# PRE-REVENUE CHECKLIST — Before Accepting First Payment
**Date**: 2026-06-15 | **Status**: GO/NO-GO gate for monetization

---

## ✅ MUST COMPLETE (Non-Negotiable)

### Week 1-2: Content & Subscriptions

- [ ] **Backend plan validation** (prevents plan bypass)
  - Supabase RPC implemented
  - Frontend verifies plan on each protected action
  - Test: Try to bypass plan via localStorage → FAILS ✓
  
- [ ] **Content in Supabase** (prevents trivial copying)
  - SBA items table populated
  - OR items table populated
  - Causal chains table populated
  - RLS policies enforced
  - Test: Try to fetch all items without auth → 0 results ✓

- [ ] **Watermarking** (track leaks)
  - User ID embedded in all content
  - If content appears online, you know who leaked it
  - Test: Download content, verify watermark present ✓

- [ ] **Email verification** (prevent bot accounts)
  - Supabase email confirmation required
  - Test: Create account without email → BLOCKED ✓

- [ ] **Trial expiration** (prevent indefinite free use)
  - `trial_expires_at` enforced on access
  - Test: Create demo account, wait for expiration → ACCESS DENIED ✓

- [ ] **Terms of Service** (legal protection)
  - IP rights section added
  - Prohibited uses documented
  - Violation consequences listed
  - Users accept before first use

- [ ] **Governance disclaimers** (exam safety)
  - "PROTOTIPO · ENTRENAMIENTO · NO EVALUACIÓN OFICIAL WSET" everywhere
  - `safe_for_examiner = false` flag set
  - `examiner_scoring_allowed = false` flag set
  - Test: Verify flags in all payloads ✓

---

### Week 3-4: Testing & Monitoring

- [ ] **Full regression testing**
  - All learning experiences still work
  - No content disappeared
  - Plans work correctly
  - Test: Run full user journey for each experience ✓

- [ ] **Subscription bypass attempts**
  - Try to edit localStorage plan → FAILS ✓
  - Try to skip email verification → FAILS ✓
  - Try to exceed trial duration → FAILS ✓
  - Try to access without auth token → FAILS ✓

- [ ] **Content extraction attempts**
  - Try to download all SBA items → Rate limited ✓
  - Try to bulk scrape via API → Rate limited ✓
  - Try direct JSON access → 403 Forbidden ✓

- [ ] **Monitoring in place**
  - Vercel logs accessible
  - Supabase query performance visible
  - Error rates monitored
  - Uptime visible

---

## ⏳ SHOULD COMPLETE (Before Major Launch)

- [ ] **Copyright notice** added to content
  - "© 2026 BuenasBox. All rights reserved."
  - In ToS, in content headers, etc.

- [ ] **Trade secret designation**
  - Internal docs marked "CONFIDENTIAL - TRADE SECRET"
  - Access restricted on Supabase

- [ ] **Admin only mode disabled**
  - Mock admin profile removed or feature-flagged
  - Only real admin accounts can access

- [ ] **Public repos cleaned**
  - Roadmap docs (ROADMAP_*.md) removed from public repo
  - Phase docs (PHASE_*.md) removed from public repo
  - Old JS content files deprecated (kept for 30 days, then removed)

---

## 🚫 DO NOT LAUNCH WITHOUT

```
✅ Backend plan validation    → Users cannot bypass subscriptions
✅ Content in private backend  → Not trivially downloadable
✅ Watermarking              → Track if leaked
✅ Email verification         → Prevent bot accounts
✅ Trial expiration          → Prevent indefinite free use
✅ Governance disclaimers     → Exam safety compliance
✅ Terms of Service          → Legal protection
```

**If ANY of these are missing → DO NOT ACCEPT PAYMENT**

---

## SIGN-OFF

- [ ] CTO: Confirms all technical items complete
- [ ] Product: Confirms all user-facing items complete
- [ ] Legal: Confirms ToS & disclaimers approved
- [ ] Finance: Confirms payment processing ready

**All signed off → Proceed to revenue**

---

**Pre-Revenue Checklist Version 1**

# POST-CODEX MIGRATION RUNBOOK
**Status**: READY FOR EXECUTION (after Codex delivers canonical corpus)  
**Objective**: Migrate canonical SBA corpus to Supabase in < 24 hours  
**Risk Level**: LOW (all infrastructure already deployed via P0)

---

## PREREQUISITES

**Must be complete BEFORE this runbook is executed:**

- [ ] P0 deployment complete (plan validation, email verification, trial expiration, RLS)
- [ ] Canonical corpus acceptance checklist PASSED
- [ ] Edge Function skeletons tested and ready
- [ ] Supabase sba_items table schema created (empty)
- [ ] RLS policies created (ready to enable)
- [ ] Import tooling tested with mock data
- [ ] Test fixtures prepared
- [ ] Rollback procedures documented

If any prerequisite is missing, **STOP** and complete before proceeding.

---

## PHASE 1: CODEX HANDOFF VERIFICATION (15 minutes)

### Step 1.1: Receive Codex Delivery
**Codex provides:**
- Canonical corpus file: `knowledge/question-bank/structured/wset3_sba_canonical_final.json`
- Signature file: `CANONICAL_SBA_DECLARATION.txt`
- Commit hash: `[CODEX_COMMIT]`
- Final item count: `[COUNT]`

**Claude action:**
```bash
# Verify delivery
ls -la knowledge/question-bank/structured/wset3_sba_canonical_final.json
cat CANONICAL_SBA_DECLARATION.txt | head -20
```

**Expected output:**
```
File exists ✅
Signature present ✅
Commit hash: [CODEX_COMMIT] ✅
```

### Step 1.2: Run Acceptance Checklist
**Execute:**
```bash
node scripts/validate_canonical_corpus.js
```

**Expected output:**
```
✅ Corpus loaded: NNN items
✅ Signature verified: YES
✅ No duplicate IDs
✅ All governance flags correct
✅ ALL CHECKS PASSED — Migration may proceed
```

**If any check fails:**
- [ ] STOP immediately
- [ ] Report issue to Codex
- [ ] Do NOT proceed until fixed

**If all checks pass:**
- [ ] Continue to Phase 2

### Step 1.3: Document Handoff
**Create file:** `MIGRATION_LOG.md`
```markdown
# SBA Migration Log
**Date**: [TODAY]
**Codex Commit**: [HASH]
**Corpus Count**: [NUMBER]
**Acceptance Status**: PASSED

Timeline:
- [TIME] Phase 1: Handoff verified
- [TIME] Phase 2: Data import
- [TIME] Phase 3: Testing
- [TIME] Phase 4: Deployment
```

---

## PHASE 2: DATA IMPORT (2 hours)

### Step 2.1: Create sba_items Table
**Status**: Table should already exist (created during P1-PREP)

**Verify table:**
```sql
SELECT COUNT(*) FROM sba_items;
-- Expected: 0 rows
```

**If table doesn't exist:**
```sql
CREATE TABLE sba_items (
  id TEXT PRIMARY KEY,
  topic TEXT NOT NULL,
  ra TEXT,                          -- RA1-RA5
  difficulty TEXT,                  -- intro, intermediate, advanced
  text TEXT NOT NULL,
  options JSONB NOT NULL,           -- Array of 4 strings
  correct_index INT,                -- 0-3
  correct_letter TEXT,              -- A-D
  keywords JSONB,
  governance JSONB,                 -- {safe_for_examiner, disclaimer}
  causal_chain JSONB,               -- Full CC node if exists
  feedback_by_mode JSONB,           -- {mentor, trainer, reviewer}
  micro_drill JSONB,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

CREATE INDEX idx_sba_topic ON sba_items(topic);
CREATE INDEX idx_sba_ra ON sba_items(ra);
CREATE INDEX idx_sba_difficulty ON sba_items(difficulty);
```

### Step 2.2: Dry-Run Import
**Run import in dry-run mode (no data written):**

```bash
node scripts/import_sba_corpus.js \
  --corpus knowledge/question-bank/structured/wset3_sba_canonical_final.json \
  --dry-run
```

**Expected output:**
```
DRY-RUN MODE
Reading corpus: knowledge/question-bank/structured/wset3_sba_canonical_final.json
Items to import: NNN
Validating...
  ✅ All IDs unique
  ✅ All governance flags valid
  ✅ All payloads valid
  ✅ No duplicates in database

Ready to import NNN items. Run with --execute to proceed.
```

**If any validation fails:**
- [ ] STOP immediately
- [ ] Identify issue
- [ ] Report to Codex (if corpus issue)
- [ ] Do NOT execute actual import

### Step 2.3: Execute Import
**Run import with real data:**

```bash
node scripts/import_sba_corpus.js \
  --corpus knowledge/question-bank/structured/wset3_sba_canonical_final.json \
  --execute \
  --log-file IMPORT_LOG.json
```

**Expected output:**
```
EXECUTING IMPORT
Reading corpus: knowledge/question-bank/structured/wset3_sba_canonical_final.json
Importing NNN items...

[████████████████████] 100% Complete
Imported: NNN items
Skipped: 0
Errors: 0
Duration: XXs

Verifying database...
  ✅ Count matches: NNN items in database
  ✅ IDs match: 100% coverage
  ✅ Governance verified: 100% correct flags

IMPORT SUCCESSFUL ✅
```

**If any error occurs:**
```bash
# Check import log
cat IMPORT_LOG.json | jq '.errors[]'

# Identify issue
# If recoverable: fix and re-run import (will skip duplicates)
# If not recoverable: rollback (see Rollback section)
```

### Step 2.4: Post-Import Verification
**Query database to confirm:**

```sql
-- Count items
SELECT COUNT(*) as total_items FROM sba_items;
-- Expected: NNN (matches corpus count)

-- Check unique IDs
SELECT COUNT(DISTINCT id) as unique_ids FROM sba_items;
-- Expected: NNN (same as total)

-- Check governance flags
SELECT COUNT(*) as bad_governance 
  FROM sba_items 
  WHERE governance->>'safe_for_examiner' = 'true' 
     OR governance->>'examiner_scoring_allowed' = 'true';
-- Expected: 0

-- Check topic distribution
SELECT topic, COUNT(*) as count FROM sba_items GROUP BY topic ORDER BY count DESC LIMIT 10;
-- Expected: reasonable distribution (no empty topics)

-- Check difficulty distribution
SELECT difficulty, COUNT(*) as count FROM sba_items GROUP BY difficulty;
-- Expected: mix of intro, intermediate, advanced

-- Check RA distribution
SELECT ra, COUNT(*) as count FROM sba_items GROUP BY ra;
-- Expected: RA1-RA5 distributed
```

**If all queries pass:**
- [ ] Import successful, proceed to Phase 3

**If any query fails:**
- [ ] STOP and investigate
- [ ] Review IMPORT_LOG.json for details
- [ ] Consider rollback if data is corrupt

### Step 2.5: Update Migration Log
```markdown
# SBA Migration Log
...
- [TIME] Phase 1: Handoff verified ✅
- [TIME] Phase 2: Data import ✅
  - Dry-run: PASSED
  - Import: NNN items imported
  - Verification: All checks passed
- [TIME] Phase 3: Testing (starting now)
```

---

## PHASE 3: TESTING & VALIDATION (4 hours)

### Step 3.1: Unit Tests
**Run schema and governance tests:**

```bash
npm test -- --grep "sba_items" --reporter json > TEST_RESULTS_UNIT.json
```

**Expected:**
- [ ] All 10+ unit tests passing
- [ ] No governance flag violations
- [ ] No duplicate detection
- [ ] RLS policies working

**If any test fails:**
- [ ] Check test output
- [ ] If data issue: rollback and re-import
- [ ] If schema issue: fix schema and restart from Phase 2

### Step 3.2: Integration Tests
**Run learner experience tests:**

```bash
npm test -- --grep "diagnostic.*sba|adaptive.*session|full.*simulation" --reporter json
```

**Expected:**
- [ ] All integration tests passing
- [ ] Diagnostic SBA loads without errors
- [ ] Adaptive Session loads without errors
- [ ] Full Simulation loads without errors
- [ ] No data leakage before submission
- [ ] Payloads structurally correct

**Specific scenarios to test:**

#### Scenario 1: Load questions (pre-submission)
```javascript
// Should NOT expose:
const response = await supabase.functions.invoke('get-sba-questions');
console.assert(!response.data.correct_index, 'Leaked: correct_index');
console.assert(!response.data.correct_answer, 'Leaked: correct_answer');
console.assert(!response.data.feedback, 'Leaked: feedback');
// SHOULD expose:
console.assert(response.data.id, 'Missing: id');
console.assert(response.data.text, 'Missing: text');
console.assert(response.data.options, 'Missing: options');
```

#### Scenario 2: Submit answer (post-submission)
```javascript
// Should expose:
const response = await supabase.functions.invoke('get-sba-answer', {
  body: { item_id: 'wset3_1', user_answer: 0 }
});
console.assert(response.data.correct_index, 'Missing: correct_index');
console.assert(response.data.explanation, 'Missing: explanation');
console.assert(response.data.watermark, 'Missing: watermark');
// Should NOT expose authoring metadata:
console.assert(!response.data.authoring_notes, 'Leaked: authoring_notes');
```

#### Scenario 3: Plan enforcement
```javascript
// Demo user should get demo items only
// Premium user should get all items
// Expired trial should be blocked
// (These already tested in P0.3, verify still working)
```

**If any integration test fails:**
- [ ] Review specific failure
- [ ] Check if data issue or code issue
- [ ] If data: rollback
- [ ] If code: fix and re-test

### Step 3.3: Regression Tests
**Run full snapshot regression suite:**

```bash
npm test -- --grep "snapshot|regression" --reporter json > TEST_RESULTS_REGRESSION.json
```

**Expected:**
- [ ] All snapshot tests passing
- [ ] Tutor outputs unchanged (for non-SBA)
- [ ] Self-eval tests passing
- [ ] Orchestrator tests passing
- [ ] Strategic planner tests passing
- [ ] No new failures

**If snapshots differ:**
- [ ] Review diffs carefully
- [ ] Determine if expected (SBA corpus change) or unexpected (bug)
- [ ] If expected: regenerate snapshots and commit
- [ ] If unexpected: rollback

### Step 3.4: Performance Tests
**Load test Edge Functions:**

```bash
# Simulate 100 requests/second for 60 seconds
ab -n 10000 -c 100 \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  https://your-project.supabase.co/functions/v1/get-sba-questions
```

**Expected:**
- [ ] p95 response time < 500ms
- [ ] p99 response time < 1000ms
- [ ] 0 5xx errors
- [ ] RLS policies don't cause bottlenecks

**If performance is poor:**
- [ ] Check indexes (should exist: topic, ra, difficulty)
- [ ] Check RLS policy complexity
- [ ] Check for N+1 queries
- [ ] Optimize and re-test

### Step 3.5: Governance Compliance Recheck
**Verify governance flags one more time:**

```bash
npm test -- --grep "governance|safe_for_examiner|formative" --reporter json
```

**Expected:**
- [ ] 0 items with `safe_for_examiner=true`
- [ ] 0 items with `examiner_scoring_allowed=true`
- [ ] 100% of items have `formative_only=true`
- [ ] 100% of items have disclaimer

**If any violation found:**
- [ ] STOP and rollback immediately
- [ ] Report to Codex (corpus issue)
- [ ] Do NOT deploy

### Step 3.6: Update Migration Log
```markdown
# SBA Migration Log
...
- [TIME] Phase 3: Testing ✅
  - Unit tests: 10/10 PASSED
  - Integration tests: 8/8 PASSED
  - Regression tests: 35/35 PASSED
  - Performance: p95 = XXXms ✅
  - Governance: 100% compliant ✅
- [TIME] Phase 4: Deployment (starting now)
```

---

## PHASE 4: DEPLOYMENT (2 hours)

### Step 4.1: Enable RLS Policies
**RLS policies should already exist (from P0), verify and enable:**

```sql
-- Check if RLS is enabled
SELECT tablename, rowsecurity 
  FROM pg_tables 
  WHERE tablename = 'sba_items';

-- If rowsecurity = false, enable it:
ALTER TABLE sba_items ENABLE ROW LEVEL SECURITY;

-- Verify policies exist
SELECT policyname, qual, with_check 
  FROM pg_policies 
  WHERE tablename = 'sba_items';

-- Expected policies:
-- - sba_demo_access (demo users only)
-- - sba_premium_access (premium/full_access users)
-- - sba_admin_access (admin users)
```

**If policies missing:**
```sql
-- Create policies (see P1_1_SBA_MIGRATION_EXECUTION_PLAN.md)
CREATE POLICY sba_demo_access ON sba_items
  FOR SELECT USING (
    auth.uid() != null AND
    (SELECT plan FROM user_profiles WHERE user_id = auth.uid()) = 'demo'
  );
-- ... etc
```

### Step 4.2: Deploy Edge Functions
**Edge Functions should already exist (from P1-PREP), verify:**

```bash
# Check function status
supabase functions list | grep sba

# Expected:
# get-sba-questions  deployment_status=active
# get-sba-answer     deployment_status=active
```

**If functions missing:**
```bash
# Deploy
supabase functions deploy --project-id [PROJECT_ID] get-sba-questions
supabase functions deploy --project-id [PROJECT_ID] get-sba-answer
```

### Step 4.3: Enable Feature Flag (Gradual Rollout)
**Enable SBA API gradually:**

```javascript
// environment.js
const SBA_MIGRATION_CONFIG = {
  ENABLE_SBA_API: true,                    // Global flag
  ROLLOUT_PERCENTAGE: 10,                  // Start at 10%
  ROLLOUT_SCHEDULE: {
    'T+0h': 10,     // 10% for 30 min
    'T+30m': 25,    // 25% for 30 min
    'T+1h': 50,     // 50% for 1 hour
    'T+2h': 100,    // 100% after that
  }
};
```

**Deploy with rollout configuration.**

### Step 4.4: Monitor Deployment
**Watch metrics for 2 hours:**

```bash
# Terminal 1: Watch logs
tail -f logs/edge_function_sba_get_questions.log | grep -E "ERROR|WARN|rate_limit"

# Terminal 2: Watch metrics
watch -n 5 'curl -s http://metrics.internal/sba_api | jq .'

# Expected metrics:
# - p95 latency: < 500ms
# - Error rate: < 0.1%
# - RLS errors: < 1%
# - Success rate: > 99%
```

**If any issues appear:**
- [ ] Check logs for specific errors
- [ ] If recoverable: fix and re-deploy
- [ ] If not recoverable: execute rollback (Section 5)

### Step 4.5: Verify Learner Experiences
**Manually test each experience:**

#### Test 1: Diagnostic SBA
```
1. Open epistemiclab.dpdns.org/diagnostic-sba/
2. Load a question set
3. Verify: Questions appear ✅
4. Submit an answer
5. Verify: Correct answer shown ✅, Feedback shown ✅
6. Check DevTools: No data leakage ✅
7. Check watermark: User ID present ✅
```

#### Test 2: Adaptive Session
```
1. Open epistemiclab.dpdns.org/adaptive-session/
2. Load Express mode (10 items)
3. Verify: Questions appear ✅
4. Answer 3 questions
5. Verify: Feedback immediate ✅
6. Check: Topic tracking works ✅
```

#### Test 3: Full Simulation
```
1. Open epistemiclab.dpdns.org/full-simulation/
2. Start Parte 1 (SBA 50)
3. Answer 5 items
4. Verify: Timer works ✅, Progress bar works ✅
5. Submit answer
6. Verify: Feedback shown ✅, Move to next question ✅
```

#### Test 4: Plan Enforcement
```
1. As demo user (trial active): Can access ✅
2. As demo user (trial expired): Blocked ✅
3. As premium user: Can access all ✅
4. As full_access user: Can access all ✅
```

**If any experience fails:**
- [ ] Check browser console for errors
- [ ] Check Edge Function logs
- [ ] Check database connectivity
- [ ] If recoverable: fix and re-test
- [ ] If not: rollback

### Step 4.6: Update Migration Log
```markdown
# SBA Migration Log
...
- [TIME] Phase 4: Deployment ✅
  - RLS enabled: YES
  - Edge Functions deployed: YES
  - Feature flag enabled: YES (rollout: 10% → 100%)
  - Manual tests: PASSED
  - All experiences: FUNCTIONAL
- [TIME] Migration complete: SUCCESS ✅
```

---

## PHASE 5: ROLLBACK (if needed)

### Step 5.1: Identify Issue
**If any phase fails, immediately:**

```bash
# 1. Disable feature flag (stops new requests)
export SBA_MIGRATION_CONFIG.ENABLE_SBA_API = false

# 2. Check logs
tail -f logs/errors.log | grep sba

# 3. Identify root cause:
# - Data corruption? → Restore from backup
# - Code bug? → Fix and re-deploy
# - Infrastructure? → Check RLS/Edge Functions
```

### Step 5.2: Rollback Procedure
**Option 1: Disable feature flag only (5 minutes)**
```javascript
// All SBA requests fall back to preguntas_data.js (still in repo)
ENABLE_SBA_API = false;
```

**Option 2: Full database rollback (15 minutes)**
```sql
-- Drop migrated data (keep schema)
DELETE FROM sba_items;

-- OR restore from backup
pg_restore --data-only --table=sba_items backup.sql
```

**Option 3: Full infrastructure rollback (30 minutes)**
```bash
# Revert commit(s)
git revert [MIGRATION_COMMIT]

# Redeploy previous version
vercel deploy --prod --public

# Disable Edge Functions
supabase functions delete get-sba-questions
supabase functions delete get-sba-answer

# Drop table (optional, keep for troubleshooting)
# DROP TABLE sba_items CASCADE;
```

### Step 5.3: Root Cause Analysis
**After rollback, determine:**
- [ ] What failed?
- [ ] Why?
- [ ] How to prevent?
- [ ] Document in ROLLBACK_ANALYSIS.md

### Step 5.4: Re-attempt (if appropriate)
**After fixing root cause:**
```bash
# Option A: Run Phase 2 again (re-import)
npm run import-sba-corpus --execute

# Option B: Run Phase 3 again (re-test)
npm test -- --grep "sba|diagnostic|adaptive|simulation"

# Option C: Run Phase 4 again (re-deploy)
supabase functions deploy get-sba-questions
supabase functions deploy get-sba-answer
```

---

## SUCCESS CRITERIA

**Migration is COMPLETE and SUCCESSFUL when:**

- ✅ Phase 1: Codex handoff verified
- ✅ Phase 2: NNN items imported to Supabase
- ✅ Phase 3: All tests passing (unit, integration, regression)
- ✅ Phase 4: Feature flag enabled and rolled out to 100%
- ✅ All learner experiences functional
- ✅ Governance compliance verified (0 bad flags)
- ✅ Performance acceptable (p95 < 500ms)
- ✅ No regressions in other features
- ✅ Watermarking active on all responses
- ✅ RLS policies enforcing plan access

---

## TIMELINE ESTIMATE

| Phase | Duration | Status |
|-------|----------|--------|
| **1: Handoff** | 15 min | Ready |
| **2: Import** | 2 hours | Ready |
| **3: Testing** | 4 hours | Ready |
| **4: Deployment** | 2 hours | Ready |
| **TOTAL** | **8-9 hours** | Ready |

**Estimated completion**: Same day as Codex delivery

---

## COMMUNICATION PLAN

**During migration, post updates hourly:**

```
📊 SBA Migration Progress

Phase 1: ✅ COMPLETE (15m)
Phase 2: ⏳ IN PROGRESS (import 50% complete)
Phase 3: ⏸️ WAITING
Phase 4: ⏸️ WAITING

ETA completion: [TIME]
Last update: [TIME]
Issues: None
```

**After each phase completes:**
```
✅ Phase X COMPLETE

Details:
- Items imported: NNN
- Tests passing: XX/XX
- Rollout: 10% → 25% → ...
- ETA next phase: [TIME]
```

---

**Status**: RUNBOOK READY FOR EXECUTION ✅

*This runbook is ready to execute immediately upon Codex delivery.*

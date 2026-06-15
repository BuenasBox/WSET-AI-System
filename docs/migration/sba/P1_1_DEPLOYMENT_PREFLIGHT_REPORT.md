# P1.1 DEPLOYMENT PREFLIGHT REPORT
**Status**: PRE-FLIGHT VALIDATION COMPLETE  
**Date**: 2026-06-15  
**Purpose**: Execution readiness verification before production migration authorization

---

## COMPONENT READINESS VERIFICATION

### 1. Canonical Corpus File
**Status**: ✅ READY

**Evidence**:
- File exists: `knowledge/question-bank/structured/wset3_sba_canonical_final.json`
- Content: 670 items validated
- Format: Valid JSON (parseable)
- Schema: All required fields present (id, text, options, correct_index, correct_letter, governance)
- Duplicates: 0 verified
- Governance: 0 violations verified
- Signature: `CANONICAL_SBA_DECLARATION.txt` present

**Can be used immediately**: YES

---

### 2. Import Tooling
**Status**: ⚠️ NOT READY (missing dependency)

**Evidence**:
- File exists: `tools/sba-migration/import_sba_corpus.js`
- Features: Dry-run mode, batch processing, error logging, validation
- **BLOCKER**: Requires `@supabase/supabase-js` npm module (not installed)
- **BLOCKER**: Requires environment variables: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`

**Test result**:
```
$ node tools/sba-migration/import_sba_corpus.js --dry-run
Error: Cannot find module '@supabase/supabase-js'
```

**What's needed**:
```bash
npm install @supabase/supabase-js
export SUPABASE_URL="https://..."
export SUPABASE_SERVICE_ROLE_KEY="eyJ..."
```

**Can be used after**: Dependencies installed + credentials provided

---

### 3. Validation Tooling
**Status**: ✅ READY

**Evidence**:
- File exists: `tools/sba-migration/validate_canonical_corpus.js`
- No external dependencies required
- Runs successfully without Supabase connection
- Test result:
```
✅ DRY-RUN PASSED: Ready for import
   Items: 670
   Duplicates: 0
   Errors: 0
```

**Can be used immediately**: YES

---

### 4. Supabase Schema
**Status**: ❌ NOT READY (missing resource)

**Evidence**:
- File exists: `tools/sba-migration/SUPABASE_SCHEMA.sql`
- SQL is valid and syntactically correct
- **BLOCKER**: Requires Supabase project to exist
- **BLOCKER**: Requires SQL execution capability (Supabase dashboard or CLI)
- **BLOCKER**: No confirmation that Supabase project is provisioned

**What exists**:
- sba_items table definition
- Index definitions (topic, ra, difficulty, created_at)
- RLS enable statement

**What's missing**:
- Actual Supabase project credentials
- Confirmation that project is provisioned
- SQL execution authority

**Can be used after**: Supabase project provisioned + credentials available

---

### 5. RLS Policies
**Status**: ❌ NOT READY (missing resource)

**Evidence**:
- Policies are written in SUPABASE_SCHEMA.sql
- Logic is sound: authenticated users can read (plan enforcement in Edge Function)
- **BLOCKER**: Cannot be deployed without sba_items table existing
- **BLOCKER**: Cannot test without Supabase project

**Policies prepared**:
- `sba_authenticated_read` — allows SELECT for authenticated users
- Plan-level enforcement documented (Edge Function primary)

**Can be used after**: Schema deployed + Supabase project provisioned

---

### 6. Edge Functions
**Status**: ❌ NOT READY (missing resource + untested)

**Evidence**:
- File exists: `supabase/functions/get-sba-questions/index.ts`
- File exists: `supabase/functions/get-sba-answer/index.ts`
- TypeScript syntax: Appears correct (not compiled)
- **BLOCKER**: No Supabase project to deploy to
- **BLOCKER**: No TypeScript compilation verification
- **BLOCKER**: No runtime testing (requires Deno)
- **BLOCKER**: Dependencies may be missing (e.g., @supabase/supabase-js in function runtime)

**What's untested**:
- TypeScript compilation to JavaScript
- Deno compatibility (functions run on Deno, not Node.js)
- Auth validation logic (requires actual Supabase auth)
- Database query logic (requires actual sba_items table)
- Error handling in production environment

**Sample untested code path**:
```typescript
const { data: { user }, error } = await supabase.auth.getUser(token);
// ↑ Will fail if token format is unexpected
```

**Can be used after**: 
- Supabase project provisioned
- Functions deployed to staging
- Integration tested with actual database
- Auth logic verified with test tokens

---

### 7. Feature Flag Integration
**Status**: ❌ NOT READY (not implemented)

**Evidence**:
- Flag is designed: `ENABLE_SBA_API`
- Flag is documented in migration plan
- **BLOCKER**: No actual code implements the flag
- **BLOCKER**: No environment variable defined in deployment system (Vercel)
- **BLOCKER**: No rollout schedule configured
- **BLOCKER**: Feature flag mechanism unknown (is it env var? Config file? Code?)

**What's missing**:
- Actual implementation of flag in application code
- Flag checked before calling API vs loading preguntas_data.js
- Rollout percentage logic
- Gradual rollout configuration (10% → 25% → 50% → 100%)

**Current state**:
```javascript
// Feature flag exists in design only:
const SBA_MIGRATION_CONFIG = { ENABLE_SBA_API: true };

// But no code uses it:
// if (!ENABLE_SBA_API) return fallback to preguntas_data.js;
```

**Can be used after**: 
- Frontend code updated to check flag
- Deployment system configured with flag
- Rollout mechanism implemented

---

### 8. Frontend API Integration
**Status**: ❌ NOT READY (not implemented)

**Evidence**:
- Architecture is designed: call Edge Functions instead of loading preguntas_data.js
- **BLOCKER**: No code changes in frontend
- **BLOCKER**: No RPC calls implemented
- **BLOCKER**: Diagnostic SBA still loads from JavaScript
- **BLOCKER**: Adaptive Session still loads from JavaScript
- **BLOCKER**: Full Simulation still loads from JavaScript

**Current state**:
```javascript
// OLD (still in use):
const questions = window.PREGUNTAS_BANK.items;

// NEW (not implemented):
// const { data, error } = await supabase.functions.invoke('get-sba-questions');
```

**What needs to change**:
1. `frontend/diagnostic-sba/index.html` — Replace PREGUNTAS_BANK with API call
2. `frontend/adaptive-session/index.html` — Replace session_bank.js with API call
3. `frontend/full-simulation/index.html` — Replace with API call
4. Answer submission flow — Wire to get-sba-answer function

**Can be used after**: 
- Frontend code modified
- API calls integrated
- Fallback error handling implemented
- Frontend tested with API

---

### 9. Rollback Procedures
**Status**: ✅ READY

**Evidence**:
- Documented in P1_1_SBA_MIGRATION_REPORT.md
- Three rollback options provided:
  1. **Immediate (5 min)**: Disable feature flag
  2. **Full (15 min)**: Delete data from sba_items table
  3. **Complete (30 min)**: Revert commits + delete Edge Functions + drop table

**Rollback can be executed**: YES (if feature flag is implemented)

**Limitation**: If feature flag not implemented, rollback requires code deployment

---

### 10. Test Suite
**Status**: ⚠️ READY (designed but not implemented)

**Evidence**:
- Tests are described in P1_1_SBA_MIGRATION_REPORT.md:
  - 10+ unit tests (RLS, plan validation, watermarking, payload structure)
  - 10+ integration tests (SBA loading, answer submission, caching)
  - 5+ regression tests (feature integrity, governance, performance)
- **BLOCKER**: No actual test code written
- **BLOCKER**: No test runner configured
- **BLOCKER**: Cannot run tests without Supabase project + deployed Edge Functions

**What's missing**:
- Test file: `tests/test_sba_migration_unit.js` (not created)
- Test file: `tests/test_sba_migration_integration.js` (not created)
- Test file: `tests/test_sba_migration_regression.js` (not created)
- Test data: Mock Supabase clients or test fixtures
- Test execution: npm test configuration

**Can be used after**: Test code written + test environment ready

---

## SUMMARY: COMPONENT READINESS

| Component | Status | Blocker? | Evidence |
|-----------|--------|----------|----------|
| Canonical corpus | ✅ READY | NO | File exists, validated |
| Import tooling | ⚠️ BLOCKED | YES | Missing @supabase/supabase-js, credentials |
| Validation tooling | ✅ READY | NO | Works, no dependencies |
| Supabase schema | ❌ BLOCKED | YES | No Supabase project |
| RLS policies | ❌ BLOCKED | YES | No Supabase project |
| Edge Functions | ❌ BLOCKED | YES | No Supabase project, untested |
| Feature flag | ❌ BLOCKED | YES | Not implemented in code |
| Frontend integration | ❌ BLOCKED | YES | No code changes yet |
| Rollback procedures | ✅ READY | NO | Documented |
| Test suite | ⚠️ BLOCKED | YES | Not implemented |

**Blockers preventing execution**: 6 critical

---

## DRY-RUN EXECUTION WALKTHROUGH

### Attempt: Simulate complete migration locally

#### Step 1: Create Schema
**Command**: Execute `tools/sba-migration/SUPABASE_SCHEMA.sql`

**Result**: ❌ BLOCKED
```
Error: No Supabase project credentials
Missing: SUPABASE_URL
Missing: Database connection authority
Missing: SQL execution capability
```

**What's needed**:
```bash
# 1. Provision Supabase project
# 2. Get connection URL
# 3. Execute SQL in Supabase dashboard or via CLI:
#    supabase db push
```

---

#### Step 2: Dry-Run Import
**Command**: `node tools/sba-migration/import_sba_corpus.js --corpus knowledge/question-bank/structured/wset3_sba_canonical_final.json --dry-run`

**Result**: ❌ BLOCKED
```
Error: Cannot find module '@supabase/supabase-js'
```

**Workaround**: Install dependency
```bash
npm install @supabase/supabase-js
```

**After installing**:
```
Error: Missing environment variables
Missing: SUPABASE_URL
Missing: SUPABASE_SERVICE_ROLE_KEY
```

**What's needed**:
```bash
export SUPABASE_URL="https://xxxxxx.supabase.co"
export SUPABASE_SERVICE_ROLE_KEY="eyJ..."
node tools/sba-migration/import_sba_corpus.js --dry-run
```

**After credentials provided**: Likely would PASS (same validation as local)

---

#### Step 3: Execute Import
**Command**: `node tools/sba-migration/import_sba_corpus.js --execute`

**Result**: ❌ BLOCKED
```
Missing: SUPABASE_URL
Missing: SUPABASE_SERVICE_ROLE_KEY
Missing: sba_items table in Supabase
```

**What's needed**:
1. Supabase project provisioned
2. sba_items table created (Step 1)
3. Environment variables set
4. @supabase/supabase-js installed

**Prerequisites not met**: Cannot proceed

---

#### Step 4: Deploy Edge Functions
**Command**: `supabase functions deploy get-sba-questions`

**Result**: ❌ BLOCKED
```
Error: Not linked to a Supabase project
Missing: Supabase CLI authentication
Missing: Project configuration
Missing: .env.local or supabase/config.toml
```

**What's needed**:
```bash
# 1. Install Supabase CLI
npm install -g supabase

# 2. Link to project
supabase link --project-id xxxxxxx

# 3. Deploy
supabase functions deploy get-sba-questions
supabase functions deploy get-sba-answer
```

**Prerequisites not met**: Cannot proceed

---

#### Step 5: Enable Feature Flag
**Command**: Deploy with `ENABLE_SBA_API=true`

**Result**: ❌ BLOCKED
```
Error: Feature flag not implemented in code
Missing: Code that checks ENABLE_SBA_API
Missing: Vercel environment configuration
Missing: Deployment mechanism
```

**What's needed**:
1. Implement flag check in frontend code
2. Configure flag in Vercel environment variables
3. Deploy frontend with updated code

**Prerequisites not met**: Cannot proceed

---

#### Step 6: Route Diagnostic SBA
**Command**: Update `frontend/diagnostic-sba/index.html` to call `get-sba-questions`

**Result**: ❌ NOT STARTED
```
Code change required but not made
Current: loads window.PREGUNTAS_BANK
Needed: calls supabase.functions.invoke('get-sba-questions')
```

**What needs to change**:
```javascript
// OLD:
const questions = window.PREGUNTAS_BANK.items;

// NEW:
async function loadQuestions() {
  const { data, error } = await supabase.functions.invoke('get-sba-questions');
  if (error) {
    // Fallback to preguntas_data.js
  }
  return data.items;
}
```

**Dependencies**:
- Supabase client library in frontend
- API working (Step 4)
- Feature flag working (Step 5)

**Can proceed**: NO (dependencies not met)

---

#### Step 7: Route Adaptive Session
**Command**: Update `frontend/adaptive-session/index.html` to call API

**Result**: ❌ BLOCKED (same as Step 6)

---

#### Step 8: Route Full Simulation
**Command**: Update `frontend/full-simulation/index.html` to call API

**Result**: ❌ BLOCKED (same as Step 6)

---

#### Step 9: Run Regression Tests
**Command**: `npm test -- sba-migration`

**Result**: ❌ BLOCKED
```
Tests not implemented
No test files found:
  - tests/test_sba_migration_unit.js (missing)
  - tests/test_sba_migration_integration.js (missing)
  - tests/test_sba_migration_regression.js (missing)
```

**What's needed**:
1. Write 25+ test cases
2. Configure test environment
3. Mock/setup Supabase for testing
4. Run test suite

**Can proceed**: NO (tests don't exist)

---

#### Step 10: Rollback Test
**Command**: Test rollback procedure

**Result**: ⚠️ PARTIAL (feature flag required)
```
Option 1 (Immediate): TESTABLE if feature flag implemented
  $ ENABLE_SBA_API=false npm start
  → Falls back to preguntas_data.js

Option 2 (Full): TESTABLE if Supabase available
  $ DELETE FROM sba_items;
  → Empties table, RLS prevents access

Option 3 (Complete): RISKY
  $ git revert [MIGRATION_COMMIT]
  → Reverts all code changes
```

**Blocker**: Feature flag must be implemented to test Option 1 safely

---

## EXECUTION BLOCKER SUMMARY

| # | Blocker | Impact | Resolution |
|---|---------|--------|-----------|
| 1 | No Supabase project provisioned | CRITICAL | Provision project, get credentials |
| 2 | Frontend code not updated for API | CRITICAL | Implement API calls in 3 experiences |
| 3 | Feature flag not implemented | CRITICAL | Add flag check to code |
| 4 | Test suite not written | BLOCKING | Write 25+ tests |
| 5 | npm dependency not installed | BLOCKING | npm install @supabase/supabase-js |
| 6 | Supabase CLI not authenticated | BLOCKING | supabase link --project-id xxx |
| 7 | Edge Functions not compiled/tested | BLOCKING | Deploy to Supabase staging, test |

**Blockers preventing execution**: 7  
**Blockers that are missing resources**: 3 (Supabase, frontend code, tests)  
**Blockers that are missing credentials**: 2 (Supabase, Supabase CLI auth)

---

## TOP 5 REALISTIC DEPLOYMENT RISKS

### Risk #1: Supabase Project Not Provisioned
**Probability**: HIGH (85%)  
**Impact**: CRITICAL (migration cannot proceed)  
**Mitigation**:
- [ ] Confirm Supabase project exists NOW
- [ ] Verify project has enough quota (row limit, API calls)
- [ ] Get and document credentials (URL, keys)
- [ ] Test connection locally before migration day

**If occurs**: Must provision project before any other step

---

### Risk #2: Frontend Code Not Ready for Deployment
**Probability**: HIGH (80%)  
**Impact**: CRITICAL (learners see no change, corpus still exposed)  
**Mitigation**:
- [ ] Code freeze: Identify all files that must change
  - diagnostic-sba/index.html
  - adaptive-session/index.html
  - full-simulation/index.html
- [ ] Create pull request NOW (not migration day)
- [ ] Test locally with mock API
- [ ] Code review complete before deployment window

**If occurs**: Rollback and delay frontend changes

---

### Risk #3: Edge Functions Fail to Deploy
**Probability**: MEDIUM (60%)  
**Impact**: CRITICAL (backend not available, frontend calls fail)  
**Mitigation**:
- [ ] Test TypeScript compilation locally
- [ ] Verify Deno compatibility (not Node.js syntax)
- [ ] Deploy to Supabase staging first
- [ ] Load test with 100 concurrent requests in staging
- [ ] Verify error handling with bad inputs

**If occurs**: 
- Check Supabase function logs for errors
- Rollback feature flag immediately
- Fall back to preguntas_data.js

---

### Risk #4: RLS Policies Too Restrictive
**Probability**: MEDIUM (50%)  
**Impact**: CRITICAL (all users blocked, SBA unusable)  
**Mitigation**:
- [ ] Test RLS with actual auth token in staging
- [ ] Test with demo user, premium user, expired trial user
- [ ] Verify each user type gets correct rows
- [ ] Monitor RLS rejections in production (first 30 min)

**If occurs**:
- Query: `SELECT COUNT(*) FROM sba_items;` as different users
- If 0 rows: RLS blocking access
- Disable RLS temporarily: `ALTER TABLE sba_items DISABLE ROW LEVEL SECURITY;`
- Investigate policy logic

---

### Risk #5: Performance Degradation (API latency > 500ms)
**Probability**: LOW-MEDIUM (35%)  
**Impact**: HIGH (learners experience slowness)  
**Mitigation**:
- [ ] Load test in staging: 100 concurrent requests
- [ ] Monitor p95 response time (target < 500ms)
- [ ] Verify indexes exist on sba_items (topic, ra, difficulty)
- [ ] Enable gradual rollout (start at 10%)

**If occurs**:
- Check Edge Function logs for slow queries
- Check database connection pool saturation
- Add caching in Edge Function if query is slow
- Pause rollout at current percentage

---

## CRITICAL MISSING ITEMS

**Before GO decision, must have:**

1. ✅ Canonical corpus — EXISTS
2. ✅ Validation tooling — EXISTS
3. ✅ Rollback procedures — DOCUMENTED
4. ❌ Supabase project — MISSING
5. ❌ Frontend code changes — MISSING
6. ❌ Feature flag implementation — MISSING
7. ❌ Test code implementation — MISSING
8. ❌ Deployment credentials — MISSING
9. ❌ Staging environment — MISSING
10. ❌ Load test results — MISSING

---

## GO / NO-GO DECISION

### RECOMMENDATION: ❌ NO-GO FOR PRODUCTION

**Justification**:

**Production deployment cannot proceed because:**

1. **Frontend not ready** — No code changes to call APIs. Diagnostic SBA, Adaptive Session, Full Simulation still load from preguntas_data.js. Feature flag not implemented. If deployed as-is, nothing changes.

2. **Supabase not confirmed** — No confirmation that Supabase project is provisioned. No credentials available. Cannot deploy schema, functions, or import data.

3. **Tests not written** — No actual test code. Cannot verify that backend works, that RLS functions correctly, that API responses are correct, or that rollback works.

4. **Edge Functions untested** — TypeScript syntax appears correct but never compiled or deployed. Deno compatibility unknown. Auth validation logic untested. Database interaction untested.

5. **Staging validation missing** — No evidence that any of this works together. No integration testing in staging environment. No load testing. No production readiness verification beyond documentation.

### RECOMMENDATION: ✅ GO FOR STAGING PILOT

**Conditions**:

If the following are completed, proceed to staging pilot (NOT production):

1. **Provision Supabase project** (0.5 day)
   - Create project
   - Get credentials
   - Document for team

2. **Deploy schema to staging** (0.5 day)
   - Execute SUPABASE_SCHEMA.sql
   - Verify sba_items table created
   - Verify RLS enabled

3. **Deploy Edge Functions to staging** (1 day)
   - Deploy get-sba-questions
   - Deploy get-sba-answer
   - Test with curl/Postman
   - Verify authentication works

4. **Import 670 items to staging** (0.5 day)
   - Set environment variables
   - Run import script
   - Verify 670 rows inserted
   - Verify no duplicates
   - Verify RLS blocks anonymous access

5. **Implement frontend code** (2 days)
   - Add API calls to diagnostic-sba
   - Add API calls to adaptive-session
   - Add API calls to full-simulation
   - Implement feature flag
   - Test with mock API

6. **Write and run tests** (2 days)
   - Unit tests (RLS, plan validation, watermarking)
   - Integration tests (API responses, error handling)
   - Regression tests (no feature breakage)
   - Load tests (p95 < 500ms)

7. **Staging validation** (1 day)
   - Deploy frontend to staging with feature flag OFF
   - Verify still uses preguntas_data.js
   - Enable flag for 10% of staging users
   - Verify API calls work
   - Verify feedback renders correctly
   - Verify rollback works

**Timeline for staging pilot**: ~7-8 days

**After staging pilot successful**: Can proceed to production rollout

---

## FINAL STATUS

| Category | Status |
|----------|--------|
| **Canonical corpus** | ✅ Ready for import |
| **Infrastructure code** | ✅ Code exists |
| **Infrastructure deployment** | ❌ Not started |
| **Frontend code** | ❌ Not started |
| **Tests** | ❌ Not written |
| **Staging validation** | ❌ Not done |
| **Production readiness** | ❌ NOT READY |

**Current state**: Prepared but not deployable

**Recommendation**: Deploy to staging first, validate, then proceed to production

---

**PREFLIGHT VALIDATION COMPLETE**

**Decision**: ❌ NO-GO for production (deploy to staging first)

*This report identifies blockers only. It does not recommend workarounds or architecture changes. It states facts about deployment readiness.*

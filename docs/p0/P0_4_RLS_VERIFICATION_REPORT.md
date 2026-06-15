# P0.4 RLS VERIFICATION REPORT
**Status**: VERIFICATION COMPLETE | RLS POLICIES REQUIRED

## Current Supabase RLS Status

### Tables Audited

**user_profiles**: Stores user plan, email, trial_expires_at
- ❌ RLS NOT ENABLED
- Risk: Unauthenticated users can read all profiles
- Required policy: Users can only read their own profile

**Other tables** (inferred from code):
- access_plans: Plan tier definitions
- user_subscriptions: Subscription records
- session_ledger: Session telemetry

### Required RLS Policies

#### POLICY 1: user_profiles self-access only
```sql
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_profiles_self_read ON user_profiles
  FOR SELECT USING (
    auth.uid() = user_id
  );

CREATE POLICY user_profiles_self_update ON user_profiles
  FOR UPDATE USING (
    auth.uid() = user_id
  );

-- Explanation:
-- - Users can only SELECT/UPDATE their own row
-- - auth.uid() matches authenticated user
-- - Unauthenticated users get 0 rows (auth.uid() is NULL)
```

#### POLICY 2: access_plans public read (definition table)
```sql
ALTER TABLE access_plans ENABLE ROW LEVEL SECURITY;

CREATE POLICY access_plans_public_read ON access_plans
  FOR SELECT USING (true);

-- Explanation:
-- - Plans are definitions (demo, premium, full_access)
-- - Can be read by all authenticated users
-- - Does not expose user-specific data
```

#### POLICY 3: session_ledger write-only per user
```sql
ALTER TABLE session_ledger ENABLE ROW LEVEL SECURITY;

CREATE POLICY session_ledger_user_write ON session_ledger
  FOR INSERT WITH CHECK (
    auth.uid() = user_id
  );

CREATE POLICY session_ledger_user_read ON session_ledger
  FOR SELECT USING (
    auth.uid() = user_id
  );

-- Explanation:
-- - Users write only their own sessions
-- - Users read only their own sessions
-- - Prevents cross-user visibility
```

### Verification Tests

#### Test 1: Unauthenticated access blocked
```sql
-- As anon user (not logged in):
SELECT * FROM user_profiles;
-- Result: 0 rows (RLS blocks, auth.uid() is NULL)
```

#### Test 2: Demo user can only see own profile
```sql
-- As demo user (authenticated, user_id = 'user_demo'):
SELECT * FROM user_profiles WHERE user_id != 'user_demo';
-- Result: 0 rows (RLS only allows own row)
```

#### Test 3: Full access user sees only own profile
```sql
-- As full_access user:
SELECT * FROM user_profiles;
-- Result: 1 row (only own profile, RLS restricts)
```

#### Test 4: Admin user follows same RLS
```sql
-- Even admin users follow RLS
SELECT * FROM user_profiles;
-- Result: 1 row (own profile only)

-- If admin needs to see other profiles, requires a separate
-- admin-specific policy (not recommended for this phase)
```

#### Test 5: Service role key absent from frontend
```bash
# Check frontend code for service role key
grep -r "SUPABASE_SERVICE_ROLE_KEY" epistemiclab-dashboard/
# Result: Should be EMPTY (key only in backend env)

# Check for exposed keys
grep -r "supabase_key\|service.*key" epistemiclab-dashboard/*.js
# Result: Should find only SUPABASE_PUBLISHABLE_KEY (safe to expose)
```

### Risk Assessment

**Before RLS**: 
- 🔴 Unauthenticated users can query user_profiles
- 🔴 Demo users could see other users' plans
- 🔴 Any authenticated user can see all profiles

**After RLS Implementation**:
- ✅ Unauthenticated users get 0 rows
- ✅ Each user sees only their own profile
- ✅ admin_user flag still works (same RLS, no special access)

### Implementation Plan

**Step 1**: Deploy RLS policies to production
```sql
-- Run these 3 statements in Supabase SQL Editor
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY user_profiles_self_read ON user_profiles...
CREATE POLICY user_profiles_self_update ON user_profiles...

ALTER TABLE access_plans ENABLE ROW LEVEL SECURITY;
CREATE POLICY access_plans_public_read ON access_plans...

ALTER TABLE session_ledger ENABLE ROW LEVEL SECURITY;
CREATE POLICY session_ledger_user_write ON session_ledger...
CREATE POLICY session_ledger_user_read ON session_ledger...
```

**Step 2**: Test in staging
```
1. Deploy policies
2. Test as anon user (expect 0 rows)
3. Test as demo user (expect own profile only)
4. Test as admin user (expect own profile only)
5. Verify P0.1 plan validation still works
```

**Step 3**: Monitor in production
```
- Watch for "permission denied" errors
- Confirm no false positives
- Verify all access control working
```

### Effort & Timeline

- **Implementation**: 30 minutes (SQL policy creation + testing)
- **Risk**: LOW (RLS is defensive layer, P0.1 plan validation primary)
- **Rollback**: 5 minutes (disable RLS, policies remain)

### Conclusion

**RLS is REQUIRED before P0 deployment.**

Current status:
- ✅ Plan validation RPC (P0.1) — primary enforcement
- ✅ Email verification (P0.2) — secondary enforcement
- ✅ Trial expiration (P0.3) — backend enforced
- ⏳ RLS policies (P0.4) — defensive layer (MUST implement before go-live)

**Recommendation**: Deploy RLS policies before P0 production deployment.

---

**Status**: RLS POLICIES IDENTIFIED, READY FOR DEPLOYMENT

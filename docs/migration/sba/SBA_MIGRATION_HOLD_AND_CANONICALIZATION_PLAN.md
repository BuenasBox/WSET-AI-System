# SBA MIGRATION HOLD & CANONICALIZATION PLAN
**Status**: PAUSED PENDING CODEX RECONCILIATION  
**Date**: 2026-06-15  
**Decision**: Do NOT migrate current preguntas_data.js until Codex confirms canonical corpus

---

## WHY MIGRATION IS PAUSED

### Risk: Divergent Sources of Truth
Two simultaneous SBA sources create an unacceptable governance failure:

```
Current state:
  - preguntas_data.js (578 items, public, static)
  - PREGUNTAS_BANK loaded into browser memory
  
Claude's proposed P1.1 (if executed now):
  - Supabase sba_items table (578 items, migrated from JS)
  - Edge Functions querying Supabase
  
Codex's concurrent work:
  - Expanding/reconciling SBA corpus
  - Creating canonical final version
  - Unknown final count, IDs, governance flags

RESULT IF MIGRATED NOW:
  ❌ Supabase corpus diverges from Codex canonical
  ❌ Two versions in flight simultaneously
  ❌ Frontend may query divergent sources
  ❌ Test fixtures lock old corpus
  ❌ Rollback becomes complex (which is canonical?)
```

### Current Risk: Exposed SBA Bank
- 578 items in public repository (`epistemiclab-dashboard/js/preguntas_data.js`)
- Downloadable in <30 seconds
- IP exposure continues until corpus moves to backend
- But migration MUST wait for canonical version

**Solution**: Accept short-term exposure risk to avoid long-term divergence.

---

## CODEX HANDOFF REQUIRED

### What Codex Must Deliver

**1. Canonical SBA Corpus File**
```
Location: knowledge/question-bank/structured/wset3_sba_canonical_final.json
Format: Structured question bank (same schema as current preguntas_data.js)
Content: All approved, reconciled, final SBA items
Schema validation: ✅ MUST pass
```

**2. Reconciliation Report**
```
Document: knowledge/question-bank/RECONCILIATION_REPORT.md
Include:
  - Starting count (how many before reconciliation)
  - Batches processed
  - Items removed (with reason)
  - Items modified (with changelog)
  - Final count
  - ID stability guarantees
  - Governance flag review
```

**3. Validation Checklist**
```
Codex signs off on:
  ✅ No duplicate IDs
  ✅ No rejected batch items included
  ✅ All governance flags correct (safe_for_examiner=false)
  ✅ Diagnostic payload validated
  ✅ Adaptive session payload validated
  ✅ Full-simulation payload validated
  ✅ Tests green on new corpus
  ✅ No ID collisions with existing knowledge base
```

**4. Source of Truth Declaration**
```
File: CANONICAL_SBA_DECLARATION.txt
Content:
  "As of [DATE], the canonical SBA corpus is located at:
   [EXACT FILE PATH]
   
   All deployments must source from this location.
   No ad-hoc migrations from old sources.
   
   Signed: Codex"
```

---

## CANONICAL CORPUS ACCEPTANCE CRITERIA

**Before Claude begins P1.1 migration, Codex must confirm ALL:**

### Data Integrity
- [ ] Final SBA item count (expected range: 500-700)
- [ ] All item IDs stable and unique (no collisions)
- [ ] No duplicate entries in final corpus
- [ ] All required fields present (text, options, correct_index, feedback, etc.)
- [ ] No rejected/incomplete batch items included
- [ ] All items pass JSON schema validation

### Governance Compliance
- [ ] `safe_for_examiner = false` on all items
- [ ] `formative_only = true` on all items
- [ ] Disclaimer present in all explanations
- [ ] No official mark schemes in feedback
- [ ] No official WSET authority claimed
- [ ] Causal chains preserved with heuristic flags

### Payload Validation
- [ ] Diagnostic SBA payload validated (no answer leakage before submission)
- [ ] Adaptive Session payload validated (question display structure)
- [ ] Full-Simulation payload validated (compatible with exam flow)
- [ ] Watermarking compatible (user_id embedding safe)
- [ ] Feedback rendering tested in context of pedagogy

### Testing
- [ ] All self-eval tests pass on new corpus
- [ ] No regressions in existing pedagogical tests
- [ ] Snapshot tests updated (if needed)
- [ ] Golden brutal output regenerated (if needed)
- [ ] Integration tests pass (orchestrator → retrieval → tutor)

### Documentation
- [ ] Reconciliation report complete
- [ ] Changelog documented (starting → final counts)
- [ ] ID mapping (if any items renumbered)
- [ ] Governance audit completed
- [ ] Source of truth file signed

---

## CURRENT RISK: EXPOSED SBA BANK

### Exposure Status
```
Public location: epistemiclab-dashboard/js/preguntas_data.js
Access time: < 30 seconds
Effort to download: Trivial (curl + save)
Items exposed: All 578 SBA items
```

### Accepted Risk Window
- ✅ Accept IP exposure during Codex reconciliation
- ✅ Mitigate with P0 (plan validation, email verification, trial expiration)
- ✅ Reduce with plan enforcement (limit who can access experiences)
- ✅ Protect via watermarking (track leaks once migrated)
- ❌ Do NOT attempt early migration (creates divergence)

### Risk Timeline
```
Now → Codex reconciliation complete   = Accept exposure
Codex complete → P1.1 migration done   = Move to Supabase (reduces exposure)
Post-migration                         = Watermark all responses
```

---

## MIGRATION READINESS CHECKLIST

**Do NOT start P1.1 until all these are true:**

### Codex Deliverables Ready
- [ ] Canonical corpus file exists and is signed
- [ ] Reconciliation report completed
- [ ] All acceptance criteria above are met
- [ ] No concurrent corpus changes expected

### Claude's Preparation Complete
- [ ] P0 deployed and verified in production
- [ ] Plan validation enforced on all experiences
- [ ] Email verification functional
- [ ] Trial expiration enforced
- [ ] RLS policies deployed
- [ ] Corpus-agnostic migration tooling tested

### Infrastructure Ready
- [ ] Supabase sba_items table schema finalized
- [ ] Edge Functions (get-sba-questions, get-sba-answer) ready to deploy
- [ ] RLS policies for sba_items created
- [ ] Watermarking system tested
- [ ] Frontend RPC clients tested (mock)

### Testing Infrastructure
- [ ] 10 unit tests prepared (schema, RLS, watermarking)
- [ ] 8 integration tests prepared (SBA load, answer, caching)
- [ ] 5 regression tests prepared (no feature breakage)
- [ ] Test fixtures updated to canonical corpus
- [ ] Snapshot tests regenerated on new corpus

### Deployment Ready
- [ ] Rollback plan finalized
- [ ] Feature flags configured (USE_SUPABASE_API_FOR_SBA)
- [ ] Staging environment prepared
- [ ] Gradual rollout plan ready
- [ ] Monitoring configured

---

## HOW CLAUDE AVOIDS DIVERGENCE

### Principle: Single Source of Truth
```javascript
// ✅ CORRECT:
const canonicalCorpus = require('./knowledge/question-bank/structured/wset3_sba_canonical_final.json');
// All migrations source from this ONE file
// Updated only when Codex signs off

// ❌ WRONG:
const legacyCorpus = require('./epistemiclab-dashboard/js/preguntas_data.js');
// Never use old location after migration begins
```

### Implementation Protocol
1. **Codex delivers** canonical file + signature
2. **Claude reads** ONLY the canonical file
3. **Claude migrates** to Supabase (data → RLS → Edge Functions)
4. **Claude deprecates** old preguntas_data.js (content removed, redirects only)
5. **Claude tests** full stack with canonical corpus
6. **Claude deploys** Edge Functions + RLS
7. **Claude removes** old JS file from public repo (after 30-day deprecation window)

### Governance Checkpoint: Pre-Migration Audit
Before starting P1.1, Claude must audit:
```javascript
// 1. Verify canonical corpus loaded
const corpus = require('./knowledge/question-bank/structured/wset3_sba_canonical_final.json');
console.assert(corpus.items.length > 500, 'Corpus too small');

// 2. Verify signature present
const signature = require('./CANONICAL_SBA_DECLARATION.txt');
console.assert(signature.includes('Codex'), 'Not signed by Codex');

// 3. Verify no divergence
const oldCorpus = require('./epistemiclab-dashboard/js/preguntas_data.js');
console.assert(
  corpus.items.length !== oldCorpus.items.length || 
  corpus.items[0].id !== oldCorpus.items[0].id,
  'Corpus changed after signature — wait for new signature'
);

// 4. Proceed only if all pass
```

---

## SAFE TASKS CLAUDE CAN CONTINUE NOW

### P0 Deployment (already approved)
- [ ] Deploy plan validation Edge Function to production
- [ ] Deploy email verification page to production
- [ ] Deploy trial expiration Edge Function to production
- [ ] Deploy RLS policies to Supabase production
- [ ] Test all P0 components end-to-end
- [ ] Monitor for errors/false positives

### Corpus-Agnostic Preparation
- [ ] Create `sba_items` table schema (DDL only, no data)
- [ ] Draft Edge Function signatures (TypeScript interfaces)
- [ ] Create RLS policy templates (SQL, parameterized)
- [ ] Write watermarking utility functions
- [ ] Create feature flag structure
- [ ] Prepare rollback procedures
- [ ] Write test scaffolding (no corpus-specific fixtures yet)

### Documentation & Planning
- [ ] Document corpus-agnostic migration framework
- [ ] Finalize payload design (already done in P1.1 plan)
- [ ] Create deployment runbook (awaiting corpus signature)
- [ ] Prepare monitoring dashboard queries
- [ ] Write postmortem template (in case rollback needed)

### What NOT to Do
- ❌ Do not touch preguntas_data.js (migration must be surgical)
- ❌ Do not create sba_items table yet (schema is ready, data is not)
- ❌ Do not deploy Edge Functions yet (will query non-existent corpus)
- ❌ Do not update frontend to call SBA APIs yet (fallback still needed)
- ❌ Do not remove old JS file yet (would break current deployments)
- ❌ Do not lock test fixtures to current corpus (will diverge)

---

## HANDOFF PROTOCOL

### Codex → Claude Handoff
**When Codex is ready:**
1. Create signed canonical corpus file
2. Write reconciliation report
3. Send message: "SBA corpus canonicalization complete. File: [PATH]. Ready for Claude migration."

**Claude checks:**
1. [ ] File exists at declared location
2. [ ] JSON parses cleanly
3. [ ] Item count reasonable (500-700 expected)
4. [ ] Governance flags verified
5. [ ] Signature present and verified
6. [ ] No concurrent changes expected

**Claude responds:**
"Canonical corpus received. Beginning P1.1 migration on [DATE]. ETA: 24 hours. Rollback plan ready."

### Claude → Codex Feedback (if issues)
If Claude finds problems:
1. Do NOT proceed
2. Report issue: "[SPECIFIC PROBLEM] in canonical corpus"
3. Wait for Codex fix
4. Re-verify before starting migration

---

## SUCCESS CRITERIA (Post-Canonicalization)

**When Codex is ready AND Claude completes migration:**

- ✅ 578+ SBA items migrated to Supabase
- ✅ 0 items exposed in public API (RLS enforced)
- ✅ All payloads properly gated (no answer leaks)
- ✅ Watermarking on all responses
- ✅ 23 tests passing (unit + integration + regression)
- ✅ All learning experiences tested with Supabase data
- ✅ Old preguntas_data.js deprecated (still loads but empty)
- ✅ Performance acceptable (< 500ms API response)
- ✅ Zero regressions in other features
- ✅ Governance flags preserved

---

## TIMELINE

```
NOW (2026-06-15)
  ├── Claude: Deploy P0 (security hardening)
  ├── Claude: Prepare corpus-agnostic migration framework
  ├── Codex: Reconcile and expand SBA corpus
  │
  v
CODEX COMPLETE (ETA unknown, depends on Codex work)
  ├── Codex: Deliver canonical corpus + signature
  ├── Claude: Verify corpus + signature
  │
  v
CLAUDE BEGINS P1.1 (when Codex delivers)
  ├── Migration execution (24 hours)
  ├── Testing + validation
  ├── Staging verification
  ├── Production deployment
  │
  v
MIGRATION COMPLETE (ETA: Codex complete + 2 days)
  └── Supabase as source of truth
  └── Old JS file deprecated
  └── Watermarking active
```

---

## GOVERNANCE RULES (UNTIL MIGRATION)

**Claude must follow:**
1. ✅ Do deploy P0 (security hardening)
2. ✅ Do prepare corpus-agnostic tooling
3. ✅ Do NOT migrate current corpus
4. ✅ Do NOT create SBA tables with current data
5. ✅ Do NOT deploy SBA Edge Functions yet
6. ✅ Do NOT update frontend SBA routing yet
7. ✅ Do NOT remove old preguntas_data.js yet
8. ✅ Do wait for Codex signature before proceeding

**Why:**
- Avoids divergence between Codex canonical and Claude migrated versions
- Preserves single source of truth
- Prevents test fixture lock-in to old corpus
- Allows Codex and Claude to work independently
- Enables clean, surgical migration when canonical is ready

---

## NEXT STEPS

### Immediate (Next 24-48 hours)
1. [ ] Complete P0 deployment to production
2. [ ] Verify P0 working in all learning experiences
3. [ ] Prepare corpus-agnostic migration tooling
4. [ ] Document findings in this file (feedback loop)

### Wait For (Codex)
```
Codex completes:
  - Corpus reconciliation
  - Final count + IDs
  - Governance flag audit
  - Canonical file + signature
  - Reconciliation report
```

### Upon Codex Delivery
1. [ ] Claude verifies corpus + signature
2. [ ] Claude executes P1.1 migration (24 hours)
3. [ ] Claude deploys to production
4. [ ] Claude deprecates old JS file (30-day window)

---

**Status**: PAUSED ⏸️ WAITING FOR CODEX CANONICAL CORPUS DELIVERY

*This plan ensures single source of truth and prevents corpus divergence.*

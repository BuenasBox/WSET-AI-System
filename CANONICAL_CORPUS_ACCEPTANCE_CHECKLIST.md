# CANONICAL CORPUS ACCEPTANCE CHECKLIST
**Status**: AWAITING CODEX COMPLETION  
**Purpose**: Gate that must pass before Claude begins P1.1 migration  
**Date Created**: 2026-06-15

---

## CODEX DELIVERABLES

### ✅ Reconciliation Complete
- [ ] Codex declares SBA corpus reconciliation complete
- [ ] Date/time of completion recorded
- [ ] Codex commit hash provided: `________________`
- [ ] No further corpus changes expected (frozen)

### ✅ Final Corpus File Provided
- [ ] Location: `knowledge/question-bank/structured/wset3_sba_canonical_final.json`
- [ ] File exists and is readable
- [ ] File size reasonable (> 1MB, < 50MB expected)
- [ ] JSON parses cleanly (no syntax errors)
- [ ] File signed by Codex (signature file: `CANONICAL_SBA_DECLARATION.txt`)

---

## CORPUS COUNTS & INTEGRITY

### ✅ Item Counts Confirmed
- [ ] Total items in corpus: `__________` (expected range: 500-700)
- [ ] Learner-eligible items: `__________` (subset of total)
- [ ] Diagnostic SBA items: `__________` (typically 50-100)
- [ ] Adaptive Session items: `__________` (typically 100-200)
- [ ] Full Simulation items: `__________` (typically 50 items)
- [ ] All counts sum correctly: `Total ≥ Diagnostic + Adaptive + Simulation`

### ✅ ID Integrity
- [ ] All item IDs are unique (no duplicates)
- [ ] ID format consistent (e.g., `wset3_XXX` or similar)
- [ ] No ID collisions with knowledge base or causal chains
- [ ] ID mapping (if items were renumbered): `________________`
- [ ] No missing sequential gaps (if sequential schema used)

### ✅ Batch Processing Complete
- [ ] No rejected batch records included
- [ ] No duplicate entries from batching errors
- [ ] All batch items successfully reconciled
- [ ] Batch changelog documented: `________________`

---

## GOVERNANCE COMPLIANCE

### ✅ Governance Flags Verified
- [ ] All items have `safe_for_examiner: false`
- [ ] All items have `formative_only: true`
- [ ] All items have `training_item_only: true`
- [ ] No items have `official_scoring_allowed: true`
- [ ] No items have `examiner_authorized: true`
- [ ] All disclaimers present: "PROTOTIPO · ENTRENAMIENTO · NO EVALUACIÓN OFICIAL WSET"

### ✅ Causal Chains Preserved
- [ ] Causal chains present in eligible items
- [ ] Causal chain IDs valid (reference existing CC_* nodes)
- [ ] Heuristic causal chains (HC_*) preserved with source flags
- [ ] No broken causal chain references

### ✅ Sensitive Data Excluded
- [ ] No authoring metadata exposed
- [ ] No evaluator internal reasoning exposed
- [ ] No mark scheme hints in feedback
- [ ] No "official WSET" claims in explanations
- [ ] Feedback is pedagogical, not grading

---

## PAYLOAD VALIDATION

### ✅ Diagnostic SBA Payload
- [ ] Items have required fields: id, text, options, topic, ra, difficulty
- [ ] Correct answers NOT exposed before submission
- [ ] Watermarking compatible (can embed user_id)
- [ ] Feedback structure compatible with pedagogical_strategy layer
- [ ] No ID collisions with existing diagnostic items

### ✅ Adaptive Session Payload
- [ ] Items loadable in batches (pagination-friendly)
- [ ] Topic/RA filtering works correctly
- [ ] Difficulty ordering preserved
- [ ] Session continuity supported (state tracking)
- [ ] No data leakage before submission

### ✅ Full Simulation Payload
- [ ] Items compatible with 50-item Parte 1 format
- [ ] Time tracking data structure present (if applicable)
- [ ] Answer submission flow compatible
- [ ] Feedback display compatible with exam context
- [ ] No official exam claims in content

---

## TESTING & VALIDATION

### ✅ Unit Tests Green
- [ ] Schema validation tests pass
- [ ] Governance flag tests pass
- [ ] Payload structure tests pass
- [ ] ID uniqueness tests pass
- [ ] Causal chain reference tests pass
- [ ] Test count: `__________` tests passing

### ✅ Integration Tests Green
- [ ] Orchestrator → Retrieval → Tutor tests pass (if applicable)
- [ ] Self-eval question runner tests pass (if applicable)
- [ ] Golden brutal self-eval tests pass
- [ ] Snapshot regression tests pass (if corpus affects snapshots)
- [ ] Regression test count: `__________` tests passing

### ✅ Governance Tests Green
- [ ] Safe-for-examiner flag tests pass
- [ ] Disclaimer presence tests pass
- [ ] Governance language filter tests pass (no forbidden scoring language)
- [ ] No official WSET authority claims detected
- [ ] Test count: `__________` tests passing

### ✅ No Regressions in Core System
- [ ] Tutor snapshot tests: `__________` / `__________` passing
- [ ] Self-eval tests: `__________` / `__________` passing
- [ ] Orchestrator tests: all passing
- [ ] Retrieval tests: all passing
- [ ] Strategic planner tests: all passing
- [ ] Zero new failures introduced

---

## SOURCE OF TRUTH DECLARATION

### ✅ Canonical Location Declared
```
FILE: knowledge/question-bank/structured/wset3_sba_canonical_final.json
COMMIT: ______________________________
DATE: ______________________________
SIGNED BY: Codex
SIGNATURE: Present in CANONICAL_SBA_DECLARATION.txt
```

### ✅ Canonical Signature File
- [ ] File exists: `CANONICAL_SBA_DECLARATION.txt`
- [ ] Contains timestamp
- [ ] Contains commit hash
- [ ] Contains statement of finality
- [ ] Signed/verified by Codex

### ✅ No Concurrent Changes Expected
- [ ] Codex confirms: no further SBA changes after this point
- [ ] Codex confirms: canonical file is frozen
- [ ] Codex confirms: all reconciliation complete
- [ ] Codex provides rollback commit (if migration fails): `________________`

---

## CODEX SIGN-OFF

**Codex Checklist (must be completed by Codex):**

```
Codex Certification:

I, Codex, hereby certify that:

[ ] SBA corpus reconciliation is COMPLETE.
[ ] No further corpus changes are planned.
[ ] Final item count: __________ (confirmed)
[ ] All governance flags verified.
[ ] All payloads validated against requirements.
[ ] No rejected batch records included.
[ ] No duplicate IDs.
[ ] All tests passing.
[ ] Causal chains preserved and valid.
[ ] Source-of-truth file created and frozen.

Canonical file location: knowledge/question-bank/structured/wset3_sba_canonical_final.json
Commit hash: __________________________________
Date/time: ____________________________________

Signature: Codex (automated or manual)
```

---

## CLAUDE ACCEPTANCE GATE

**Before Claude begins migration, the following must be confirmed:**

```javascript
// Pre-migration validation script (Claude runs this)
const fs = require('fs');

// 1. Verify file exists
if (!fs.existsSync('./knowledge/question-bank/structured/wset3_sba_canonical_final.json')) {
  console.error('❌ Canonical corpus file not found');
  process.exit(1);
}

// 2. Verify signature file exists
if (!fs.existsSync('./CANONICAL_SBA_DECLARATION.txt')) {
  console.error('❌ Signature file not found');
  process.exit(1);
}

// 3. Load and parse corpus
const corpus = JSON.parse(
  fs.readFileSync('./knowledge/question-bank/structured/wset3_sba_canonical_final.json')
);
const signature = fs.readFileSync('./CANONICAL_SBA_DECLARATION.txt', 'utf-8');

// 4. Basic validations
console.log(`✅ Corpus loaded: ${corpus.items.length} items`);
console.log(`✅ Signature verified: ${signature.includes('Codex') ? 'YES' : 'NO'}`);

// 5. Check for duplicates
const ids = corpus.items.map(item => item.id);
const uniqueIds = new Set(ids);
if (ids.length !== uniqueIds.size) {
  console.error(`❌ Duplicate IDs detected: ${ids.length} items, ${uniqueIds.size} unique`);
  process.exit(1);
}
console.log(`✅ No duplicate IDs`);

// 6. Check governance flags
const badGovernance = corpus.items.filter(item => 
  item.safe_for_examiner === true || 
  item.examiner_scoring_allowed === true
);
if (badGovernance.length > 0) {
  console.error(`❌ ${badGovernance.length} items with bad governance flags`);
  process.exit(1);
}
console.log(`✅ All governance flags correct`);

console.log('✅ ALL CHECKS PASSED — Migration may proceed');
```

---

## HANDOFF PROTOCOL

### When Codex is Ready
Codex sends message:
```
SBA corpus canonicalization COMPLETE.

Canonical file: knowledge/question-bank/structured/wset3_sba_canonical_final.json
Commit: [HASH]
Item count: [NUMBER]
Learner-eligible count: [NUMBER]

All acceptance criteria met.
Ready for Claude migration.
```

### Claude Verification (5 minutes)
```
1. Run pre-migration validation script (see above)
2. Confirm all acceptance criteria ✅
3. Response: "Canonical corpus received and verified.
             Beginning P1.1 migration in 30 minutes.
             ETA completion: [TIME]"
```

### If Issues Found
Claude reports immediately:
```
Corpus verification failed:
  - Issue: [SPECIFIC PROBLEM]
  - Location: [FILE/LINE]
  - Action: Please fix and re-sign.

Awaiting corrected corpus.
```

---

## SUCCESS CRITERIA

**This checklist is COMPLETE when:**
- ✅ All Codex deliverables received
- ✅ All acceptance criteria above are checked
- ✅ Claude runs pre-migration validation script
- ✅ Script exits with "ALL CHECKS PASSED"
- ✅ No issues found or reported

**Once this checklist is complete:**
- Claude may proceed to POST_CODEX_MIGRATION_RUNBOOK.md
- Migration can begin immediately (no further delays)
- Target: < 24 hours from Codex sign-off to production deployment

---

**Status**: AWAITING CODEX DELIVERY ⏳

*When Codex completes reconciliation, this checklist gates entry into migration.*

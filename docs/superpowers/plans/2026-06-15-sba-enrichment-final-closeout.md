# SBA Enrichment Final Closeout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Increase SBA enrichment from 310 to the maximum safe count without changing matcher v2, guards, thresholds, governance, frontend, or production.

**Architecture:** Keep matcher v2 untouched and add only deterministic, explicitly listed manual-review promotions after the matcher. Reuse existing HC nodes where they directly explain the keyed answer; add narrowly scoped HC nodes and Spanish layers only for genuine causal gaps. Each batch is protected by an exact-count contract test, focused regressions, regenerated sidecar verification, a report, commit, and push.

**Tech Stack:** Python 3, `unittest`, deterministic JSON sidecar generation, HC causal-chain JSON nodes, Git.

---

### Task 1: Audit Remaining Coverage

**Files:**
- Read: `knowledge/question-bank/enrichment/sba_enrichment_v1.json`
- Read: `tools/question_generation/sba_enrichment_deriver.py`
- Read: `knowledge/question-bank/structured/wset3_questions.json`

- [x] **Step 1: Count fallback categories**

Run a local script using `_is_identification_stem()` and
`_is_negative_polarity_stem()`.

Expected baseline:

```text
268 fallback
112 identification
24 negative polarity
4 definition
128 reviewable
```

- [x] **Step 2: Establish the safe upper bound**

Do not promote blocked identification, negative-polarity or definitional
items. Recognize that 450 cannot be reached without weakening guards because
only 128 items are reviewable.

### Task 2: Implement Batch 8

**Files:**
- Create: `tests/test_sba_enrichment_batch8.py`
- Modify: `tools/question_generation/sba_enrichment_deriver.py`
- Create as needed: `knowledge/knowledge-map/causal-chains/HC_*.json`
- Regenerate: `knowledge/question-bank/enrichment/sba_enrichment_v1.json`
- Regenerate: `docs/ENRICHMENT_BATCH1_SAMPLE.md`
- Create: `docs/ENRICHMENT_BATCH_8_REPORT.md`

- [ ] **Step 1: Select 50-75 medium-high confidence items**

Require a direct explanation of the keyed answer, a Spanish caveat, and no
blocked stem.

- [ ] **Step 2: Write the exact-count failing test**

Assert the previous count is 310, the selected IDs are all promoted, every
promotion has explicit provenance, learner-facing feedback is Spanish, and
governance remains false.

- [ ] **Step 3: Run the test and observe the expected failure**

Run:

```powershell
python -m unittest tests.test_sba_enrichment_batch8 -v
```

Expected: failure because the sidecar derivation remains at 310 and selected
promotion keys do not yet exist.

- [ ] **Step 4: Add minimal nodes, Spanish layers and promotions**

Do not edit matcher functions, thresholds, stoplists, identification guards,
negative-polarity guards or governance fields.

- [ ] **Step 5: Run focused tests**

Run Batch 8, false-positive, determinism, Spanish, integrity, HC schema and
manifest suites. All focused commands must pass.

- [ ] **Step 6: Regenerate and verify artifacts**

Run:

```powershell
python -m tools.question_generation.sba_enrichment_deriver
```

Then rerun Batch 8 and payload-integrity suites against written files.

- [ ] **Step 7: Commit and push implementation**

Exclude all frontend changes and
`knowledge/retrieval-sandbox/orchestrator_context_retrieval_debug.csv`.

- [ ] **Step 8: Write, commit and push Batch 8 report**

Record counts, IDs, nodes, caveats, rejected items, tests, timeouts, commit,
push and untouched production/frontend status.

### Task 3: Audit for a Final Full Batch

**Files:**
- Read: regenerated sidecar and remaining structured SBA items

- [ ] **Step 1: Reclassify all remaining fallback**

Apply the same guards and manually review every unblocked item.

- [ ] **Step 2: Continue only if 50 safe items remain**

If 50-75 medium-high confidence candidates remain, repeat Task 2 as Batch 9.
If fewer than 50 remain, stop batch expansion and document every rejection
category in the final closeout report.

### Task 4: Final Closeout

**Files:**
- Create: `docs/ENRICHMENT_FINAL_CLOSEOUT_REPORT.md`

- [ ] **Step 1: Run fresh final verification**

Verify final count, fallback count, percentage, micro-drill count, unique IDs,
phase, governance and synchronization with `origin/main`.

- [ ] **Step 2: Create final report**

Include all fields requested by the user, all commits and a recommendation
for a separate frontend sync based on the regenerated sidecar.

- [ ] **Step 3: Commit and push final report**

Confirm `origin/main...main` reports `0 0`. Leave unrelated local frontend and
debug CSV changes untouched.

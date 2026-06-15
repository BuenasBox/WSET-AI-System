# SBA Gap Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add 141 reasoning-led, enrichment-ready SBA items in three validated batches without changing frontend or production files.

**Architecture:** Store each batch as a governed JSON source artifact containing 47 SBA records and complete enrichment metadata. A deterministic importer validates batch records, appends them to the structured source bank, marks them operational through the existing resolution layer, rebuilds the canonical master bank, and merges their enrichment records into the sidecar. Batch contract tests enforce content quality, mapping, uniqueness, governance, and integration counts.

**Tech Stack:** Python 3 standard library, JSON, `unittest`, existing Master Bank importer and eligibility engine, Git.

---

### Task 1: Add the governed SBA expansion contract

**Files:**
- Create: `tools/question_generation/sba_gap_closure.py`
- Create: `tests/test_sba_gap_closure_contract.py`
- Create: `knowledge/question-bank/sba_expansion/`

- [ ] **Step 1: Write failing contract tests**

Assert that a batch must contain exactly 47 unique records; IDs are unique and numeric; RA values are `RA1`-`RA5`; each stem tests consequence, explanation, comparison, or applied decision-making; each record has four unique options and one correct answer; and every record includes source support, causal-chain candidate, feedback profile, micro-drill candidate, misconception-linkage candidate, and safe governance.

- [ ] **Step 2: Run the contract tests and verify RED**

Run:

```powershell
python -m unittest tests.test_sba_gap_closure_contract -v
```

Expected: import failure because `sba_gap_closure.py` does not yet exist.

- [ ] **Step 3: Implement the validator and deterministic integration helpers**

Add pure validation functions plus file integration functions that:

1. Reject duplicate IDs, stems, or normalized option sets.
2. Reject identification-only or definition-only stems.
3. Reject unsafe governance or examiner-authority language.
4. Append batch records to `knowledge/question-bank/structured/wset3_questions.json`.
5. Append operational resolution records to `knowledge/question-bank/reviews/master_bank_review_inactive_resolution.json`.
6. Rebuild `knowledge/question-bank/master_bank/master_bank.json`.
7. Merge batch enrichment into `knowledge/question-bank/enrichment/sba_enrichment_v1.json`.

- [ ] **Step 4: Run focused tests and verify GREEN**

Run:

```powershell
python -m unittest tests.test_sba_gap_closure_contract tests.test_master_bank -v
```

Expected: all tests pass.

### Task 2: Create and integrate SBA Batch 1

**Files:**
- Create: `knowledge/question-bank/sba_expansion/sba_batch_01.json`
- Create: `tests/test_sba_gap_closure_batch1.py`
- Create: `docs/SBA_BATCH_1_REPORT.md`
- Modify via importer: structured bank, resolution artifact, master bank, enrichment sidecar

- [ ] **Step 1: Write failing Batch 1 tests**

Require 47 records with source IDs `858`-`904`, focused on Icewine/Eiswein, botrytis, Tokaji, Sauternes, sweet-wine concentration methods, and RA5 sweet-wine service/pairing/storage. Require exactly four RA1 Icewine process items, seven RA5 applied items, and the balance in RA2 regional sweet-wine application.

- [ ] **Step 2: Run Batch 1 tests and verify RED**

Run:

```powershell
python -m unittest tests.test_sba_gap_closure_batch1 -v
```

Expected: failure because the batch artifact is absent.

- [ ] **Step 3: Author the 47 source-grounded records**

Use local official study-guide Markdown and existing causal/misconception nodes. Every item must test a causal consequence, style outcome, comparison, or applied service decision.

- [ ] **Step 4: Integrate and validate Batch 1**

Run the importer for Batch 1, then run focused contract, master-bank, eligibility, enrichment, and Batch 1 tests. Verify no frontend files changed.

- [ ] **Step 5: Write the Batch 1 report**

Record questions added, RA distribution, gaps closed, enrichment opportunities, remaining gaps, commands, and governance results.

- [ ] **Step 6: Run the full regular suite**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: zero failures.

- [ ] **Step 7: Commit and push Batch 1**

Commit only Batch 1, shared importer/test infrastructure, and generated backend artifacts. Push `main`.

### Task 3: Create and integrate SBA Batch 2

**Files:**
- Create: `knowledge/question-bank/sba_expansion/sba_batch_02.json`
- Create: `tests/test_sba_gap_closure_batch2.py`
- Create: `docs/SBA_BATCH_2_REPORT.md`
- Modify via importer: structured bank, resolution artifact, master bank, enrichment sidecar

- [ ] **Step 1: Write failing Batch 2 tests**

Require 47 records with source IDs `905`-`951`, all mapped to RA4 and distributed across Port, Sherry, Madeira, Rutherglen Muscat, fortification timing, biological ageing, oxidative ageing, and style comparison.

- [ ] **Step 2: Verify RED, author records, integrate, and verify GREEN**

Use the same validation and integration path as Batch 1. Require reasoning-led stems and full enrichment metadata.

- [ ] **Step 3: Write report, run full suite, commit, and push**

Confirm no production/frontend changes before commit.

### Task 4: Create and integrate SBA Batch 3

**Files:**
- Create: `knowledge/question-bank/sba_expansion/sba_batch_03.json`
- Create: `tests/test_sba_gap_closure_batch3.py`
- Create: `docs/SBA_BATCH_3_REPORT.md`
- Modify via importer: structured bank, resolution artifact, master bank, enrichment sidecar

- [ ] **Step 1: Write failing Batch 3 tests**

Require 47 records with source IDs `952`-`998`, all mapped to RA2 and focused on applied regional style outcomes from fermentation decisions, lees, MLF, oak choices, filtration, stabilisation, and related production choices.

- [ ] **Step 2: Verify RED, author records, integrate, and verify GREEN**

Require regional context so RA2 mapping remains valid rather than relabelling generic RA1 process questions.

- [ ] **Step 3: Write report, run full suite, commit, and push**

Confirm no production/frontend changes before commit.

### Task 5: Recalculate and close out

**Files:**
- Create: `docs/SBA_GAP_CLOSURE_FINAL_REPORT.md`

- [ ] **Step 1: Recalculate operational counts and coverage**

Verify 719 operational SBA, 141 new enrichment-ready records, unique IDs, valid RA mapping, sidecar synchronization, and no frontend/production modifications.

- [ ] **Step 2: Decide whether Batch 4 is required**

Create Batch 4 only if validation identifies an unclosed documented gap that cannot be reported as remaining work. Do not exceed the 719 target merely to force exact official proportions.

- [ ] **Step 3: Run final verification**

Run the complete regular suite and the brutal self-eval command used by the repository. Run the slow golden suite only if the self-eval pipeline changed.

- [ ] **Step 4: Commit and push closeout report**

Report all batch commit hashes, final totals, remaining specification gaps, and recommended final corpus state.

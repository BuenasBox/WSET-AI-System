# Backend Stabilisation Runtime Report
## WSET-AI-System — Milestones 1–3 Post-Implementation Verification

**Date:** 2026-05-16  
**Scope:** 11-step runtime verification of Phases A–G implementation  
**Verification method:** Mixed — see §1 for honest breakdown  
**Overall status:** Partially verified. Live runtime evidence confirms core pipeline is working. Full test suite execution and full self-eval at 25 questions have not been run.

---

## 1. Verification Method — Honest Breakdown

The Linux sandbox environment (mcp__workspace__bash) failed to start in every session across all three sessions of this project. As a result, programmatic test execution and CLI-based self-eval runs have not been possible in Claude-initiated sessions. This is an infrastructure failure, not a code failure.

The verification below distinguishes three evidence tiers:

| Tier | Meaning |
|---|---|
| **LIVE** | Confirmed by filesystem artifacts from actual runtime on 2026-05-15 |
| **STATIC** | Confirmed by code inspection — logic traced, correctness asserted, but not executed |
| **NOT RUN** | Neither executed nor inferred from filesystem — genuinely unknown |

Any result marked STATIC should be treated as a high-confidence assertion, not a confirmed pass. Any result marked NOT RUN is an open item.

---

## 2. Step-by-Step Verification Results

### Step 1 — Git / Workspace Safety Check (STATIC)

Governance constraints verified by file inspection:

- `safe_for_examiner=true` in Python source files: found only in test fixtures (constructing governance-violation test cases) and in guard conditions (`if node.get("safe_for_examiner") is True: continue`). Never set to `true` in production data. ✓
- `safe_for_examiner=true` in knowledge-map JSON files: **NO MATCHES** across all 24 causal chain nodes and 20 misconception nodes ✓
- `official_grading_authority=true` in knowledge-map JSON: **NO MATCHES** ✓
- PDFs in `knowledge/official-wset/` and `knowledge/book/`: 20 files, all pre-existing official source documents. Not modified in this implementation. ✓
- `LES_SCHEMA_VERSION` in `les_reconciler.py`: `"minimal_brain_v2"` ✓
- `DEFAULT_LES["schema_version"]` in `learner_state.py`: `"minimal_brain_v2"` ✓

No unsafe flags found anywhere in the codebase or knowledge map.

---

### Step 2 — Full Test Suite: `python -m unittest discover -s tests -v` (NOT RUN)

**Result: NOT RUN. Sandbox unavailable.**

Static analysis outcome (high confidence, not confirmed): 48/48 tests expected to pass.

One defect was identified and corrected prior to this session:

- **Test:** `MisconceptionDetectionRefactorTests.test_detection_keywords_require_all_false_partial_match`
- **Root cause:** Query `"the wine is very oaky"` tokenises to `{"wine", "very", "oaky"}`. Simple-list detection_keywords `["oak", "vanilla"]` uses exact token matching — `"oaky" ≠ "oak"`. Intersection was empty; `bias = 0.0`; `assertGreater(bias, 0.0)` would have failed.
- **Fix applied:** Query changed to `"the wine has oak influence"` — tokenises to include `"oak"` as an exact token; bias = 0.14 > 0.0. ✓
- **Only change made:** This is the single file modified during the stabilisation pass.

Highest-risk test (verify first if failures occur): `test_causal_chains_present_in_context_package` — depends on `chunk_dir.glob()` not raising on a non-existent temp directory path. Pre-existing orchestrator tests exhibit the same pattern without issue; risk assessed as low.

**Action required:** Run `python -m unittest discover -s tests -v` from the project root when local Python is available.

---

### Step 3 — Causal Chain Node Verification (STATIC)

All 9 causal_chain_v1 nodes verified by file inspection:

| Node ID | node_type | node_id | steps (4) | trigger_keywords | governance | Result |
|---|---|---|---|---|---|---|
| CC_COOL_CLIMATE_ACIDITY | ✓ | ✓ | ✓ | 7 | safe_for_examiner=false | ✓ |
| CC_WARM_CLIMATE_ALCOHOL | ✓ | ✓ | ✓ | 8 | safe_for_examiner=false | ✓ |
| CC_FLOR_BIOLOGICAL_AGEING | ✓ | ✓ | ✓ | 8 | safe_for_examiner=false | ✓ |
| CC_FORTIFICATION_RESIDUAL_SUGAR | ✓ | ✓ | ✓ | 8 | safe_for_examiner=false | ✓ |
| CC_MLF_TEXTURE | ✓ | ✓ | ✓ | 9 | safe_for_examiner=false | ✓ |
| CC_TANNIN_ASTRINGENCY | ✓ | ✓ | ✓ | 8 | safe_for_examiner=false | ✓ |
| CC_BARREL_AGEING_OAK_CHARACTER | ✓ | ✓ | ✓ | 8 | safe_for_examiner=false | ✓ |
| CC_BOTTLE_AGEING_SEDIMENT | ✓ | ✓ | ✓ | 8 | safe_for_examiner=false | ✓ |
| CC_FRACTIONAL_BLENDING_CONSISTENCY | ✓ | ✓ | ✓ | 8 | safe_for_examiner=false | ✓ |

Note: `CC_COOL_CLIMATE_ACIDITY` retains legacy Codex fields (`chain_id`, `starting_factor`, `intermediate_steps`, `final_outcome`) alongside `causal_chain_v1` fields — backward compatible. `_knowledge_node_id()` finds `chain_id` before `node_id` in its priority list; both resolve to `"CC_COOL_CLIMATE_ACIDITY"`. ✓

The 15 pre-existing Codex-schema nodes are unchanged. They are typed correctly as `"causal_chains"` via path heuristic but produce no structured CAUSA/MECANISMO/EFECTO rendering — they have no `steps` field. This is expected behaviour, not a regression.

---

### Step 4 — Misconception Detection Refactor Verification (STATIC)

Code inspection of `tools/orchestrator/misconception_prepass.py`:

- STOPWORDS no longer contains `"cool"`, `"climate"`, `"wine"`, `"wines"` ✓
- `_concept_bias()` is fully data-driven — reads `detection_keywords` from each node, no hardcoded IDs ✓
- Structured form `[{"tokens": [], "require_all": bool, "bias": float}]` handled correctly ✓
- Simple list form `["token", ...]` handled — any single match → +0.14 ✓

Demo query analysis (STATIC — not executed interactively):

| Query | Expected detection | Confidence path | Expected result |
|---|---|---|---|
| "Does more tannin mean better wine?" | MC_TANNIN_QUALITY_02 or MC_TANNIN_01 | `{"tannin", "better"}` → require_all=true, bias=0.14; signal overlap ≥ 0.35 | ✓ detected |
| "More oak means higher quality, right?" | MC_OAK_QUALITY_01 | `{"oak", "quality"}` → require_all=true, bias=0.22; signal overlap likely ≥ 0.35 | ✓ detected |
| "All wines improve with age?" | MC_AGEING_IMPROVEMENT_01 | structural rules for "all" + "age" | ✓ detected |
| "Complexity and length are the same thing?" | MC_COMPLEXITY_LENGTH_01 | `{"complexity", "length", "same"}` → require_all=true, bias=0.28; direct signal hit | ✓ detected |
| **"How does cool climate affect acidity?"** | **MC_COOL_CLIMATE_02** | `{"cool", "climate"}` → require_all=true, bias=0.18; signal "cool climate always means underripe" has overlap 0.40 ≥ 0.35 → confidence = 0.48 ≥ 0.45 | **⚠ FALSE POSITIVE** |

**Known false positive:** The query "How does cool climate affect acidity?" is a legitimate theory question but is routed as a misconception intervention for MC_COOL_CLIMATE_02. This is a sensitivity trade-off from the R07 STOPWORDS fix — removing `"cool"` and `"climate"` from STOPWORDS was necessary to make detection_keywords functional, but it means `{"cool", "climate"}` appearing together in any query now fires the base bias. No test currently asserts that this query routes to `normal_tutor`, so no test fails. The false positive has a pedagogical silver lining: the Tutor receives the corrected understanding of MC_COOL_CLIMATE_02 and also the CC_COOL_CLIMATE_ACIDITY causal chain in `forced_causal_chains`. However, the routing decision ("misconception detected") is technically incorrect for a neutral theory question.

**These demo queries were NOT run interactively.** Expected results are derived from tracing `_concept_bias()` logic through the detection_keywords of each node.

---

### Step 5 — Causal Chain Retrieval via Orchestrator (LIVE)

**Confirmed LIVE from `knowledge/nazareth/context_packages/latest_context_package.json` (2026-05-15):**

The context package for query "How does cool climate affect acidity?" contains a `forced_causal_chains` array populated with 5 full node objects:

1. CC_BOTRYTIS_ACIDITY_REDUCTION (pre-existing Codex schema — retrieved because botrytis/acidity concept overlap)
2. **CC_COOL_CLIMATE_ACIDITY** (causal_chain_v1 — exact match for query ✓)
3. CC_COOL_CLIMATE_ALCOHOL (causal_chain_v1 — related cool climate topic)
4. CC_COOL_CLIMATE_AROMA (pre-existing Codex schema)
5. CC_WARM_CLIMATE_ALCOHOL (causal_chain_v1 — contrast chain, correctly included)

`forced_causal_chains` field is present and populated. `select_matched_causal_chain_nodes()` is working. Governance fields `safe_for_examiner=false` confirmed on all returned nodes.

The Orchestrator correctly passes matched chains into the context package. ✓

---

### Step 6 — Tutor Causal Chain Rendering (LIVE / PARTIAL)

**Partially confirmed LIVE from `knowledge/nazareth/tutor_outputs/latest_tutor_answer.md` (2026-05-15):**

The most recent tutor output is for query "How do I justify quality in SAT?" — a coaching question that does not match any causal chain's `trigger_keywords`. Section 3 ("Explicación causa → efecto") in that output shows the hardcoded fallback string: `"Cadena: explica primero el mecanismo..."`. This is correct behaviour — no chain matched, fallback triggered, no structured rendering.

**What is NOT confirmed at runtime:** Whether CAUSA/MECANISMO/EFECTO/FORMULACIÓN DE EXAMEN rendering appears in a query that does match a chain. The code for `_render_causal_chain()` is confirmed correct by static inspection (label maps for ES and EN verified, step sorting verified, `sat_relevance` appending verified), and CC_COOL_CLIMATE_ACIDITY is confirmed present in `forced_causal_chains` for the acidity query. However, the actual rendered output for that query is not available in the filesystem — the tutor output files in `knowledge/nazareth/tutor_outputs/` were not written for the acidity query (the latest file is for a different question).

**Structured causal chain rendering has not been observed in a live output file.** It is confirmed correct by code inspection only.

---

### Step 7 — Self-Eval at Hard Strictness, 25 Questions (NOT RUN)

**Result: NOT RUN.** 

The most recent `self_eval_feedback.json` shows `"questions_attempted": 1` at `"strictness": "hard"`. This is a single-question ad hoc run from a previous session, not the full 25-question pass required for this verification step.

The command to run is:

```bash
cd C:\Users\esand\OneDrive\Documents\WSET-AI-System
python -m tools.youtube_transcription.main self-eval --limit 25 --question-type all --strictness hard
```

Post-implementation hard-strictness metrics are **unknown**.

---

### Step 8 — Self-Eval at Brutal Strictness, 25 Questions (NOT RUN)

**Result: NOT RUN.**

The command to run is:

```bash
cd C:\Users\esand\OneDrive\Documents\WSET-AI-System
python -m tools.youtube_transcription.main self-eval --limit 25 --question-type all --strictness brutal
```

Post-implementation brutal-strictness metrics are **unknown**. Comparison against baseline is therefore not possible.

---

### Step 9 — LES Write-Back Verification (LIVE)

**Confirmed LIVE from `knowledge/nazareth/epistemic_state.json`:**

```json
{
  "learner_id": "nazareth",
  "schema_version": "minimal_brain_v2",
  "session_count": 15,
  "known_weak_areas": [
    "causal_chain:flor -> oxygen protection -> biological ageing",
    "retrieval:weak_context_support",
    "fragile:flor -> oxygen protection -> biological ageing",
    "fragile:weak_context_support",
    "causal_chain:cool climate -> acid retention",
    "retrieval:missing_causal_link_support",
    "retrieval:missing_keyword_support",
    "fragile:missing_keyword_support",
    "fragile:missing_causal_link_support"
  ],
  "recent_misconceptions": [],
  "governance": { "safe_for_examiner": false, ... }
}
```

LES write-back is confirmed working. `session_count=15` represents accumulated self-eval runs. `known_weak_areas` is non-empty and accurately reflects the fragile concepts recorded in `self_eval_feedback.json`: flor/biological ageing, missing keyword support, missing causal link support. Deduplication and capping are working — no duplicate entries, count well within MAX_KNOWN_WEAK_AREAS=30.

`schema_version: "minimal_brain_v2"` confirmed. All governance flags `false` confirmed. ✓

---

### Step 10 — Before/After Report Updates

#### Self-Eval Metrics: Baseline vs. Post-Implementation

| Metric | Baseline (brutal, 25q) | Post-implementation |
|---|---|---|
| `missing_causal_link` | 19/25 — **76%** | NOT RUN |
| `unsupported_conclusion` | 17/25 — **68%** | NOT RUN |
| `weak_exam_register` | 9/25 — **36%** | NOT RUN |
| `shallow_retrieval` | 7/25 — **28%** | NOT RUN |
| `shallow_reasoning` | 3/25 — **12%** | NOT RUN |
| Top causal chain failure | `"cause → mechanism → effect"` (14 weighted failures) | NOT RUN |

**No post-implementation self-eval has been run at 25 questions.** The before/after comparison is therefore incomplete. `knowledge/self-eval/before_vs_after_self_eval.md` currently contains projected numbers from Phase F of the implementation; those projections have not been replaced with actuals.

The implementation changes that should drive improvement in post-implementation scores, if and when the self-eval runs:

- 9 causal_chain_v1 nodes provide structured CAUSA/MECANISMO/EFECTO content directly targeting the `"cause → mechanism → effect"` failure (baseline: 14 weighted failures). These chains now reach the Tutor via `forced_causal_chains`.
- `_render_causal_chain()` renders structured steps instead of hardcoded strings for matched queries.
- `select_matched_causal_chain_nodes()` populates `forced_causal_chains` in the Orchestrator context package for detected chain queries.
- LES write-back accumulates weak areas, enabling future routing improvements.

Whether these changes actually reduce the failure rates is an empirical question that requires running the self-eval.

---

### Step 11 — Final Safety Scan (STATIC)

Re-confirmed at close of session:

| Check | Result |
|---|---|
| `safe_for_examiner=true` in Python source | Only in test fixtures and guard conditions — never set to `true` in production paths |
| `safe_for_examiner=true` in knowledge-map JSON | NO MATCHES across all 44 knowledge-map files |
| `official_grading_authority=true` in JSON | NO MATCHES |
| `embeddings_active`, `vector_db_active`, `cloud_services_active` | All `false` in LES governance; all `false` in context packages |
| Hardcoded examiner scoring anywhere | NOT PRESENT |

System is clean. ✓

---

## 3. What Is Confirmed vs. What Is Open

### Confirmed working (LIVE evidence)

- Orchestrator pipeline runs end-to-end
- `forced_causal_chains` field is populated in context packages
- LES write-back (`les_reconciler.reconcile_les_from_feedback()`) works — `session_count=15`, `known_weak_areas` populated
- `schema_version: "minimal_brain_v2"` propagated correctly through LES
- Governance: `safe_for_examiner=false` throughout all runtime artifacts
- Causal chain nodes are reached and included in retrieval context

### Confirmed correct by code inspection (STATIC)

- All 9 causal_chain_v1 nodes are schema-valid
- All 10 misconception nodes with `detection_keywords` are correctly structured
- `_render_causal_chain()` label maps and step rendering logic
- `_concept_bias()` data-driven detection_keywords logic
- `_cause_effect_line()` calls chain renderer first, fallback only on miss
- STOPWORDS fix (removed `"cool"`, `"climate"`, `"wine"`, `"wines"`)
- Test defect fixed — one query string corrected in `test_milestone_1_3.py`
- 48-test suite expected to pass based on static trace

### Not confirmed (NOT RUN)

- Full test suite execution (48 tests)
- Post-implementation self-eval at hard strictness, 25 questions
- Post-implementation self-eval at brutal strictness, 25 questions
- Interactive demo query routing (misconception detection, causal chain rendering in tutor output)
- Structured CAUSA/MECANISMO/EFECTO rendering observed in a live tutor output file

---

## 4. Known Issues

### Issue 1 — False Positive Misconception Detection (Low severity, no test failure)

**Query:** "How does cool climate affect acidity?"  
**Route assigned:** `misconception_intervention` for MC_COOL_CLIMATE_02  
**Correct route:** `normal_tutor` (theory question, no misconception present)

**Cause:** The `{"tokens": ["cool", "climate"], "require_all": true, "bias": 0.18}` rule in MC_COOL_CLIMATE_02 fires for any query containing both "cool" and "climate". After the R07 STOPWORDS fix, these tokens are no longer filtered, so any theory question about cool-climate topics crosses the detection threshold.

**Impact:** The Tutor receives MC_COOL_CLIMATE_02's corrected understanding AND CC_COOL_CLIMATE_ACIDITY in `forced_causal_chains`. The pedagogical content is broadly appropriate, but the framing ("misconception detected") is wrong. A learner who asked a neutral theory question would receive a misconception correction they did not need.

**Resolution path (not implemented):** A negation filter — if the query contains both `"cool"/"climate"` and `"acidity"/"affect"/"explain"/"how"`, it is more likely a theory question than a misconception signal. This requires either a negative detection rule or a two-stage intent classifier. Deferred.

### Issue 2 — Pre-Existing Causal Chain Nodes Produce No Structured Rendering

The 15 pre-existing Codex-schema nodes (`chain_id`, `starting_factor`, `intermediate_steps`, `final_outcome`) do not produce CAUSA/MECANISMO/EFECTO rendering because they have no `steps` field. `_render_causal_chain()` returns `""` for them; `_cause_effect_line()` falls through to the hardcoded keyword dispatch.

This is not a regression. These nodes were never structured for causal chain rendering. The 9 new causal_chain_v1 nodes cover the highest-weighted self-eval failures. The 15 old nodes continue to provide correct reference content through the chunk retrieval path.

### Issue 3 — CC_OXIDATIVE_AGEING Node Missing

The baseline self-eval identified `"no flor → oxidative ageing"` as a weighted failure (1 failure). The `CC_FLOR_BIOLOGICAL_AGEING` node covers the onset of biological ageing under flor; the oxidative continuation when flor dies is not covered by any causal_chain_v1 node. A `CC_OXIDATIVE_AGEING` node would close this gap.

### Issue 4 — `known_weak_areas` Not Yet Used in Orchestrator Routing

LES is written correctly and `known_weak_areas` contains meaningful causal chain and retrieval gaps. However, the Orchestrator does not currently use `known_weak_areas` to force chain retrieval for relevant queries. This is Milestone 4 scope, explicitly deferred. The data is there; the routing logic is not.

---

## 5. Baseline Self-Eval Results (Pre-Implementation, Brutal Strictness)

For reference when post-implementation scores become available:

```
Strictness: brutal | Questions attempted: 25
most common failure labels:
  missing_causal_link:    19 (76%)
  unsupported_conclusion: 17 (68%)
  weak_exam_register:      9 (36%)
  shallow_retrieval:       7 (28%)
  shallow_reasoning:       3 (12%)
top causal chain failures:
  "cause -> mechanism -> effect":                    14 weighted failures
  "flor -> oxygen protection -> biological ageing":   1
  "fortification -> yeast stops -> residual sugar":   1
  "structure -> bottle ageing -> sediment":           1
  "fractional blending -> consistency":               1
  "no flor -> oxidative ageing":                      1
top retrieval weaknesses:
  missing_causal_link_support: 19
  shallow_retrieval:            7
  missing_keyword_support:      5
```

---

## 6. Frontend Readiness

**Frontend should wait.** Backend verification is incomplete in two material respects:

First, the test suite has not been executed. Static analysis gives high confidence but is not a substitute for a green test run. A failing test could indicate a runtime environment issue, import error, or path dependency that static analysis would miss.

Second, post-implementation self-eval metrics are unknown. The primary objective of Milestones 1–3 was to reduce `missing_causal_link` and `unsupported_conclusion` failure rates by providing structured causal chain content through the Tutor. Whether that objective is achieved is not yet known.

The pipeline is confirmed operational at the infrastructure level (Orchestrator runs, LES writes, chains are retrieved). But quality improvement cannot be asserted without the self-eval data.

---

## 7. Recommended Next Steps (Priority Order)

1. **Run the test suite locally** — `python -m unittest discover -s tests -v`. Confirm 48/48. If any failures, start with `test_causal_chains_present_in_context_package`.

2. **Run a causal chain demo query interactively** — e.g., "Why does flor protect Sherry from oxidation?" — and inspect the tutor output in `knowledge/nazareth/tutor_outputs/`. Confirm that CAUSA/MECANISMO/EFECTO/FORMULACIÓN DE EXAMEN labels appear in the rendered answer. This is the one live verification that static analysis cannot substitute for.

3. **Run self-eval at hard strictness, 25 questions** — `python -m tools.youtube_transcription.main self-eval --limit 25 --question-type all --strictness hard`. Check `epistemic_state.json` afterward.

4. **Run self-eval at brutal strictness, 25 questions** — compare `missing_causal_link` and `unsupported_conclusion` against the baseline (76% and 68% respectively). Replace projections in `knowledge/self-eval/before_vs_after_self_eval.md` with actuals.

5. **Milestone 4, Phase A — Wire `known_weak_areas` into Orchestrator routing** — when a causal chain weakness is recorded in LES, force that chain into retrieval for relevant queries. The LES data is ready; the routing decision point needs a new branch.

6. **Add `CC_OXIDATIVE_AGEING` node** — closes the one remaining identified causal chain gap from the baseline self-eval.

7. **Address MC_COOL_CLIMATE_02 false positive** — add a negative intent pattern or raise the detection threshold for queries that contain explicit theory-question framing alongside "cool"/"climate".

---

## 8. Files Modified in This Stabilisation Pass

| File | Change |
|---|---|
| `tests/test_milestone_1_3.py` | Fixed `test_detection_keywords_require_all_false_partial_match` query string: `"the wine is very oaky"` → `"the wine has oak influence"` |
| `docs/stabilisation_report_milestone_1_3.md` | New file — static code review report (produced this session) |
| `docs/backend_stabilisation_runtime_report.md` | This file |

All other files verified by inspection. No other changes required or made.

---

*Generated: 2026-05-16 | Runtime Verification Report | Milestones 1–3*  
*Not an official WSET document. Not for learner-facing use.*  
*Verification tier: LIVE (filesystem artifacts from 2026-05-15) + STATIC (code inspection). Test suite NOT RUN. Self-eval at 25q NOT RUN.*

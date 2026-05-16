# Technical Risk Register — Post Minimal Brain v4
## WSET-AI-System — Architecture Risk Assessment

**Author:** Claude (Cowork) — Architecture Review Role
**Date:** 2026-05-15
**Input:** Full code inspection, self-eval output, implementation_review_minimal_brain.md findings
**Scope:** All identified technical risks from the v1–v4 implementation series
**Risk scoring:** Severity × Likelihood = Exposure (1–5 scale each; Exposure = product, max 25)

---

## Risk Register Summary

| ID | Risk Title | Severity | Likelihood | Exposure | Status |
|---|---|---|---|---|---|
| R01 | LES never written back | 5 | 5 | 25 | **Active** |
| R02 | `_concept_bias()` hardcodes node IDs | 4 | 5 | 20 | **Active** |
| R03 | Self-eval disconnected from Orchestrator | 4 | 5 | 20 | **Active** |
| R04 | Tutor synthesis is keyword dispatch | 4 | 4 | 16 | **Active** |
| R05 | Only 3 of 10 misconception nodes | 3 | 5 | 15 | **Active** |
| R06 | Schema version divergence (v1/v2) | 2 | 4 | 8 | **Latent** |
| R07 | STOPWORDS removes domain-critical tokens | 3 | 3 | 9 | **Active** |
| R08 | `requires_human_review: True` on all official chunks | 3 | 2 | 6 | **Managed** |
| R09 | `test_retrieved_context_is_used` tests label not content | 3 | 5 | 15 | **Active** |
| R10 | `brutal` strictness miscalibrated for production | 2 | 3 | 6 | **Latent** |
| R11 | No causal chain nodes in knowledge graph | 4 | 5 | 20 | **Active** |
| R12 | Self-eval and LES describe same learner, never reconciled | 3 | 4 | 12 | **Active** |
| R13 | Misconception detection signals too literal | 3 | 4 | 12 | **Active** |
| R14 | Orchestrator planning cycle at Phase 2 of 5 | 4 | 4 | 16 | **Active** |
| R15 | Golden chunk boost hardcoded in retrieval sandbox | 2 | 3 | 6 | **Latent** |

---

## Risk Details

---

### R01 — LES Never Written Back

**Severity:** 5 (system-level failure)
**Likelihood:** 5 (certainty — no write path exists)
**Exposure:** 25

**Description:**
The Learner Epistemic State (`knowledge/nazareth/epistemic_state.json`) is read at the start of every Orchestrator call and its fields are passed downstream in the context package. It is never written to by any automated process. `session_count` is 0. `known_weak_areas` is empty. `recent_misconceptions` is empty. This is true after 25 self-eval questions that identified 19 instances of `missing_causal_link` and 17 instances of `unsupported_conclusion`.

The `evaluation_reporter.py` deliberately avoids writing to the LES: `"note": "Tutor-development simulation only; does not overwrite real LES."` This caution was correct early in development. It is now the primary reason the system has zero adaptive capability.

**Impact:**
Every student interaction is processed as if it is the first. The Orchestrator reads an empty LES and routes identically regardless of what has been learned about the student. The adaptive cognitive tutoring architecture described in the 8 design documents does not exist in practice.

**Current mitigations:** None. The LES is read-only in the current implementation.

**Remediation:**
Implement `reconcile_les_from_feedback()` in `tools/self_eval/evaluation_reporter.py` or a new `tools/orchestrator/les_reconciler.py`. Read `self_eval_feedback.json`, extract `fragile_concepts` and `causal_chains_missing`, write to LES. Increment `session_count`. See `next_backend_milestone_recommendation.md`, Milestone 1.

**Blocking:** Yes — this risk blocks all adaptive behavior in the system. Milestones 2 and 3 are less valuable until this is resolved.

---

### R02 — `_concept_bias()` Hardcodes Node IDs

**Severity:** 4 (silent failures as system grows)
**Likelihood:** 5 (certainty — the coupling is in the code today)
**Exposure:** 20

**Description:**
The `_concept_bias()` function in `tools/orchestrator/misconception_prepass.py` contains hardcoded references to `MC_ACIDITY_01`, `MC_TANNIN_01`, and `MC_COOL_CLIMATE_02` by node ID. The bias logic uses token sets that are more expressive than the `detection_signals` in the node files:

```python
if (
    node_id == "MC_ACIDITY_01"
    and {"acid", "acidic", "acidity"} & query_tokens
    and {"quality", "lower", "poor", "unripe"} & query_tokens
):
    bias += 0.24
```

Adding a 4th misconception node file does not give it any detection bias. The developer must also manually update `_concept_bias()`. This coupling is invisible — there is no error, no test failure, and no warning when a node is added without a corresponding bias entry. The new node simply has much lower detection confidence than the original 3.

The primary demo query ("So high acidity means the wine is lower quality?") is detected entirely through this bias, not through signal matching. Without the +0.24 bias, the confidence falls below the 0.45 threshold and no detection fires.

**Impact:**
As the misconception library grows toward 10 nodes, each new node added without a `_concept_bias()` entry is effectively half-functional. The detection will pass for literal signal matches but fail for paraphrase queries — exactly the queries real exam students produce.

**Current mitigations:** None. The three existing nodes happen to work because they were authored alongside their bias entries.

**Remediation:**
Add a `detection_keywords` field to each misconception node JSON. Refactor `_concept_bias()` to iterate loaded nodes, read their `detection_keywords`, and compute bias dynamically. Remove hardcoded node ID references from the Python source. The node file becomes the single source of truth for detection behavior.

**Blocking:** Yes for Milestone 3 — expanding to 10 nodes without this refactoring multiplies the maintenance surface 3.3x.

---

### R03 — Self-Eval Diagnostics Disconnected From Orchestrator

**Severity:** 4 (prevents learning loop from closing)
**Likelihood:** 5 (certainty — no code path connects them)
**Exposure:** 20

**Description:**
`self_eval_feedback.json` contains `orchestrator_recommendations`, a list of actionable directives including:
- "Increase forced causal-chain retrieval for 'cause -> mechanism -> effect' (weighted failures=14)"
- "Improve retrieval plan for 'missing_causal_link_support' (weighted failures=19)"

These recommendations are correct and directly actionable. They are not read by anything. The Orchestrator reads `epistemic_state.json`. The self-eval writes `self_eval_feedback.json`. There is no code path from the second file to the first, and no code path from either file to the Orchestrator's routing decision.

**Impact:**
The self-eval is a correct diagnostic system producing correct output. That output accumulates in a file that nothing reads. The system does not learn from its self-evaluation. The `orchestrator_recommendations` are a letter to a recipient who does not exist yet.

**Current mitigations:** None. The `evaluation_reporter.py` note acknowledges this explicitly.

**Remediation:**
R01 remediation (LES write-back) directly addresses this — `reconcile_les_from_feedback()` is the code path from self-eval output to LES. Once the LES is populated, the Orchestrator reads it. The Orchestrator then needs to be extended to use `known_weak_areas` in routing (see R14 for the planning gap).

---

### R04 — Tutor Synthesis Is Keyword Dispatch

**Severity:** 4 (output quality ceiling is artificial)
**Likelihood:** 4 (every query goes through this path currently)
**Exposure:** 16

**Description:**
`_idea_from_context_item()` in `tools/tutor/answer_builder.py` processes retrieved context chunks by building a `haystack` from their metadata fields, then matching the haystack against keyword patterns to return hardcoded strings:

```python
if "cool climate" in haystack or "slow ripening" in haystack or "acid retention" in haystack:
    return "el clima fresco tiende a ralentizar la maduración y conservar acidity"
```

The returned string is not from the retrieved chunk. It is a hardcoded Spanish sentence written at development time. The chunk's actual text is discarded. The "Ideas usadas del contexto" section in Tutor output contains source labels followed by hardcoded content, giving the appearance of context use while not using context.

`_official_idea_from_text()` is similarly keyword-dispatched on the query itself:

```python
if "cool" in query and "acid" in query:
    return "el material oficial relaciona clima/growing environment con maduración y retención de acidez"
```

**Impact:**
The Tutor cannot produce novel synthesis for queries outside the keyword dispatch patterns. It can correctly answer the ~5 question types it was authored for. For any other query, it falls through to generic fallback strings. The official WSET corpus is indexed and retrieved but its actual text content never reaches the Tutor output.

**Current mitigations:** The keyword dispatch strings are pedagogically correct. The system does not produce wrong answers — it produces limited answers.

**Remediation:**
Milestone 2 (causal chain nodes) partially addresses this for causal queries. Full remediation requires LLM integration reading the actual context package. The current deterministic synthesis is a reasonable placeholder until LLM integration is warranted.

---

### R05 — Only 3 of 10 Misconception Nodes

**Severity:** 3 (coverage gap in primary intervention type)
**Likelihood:** 5 (certainty — 7 nodes are absent)
**Exposure:** 15

**Description:**
The `misconception_cognition_framework.md` document specified 10 exam-destructive misconceptions as the target coverage. The current implementation has MC_ACIDITY_01, MC_TANNIN_01, and MC_COOL_CLIMATE_02. Seven misconceptions that are provably exam-destructive at WSET L3 — including oak = quality, tannin = bitterness (distinct from MC_TANNIN_01's version), alcohol = body = quality, residual sugar = sweetness, complexity = length — have no node representation.

**Impact:**
Students who hold these 7 misconceptions receive standard `answer_normally` routing. The misconception intervention path — the most pedagogically valuable path — is not triggered for 7 of the 10 identified exam failure modes.

**Current mitigations:** The 3 existing nodes cover the most commonly surfaced misconceptions in demo queries.

**Remediation:**
Milestone 3 in `next_backend_milestone_recommendation.md`. 7 new JSON nodes following the existing schema. Requires R02 remediation first to avoid the `_concept_bias()` maintenance trap.

---

### R06 — Schema Version Divergence (LES v1, Staging v2)

**Severity:** 2 (latent — no current failure)
**Likelihood:** 4 (will surface when consistency checking is added)
**Exposure:** 8

**Description:**
`tools/orchestrator/learner_state.py` writes LES files with `schema_version: "minimal_brain_v1"`. `tools/orchestrator/orchestrator.py` writes session staging with `schema_version: "minimal_brain_v2"`. These have diverged. No code currently reads both and compares them. When LES consistency checking, migration logic, or schema validation is added, the version mismatch will create false inconsistency signals.

**Impact:**
Currently zero. Will become a debugging nuisance when schema evolution is managed more carefully.

**Remediation:**
Bump LES `schema_version` to `minimal_brain_v2` in `write_les_defaults()` as part of the R01 LES write-back work. The schema version should be a single constant defined in `learner_state.py` and imported by `orchestrator.py`.

---

### R07 — STOPWORDS Removes Domain-Critical Tokens

**Severity:** 3 (detection quality degraded for core topics)
**Likelihood:** 3 (affects queries about wine, climate, cool conditions)
**Exposure:** 9

**Description:**
The STOPWORDS set in `misconception_prepass.py` includes:

```python
STOPWORDS = {"a", "an", "the", "is", ..., "cool", "climate", "wine", "wines"}
```

`"cool"` and `"climate"` are WSET L3 domain vocabulary. They appear in detection signals for MC_COOL_CLIMATE_02 and in causal chain topics throughout the knowledge graph. Removing them from query tokens reduces the signal token set for cool-climate queries. The `_concept_bias()` function compensates for this in the 3 existing nodes, but the compensation is itself part of the maintenance coupling in R02.

**Impact:**
The query "Does cool climate make wine higher quality?" loses its two most specific tokens before signal matching. Detection must rely more heavily on `_concept_bias()` rather than signal overlap. When `_concept_bias()` is refactored away (R02 remediation), cool-climate detection quality drops if STOPWORDS is not also corrected.

**Remediation:**
Remove `"cool"`, `"climate"`, `"wine"`, and `"wines"` from STOPWORDS. These are not grammatically inert function words. Adjust STOPWORDS to contain only true function words (articles, prepositions, auxiliary verbs).

---

### R08 — `requires_human_review: True` on All Official Chunks

**Severity:** 3 (disclosure obligation, not a quality failure)
**Likelihood:** 2 (risk of using unreviewed content is disclosed in output)
**Exposure:** 6

**Description:**
Every chunk from `official_wset_chunks.py` carries `requires_human_review: True` because no official chunk has passed through a calibration gate. The Tutor uses these chunks in pedagogy while acknowledging they have not been reviewed for accuracy against the exam marking keys.

**Impact:**
If any official chunk contains a transcription error, OCR artifact, or editorial error from the markdown extraction process, it will be retrieved and used in Tutor synthesis without flagging. The disclaimer in Tutor output covers this at the governance level, but the accuracy risk is real.

**Current mitigations:** The Tutor disclaimer (`DISCLAIMER_ES`, `DISCLAIMER_EN`) is appended to all output and is tested. The official corpus extraction process was audited in the Phase 3 system audit.

**Remediation:**
Establish a calibration gate: a human review pass over the `official_wset_chunks.jsonl` file that changes `requires_human_review` to `False` for verified chunks. Until then, the disclosure is appropriate and the risk is managed.

---

### R09 — `test_retrieved_context_is_used` Tests Label, Not Content

**Severity:** 3 (test gives false confidence about synthesis quality)
**Likelihood:** 5 (certainty — the test is checking the wrong thing)
**Exposure:** 15

**Description:**
The test `test_retrieved_context_is_used` in `tests/test_tutor_answer_builder.py` passes when "Ideas usadas del contexto" appears in the Tutor output. This section header is always present regardless of whether actual chunk text was used. The test is testing the presence of a label, not the quality of what follows it.

This means R04 (keyword dispatch masquerading as context synthesis) is invisible to the test suite. The test passes on a system that discards all retrieved chunk text. A developer reading the test results concludes the synthesis is working correctly.

**Impact:**
The test provides false confidence in the synthesis layer. When the system is extended with LLM synthesis or actual chunk text rendering, there is no existing test to catch regressions where synthesis quality degrades back to keyword dispatch.

**Remediation:**
Add a content-aware test:
```python
def test_retrieved_context_content_appears_in_output(self):
    # write a package with a chunk containing unique text
    # assert that unique text (or a paraphrase detectable by token overlap) appears in output
```

This test should fail against the current implementation and pass after LLM integration or causal chain rendering is in place. A failing test that honestly documents a gap is more useful than a passing test that hides it.

---

### R10 — `brutal` Strictness Miscalibrated for Production Assessment

**Severity:** 2 (diagnostic data skewed; not a production risk)
**Likelihood:** 3 (self-eval ran at brutal; production default is hard)
**Exposure:** 6

**Description:**
The self-eval that produced the 19/25 `missing_causal_link` failures ran at `brutal` strictness. `brutal` requires `→` connectors in a context where `→` also appears in Markdown section headers (`## 4. Cadena causa → efecto`). This may produce false negative causal detections — the header contains `→` as a structural character, not a causal connector.

The production default strictness is `hard`. The 76% failure rate at `brutal` does not directly indicate what the failure rate is at `hard`. The diagnostic priorities (`missing_causal_link` first) may be correct, but the magnitude should be verified against `hard` before committing to causal chain remediation as the top priority.

**Impact:**
Low. The causal chain gap is real — the issue is whether it is 76% severe or 40% severe. The remediation (Milestone 2) is correct in either case.

**Remediation:**
Run the 25-question self-eval at `hard` strictness. Compare failure distributions. If `missing_causal_link` drops below 40%, adjust Milestone ordering but not content.

---

### R11 — No Causal Chain Nodes in Knowledge Graph

**Severity:** 4 (fundamental reasoning structure absent)
**Likelihood:** 5 (certainty — the `causal-chains/` directory does not exist)
**Exposure:** 20

**Description:**
The `graph_reasoning_and_pathfinding.md` design document specifies causal chain nodes as a first-class knowledge graph type. The knowledge graph currently has misconception nodes and (presumably) concept nodes. There are no causal chain nodes. There is no `knowledge/knowledge-map/causal-chains/` directory.

The self-eval's dominant failure (`cause -> mechanism -> effect`, 14 weighted failures) is not addressable through retrieval tuning or Tutor template changes — it requires structured causal chain objects that can be passed as typed inputs to the Tutor rendering layer.

**Impact:**
The Tutor cannot produce distinction-level causal reasoning from the current knowledge structure. No amount of retrieval tuning will fix this — the fix requires creating the knowledge objects.

**Remediation:**
Milestone 2 in `next_backend_milestone_recommendation.md`. Create `knowledge/knowledge-map/causal-chains/` and populate with 9 minimum nodes covering the top self-eval failure chains.

---

### R12 — Self-Eval and LES Describe Same Learner With No Reconciliation

**Severity:** 3 (data integrity risk as both files grow)
**Likelihood:** 4 (both files are being updated independently)
**Exposure:** 12

**Description:**
`knowledge/self-eval/self_eval_feedback.json` and `knowledge/nazareth/epistemic_state.json` both describe Nazareth's learning state. The feedback file contains `fragile_concepts`, `causal_chains_missing`, and `top_misconception_risks`. The LES contains `known_weak_areas`, `recent_misconceptions`, and `session_count`. Neither file references the other.

As self-eval runs accumulate, these files will diverge. The feedback file will show 50 failing questions across 10 runs. The LES will still show `session_count: 0` and empty weak areas. Any code that reads the LES to understand the learner will have a different picture than code that reads the feedback file.

**Impact:**
Currently cosmetic — both files are essentially empty. Will become a genuine data integrity problem once the LES is written back (R01 remediation) and the feedback file accumulates real run data.

**Remediation:**
R01 remediation (LES write-back via `reconcile_les_from_feedback()`) is the structural fix. The function creates the code path from feedback to LES, making the LES the canonical learner state and the feedback file the input source.

---

### R13 — Misconception Detection Signals Too Literal

**Severity:** 3 (paraphrase queries will not be detected)
**Likelihood:** 4 (exam students paraphrase misconceptions constantly)
**Exposure:** 12

**Description:**
MC_ACIDITY_01's detection signals:
- "I don't like acidic wines"
- "This wine is too acidic so it must be poor quality"
- "High acidity means it's unripe"

A student asking "doesn't sourness mean the wine is lower grade?" holds the same misconception but matches zero signals. The signals require near-literal matches because they are phrased as complete sentences rather than keyword-level token sets.

**Impact:**
Detection fails for paraphrase queries. The misconception intervention path is not triggered. The student receives standard `answer_normally` routing and the misconception is not corrected.

**Remediation:**
Expand each node's `detection_signals` to include at least 5 paraphrase variants. Add a `detection_keywords` field with the token-level representation used by the refactored `_concept_bias()`. See R02 remediation and Milestone 3 in `next_backend_milestone_recommendation.md`.

---

### R14 — Orchestrator Planning Cycle at Phase 2 of 5

**Severity:** 4 (system cannot do proactive tutoring)
**Likelihood:** 5 (certainty — the 5-phase cycle is not implemented)
**Exposure:** 16 (severity reduced because this is by design, not by failure)

**Description:**
The `strategic_orchestrator_design.md` document specifies a 5-phase cognitive planning cycle:
1. Read LES and derive priority list
2. Classify query enriched with LES context
3. Generate session plan (ordered sequence of pedagogical acts)
4. Direct agents with LES-enriched directives
5. Update LES based on step outcomes

Current implementation: Phase 2 (classify) and Phase 4 (directive). Phase 1 is a read-only stub. Phases 3 and 5 are absent.

The Orchestrator routes, not plans. A student with `known_weak_areas: ["tannin", "MLF"]` receives identical routing to a student with empty weak areas. There is no session agenda, no proactive prioritization, no multi-step sequencing.

**Impact:**
The Orchestrator cannot initiate a tutoring sequence based on what it knows about the learner. It can only respond to student queries. The "strategic brain" design is not yet operational.

**Current mitigations:** This is the intended state at v4. The implementation notes acknowledge this gap. The architecture supports extension to full planning.

**Remediation:**
Phases 3 and 5 cannot be meaningfully implemented until Phase 1 is real — which requires R01 (LES write-back) to be resolved. This is a known dependency, not a failure.

---

### R15 — Golden Chunk Boost Hardcoded in Retrieval Sandbox

**Severity:** 2 (latent maintenance coupling)
**Likelihood:** 3 (requires adding new canonical question-answer pairs)
**Exposure:** 6

**Description:**
`tutor_retrieval_sandbox.py` contains a priority boost mechanism for "golden chunks" — specific chunks that are pre-identified as the most relevant for known question types. This mechanism uses a score multiplier applied when a chunk's metadata matches known query patterns. Adding new canonical question-answer pairs requires updating the boost configuration manually.

**Impact:**
Low. The same class of maintenance coupling as R02 but for retrieval rather than detection. Will produce subtle retrieval quality degradation when new official corpus content is added without corresponding boost configuration updates.

**Remediation:**
Move the boost configuration to a JSON file that can be extended without modifying Python source. Low priority — address after Milestones 1–3.

---

## Risk Heatmap

```
Severity
5 | R01                          |
4 |      R02, R03    R14    R11  |
3 |           R04  R09  R07  R13 R05    R08  |
2 |                     R06  R10  R15   |
1 |                                          |
  |---1---------2---------3---------4---------5--- Likelihood
```

Active critical cluster: R01, R02, R03, R11 — all high severity and certain/near-certain likelihood. These four risks represent the core gap between the architectural design and the current implementation.

---

## Resolved Risks (Not Requiring Action)

**Governance enforcement** — The `safe_for_examiner: False` flag is correctly threaded through every module, test, and output. `_validate_governance()` raises a `ValueError` on violation. The test `test_safe_for_examiner_violation_causes_safe_failure` passes. This governance layer is sound and does not require remediation.

**Context package schema** — The context package produced by `build_context_package()` is well-structured for LLM integration. Every field needed for governed, source-attributed synthesis is present. No restructuring required.

**Tutor/Examiner corpus separation** — The corpora are correctly separated. The official corpus is indexed and retrieved for Tutor use only. No Examiner scoring logic exists. The architectural separation is sound.

---

*Generated: 2026-05-15 | Architecture Review | Based on full code inspection and self-eval output*
*Not an official WSET document. Not for learner-facing use.*

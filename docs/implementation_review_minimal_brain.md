# Implementation Review: Minimal Brain v1–v4
## WSET-AI-System — Post-Implementation Architecture Audit

**Reviewer:** Claude (Cowork) — Architecture Review Role
**Date:** 2026-05-15
**Scope:** tools/orchestrator/, tools/tutor/, tools/retrieval/, tools/self_eval/, knowledge/nazareth/, knowledge/knowledge-map/, knowledge/official-wset/study-guide/official-chunks/, tests/
**Evidence base:** Full code inspection of all implemented modules, live data files, test suite, self-eval output
**Status:** Authoritative internal review — honest assessment, no flattery

---

## Preamble

The Minimal Brain v1–v4 implementation is a genuine engineering achievement. The module separation is correct, governance enforcement is thorough, and the self-eval loop represents a level of system self-awareness that most prototype tutoring systems never reach. These are real accomplishments.

What follows is a brutally honest account of what is not yet working, why, and what it means for the exam preparation goal.

---

## Question 1: Is Minimal Brain v1/v2/v3/v4 coherent with the intended Orchestrator-as-brain architecture?

**Verdict: Partially. The structure is correct; the substance is missing.**

The module hierarchy (orchestrator → retrieval → tutor → self_eval) correctly reflects the intended agent separation described in `agent_role_redefinition.md`. Each module has a well-defined boundary, governance flags are threaded correctly through the stack, and the context package pattern (Orchestrator writes structured directive → Tutor reads it) is a sound implementation of the Orchestrator-as-planner concept.

However, the Orchestrator's behavior does not yet match the cognitive architecture specification. The intended design (Document 2: `strategic_orchestrator_design.md`) specifies a 5-phase cycle:
1. Read LES and derive priority list
2. Classify query enriched with LES context
3. Generate a session plan (an ordered sequence of pedagogical acts)
4. Direct agents with LES-enriched directives
5. Update LES based on step outcomes

What is implemented is a 2-branch routing function: if a misconception is detected, route to `misconception_intervention`; otherwise, route to `answer_normally`. This is Phase 2 (classify) and Phase 4 (directive), with Phase 1 as a read-only stub, and Phases 3 and 5 absent entirely.

The Orchestrator is shaped like a router that calls itself a planner. The architecture supports the evolution to full planning, but calling it a planner now would be inaccurate.

---

## Question 2: Is the Orchestrator actually planning, or still mostly routing?

**Verdict: Routing. Confident verdict.**

Evidence from `orchestrator.py`:

```python
if prepass["detected"]:
    decision = {"route": "misconception_prepass", ...}
    tutor_directive = {"pedagogical_act": "misconception_intervention", ...}
else:
    decision = {"route": "normal_tutor", ...}
    tutor_directive = {"pedagogical_act": "answer_normally", ...}
```

This is a binary branch, not a plan. A plan would be an ordered list of pedagogical acts with success criteria evaluated between steps. The directive today is a single-act object. There is no session agenda, no proactive prioritization, no multi-step sequencing, and no evaluation of step outcomes.

The Orchestrator does read the LES (`build_les_context`) and threads it into the context package. But it does not use the LES to generate priorities. The fields `known_weak_areas` and `recent_misconceptions` are passed downstream for informational purposes but do not affect the routing decision. A student with `known_weak_areas: ["tannin", "MLF"]` receives identical routing behavior to a student with `known_weak_areas: []`.

This is the most important gap between the implementation and the architecture. Everything else is downstream of it.

---

## Question 3: Is the LES being used meaningfully, or just loaded?

**Verdict: Just loaded. The LES does not grow and does not influence decisions.**

The live `epistemic_state.json`:
```json
{
  "schema_version": "minimal_brain_v1",
  "known_weak_areas": [],
  "recent_misconceptions": [],
  "session_count": 0
}
```

The self-eval ran 25 questions with `brutal` strictness. It identified `missing_causal_link` in 19 of 25 responses — a highly consistent signal about a structural weakness in the Tutor's output. None of this diagnostic information was written to the LES. `session_count` remains 0. `known_weak_areas` remains empty.

The `evaluation_reporter.py` deliberately notes: `"note": "Tutor-development simulation only; does not overwrite real LES."` This was a correct cautious decision for early development. It is now the primary constraint preventing the system from being adaptive.

The LES is read at the start of every Orchestrator call and its fields are threaded into the context package. But because the LES never updates, this read always returns the same empty state. The system processes every student interaction as if it is the first.

---

## Question 4: Is misconception detection strong enough for v1?

**Verdict: Functional but architecturally fragile. Detection for the primary demo queries relies on hardcoded bias, not node data.**

There are 3 misconception nodes in `knowledge/knowledge-map/misconceptions/`: MC_ACIDITY_01, MC_TANNIN_01, and MC_COOL_CLIMATE_02. The cognitive architecture documents specified 10 exam-destructive misconceptions. Implementation is at 30% of target coverage.

More significantly: the detection signals in the actual node files are narrow. MC_ACIDITY_01's detection signals are:
- "I don't like acidic wines"
- "This wine is too acidic so it must be poor quality"
- "High acidity means it's unripe"

The primary demo query "So high acidity means the wine is lower quality?" does not match any of these signals through token overlap alone. Detection for this query depends entirely on the hardcoded `_concept_bias()` function:

```python
if (
    node_id == "MC_ACIDITY_01"
    and {"acid", "acidic", "acidity"} & query_tokens
    and {"quality", "lower", "poor", "unripe"} & query_tokens
):
    bias += 0.24
```

This works — but it creates a dangerous coupling. The `_concept_bias()` function contains hardcoded references to `MC_ACIDITY_01`, `MC_TANNIN_01`, and `MC_COOL_CLIMATE_02` by ID. Adding a 4th misconception node does not automatically give it detection bias — a developer must also manually update `_concept_bias()`. This is a maintenance trap that will cause silent detection failures as the node count grows.

The detection signals in the node files should be doing more of the work that `_concept_bias()` is doing. The signals are too narrow and too literal; they need paraphrase coverage.

---

## Question 5: Are context packages properly structured for future LLM-assisted Tutor synthesis?

**Verdict: Yes — this is the strongest component of the implementation.**

The context package schema produced by `build_context_package()` is well-structured for an LLM consumer. It contains:
- `student_query` — the raw student input
- `pedagogical_act` — the Orchestrator's instruction type
- `forced_retrieval_nodes` — nodes that must appear in the response
- `matched_misconception` — full misconception node when detected
- `learner_state_context` — LES snapshot
- `retrieved_context` — ranked list of chunks with source metadata, governance flags, reasoning type, and pedagogical role
- `tutor_directive` — enriched directive including language instruction and source handling rules
- `success_criteria` — what a successful response must achieve
- `governance` — corpus, examiner status, source authority flags

Every chunk in `retrieved_context` carries `safe_for_examiner: False`, `agent_corpus: tutor`, `requires_human_review`, and `source_type` for trust tier identification. An LLM reading this package has everything it needs to produce a governed, source-attributed response.

The source distinction between `official_wset_extracted` chunks and `manual_curated_srt`/`youtube_transcript` chunks is correct and meaningful. When both are present, the package correctly signals which is the authoritative reference and which is pedagogical enrichment.

This component is ready for LLM integration. The package does not need restructuring — it needs population (more misconception nodes, causal chain nodes, broader retrieval corpus).

---

## Question 6: Is official WSET support correctly integrated as Tutor support without becoming Examiner scoring?

**Verdict: Yes — governance is correctly enforced at every layer.**

`official_wset_chunks.py` sets on every chunk:
- `safe_for_examiner: False`
- `official_grading_authority: False`
- `requires_human_review: True`
- `source_trust_tier: 1`
- `agent_corpus: tutor`

These flags are preserved through the retrieval sandbox into the context package. The `_validate_governance()` function in `answer_builder.py` raises a `ValueError` if `safe_for_examiner` or `examiner_scoring_allowed` is truthy. The test suite verifies this with a dedicated test (`test_safe_for_examiner_violation_causes_safe_failure`).

The official corpus is indexed and retrieved for Tutor use only. The answer builder correctly labels official chunks differently from pedagogical chunks in `_source_note()` and `_is_official_source()`.

One note: `requires_human_review: True` on all official chunks is correct — no official chunk has been through the calibration gate — but it means the Tutor is using content it acknowledges has not been reviewed for accuracy. This is acceptable at this development stage as long as the disclosure is present in Tutor output. The Tutor disclaimer (`DISCLAIMER_ES`, `DISCLAIMER_EN`) is present and is tested.

---

## Question 7: Does Tutor Synthesis v4 genuinely use retrieved context, or is it still mostly templated?

**Verdict: Mostly templated. Retrieved context influences structure labels, not content.**

The critical evidence is in `_extract_context_ideas()` and `_idea_from_context_item()`. When a context chunk is processed:

1. Its `text_excerpt`, `why_retrieved`, `reasoning_type`, and `pedagogical_role` are concatenated into a `haystack`
2. The haystack is matched against keyword patterns (`"cool climate" in haystack`, `"tannin" in haystack`, etc.)
3. A hardcoded string is returned based on which pattern matched

Example from `_idea_from_context_item()`:
```python
if "cool climate" in haystack or "slow ripening" in haystack or "acid retention" in haystack:
    return "el clima fresco tiende a ralentizar la maduración y conservar acidity"
```

This string is not from the retrieved chunk. It is a hardcoded Spanish sentence that the keyword match triggers. The actual text of the chunk is discarded. The "Ideas usadas del contexto" section in the Tutor output lists source labels followed by this hardcoded content — giving the appearance of context use while not actually using the context.

The `_official_idea_from_text()` function similarly produces hardcoded strings triggered by query keywords, not by chunk content:
```python
if "cool" in query and "acid" in query:
    return "el material oficial relaciona clima/growing environment con maduración y retención de acidez"
```

This is keyword dispatch wearing a context-synthesis costume. It is not wrong — the hardcoded strings are pedagogically correct — but it is not what "genuinely uses retrieved context" means. An LLM reading the actual chunk text would produce a better synthesis. The current approach is a reasonable deterministic placeholder, but it must not be confused with real retrieval-grounded synthesis.

The test `test_retrieved_context_is_used` passes because it checks for "Ideas usadas del contexto" in the output, not for actual chunk text. This test is testing the label, not the content.

---

## Question 8: Is Self-Eval v2 producing useful cognitive diagnostics?

**Verdict: Yes — the diagnostic categories are correct and the output is actionable, but there is a calibration problem with brutal strictness.**

The self-eval summary from 25 questions (brutal strictness):
- `missing_causal_link`: 19/25 (76%)
- `unsupported_conclusion`: 17/25 (68%)
- `weak_exam_register`: 9/25 (36%)
- `shallow_retrieval`: 7/25 (28%)
- Top priority causal chain: `cause -> mechanism -> effect` (14 weighted failures)

These are genuine signals. The dominant failure pattern — missing causal link — is precisely the distinction-level gap that WSET L3 examiners penalize. If the self-eval is correctly identifying this, it is doing something useful.

However, at `brutal` strictness, `_has_cause_mechanism_effect()` requires:
- At least 1 causal connector (because, therefore, leads to, etc.)
- At least 1 mechanism term (mechanism, maduración, retención, fermentación, etc.)
- At least 1 effect term (therefore, results, frescura, quality, calidad, etc.)

The Tutor's hardcoded output sections use `→` connectors but the mechanism terms are in Spanish (`maduración`, `retención`) and the effect terms are also Spanish (`frescura`). Looking at `_has_cause_mechanism_effect()`, `→` is in the connectors list but may appear in Markdown headers (`## 4. Cadena causa → efecto`) where it is structural, not connective. This could produce false negatives in the causal detection.

The 76% failure rate at brutal strictness warrants recalibration. Running the same 25 questions at `hard` (the production default) would give a more realistic picture of actual tutoring quality.

The most important structural problem: the self-eval output (`self_eval_feedback.json`) identifies 19 weighted failures for `cause -> mechanism -> effect` — but the Orchestrator reads the LES and finds `known_weak_areas: []`. The diagnostic and the planning system are not connected.

---

## Question 9: Are there risks of duplicated structures, stale files, or governance drift?

**Verdict: Yes — three specific risks identified.**

**Risk 1: `_concept_bias()` is a hidden duplicate of node detection logic.**
The misconception nodes define `detection_signals`. The pre-pass is supposed to match those signals. But the most effective detection for the primary queries runs through `_concept_bias()` — hardcoded logic that duplicates and extends what the nodes express. When a new node is added, the developer must update both the node file and the `_concept_bias()` function. The node file is the documented interface; `_concept_bias()` is a hidden implementation that overrides it. This will produce confusion and silent detection failures.

**Risk 2: The LES schema version is `minimal_brain_v1` but the staging schema is `minimal_brain_v2`.**
`learner_state.py` writes LES files with `schema_version: minimal_brain_v1`. `orchestrator.py` writes session staging with `schema_version: minimal_brain_v2`. These versions have diverged. If the LES is ever read and compared to staging for consistency checking, the version mismatch will create false inconsistency signals. No code currently checks this, but the version divergence is a future maintenance hazard.

**Risk 3: Self-eval feedback file and LES are maintained separately with no reconciliation path.**
`self_eval_feedback.json` is written to `knowledge/nazareth/` alongside `epistemic_state.json`. Both describe Nazareth's learning state. Neither references the other. The `orchestrator_recommendations` list in the feedback file contains exactly the kind of data the Orchestrator should use for planning — but there is no code path from feedback to planning. As the self-eval accumulates runs, these files diverge in their picture of the learner, with no mechanism to reconcile them.

---

## Question 10: What is the next highest-leverage implementation milestone?

**Verdict: LES write-back is the dependency unlocking everything else. Causal chain synthesis is the highest-leverage content improvement.**

Two answers, in dependency order:

**Unblock: LES write-back after self-eval.** The self-eval currently produces `self_eval_feedback.json` with correct diagnostic data. A single function that reads this feedback and updates `epistemic_state.json` — incrementing `session_count`, appending identified gaps to `known_weak_areas`, adding flagged misconception IDs to `recent_misconceptions` — would make the LES meaningful. Without this, the system's adaptive capability is zero regardless of what else is built.

**Highest leverage: Causal chain knowledge graph nodes and a rendering layer.** The dominant self-eval failure is `missing_causal_link` (76%). This is not a Tutor prompt problem — it is a retrieval structure problem. The Tutor currently receives a flat list of text excerpts and produces keyword-dispatched content. If the Orchestrator could retrieve a structured causal chain node (e.g., `CC_COOL_CLIMATE_ACIDITY`) and pass it as a typed object to the Tutor, the Tutor could render it as an ordered step sequence (cause → mechanism → effect → exam formulation) rather than a keyword lookup. This directly addresses the dominant failure pattern and does not require LLM integration or embeddings.

---

*Generated: 2026-05-15 | Architecture Review | Based on full code inspection*
*Not an official WSET document. Not for learner-facing use.*

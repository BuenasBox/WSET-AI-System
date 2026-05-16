# Next Backend Milestone Recommendation
## WSET-AI-System — Post-Brain v4 Implementation Roadmap

**Author:** Claude (Cowork) — Architecture Review Role
**Date:** 2026-05-15
**Input:** Full code inspection, self-eval output (25 questions, brutal strictness), implementation_review_minimal_brain.md findings
**Scope:** Ordered recommendation for the next 3 backend milestones, with rationale and dependency analysis
**Status:** Authoritative recommendation — not a wishlist

---

## Preamble

The system has earned its current state. The governance enforcement is correct, the module separation is defensible, and the context package schema is ready for LLM integration. What is missing is adaptive behavior — the ability for the system to change what it does based on what it has learned about the learner.

The 3 milestones below are ordered by dependency. Each one is a prerequisite for the ones after it. Implementing them out of order is possible but produces scaffolding that must be torn down later.

---

## Milestone 1: LES Write-Back After Self-Eval

**Priority: Critical dependency — implement before anything else.**

### What is currently broken

The Learner Epistemic State (`knowledge/nazareth/epistemic_state.json`) has never been written to by any automated process. It contains:

```json
{
  "known_weak_areas": [],
  "recent_misconceptions": [],
  "session_count": 0
}
```

This is the state after 25 self-eval questions, including 19 instances of `missing_causal_link` and 17 instances of `unsupported_conclusion`. The system ran a diagnostic session and wrote the results nowhere useful.

The `evaluation_reporter.py` produces `self_eval_feedback.json` with correct diagnostic data, including `orchestrator_recommendations` and `fragile_concepts`. It explicitly avoids writing to the LES (`"note": "Tutor-development simulation only; does not overwrite real LES"`). This was a correct decision during early development. It is now the primary reason the system has zero adaptive capability.

### What must be built

A single function — call it `reconcile_les_from_feedback()` — that:

1. Reads `self_eval_feedback.json` from `knowledge/self-eval/`
2. Extracts `fragile_concepts`, `causal_chains_missing`, and `orchestrator_recommendations`
3. Appends identified gaps to `known_weak_areas` in the LES (deduplicated)
4. Appends flagged misconception IDs to `recent_misconceptions` (capped at last 10)
5. Increments `session_count` by the number of questions attempted in the feedback run
6. Writes the updated LES back to `knowledge/nazareth/epistemic_state.json`
7. Bumps `schema_version` to `minimal_brain_v2` (aligning with the staging schema)

This function should be callable from `evaluation_reporter.py` as a final step after `write_self_eval_feedback()`, and also as a standalone CLI for manual reconciliation.

### What this unlocks

Once the LES contains real data, everything downstream changes:

- The Orchestrator's `build_les_context()` returns a non-empty state
- The context package carries learner-specific context instead of blank fields
- Future Orchestrator planning (Milestone 3) can prioritize weak areas over arbitrary question order
- The `known_weak_areas` list becomes the actual input to the session agenda

### What it does not unlock yet

LES write-back alone does not make the Orchestrator use weak areas in routing. It makes the data available. The planning layer (Milestone 3) is what reads and acts on it. But you cannot build that until the data is there.

### Governance requirements

- The function must enforce `safe_for_examiner: False` on the written LES
- The function must never write examiner-related fields to the LES
- The function must not modify `governance` block flags in the LES
- A new test: `test_les_writeback_after_self_eval_increments_session_count()`

### Estimated scope

One new function in `tools/self_eval/evaluation_reporter.py` or a new `tools/orchestrator/les_reconciler.py`. Approximately 60–80 lines of code. No new dependencies, no new modules, no embeddings, no API calls. This is not a large piece of work. The reason it has not happened is the deliberate caution flag in the reporter — remove it, replace it with a write call.

---

## Milestone 2: Causal Chain Knowledge Graph Nodes + Tutor Rendering Layer

**Priority: Highest-leverage content improvement — implement immediately after Milestone 1.**

### Why this is the most important content change

The dominant self-eval failure is `missing_causal_link` (19/25 questions, 76%). The self-eval summary names `cause -> mechanism -> effect` as the top failing causal chain with 14 weighted failures. WSET L3 Distinction requires articulating why something is true, not just that it is true. The system is failing at exactly the level that separates a Merit from a Distinction answer.

This is not a prompt problem. It is not a scoring-strictness calibration problem. It is a structural retrieval problem. The Tutor currently receives a flat list of text excerpts and produces keyword-dispatched content through `_idea_from_context_item()`. There is no causal chain object in the knowledge graph for the Tutor to render. There is no structured representation of `cause → mechanism → effect → exam formulation` that can be passed to the Tutor as a typed input.

### What must be built: Part A — Causal Chain Nodes

Create a new node type in `knowledge/knowledge-map/causal-chains/`. Each node represents one complete causal chain relevant to a WSET L3 exam question. The minimum required set, based on self-eval failure data:

**CC_COOL_CLIMATE_ACIDITY** — cause: cool growing environment / mechanism: slow ripening delays sugar accumulation, preserving malic/tartaric acid / effect: high acidity, freshness, lower alcohol / exam formulation: "Cool climates slow ripening, preserving acidity and producing wines with higher acidity, freshness, and lower alcohol levels."

**CC_WARM_CLIMATE_ALCOHOL** — cause: warm growing environment / mechanism: rapid ripening, high sugar accumulation / effect: high alcohol, low acidity, fuller body / exam formulation: "Warm climates accelerate ripening, increasing sugar and thus potential alcohol, producing fuller-bodied wines with lower acidity."

**CC_FLOR_BIOLOGICAL_AGEING** — cause: flor yeast layer / mechanism: oxygen exclusion, acetaldehyde production, yeast autolysis / effect: biological ageing character (almond, bread, low oxidation) / exam formulation: "Flor yeast protects wine from oxygen, producing biological ageing with flavours of almond and bread dough."

**CC_FORTIFICATION_RESIDUAL_SUGAR** — cause: grape spirit addition / mechanism: yeast activity inhibited above ~15-16% ABV / effect: fermentation stops, residual sugar retained / exam formulation: "Fortification raises alcohol to a level that kills yeast, stopping fermentation and retaining residual sugar."

**CC_MLF_TEXTURE** — cause: malolactic fermentation / mechanism: malic acid converted to lactic acid, CO₂ released / effect: reduced acidity, softer texture, possible buttery note / exam formulation: "MLF converts sharp malic acid to softer lactic acid, reducing acidity and adding a creamy texture."

**CC_TANNIN_ASTRINGENCY** — cause: tannin contact with proteins / mechanism: tannin-protein binding, salivary protein precipitation / effect: astringent, drying tactile sensation / exam formulation: "Tannins bind to salivary proteins, causing astringency — a drying, gripping sensation."

**CC_BARREL_AGEING_OAK_CHARACTER** — cause: barrel ageing / mechanism: oxygen ingress through staves, tannin/flavour extraction from oak / effect: vanilla/toast/spice, softer tannins, colour stabilisation / exam formulation: "Barrel ageing imparts vanilla and toast flavours from oak and allows slow oxygen ingress, softening tannins."

**CC_BOTTLE_AGEING_SEDIMENT** — cause: extended bottle ageing / mechanism: tannins and pigments polymerise and precipitate / effect: sediment formation, softer tannins, tertiary aromas / exam formulation: "In the bottle, tannins and pigments polymerise over time, forming sediment and producing tertiary aromas."

**CC_FRACTIONAL_BLENDING_CONSISTENCY** — cause: solera fractional blending system / mechanism: older wine in lower butts refreshed with younger wine / effect: consistent house style, no vintage variation / exam formulation: "The solera system blends wine across multiple vintages, producing a consistent non-vintage style."

These 9 chains directly address the top weighted failures from the self-eval. Each node schema:

```json
{
  "node_type": "causal_chain",
  "node_id": "CC_COOL_CLIMATE_ACIDITY",
  "topic": "cool climate and acidity",
  "trigger_keywords": ["cool climate", "cold climate", "high altitude", "acidity", "freshness"],
  "steps": [
    {"step": 1, "label": "cause",      "text": "Cool growing environment"},
    {"step": 2, "label": "mechanism",  "text": "Slow ripening delays sugar accumulation and preserves natural grape acids"},
    {"step": 3, "label": "effect",     "text": "Wines retain higher acidity, freshness, and lower alcohol"},
    {"step": 4, "label": "exam_formulation", "text": "Cool climates slow ripening, preserving acidity and producing wines with higher acidity, freshness, and lower alcohol levels."}
  ],
  "sat_relevance": "use in quality justification when assessing high acidity as a positive structural element",
  "linked_misconceptions": ["MC_COOL_CLIMATE_02"],
  "agent_corpus": "tutor",
  "safe_for_examiner": false,
  "governance": {"safe_for_examiner": false, "examiner_scoring_allowed": false}
}
```

### What must be built: Part B — Retrieval Integration

The retrieval sandbox (`tutor_retrieval_sandbox.py`) already loads knowledge nodes via `load_knowledge_nodes()`. This function reads all JSON files from `knowledge/knowledge-map/` recursively. Adding causal chain nodes to a new subdirectory is enough to make them loadable — no retrieval code changes required for loading.

What does require changes: `score_chunk_for_query()` and the ranking logic. Causal chain nodes must be scored against the query and — when relevant — ranked above standard text chunks. The node's `trigger_keywords` field provides the matching surface. When a query matches ≥2 trigger keywords, the causal chain node should receive a priority boost comparable to the current golden chunk boost.

Add a retrieval field to context packages:

```json
"forced_causal_chains": [
  {
    "node_id": "CC_COOL_CLIMATE_ACIDITY",
    "steps": [...],
    "sat_relevance": "..."
  }
]
```

This field carries the matched causal chain node(s) as typed objects — not keyword-dispatched strings.

### What must be built: Part C — Tutor Rendering Layer

This is the change that eliminates `_idea_from_context_item()`'s keyword dispatch for known causal queries.

Add `_render_causal_chain()` to `answer_builder.py`:

```python
def _render_causal_chain(chain: dict, language: str) -> str:
    steps = chain.get("steps", [])
    lines = []
    for step in steps:
        label = step["label"].upper()
        text = step["text"]
        lines.append(f"**{label}:** {text}")
    return "\n".join(lines)
```

In `_build_misconception_answer()` and `_build_normal_answer()`, check for `forced_causal_chains` in the context package before falling through to `_extract_context_ideas()`. If causal chains are present, render them using `_render_causal_chain()`. The output goes into the "Cadena causa → efecto" section that is already present in the template.

This produces output like:

```
## 4. Cadena causa → efecto

**CAUSE:** Cool growing environment
**MECHANISM:** Slow ripening delays sugar accumulation and preserves natural grape acids
**EFFECT:** Wines retain higher acidity, freshness, and lower alcohol
**EXAM FORMULATION:** Cool climates slow ripening, preserving acidity and producing wines with higher acidity, freshness, and lower alcohol levels.
```

This is a genuine structured causal chain from a knowledge graph node. The self-eval's `_has_cause_mechanism_effect()` would detect this correctly — it contains a mechanism term (`ripening`, `acids`) and an effect term (`freshness`, `alcohol`). The `missing_causal_link` failure rate should drop substantially.

### Expected impact on self-eval metrics

| Metric | Current (brutal) | Expected after Milestone 2 |
|---|---|---|
| `missing_causal_link` | 76% (19/25) | < 30% for covered topics |
| `unsupported_conclusion` | 68% | Reduced for causal queries |
| `shallow_retrieval` | 28% | Reduced for node-matched queries |

These are estimates based on the coverage of the 9 chains against the 25 self-eval questions. The chains cover the top weighted failure (`cause -> mechanism -> effect` 14/25) and most of the named failing chains.

### Governance requirements

- Every causal chain node must include `"safe_for_examiner": false` and `"agent_corpus": "tutor"`
- The rendered causal chain in Tutor output must be wrapped in the existing Tutor disclaimer
- The `_validate_governance()` function in `answer_builder.py` must check `forced_causal_chains` governance flags
- A new test: `test_causal_chain_node_rendered_in_tutor_output()`

---

## Milestone 3: Misconception Detection Signal Expansion

**Priority: High — implement after Milestones 1 and 2.**

### The current state

The system has 3 misconception nodes (MC_ACIDITY_01, MC_TANNIN_01, MC_COOL_CLIMATE_02). The `misconception_cognition_framework.md` document specified 10 exam-destructive misconceptions. Coverage is at 30%.

More importantly, the detection signals in the existing nodes are too literal. MC_ACIDITY_01's signals do not match the primary demo query ("So high acidity means the wine is lower quality?") through signal matching alone. Detection depends on `_concept_bias()`, a hardcoded function that must be manually updated when a new node is added.

### What must be built: Part A — 7 New Misconception Nodes

Priority order based on WSET L3 exam destructiveness:

1. **MC_TANNIN_QUALITY_02** — "More tannin = better wine / more age-worthy wine." Corrected: tannin level must be balanced with fruit, acidity, and alcohol. High tannin without structure is a fault.
2. **MC_OAK_QUALITY_01** — "More oak = higher quality." Corrected: oak is a tool, not a quality marker. Excessive oak masks fruit character and is penalised at L3.
3. **MC_ALCOHOL_QUALITY_01** — "Higher alcohol = more body = higher quality." Corrected: alcohol contributes to body but only in balance with other structural elements. Unbalanced high alcohol is a fault.
4. **MC_RESIDUAL_SUGAR_SWEET_01** — "Residual sugar always means the wine is sweet." Corrected: perceived sweetness depends on the balance of sugar against acidity and tannin. A wine with RS can taste dry if acidity is high.
5. **MC_COMPLEXITY_LENGTH_01** — "Complexity and length are the same thing." Corrected: complexity is the range of flavour types simultaneously present; length is the persistence of flavour after swallowing.
6. **MC_AGEING_IMPROVEMENT_01** — "All wines improve with age." Corrected: most wines are made to be consumed young. Only wines with specific structural characteristics (tannin, acid, RS, or specific stylistic choices) benefit from extended cellaring.
7. **MC_COLD_STABILISATION_QUALITY_01** — "Tartrate crystals in white wine mean the wine is poor quality." Corrected: tartrate crystals are a natural byproduct of cold temperatures and have no impact on wine quality or flavour.

Each node follows the existing `mc_acidity_01.json` schema. Detection signals must include at least 5 paraphrase variants of the core misconception, not 3 literal statements.

### What must be built: Part B — Refactor `_concept_bias()` Away From Node IDs

The `_concept_bias()` function in `misconception_prepass.py` must be refactored to read from node files rather than hardcoding node IDs. The approach:

1. Each misconception node gains a `detection_keywords` field — a list of token sets analogous to what `_concept_bias()` currently hardcodes
2. `_concept_bias()` iterates over loaded nodes, reads their `detection_keywords`, and applies token-overlap bias automatically
3. Node IDs are no longer hardcoded in Python — the node file is the single source of truth for detection behavior

This refactoring is not optional. The current approach will cause silent detection failures as node count grows from 3 to 10. Without it, Milestones 3A and the detection expansion produce nodes that technically exist but are not reliably detected.

### What must be built: Part C — Expand Detection Signal Coverage

Each new node's `detection_signals` must be written with paraphrase breadth as the primary criterion. The current signals are surface-literal — they match exact phrases. WSET exam students rephrase misconceptions in every possible way. Each signal list should cover:
- Direct statement of the misconception ("high acidity means lower quality")
- Question form ("doesn't high acidity mean it's low quality?")
- Comparative form ("if it's more acidic, it must be worse, right?")
- Implicit form ("this wine is too sharp, so it probably got a low score")
- Exam answer form ("I would say the high acidity detracts from the quality")

---

## What Not to Do Next

The following items are explicitly deferred until Milestones 1–3 are complete:

**LLM integration** — The context package is ready for LLM synthesis, but there is no point integrating an LLM when the retrieval layer is feeding it keyword-dispatched strings instead of causal chain nodes. Fix the retrieval structure first.

**Embeddings or vector search** — Token overlap retrieval is working. The dominant self-eval failure is not a retrieval precision problem — it is a retrieval structure problem. Causal chain nodes solve the structural problem without embeddings.

**Frontend / learner-facing interface** — The system is not reliable enough for learner-facing use. The LES never writes back, the Tutor synthesis is keyword dispatch, and 76% of answers fail causal link checks at brutal strictness. A frontend would surface a system that cannot yet do what it claims.

**Orchestrator planning (5-phase cycle)** — This is the right long-term target but is blocked by Milestone 1. The planning cycle requires non-empty LES data to prioritize. Build the write-back first, then build the planner.

**Examiner module** — Not appropriate until the Tutor's answer quality clears the causal link bar at hard strictness.

---

## Summary

| Milestone | What it fixes | Dependency | Scope |
|---|---|---|---|
| 1. LES Write-Back | Zero adaptive capability; LES always empty | None — start here | ~80 lines |
| 2. Causal Chain Nodes + Rendering | 76% `missing_causal_link` failure rate | Milestone 1 (for LES to track coverage) | ~300 lines + 9 JSON nodes |
| 3. Misconception Signal Expansion | 30% misconception coverage; `_concept_bias()` coupling | Milestone 2 (tests calibrated) | 7 JSON nodes + refactor |

The system has a sound architecture and a working diagnostic pipeline. The pipeline is not connected to the planner, and the planner is not building plans. Fix the write-back. Add the causal structure. Expand the misconception library. In that order.

---

*Generated: 2026-05-15 | Architecture Review | Based on full code inspection and self-eval output*
*Not an official WSET document. Not for learner-facing use.*

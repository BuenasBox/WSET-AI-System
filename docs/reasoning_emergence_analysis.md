# Reasoning Emergence Analysis
## WSET-AI-System — Phase 1 Audit

**Auditor:** Claude (Cowork) — Full System Audit
**Date:** 2026-05-15
**Methodology:** System architecture review + retrieval sandbox analysis + prompt engineering inspection + knowledge graph design evaluation
**Primary question:** Is this system evolving toward a real reasoning tutor, or is it still only a sophisticated retrieval system?

---

## 1. The Question, Framed Precisely

"Reasoning" in an educational AI tutor means the system can:

1. **Diagnose** what a student believes (not just what they asked)
2. **Trace** a causal explanation step by step, not retrieve a pre-written answer
3. **Adapt** depth and strategy based on what the student already knows
4. **Correct** misconceptions before they harden
5. **Predict** what a student needs next without being asked

None of these require general intelligence. They require a structured knowledge representation + retrieval logic + response generation that is tightly constrained to a domain.

The question is: does this system have the components to do any of these, and are they operational?

---

## 2. What Currently Exists — An Honest Inventory

### A. Retrieval intelligence (partially working)

The retrieval system classifies query intent (9 types), expands queries using domain-specific vocabulary and misconception strings, and — for a subset of topics — activates graph traversal to retrieve causally structured content.

This is **real retrieval intelligence**, not vanilla vector search. The "cool climate → acidity" retrieval run demonstrates that the system can find multiple related causal chains from a single query, matching not just the topic but the mechanism.

What is working: intent classification, query expansion, dictionary boosting, golden chunk boosting, basic graph lookup.

What is not working: misconception pre-pass, cross-region comparison traversal, synthesis (the system retrieves building blocks but does not assemble them into arguments).

### B. Knowledge graph (designed, partially built)

The knowledge graph architecture is well-designed: five node types (topics, concepts, relationships, misconceptions, causal chains), a controlled vocabulary of 15 relationship types, schema validation, and a clear traversal logic. The graph correctly separates definitional knowledge from causal knowledge from misconception correction.

The KNOWLEDGE_GRAPH_ARCHITECTURE.md and retrieval sandbox run_04 confirm that causal chains are operational for approximately 8 concepts (RA1 foundational). This includes malic acid, tartaric acid, cool climate, acidity, MLF, botrytis, lees ageing, and related chains.

What is working: graph schema, concept-to-chain traversal for RA1, distinction notes per chain.

What is not working: regions (RA2), sparkling (RA3), fortified (RA4), wine law (RA5) are not in the graph. Cross-concept relationship edges are sparse. Topic nodes do not yet exist.

### C. Governance and agent architecture (strongest component)

AGENT_BOUNDARIES.md is exceptional. The Tutor/Examiner separation is architecturally sound and epistemologically correct. The trust tier model is rigorous. The calibration gate prevents premature Examiner Agent activation.

The Examiner Agent prompt is well-calibrated: it correctly prioritises precision, BICL support, and cause-effect linkage over encyclopedic breadth. The error taxonomy (14 error labels) is a genuine diagnostic tool.

What is working: conceptual design, governance documentation, agent prompts.

What is not working: Examiner Agent has no corpus, no calibration manifest, and has never actually scored anything.

### D. Pedagogical prompts (operational)

The Tutor Agent prompt encodes a specific pedagogical strategy:

```
Concept → Why it matters → Effect in the wine → How to write it for marks
```

This is a cause-effect teaching frame built into the system prompt. It is operationally correct for WSET L3 Distinction coaching. The prompt is not just instructional text — it specifies output templates that produce structured, teachable responses.

What is working: Tutor Agent is operational and produces pedagogically appropriate responses when given retrieval content.

What is not working: The Tutor Agent currently receives retrieval content from Wine With Jimmy only (official corpus not indexed), meaning its explanations may be pedagogically framed but not always textually grounded in WSET official language.

### E. Learner memory (empty but designed)

The Nazareth system (`knowledge/nazareth/`) is designed to store per-learner weak areas, mock history, study patterns, and distinction feedback. The Orchestrator prompt includes logic for recurring weak area prioritisation:

```
priority = exam_relevance + recurrence + severity + proximity_to_exam - recent_improvement
```

This is a genuine prioritisation model. It would enable adaptive tutoring. But all Nazareth directories are empty — no learner history exists yet.

---

## 3. Assessment Against Reasoning Capability Levels

### Level A — Static semantic retrieval only

The system **exceeds** this level. Query intent classification, misconception-aware expansion, graph traversal, and trust tier filtering are all beyond static semantic retrieval.

**Verdict: Not at this level.**

### Level B — Retrieval + pedagogical orchestration

The system **is at this level**, partially. The Tutor Agent + Orchestrator + retrieval pipeline form a pedagogical orchestration layer. Routing logic exists. Response templates are pedagogically structured. The cause-effect teaching frame is encoded.

**Verdict: Current operational level = late-stage B.**

### Level C — Genuine reasoning tutor

A genuine reasoning tutor would:
- Detect what a student believes before answering (misconception pre-pass — **designed but not operational**)
- Traverse a causal chain and present it step by step with comprehension checks (**designed but not rendered as structured output yet**)
- Adapt depth based on the learner's demonstrated level (**designed in Nazareth + Orchestrator; not operational, no history**)
- Correct before explaining, not after (**pre-pass not running**)
- Synthesise across multiple knowledge sources into a unified argument (**retrieval delivers parts, LLM synthesises — this IS happening, but unstructured**)

**Verdict: The system has the architectural intent of Level C and the tooling to reach it. It is not there yet. Estimated distance from C: 6–12 months of targeted engineering.**

---

## 4. What Is Still Simulated

| Capability | Appears to work | What is actually happening |
|---|---|---|
| Misconception detection | ✅ In query expansion | ❌ Strings in expansion terms, not pre-pass activation |
| Causal chain traversal | ✅ In run_04 results | ⚠️ Retrieval brings the chain; synthesis is LLM-side only |
| Adaptive depth | ✅ In prompt design | ❌ No learner model active to trigger it |
| Cross-region comparison | ✅ In retrieval architecture | ❌ Relationship edges not populated for regions |
| Examiner calibration | ✅ In agent prompt | ❌ No corpus to retrieve from; never executed |
| Knowledge graph boosting | ✅ In run_04 | ⚠️ Only RA1 concepts; other RAs fall back to lexical |

---

## 5. Cognition Emergence Potential — Scoring

| Cognitive capability | Current state | Potential | Gap |
|---|---|---|---|
| Causal explanation | Partial (RA1 only) | High | Graph expansion + synthesis layer |
| Adaptive tutoring | Designed only | High | Learner memory activation |
| Misconception diagnosis | Strings in expansion | High | Pre-pass activation |
| SAT justification logic | Partially lexical | Medium | SAT chain nodes (Phase 7) |
| Exam coaching | Operational via prompt | Medium-High | Distinction notes integration |
| Conceptual decomposition | Via graph for RA1 | High | Graph coverage expansion |
| Multi-step reasoning | Retrieves pieces, LLM synthesises | Medium | Synthesis bridge layer |

---

## 6. The Honest Answer

This system is evolving toward a genuine reasoning tutor. It is not there yet, and it is further away than its documentation might suggest — because the most powerful components (knowledge graph, misconception pre-pass, learner model, Examiner corpus) are either partially built, designed-but-unactivated, or empty.

What makes this system **genuinely promising** is not what is built, but what is designed. The governance architecture, retrieval logic, pedagogical framing, and graph schema are all production-quality thinking about a hard problem. The architectural decisions are correct.

The gap between the documentation and the operational reality is currently wide. Closing that gap, specifically by activating the misconception pre-pass, indexing the official corpus, and expanding the knowledge graph, would produce measurable reasoning improvement without any new architectural work.

The system is not proto-cognition. It is a sophisticated pedagogical retrieval system that is engineered to become a reasoning tutor. The distinction matters: one is an emergent property, the other is a goal requiring sustained engineering.

---

*Generated: 2026-05-15 | Claude (Cowork) — Audit Role*

# Full System Reasoning Audit
## WSET-AI-System — Complete Holistic Assessment

**Auditor:** Claude (Cowork) — Full System Audit
**Date:** 2026-05-15
**Scope:** All system components — corpus, retrieval, knowledge graph, governance, agent architecture, reasoning potential
**Methodology:** Direct file inspection + architecture review + retrieval sandbox analysis + cross-document consistency audit
**Status:** Authoritative internal assessment — requires human validation before acting on recommendations

---

## Part I — System Overview

The WSET-AI-System is a purpose-built AI tutoring and evaluation platform for a specific learner preparing for the WSET Level 3 Award in Wines on 2026-08-08, targeting Distinction. It is not a general-purpose educational AI — it is a tightly scoped system designed around a single domain, a single exam, and a single learner.

This specificity is a strength. It permits a level of governance, calibration, and pedagogical precision that general-purpose systems cannot achieve. It is also a constraint: every architectural choice must be evaluated against its utility for this specific exam, with 85 days remaining.

---

## Part II — Component Inventory and Status

### 2.1 Official WSET Corpus

| Item | Status |
|---|---|
| Study guide extracted | ✅ 46 chapters, ~450k chars |
| Ch.11 extraction failure | ✅ Repaired 2026-05-15 |
| Column-layout OCR artifacts | ⚠️ Systemic — all chapters affected |
| Indexed in retrieval pipeline | ❌ Not yet embedded |
| Specification processed | ❌ Empty (`gitkeep` only) |
| SAT document processed | ❌ Empty |
| Marking keys processed | ❌ Empty |
| Sample papers processed | ❌ Empty |

### 2.2 Pedagogical Corpus (Wine With Jimmy)

| Item | Status |
|---|---|
| Raw transcripts | ✅ Large collection (100+ videos) |
| Cleaned markdown | ✅ Active subset |
| Golden chunk annotations | ✅ 166 golden chunks identified |
| Indexed in retrieval | ✅ 333 chunks active |
| Diploma content tagged | ❌ Not yet separated from L3 |
| Human accuracy review | ❌ Not performed |

### 2.3 Knowledge Graph

| Item | Status |
|---|---|
| Architecture designed | ✅ Excellent documentation |
| Schema defined | ✅ 5 node types, 15 relationship types |
| RA1 concepts built | ✅ ~8 concepts, 17 causal chains (per architecture doc) |
| RA2–RA5 nodes | ❌ Not built |
| Graph active in retrieval | ✅ Confirmed (run_04 graph boost active) |
| Topic nodes | ❌ Not yet created |

### 2.4 Governance Layer

| Item | Status |
|---|---|
| AGENT_BOUNDARIES.md | ✅ Comprehensive, authoritative |
| SEMANTIC_RETRIEVAL_ARCHITECTURE.md | ✅ Detailed, correct |
| Trust tier system | ✅ Defined |
| Calibration gate | ✅ Designed | ❌ Never executed |
| Calibration manifest | ❌ Does not exist |
| Ingestion manifest | ❌ Does not exist |
| Logging infrastructure | ❌ Does not exist |

### 2.5 Agent Prompts

| Item | Status |
|---|---|
| Tutor Agent prompt | ✅ Operational, well-designed |
| Examiner Agent prompt | ✅ Well-designed | ❌ No corpus to retrieve from |
| Orchestrator prompt | ✅ Defined | ❌ Not implemented in code |
| Error taxonomy (14 labels) | ✅ Defined in Examiner prompt |

### 2.6 Learner Memory (Nazareth)

| Item | Status |
|---|---|
| Directory structure created | ✅ Folders exist |
| Per-learner data | ❌ Empty |
| Weak area tracking | ❌ Not activated |
| Mock history | ❌ Empty |

### 2.7 Retrieval Infrastructure

| Item | Status |
|---|---|
| 333 tutor chunks indexed | ✅ Active |
| Dictionary boosting (424 terms) | ✅ Active |
| Intent classification | ✅ Active |
| Query expansion | ✅ Active |
| Graph boosting (RA1) | ✅ Active |
| Misconception pre-pass | ❌ Not operational |
| Examiner corpus | ❌ Empty |

---

## Part III — Semantic Architecture Evaluation

### 3.1 Conceptual Retrieval

**Current capability:** Works for RA1 concepts (acidity, tannin, climate, MLF, botrytis, lees ageing) via graph. Works for SAT and exam strategy topics via lexical/golden chunk boosting. Fails for regions, wine laws, sparkling and fortified wine production details — falls back to lexical.

**Assessment:** Functional for ~20% of curriculum scope. Lexical for the remaining 80%.

### 3.2 Cause-Effect Reasoning

**Current capability:** The retrieval system can retrieve multiple causal chain nodes for a concept-matched query. Run_04 demonstrates three distinct causal chains retrieved for "cool climate → acidity." The content for causal explanation exists. The synthesis into a structured step-by-step response is LLM-dependent — not guaranteed.

**Assessment:** Causal content is available; causal reasoning delivery is inconsistent.

### 3.3 SAT Reasoning

**Current capability:** SAT queries retrieve pedagogical content about SAT structure, BICL, and quality descriptors. The SAT document itself has not been processed. The Examiner Agent's SAT scoring criteria have no retrieval source.

**Assessment:** SAT tutoring is functional. SAT assessment is not calibrated to official standards.

### 3.4 Misconception Correction

**Current capability:** Misconception strings are in query expansion, providing passive matching. Active pre-pass detection is not operational. Corrections may occur coincidentally through retrieved chunk content.

**Assessment:** Passive misconception exposure. No active diagnosis or correction pathway.

### 3.5 Cross-Region Comparison

**Current capability:** No region concept nodes exist. Comparative queries retrieve chunks from region-specific Wine With Jimmy videos via lexical matching. No structured relationship traversal is possible.

**Assessment:** Supported only by coincidental lexical co-occurrence. Not structured comparison.

### 3.6 Hierarchical Understanding

**Current capability:** The topic taxonomy is designed (RA1–RA5 structure) but topic nodes do not exist. The graph has no hierarchical structure yet — only flat concept nodes with lateral chain connections.

**Assessment:** No hierarchical traversal possible. Subject breadth is invisible to the retrieval system.

---

## Part IV — The Brutal Honesty Section

### What this system REALLY is today

**This system is an advanced pedagogical retrieval system with proto-reasoning capability in a narrow domain.**

Let me be specific about what each of those words means:

**Advanced** — The retrieval architecture is genuinely sophisticated. The combination of intent classification, query expansion using domain vocabulary and misconception strings, trust tier filtering, and knowledge graph boosting is not something you find in off-the-shelf RAG setups. This was designed by someone who understands both retrieval engineering and educational theory. It is impressive work.

**Pedagogical retrieval** — Every interaction the Tutor Agent has is retrieval-then-synthesis. It finds relevant chunks, hands them to an LLM with a pedagogically-designed prompt, and the LLM synthesises a response. The intelligence is split: retrieval intelligence is largely in the system; explanatory intelligence is largely in the LLM. This is not a weakness — it is the correct architecture. The goal is not to encode reasoning into the retrieval system but to structure retrieval so well that the LLM's synthesis is always well-supported and correctly framed.

**Proto-reasoning in a narrow domain** — For RA1 foundational concepts, the system does something that approaches reasoning: it retrieves causally structured content, presents it through a cause-effect teaching frame, and can walk a student through a mechanism. For "how does cool climate affect acidity," the system provides a multi-chain, graph-traversal-backed answer that is structurally correct. This is proto-reasoning. It works because the knowledge graph is populated for this narrow domain.

**What it is not:**

It is not a cognitive system. It does not hold beliefs, update models, or generate novel explanations. It retrieves, composes, and presents. When the knowledge graph is populated and the misconception pre-pass is active, the composure will become more principled. But the reasoning is always retrieval-conditioned.

It is not yet adaptive. Without Nazareth active, it does not know who the student is, what they struggled with yesterday, or how close they are to Distinction. It tutors the same way for every query. This is the most important gap from an educational effectiveness standpoint.

It is not calibrated. The Examiner Agent has no corpus. Every score it produces today is based on the LLM's pre-trained knowledge of WSET standards, not on official marking key retrieval. The governance framework is designed to prevent this from being presented as calibrated assessment — but if a user activates the Examiner Agent and asks for a score, they receive an uncalibrated estimate framed with official-looking structure.

### What is genuinely impressive

1. The governance architecture. AGENT_BOUNDARIES.md is production-quality thinking. The trust tier model, calibration gate, scoring authority ladder, and agent separation rules are all correct and comprehensive. Few educational AI systems think this carefully about epistemological provenance.

2. The knowledge graph design. The five-node architecture with 15 relationship types, causal chain step structures, distinction notes, and misconception detection signals is a genuine contribution to educational AI design. Most knowledge graphs for tutoring systems are flat taxonomy trees. This one is mechanistically rich.

3. The retrieval intelligence. The combination of intent classification, misconception-aware query expansion, and graph boosting produces retrieval results that are meaningfully better than vanilla semantic search for domain-specific queries.

4. The pedagogical framing. The Tutor Agent prompt's cause-effect teaching template and the Examiner Agent's error taxonomy are not boilerplate. They encode genuine WSET pedagogical expertise into the agent's operating model.

### What is still illusion

1. **Adaptive tutoring** — The system presents as if it knows the student. It does not. Nazareth is empty.

2. **Calibrated assessment** — The Examiner Agent's structured output format creates the impression of official calibration. The calibration manifest does not exist.

3. **Full curriculum coverage** — The retrieval system works impressively for RA1. Queries about the regions of Germany, the solera system in Sherry, or the role of gyropalettes in Champagne production are handled by lexical matching against YouTube transcripts, not by graph-structured causal knowledge.

4. **Misconception correction** — The pre-pass is designed. The misconception nodes exist (for RA1). But the pathway from student input → misconception detection → forced correction retrieval → intervention is not operational.

---

## Part V — Conclusions

### Is this system evolving toward a real reasoning tutor?

**Yes — and the trajectory is credible.**

The system has made the right architectural bets: causal structure over factual lists, misconception correction over passive information delivery, learner memory over stateless sessions, calibrated assessment over simulated scoring. These are the correct design principles for an educational reasoning system.

The current gap is implementation depth, not architectural direction. Every component that would make this a genuine reasoning tutor exists in either implemented or designed form. None of the missing pieces require rethinking the architecture — they require completing the execution.

The five breakthroughs in the strategic roadmap (official corpus activation, misconception pre-pass, structured causal synthesis, learner model, Examiner calibration) do not change the architecture. They complete it.

### The exam is in 85 days

The most important thing the system can do in the next 30 days is:

1. Index the official corpus (so the Tutor speaks in WSET register)
2. Activate the misconception pre-pass (so the Tutor corrects before it explains)
3. Implement structured causal chain synthesis (so the Tutor teaches mechanisms, not facts)

These three changes, achievable without new infrastructure, would produce a measurably better tutoring experience for the specific learner preparing for the specific exam on 2026-08-08.

The governance framework, retrieval architecture, and knowledge graph design are already at a level that supports these activations. The hard thinking has been done. The engineering is straightforward.

---

*This audit reflects the system state as of 2026-05-15.*
*It is a point-in-time assessment. Re-audit recommended after Breakthrough 1 (official corpus activation).*
*Generated by: Claude (Cowork) — Audit Role*
*Not an official WSET document. Not for learner-facing use.*

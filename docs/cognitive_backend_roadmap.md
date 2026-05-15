# Cognitive Backend Roadmap
## WSET-AI-System — Cognitive Architecture Design Series

**Author:** Claude (Cowork) — Cognitive Architecture Designer Role
**Date:** 2026-05-15
**Series position:** 8 of 8 — Implementation sequence for the cognitive architecture designed in Documents 1–7
**Status:** Strategic roadmap — not a sprint plan; effort estimates are approximate; depends on single developer timeline

---

## Framing

The Strategic Architecture Roadmap (existing doc, 2026-05-15) identified 5 engineering breakthroughs ordered by exam-date impact. This document is different in kind. It is a **cognitive capability emergence sequence** — a description of when each reasoning-like behavior becomes possible in the system, and what must be built first.

The existing roadmap asks: "What should we build?" This document asks: "When does the system start being able to do X?" The distinction matters because some capabilities require multiple components to be in place before they emerge. Knowing the dependency order prevents investing in component B before component A — the classical mistake that produces a system with impressive parts that cannot be integrated.

The exam date is 2026-08-08. Today is 2026-05-15. 85 days.

---

## Cognitive Capability Map

The following capabilities are the meaningful educational milestones. Each has a dependency chain.

| Capability | What it means educationally | Dependencies | Estimated availability |
|---|---|---|---|
| C1: Misconception-first tutoring | System corrects before it explains | Misconception pre-pass activated | Phase 1 |
| C2: Structured causal explanations | System explains mechanisms, not just facts | Causal chain rendering layer | Phase 1 |
| C3: Official WSET register | System teaches in WSET language, not YouTube language | Official corpus indexed | Phase 1 |
| C4: Epistemic state awareness | System knows what the student believes | LES schema + write operations | Phase 2 |
| C5: Priority-ranked session planning | System teaches what student needs, not just what they ask | LES + Orchestrator planning | Phase 2 |
| C6: SAT constraint evaluation | System gives structural feedback on SAT quality conclusions | SAT Cognitive Engine | Phase 2 |
| C7: Graph pathfinding | System sequences teaching from prerequisites to targets | Graph traversal + LES intersection | Phase 3 |
| C8: Hardening risk management | System escalates intervention based on misconception persistence | LES misconception registry complete | Phase 3 |
| C9: Calibrated assessment | System scores against official marking keys, not LLM priors | Examiner corpus + calibration gate | Phase 4 |
| C10: Full closed-loop learning | Diagnose → teach → assess → re-teach in a documented chain | All above + Orchestrator integration | Phase 4 |

---

## Phase 1 — Immediate Cognitive Unlocks (Weeks 1–3, before exam)

**Target exam-proximate date: 2026-06-05**

These three capabilities require no new infrastructure and unlock the most exam-relevant educational improvements. They are achievable in parallel.

### 1A — Misconception Pre-Pass Activation (C1)

**What gets built:**
A pre-pass function that runs before every Tutor response. Takes the student's raw input, iterates over all misconception nodes' `detection_signals` arrays, and returns a match result with intervention type if a match is found.

The Tutor Agent prompt is updated to: if pre-pass returns a match, execute the specified intervention using forced retrieval of the misconception node before proceeding with the standard explanation.

**What becomes possible:**
Every session from this point forward actively corrects misconceptions before explaining. The student who says "So high acidity means the wine is harsh?" receives a correction before the explanation of cool climate and acidity — not a response that accidentally includes the correct information which they then reinterpret through the wrong belief.

**Effort:** 2–4 days. String matching function + Tutor prompt update + forced retrieval path.

**Does not require:** LES (pre-pass works against static misconception nodes), embeddings, new infrastructure.

### 1B — Causal Chain Structured Rendering (C2)

**What gets built:**
A response synthesis layer that, when a causal chain node is retrieved (detected by the `CC_` prefix in the node ID), renders the chain's steps explicitly rather than handing them to the LLM as unstructured context.

The rendered structure:
```
Step 1 — [cause]: ...
Step 2 — [mechanism]: ...
Step 3 — [effect in wine]: ...
Step 4 — [exam consequence]: ...
Distinction note: ...
```

This structure is injected into the Tutor's context window as a formatted prompt addition, not as raw chunk text. The LLM synthesises around the structure rather than generating the structure itself.

**What becomes possible:**
Every cause-effect query about an RA1 concept produces a consistently structured, step-labelled explanation that trains the student to think in causal chains — the exact cognitive pattern that WSET examiners reward at Distinction level.

**Effort:** 3–5 days. Chain node parser + rendering layer + Tutor prompt update for structured context handling.

**Does not require:** LES, embeddings, new infrastructure. Works immediately for the 8–17 RA1 concepts currently in the graph.

### 1C — Official WSET Corpus Indexing (C3)

**What gets built:**
The 46 extracted WSET L3 study guide markdown chapters, chunked and embedded alongside the existing Wine With Jimmy corpus. Trust tier metadata: `trust_tier: 1` (official WSET, not marking key).

The Tutor Agent retrieval pipeline updated to include these chunks. Tutor prompt updated with source citation instruction: when official study guide content is retrieved, cite it: "According to the WSET L3 study guide..."

**What becomes possible:**
Tutor explanations draw on official WSET language, not just pedagogical YouTuber language. The register of Tutor explanations shifts toward what examiners expect to see. Students who study exclusively from this system stop learning wine in Jimmy's vocabulary and start learning it in WSET's vocabulary.

**Effort:** 3–5 days. Chunking + embedding (requires embedding pipeline to be running) + retrieval pipeline update.

**Requires:** Column-aware re-extraction recommended for fidelity (addresses OCR artifacts in current markdown), but not blocking — current markdown is usable.

---

## Phase 2 — Epistemic Awareness (Weeks 3–6)

**Target exam-proximate date: 2026-06-26**

These capabilities require the LES infrastructure to be in place before they become possible. Phase 2 cannot precede Phase 1.

### 2A — LES Schema and Write Operations (C4)

**What gets built:**
The LES JSON schema (specified in Document 1) implemented as a file at `knowledge/nazareth/nazareth/epistemic_state.json`. The Orchestrator is updated to perform write operations to the LES after each Examiner session: mapping error taxonomy labels to belief node and misconception registry updates.

An initial LES seeding step populates Nazareth's starting state from any existing session history (if any Examiner sessions have been run) or from a blank-state template.

**What becomes possible:**
The system begins accumulating a record of what Nazareth believes. Each session generates diagnostic data that is preserved in the LES for use in future sessions. The system is no longer stateless.

**Effort:** 5–8 days. Schema implementation + Orchestrator write operations + error taxonomy → LES mapping logic.

### 2B — Priority-Ranked Session Planning (C5)

**What gets built:**
The Orchestrator reads the LES at session start and generates a priority list using the priority formula (Document 2). The Orchestrator presents the top-priority item proactively at session start if it differs from the student's stated query topic.

The proactive opening template: "Before we take your question, I want to work on something I've noticed across our sessions: [priority item]. Let's spend five minutes on this first."

**What becomes possible:**
The system stops being purely reactive to student queries. It pursues its own pedagogical agenda based on accumulated diagnostic data. Students who repeatedly avoid certain topics (common when those topics are associated with difficulty or past failures) are guided back to them. High-hardening-risk misconceptions are addressed before they become correction-resistant.

**Effort:** 4–6 days. Priority formula implementation + Orchestrator planning logic + proactive opening template.

**Depends on:** 2A (LES must have enough data to generate a meaningful priority list; minimum 2–3 Examiner sessions).

### 2C — SAT Cognitive Engine Phase 1 (C6)

**What gets built:**
The BICL Constraint Propagator and Commitment Classifier from Document 4. These two components can be implemented without the full SAT Cognitive Engine and immediately improve SAT feedback quality.

The BICL Constraint Propagator computes the valid quality conclusion range from BICL input and flags conclusions that violate the constraints. The Commitment Classifier identifies `sat_non_commitment` and `bicl_not_supported` structurally (not relying on LLM judgment).

**What becomes possible:**
SAT feedback becomes structurally grounded. The system can tell a student: "Your quality conclusion of 'very good' cannot be supported by your BICL analysis because you rated length as 'short' — outstanding and very good quality conclusions require at least medium finish length. A 'good' or 'acceptable' conclusion would be supported by your evidence." This is precise, actionable, and not dependent on LLM assessment.

**Effort:** 5–7 days. Constraint propagator + commitment classifier + Examiner prompt update to use these components.

---

## Phase 3 — Graph Intelligence (Weeks 6–10)

**Target exam-proximate date: 2026-07-24**

These capabilities require both Phase 1 and Phase 2 to be in place. At this point, with approximately 15 days to exam, the system should be used primarily for targeted drills on the highest-priority gaps identified by the LES, not for broad new content coverage.

### 3A — Knowledge Graph Expansion to RA2–RA5

**What gets built:**
Concept and topic nodes for the 8 major WSET L3 regions, the major sparkling and fortified production methods, and the EU wine law framework. Prerequisite edges between nodes. `contrasts_with` and `often_confused_with` edges between commonly confused concepts.

Priority expansion order (by exam relevance): Bordeaux/Burgundy → Champagne/Germany → Italy/Spain → Fortified (Port/Sherry) → Wine law.

**What becomes possible:**
Graph retrieval works beyond RA1. Comparative teaching ("How does Burgundy's appellation system differ from Bordeaux's?") becomes graph-backed rather than lexically retrieved. Regional queries get the same structured causal support that RA1 queries have had since the beginning.

**Effort:** 8–12 days. High node-building effort; each node requires careful design against WSET L3 specification. The prerequisite edge structure must be pedagogically validated.

### 3B — Orchestrator Pathfinding Integration (C7)

**What gets built:**
The graph traversal functions from Document 5 integrated into the Orchestrator's session planning cycle. When the Orchestrator selects a target concept for teaching, it first runs the prerequisite traversal against the LES and generates a teaching path if prerequisites are unmet.

**What becomes possible:**
The system never attempts to teach a concept whose prerequisites are unknown to the student. Teaching sequences are automatically correct — the graph enforces pedagogical order without the Orchestrator having to manually encode "teach A before B before C."

**Effort:** 4–6 days. Traversal functions + LES intersection + Orchestrator plan generator update.

**Depends on:** 3A (graphs must have RA2–RA5 nodes for pathfinding to be useful beyond RA1).

### 3C — Hardening Risk Management (C8)

**What gets built:**
The hardening risk score formula (Document 3) implemented as a continuous computation on the LES misconception registry. The Orchestrator is updated to check hardening risk thresholds before proceeding with new content: if any misconception has `hardening_risk > 0.6`, new content coverage is suspended until intervention is completed.

**What becomes possible:**
The system actively prevents the worst pedagogical failure mode: loading new correct information on top of unresolved misconceptions. Students who reach the exam with high-hardening-risk misconceptions are the ones who "know so much but still fail" — they have built knowledge on wrong foundations.

**Effort:** 2–3 days. Formula implementation + Orchestrator threshold check + intervention escalation logic.

---

## Phase 4 — Calibrated Assessment and Closed Loop (Post-Exam or Extended Pre-Exam)

**Target date: Post-exam (system evolution) or 2026-07-31 if calibration gate can be completed in time**

### 4A — Examiner Corpus Activation (C9)

**What gets built:**
The WSET official marking keys extracted, chunked, embedded, and indexed in the Examiner corpus with `trust_tier: 0`. The calibration gate checklist completed. `calibration_manifest.json` created and signed off by a WSET-qualified reviewer. The Examiner Agent updated to retrieve from this corpus.

**What becomes possible:**
Examiner scoring is grounded in official marking criteria, not LLM priors. A student's answer can be assessed against "the official marking key states that a Pass answer must demonstrate X, and a Merit answer must demonstrate Y." The mandatory disclosure remains but its severity decreases — the Examiner's outputs are now calibrated, not merely plausible.

**Effort:** 14–21 days. Primarily blocked by the human review step in the calibration gate. Engineering effort alone is 5–7 days.

### 4B — Full Closed-Loop Integration (C10)

**What gets built:**
The complete pipeline: Examiner diagnoses → Orchestrator maps to LES → Orchestrator directs Tutor to address diagnosis → Tutor drills the specific mechanism → Examiner re-evaluates in next session → LES updated with improvement trajectory.

**What becomes possible:**
The system can pursue a documented learning objective across multiple sessions: "Nazareth failed to link high acidity to ageability in session 12. Orchestrator scheduled targeted teaching in session 13. Tutor drilled CC_COOL_CLIMATE_ACIDITY → AGEABILITY_LINK. Session 14 Examiner evaluation shows improvement: `missing_causal_link` absent from this concept." This is a traceable, auditable learning loop.

**Effort:** 5–8 days of integration work, once 4A is in place.

---

## What Changes for Nazareth in Each Phase

| Phase | Nazareth experiences |
|---|---|
| Pre-Phase 1 (today) | Good explanations that may arrive in wrong order, miss active misconceptions, and use YouTube vocabulary |
| After Phase 1 | Misconceptions corrected before explanation; mechanistic explanations; WSET register |
| After Phase 2 | System knows Nazareth's weak areas and pursues them proactively; SAT feedback is structural |
| After Phase 3 | Teaching arrives in correct prerequisite order; misconception escalation prevents knowledge loading on wrong foundations |
| After Phase 4 | Scored feedback is calibrated; learning loops are traceable; the full vision is operational |

---

## What Does NOT Change Across All Phases

- The knowledge graph schema and node architecture — this is already correct
- The governance framework (AGENT_BOUNDARIES.md) — this is already excellent
- The trust tier system — already correct, just needs enforcement
- The agent separation principle — Tutor/Examiner/Orchestrator division is the right architecture
- The pedagogical teaching template — Concept → Why → Effect → Exam formulation is correct for WSET L3

The architecture is right. The implementation depth is the variable.

---

## The Single Most Important Thing for the Exam Date

If only one thing from this roadmap can be completed before 2026-08-08, it should be Phase 1A: **Misconception Pre-Pass Activation.**

This is the change that most directly addresses the failure mode that separates Pass from Distinction in WSET L3 tasting. Students who fail to reach Distinction typically have 3–5 misconceptions that produce structurally wrong answers to otherwise manageable questions. A system that catches those misconceptions every time they appear in student input — and corrects them before providing any new information — removes the root cause of those wrong answers.

Everything else in this roadmap makes the system more intelligent, more adaptive, more precise. But Phase 1A makes the system correct in the way that most directly affects the exam score. That is the right priority.

---

*Generated: 2026-05-15 | Cognitive Architecture Design Series | Document 8 of 8*
*Not an official WSET document. Not for learner-facing use.*
*This series is a design specification. Implementation decisions must be made by the system's engineer, informed by these documents.*

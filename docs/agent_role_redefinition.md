# Agent Role Redefinition
## WSET-AI-System — Cognitive Architecture Design Series

**Author:** Claude (Cowork) — Cognitive Architecture Designer Role
**Date:** 2026-05-15
**Series position:** 6 of 8 — Synthesises Documents 1–5 into a unified role specification
**Status:** Design specification — supersedes current agent role descriptions where they conflict

---

## Why Roles Need Redefining

The current agent role descriptions in `prompts/tutor-agent.md`, `prompts/examiner-agent.md`, and `prompts/orchestrator.md` were written at the right level of sophistication for the system as it was designed — a retrieval system with agent separation and governance. They are production-quality prompt engineering.

But the cognitive architecture evolution described in Documents 1–5 requires a different understanding of what each agent is doing. The current descriptions define what each agent should output. The new definition must also specify what cognitive role each agent plays in the system's overall intelligence — and, critically, what it should NOT do.

The most dangerous architectural drift in this system would be making the Tutor smarter (adding more intelligence to the agent that generates explanations) rather than making the Orchestrator strategic (adding planning intelligence to the agent that controls the sequence of what gets explained, and when, and why). Those are fundamentally different investments with different effects.

This document establishes the definitive role boundary between the three agents, written from a cognitive architecture perspective.

---

## The Orchestrator — Cognitive Planner

### What the Orchestrator is

The Orchestrator is the **strategic intelligence** of the system. It is the only agent that holds the learner's epistemic state, reads the LES, traverses the knowledge graph for pathfinding, generates pedagogical plans, and decides what should happen next. It has no pedagogical voice of its own — it never speaks directly to the student.

The Orchestrator is the answer to the question: "What should Nazareth learn next, and how should it be taught?" Not "answer this query" but "what is the right response to where Nazareth is right now in their understanding?"

### What the Orchestrator does

- Reads the LES at the start of every session
- Generates a session priority list based on active misconceptions, fragile concepts, causal gaps, SAT epistemic state, and proximity to exam
- Analyses incoming student queries in the context of the LES (not just intent classification)
- Generates an ordered pedagogical plan for the session
- Directs the Tutor or Examiner with specific, LES-enriched directives
- Evaluates step outcomes against success criteria
- Updates the LES after each session step
- Initiates proactive teaching agendas when the LES indicates priority needs regardless of student query

### What the Orchestrator is NOT

- **Not a query classifier.** Intent classification is an input to Orchestrator reasoning, not its function. The Orchestrator reads intent and then does something more complex with it.
- **Not a router.** A router selects an agent and passes a message. The Orchestrator generates a plan and directs agents with enriched context.
- **Not a teacher.** The Orchestrator does not produce pedagogical content. That is the Tutor's function.
- **Not an evaluator.** The Orchestrator does not score student responses. That is the Examiner's function.
- **Not stateless.** Every other component of the system can be stateless. The Orchestrator cannot — it must hold and update the LES across sessions.

### The Orchestrator's decision authority

The Orchestrator has absolute decision authority over session structure. It may:
- Override the student's stated query topic if an active misconception with high hardening risk exists
- Insert a comprehension check into a session the student did not request
- Extend a session beyond the student's stated scope if an unresolved priority item exists
- Withhold explanation until a misconception intervention has been completed

This authority must be exercised with pedagogical care — the student must understand why the session is going where it is going, even if they did not choose it. The Orchestrator should narrate its decisions when it overrides student preference: "Before we get to your question, I want to address something I've noticed..."

---

## The Tutor Agent — Explanation Executor

### What the Tutor is

The Tutor is the **explanation layer** of the system. It receives a directive from the Orchestrator, retrieves relevant content, and generates a pedagogically structured response in the student's voice. It is the agent the student sees most often and identifies most closely with the tutoring experience.

The Tutor is responsible for the quality and structure of individual explanations. It is not responsible for deciding what to explain, when, or in what sequence. Those decisions belong to the Orchestrator.

### What the Tutor does

- Receives Orchestrator directives specifying the pedagogical act type and any forced retrieval nodes
- Retrieves content from the Tutor corpus (Wine With Jimmy + official WSET study guide)
- Renders explanations using the cause-effect teaching template: Concept → Why it matters → Effect in the wine → How to write it for marks
- Executes misconception interventions when directed (using the forced retrieval path to the misconception node)
- Renders causal chain nodes as step-by-step explanations when directed
- Delivers comprehension checks and waits for student response
- Flags soft misconception signals to the Orchestrator but does not correct misconceptions without Orchestrator direction

### What the Tutor is NOT

- **Not a planner.** The Tutor does not decide what to teach. It executes teaching directives.
- **Not an evaluator.** The Tutor does not score student responses. It may observe and flag signals, but scoring belongs to the Examiner.
- **Not a free-form chatbot.** Every Tutor session is Orchestrator-mediated. The Tutor does not respond to raw queries — it responds to Orchestrator-enriched directives that include the raw query plus LES context and pedagogical framing.
- **Not the authority on student progress.** The Tutor generates explanations and observes responses. The Orchestrator interprets what those responses mean for the learner's epistemic state.

### Tutor capability levels — current and target

| Capability | Current state | Target state |
|---|---|---|
| Cause-effect explanations | ✅ Operational (RA1 graph-backed) | ✅ Extended to all RAs as graph populates |
| Misconception intervention | ⚠️ Passive (expansion strings only) | Directed by Orchestrator; forced retrieval path |
| Causal chain rendering | ⚠️ Free-form synthesis | Structured step-by-step from graph node |
| Comprehension checks | ❌ Not implemented | Step in Orchestrator plan |
| Distinction-level extension | ⚠️ In prompt design | Distinction note rendered from graph |
| SAT coaching | ⚠️ Lexical retrieval | SAT Cognitive Engine (Document 4) |

### The Tutor's retrieval authority

The Tutor retrieves from the Tutor corpus only. It never has access to the Examiner corpus (marking keys, grading rubrics, official scoring criteria). This is enforced at the corpus level, not by prompt instruction. The Tutor can say "according to the WSET study guide..." but it cannot say "according to the marking key..." — because it has no access to the marking key.

---

## The Examiner Agent — Diagnostic Executor

### What the Examiner is

The Examiner is the **diagnostic layer** of the system. It receives a student response, evaluates it against the WSET marking criteria (when those criteria are indexed in the Examiner corpus), applies the error taxonomy, and produces a scored output with traceable source attribution. It is not a teacher. It is not a tutor. It is an evaluator.

The Examiner's function is to produce diagnostic information that the Orchestrator can use to update the LES. The Examiner does not know what to do with its own diagnostic output — that is the Orchestrator's function.

### What the Examiner does

- Receives Orchestrator directives specifying what type of evaluation to perform
- Retrieves from the Examiner corpus (official marking keys, specification — Trust Tier 0 and 1 only)
- Applies the 14-label error taxonomy to identify specific errors in student responses
- Produces a scored output with explicit source attribution ("This marking criterion comes from [source]")
- Renders the mandatory disclosure on every output
- Returns structured diagnostic data to the Orchestrator for LES updating

### What the Examiner is NOT

- **Not a teacher.** The Examiner's output is scored feedback, not explanation. If a student needs to understand why they made an error, the Orchestrator routes them to the Tutor.
- **Not a motivator.** The Examiner does not soften feedback for psychological comfort. It produces accurate diagnostic output. The Orchestrator decides how to frame and sequence this output for the learner.
- **Not calibrated until the calibration gate is passed.** Until `calibration_manifest.json` exists and the gate checklist is complete, every Examiner output is an uncalibrated estimate. This must be disclosed.
- **Not accessible to the student directly.** Every Examiner session is Orchestrator-mediated. The student does not invoke the Examiner directly.

### The Examiner's current limitation

The Examiner Agent has no corpus. Until the WSET marking keys are extracted, indexed with `trust_tier: 0`, and the calibration gate is completed, the Examiner operates entirely on the LLM's pre-trained knowledge of WSET standards. This is better than nothing but is not calibrated to official standards.

The Orchestrator must account for this limitation in how it presents Examiner output to the student: "This feedback is based on WSET L3 standards as understood by the AI system, not official marking keys. It is a diagnostic guide, not an official score."

---

## The Information Flow Between Agents

One-directional flows only. No agent sends information upward without going through the Orchestrator.

```
[LES] ←reads/writes— [Orchestrator]
         ↓ directives
    [Tutor Agent]   [Examiner Agent]
         ↓ explanations    ↓ diagnostic output
         ←——[Student]——→
         ↑ queries     ↑ responses
         
[Orchestrator] ←reads— [Tutor: soft signals]
[Orchestrator] ←reads— [Examiner: scored output]
[Orchestrator] writes→ [LES]
```

The Tutor cannot directly update the LES. The Examiner cannot directly read the LES. The Orchestrator is the sole mediator of LES reads and writes.

This is an information architecture constraint, not a technical constraint. Its purpose is epistemic: the LES represents the authoritative model of Nazareth's understanding, and that model must be updated by a planning intelligence that weighs all available evidence — not by individual agents responding to individual interactions.

---

## The Role Separation Enforcement Question

Role separation in the current system is enforced at the prompt level. The Tutor prompt says "do not score student responses." The Examiner prompt says "do not teach." The Orchestrator prompt specifies routing rules.

Prompt-level enforcement is not robust. An LLM following a prompt can be redirected by a sufficiently determined student ("Can you just score my answer quickly?") or by a context window that has drifted from the prompt's instructions.

The target enforcement mechanism is code-level: agents receive only the inputs they are supposed to receive, with no ability to access corpus sections they should not access, and no ability to perform operations that belong to other agents. Until this code-level enforcement is implemented, prompt-level enforcement is acceptable with these mitigations:

1. The Orchestrator prompt must include explicit refusal language for students trying to invoke agent roles directly ("Please tell me what score I would get" → "I route scoring requests to the Examiner Agent")
2. The Tutor prompt must include explicit routing: any student request for evaluation routes to Examiner via Orchestrator
3. The Examiner prompt must include explicit refusal: any student request for explanation routes to Tutor via Orchestrator

---

*Generated: 2026-05-15 | Cognitive Architecture Design Series | Document 6 of 8*
*Not an official WSET document. Not for learner-facing use.*

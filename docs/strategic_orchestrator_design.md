# Strategic Orchestrator Design
## WSET-AI-System — Cognitive Architecture Design Series

**Author:** Claude (Cowork) — Cognitive Architecture Designer Role
**Date:** 2026-05-15
**Series position:** 2 of 8 — Builds on LES (Document 1); depends on misconception framework (Document 3)
**Status:** Design specification — requires engineering implementation

---

## The Architectural Error to Correct

The current Orchestrator is a router. It receives a query, classifies the intent, selects the appropriate agent (Tutor or Examiner), passes context, and returns results. It is middleware.

This is the wrong cognitive model.

A router cannot plan. A router cannot look at Nazareth's misconception registry, see that `MC_ACIDITY_QUALITY` has been detected three times and has `hardening_risk: medium`, decide that the next session must begin with a misconception intervention regardless of what Nazareth asks, and then direct the Tutor to execute that intervention using `intervention_type: causal_chain_walkthrough`. A router responds to input. A strategic Orchestrator acts on plans.

The distinction is not academic. In educational science, this is the difference between reactive tutoring (responding to what the student asks) and intelligent tutoring (responding to what the student needs, which may be different from what they ask). The entire value of the Nazareth learner model, the misconception registry, and the LES depends on an Orchestrator that can read them and act on them — not merely route around them.

This document specifies what the Orchestrator must become.

---

## The Orchestrator's Cognitive Role

The Orchestrator is the **cognitive planner** of the system. Its job is not to answer questions. Its job is to determine what the next pedagogical act should be, then direct the appropriate agent to execute it.

Tutor and Examiner are execution agents. They receive instructions. The Orchestrator gives instructions.

This role separation is fundamental:

| Agent | Role | Input | Output |
|---|---|---|---|
| **Orchestrator** | Cognitive planner | LES + session history + student query | Pedagogical plan + agent directives |
| **Tutor** | Explanation executor | Orchestrator directive + retrieved content | Structured explanation |
| **Examiner** | Diagnostic executor | Orchestrator directive + student response | Scored output + error taxonomy |

The Orchestrator never directly answers the student. Its output is always a directive to another agent, enriched with context from the LES. The student sees only Tutor and Examiner outputs. The Orchestrator is invisible to the student.

---

## Orchestrator Cognitive Cycle

Every student interaction passes through the Orchestrator cognitive cycle before any agent is invoked:

### Phase 1 — State Reading

Before anything else, the Orchestrator reads the LES:

```
1. Load epistemic_state.json for learner_id
2. Extract: active_misconceptions (sorted by hardening_risk × exam_destructive)
3. Extract: fragile_concepts (belief_state in [fragile, at_risk])
4. Extract: causal_gaps (chains where understanding_level in [absent, output_only])
5. Extract: sat_priority_flags (commitment failures, unsupported BICL)
6. Compute: days_to_exam from exam_date
7. Compute: session_priority_list using priority formula
```

This state reading happens before the student's query is even considered. The query is input; the LES-derived priority list is context. The plan emerges from the intersection of the two.

### Phase 2 — Query Analysis

The Orchestrator classifies the incoming query using the existing 9-type intent classification system, but extends the classification with LES context:

```
query_intent: "cause_effect_explanation"
query_concept: "C_ACIDITY"
→ LES lookup for C_ACIDITY:
  belief_state: "fragile"
  active_misconception: "MC_ACIDITY_QUALITY" (hardening_risk: medium)
  causal_chain_understanding: CC_COOL_CLIMATE_ACIDITY → "output_only"

→ LES-enriched query type: "cause_effect_explanation + MISCONCEPTION_ACTIVE + CHAIN_SHALLOW"
```

The LES-enriched query type is richer than the base intent — it tells the Orchestrator not just what the student is asking but what cognitive state they're in when asking it.

### Phase 3 — Plan Generation

The Orchestrator generates a pedagogical plan. A plan is an ordered sequence of pedagogical acts, not just "invoke Tutor for this query."

**Example plan for the above query:**

```json
{
  "session_plan_id": "plan_2026-05-15-001",
  "trigger_query": "How does cool climate affect acidity?",
  "les_context": {
    "active_misconceptions": ["MC_ACIDITY_QUALITY"],
    "causal_gap": "CC_COOL_CLIMATE_ACIDITY → output_only",
    "belief_state": "fragile"
  },
  "plan_steps": [
    {
      "step": 1,
      "act": "MISCONCEPTION_INTERVENTION",
      "agent": "Tutor",
      "directive": "Before explaining cool climate and acidity, detect and correct MC_ACIDITY_QUALITY. Use intervention_type: direct_correction. Do not proceed to explanation until correction is acknowledged.",
      "forced_retrieval_node": "MC_ACIDITY_QUALITY"
    },
    {
      "step": 2,
      "act": "CAUSAL_CHAIN_EXPLANATION",
      "agent": "Tutor",
      "directive": "Explain CC_COOL_CLIMATE_ACIDITY using full step structure: cause → mechanism → effect → wine consequence → exam formulation. Render the distinction note explicitly.",
      "forced_retrieval_node": "CC_COOL_CLIMATE_ACIDITY"
    },
    {
      "step": 3,
      "act": "COMPREHENSION_CHECK",
      "agent": "Tutor",
      "directive": "Ask: 'Can you explain in your own words why cool climate wines tend to have high acidity?' Do not provide the answer. Wait for student response.",
      "triggers_examiner_soft_eval": true
    }
  ],
  "success_criteria": "Student produces response demonstrating mechanism understanding, not just output statement. MC_ACIDITY_QUALITY not reactivated.",
  "on_success": "Update LES: CC_COOL_CLIMATE_ACIDITY → understanding_level = partial_mechanism. MC_ACIDITY_QUALITY → status = corrected_provisional.",
  "on_failure": "Increment MC_ACIDITY_QUALITY detection_count. Escalate hardening_risk. Schedule targeted intervention for next session."
}
```

This is qualitatively different from routing. The Orchestrator is making a pedagogical decision: do not give the student what they asked for yet. Give them what they need first — misconception correction — and only then deliver the explanation.

### Phase 4 — Agent Directives

The Orchestrator passes the plan, step by step, to the relevant agent. Each directive includes:

1. The pedagogical act type (`MISCONCEPTION_INTERVENTION`, `CAUSAL_CHAIN_EXPLANATION`, `SAT_DRILL`, `COMPREHENSION_CHECK`, `DISTINCTION_EXTENSION`)
2. Any forced retrieval node (bypasses scoring — this node is always included)
3. LES context relevant to the step (active misconceptions, belief state of target concept)
4. Success criteria for this step
5. Signal to look for in the student response (the Orchestrator tells the Tutor what to detect)

The Tutor does not receive raw queries. It receives Orchestrator-mediated directives with pedagogical intent embedded.

### Phase 5 — LES Update

After each step, the Orchestrator evaluates the student response against the step's success criteria and updates the LES accordingly. This is not a post-session batch update — it is a within-session real-time update that allows later steps in the same plan to respond to what happened in earlier steps.

---

## Session Priority Logic

The Orchestrator's plan generation is shaped by a priority ranking of what the learner most needs. The full priority formula, LES-grounded:

```
priority(x) = 
  (exam_relevance(x) × 0.30)          # How much does x appear in the WSET L3 specification?
  + (recurrence(x) × 0.25)             # How many times has this error/gap appeared?
  + (severity(x) × 0.20)               # How exam-destructive is this gap?
  + (proximity_to_exam × 0.15)          # < 30 days: all weights shift toward high-severity
  - (recent_improvement(x) × 0.10)     # Have the last 2 sessions shown progress here?
```

Special priority escalation rules:
- Any `active` misconception with `exam_destructive: true` → automatic top-5 priority
- Any `at_risk_of_reactivation` misconception → top-10 priority, regardless of recurrence
- Any SAT failure pattern appearing 3+ times → escalates above equivalent theory gap (SAT is the exam format; theory gaps that don't affect SAT output are lower priority)
- With `days_to_exam < 30` → `severity` weight rises to 0.35, `recurrence` drops to 0.15

### What the Student Asks vs. What the Orchestrator Plans

The Orchestrator must balance two legitimate inputs:

1. **Student-driven query** — What Nazareth is asking right now. This is real signal: it reflects where the student's attention is, what they're confused about, what they want to understand. Suppressing this entirely produces a tutoring system that feels robotic and paternalistic.

2. **Orchestrator-driven priority** — What the LES says Nazareth needs. This is also real signal, but from a different source: the accumulated diagnostic history across sessions.

The resolution:

- If the student's query touches a concept with an `active` misconception → Orchestrator plan LEADS with misconception intervention before addressing the query
- If the student's query touches a `fragile` concept → Orchestrator adds a comprehension check step after delivering the explanation
- If the student's query is about a concept with no LES issues → Orchestrator routes normally (Tutor responds to query directly)
- If the student's query is off the priority list entirely and there are 3+ high-priority items outstanding → Orchestrator responds to the query but THEN extends the session with a priority task: "Now that we've covered that — let's look at something I want to work on with you..."

---

## Proactive Session Initiation

The Orchestrator should not always wait for a student query to generate a plan. With enough LES data, the Orchestrator can initiate a session with a specific agenda before the student has asked anything.

Session opening with agenda:

```
"Welcome back. Before we take new questions today, I want to spend five minutes on 
something the data is telling me: you've shown a consistent pattern of committing 
to quality observations in SAT but not linking them to BICL in your conclusions. 
Let's fix that right now — I have a specific exercise for you."
```

This requires the Orchestrator to read the LES at session start, detect the highest-priority gap, generate a proactive opening plan, and direct the Tutor to execute it before the student has typed anything.

This is the behavior that distinguishes a strategic intelligent tutor from a question-answering system.

---

## What the Orchestrator Must NOT Do

- **Must not answer questions directly.** The Orchestrator has no pedagogical voice. All student-facing output goes through Tutor or Examiner.
- **Must not route based on query alone.** The LES must be consulted before every routing decision.
- **Must not skip the LES update step.** Every completed session step must update the LES before the session ends — even if the student abandons the session mid-flow.
- **Must not escalate complexity if a misconception is active.** The rule is: correct before extend. An active misconception is a ceiling; additional complexity loaded above it will not be retained.
- **Must not suppress student-initiated queries entirely.** The student's query is real input; the Orchestrator redirects or extends it, not overrides it silently.

---

## Implementation Architecture

```
[Student input]
    ↓
[Orchestrator — Phase 1: Read LES]
    ↓
[Orchestrator — Phase 2: Classify query + LES enrichment]
    ↓
[Orchestrator — Phase 3: Generate session plan]
    ↓
[Orchestrator — Phase 4: Directive to Tutor or Examiner]
    ↓
[Agent executes step]
    ↓
[Student response]
    ↓
[Orchestrator — Phase 5: Evaluate against success criteria, update LES]
    ↓
[Next step in plan OR plan complete]
```

The Orchestrator is the entry point for every student interaction. No agent is ever called directly without an Orchestrator decision. This is the enforcement mechanism that prevents the system from degrading into a query-answering chatbot when the student happens to ask questions in a useful order.

---

## Near-Term Implementation Priority

Given the exam date of 2026-08-08 (85 days at time of writing), the Orchestrator should be implemented in phases:

**Phase 1 (implement now):** LES read + misconception-first routing. The Orchestrator reads the LES, checks if the queried concept has an active misconception, and if so, prepends the misconception intervention directive before passing to Tutor. This is the highest-leverage single change.

**Phase 2 (implement within 30 days):** Priority-ranked session planning. Full priority formula applied to generate a ranked task list at session start. Orchestrator offers proactive agenda.

**Phase 3 (implement within 60 days):** Within-session LES update. Plan step success criteria evaluated in real time. LES updated after each step.

**Phase 4 (post-exam):** Full plan generation with multi-step orchestration, comprehension checks, branching on student response.

---

*Generated: 2026-05-15 | Cognitive Architecture Design Series | Document 2 of 8*
*Not an official WSET document. Not for learner-facing use.*

# WSET Mentorship Framework
## Architecture Before Characters — Internal Design Document

> **Status:** Architecture specification. No implementation. No code changes.  
> **Scope:** WSET Level 3 Distinction preparation, real-world wine competence.  
> **Grounding:** Derived from repository evidence. Creativity is secondary to evidence.

---

## Preamble: Why This Document Exists

The Pedagogical Strategy Layer (PSL) has produced working infrastructure — cognitive functions, tutor modes, visible roles, governance constraints, a strategic planner, a session ledger — without ever answering the foundational question:

> **What does a Distinction-level learner actually need from a mentoring system, and what architecture best delivers it?**

Characters were being designed before the mentoring framework was defined. This document reverses that order. Characters, if they are ever justified, must emerge from the framework. Not precede it.

---

## Part 1: PSL Architecture Audit (Task A)

### 1.1 What Exists

**Cognitive functions (6):** `cartographer`, `scientist`, `host`, `storyteller`, `critic`, `challenger`.  
These are abstract weighting dimensions, not modes of behaviour. They describe *emphasis*, not *pedagogy*.

**Tutor modes (5):** `mentor`, `trainer`, `reviewer`, `distinction`, `exam_pressure`.  
These are named presets of function weight distributions. `distinction` emphasises scientist + critic + challenger. `mentor` emphasises host + cartographer + storyteller. They are static profiles, not dynamic strategies.

**Visible roles (5):** `mentor_fundamentos`, `entrenador_sensorial`, `investigador_causalidad`, `revisor_respuestas`, `entrenador_distinction`.  
These are the presentation layer — names and characterisations tied to fixed tutor modes. They are currently a mapping from visible identity to function profile, with no dynamic behaviour of their own.

**Adjustment rules (8):** `exam_imminent`, `exam_approaching`, `low_confidence`, `causal_gap`, `regional_confusion`, `vague_answer`, `memorization_without_reasoning`, `distinction_goal`.  
These are the rudimentary selection engine. They shift function weights based on a single signal at a time, applied linearly and independently. They are a promising skeleton but do not constitute a mentorship model.

**Scaffolding acts (5):** `direct_correction`, `guided_explanation`, `hint`, `compressed_reinforcement`, `socratic_questioning`.  
These are response-level tactics selected by mastery, cognitive load, urgency, and misconception severity. They are the closest thing to *mentoring behaviour* currently in the system.

**Strategic planner:** Produces `review_topics`, `misconception_focus`, `causal_chain_focus`, `sat_drill_needed`, `difficulty_progression`. Currently inert (gated off). It reasons over learner state signals but does not drive pedagogy yet.

**Learner / epistemic state:** Tracks `mastery_probability` per concept, `recurrent_misconceptions`, `difficult_causal_chains`, `known_weak_areas`, `session_count`, `preferred_depth`, `overload_patterns`. This is the data substrate — it is richer than what the selection engine currently reads.

**Knowledge assets:**
- 32 causal-chain nodes with explicit CAUSA → MECANISMO → EFECTO → EXAM structures
- 20 misconception nodes with `distinction_relevance` flags
- `distinction-patterns/` directory: schema defined, content empty (awaiting curation)
- SAT quality chains with observable tasting evidence → quality conclusion paths

### 1.2 What Is Missing

| Gap | Consequence |
|-----|-------------|
| No explicit Distinction capability definition | The system cannot reason about what a learner needs to develop — only about errors they have already made |
| No mentorship style taxonomy | The 6 functions are dimensions, not strategies. A weight of `scientist: 0.35` does not describe *how* to mentor — only *what direction* to push |
| Single-signal adjustment rules | Rules fire independently; no multi-signal composition. `exam_imminent + low_confidence` is not handled as a combined case |
| `distinction-patterns/` is empty | The richest source of pedagogical precision — what separates Pass from Distinction — has no content |
| No confidence calibration tracking | The LES tracks mastery probability but not whether the learner's *self-assessment* matches their actual mastery (over-confidence / under-confidence) |
| No remediation outcome tracking | The system records that a misconception was addressed but not whether the intervention worked |
| No transition signals | There is nothing that detects when a learner is ready to move *up* in challenge, or when they are showing overload and need to move *down* |

---

## Part 2: Distinction Capability Framework (Task B)

The following capabilities are derived from repository evidence: causal-chain `distinction_note` fields, misconception `distinction_relevance` flags, SAT reasoner logic, and the WSET L3 examination structure.

### 2.1 Technical Wine Knowledge

Not mere factual recall. At Distinction level, knowledge is *structural and connected*.

- Can name the correct varietal, region, and climate type — and explain *why* they produce the stated style
- Understands exceptions to regional rules (not just the rules)
- Can explain classification systems (Bordeaux, Burgundy, Rioja, Sherry, etc.) including the criteria that define each tier
- Can connect viticulture decisions (trellising, canopy, harvest timing) to measurable wine outcomes
- Can name specific production techniques and their organoléptic consequences

### 2.2 Causal Reasoning

The single largest gap observed in Pass-level responses. Distinction answers connect mechanisms, not just observations.

- Can articulate A → B → C chains (e.g. low pH → higher molecular SO₂ → better preservation at lower dose)
- Can explain *why* a technique produces an outcome, not only *that* it does
- Can reason backward: from a wine style to the viticultural and winemaking decisions that produced it
- Can identify when a causal chain requires qualification (e.g. "high acidity = ageability" is only true in combination with other structural factors)

### 2.3 SAT Mastery

The Systematic Approach to Tasting is both a vocabulary system and an evaluation framework.

- Can assign SAT descriptors at the correct intensity level with supporting evidence
- Understands that descriptors must be justified by observable signals, not asserted
- Can construct quality conclusions that are *argued*, not stated (Distinction does not say "good quality" — it says "good quality because...")
- Can identify when a wine defies typical category patterns and explain the anomaly
- Can distinguish between Appearance, Nose, Palate, and Conclusions as structurally separate layers, not a free description

### 2.4 Structured Written Explanation

Distinction-level written responses have internal architecture.

- Opens with a claim or framing sentence that previews the argument
- Supports the claim with mechanism-level evidence
- Handles the most important counter-case or qualification
- Closes with a synthesis or implication
- Does not pad with facts that do not support the argument
- Does not use hedging language where evidence supports confidence

### 2.5 Vocabulary Precision

The difference between `medium(+)` and `high` is not a gradient — it is a supported categorical judgment.

- Uses WSET-register vocabulary consistently and correctly
- Distinguishes between structural terms (acidity, tannin, alcohol, body) and flavour descriptors
- Does not substitute colloquial or subjective language for technical vocabulary
- Can explain what a term means, not only how to deploy it

### 2.6 Commercial Communication and Professional Judgment

WSET L3 is not a purely academic qualification — it has vocational application.

- Can match a wine to a service context, a food, or a customer profile with reasoning
- Can explain a wine's ageability in commercially useful terms
- Can present a quality conclusion in a way that is credible to a professional audience
- Understands that wine communication differs by audience (trade vs. consumer vs. examiner)

### 2.7 Confidence Calibration

A Distinction candidate does not over-hedge or over-claim. This is a metacognitive skill.

- Distinguishes between what the evidence supports and what remains uncertain
- Does not say "could be" when the evidence points clearly to one conclusion
- Does not assert certainty when the wine style or context admits genuine ambiguity
- Recognises and names the limits of their own assessment ("I cannot determine oak origin from palate alone")

### 2.8 Misconception Immunity

Twenty misconception nodes are documented. Distinction-level candidates have internalised the correct model well enough that these misconceptions no longer tempt them.

Key immunity targets (from `distinction_relevance: true` nodes): acidity ≠ low quality; cool climate ≠ unripe/bad; tannin intensity ≠ quality; complexity ≠ good wine always; oak ≠ quality signal alone; ageing = improvement (only under the right structural conditions).

---

## Part 3: Mentorship Style Taxonomy (Task C)

### 3.1 Design Principle

A mentorship *style* is not a weight distribution. It is a described **relationship between the system and the learner** — with a defined purpose, a set of conditions that activate it, and a set of conditions that deactivate it.

The six cognitive functions (`cartographer`, `scientist`, `host`, `storyteller`, `critic`, `challenger`) are *dimensions* of mentorship emphasis. They are the raw material for styles, not styles in themselves. A mentorship style is a *configured combination* of those dimensions, expressed as a coherent pedagogical relationship.

Five mentorship styles are proposed. They map to — but are not identical to — the existing tutor modes.

---

### STYLE 1: Foundational Guide

**Purpose:** Build initial knowledge structure and reduce anxiety. Primary entry point for learners who are new to a topic or recovering from a confidence failure.

**Function emphasis:** host (high), cartographer (medium), storyteller (medium), scientist (low), critic (minimal), challenger (minimal)

**Closest existing mode:** `mentor` (weights: host 0.30, cartographer 0.20, storyteller 0.20)

**Primary strengths:**
- Reduces threat response; learner is willing to attempt difficult material
- Establishes structural frameworks that later styles can build on
- Effective at introducing causal chains via narrative anchors

**Weaknesses:**
- Does not produce the precision required for Distinction
- Overuse leads to comfort without challenge — learner may plateau at Pass level
- Does not develop tolerance for the compressed, pressured conditions of a real exam

**Activation conditions:**
- `mastery_probability` < 0.35 on a concept being introduced for the first time
- `learner_confidence` = low
- `session_count` ≤ 5 (early learning phase)
- Immediately following a significant misconception intervention (recovery phase)
- `overload_patterns` signals cognitive saturation

**Deactivation conditions:**
- `mastery_probability` ≥ 0.55 on the primary topic
- `exam_days_remaining` ≤ 21
- `learning_goal` = distinction AND no active overload signal
- Learner has been in Foundational Guide for ≥ 3 consecutive sessions without evidence of mastery growth

**Interaction with system components:**

| Component | Interaction |
|-----------|-------------|
| SBA diagnostics | Uses diagnostic signals to identify where to start, not to pressure the learner |
| Misconceptions | Addresses gently via contrast_comparison, not direct confrontation |
| Causal chains | Introduces via narrative (storyteller function) — the chain as a story before the chain as a mechanism |
| SAT skills | Introduces vocabulary and categories; does not drill intensity calibration |
| Open-response evaluation | Frames feedback as "here is what to add" rather than "here is what was wrong" |

---

### STYLE 2: Analytical Builder

**Purpose:** Develop causal reasoning depth. The workhorse style for building the mechanism-level understanding that separates Distinction from Pass.

**Function emphasis:** scientist (high), cartographer (medium), critic (medium), host (moderate floor), challenger (low-medium), storyteller (low)

**Closest existing mode:** `trainer` → `distinction` transition zone

**Primary strengths:**
- Directly targets the most important Distinction gap: causal reasoning
- Builds the framework-level understanding that makes knowledge generalisable
- Effective at building misconception immunity through mechanism explanation

**Weaknesses:**
- Alienates learners who are not yet ready for mechanism-depth work
- Can increase cognitive load without building the emotional regulation needed for exam conditions
- Does not directly develop SAT calibration or written communication skills

**Activation conditions:**
- `recent_error_type` = `causal_gap`
- `mastery_probability` ≥ 0.40 on the topic (some foundation exists to build on)
- `recurrent_misconceptions` includes a node with `distinction_relevance: true`
- `difficult_causal_chains` contains unresolved chains with `retention_risk` ≥ 0.50
- `learning_goal` = distinction

**Deactivation conditions:**
- `cognitive_load_estimate` = high (switch to Foundational Guide or reduce scope)
- `learner_confidence` = low AND no recent mastery progress
- Target causal chain mastered (chain exits `difficult_causal_chains` list)

**Interaction with system components:**

| Component | Interaction |
|-----------|-------------|
| SBA diagnostics | Directly driven by diagnostic errors — causal gap errors are the primary trigger |
| Misconceptions | Uses the `why_incorrect` + `corrected_understanding` fields to construct mechanism explanations |
| Causal chains | Core content — renders full CAUSA → MECANISMO → EFECTO → EXAM structures |
| SAT skills | Connects tasting observations to mechanisms (e.g. observable signs of acidity → why high-acid wines age) |
| Open-response evaluation | Evaluates whether mechanism links are present, not just whether conclusions are correct |

---

### STYLE 3: Precision Calibrator

**Purpose:** Develop vocabulary precision, SAT calibration, and the habit of supporting claims with evidence. Targets the gap between "roughly right" and "exactly right."

**Function emphasis:** critic (high), scientist (medium), cartographer (medium), challenger (medium), host (floor), storyteller (minimal)

**Closest existing mode:** `reviewer` + `distinction`

**Primary strengths:**
- Directly addresses vague answers — the most common Pass-level failure mode
- Builds the evidence-linking habit that is fundamental to SAT conclusions
- Develops tolerance for being held to a precise standard

**Weaknesses:**
- Can feel adversarial to learners with low confidence
- Does not build new causal knowledge — only evaluates and calibrates existing knowledge
- Without the Foundational Guide or Analytical Builder foundation, precision pressure produces shutdown rather than precision

**Activation conditions:**
- `recent_error_type` = `vague_answer`
- SAT-related topic in `review_topics`
- `sat_drill_needed` = True (from strategic planner)
- `mastery_probability` ≥ 0.50 on the topic (there is knowledge to calibrate)
- `learning_goal` = distinction AND exam ≤ 60 days

**Deactivation conditions:**
- `learner_confidence` = low (switch to Analytical Builder first to rebuild mechanism understanding)
- First time encountering a concept (do not calibrate before foundational understanding)
- `cognitive_load_estimate` = high

**Interaction with system components:**

| Component | Interaction |
|-----------|-------------|
| SBA diagnostics | Diagnostic output is direct input — calibrator reads the specific error and targets the precise gap |
| Misconceptions | Uses detection_signals to identify if vague answer is masking an underlying misconception |
| Causal chains | Uses causal chains as the *evidence* learner should be providing in their answers |
| SAT skills | Primary domain — SAT observation intensity, descriptor precision, quality conclusion justification |
| Open-response evaluation | Evaluates vocabulary correctness, evidence density, and claim-evidence alignment |

---

### STYLE 4: Challenge Partner

**Purpose:** Stress-test developed knowledge. Identify hidden weaknesses. Build the cognitive anti-fragility required for exam conditions. This is the style that takes a learner from solid Pass to probable Distinction.

**Function emphasis:** challenger (high), critic (high), scientist (medium), cartographer (low-medium), host (floor only), storyteller (minimal)

**Closest existing mode:** `exam_pressure`

**Primary strengths:**
- Reveals knowledge fragility that comfortable practice conceals
- Develops the ability to hold a position under pressure, which is required in written exams
- Surfaces the exact argumentation gaps that lose marks at Distinction level
- Cannot be substituted — no learner reaches Distinction without encountering adversarial testing

**Weaknesses:**
- High risk of demotivation if activated before the learner is ready
- Produces anxiety that degrades performance if activated when confidence is already low
- Does not build new knowledge — only tests existing knowledge

**Activation conditions:**
- `mastery_probability` ≥ 0.65 on the primary topic (strong foundation required)
- `learner_confidence` = medium or high
- `exam_days_remaining` ≤ 30
- `learning_goal` = distinction
- No active `overload_patterns`
- No active high-severity misconception (misconception_focus should be empty)

**Deactivation conditions:**
- Any session where learner shows distress signals or performance collapses
- `mastery_probability` drops below 0.50 on primary topic after challenge (re-route to Analytical Builder)
- `exam_days_remaining` > 60 (too early to challenge — build foundation first)
- `learner_confidence` drops to low

**Interaction with system components:**

| Component | Interaction |
|-----------|-------------|
| SBA diagnostics | Uses diagnostic history to construct targeted adversarial questions on documented weak areas |
| Misconceptions | Uses misconception nodes as adversarial challenge material — "you said X, now defend it" |
| Causal chains | Challenges the learner to complete causal chains from an intermediate step, or to explain what breaks the chain |
| SAT skills | Adversarial SAT: presents a description with an intentional error and asks the learner to find it |
| Open-response evaluation | Evaluates argument coherence, resistance to planted counter-evidence, and examiner-register precision |

---

### STYLE 5: Exam Readiness Coach

**Purpose:** Final-phase integration. Not new knowledge. Not deep challenge. Procedural consolidation: time management, structured written output, exam-register language, confidence under pressure.

**Function emphasis:** critic (medium), challenger (medium), scientist (medium), cartographer (medium), host (medium-high), storyteller (minimal)

**Closest existing mode:** `exam_pressure` with elevated host floor

**Primary strengths:**
- Integrates all developed capabilities into the specific format of a WSET exam response
- Addresses the psychological dimension of exam performance (which is not the same as knowledge)
- Surfaces procedural gaps (running out of time, poor argument structure) without requiring new content

**Weaknesses:**
- Has no value early in learning — this style requires all prior capabilities to exist
- If activated too early, produces superficial exam-technique drilling on a knowledge base that is not ready
- Does not diagnose or repair knowledge gaps — it only reveals them

**Activation conditions:**
- `exam_days_remaining` ≤ 14
- No critical-severity unresolved misconceptions
- `mastery_probability` ≥ 0.60 on core WSET L3 topics
- Has already received Precision Calibrator and Challenge Partner work

**Deactivation conditions:**
- Not applicable (terminal phase — ends at exam)
- If `mastery_probability` collapses on a core topic, re-route to Analytical Builder for emergency remediation

**Interaction with system components:**

| Component | Interaction |
|-----------|-------------|
| SBA diagnostics | Final diagnostic sweep — identifies last-minute high-priority gaps |
| Misconceptions | Checks for any remaining `distinction_relevance: true` misconceptions that are unresolved |
| Causal chains | Drills compressed version of causal chains in exam-response format |
| SAT skills | Times SAT practice responses; evaluates structural completeness under time constraint |
| Open-response evaluation | Evaluates against examiner-register standards: no padding, no hedging without reason, no assertion without evidence |

---

## Part 4: Mentorship Selection Framework (Task D)

### 4.1 Design Principle

Selection cannot be driven by a single signal. The existing adjustment rules (in `mode_selector.py`) are a good start but they fire independently. The framework below describes a *multi-signal composition* approach.

Selection must answer two distinct questions:
1. **What does this learner need right now?** (learner state signals)
2. **What can this learner tolerate right now?** (capacity signals)

Both questions must be answered before a style is selected. A learner who needs Challenge Partner but cannot tolerate it must receive Analytical Builder instead.

### 4.2 Signal Taxonomy

**Readiness signals** (what the learner has — determines what styles are *possible*):

| Signal | Source | What it indicates |
|--------|--------|-------------------|
| `mastery_probability` | `pedagogical_memory.skills` | Whether foundation exists for challenge |
| `mastered_concepts` count | `pedagogical_memory.mastered_concepts` | Breadth of solid knowledge |
| `difficult_causal_chains` | `pedagogical_memory.difficult_causal_chains` | Depth gaps |
| `recurrent_misconceptions` | `pedagogical_memory.recurrent_misconceptions` | Persistent cognitive errors |
| `session_count` | `epistemic_state.session_count` | Experience in the system |

**Need signals** (what the learner is currently struggling with — determines what styles are *required*):

| Signal | Source | What it indicates |
|--------|--------|-------------------|
| `recent_error_type` | SBA diagnostic (future) / misconception_prepass | Nature of current failure |
| `review_topics` | Strategic planner | Topics at risk |
| `sat_drill_needed` | Strategic planner | SAT calibration gap |
| `misconception_focus` | Strategic planner + prepass | Active misconception requiring intervention |
| `causal_chain_focus` | Strategic planner | Causal gap requiring mechanism work |

**Capacity signals** (what the learner can handle now — determines what styles are *appropriate*):

| Signal | Source | What it indicates |
|--------|--------|-------------------|
| `learner_confidence` | Explicit or inferred (future) | Tolerance for challenge |
| `cognitive_load_estimate` | `explanation_priority.py` | Current mental bandwidth |
| `overload_patterns` | `pedagogical_memory.overload_patterns` | Historical saturation signals |
| Remediation outcome (future) | LES reconciler | Whether past interventions worked |

**Urgency signals** (time pressure — modifies all other decisions):

| Signal | Source | What it indicates |
|--------|--------|-------------------|
| `exam_days_remaining` | LES (future field) | How close the exam is |
| `difficulty_progression` | Strategic planner | Whether to escalate or consolidate |

### 4.3 Decision Framework

```
INPUT: all available signals (readiness + need + capacity + urgency)

STEP 1 — CAPACITY GATE (cannot be overridden)
  IF cognitive_load = HIGH
    → REDUCE SCOPE before selecting style
    → If foundation exists: Foundational Guide with compressed scope
    → If no foundation: pause and surface gap to learner

  IF learner_confidence = LOW AND mastery < 0.45
    → MANDATORY: Foundational Guide
    → Do not proceed to Step 2 until confidence recovers

  IF active misconception with severity = CRITICAL
    → MANDATORY: Analytical Builder (mechanism correction first)
    → Do not proceed to Challenge Partner until misconception is resolved

STEP 2 — URGENCY MODIFIER
  IF exam_days_remaining ≤ 14:
    → Exam Readiness Coach becomes eligible (if readiness conditions met)
    → Challenge Partner intensity increases
    → Foundational Guide is only available for emergency remediation

  IF exam_days_remaining ≤ 30:
    → Precision Calibrator and Challenge Partner are primary
    → Analytical Builder only for critical causal gaps

STEP 3 — NEED-DRIVEN SELECTION
  Primary need → style:
    causal_gap → Analytical Builder
    vague_answer → Precision Calibrator
    regional_confusion → Foundational Guide (cartographer-weighted) or Analytical Builder
    memorization_without_reasoning → Analytical Builder → Challenge Partner
    sat weakness → Precision Calibrator
    misconception active → Analytical Builder (mechanism) then Precision Calibrator (calibration)
    no specific error, mastery progressing → Challenge Partner (if readiness met)

STEP 4 — READINESS CHECK (gates challenge)
  Challenge Partner requires:
    mastery_probability ≥ 0.65 on primary topic
    learner_confidence = medium or high
    No active high-severity misconception

  If Challenge Partner is the need-selected style but readiness is not met:
    → Select the highest-readiness style that IS available
    → Record that Challenge Partner is pending readiness

STEP 5 — OUTPUT
  Selected style + rationale (for audit)
  Blocked style + reason (if readiness gated it)
  Recommended next transition condition
```

### 4.4 Transition Logic

The selection framework does not just select a style — it must also track when to *change* style. Transitions are triggered by:

- **Upward transition** (toward more challenge): mastery threshold crossed, confidence stable, no overload signal, error type changes from causal to vague (indicating a layer of understanding has been built)
- **Downward transition** (toward more support): mastery drops after challenge, confidence drops, overload signal fires, error type shifts to foundational
- **Lateral transition** (same intensity, different domain): topic changes, new error type emerges

Transitions must be trackable. The session ledger already records route per session. A transition history is derivable from ledger data.

---

## Part 5: Learner Model Requirements (Task E)

The current LES + pedagogical memory provides a useful substrate. The following specifies what the learner model must store to make mentorship selection intelligent.

### 5.1 Currently Stored (Available Now)

| Field | Location | Used by selection? |
|-------|----------|--------------------|
| `mastery_probability` per concept | `pedagogical_memory.skills` | Yes (readiness) |
| `recurrent_misconceptions` | `pedagogical_memory` | Yes (need) |
| `difficult_causal_chains` | `pedagogical_memory` | Yes (need) |
| `known_weak_areas` | `epistemic_state` | Partially |
| `session_count` | `epistemic_state` | Partially |
| `overload_patterns` | `pedagogical_memory` | Yes (capacity) |
| Route per session | `session_ledger` | Not yet read by planner |

### 5.2 Required But Not Yet Stored

**A. Remediation outcome tracking**

When a misconception intervention fires, was it effective? The system currently records that an intervention occurred but not whether the learner subsequently answered correctly on the same topic.

Required fields: `intervention_at`, `topic`, `misconception_id`, `follow_up_mastery_delta`, `resolved: bool`

**B. Confidence calibration**

The gap between self-assessed confidence and actual mastery is one of the most important signals for mentorship selection. A learner who is over-confident needs Challenge Partner earlier. A learner who is under-confident needs Foundational Guide longer.

Required field: `confidence_calibration_delta` per topic — estimated difference between stated confidence and mastery_probability.

This requires a mechanism for eliciting learner self-assessment, even informally.

**C. Exam proximity**

`exam_days_remaining` is referenced in 3 of the 8 adjustment rules and is central to the urgency modifier in the selection framework. It does not exist in the current LES schema.

Required field: `exam_date` (ISO date) in `epistemic_state`. Derivable `exam_days_remaining` at runtime.

**D. Error type history**

`recent_error_type` is used as a signal in the mode_selector but there is no persistent history of error types. A single session's error type can be noise. Patterns across sessions are signal.

Required fields: `error_type_history` per topic — rolling list of the last N error types observed, with timestamps.

**E. Causal chain mastery per chain**

Currently the system tracks `difficult_causal_chains` (which chains are hard) but not mastery per chain. A chain being "difficult" is a binary flag; what is needed is a probability estimate similar to concept mastery.

Required field: `causal_chain_mastery_probability` per `chain_id`.

**F. SAT component mastery**

SAT mastery is currently binary (sat_drill_needed: bool). The SAT has multiple components — appearance, nose, palate, conclusions — and within palate, multiple structural elements. Distinction-level SAT mastery requires component-level tracking.

Required fields: `sat_component_mastery` dict keyed by SAT layer (appearance, nose, palate_sweetness, palate_acidity, palate_tannin, palate_body, palate_finish, quality_conclusion, ageing_potential).

**G. Distinction readiness index**

A composite signal that aggregates readiness across all Distinction capability dimensions (from Part 2). Not a score. A structured readiness map.

Required fields: presence/absence (not probability) of evidence for each of the 8 Distinction capabilities, updated per session.

**H. Response time patterns (future — low priority)**

Response latency is mentioned in the task but is low priority for local deterministic operation. It would require timed interaction infrastructure that does not exist. Defer to a future interactive layer.

### 5.3 Learner Model Schema (Future State)

```
epistemic_state:
  learner_id
  current_level
  exam_date                         ← NEW
  known_weak_areas
  recent_misconceptions
  session_count
  governance

pedagogical_memory:
  skills:
    concept_id:
      mastery_probability
      attempts / successes / recent_failures
      misconception_hits
      error_type_history             ← NEW
      last_seen
      confidence_trend
  recurrent_misconceptions:
    misconception_id:
      persistence
      last_triggered
      intervention_outcome           ← NEW (resolved: bool, mastery_delta)
  difficult_causal_chains:
    chain_id:
      retention_risk
      mastery_probability            ← NEW
      last_triggered
  sat_component_mastery             ← NEW (dict by SAT layer)
  confidence_calibration_delta      ← NEW (overall or per topic)
  mastered_concepts
  preferred_depth
  overload_patterns
  distinction_readiness             ← NEW (dict by capability dimension)
  governance
```

---

## Part 6: Risk Assessment — Challenging the Framework (Task F)

### 6.1 Unnecessary Complexity

**Risk:** The 5-style taxonomy may be over-specified. Do Foundational Guide and Analytical Builder require distinct styles, or are they points on the same continuum?

**Assessment:** They are genuinely distinct because their *relationship to the learner* differs — Foundational Guide reduces cognitive threat; Analytical Builder increases cognitive demand. A weight shift alone (more host → less scientist) does not capture this. The distinction is pedagogically real.

**However:** `Exam Readiness Coach` is potentially redundant with a high-urgency configuration of `Challenge Partner` + `Precision Calibrator`. It should be audited in Phase 2 — if it proves to be simply a time-modulated blend of the other styles, collapse it.

### 6.2 Duplicated Concepts

**Risk:** Cognitive functions overlap with mentorship styles. `critic` function vs. `Precision Calibrator` style. `challenger` function vs. `Challenge Partner` style.

**Assessment:** This is real and must be managed carefully. The functions are *dimensions*; the styles are *named configurations of those dimensions*. The naming must never become confusing. The implementation must use styles (not function names) as the user-visible layer. Functions remain internal.

**Risk:** `tutor_modes` and mentorship styles now coexist. `distinction` mode and `Challenge Partner` style are close but not identical.

**Assessment:** The existing tutor modes should be progressively mapped to the mentorship styles. `mentor` → Foundational Guide. `trainer` → Analytical Builder. `reviewer` → Precision Calibrator. `distinction` / `exam_pressure` → Challenge Partner / Exam Readiness Coach. The mode system does not need to be removed, but future development should use styles as the authoritative layer and treat modes as presets.

### 6.3 Governance Risks

**Risk:** Mentorship styles could drift toward persona/roleplay if described in human terms. "The way The Calibrator would respond to this" is the beginning of a character system, not a framework.

**Assessment:** Acute risk. Every style description in this document must remain *functional and pedagogical*, not characterological. The governance rule must be: styles describe **what the system does**, never **who the system is**. No names, no biographies, no voices, no personalities attached to styles.

**Risk:** `exam_days_remaining` being used as a signal could create false authority — the system behaving as though it knows the exam is coming and calibrating toward it might be perceived as examiner-adjacent.

**Assessment:** The signal is pedagogical (preparation intensity) not evaluative (predicting exam outcome). The governance constraint is that the system can intensify preparation but cannot claim to know what the exam will test or simulate the exam itself in a way that implies official authority.

### 6.4 False Authority Risks

**Risk:** `Precision Calibrator` style, applied to SAT responses, could be perceived as the system grading tasting notes against an official standard.

**Assessment:** This is a concrete risk. The system must always frame SAT calibration as "here is what WSET-register evidence looks like" rather than "your answer would receive X marks." The scaffolding acts `direct_correction` and `hint` are the safe vocabulary — not grading language.

### 6.5 Roleplay Risks

**Risk:** The mentorship style descriptions in this document use phrases like "challenge partner," "foundational guide" — these are inherently relational. If a visible representation is attached, the relationship becomes a character.

**Assessment:** The risk is manageable if visible representations are never described as entities with opinions, emotions, or personalities. A visible representation is a *presentation mode* for a style, not a character with its own existence.

### 6.6 Scalability Risks

**Risk:** Five mentorship styles with multi-signal selection requires more LES data than currently exists. The framework cannot be fully activated until `exam_date`, `error_type_history`, `intervention_outcome`, and `causal_chain_mastery_probability` are implemented.

**Assessment:** The framework is designed to degrade gracefully. With limited data, the strategic planner produces a conservative plan. The selection logic defaults to Foundational Guide when readiness signals are absent. This is the correct behavior.

### 6.7 Learner Confusion Risks

**Risk:** Learners should not need to know what style is being applied. If the mentorship style leaks into the interaction vocabulary ("I am now in Challenge Partner mode"), it creates confusion.

**Assessment:** Styles are internal routing decisions. The only learner-visible dimension is the *behavior* — the kinds of questions asked, the intensity of the feedback, the presence or absence of emotional scaffolding. Styles must be invisible to the learner.

---

## Part 7: Are Visible Mentor Representations Justified? (Task G)

### 7.1 The Four Options

**Option A: No visible mentors at all.**  
The system operates as a pure tutoring interface. Questions appear, feedback appears, no face or name is attached.

*Benefits:* Zero risk of character drift. Zero governance exposure from persona design. Maximum focus on content.  
*Risks:* Low engagement for learners who benefit from relational framing. Higher attrition for learners in early learning phases where emotional scaffolding is valuable.  
*Verdict:* Academically cleanest but not optimal for learner retention and motivation, particularly at the start of a demanding qualification.

**Option B: Pure mentorship modes.**  
The system indicates which mode is active (e.g. "review mode" / "challenge mode") without any visual representation.

*Benefits:* Transparent about system behaviour. No character risk. Learner understands why the feedback tone changed.  
*Risks:* Abstract mode labels may not translate into meaningful learner experience. "Precision Calibrator mode" means nothing to a learner who just wants to understand Burgundy.  
*Verdict:* Better than nothing for transparency, but insufficient as a standalone learner experience.

**Option C: Limited visible representations — functional, not characterological.**  
Each mentorship style has a simple visual identifier: an icon, a colour palette, a tone indicator — something that signals "this is a calibration-focused session" without implying a character with a personality.

*Benefits:* Gives the learner an experience anchor without creating a character system. Keeps design grounded in function. Avoids the governance and complexity risks of full characters.  
*Risks:* Still requires a design system. Can drift toward characters over time if not governed.  
*Verdict:* The most appropriate option for this system at this stage.

**Option D: Full character system.**  
Five or six named characters, each with visual design, backstory, personality, and consistent voice.

*Benefits:* Highest engagement potential. Strongest learner identification. Most commercially compelling.  
*Risks:* Every risk identified in Part 6 is amplified. The character becomes the product rather than the pedagogy. Governance complexity scales with character complexity. Development overhead is very high relative to pedagogical value. The characters currently designed (in `FUTURE_TUTOR_CHARACTER_DNA.md`) were designed before the mentorship framework — they do not map cleanly onto the 5 mentorship styles.  
*Verdict:* **Not justified at this stage.** The framework is not complete enough to anchor a character system. Characters designed before the framework will constrain the framework. This is the reversal that must be avoided.

### 7.2 Recommendation

**Adopt Option C (limited visible representations) as the design target.**

A visual identity should signal the active mentorship style without characterising it as a person. Specifically:

1. Each mentorship style has a visual mode indicator (icon + colour + brief label)
2. The indicator is functional: "analysis mode," "calibration mode," "challenge mode"
3. No names, no faces, no personalities
4. The `visible_tutor_characters.json` and `FUTURE_TUTOR_CHARACTER_DNA.md` are suspended as active design deliverables — they are research archives only until the mentorship framework is sufficiently proven to anchor character design safely

If characters are ever revisited, they must emerge from the framework as follows:
- Each character maps exactly to one mentorship style (or a defined blend of adjacent styles)
- Character personality is *derived from* the pedagogical function, not invented separately
- Characters are design decisions made after the mentorship framework is stable and tested

---

## Part 8: Recommended Next Research Phase

### Phase 2A (Immediate): Populate `distinction-patterns/`

The `distinction-patterns/` directory has a schema and zero content. This is the highest-priority knowledge gap. Without distinction pattern content, the system cannot identify the specific quality of reasoning that separates Distinction from Pass.

**Required:** Curate 10-15 `dp_*.json` files covering the highest-frequency WSET L3 topics where the Pass/Distinction gap is documented. Start with: acidity, oak influence, climate and wine style, SAT quality conclusions, ageing potential argumentation, regional classification systems.

### Phase 2B: Add `exam_date` to LES and wire `exam_days_remaining`

This single field unlocks the urgency modifier in the selection framework. It is the highest-leverage low-complexity change.

### Phase 2C: Implement mentorship style selection as a deterministic function

Take the decision framework in Part 4.3 and implement it as a pure function over LES + pedagogical memory, following the same isolation pattern as `strategic_planner.py`. It should return a `selected_style`, `rationale`, and `transition_condition`. No side effects. Full test coverage.

### Phase 2D: Implement `error_type_history` in pedagogical memory

Extend skill state in `knowledge_tracing.py` with a rolling `error_type_history` list (last 5 error types per concept, with timestamps). This converts single-session noise into multi-session signal.

### Phase 2E: Audit and map existing tutor modes to mentorship styles

Document the formal mapping between the 5 existing tutor modes and the 5 mentorship styles. Identify where they diverge. Plan a migration path that preserves backward compatibility while making styles the authoritative layer.

### Phase 3 (Future): SAT component mastery tracking

Extend the learner model with component-level SAT mastery. This requires SBA (structured-answer) diagnostics that can parse a tasting note and identify which SAT layer was weak. This is non-trivial and should not be attempted until distinction-patterns content and the mentorship selection function are stable.

---

## Summary Tables

### Distinction Capability Framework (condensed)

| Capability | Core Requirement | Current System Coverage |
|-----------|-----------------|------------------------|
| Technical wine knowledge | Structural + connected, not factual recall | Retrieval layer covers; distinction patterns empty |
| Causal reasoning | A→B→C mechanism chains, not just conclusions | 32 causal chains; not yet linked to capability tracking |
| SAT mastery | Evidence-supported, calibrated, structured | SAT reasoner exists; component mastery not tracked |
| Structured written explanation | Claim → evidence → qualification → synthesis | No evaluation of argument structure yet |
| Vocabulary precision | WSET-register, correct intensity level | SAT reasoner partially covers; no answer-level check |
| Commercial communication | Audience-aware, service-applicable | `host` function exists; no commercial scenario evaluation |
| Confidence calibration | Certainty matched to evidence strength | No calibration delta tracking |
| Misconception immunity | 20 nodes; `distinction_relevance` flags | Prepass detection exists; remediation outcome not tracked |

### Mentorship Style → Tutor Mode Mapping

| Mentorship Style | Primary Need | Closest Existing Mode | Key Gap in Existing Mode |
|-----------------|-------------|----------------------|-------------------------|
| Foundational Guide | Build foundation, reduce threat | `mentor` | No deactivation logic; no overload signal integration |
| Analytical Builder | Causal reasoning depth | `trainer` → `distinction` transition | No causal chain mastery tracking |
| Precision Calibrator | SAT calibration, evidence linking | `reviewer` + `distinction` | No component-level SAT tracking |
| Challenge Partner | Stress-test, anti-fragility | `exam_pressure` | Readiness gate not implemented |
| Exam Readiness Coach | Procedural integration, exam format | `exam_pressure` with host floor | No exam proximity signal in LES |

---

*This document is a development planning artifact. It does not represent WSET assessment or examiner evaluation. No code was modified. No implementation was performed.*

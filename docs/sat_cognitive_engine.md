# SAT Cognitive Engine
## WSET-AI-System — Cognitive Architecture Design Series

**Author:** Claude (Cowork) — Cognitive Architecture Designer Role
**Date:** 2026-05-15
**Series position:** 4 of 8 — Structurally independent from Documents 1–3; represents a parallel cognitive module
**Status:** Design specification — requires engineering implementation

---

## Why SAT Is Not a Topic

The most important architectural decision about SAT is recognising what it is not.

SAT is not a topic. You cannot teach SAT the way you teach "regions of Bordeaux" or "the role of tannin in wine structure." SAT is a cognitive procedure — a structured method for moving from sensory observation through inference to evaluative conclusion. It requires a specific type of reasoning, in a specific direction, under specific constraints of uncertainty and commitment. It is architecturally different from theory retrieval and explanation.

The current system handles SAT as a retrieval problem: a student asks a SAT-related question, the query is classified as `sat_coaching`, the retrieval pipeline fetches chunks from Wine With Jimmy content about SAT structure, BICL, quality descriptors. The Tutor Agent synthesises an explanation. This is a reasonable first approach, and it works better than nothing — but it misses the fundamental nature of what SAT assessment requires.

This document specifies the SAT Cognitive Engine: a dedicated module that handles SAT reasoning as the distinct cognitive process it is.

---

## The Cognitive Structure of SAT

### Theory reasoning: Cause → Mechanism → Effect

Theory reasoning in wine starts with a cause and moves forward through a mechanism to an effect. The knowledge structure is:

```
Cool climate (cause)
  → Malic acid is retained rather than degraded by heat (mechanism)
  → Wine has higher total acidity, lower pH (effect in chemistry)
  → Wine tastes fresh, has better ageing potential, pairs well with fatty foods (consequence)
  → "High acidity" in SAT, linked to freshness and ageability (exam formulation)
```

The reasoning direction is forward: cause → mechanism → effect → consequence. The student is given the cause and asked to construct the chain forward. Knowledge is generative.

### SAT reasoning: Observation → Inference → Cause

SAT reasoning runs in the opposite direction. The student begins with a finished wine — a set of observable characteristics — and must reason backward to infer what caused those characteristics and evaluate whether they meet quality criteria.

```
Observation: pale lemon colour, medium acidity, green apple + citrus aromas, light body, high acidity, short finish
  → Inference: likely cool-climate origin; varietal character suggests Riesling or Sauvignon Blanc; short finish and light body suggest young, possibly inexpensive wine
  → Quality assessment: acceptable quality — technically sound, shows varietal character, but limited complexity and length prevent higher rating
  → BICL justification: Balance reasonable (structure holds), Intensity moderate, Complexity limited to primary fruit, Length short
  → Conclusion: Acceptable quality for everyday consumption
```

The reasoning direction is backward: observation → inference → cause + quality judgment. The student is given the effect and asked to reason back to what caused it and whether the causing-conditions produced a quality outcome.

This is not merely a different application of the same knowledge. It is structurally different reasoning:

| Dimension | Theory reasoning | SAT reasoning |
|---|---|---|
| Starting point | Cause (given) | Observable characteristics (given) |
| Direction | Forward (cause → effect) | Backward (effect → inferred cause) |
| Certainty | High (if you know the chain) | Inherently uncertain (multiple possible causes) |
| Output type | Explanation | Judgment + justification |
| Cognitive demand | Recall + chain traversal | Inference + commitment |
| Failure mode | Incomplete chain | Commitment failure, unsupported conclusion |

### The Commitment Demand

The central cognitive challenge of SAT is not perceptual accuracy. It is decisional commitment.

A student can accurately observe every characteristic of a wine and still fail to produce a correct SAT response because they refuse to commit to a quality conclusion. This is `sat_non_commitment` — the most common high-stakes error in WSET L3 assessment. The student hedges: "this could be acceptable or good quality, depending on the context" when the examiner requires a committed judgment from the WSET quality definition.

`sat_non_commitment` is not a knowledge gap. The student who hedges knows the quality descriptors. They know BICL. They know what acceptable vs. good vs. outstanding quality means. What they cannot do is commit to a judgment under conditions of sensory uncertainty and perform the rhetorical act of asserting that judgment with supporting evidence.

This is a different cognitive failure from a factual error, and it requires a different intervention.

---

## SAT Cognitive Engine Architecture

The SAT Cognitive Engine is a specialized sub-module within the Tutor Agent's execution context, activated whenever the Orchestrator classifies a session as `SAT_DRILL`, `SAT_EVALUATION`, or `SAT_COACHING`.

### Module Components

**1. Observation Accuracy Validator**

Checks whether the student's sensory observations are within the expected range for the wine being assessed. If a student claims "deep ruby" for a wine the system knows is light garnet (from the exercise specification), the validator flags this as an observation error before the inference layer runs.

This prevents inference errors from being attributed to reasoning failures when they are actually perceptual errors.

```
Input: student_observation_set, wine_specification
Output: observation_accuracy_report {
  appearance: {accurate: bool, errors: [], over_statements: [], under_statements: []},
  nose: {...},
  palate: {...},
  finish: {...}
}
```

**2. Inference Chain Evaluator**

Evaluates whether the student's inferences follow logically from their observations. The evaluator has access to the knowledge graph and checks whether the observation → inference link is valid.

```
Student: "high acidity → cool climate origin"
Inference chain evaluator:
  - Is "high acidity → cool climate origin" a valid inference? YES (directionally)
  - Is it the ONLY valid inference? NO (could also be early harvest, high-altitude site, MLF not performed)
  - Did the student acknowledge uncertainty appropriately? [check hedging language]
  - Did the student support the inference with additional corroborating evidence? [check for converging support]
```

The evaluator does not penalize uncertainty acknowledgment — it rewards it. A student who says "the high acidity and green fruit character suggest a cool climate or high-altitude origin, though the ripeness of the secondary fruit notes is consistent with a warmer site in a good vintage" is demonstrating better inferential reasoning than a student who asserts "cool climate" without qualification.

**3. BICL Constraint Propagator**

This is the architectural core of the SAT Cognitive Engine. BICL (Balance, Intensity, Complexity, Length) is not just a checklist — it is a constraint system. Each element constrains the range of quality conclusions that can be supported.

The constraint propagator takes the student's observed BICL values and computes the valid range of quality conclusions they could support:

```
BICL input:
  Balance: reasonable (structure sound, no dominating elements)
  Intensity: medium (neither pronounced nor light)
  Complexity: limited (primary fruit only, no secondary/tertiary development)
  Length: short (flavour fades within 5–10 seconds)

Constraint propagation:
  Complexity: limited → cannot support "outstanding" or "very good" quality
  Length: short → cannot support "outstanding" quality
  Balance: reasonable → supports at least "acceptable"
  Intensity: medium → consistent with "acceptable" or "good"

Valid quality conclusion range: "acceptable" to "good"
Student must commit to one of these. "Outstanding" is out of constraint.
```

The constraint propagator makes explicit what BICL evidence supports and what it rules out. The student who writes "I would say this wine is acceptable quality, possibly good, because the BICL..." is working within the constraint space. The student who writes "outstanding quality" when Length is short has violated a constraint — and the evaluator can identify exactly which constraint was violated.

**4. Commitment Classifier**

Classifies the student's quality conclusion along two dimensions:

- **Specificity:** Did the student name a quality level from the WSET scale (unacceptable / acceptable / good / very good / outstanding)?
- **Support:** Is the quality claim supported by named BICL evidence?

Outputs a commitment classification:

```
commitment_classification: {
  quality_level_named: true/false,
  bicl_evidence_cited: true/false,
  causal_link_stated: true/false,  # "because the balance and length suggest..."
  commitment_confidence: "hedged" / "assertive" / "overclaiming",
  error_labels: ["sat_non_commitment", "bicl_not_supported", ...]
}
```

**5. Style-Quality Separation Checker**

Checks whether the student correctly separates style statements (this is a light-bodied, high-acid, aromatic wine) from quality statements (this wine achieves good quality for its type). Students commonly conflate these: "this is a light-bodied wine, so it's lower quality" confuses a style descriptor with a quality judgment.

```
Student: "Light body means this wine cannot be high quality"
Checker: STYLE_QUALITY_CONFLATION detected
  Rule violated: body weight is a style attribute, not a quality indicator
  Counter-evidence: Mosel Spätlese Riesling (light body, very good+ quality)
```

---

## SAT Session Types and Orchestrator Integration

The Orchestrator selects SAT session types from the SAT Cognitive Engine's repertoire:

### SAT Session Type 1 — Observation Calibration

Goal: Ensure the student's sensory vocabulary maps correctly to WSET SAT descriptors.
Format: Tutor provides a wine description; student writes observations using SAT vocabulary; observation accuracy validator evaluates.
Priority trigger: `sat_epistemic_state.observation_accuracy` shows any element below `reliable`.

### SAT Session Type 2 — Inference Drilling

Goal: Train the student to reason from observation to inferred cause.
Format: Tutor provides a complete observation set; student writes inference section only (no quality conclusion); inference chain evaluator assesses.
Priority trigger: Multiple sessions showing correct observations but incorrect or missing inferences.

### SAT Session Type 3 — BICL Construction

Goal: Train the student to assemble a BICL argument from observations.
Format: Tutor provides observations and inferences; student must construct a BICL justification; constraint propagator validates.
Priority trigger: `bicl_not_supported` error label appearing in 2+ Examiner sessions.

### SAT Session Type 4 — Commitment Practice

Goal: Force the student to commit to a quality conclusion without hedging.
Format: Tutor provides a complete SAT including BICL; student writes ONLY the quality conclusion. Student may not use "possibly," "could be," "depending on." Commitment classifier evaluates.
Priority trigger: `sat_non_commitment` error label, any occurrence.
Note: This session type must be preceded by a brief explanation of why commitment is required: "In a WSET examination, examiners expect you to make a judgment. Hedging is not rewarded — it reads as uncertainty about the framework, not appropriate intellectual humility."

### SAT Session Type 5 — Full SAT with Integrated Evaluation

Goal: Full end-to-end SAT practice with all components evaluated.
Format: Tutor provides a wine exercise; student writes complete SAT; all five engine components run in sequence; Orchestrator routes weak points to targeted follow-up.
Priority trigger: Nazareth is 30+ days from exam and has not completed a full SAT in the last 7 days.

---

## The SAT Epistemic State in the LES

The LES SAT epistemic state (from Document 1) feeds directly into the SAT Cognitive Engine:

```json
"sat_epistemic_state": {
  "commitment_behavior": "avoidant",    → Orchestrator flags SAT Session Type 4
  "most_common_failures": ["sat_non_commitment", "bicl_not_supported"],
  "observation_accuracy": {
    "finish": "absent_from_responses"   → Orchestrator flags SAT Session Type 1 for finish
  },
  "inference_quality": {
    "production_method_inference": "absent"  → Orchestrator flags SAT Session Type 2 for production method
  }
}
```

The Orchestrator reads these states and selects the appropriate SAT session type. It does not wait for the student to request SAT practice — if the LES shows `commitment_behavior: avoidant` and there are 20 days to exam, the Orchestrator proactively schedules SAT Session Type 4 in the next session regardless of what the student asks.

---

## What SAT Coaching Must NOT Do

- **Must not provide "model answers" for memorisation.** A student who memorises SAT phrasings without understanding the underlying constraint structure will fail on a new wine. SAT competence requires being able to apply the framework to any wine, not to produce a familiar-sounding response.

- **Must not conflate theory knowledge with SAT performance.** A student who can explain the chemistry of malolactic fermentation may still write a poor SAT note. Theory knowledge and SAT performance are related but not equivalent.

- **Must not reward hedging.** "This wine could be acceptable or good quality" is not a good answer. The SAT engine must identify hedging and prompt for a committed judgment.

- **Must not skip the inference layer.** Students who move directly from observation to quality conclusion without explicitly reasoning through BICL are training a shortcut that will fail them when the wine is unfamiliar or complex.

---

*Generated: 2026-05-15 | Cognitive Architecture Design Series | Document 4 of 8*
*Not an official WSET document. Not for learner-facing use.*

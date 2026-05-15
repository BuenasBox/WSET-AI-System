# Learner Epistemic State Architecture
## WSET-AI-System — Cognitive Architecture Design Series

**Author:** Claude (Cowork) — Cognitive Architecture Designer Role
**Date:** 2026-05-15
**Series position:** 1 of 8 — Foundational layer; all other documents depend on this one
**Status:** Design specification — requires engineering implementation

---

## The Core Problem

The system currently models correct wine knowledge. It does not model what Nazareth (the learner) currently believes.

This is not a retrieval gap. It is a representational gap. No amount of improved chunking, better embeddings, or richer causal chains closes it — because the gap is not about what content the system holds, but about what the student holds. A student approaching the WSET L3 Distinction level is not empty. They carry beliefs, some correct, some partially correct, some inverted, some confidently held despite being wrong. The system, in its current form, is blind to all of it.

The Learner Epistemic State (LES) is the architectural layer that fixes this. It is a structured representation of what Nazareth currently believes about the WSET L3 domain, maintained across sessions, updated after every interaction, and read by the Orchestrator before every pedagogical decision.

---

## What "Epistemic State" Means Here

"Epistemic state" does not mean "list of topics covered." A topic coverage checklist answers the question: *Has Nazareth encountered information about tannin?* The epistemic state answers the question: *What does Nazareth believe about tannin, and how reliably?*

These are different questions with different implications for tutoring.

A student who has encountered information about tannin and correctly understands its source (grape skins, seeds, stems), its role in structure, its interaction with proteins, and its trajectory in ageing — that student needs depth extension. They need distinction-level nuance: why grape-derived tannin differs from wood-derived tannin in texture, how tannin level interacts with acidity to determine ageing potential, how to articulate this in SAT quality conclusion language.

A student who has encountered the same information but holds the belief that "more tannin = higher quality wine" — that student needs correction first, not extension. Every additional fact loaded on top of an inverted causal belief makes the inversion harder to dislodge.

The system cannot distinguish these two students today. The LES makes this distinction its central architectural commitment.

---

## Schema Design

### 1. Top-Level LES Object

```json
{
  "learner_id": "nazareth",
  "schema_version": "1.0",
  "last_updated": "2026-05-15T...",
  "exam_date": "2026-08-08",
  "days_to_exam": 85,

  "belief_nodes": { ... },
  "misconception_registry": { ... },
  "knowledge_stability_map": { ... },
  "causal_understanding_map": { ... },
  "sat_epistemic_state": { ... },
  "session_history": [ ... ],
  "weak_area_index": { ... }
}
```

### 2. Belief Nodes

Each belief node represents what the learner believes about a specific concept in the knowledge graph. It is not a binary "knows / doesn't know" flag. It is a multi-dimensional belief object.

```json
"belief_nodes": {
  "C_ACIDITY": {
    "concept_id": "C_ACIDITY",
    "concept_name": "Acidity",
    "belief_state": "partially_correct",
    "confidence": 0.72,
    "stability": "fragile",
    "last_assessed": "2026-05-10",
    "exposures": 4,
    "correct_responses": 2,
    "incorrect_responses": 1,
    "corrected_responses": 1,
    "held_beliefs": [
      {
        "belief_text": "Cool climates produce wines with higher acidity",
        "correctness": "correct",
        "confidence_in_belief": "high",
        "source": "tutor_session_003"
      },
      {
        "belief_text": "High acidity means the wine is unpleasant or harsh",
        "correctness": "incorrect",
        "confidence_in_belief": "medium",
        "source": "inferred_from_sat_response_007",
        "linked_misconception": "MC_ACIDITY_QUALITY"
      }
    ],
    "causal_chain_understanding": {
      "CC_COOL_CLIMATE_ACIDITY": "partial",
      "CC_MLF_ACIDITY_REDUCTION": "absent"
    },
    "distinction_gap": "Cannot articulate malic vs. tartaric acid retention. Cannot link acidity to ageability in SAT conclusion."
  }
}
```

**Belief state values:**
- `absent` — No belief formed; concept has not been encountered or assessed
- `fragmented` — Isolated facts held without causal structure
- `partially_correct` — Core belief is directionally right but incomplete or imprecise
- `correct_but_shallow` — Correct understanding but cannot explain the mechanism
- `correct_with_mechanism` — Can explain cause and effect
- `distinction_level` — Meets the full causal chain + exam articulation standard

**Stability values:**
- `fragile` — Belief appeared recently or has been self-contradicted across sessions
- `consolidating` — Consistent across 2–3 sessions
- `stable` — Consistent and confident across 4+ sessions
- `at_risk` — Previously stable belief showing regression signals (e.g., correct in isolation, wrong in SAT context)

### 3. Misconception Registry

This is the most critical component of the LES. Each entry tracks an active or historical misconception — not a vague "error area" but a specific false belief with its current status.

```json
"misconception_registry": {
  "MC_ACIDITY_QUALITY": {
    "misconception_id": "MC_ACIDITY_QUALITY",
    "misconception_text": "High acidity indicates lower quality wine",
    "causal_inversion": true,
    "severity": "high",
    "first_detected": "2026-05-03",
    "last_detected": "2026-05-10",
    "detection_count": 3,
    "current_status": "active",
    "intervention_attempts": [
      {
        "date": "2026-05-05",
        "intervention_type": "causal_chain_walkthrough",
        "outcome": "partial_correction",
        "notes": "Learner accepted correction in isolation but reactivated misconception in SAT context"
      }
    ],
    "hardening_risk": "medium",
    "linked_concept": "C_ACIDITY",
    "exam_destructive": true,
    "blocks_sat_quality_conclusion": true
  }
}
```

**Status values for misconceptions:**
- `active` — Currently detected in learner responses
- `corrected_provisional` — Correction accepted but not yet stable (< 3 clean sessions)
- `corrected_stable` — No reactivation after 3+ sessions
- `at_risk_of_reactivation` — Stable but context-dependent (correct in theory, reactivates under SAT pressure)
- `resolved` — Confirmed absent across 5+ sessions

**Hardening risk model:**

A misconception that is detected but not immediately corrected hardens. Hardening means the false belief becomes more difficult to correct with each passing session because the student has built further knowledge on top of it. The hardening risk score increases as a function of:
- Number of sessions since first detection without correction
- Proximity of the misconception to core exam concepts
- Whether the misconception appears in SAT responses (cross-context activation = higher risk)

### 4. Knowledge Stability Map

A rapid-access view of which concepts are stable, fragile, or absent. Used by the Orchestrator for session planning without full LES traversal.

```json
"knowledge_stability_map": {
  "RA1_VITICULTURE": {
    "C_ACIDITY": "fragile",
    "C_TANNIN": "correct_but_shallow",
    "C_COOL_CLIMATE": "correct_with_mechanism",
    "C_WARM_CLIMATE": "partially_correct",
    "C_MLF": "absent",
    "C_BOTRYTIS": "fragmented"
  },
  "RA2_REGIONS": {
    "T_BORDEAUX": "fragmented",
    "T_BURGUNDY": "absent",
    "T_CHAMPAGNE": "fragmented",
    "T_GERMANY": "absent",
    "T_ITALY": "absent",
    "T_SPAIN": "absent"
  },
  "RA3_SPARKLING": {
    "T_TRADITIONAL_METHOD": "partially_correct",
    "T_TRANSFER_METHOD": "absent",
    "T_TANK_METHOD": "absent"
  },
  "RA4_FORTIFIED": {
    "T_PORT": "fragmented",
    "T_SHERRY": "absent"
  },
  "RA5_WINE_LAW": {
    "T_EU_CLASSIFICATION": "fragmented",
    "T_FRANCE_AOC": "absent"
  }
}
```

### 5. Causal Understanding Map

Tracks whether the learner understands causal chains — not just that they know the output, but that they can follow the mechanism. This is the distinction between "Nazareth knows that cool climate produces high acidity" and "Nazareth can explain why, step by step, in exam register."

```json
"causal_understanding_map": {
  "CC_COOL_CLIMATE_ACIDITY": {
    "chain_id": "CC_COOL_CLIMATE_ACIDITY",
    "understanding_level": "output_only",
    "can_state_cause": true,
    "can_state_mechanism": false,
    "can_state_wine_consequence": true,
    "can_articulate_for_exam": false,
    "distinction_note_understood": false,
    "assessed_in_sat": false,
    "sat_articulation_quality": null
  },
  "CC_MLF_ACIDITY_REDUCTION": {
    "chain_id": "CC_MLF_ACIDITY_REDUCTION",
    "understanding_level": "absent",
    "can_state_cause": false,
    "can_state_mechanism": false,
    "can_state_wine_consequence": false,
    "can_articulate_for_exam": false,
    "distinction_note_understood": false,
    "assessed_in_sat": false,
    "sat_articulation_quality": null
  }
}
```

### 6. SAT Epistemic State

SAT reasoning is cognitively distinct from theory reasoning. The learner may correctly understand causal theory yet fail at SAT because the cognitive demand is reversed. The SAT epistemic state tracks SAT-specific cognitive behavior independently.

```json
"sat_epistemic_state": {
  "overall_sat_level": "pass_range",
  "commitment_behavior": "avoidant",
  "most_common_failures": [
    "sat_non_commitment",
    "bicl_not_supported",
    "missing_causal_link"
  ],
  "quality_conclusion_pattern": {
    "makes_quality_claim": true,
    "supports_with_bicl": false,
    "links_to_style": false,
    "commits_to_level": false
  },
  "observation_accuracy": {
    "appearance": "reliable",
    "nose": "reliable",
    "palate": "fragile",
    "finish": "absent_from_responses"
  },
  "inference_quality": {
    "climate_inference": "partially_correct",
    "variety_inference": "fragile",
    "production_method_inference": "absent"
  },
  "sat_misconceptions": [
    "MC_SAT_MORE_TERMS_HIGHER_SCORE",
    "MC_QUALITY_EQUALS_PERSONAL_PREFERENCE"
  ]
}
```

---

## How the LES Is Maintained

### Write Operations — When and What

The LES is updated after every Examiner Agent scoring session. Tutor interactions may generate soft signals (e.g., the learner asks a question that implies a misconception) but these are not directly written to the LES without Examiner confirmation. The write protocol:

**After Examiner session:**
1. Examiner returns scored output with error taxonomy labels
2. Orchestrator maps each error label to a belief node or misconception node
3. Orchestrator updates: confidence scores, belief state, misconception detection count, causal chain understanding level
4. If a new misconception is detected (not in registry), Orchestrator creates a new entry with status `active`, hardening_risk `low`
5. If a known misconception reactivates after provisional correction, status reverts to `active`, hardening_risk increments

**After Tutor session (soft signals only):**
1. Student question implies a misconception (e.g., "So high acidity means the wine is acidic and sharp?")
2. Orchestrator logs this as a `soft_detection_signal` against the relevant misconception node
3. Three consecutive soft signals without Examiner confirmation = promotes to `suspected_active`, flagged for next Examiner session

### Read Operations — Orchestrator Planning

The Orchestrator reads the LES at the start of every session planning cycle. The read produces:

1. **Active misconception list** — sorted by `hardening_risk` × `exam_destructive` × `days_since_first_detection`
2. **Fragile concept list** — concepts in `fragile` or `at_risk` stability state
3. **Causal gap list** — chains where `understanding_level` is `output_only` or `absent`
4. **SAT priority flags** — commitment failures, BICL unsupported conclusions
5. **Session priority score** — computed across all four lists using the priority formula

---

## The Priority Formula, Extended

The existing formula in the Orchestrator prompt:

```
priority = exam_relevance + recurrence + severity + proximity_to_exam - recent_improvement
```

For the LES, each variable is now LES-grounded:

- `exam_relevance` — drawn from the knowledge graph's node weight for this concept in the WSET L3 specification coverage
- `recurrence` — drawn from `detection_count` in the misconception registry or `incorrect_responses` in the belief node
- `severity` — drawn from `hardening_risk` and `exam_destructive` flags
- `proximity_to_exam` — computed from `days_to_exam` in the LES top-level object
- `recent_improvement` — drawn from the last 3 session entries in `session_history` for this concept

---

## What Becomes Possible

With the LES active, the system can:

**Know before it teaches.** Before the Orchestrator selects a teaching task, it knows what Nazareth currently believes about the concept — not just whether they've seen it.

**Detect reactivation.** A misconception that was corrected and then reappears is more dangerous than a new misconception. The LES tracks this reactivation pattern. The Orchestrator can escalate intervention type in response.

**Identify hardening risk.** A misconception that has been detected 4 times without successful correction has a high hardening risk. The Orchestrator de-prioritizes additional content coverage and prioritizes intervention.

**Separate SAT failures from theory failures.** A student who fails to commit to a quality conclusion in SAT is not failing because they don't know the theory. They are failing because SAT cognition — committing to a judgment under uncertainty — is a different cognitive demand. The LES captures this distinction.

**Plan for distinction, not just pass.** The `belief_state: "correct_but_shallow"` status identifies the learner who has correct understanding but cannot articulate the mechanism for marks. This is the distinction gap. The LES makes it visible; the Orchestrator can then direct targeted distinction-level drilling rather than re-teaching already-understood material.

---

## Implementation Notes

The LES is a structured JSON file per learner, stored at:
`knowledge/nazareth/{learner_id}/epistemic_state.json`

It is read-only for the Tutor Agent. The Examiner Agent writes diagnostic data to a staging object (`knowledge/nazareth/{learner_id}/session_staging.json`). The Orchestrator performs the merge from staging into the canonical LES after each session.

The LES does not require vector embeddings. Reads and writes are by key access. The entire file for one learner is unlikely to exceed 500KB even after 100 sessions.

Version control: the LES should be appended-only in the `session_history` array. No belief node or misconception entry should be deleted — only status-updated. The history is an audit trail.

---

*Generated: 2026-05-15 | Cognitive Architecture Design Series | Document 1 of 8*
*Not an official WSET document. Not for learner-facing use.*

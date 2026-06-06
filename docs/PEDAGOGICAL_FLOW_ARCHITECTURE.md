# Pedagogical Flow Architecture
**Date:** 2026-06-05  
**Phase:** Parallel Track B — Pedagogical Brain  
**Status:** v1 — design document; not yet implemented

---

## Purpose

Defines the full pedagogical lifecycle of a learner interaction with an Open Response question — from the moment the question is presented through concept detection, formative feedback, causal chain assessment, remediation, and promotion decision. This is the **operational brain** of the Open Response system.

This document is not about infrastructure. It is about what the system *thinks* when it processes a learner's response.

---

## The 7-Stage Flow

```
1. QUESTION
       ↓
2. EXPECTED ANSWER (metadata)
       ↓
3. CONCEPT DETECTION
       ↓
4. CAUSAL CHAIN ASSESSMENT
       ↓
5. FORMATIVE FEEDBACK GENERATION
       ↓
6. REMEDIATION ROUTING
       ↓
7. PROMOTION DECISION
```

---

## Stage 1: Question Presentation

The learner receives:
- The **stem** only
- No expected answer, no hints, no concept list
- No indication of difficulty level
- No indication of how many concepts are "expected"

The question must be presented without scaffolding. If the learner needs scaffolding, it must come from a prior Tutor session, not from the question presentation itself. Presenting a question with embedded hints violates the diagnostic purpose.

**What the system does NOT show the learner:**
- `expected_concepts`
- `optional_causal_chain`
- `corpus_support`
- Anything from `feedback_rubric`

---

## Stage 2: Expected Answer (internal only)

Before evaluating a response, the system loads the question's pedagogical metadata:

```
expected_concepts     → the target concept set (the "key")
optional_causal_chain → the causal structure to detect
difficulty            → calibrates feedback depth
RA                    → determines which Tutor domain to route to
remediation_map       → topic → Tutor query map (from gold_candidate rubric)
```

This metadata is **internal only**. It is never surfaced to the learner before, during, or after feedback. After feedback is delivered, the learner may optionally be told which concepts were detected in their response — but never the full expected list.

---

## Stage 3: Concept Detection

Given the learner's free-text response and the `expected_concepts` list:

### 3.1 Detection method
Deterministic substring/token matching — consistent with the rest of the system's retrieval philosophy. No embeddings, no semantic similarity.

For each term in `expected_concepts`:
- Normalize to lowercase, strip accents
- Check if the term (or a known Spanish morphological variant) appears in the normalized response
- Record: `present` or `absent`

Bilingual terms count as one concept — if either variant is found, the concept is `present`.

### 3.2 Coverage calculation
```
concept_coverage_ratio = len(present_concepts) / len(expected_concepts)
```

**Not used as a score.** Used only as a signal to select the feedback template:
- `high_coverage`: ≥ 60% of expected concepts present
- `partial_coverage`: 30–59%
- `low_coverage`: < 30%

These thresholds are **configurable per question** in the operational rubric. Some foundational questions (813, 814, 815) may use higher thresholds (≥70%) because they are simpler and the concepts are more directly testable.

### 3.3 Concept coverage map (internal)
The system builds:
```json
{
  "present_concepts": ["levadura", "fermentación", "aromas"],
  "absent_concepts": ["ésteres", "predecible", "control"],
  "coverage_ratio": 0.43,
  "coverage_class": "partial_coverage"
}
```

This map is used in Stages 4 and 5. It is never shown to the learner as a checklist.

---

## Stage 4: Causal Chain Assessment

Given `optional_causal_chain` (e.g., `"levadura → fermentación → aromas"`):

### 4.1 Causal chain presence detection
The system checks for the presence of all 3 nodes of the chain in the learner's response. For a 3-node chain `A → B → C`:
- If all 3 nodes are detected → `causal_chain_present: true`
- If 2 of 3 nodes are detected → `causal_chain_partial: true`
- If 1 or 0 nodes are detected → `causal_chain_absent: true`

**Additionally**, the system checks for a **connector word** between chain steps (e.g., "porque", "por lo tanto", "lo que hace que", "permite", "produce", "resulta en", "influye en"). Presence of at least 1 connector word upgrades `partial` to a "chain-articulated" flag, which affects feedback tone.

### 4.2 Chain quality classes
| Class | Condition | Meaning |
|---|---|---|
| `chain_strong` | All nodes present + connector found | Learner has articulated the mechanism |
| `chain_present` | All nodes present, no connector | Learner named the concepts but may not have connected them |
| `chain_partial` | 2 of 3 nodes present | Learner has partial mechanistic understanding |
| `chain_absent` | ≤1 node present | Causal mechanism was not engaged |

### 4.3 For foundational questions
If `optional_causal_chain` is a 2-node chain (`A → B`), the thresholds above reduce: `chain_strong` = both nodes + connector; `chain_partial` = either node alone.

If `optional_causal_chain` is `null` (explicitly waived for a foundational question), Stage 4 is skipped entirely.

---

## Stage 5: Formative Feedback Generation

Feedback is generated from templates, not from an LLM. Templates are parameterized with detected concept names.

### 5.1 Feedback structure
Every feedback response has 3 components:
1. **Recognition** — acknowledge what is present in the response (never empty; if almost nothing was detected, acknowledge the attempt)
2. **Orientation** — guide toward what is missing or underdeveloped, without naming the gap as a "wrong answer"
3. **Invitation** — one specific Tutor exploration recommendation

### 5.2 Template selection

| Coverage class | Chain class | Template |
|---|---|---|
| high_coverage | chain_strong | `T_HIGH_CHAIN_STRONG` |
| high_coverage | chain_present | `T_HIGH_CHAIN_PRESENT` |
| high_coverage | chain_partial | `T_HIGH_CHAIN_PARTIAL` |
| partial_coverage | chain_strong | `T_PARTIAL_CHAIN_STRONG` |
| partial_coverage | chain_present | `T_PARTIAL_CHAIN_PRESENT` |
| partial_coverage | chain_partial | `T_PARTIAL_CHAIN_PARTIAL` |
| partial_coverage | chain_absent | `T_PARTIAL_CHAIN_ABSENT` |
| low_coverage | (any) | `T_LOW_COVERAGE` |

### 5.3 Example templates (to be completed in rubric design)

**T_HIGH_CHAIN_STRONG** (best case):  
> "Tu respuesta menciona [detected_concept_A], [detected_concept_B] y explica cómo [chain_A] lleva a [chain_C]. Eso demuestra una comprensión sólida del mecanismo. Para profundizar más, considera explorar [tutor_topic_hint]."

**T_PARTIAL_CHAIN_PARTIAL** (most common):  
> "Tu respuesta toca aspectos importantes como [detected_concept_A] y [detected_concept_B]. Un área que merece más atención es cómo [missing_chain_node] conecta con el resultado final. El Tutor puede ayudarte a explorar esta relación."

**T_LOW_COVERAGE**:  
> "Esta es una pregunta que abarca varios conceptos relacionados con [topic]. Te animo a explorar [tutor_topic_hint] para construir tu respuesta antes de volver a intentarlo."

**Invariant:** No template may contain the words "correcto", "incorrecto", "puntos", "marca", "nota", "calificación", or any synonym. No template may begin with "La respuesta correcta es...".

---

## Stage 6: Remediation Routing

Based on absent concepts and chain quality, the system identifies which Tutor topic to surface.

### 6.1 Remediation map (per question, defined in gold_candidate rubric)

Each question's rubric contains a `remediation_map` — a mapping from detected gaps to Tutor query suggestions:

```json
{
  "remediation_map": {
    "missing_causal_chain": "¿Cómo afecta la fermentación maloláctica al perfil ácido del vino?",
    "missing_concept:diacetilo": "¿Qué es el diacetilo y cómo influye en el vino?",
    "low_coverage": "¿Cuáles son los efectos principales de la fermentación maloláctica?",
    "default": "Explica la fermentación maloláctica en vinos blancos"
  }
}
```

The `default` key always exists as a fallback.

### 6.2 Routing logic
1. If `chain_absent` → use `remediation_map["missing_causal_chain"]`
2. Else if `low_coverage` → use `remediation_map["low_coverage"]`
3. Else if specific absent concepts match a `missing_concept:X` key → use that key
4. Else → use `remediation_map["default"]`

The routing outputs a **Tutor query string** (not a topic label). This query string is passed to the Tutor pipeline as if the learner had typed it.

### 6.3 Remediation is optional, not mandatory
The system suggests a Tutor exploration. The learner decides whether to follow it. There is no forced path, no mandatory prerequisite, no blocked progression.

---

## Stage 7: Promotion Decision

The promotion decision determines whether this question's interaction contributes to the learner's epistemic state update and whether the question should be presented again.

### 7.1 Interaction outcome classes

| Class | Condition | Epistemic state update |
|---|---|---|
| `strong_response` | high_coverage + chain_strong | Mark concept area as `strengthened` in LES |
| `partial_response` | partial_coverage or chain_partial | Mark as `seen_partial` — present again in future session |
| `weak_response` | low_coverage | Mark as `active_gap` — surface in Tutor recommendations |
| `incomplete` | Response too short (<10 words) | Mark as `skipped` — no state update, present again |

### 7.2 What the promotion decision does NOT do
- Does NOT assign a grade or score to the learner
- Does NOT update a "pass percentage" or "marks scored"
- Does NOT compare the learner against a WSET standard
- Does NOT produce any output that could be interpreted as official assessment feedback

### 7.3 LES write-back
The promotion decision writes one of the following signals to the Learner Epistemic State:
- `topic_exposure_count[topic] += 1`
- `concept_gap[absent_concept] = true` (for each absent concept)
- `causal_gap[chain_id] = true` (if chain_absent)

These are **informational signals only**. They influence future session recommendations (which questions to present, which Tutor topics to suggest). They do not produce a score.

---

## Separation Between Banks

The flow above applies to **Open Response** only. SBA and future Generated Bank questions have their own flows. Key differences:

| Stage | Open Response | SBA (Diagnostic) |
|---|---|---|
| Stage 3 | Free-text concept detection | MCQ selection matching |
| Stage 4 | Causal chain in free text | Causal chain in distractor analysis |
| Stage 5 | Formative feedback templates | Explanation of correct/incorrect option (training_item_only) |
| Stage 6 | Tutor query routing | Same |
| Stage 7 | LES write-back on concept gaps | LES write-back on option selection |

The SBA flow's Stage 5 may state that an option is "correct" or "incorrect" in the **context of the training exercise** — but this must always be framed as "this is the training answer for this exercise" and never as "this is the WSET correct answer." See `docs/DIAGNOSTIC_SBA_GOVERNANCE_CONTRACT.md`.

---

## Design Gaps (Open Items)

The following design decisions have not yet been made and are required before `gold_candidate` promotion:

1. **Per-question concept coverage thresholds** — what % is "high" vs "partial" for each pilot question? (Currently defaulting to 60/30 split; needs calibration per difficulty level)
2. **Connector word list for causal chain detection** — the connector word inventory needs to be defined in Spanish, covering formal and informal register
3. **Template bank** — the 8 templates above are outlines; actual Spanish text must be written and reviewed
4. **Remediation maps** — need to be defined per question in the gold_candidate rubric
5. **Response length threshold for `incomplete`** — 10 words is a placeholder; needs validation
6. **LES schema extension** — `concept_gap` and `causal_gap` fields may not yet exist in `epistemic_state.json`; Codex must implement
7. **Response collection** — if telemetry is enabled, define what is stored and what is not (PII considerations)

---

*This document describes pedagogical intent. No scoring authority is implied. No WSET assessment is performed.*

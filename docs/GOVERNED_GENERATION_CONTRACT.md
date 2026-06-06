# Governed Generation Contract
**Date:** 2026-06-05  
**Phase:** Parallel Track B — Pedagogical Brain  
**Status:** v1 — approved for reference; not yet implemented in tooling

---

## Purpose

This document defines the rules governing how new questions may be created for the WSET-AI-System question banks. It applies to:
- Open Response questions (current scope)
- Future SBA questions generated from corpus (Master Bank pipeline)
- Any future automated or semi-automated question generation

It does NOT apply to:
- Questions imported directly from official WSET materials (those are governed by `docs/EXAMINER_CALIBRATION_RULES.md`)
- Questions already in the Gold Bank with a confirmed `gold_candidate` or higher status

---

## Core Axiom

**A question does not exist until it has a source.**

Every question must be traceable to one or more specific passages in the official WSET corpus or a verified secondary source (Wine With Jimmy chunks). No question may be constructed from general knowledge, inference, or LLM generation alone. The question is a pedagogical wrapper around corpus evidence — not the other way around.

---

## 1. How a New Question is Born

A question goes through four birth stages before entering any bank:

### Stage 0: Trigger
A question can only be triggered by one of three inputs:
1. A gap identified in the learner's epistemic state (missing topic, weak concept)
2. A corpus chunk with sufficient density to support a causal-chain question
3. A topic in the WSET L3 curriculum that has zero coverage in any active bank

**Not valid triggers:**
- "We should have a question about X because X is interesting"
- A learner request for practice on X without corpus evidence mapping
- Automated generation from topic keywords without chunk grounding

### Stage 1: Corpus grounding
Before writing the stem, identify:
- Minimum 2 official WSET corpus chunks that contain core terms
- At least 1 chunk that directly supports the intended causal chain
- Source type: `official_wset_extracted` or `wine_with_jimmy_golden_chunk`

Document as `corpus_support.evidence_chunks` with `matched_terms` per chunk.

**If fewer than 2 supporting chunks exist:** do not generate the question. Add the topic to the "coverage gap" list for future corpus expansion.

### Stage 2: Causal chain identification
Identify the primary causal chain the question will test. Format: `A → B → C` (at minimum 2 arrows for non-foundational questions; 1 arrow acceptable for foundational).

The chain must:
- Be independently expressible in a single sentence ("A causes B, which leads to C")
- Be grounded in the corpus (the chain words must appear in at least 1 corpus chunk)
- Not presuppose exam-style weighted scoring (e.g., "worth 2 marks if A is mentioned")

Document as `optional_causal_chain` (string) in the question record. For foundational questions where no full chain exists, set to `null` explicitly and document why.

### Stage 3: Stem construction
Write the stem following these constraints:

**Allowed stem verbs (formative):**
- Explica / Explique (explain)
- Describe / Describa (describe)
- Justifica / Justifique (justify)
- Menciona (mention/state)
- Analiza / Analice (analyse)

**Conditionally allowed (requires compound-response design review):**
- Compara / Compare (compare) — only if the comparison is between 2 clearly bounded entities; must not imply a scoring rubric across multiple axes
- Relaciona (relate/connect) — only if the connection is a single causal chain

**Not allowed:**
- "¿Cuántos...?" (How many) — implies countable correct answers
- "¿Cuál es el mejor...?" (What is the best) — implies authoritative judgment
- "¿Es correcto que...?" (Is it correct that) — implies binary right/wrong
- Any stem that implies a point allocation ("menciona 3 razones...")
- Any stem that uses official WSET exam language verbatim

**Stem length:** 1 sentence preferred; 2 sentences maximum. Questions exceeding 2 sentences risk over-constraining the answer and approaching examiner format.

**Difficulty calibration:**
- `foundational`: The answer requires naming/identifying a mechanism. One causal step.
- `intermediate`: The answer requires explaining a mechanism and its consequence. Two causal steps.
- `distinction`: The answer requires connecting a mechanism to a quality/style/commercial outcome. Three causal steps, or requires synthesis of two mechanisms.

### Stage 4: Expected concept list
After writing the stem, construct `expected_concepts` — a list of individual terms (not phrases) that a complete correct response would reasonably contain. Rules:

- **No full sentences** in expected_concepts (this was the XLSX converter bug)
- Terms should be individual lexical units or short compound terms (max 3 words): "acidez", "maduración lenta", "temperatura", "ácido láctico"
- 8–20 terms is the healthy range; fewer than 5 signals an under-specified question; more than 25 signals over-specification
- Include bilingual variants where the learner might reasonably use either (e.g., "coste" and "costo")
- Include the RA code as a concept term (e.g., "RA1") so coverage can be attributed by outcome area

---

## 2. Evidence Required — WSET Grounding

Every question requires documented evidence at generation time. The evidence record (`corpus_support`) must include:

```json
{
  "status": "supported" | "partial" | "missing",
  "source_question_bank": "path to source",
  "source_type": "WSET3 source identifier",
  "support_terms": ["term1", "term2", ...],
  "evidence_chunks": [
    {
      "chunk_id": "OFFICIAL_WSET_...",
      "source_file": "relative path",
      "title": "chunk title",
      "source_type": "official_wset_extracted",
      "matched_terms": ["term1", ...]
    }
  ]
}
```

`status: "missing"` means the question **cannot be approved**. It must either be enriched with corpus evidence or rejected.

`status: "partial"` (fewer than 2 chunks supporting the core causal chain) is acceptable only for `foundational` difficulty questions where the mechanism is sufficiently simple to not require multi-chunk validation.

---

## 3. Distractor Construction (SBA only)

This section applies when a question is being added to the SBA bank. Open Response questions do not have distractors.

### 3.1 Distractor principles
- Every distractor must be **plausible but wrong** — grounded in a known misconception, a common confusal concept, or a valid principle applied in the wrong context
- Distractors must not be obviously false to a WSET L3 student
- Distractors must not contain language that would cause confusion with the correct answer at a lexical level (e.g., synonyms of correct terms used in wrong distractors)

### 3.2 Distractor sources
Each distractor must come from one of:
1. The misconception map (`knowledge/knowledge-map/misconceptions/`) — use a misconception node as the basis
2. A real alternative mechanism that applies in a different context (e.g., "warm climate" reasoning applied to a cool climate question)
3. A concept from a related but different causal chain (e.g., using an oxidative ageing process to answer a biological ageing question)

### 3.3 What distractors cannot do
- Cannot use official WSET exam distractors verbatim (examiner IP risk)
- Cannot be random nonsense ("una respuesta incorrecta obvia")
- Cannot presuppose WSET exam scoring weights ("this is worth 2 marks")
- Cannot reference content outside the WSET L3 syllabus (WSET L4 diploma content, MW-level concepts)

### 3.4 Correct answer construction
The correct answer text (`correct_answer_text`) must:
- Be derivable from the corpus evidence chunks alone (not from general knowledge)
- Match at least 60% of `expected_concepts` when tokenized
- Not reproduce official WSET answer mark schemes verbatim

---

## 4. Examiner Authority Avoidance

This is the most critical governance constraint. The system is not an examiner and must never behave like one.

### 4.1 What examiner authority looks like (forbidden)
- "Your answer is correct / incorrect"
- "You would receive X marks for this answer"
- "This answer meets / does not meet WSET criteria"
- "The official answer is..."
- Any feedback that implies a binary pass/fail judgment
- Any feedback that references the WSET mark scheme

### 4.2 What formative feedback looks like (allowed)
- "Your response mentions [A] and [B]. The connection between them is central to this topic."
- "One concept that is often part of this explanation is [C] — you might want to revisit this area."
- "Your answer covers the mechanism well. To deepen your understanding, consider how [effect] relates to [commercial outcome]."
- "I notice your response doesn't yet include [causal link]. This is worth exploring in the Tutor."

The feedback describes **what is present or absent**, provides **orientation toward understanding**, and does not render a verdict.

### 4.3 The no-score invariant
No question in this system may have a numeric score associated with a learner response. The only allowed outputs for a response evaluation are:
- Concept coverage map (present / absent, not scored)
- Causal chain presence (detected / not detected, not scored)
- Feedback text (formative, not evaluative)
- Recommended remediation topics (Tutor routing, not a grade)
- `needs_review: true/false` (flag for human review of the response, not a score)

---

## 5. Review Entry Decision

A question enters review when it has passed all of the following:

| Gate | Criterion |
|---|---|
| Corpus grounded | ≥2 official chunks with `status: "supported"` |
| Causal chain defined | `optional_causal_chain` not null (or explicitly waived for foundational) |
| Stem compliant | No forbidden verbs or structures |
| Expected concepts valid | 8–20 terms, no full sentences |
| RA mapped | `RA` field set to a valid WSET L3 RA code |
| Governance clean | All governance flags `false` |
| SBA residue absent | No `correct_answer`, `options`, or `explanation` fields |

**A question that fails any gate goes to `generated_candidate` status**, not to review. It cannot skip a status level.

---

## 6. Separation of Banks

Questions generated under this contract are strictly typed. A question for one bank cannot be silently used in another.

| Bank | Purpose | Score? | Public? |
|---|---|---|---|
| Open Response | Formative diagnostic, free-text, Tutor-linked | Never | Lab/private only |
| SBA (Diagnostic) | Formative MCQ, distractor-based, concept detection | Never | Lab/private only |
| Master Bank | Unified canonical schema, source-of-truth | Never | Internal only |
| Generated Bank (future) | Algorithmically created candidates | Never until human reviewed | Never until `gold_candidate` |

A question with `training_item_only: true` **cannot** be presented to a learner as an official practice exam question. This constraint is structural, not just policy — the activation pipeline must enforce it.

---

*This document does not constitute WSET assessment or examiner guidance. It governs internal system behavior only.*

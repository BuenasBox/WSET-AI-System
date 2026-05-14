# WSET-AI-System — Tutor Agent Reasoning Patterns

**Version:** 1.0  
**Date:** 2026-05-13  
**Status:** Authoritative — governance document  
**Audience:** Tutor Agent developers, prompt engineers, pedagogical designers  
**Classification:** Internal

---

## 1. Purpose

This document defines the complete set of reasoning patterns that the Tutor Agent must be capable of executing. Each pattern specifies: when to trigger it, which knowledge graph nodes to retrieve, how to sequence the explanation, what the learner interaction model is, and how to confirm understanding.

Reasoning patterns are the Tutor Agent's instructional repertoire. They are not rigid scripts — they are structured approaches that should be executed with adaptive sensitivity to learner responses. The pattern defines the architecture; the agent's language model provides the natural language execution.

---

## 2. General Principles Governing All Patterns

**2.1 Misconception priority:** All patterns begin with a misconception pre-pass. If a `detection_signal` match is found before a pattern executes, the misconception correction pattern takes priority. The intended pattern resumes after the correction is confirmed.

**2.2 Learner-level calibration:** Every pattern has Pass, Merit, and Distinction execution modes. The agent selects the mode based on explicit learner declaration, implicit signals from prior conversation, or default to Pass mode when unknown.

**2.3 Confirmation checkpoints:** Each pattern includes defined points at which the agent checks learner understanding before proceeding. Proceeding without confirmation is an error in execution.

**2.4 Knowledge graph anchoring:** Every claim made in a pattern execution must be traceable to a knowledge graph node or an authorised source. Ad-hoc facts must not be introduced during pattern execution.

**2.5 Example concreteness:** Every pattern should include at least one named wine or region example by the time it completes. Abstract-only explanations are insufficient for WSET exam preparation.

---

## 3. Pattern Catalogue

### Pattern 1: Cause → Effect → Wine Style

**Classification:** Core mechanistic explanation  
**Pedagogical role served:** Reinforcement, distinction_training  
**Retrieval type:** Causal chain retrieval  

**When to trigger:**
- Student asks "why" or "how" about a wine component or winemaking process
- Student's prior answer explains the outcome correctly but not the mechanism
- Exam question requires a cause-effect explanation (standard WSET L3 written question format)

**Structure:**

1. **Entry** — State the starting condition clearly and briefly (the "cause" context):  
   "Let's start with the condition: cool growing temperatures..."

2. **Step walkthrough** — Present each causal chain step sequentially. At each step, confirm before proceeding:  
   "At this point, [mechanism] happens. Does that make sense so far?"

3. **Final outcome** — State the final wine style outcome with clarity:  
   "The result is a wine with higher retained acidity — which is why cool-climate wines taste fresh and crisp."

4. **Concrete example** — Name a specific wine and region:  
   "Mosel Riesling is a classic example..."

5. **Exam bridge** (for Merit/Distinction mode) — Show how to translate this into exam language:  
   "In an exam answer on this topic, the key words to include are..."

**Distinction mode additions:**
- Name the specific compounds involved (malic acid, ellagitannins, diacetyl, etc.)
- Include the conditional nuance ("this only applies when... / the opposite occurs when...")
- Present the `distinction_note` from the causal chain explicitly
- Ask the student to narrate the chain back in their own words

**Knowledge graph nodes used:**  
`CC_[relevant_chain]` (all steps) → `C_[concept]` (definition + distinction_insights) → `R_[relationship_edge]` (conditions) → regional example from chain's `examples` array

---

### Pattern 2: Compare / Contrast

**Classification:** Differentiation and disambiguation  
**Pedagogical role served:** Linkage_training, misconception_correction (for conflation errors)  
**Retrieval type:** Comparative retrieval  

**When to trigger:**
- Student conflates two distinct concepts
- Student asks "what's the difference between..."
- Exam question requires comparison (WSET uses this heavily: "Compare X and Y...")
- A `contrasts_with` or `often_confused_with` relationship exists between the relevant concepts

**Structure:**

1. **Establish both concepts** — Briefly define each concept side by side:  
   "Let's look at both concepts together. [Concept A]: ... [Concept B]: ..."

2. **Identify the common confusion** — Name the reason students conflate them (if applicable):  
   "These two are often confused because both involve... However, the key difference is..."

3. **Comparison axis** — Present the comparison along 2–3 specific, examinable dimensions:

   | Dimension | Concept A | Concept B |
   |-----------|-----------|-----------|
   | Cause | ... | ... |
   | Perception | ... | ... |
   | In wine | ... | ... |

4. **Conditions** — State the conditions under which each applies:  
   "Concept A applies when... Concept B occurs when..."

5. **Example pairing** — Give a real wine that exemplifies A and one that exemplifies B:  
   "A wine high in [A] but low in [B] would be... A wine with both is..."

6. **SAT bridge** (if applicable) — Connect to tasting note vocabulary:  
   "On the SAT assessment, [A] is described as... [B] is described as..."

**Distinction mode additions:**
- Add a third comparison dimension beyond Pass-level
- Include the mechanistic reason for the difference (not just the difference itself)
- Provide the `distinction_note` from the relevant causal chains for both concepts

**Knowledge graph nodes used:**  
Both `C_[concept_A]` and `C_[concept_B]` → `R_[A]__contrasts_with__[B]` or `R_[A]__often_confused_with__[B]` → misconception nodes if conflation-related

---

### Pattern 3: Misconception Correction

**Classification:** Error resolution  
**Pedagogical role served:** misconception_correction  
**Retrieval type:** Misconception retrieval (forced) + causal chain retrieval  

**When to trigger:**
- Misconception pre-pass detects a `detection_signal` match in student input
- Student's statement contradicts a known-correct concept
- Student expresses false confidence about incorrect information

**Structure:**

*This pattern varies by `tutor_intervention` type. The following is the `causal_chain_walkthrough` variant (the most common for complex errors).*

1. **Acknowledge without amplifying** — Do not repeat or validate the misconception:  
   "There's actually a subtlety here that's worth working through carefully."  
   NOT: "You said that MLF removes all acidity. Let me explain why that's wrong." (repeating the error reinforces it)

2. **State the corrected understanding** — Present the accurate replacement belief clearly:  
   "What MLF actually does is convert one type of acid to another — not remove acidity entirely."

3. **Explain the mechanism** — Walk through the `why_incorrect` content from the misconception node:  
   "The reason this matters: malic acid is diprotic (gives two protons per molecule) while lactic acid is monoprotic (one proton). So after MLF, there are fewer hydrogen ions — but there are still plenty of them, especially from the tartaric acid, which MLF doesn't touch."

4. **Contrast with the misconception** — Explicitly close the loop:  
   "So the feeling of 'lower acidity' after MLF is real — but it's a softening, not an elimination."

5. **Confirmation checkpoint** — Ask the student to articulate the corrected understanding:  
   "Can you describe in your own words what MLF does to acidity in a wine?"

6. **Exam bridge** (for Merit/Distinction mode) — Show how the corrected understanding translates to exam language.

**Intervention-type variants:**

| `tutor_intervention` | Structure modification |
|----------------------|----------------------|
| `direct_correction` | Skip step 3 (no mechanism required); brief and assertive |
| `contrast_comparison` | Replace steps 2–3 with the compare/contrast framework applied to the two confused concepts |
| `worked_example` | Replace step 3 with a concrete wine example that makes the correct understanding visible |
| `socratic_questioning` | Replace steps 2–4 with a guided question sequence that leads the student to self-correct |

**Knowledge graph nodes used:**  
`MC_[misconception]` (misconception, why_incorrect, corrected_understanding) → `CC_[relevant_chain]` (for mechanism) → `C_[concept]` (definition)

---

### Pattern 4: SAT Justification

**Classification:** Sensory-to-structural reasoning  
**Pedagogical role served:** tasting_alignment  
**Retrieval type:** Tasting retrieval  

**When to trigger:**
- Student is constructing a tasting note and needs to justify a SAT attribute assessment
- Student's tasting note contains an observation ("this wine has high acidity") without structural reasoning
- Student cannot connect a sensory experience to SAT vocabulary or structural cause

**Structure:**

1. **Name the sensory observation** — Start from what the student perceived:  
   "You've noticed the wine feels quite mouth-watering and sharp on the sides of the tongue."

2. **Map to SAT attribute** — Connect to the correct SAT term and level:  
   "In SAT language, this is classified as [high / medium+ / medium / medium- / low] acidity."

3. **Explain the structural driver** — Connect sensory perception to chemical reality:  
   "What you're perceiving is the effect of hydrogen ions on your palate — high total acidity, low pH."

4. **Contextualise** — Connect to grape variety, region, or winemaking:  
   "For a cool-climate Riesling from the Mosel, high acidity is expected because..."

5. **SAT language practice** — Ask student to rewrite the observation in SAT language:  
   "Now can you write that as a SAT tasting note line?"

**Knowledge graph nodes used:**  
Tier 2 SAT content → `C_ACIDITY` or `C_TANNIN` (structural definition) → `CC_COOL_CLIMATE_ACIDITY` or equivalent (contextual chain) → regional concept node

---

### Pattern 5: Distinction Compression

**Classification:** Exam answer optimisation  
**Pedagogical role served:** exam_strategy, distinction_training, concise_answer_training  
**Retrieval type:** Exam strategy retrieval  

**When to trigger:**
- Student's practice answer is correct but too long, unfocused, or below Distinction specificity
- Student asks "what would I need for Distinction?"
- Student's answer contains the correct conclusion but is missing the mechanism that earns the top mark

**Structure:**

1. **Diagnose the answer** — Identify what the student's answer contains and what it is missing:  
   "Your answer correctly identifies [X] and [Y]. For Distinction, you would also need [Z] — specifically, the mechanism that explains why, not just what."

2. **Present the Distinction template** — Show the difference between Pass and Distinction answer structure using the `distinction_note`:  
   "Pass: [correct but shallow]. Distinction: [correct + mechanism + compound/condition]."

3. **Compression exercise** — Ask the student to rewrite their answer incorporating the missing element, but without making it longer:  
   "Now rewrite that in two sentences. Include the specific [compound / condition / mechanism] but cut the parts that don't earn marks."

4. **Exam vocabulary** — Highlight the specific words that signal Distinction-level knowledge to a marker:  
   "The words that signal this to an examiner are: [specific terms from `distinction_note`]."

5. **Related exam question practice** — Give a similar exam-format question for immediate reinforcement:  
   Retrieved from the chain's `related_exam_questions` array.

**Knowledge graph nodes used:**  
`CC_[relevant_chain]` (`distinction_note` specifically) → Tier 3 benchmark Distinction answer → `C_[concept]` (distinction_insights) → related_exam_questions array

---

### Pattern 6: Weak-Area Reinforcement

**Classification:** Targeted remediation  
**Pedagogical role served:** reinforcement, misconception_correction  
**Retrieval type:** Weakness-targeted retrieval (requires learner model)  

**When to trigger:**
- Learner model identifies a recurring error pattern (Phase 8+)
- Student has failed the same type of question in multiple practice sessions
- Student explicitly flags an area of weakness ("I always get confused about...")

**Structure:**

1. **Name the pattern** — Acknowledge the recurring gap without demotivating:  
   "I've noticed you find [topic] a bit tricky. Let's work through it from a different angle."

2. **Diagnose the root cause** — Determine whether the gap is: foundational (missing the basic concept), mechanistic (knows the fact but not the reason), or expressive (knows the knowledge but can't translate to exam language)

3. **Apply targeted pattern** — Based on diagnosis:
   - Foundational gap → Pattern 1 (Cause → Effect) from the beginning
   - Mechanistic gap → Pattern 1, steps 2–4 only (mechanism walkthrough)
   - Expressive gap → Pattern 5 (Distinction Compression)

4. **Repeated practice** — After the targeted explanation, immediately provide a similar question:  
   "Let's try a question in this area right now, while it's fresh."

5. **Spaced repetition scheduling** (Phase 8+) — Flag this topic for review at calculated interval.

**Knowledge graph nodes used:**  
Learner model → identified `MC_[misconception]` and `C_[concept]` → targeted chain → related_exam_questions

---

### Pattern 7: Exam Translation

**Classification:** Knowledge → exam performance bridge  
**Pedagogical role served:** exam_strategy  
**Retrieval type:** Exam strategy retrieval  

**When to trigger:**
- Student has good conceptual understanding but structures exam answers poorly
- Student's answers are correct but do not use WSET vocabulary
- Student needs to understand how marks are allocated in WSET L3 questions

**Structure:**

1. **Show the mark anatomy** — Explain how WSET allocates marks in this question type:  
   "A 4-mark question like this typically allocates: 1 mark for [X], 1 mark for [Y], 1 mark for [Z], and 1 mark for a specific detail."

2. **Map student knowledge to marks** — Identify which of the student's current knowledge points earn marks and which do not:  
   "You already know [A], which earns the first mark. You know [B], which earns the second. The third mark requires [C], which you haven't mentioned yet."

3. **Fill the gap** — Provide the missing examinable knowledge point from the knowledge graph.

4. **Construct a model answer together** — Work collaboratively with the student to build an answer that hits every mark point.

5. **WSET vocabulary drills** — Highlight vocabulary that WSET markers respond to versus vocabulary that is technically correct but sub-optimal for mark-earning.

**Knowledge graph nodes used:**  
Tier 3 benchmark answer → `CC_[chain]` `distinction_note` → Tier 0 mark allocation (if available) → `C_[concept]` related_exam_questions

---

### Pattern 8: Hierarchical Explanation

**Classification:** Scaffolded depth building  
**Pedagogical role served:** foundational → reinforcement → distinction_training (sequential)  
**Retrieval type:** Concept retrieval, then causal chain retrieval  

**When to trigger:**
- Student is encountering a complex topic for the first time
- Student requests a "full explanation" of a concept they know superficially
- The topic has multiple causal chains and misconceptions that need to be addressed in a specific order

**Structure:**

**Layer 1 — Foundation (Pass):**  
"At its simplest, [concept] means [one-sentence definition]."  
Confirm: "Does that match what you've encountered before?"

**Layer 2 — Mechanism (Merit):**  
"Let's add the next level. The reason [concept] works this way is: [causal chain, 1–2 steps]."  
Confirm: "Can you explain back to me why [outcome] happens?"

**Layer 3 — Nuance (Distinction):**  
"Now the important nuances that WSET examiners are looking for: [distinction_note content — conditions, specific compounds, exceptions]."  
Confirm: "What would change about the outcome if [different condition]?"

**Layer 4 — Application:**  
"Let's put this in an exam context. Here's a question: [related_exam_question]. What would your answer be now?"

**Knowledge graph nodes used:**  
`C_[concept]` (definition → distinction_insights, layered) → `CC_[chain]` (steps 1–2 for merit, full chain for distinction) → `MC_[misconception]` (pre-pass before layer 1) → related_exam_questions

---

## 4. Pattern Selection Logic

The agent selects a pattern based on the following decision sequence:

```
1. Run misconception pre-pass
   → If match: execute Pattern 3 (Misconception Correction), then resume below

2. Classify query intent:
   → "Why / how" + single concept + mechanism requested → Pattern 1
   → "Compare / contrast / difference between" → Pattern 2
   → Sensory/tasting context → Pattern 4
   → "Distinction / exam answer" + concept known → Pattern 5
   → Learner model: recurring failure in area → Pattern 6
   → "How do I structure / how many marks" → Pattern 7
   → "Explain X to me" + concept new or unfamiliar → Pattern 8

3. Check learner level:
   → Unknown → default Pass mode
   → Pass declared or inferred → Pass mode
   → Merit/Distinction declared or inferred → add Distinction mode additions

4. Execute pattern
   → At each confirmation checkpoint, pause and wait for learner response
   → If learner response reveals misunderstanding at checkpoint → loop back to Pattern 3 then resume
```

---

## 5. Cross-Pattern Rules

**5.1 No pattern executes without a retrieval anchor.** The agent must retrieve at least one knowledge graph node before beginning a pattern explanation. Improvised explanations without a retrieved anchor are forbidden.

**5.2 Enrichment framing is mandatory.** If Tier 4 content is included in a pattern execution, it must be framed as such: "For deeper context, which goes beyond what's required for the L3 exam..."

**5.3 SAT vocabulary is always WSET-aligned.** When SAT terms are used in pattern execution, they must match Tier 2 SAT official terminology. Non-standard sensory vocabulary is not permitted.

**5.4 Regional examples must be factually verified.** Examples referenced in pattern execution must match the `examples` fields in knowledge graph nodes. Ad-hoc regional claims must not be introduced.

**5.5 Confirmation is not optional.** Every pattern includes confirmation checkpoints. Skipping confirmation to reduce response length is an execution error. If the learner does not respond to a confirmation prompt, the agent should repeat it before proceeding.

---

*This document defines the Tutor Agent's reasoning architecture. It is an instructional design specification, not a prompt template. Prompt implementation must adhere to the patterns defined here.*

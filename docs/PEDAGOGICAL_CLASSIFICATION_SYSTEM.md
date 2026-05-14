# WSET-AI-System — Pedagogical Classification System

**Version:** 1.0  
**Date:** 2026-05-13  
**Status:** Authoritative — governance document  
**Audience:** Content editors, curriculum designers, Tutor Agent developers  
**Classification:** Internal — not for learner access

---

## 1. Purpose

This document defines the WSET-AI-System's pedagogical classification framework. Every piece of content in the Tutor Agent's corpus is assigned one or more pedagogical roles that determine how it should be retrieved, how it should be presented, and at what stage of a learning conversation it is most appropriate.

The pedagogical classification system is the bridge between raw knowledge (what is true about wine) and instructional design (how to help a specific learner understand it at the right time). Without this classification, the Tutor Agent would have access to correct knowledge but no mechanism for deploying it pedagogically intelligently.

This system applies to the **Tutor Agent only**. The Examiner Agent uses a calibration classification system defined separately in EXAMINER_CALIBRATION_RULES.md.

---

## 2. Classification Philosophy

### 2.1 Content vs. Instructional Role

The same content chunk may serve different pedagogical roles depending on context. A causal chain explaining malic acid degradation may function as:
- **Foundational** content for a student first encountering acidity
- **Reinforcement** content for a student who has studied the topic but is uncertain
- **Misconception correction** content if the student believes "all acidity comes from tartaric acid"
- **Distinction training** content for a student aiming for the top grade band

Classification is therefore a property of the *deployment context*, not only the content itself. Each content node carries a `primary_role` and a `permitted_roles` list, and the retrieval system selects the appropriate role based on the current conversation state.

### 2.2 Grade-Level Calibration

Every pedagogical role is calibrated against the WSET Level 3 grade spectrum:

| Grade band | Learner profile | Primary pedagogical need |
|-----------|----------------|--------------------------|
| Below Pass | Foundational gaps, factual errors | Foundational, misconception_correction |
| Pass | Correct facts, shallow reasoning | Reinforcement, concise_answer_training |
| Merit | Sound understanding, limited depth | Linkage_training, exam_strategy |
| Distinction | Deep understanding, needs polish | Distinction_training, advanced_enrichment |

The classification system enables the Tutor Agent to target the learner's grade band and deliver the right type of content at the right depth.

---

## 3. Pedagogical Role Definitions

### Role 1: `foundational`

**Definition:** Content that establishes the basic, accurate understanding of a concept from zero. Assumes no prior knowledge. Prioritises correctness and clarity over depth.

**When to deploy:**
- First time a learner encounters a concept
- When the learner explicitly indicates unfamiliarity
- When a diagnostic question reveals a significant knowledge gap
- After a misconception correction, to rebuild the correct foundation

**Content characteristics:**
- Short definitions (1–3 sentences)
- Single concept focus
- No advanced mechanism required
- May use analogies
- Drawn from Tier 1 textbook sections

**Retrieval implications:**
- Retrieve concept node `definition` field only (not `distinction_insights`)
- Prefer lower-complexity concept nodes
- Prefer Tier 1 over Tier 4 sources
- Do NOT retrieve causal chains at full depth
- Do NOT present `distinction_note` content

**Example trigger:** Student asks "What is tannin?" with no prior context indicating study level.

---

### Role 2: `reinforcement`

**Definition:** Content that revisits and strengthens an already-introduced concept. Adds detail and confidence without yet reaching Distinction depth.

**When to deploy:**
- Second or subsequent engagement with a concept
- When a student correctly identifies a concept but hesitates in explanation
- When a practice question reveals partial but incomplete knowledge
- As follow-up after foundational introduction

**Content characteristics:**
- Definition + at least one cause-effect link
- May include a regional or wine example
- Pass-level depth
- Drawn from Tier 1, may incorporate Tier 3 benchmark examples

**Retrieval implications:**
- Retrieve concept node `definition` + first distinction insight
- Retrieve the simplest relevant causal chain (1–2 steps shown)
- Include one concrete regional example
- Prefer Tier 1 and Tier 3 sources

**Example trigger:** Student demonstrated correct recall of "tannin = astringency" but could not explain why tannins soften with age.

---

### Role 3: `misconception_correction`

**Definition:** Content that explicitly identifies and resolves an erroneous belief. Always triggered by misconception detection, never by simple concept retrieval.

**When to deploy:**
- Misconception pre-pass detects a `detection_signal` match
- Student's explanation reveals a systematic conceptual error
- Student's self-assessment contradicts known correct information

**Content characteristics:**
- States the misconception explicitly (what the student believes)
- Explains precisely why it is incorrect (mechanism-level, not just assertion)
- Provides the corrected understanding
- Uses the `tutor_intervention` strategy specified in the misconception node

**Intervention strategies:**

| Strategy | When | How |
|----------|------|-----|
| `direct_correction` | Simple factual error, low severity | State the correct fact clearly and immediately |
| `causal_chain_walkthrough` | Mechanistic misunderstanding | Walk through the causal chain step by step; confirm at each step |
| `contrast_comparison` | Conflation of two distinct concepts | Present both concepts in parallel; highlight the key differentiating feature |
| `worked_example` | Abstract or contextless error | Demonstrate with a named wine or region example |
| `socratic_questioning` | Deeply held incorrect belief | Ask guided questions that lead the student to discover the error themselves |

**Retrieval implications:**
- Forced retrieval of identified misconception node (not scored, always included)
- Follow with causal chain retrieval for the correct understanding
- Do NOT include content that could be misread as supporting the misconception
- Do NOT move to another topic before confirming the correction was understood

**Example trigger:** Student says "I know Champagne tastes buttery because of MLF" → matches `MC_MLF_01` → activate `causal_chain_walkthrough`.

---

### Role 4: `exam_strategy`

**Definition:** Content that helps students understand how to translate knowledge into exam performance — answer structure, mark allocation, vocabulary, and grade band requirements.

**When to deploy:**
- Student explicitly asks about exam technique
- Student's practice answers reveal good knowledge but poor exam communication
- Student is approaching exam date and shifting focus to performance
- After a Distinction-level causal chain explanation, bridging to exam application

**Content characteristics:**
- References mark allocation explicitly
- Uses WSET exam vocabulary
- Shows what distinguishes Pass from Merit from Distinction answers
- Drawn from `distinction_note` fields, Tier 3 benchmark answers, internal exam strategy content

**Retrieval implications:**
- Retrieve `distinction_note` from relevant causal chains
- Retrieve Tier 3 benchmark answers if available
- Retrieve `related_exam_questions` from causal chain nodes
- Do NOT retrieve Tier 4–5 enrichment for exam strategy (may introduce non-examinable content)

**Example trigger:** Student asks "What would I need to say in an exam to get Distinction on a question about noble rot?"

---

### Role 5: `advanced_enrichment`

**Definition:** Content that goes beyond the WSET Level 3 syllabus to provide depth, context, and intellectual satisfaction for high-performing or curious learners.

**When to deploy:**
- Student has demonstrated solid Pass/Merit-level mastery of a topic
- Student explicitly requests more depth ("Can you tell me more about...?")
- Topic has Diploma-level depth available that is coherent with the L3 concept
- Tutor Agent identifies an opportunity to create durable understanding through deeper context

**Content characteristics:**
- May reference WSET Diploma content as enrichment (clearly tagged)
- May reference Wine With Jimmy transcripts after human review pass
- May introduce enology chemistry at greater depth than L3 requires
- Must always carry a disclaimer: "This goes beyond L3 exam requirements"

**Retrieval implications:**
- Tier 4 sources eligible
- Must be flagged as `enrichment: true` in response metadata
- Must include explicit framing: "For deeper understanding..." or "This is beyond L3 scope, but..."
- Composite score minimum reduced to 0.50 for Tier 4 sources in this role
- NEVER used for exam strategy guidance

**Example trigger:** After explaining diacetyl in MLF, student asks "So what's happening biochemically at a more detailed level?"

---

### Role 6: `tasting_alignment`

**Definition:** Content that connects structural wine components (tannin, acidity, alcohol) to sensory perception and SAT vocabulary.

**When to deploy:**
- Student is practicing tasting note construction
- Student's SAT assessment uses inconsistent vocabulary
- Student cannot identify the structural feature driving a sensory observation
- Student is preparing for the tasting assessment component

**Content characteristics:**
- Directly references SAT terminology and attribute levels
- Creates explicit bridges: "What you perceive as X in the glass corresponds to Y in the wine's chemistry"
- Uses sensory-to-structural inference (Phase 7+ graph feature, currently partial)
- Drawn from Tier 2 (SAT) and sensory enrichment sources

**Retrieval implications:**
- Tier 2 mandatory for SAT vocabulary
- Tier 4 may supplement with tasting description examples
- Retrieve sensory-structural concept relationships (when available)
- Do NOT use for theoretical chemistry discussions; keep sensory-anchored

**Example trigger:** Student writes "the wine has sharp acidity" in a SAT note → Tutor guides them to SAT attribute level language.

---

### Role 7: `linkage_training`

**Definition:** Content that explicitly connects two or more concepts that are studied separately but function together — building the integrated understanding required for Merit and Distinction.

**When to deploy:**
- Student has mastered individual concepts but fails to connect them in answers
- Student's practice answer treats a multi-factor topic as single-factor
- Student asks about a complex topic where multiple causal chains converge
- Tutor identifies a cross-concept question type that the student will face in the exam

**Content characteristics:**
- Explicitly names multiple linked concepts
- Uses relationship edge content (`influences`, `accompanies`, `often_confused_with`)
- May synthesise two causal chains into a combined explanation
- Drawn from relationship nodes + intersecting concept nodes

**Retrieval implications:**
- Retrieve relationship edges between target concepts
- Retrieve both concept nodes
- Retrieve converging causal chains
- Use comparative retrieval type as secondary
- Maximum 6 chunks to manage complexity

**Example trigger:** Student understands tannin AND ageing separately but cannot explain how tannin enables ageing.

---

### Role 8: `concise_answer_training`

**Definition:** Content that helps students compress their knowledge into the precise, economical exam answers required by WSET's mark scheme.

**When to deploy:**
- Student's practice answers are accurate but too long, unfocused, or padded
- Student is over-explaining to compensate for uncertainty
- Student needs to demonstrate they can identify the critical point in a limited word count

**Content characteristics:**
- Short, high-signal sentences that model correct exam economy
- Drawn from Tier 3 benchmark answers (Pass/Merit level) and `distinction_note` fields
- Explicitly shows what to include and what to omit
- Does NOT introduce new facts — refines presentation of known facts

**Retrieval implications:**
- Retrieve `distinction_note` field specifically
- Retrieve Tier 3 benchmark Pass/Merit answers as models
- Avoid Tier 4 enrichment (too much depth for this role)
- Maximum 3 chunks; brevity is the point

**Example trigger:** Student writes a correct 200-word answer for a 2-mark question.

---

### Role 9: `distinction_training`

**Definition:** Content that provides the specific mechanistic depth, compound naming, conditional nuance, and multi-factor synthesis required for the Distinction grade band.

**When to deploy:**
- Student has demonstrated Merit-level understanding and is targeting Distinction
- Student's practice answer is missing the specific mechanism, compound name, or condition that elevates a Merit answer to Distinction
- Tutor has identified that the student's explanation is correct but shallow
- Student explicitly asks "What would I need to add for Distinction?"

**Content characteristics:**
- Full causal chains (all steps, not just outcome)
- Named compounds where relevant (malic acid, ellagitannins, diacetyl, mannoproteins, gluconic acid)
- Specific conditions ("only under alternating mist and dry afternoons")
- Specific regional or wine examples with factual detail
- `distinction_note` fields from causal chains
- Tier 4 enrichment eligible (with framing)

**Retrieval implications:**
- Retrieve full causal chain (all steps)
- Retrieve `distinction_note` explicitly
- Retrieve `related_exam_questions` for practice
- Tier 4 eligible if enrichment adds mechanistic depth
- Maximum composite score weight given to CRS (causal richness)

**Example trigger:** Student's practice answer on MLF says "MLF converts malic acid to lactic acid and softens the wine" — correct but missing mechanism, diprotic/monoprotic distinction, tartaric acid stability, and diacetyl variable.

---

## 4. Classification Assignment Rules

### 4.1 Primary Role Assignment

Each knowledge graph node is assigned a `primary_pedagogical_role` at ingestion. This is the default role when no learner model is active or when context is insufficient to determine a more specific role.

| Node type | Default primary role |
|-----------|---------------------|
| Concept definition | `foundational` |
| Concept distinction_insights | `distinction_training` |
| Causal chain (moderate complexity) | `reinforcement` |
| Causal chain (complex) | `distinction_training` |
| Causal chain distinction_note | `exam_strategy` |
| Misconception node | `misconception_correction` |
| Benchmark answer (Pass) | `concise_answer_training` |
| Benchmark answer (Distinction) | `distinction_training` |
| Regional example in chain | `reinforcement` |
| SAT vocabulary content | `tasting_alignment` |
| Tier 4 enrichment | `advanced_enrichment` |

### 4.2 Context-Override Rules

The retrieval system may override the primary role based on conversation context:

| Context signal | Override to |
|---------------|-------------|
| First mention of concept | `foundational` |
| `detection_signal` match | `misconception_correction` |
| "exam" or "Distinction" in query | `exam_strategy` or `distinction_training` |
| "more detail" or "deeper" in query | `advanced_enrichment` |
| Tasting note context active | `tasting_alignment` |
| Practice answer too long | `concise_answer_training` |
| Two concepts in same query | `linkage_training` |

### 4.3 Role Stack Ordering

When multiple roles are relevant simultaneously, they are deployed in this priority order:
1. `misconception_correction` (always first if triggered)
2. `foundational` (if concept is new)
3. `reinforcement` (if concept partially known)
4. `linkage_training` (if multiple concepts connected)
5. `exam_strategy` or `distinction_training` (if exam focus active)
6. `advanced_enrichment` (if deeper detail requested)

---

## 5. Role-Retrieval Interaction Matrix

| Role | Dense search | Graph traversal | Tier 4 eligible | Min score | Max chunks |
|------|-------------|-----------------|----------------|-----------|-----------|
| foundational | Yes | Limited | No | 0.60 | 3 |
| reinforcement | Yes | Yes | No | 0.60 | 4 |
| misconception_correction | Forced | Forced | No | N/A (forced) | 2 |
| exam_strategy | Yes | Yes (distinction_note) | No | 0.65 | 4 |
| advanced_enrichment | Yes | Yes | Yes | 0.55 | 5 |
| tasting_alignment | Yes | Sensory graph | Yes (limited) | 0.60 | 4 |
| linkage_training | Yes | Yes (relationship edges) | No | 0.60 | 6 |
| concise_answer_training | Yes | Yes (distinction_note) | No | 0.65 | 3 |
| distinction_training | Yes | Full chain traversal | Yes | 0.60 | 5 |

---

## 6. Quality Assurance for Classification

### 6.1 Classification Drift Prevention

Pedagogical roles must be reviewed each time a content node is updated. Role assignment is not permanent — a misconception node that was `misconception_correction` when created may also need `distinction_training` annotation if it contains complex mechanistic content.

### 6.2 Coverage Auditing

Each topic in the WSET L3 curriculum should have content nodes covering all nine pedagogical roles. A topic with only `foundational` and `distinction_training` content, but no `misconception_correction` nodes, is classified as a coverage gap and flagged for editorial attention.

### 6.3 Forbidden Role Assignments

The following role assignments are explicitly forbidden:

| Assignment | Why forbidden |
|-----------|---------------|
| `exam_strategy` role to Tier 4 sources | May introduce non-examinable content as exam guidance |
| `distinction_training` role without causal mechanism | Distinction requires mechanistic depth; pure fact lists are not Distinction-training |
| `foundational` role to deprecated content | Deprecated content must never serve as a learner's first exposure to a concept |
| Any pedagogical role to Tier 0 mark scheme content | Tier 0 is for Examiner Agent calibration, not Tutor Agent pedagogical deployment |

---

*This document is authoritative for pedagogical content classification. It does not constitute official WSET assessment guidance.*

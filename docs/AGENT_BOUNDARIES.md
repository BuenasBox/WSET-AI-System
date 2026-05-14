# WSET-AI-System — Agent Boundaries Specification

**Document type:** Internal Architecture Specification  
**Status:** Active  
**Version:** 1.0  
**Last updated:** 2026-05-13  
**Owner:** WSET-AI-System project  
**Scope:** Tutor Agent · Examiner Agent · Orchestrator (future)

---

> ⚠️ **Governing principle**
>
> The Tutor Agent and Examiner Agent are epistemologically separate systems.
> They share a runtime environment but must never share a knowledge namespace, a
> memory context, a RAG corpus, or a scoring authority. Mixing these two agents'
> knowledge sources is a correctness and integrity violation, not merely a design
> preference. Treat every boundary in this document as a hard constraint, not a
> guideline.

---

## Table of Contents

1. [Definitions](#1-definitions)
2. [Agent Roles](#2-agent-roles)
3. [Allowed Knowledge Sources](#3-allowed-knowledge-sources)
4. [Forbidden Knowledge Sources](#4-forbidden-knowledge-sources)
5. [Scoring Authority Rules](#5-scoring-authority-rules)
6. [Calibration Hierarchy](#6-calibration-hierarchy)
7. [Data Trust Tiers](#7-data-trust-tiers)
8. [Pedagogical vs Evaluative Separation](#8-pedagogical-vs-evaluative-separation)
9. [Anti-Contamination Rules](#9-anti-contamination-rules)
10. [RAG Boundary Rules](#10-rag-boundary-rules)
11. [Memory Isolation Rules](#11-memory-isolation-rules)
12. [Prompt Governance Principles](#12-prompt-governance-principles)
13. [Future Orchestration Guidelines](#13-future-orchestration-guidelines)
14. [Human Review Requirements](#14-human-review-requirements)
15. [Safety Principles for Educational Accuracy](#15-safety-principles-for-educational-accuracy)
16. [Embeddings and Vector DB Ingestion Rules](#16-embeddings-and-vector-db-ingestion-rules)
17. [Fine-Tuning Rules](#17-fine-tuning-rules)
18. [Logging and Auditability Principles](#18-logging-and-auditability-principles)
19. [Recommended Future Architecture](#19-recommended-future-architecture)
20. [Allowed and Forbidden Flow Examples](#20-allowed-and-forbidden-flow-examples)
21. [Risk Register](#21-risk-register)
22. [Scaling to WSET Diploma](#22-scaling-to-wset-diploma)

---

## 1. Definitions

These definitions are authoritative within this project. All code, prompts, and
configuration files must use these terms consistently.

### 1.1 Official

> **Official** material is any document produced, endorsed, or published by the
> Wine & Spirit Education Trust (WSET) as part of its accredited Level 3 Award
> curriculum. This includes, and is limited to:
>
> - The WSET Level 3 Award Specification (current edition)
> - The Systematic Approach to Tasting Wine® (SAT) document
> - Official WSET Study Guide (Level 3)
> - Official WSET Sample Papers (published by WSET)
> - Official WSET Mock Exams (published by WSET)
> - Official WSET Marking Keys and Model Answers (published by WSET)
> - Official WSET Calibration Documents (published or distributed by WSET for
>   accredited providers)

**What is not official:** Any third-party interpretation, summary, tutorial,
video transcript, student note, AI-generated explanation, or internal training
question bank — regardless of how accurate it may be.

### 1.2 Pedagogical

> **Pedagogical** material is content whose purpose is to help a learner
> understand, remember, or apply wine knowledge. It includes explanations,
> analogies, worked examples, mnemonics, and practice questions. Pedagogical
> material may be accurate and valuable, but it does not carry scoring authority
> under any circumstances.

Examples: Wine With Jimmy YouTube transcripts, tutor-generated explanations,
enrichment layers, internal question bank questions, study pattern data.

### 1.3 Generated

> **Generated** content is any text, answer, explanation, or question produced
> by an AI model (including this system), a human tutor outside of official WSET
> channels, or any automated pipeline. Generated content has `source_trust_tier:
> internal_training` and `official_grading_authority: false` in all data
> schemas.

Generated content may be used freely by the Tutor Agent. It must never be used
by the Examiner Agent for scoring decisions.

### 1.4 Benchmark

> A **benchmark answer** is a human-curated, expert-reviewed model answer for an
> open-response question, stored in `knowledge/benchmark-answers/`. Benchmark
> answers are pedagogical references — they guide the Tutor Agent in giving
> high-quality feedback — but they are not official WSET marking keys. They must
> not be presented to the user as official expected answers.

### 1.5 Calibration

> **Calibration** in this system refers to the process of aligning an agent's
> scoring or feedback behaviour with official WSET standards. Only official WSET
> marking keys and model answers stored in `knowledge/official-wset/marking-keys/`
> and `knowledge/calibration/` (after human validation) may be used for
> calibration. The Examiner Agent's calibration set must be reviewed and approved
> by a human WSET-qualified reviewer before activation.

---

## 2. Agent Roles

### 2.1 Tutor Agent

| Attribute | Value |
|-----------|-------|
| **Primary function** | Pedagogical support — teach, explain, clarify, practise |
| **Persona** | Knowledgeable, encouraging, patient study companion |
| **Scoring authority** | None — may give formative feedback only |
| **Knowledge namespace** | `tutor_corpus` (see §3) |
| **Session memory** | Per-learner, persistent across sessions via `knowledge/nazareth/` |
| **Output type** | Explanations, hints, practice feedback, study plans, flashcards |
| **Tone** | Adaptive to learner; may use analogies and informal language |

The Tutor Agent's job is to maximise learning outcomes. It is not a judge. When a
learner answers a practice question incorrectly, the Tutor Agent explains why —
drawing on pedagogical material — without issuing a summative score or implying
official pass/fail assessment.

### 2.2 Examiner Agent

| Attribute | Value |
|-----------|-------|
| **Primary function** | Evaluative — assess responses against official WSET standards |
| **Persona** | Neutral, precise, calibrated to official WSET marking criteria |
| **Scoring authority** | Practice assessment only — explicitly NOT official WSET certification |
| **Knowledge namespace** | `examiner_corpus` (see §3) |
| **Session memory** | Stateless per session — no learner history in scoring context |
| **Output type** | Structured assessment: mark, band, criterion-level feedback |
| **Tone** | Formal, objective, criterion-referenced |

> ⚠️ **Critical distinction:** The Examiner Agent provides practice assessment,
> not official WSET certification. Every response from the Examiner Agent must
> include a disclosure that results are indicative only and do not constitute
> official WSET assessment.

### 2.3 Orchestrator (future)

The Orchestrator routes learner requests to the appropriate agent. It must never
allow knowledge or context from one agent's namespace to bleed into the other's.
See §13 for full orchestration guidelines.

---

## 3. Allowed Knowledge Sources

### 3.1 Tutor Agent — Allowed Sources

| Source | Location | Trust tier | Notes |
|--------|----------|------------|-------|
| Wine With Jimmy transcripts (clean) | `knowledge/wine-with-jimmy/clean/` | `pedagogical` | Must be ingested and deduplicated; not for scoring |
| Internal question bank | `knowledge/question-bank/structured/` | `internal_training` | `official_grading_authority: false` on all records |
| Benchmark answers | `knowledge/benchmark-answers/` | `pedagogical` | Human-curated; labelled as pedagogical, not official |
| Nazareth learner study patterns | `knowledge/nazareth/` | `private_learner` | Per-learner only; never cross-contaminated |
| Enrichment layers | `knowledge/enrichment/` | `pedagogical` | Topic mapping, difficulty, causal chains, common errors |
| Benchmark wines | `knowledge/benchmark-wines/` | `pedagogical` | Tasting note references |
| WSET official specification | `knowledge/official-wset/specification/` | `official` | Read-only reference; Tutor may cite but not score against |
| WSET study guide | `knowledge/official-wset/study-guide/` | `official` | Read-only reference for explanations |
| Generated pedagogical explanations | in-context or cached | `generated` | Must be clearly labelled as AI-generated to learner |

### 3.2 Examiner Agent — Allowed Sources

| Source | Location | Trust tier | Notes |
|--------|----------|------------|-------|
| WSET Level 3 Specification | `knowledge/official-wset/specification/` | `official` | Primary authority |
| WSET SAT (Systematic Approach to Tasting) | `knowledge/official-wset/sat/` | `official` | Tasting assessment authority |
| WSET Marking Keys | `knowledge/official-wset/marking-keys/` | `official` | Only human-validated files; see §14 |
| WSET Sample Papers | `knowledge/official-wset/sample-papers/` | `official` | For question type calibration only |
| WSET Mock Exams | `knowledge/official-wset/mock-exams/` | `official` | For question type calibration only |
| Validated calibration docs | `knowledge/calibration/` | `official` (after validation) | Must pass human review gate before use; see §6 |

**The Examiner Agent's allowed source list is closed.** Any new source requires
an explicit update to this document, human review, and a version increment.

---

## 4. Forbidden Knowledge Sources

### 4.1 Forbidden for the Examiner Agent

The following sources are **absolutely forbidden** from the Examiner Agent's RAG
corpus, prompt context, fine-tuning data, and memory:

| Forbidden source | Reason |
|-----------------|--------|
| Wine With Jimmy transcripts (any stage: raw, clean, indexed) | Pedagogical content; not officially calibrated to WSET standards |
| Internal question bank (`question-bank/`) | `official_grading_authority: false`; questions were not issued by WSET |
| AI-generated explanations (any model) | Cannot be traced to official WSET authority; introduces scoring drift |
| Benchmark answers (`benchmark-answers/`) | Human-curated but not official WSET marking keys |
| Enrichment layers (`enrichment/`) | AI-generated metadata; not official |
| Nazareth learner data | Private learner patterns; irrelevant to objective scoring |
| Any YouTube, web, or third-party content | Not official; provenance unverifiable |
| Tutor Agent session memory | Contaminated with pedagogical framing |
| Student practice responses from prior sessions | Circularity risk: model answers must not be influenced by learner output |
| Benchmark wines | Tasting notes are pedagogical references, not SAT-calibrated assessments |

### 4.2 Forbidden for the Tutor Agent

| Forbidden action | Reason |
|-----------------|--------|
| Presenting internal questions as official WSET exam questions | Misleads the learner about exam content |
| Using question bank answers as official marking keys | `official_grading_authority: false` |
| Storing Examiner Agent scores in Nazareth memory without disclosure | Mixing evaluative and pedagogical contexts |
| Generating responses that imply official WSET endorsement | Legal and accuracy risk |
| Citing unofficial sources as equivalent to official WSET material | Epistemological contamination |

---

## 5. Scoring Authority Rules

### 5.1 The Authority Ladder

```
HIGHEST AUTHORITY
    │
    ▼
  Official WSET marking keys + specification
  (knowledge/official-wset/marking-keys/, /specification/)
    │
    ▼
  Human WSET-qualified reviewer validation
  (knowledge/calibration/ — post-review only)
    │
    ▼
  Examiner Agent scoring output
  [practice only — not certification]
    │
    ▼
  Benchmark answers
  (knowledge/benchmark-answers/)
    │
    ▼
  Tutor Agent formative feedback
    │
    ▼
  Internal question bank answers
  (knowledge/question-bank/)
    │
    ▼
LOWEST AUTHORITY
  Generated / AI-produced explanations
```

### 5.2 Scoring Rules

1. **The Examiner Agent may only score against sources at or above its own
   level in the authority ladder** — i.e., official WSET materials and validated
   calibration docs only.

2. **The Examiner Agent must never derive a score from sources below its level**
   — benchmark answers, question bank items, or generated explanations must not
   influence its marks even if injected into context.

3. **All Examiner Agent scores carry a mandatory disclosure:** *"This assessment
   is for practice purposes only and does not constitute official WSET
   certification. Official results are issued by WSET through accredited
   providers only."*

4. **The Tutor Agent must never issue a summative score.** It may provide
   formative feedback of the form: *"Your answer covers X and Y well; consider
   adding Z to reach Distinction level."* It must not say: *"Your answer would
   score 14/20."*

5. **Pass/fail thresholds** used by the Examiner Agent must be sourced from
   the official WSET specification only. The internal question bank simulator's
   55% threshold is for practice orientation only and must not be presented as
   the official WSET pass mark without verification against the current
   specification.

---

## 6. Calibration Hierarchy

### 6.1 Definition of calibration tiers

| Tier | Label | Description | Who validates |
|------|-------|-------------|---------------|
| Tier 0 | `wset_official` | Content published directly by WSET | WSET itself |
| Tier 1 | `human_validated` | Content reviewed and approved by a WSET-qualified human reviewer for use in this system | Named human reviewer + date |
| Tier 2 | `ai_assisted_review` | AI-assisted review with human spot-check; not for Examiner Agent scoring | Project team |
| Tier 3 | `internal_training` | Internal training bank; no official authority | Automated pipeline |
| Tier 4 | `generated` | AI-generated; no authority | Automated |

### 6.2 Calibration gate for Examiner Agent activation

Before the Examiner Agent is activated for any scoring function, all sources in
`knowledge/calibration/` must pass the following gate:

- [ ] Source file identified and provenance documented
- [ ] Human reviewer (WSET Level 3 or higher qualification) has reviewed the
      marking key
- [ ] Reviewer name, date, and qualification recorded in a companion
      `calibration_manifest.json`
- [ ] File hash recorded to detect future tampering
- [ ] Trust tier set to `human_validated` (Tier 1) or `wset_official` (Tier 0)

**Any calibration document that has not passed this gate must not be ingested
into the Examiner Agent's RAG corpus, even in a staging environment.**

---

## 7. Data Trust Tiers

| Trust tier label | Numeric tier | Allowed for Tutor | Allowed for Examiner (scoring) | Allowed for Examiner (context) | Can be embedded | Can be fine-tuned on |
|-----------------|:------------:|:-----------------:|:------------------------------:|:------------------------------:|:---------------:|:--------------------:|
| `wset_official` | 0 | ✅ | ✅ | ✅ | ✅ (after validation) | ⚠️ (human review required) |
| `human_validated` | 1 | ✅ | ✅ | ✅ | ✅ (after validation) | ⚠️ (human review required) |
| `ai_assisted_review` | 2 | ✅ | ❌ | ⚠️ (read-only reference only) | ✅ (tutor corpus only) | ❌ |
| `internal_training` | 3 | ✅ | ❌ | ❌ | ✅ (tutor corpus only) | ❌ |
| `generated` | 4 | ✅ | ❌ | ❌ | ✅ (tutor corpus only) | ❌ |
| `private_learner` | 5 | ✅ (own learner only) | ❌ | ❌ | ❌ | ❌ |

**Rules:**
- Trust tier is assigned at ingestion time and stored in the record schema
  (`source_trust_tier` field).
- Trust tier may be promoted (e.g., from Tier 3 to Tier 1) only by a human
  reviewer following the calibration gate in §6.2.
- Trust tier may never be promoted automatically by any pipeline.
- Trust tier demotion (lowering authority) is always safe and does not require
  human review.

---

## 8. Pedagogical vs Evaluative Separation

This is the foundational principle of the entire agent architecture.

### 8.1 The core distinction

| Dimension | Tutor Agent (Pedagogical) | Examiner Agent (Evaluative) |
|-----------|--------------------------|------------------------------|
| **Goal** | Maximise learning | Accurately assess performance |
| **Tone** | Encouraging, adaptive | Neutral, criterion-referenced |
| **Feedback type** | Formative (process-oriented) | Summative (outcome-oriented) |
| **Knowledge source** | Broad: official + pedagogical + generated | Narrow: official + validated only |
| **Scoring** | Not permitted | Permitted (practice only) |
| **Error handling** | Explain and guide | Record and report |
| **Memory** | Persistent learner model | Stateless per session |
| **Calibration** | Not required | Required before activation |

### 8.2 Why mixing is dangerous

If the Tutor Agent's pedagogical framing leaks into the Examiner Agent's scoring
context, the following failure modes become possible:

1. **Scoring drift:** The Examiner Agent rewards a learner for a well-explained
   but technically incorrect answer because it was exposed to the Tutor's
   encouraging framing of the same answer.

2. **False confidence:** A learner receives a high practice score based on
   pedagogically-framed answers that would not pass official WSET marking
   criteria.

3. **Calibration contamination:** Generated explanations in the Tutor corpus
   establish incorrect facts that propagate into the Examiner Agent's scoring
   heuristics over time.

4. **Compliance risk:** If the system is ever used to claim alignment with
   official WSET standards, contamination of the Examiner Agent's corpus with
   non-official material constitutes a misrepresentation.

### 8.3 The separation is not symmetrical

The Tutor Agent *may* cite official WSET material. The Examiner Agent *may not*
use pedagogical material. The separation is one-directional: official knowledge
flows into both agents; pedagogical knowledge flows only into the Tutor Agent.

```
Official WSET material ──────────────────────────┬──► Tutor Agent ✅
                                                  └──► Examiner Agent ✅

Pedagogical / Generated material ────────────────►  Tutor Agent ✅
                                                     Examiner Agent ❌
```

---

## 9. Anti-Contamination Rules

### 9.1 Vector store isolation

- The Tutor Agent and Examiner Agent must use **physically separate vector
  collections** (separate namespaces, indices, or databases).
- Collection names must include the agent identity:
  `wset_tutor_*` and `wset_examiner_*`.
- No shared collection is permitted, even for read-only access.

### 9.2 Prompt context isolation

- The system prompt of the Examiner Agent must explicitly enumerate its
  forbidden sources and instruct the model to refuse if asked to draw on them.
- The Examiner Agent's system prompt must not be modified by any automated
  pipeline without human review.
- Dynamic context injection into the Examiner Agent's prompt is restricted to
  sources in `examiner_corpus` (§3.2) only.

### 9.3 Response isolation

- Examiner Agent responses must not be stored in the Tutor Agent's context
  window or RAG corpus.
- Tutor Agent session history must not be included in Examiner Agent prompts.
- If the Orchestrator routes a request from a Tutor session to the Examiner
  Agent, it must create a new, clean context for the Examiner Agent. It must not
  forward prior Tutor conversation turns.

### 9.4 File system isolation

| Path | Accessible by Tutor | Accessible by Examiner |
|------|:-------------------:|:----------------------:|
| `knowledge/official-wset/` | ✅ (read) | ✅ (read) |
| `knowledge/wine-with-jimmy/` | ✅ | ❌ |
| `knowledge/question-bank/` | ✅ | ❌ |
| `knowledge/benchmark-answers/` | ✅ | ❌ |
| `knowledge/benchmark-wines/` | ✅ | ❌ |
| `knowledge/enrichment/` | ✅ | ❌ |
| `knowledge/nazareth/` | ✅ (own learner) | ❌ |
| `knowledge/calibration/` | ❌ | ✅ (validated only) |

### 9.5 Contamination detection

Any automated ingestion pipeline must:
1. Check the `source_trust_tier` of every document before routing it.
2. Refuse to ingest Tier 3/4 documents into `examiner_corpus`.
3. Log a `CONTAMINATION_ATTEMPT` event if a Tier 3/4 document is presented to
   the Examiner Agent's ingestion pipeline.
4. Alert a human reviewer on any `CONTAMINATION_ATTEMPT` event.

---

## 10. RAG Boundary Rules

### 10.1 Corpus definitions

| Corpus name | Agent | Sources | Embedding model | Index name |
|-------------|-------|---------|-----------------|------------|
| `tutor_corpus` | Tutor Agent | Tiers 0–4 (see §7) | TBD | `wset_tutor_v1` |
| `examiner_corpus` | Examiner Agent | Tiers 0–1 only | TBD | `wset_examiner_v1` |

### 10.2 Ingestion rules

1. Every document ingested into any corpus must have its `source_trust_tier`
   recorded in the vector metadata at ingestion time.
2. Every chunk in the vector store must carry: `source_trust_tier`,
   `source_file`, `agent_corpus`, `ingestion_date`, `chunk_id`.
3. Retrieval must filter by `agent_corpus` before returning results. A query
   against `examiner_corpus` must never return chunks tagged `agent_corpus:
   tutor_corpus`.
4. Retrieval must also filter by `source_trust_tier ≤ 1` for any Examiner Agent
   query.
5. **Similarity score thresholds** must be set conservatively for the Examiner
   Agent. A low-confidence retrieval (below threshold) must trigger a "no
   relevant official source found" response rather than a hallucinated answer.

### 10.3 Query routing

```
Learner query
    │
    ▼
Orchestrator classifies query intent:
    ├── "I want to learn / understand / practise"  ──► Tutor Agent (tutor_corpus)
    ├── "Evaluate my answer / score me"            ──► Examiner Agent (examiner_corpus)
    └── "Both"                                     ──► Tutor first, then Examiner
                                                       (separate contexts — see §13)
```

### 10.4 Cross-corpus references

The Tutor Agent may retrieve from `examiner_corpus` for informational purposes
(e.g., citing official WSET specification text to explain a concept). This
retrieval must be:
- Read-only
- Clearly attributed: *"According to the official WSET Level 3 specification…"*
- Never mixed with Tier 3/4 content in the same response without clear
  sourcing labels

The Examiner Agent must never retrieve from `tutor_corpus`.

---

## 11. Memory Isolation Rules

### 11.1 Tutor Agent memory

| Memory type | Storage | Scope | Retention |
|-------------|---------|-------|-----------|
| Short-term (session) | In-context | Current session only | Cleared on session end |
| Long-term (learner model) | `knowledge/nazareth/{learner_id}/` | Per learner | Persistent; learner-controlled deletion |
| Weak-area tracking | `knowledge/nazareth/{learner_id}/weak-areas/` | Per learner | Updated after each session |
| Mock history | `knowledge/nazareth/{learner_id}/mock-history/` | Per learner | Append-only |
| Distinction feedback | `knowledge/nazareth/{learner_id}/distinction-feedback/` | Per learner | Append-only |

### 11.2 Examiner Agent memory

The Examiner Agent is **stateless** with respect to learner history.

| Rule | Rationale |
|------|-----------|
| No learner history in scoring context | Prevents halo effects from prior performance |
| No cross-session memory | Each assessment is independent |
| No access to `knowledge/nazareth/` | Learner patterns must not influence score |
| Session context cleared after each evaluation | Prevents context accumulation |

### 11.3 Shared memory — explicitly forbidden

The following memory operations are forbidden across agent boundaries:

- Writing Examiner Agent scores to the Tutor Agent's session context
- Reading Tutor Agent session history in the Examiner Agent's prompt
- Sharing a Redis/cache key-value store between agents without namespace
  isolation
- Writing to `knowledge/nazareth/` from the Examiner Agent

> ⚠️ **Exception:** The Orchestrator may write Examiner Agent scores to
> `knowledge/nazareth/{learner_id}/mock-history/` as a structured record
> **after** the Examiner Agent session has ended and the score has been
> finalised — but only via the Orchestrator, never directly from the Examiner
> Agent.

---

## 12. Prompt Governance Principles

### 12.1 Prompt classification

Every prompt in this system is classified as one of:

| Class | Definition | Change control |
|-------|-----------|----------------|
| `system_prompt` | The primary instruction set defining agent identity and boundaries | Human review required; version-controlled; hash-logged |
| `rag_context` | Retrieved document chunks injected into context | Governed by corpus rules (§10); no human review per-query |
| `user_turn` | Learner input | Not pre-approved; must be sanitised by Orchestrator |
| `few_shot` | Example Q&A pairs in prompt | Must adhere to source rules for each agent |
| `tool_result` | Output from a tool call injected into context | Must carry source metadata |

### 12.2 Rules for Examiner Agent system prompts

1. The system prompt must include an explicit list of forbidden sources.
2. The system prompt must include the official disclosure statement (§5.2 rule 3).
3. The system prompt must instruct the model to respond with a structured error
   if asked to score against non-official sources.
4. The system prompt must not be overridden by user input. The Orchestrator must
   validate that no user turn contains prompt injection attempts before passing
   to the Examiner Agent.
5. Changes to the Examiner Agent system prompt require:
   - A diff recorded in version control
   - Human sign-off
   - A version number increment in the prompt file header
   - Re-validation of calibration against a held-out test set

### 12.3 Rules for Tutor Agent system prompts

1. The system prompt must clearly state the agent is a learning assistant, not
   an official WSET examiner.
2. The system prompt must instruct the agent never to present internal questions
   as official WSET exam questions.
3. The Tutor Agent's prompt may be updated with less ceremony than the Examiner
   Agent's, but changes must still be version-controlled.

### 12.4 Few-shot examples

| Agent | Allowed few-shot sources | Forbidden few-shot sources |
|-------|--------------------------|---------------------------|
| Tutor | Pedagogical, generated, benchmark answers | Must not present non-official answers as official |
| Examiner | Official WSET model answers (marking keys) only | All Tier 3/4 content |

---

## 13. Future Orchestration Guidelines

### 13.1 Orchestrator responsibilities

The Orchestrator (not yet implemented) will:

1. Classify incoming learner requests by intent.
2. Route to the appropriate agent with a clean, isolated context.
3. Enforce corpus access rules as the single gatekeeper.
4. Sanitise user input before routing to prevent prompt injection.
5. Never forward Tutor Agent context to the Examiner Agent, or vice versa.
6. Write evaluation results to `knowledge/nazareth/` only after the Examiner
   Agent session has ended.

### 13.2 Routing logic specification

```
Input: learner_message, session_state

IF intent == LEARN:
    agent = TutorAgent
    corpus = tutor_corpus
    context = [system_prompt_tutor, rag_tutor, session_history_tutor]

ELSE IF intent == EVALUATE:
    agent = ExaminerAgent
    corpus = examiner_corpus
    context = [system_prompt_examiner, rag_examiner]  // no session history
    // mandatory: new context object, never reuse tutor context

ELSE IF intent == MIXED:
    step_1 = TutorAgent(LEARN)
    step_2 = ExaminerAgent(EVALUATE)  // new context, not inheriting step_1
    merge_results_for_display_only   // display only, not re-injected into either agent

ALWAYS:
    sanitise(learner_message) before routing
    log(routing_decision, agent, corpus, timestamp)
    attach(source_trust_tier) to every retrieved chunk
```

### 13.3 Orchestrator must not do

- Inject Examiner Agent score history into Tutor Agent context
- Allow the learner to switch agents mid-session without context reset
- Cache Examiner Agent responses and reuse them as Tutor Agent context
- Modify the Examiner Agent's system prompt at runtime

### 13.4 Error handling

If the Examiner Agent cannot find a relevant official source in `examiner_corpus`
for a given question type, it must return a structured response:

```json
{
  "status": "no_official_source_found",
  "message": "No validated official WSET source was found for this question.
              This question cannot be scored at this time.",
  "recommendation": "Route to Tutor Agent for pedagogical support."
}
```

It must never hallucinate an official answer when no retrieval is available.

---

## 14. Human Review Requirements

### 14.1 When human review is mandatory

| Trigger | Reviewer required | Record location |
|---------|------------------|-----------------|
| Adding any new source to `examiner_corpus` | WSET-qualified reviewer (L3+) | `knowledge/calibration/calibration_manifest.json` |
| Modifying Examiner Agent system prompt | Project owner | Version-controlled prompt file |
| Promoting any document from Tier 3→2 or 2→1 | Subject matter expert | `source_trust_tier` field update + log |
| Activating Examiner Agent in any new environment | Project owner | Deployment checklist |
| Any `CONTAMINATION_ATTEMPT` event | Project owner | Incident log |
| First ingestion of official WSET documents | WSET-qualified reviewer | `calibration_manifest.json` |
| Any change to pass/fail thresholds | Project owner | `AGENT_BOUNDARIES.md` update |

### 14.2 Calibration manifest format

Every file in `knowledge/calibration/` must have a companion entry in
`knowledge/calibration/calibration_manifest.json` with the following structure:

```json
{
  "file": "marking_key_level3_2024.pdf",
  "source": "WSET official — received from [provider]",
  "trust_tier": 0,
  "reviewer_name": "[name]",
  "reviewer_qualification": "WSET Level 3 / Diploma / Educator",
  "review_date": "YYYY-MM-DD",
  "sha256": "[file hash]",
  "notes": "",
  "approved_for_examiner_agent": true
}
```

### 14.3 Ongoing review cadence

| Review type | Frequency | Owner |
|-------------|-----------|-------|
| Official source currency check (new WSET editions) | Annually | Project owner |
| Calibration manifest audit | Every 6 months | WSET-qualified reviewer |
| Examiner Agent scoring accuracy spot-check | Quarterly | Project owner |
| Prompt governance review | After any system change | Project owner |

---

## 15. Safety Principles for Educational Accuracy

### 15.1 Core safety principles

1. **Never present AI-generated content as official WSET statements.** Every
   response must be attributable to a source tier. If the source is Tier 3 or
   lower, it must not be presented as authoritative.

2. **Never fabricate marking criteria.** If the Examiner Agent cannot locate an
   official marking key for a question, it must say so explicitly. Fabricating
   marking criteria is worse than no feedback.

3. **Distinguish levels of certainty.** The Tutor Agent must use hedging language
   when drawing on non-official sources: *"Based on the Wine With Jimmy
   materials…"* vs. *"According to the official WSET specification…"*

4. **Protect learner exam readiness.** A learner who is told they are "Distinction
   ready" based on internal practice scores may be genuinely unprepared for the
   official exam. The system must consistently communicate the gap between
   practice scores and official results.

5. **No competitive or harmful comparisons.** The system must not compare learner
   performance to other learners, imply that a learner is unlikely to pass, or
   make statements that could be psychologically harmful.

6. **Version-lock official sources.** If a new edition of the WSET specification
   is released, the old edition must not be silently replaced. Both versions must
   be retained with clear date labels, and the Examiner Agent must be explicitly
   reconfigured to use the new edition.

### 15.2 Accuracy failure modes and mitigations

| Failure mode | Risk level | Mitigation |
|-------------|-----------|------------|
| Examiner Agent scores against Tier 3 questions | Critical | Anti-contamination rules (§9); corpus isolation (§10) |
| Tutor Agent presents internal bank answers as official | High | Prompt governance (§12.3); mandatory disclosure labels |
| Official source is outdated edition | High | Version-lock policy (§15.1 rule 6); annual review (§14.3) |
| Marking key is misinterpreted by the model | Medium | Human spot-check (§14.3); calibration gate (§6.2) |
| Learner conflates practice score with official result | Medium | Mandatory disclosure on every Examiner Agent response (§5.2) |
| RAG retrieval returns incorrect chunk | Medium | Confidence threshold (§10.2 rule 5); source attribution in responses |

---

## 16. Embeddings and Vector DB Ingestion Rules

### 16.1 Pre-ingestion checklist

Before any document is embedded and ingested into either corpus:

- [ ] `source_trust_tier` has been assigned
- [ ] Source file is stored in the correct `knowledge/` subdirectory
- [ ] Document has been deduplicated (no existing chunk from same source)
- [ ] For Examiner corpus: calibration gate (§6.2) has passed
- [ ] `agent_corpus` tag has been decided (`tutor` or `examiner`)
- [ ] Chunking strategy has been chosen and documented (chunk size, overlap,
      metadata preserved)
- [ ] File hash recorded to detect tampering

### 16.2 Metadata required on every vector chunk

```json
{
  "chunk_id": "uuid",
  "source_file": "relative path from knowledge/",
  "source_trust_tier": 0,
  "agent_corpus": "examiner",
  "ingestion_date": "YYYY-MM-DD",
  "wset_level": 3,
  "ra": "RA1",
  "topic": "",
  "page_or_line": "",
  "sha256_source": ""
}
```

### 16.3 Chunking rules

- Chunk size and overlap must be chosen to preserve sentence-level meaning.
  Recommended starting point: 512 tokens, 64-token overlap.
- Questions and their model answers must never be split across chunks.
- SAT marking criteria must be chunked at the criterion level, not split across
  attribute descriptors.

### 16.4 Embedding model selection

- The same embedding model must be used for all documents within a single corpus.
  Mixing embedding models within a corpus makes similarity scores incomparable.
- Embedding model upgrades require full re-ingestion of the affected corpus.
- Embedding model and version must be recorded in a corpus manifest file
  alongside the vector DB.

### 16.5 Forbidden ingestion paths

| Action | Reason |
|--------|--------|
| Ingesting Wine With Jimmy raw audio directly | Must go through clean pipeline first |
| Ingesting student responses into any corpus | Circular contamination; learner data privacy |
| Ingesting web-scraped WSET content | Provenance unverifiable; may be paraphrased or incorrect |
| Ingesting previous AI model outputs as training data | Closes the loop; creates model collapse risk |
| Re-ingesting the same document under a higher trust tier without human review | Trust tier fraud |

---

## 17. Fine-Tuning Rules

Fine-tuning a base model on this project's data is a future option, but carries
significant risks that must be managed explicitly.

### 17.1 Fine-tuning is forbidden on

| Data | Reason |
|------|--------|
| Internal question bank | Not official; would teach the model incorrect answer authority |
| Wine With Jimmy transcripts | Pedagogical style may conflict with official WSET register |
| AI-generated explanations (any tier) | Amplifies existing model patterns; cannot improve accuracy |
| Student practice responses | Privacy; circular contamination |
| Any data without human-verified `source_trust_tier ≤ 1` | Cannot verify accuracy |

### 17.2 Fine-tuning may be considered on

| Data | Conditions |
|------|-----------|
| Official WSET specification text | Only for Examiner-facing models; human sign-off required |
| Official WSET marking keys | Only after calibration gate (§6.2); extensive test evaluation |
| Human-validated calibration docs | Only after full trust tier promotion |

### 17.3 Fine-tuning evaluation requirements

Before deploying any fine-tuned model:

1. Held-out evaluation set must be drawn exclusively from official WSET sources.
2. Scoring accuracy on held-out set must exceed baseline (non-fine-tuned) model.
3. Contamination test: the fine-tuned model must refuse to score against Tier 3
   sources even when prompted.
4. Human reviewer must independently evaluate a random sample of 50 responses.
5. Fine-tuning must be re-evaluated after any new WSET specification edition.

### 17.4 Fine-tuning is not a substitute for RAG calibration

Fine-tuning encodes knowledge into weights. RAG retrieves from a controllable,
auditable source. For a system where official source provenance is critical,
RAG with strict corpus governance is preferred over fine-tuning. Fine-tuning
should only be considered for style/format adaptation, not for knowledge injection.

---

## 18. Logging and Auditability Principles

### 18.1 What must be logged

Every interaction involving the Examiner Agent must produce an audit log entry
containing:

| Field | Description |
|-------|-------------|
| `session_id` | Unique per session |
| `agent` | `examiner` or `tutor` |
| `timestamp` | ISO 8601 |
| `learner_id` | Anonymised or hashed |
| `query_intent` | Classified intent |
| `retrieved_chunks` | List of chunk IDs used in context |
| `source_trust_tiers_used` | List of tiers present in context |
| `response_type` | `score`, `feedback`, `explanation`, `error` |
| `score_issued` | Numeric score if applicable |
| `disclosure_shown` | Boolean — was the mandatory disclosure presented? |
| `contamination_flag` | Boolean — was a Tier 3/4 chunk retrieved? |

### 18.2 Log retention and access

- Logs must be retained for a minimum of 2 years.
- Logs must be stored separately from learner content data.
- Logs must be accessible to the project owner for audit purposes.
- Logs must not be used as training data for any model without explicit human
  review and anonymisation.

### 18.3 Contamination events

Any log entry with `contamination_flag: true` must trigger:
1. An immediate alert to the project owner.
2. A review of the ingestion pipeline.
3. A hold on Examiner Agent responses until the source of contamination is
   identified and remediated.

### 18.4 Score auditability

A learner must be able to request a full audit trail for any practice score
they received, showing:
- The question asked
- Their response
- The marking key used (source cited)
- The score awarded and the criterion it corresponds to
- The mandatory disclosure statement

This audit trail must be derivable from the log without rerunning the model.

---

## 19. Recommended Future Architecture

### 19.1 Target architecture diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Orchestrator                            │
│  ┌──────────────┐                        ┌──────────────────┐   │
│  │ Intent       │                        │ Context Builder  │   │
│  │ Classifier   │                        │ (corpus-aware)   │   │
│  └──────┬───────┘                        └────────┬─────────┘   │
│         │                                         │             │
│    ┌────▼──────────────────────────┐              │             │
│    │         Router                │              │             │
│    └──────┬─────────────┬──────────┘              │             │
│           │             │                         │             │
│     ┌─────▼──────┐ ┌────▼─────────┐               │             │
│     │ Tutor      │ │ Examiner     │               │             │
│     │ Agent      │ │ Agent        │               │             │
│     └─────┬──────┘ └────┬─────────┘               │             │
│           │             │                         │             │
│   ┌───────▼──────┐  ┌───▼────────────┐            │             │
│   │ tutor_corpus │  │ examiner_corpus│◄────────────┘             │
│   │ (Tiers 0–4) │  │ (Tiers 0–1)   │                           │
│   └──────────────┘  └────────────────┘                          │
│                                                                 │
│          ┌──────────────────────────────────┐                  │
│          │         Nazareth Store            │                  │
│          │  (Tutor write / Examiner ❌)       │                  │
│          └──────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
```

### 19.2 Technology recommendations

| Component | Recommended approach | Notes |
|-----------|---------------------|-------|
| Vector DB | Separate collections per agent | Pinecone namespaces, Qdrant collections, or Chroma collections |
| Metadata filtering | Hard filter on `agent_corpus` at query time | Not optional |
| Session management | Stateless for Examiner; stateful for Tutor | Redis or in-memory for Tutor sessions |
| Logging | Structured JSON logs, append-only | ELK stack or equivalent |
| Prompt versioning | Git-tracked prompt files with header metadata | Semantic versioning |
| Calibration manifest | JSON file, hash-verified | Git-tracked, human-updated only |

### 19.3 Phased rollout

| Phase | What is active | What is not yet active |
|-------|---------------|----------------------|
| Phase 1 (current) | Question bank, practice simulator | Tutor Agent, Examiner Agent, RAG |
| Phase 2 | Tutor Agent with RAG over tutor_corpus | Examiner Agent |
| Phase 3 | Examiner Agent, post calibration gate | Fine-tuning |
| Phase 4 | Orchestrator, full learner journey | WSET Diploma scope |

The Examiner Agent must not be activated until Phase 3 calibration requirements
are fully met (§6.2, §14).

---

## 20. Allowed and Forbidden Flow Examples

### 20.1 Allowed flows

| # | Scenario | Agent | Sources used | Outcome |
|---|----------|-------|-------------|---------|
| A1 | Learner asks "Why does Burgundy use whole-bunch fermentation?" | Tutor | Wine With Jimmy transcripts + enrichment layer | Pedagogical explanation; no score |
| A2 | Learner submits a SAT tasting note for practice assessment | Examiner | Official WSET SAT + marking key (Tier 0) | Structured score with criterion feedback + mandatory disclosure |
| A3 | Learner asks "What does the WSET specification say about Champagne disgorgement?" | Tutor | Official WSET specification (Tier 0) cited directly | Verbatim or paraphrased official text, attributed |
| A4 | Tutor Agent references official specification to explain a concept | Tutor | official-wset/specification/ | Explanation cites source tier clearly |
| A5 | Examiner Agent cannot find relevant chunk in examiner_corpus | Examiner | None | Returns structured "no official source found" error; no hallucination |
| A6 | Orchestrator writes Examiner score to Nazareth mock history | Orchestrator | Examiner output (post-session) | Score stored in `mock-history/`; Examiner session closed first |

### 20.2 Forbidden flows

| # | Scenario | Why forbidden |
|---|----------|--------------|
| F1 | Examiner Agent retrieves from `question-bank/` to score a response | Question bank has `official_grading_authority: false` |
| F2 | Tutor Agent tells learner "Your answer would score 16/20 in the official exam" | Tutor has no scoring authority; implies official assessment |
| F3 | Examiner Agent uses Wine With Jimmy transcript as a marking reference | Tier 4 pedagogical content; not a marking key |
| F4 | Orchestrator forwards Tutor session history to Examiner Agent context | Crosses memory boundary; introduces scoring bias |
| F5 | Examiner Agent generates a model answer when no marking key is found | Fabricates official criteria; high accuracy risk |
| F6 | Tutor Agent presents internal bank question as "an official WSET exam question" | Internal bank is not official WSET material |
| F7 | Examiner Agent stores learner name + score in a shared cache accessible to Tutor | Violates Examiner statelessness; risks halo effect |
| F8 | Fine-tuning a model on AI-generated explanations to improve Examiner accuracy | Amplifies generated content into model weights |

---

## 21. Risk Register

| Risk ID | Risk | Likelihood | Impact | Mitigation | Owner |
|---------|------|-----------|--------|------------|-------|
| R01 | Official WSET source is outdated when new edition is released | Medium | Critical | Annual review (§14.3); version-lock policy | Project owner |
| R02 | Examiner Agent RAG retrieves Tier 3 content due to misconfiguration | Low | Critical | Hard corpus filter (§10.2); contamination logging (§9.5) | Developer |
| R03 | Learner conflates practice score with official WSET result | Medium | High | Mandatory disclosure (§5.2); UI-level disclaimer | Project owner |
| R04 | Wine With Jimmy content contains factual errors | Medium | Medium | Tutor source attribution; not used for scoring | Project owner |
| R05 | Calibration manifest not updated after new official docs added | Medium | High | Review cadence (§14.3); gate enforcement (§6.2) | Project owner |
| R06 | Prompt injection via learner input reaches Examiner Agent | Low | High | Input sanitisation (§13.1); system prompt hardening (§12.2) | Developer |
| R07 | Fine-tuning degrading model accuracy by amplifying internal bank patterns | Medium | High | Fine-tuning restrictions (§17.1) | Developer |
| R08 | Nazareth data leaked across learners | Low | High | Per-learner isolation; no cross-learner queries | Developer |
| R09 | WSET changes marking criteria mid-year | Low | Critical | Annual review (§14.3); specification version pinning | Project owner |
| R10 | System implies official WSET endorsement | Low | Critical | Prompt governance (§12); legal disclaimer in UI | Project owner |

---

## 22. Scaling to WSET Diploma

The WSET Diploma (Level 4) introduces significantly more complexity:

### 22.1 Additional scope considerations

| Dimension | Level 3 | Level 4 Diploma |
|-----------|---------|-----------------|
| Subjects | Single integrated | D1 (Wines of the World), D2 (Wines of the World essay), D3 (Spirits), D4 (Sparkling), D5 (Fortified), D6 (Business of Wine) |
| Response types | Multiple choice + short answer | Extended essays; tasting of multiple wines |
| Marking complexity | Criterion-level marks | Band-based holistic marking; examiner discretion |
| Calibration requirement | Single marking key | Cross-examiner calibration; chief examiner review |
| Official sources | One specification | Multiple unit specifications; D2 essay briefs |

### 22.2 Architecture implications

1. **Each Diploma unit will require a separate `examiner_corpus` namespace.**
   A single Examiner Agent cannot serve all units simultaneously without
   cross-contamination between, for example, D3 spirits criteria and D1 wine
   criteria.

2. **Essay marking (D2) is fundamentally different** from short-answer marking.
   The Examiner Agent will need a holistic scoring rubric rather than
   criterion-level marks. This requires a separate calibration process and
   cannot share the Level 3 marking framework.

3. **SAT is common to multiple levels** but the band descriptors change between
   Level 3 and Diploma. The version of the SAT used must be pinned per level and
   per examiner_corpus.

4. **The Tutor Agent can scale horizontally** — one tutor corpus per unit, or
   one unified tutor corpus with unit-level metadata filtering, is both feasible.

5. **Human review requirements increase substantially** at Diploma level. The
   calibration gate (§6.2) must be extended to require D-level-qualified
   reviewers (Diploma graduates or WSET Educators).

6. **This document must be versioned for each level.** When Diploma scope is
   added, a companion `AGENT_BOUNDARIES_DIPLOMA.md` should be created rather
   than modifying this document, to preserve the Level 3 specification.

### 22.3 Do not pre-build Diploma infrastructure now

The current system is scoped for Level 3 only. Do not create Diploma-specific
knowledge folders, corpora, or calibration manifests until the Diploma scope is
formally activated. Premature infrastructure creates contamination risk and
maintenance burden.

---

## Appendix A — Quick Reference Card

### Tutor Agent: permitted at a glance

✅ Explain, teach, guide, encourage  
✅ Use Wine With Jimmy, question bank, enrichment, benchmark answers  
✅ Cite official WSET spec for explanations  
✅ Track learner weak areas and study patterns  
✅ Give formative feedback ("consider adding X")  
❌ Issue summative scores  
❌ Present internal questions as official WSET  
❌ Access `knowledge/calibration/`  

### Examiner Agent: permitted at a glance

✅ Score practice responses against official criteria  
✅ Use official WSET marking keys and specification (Tier 0–1 only)  
✅ Provide criterion-level structured feedback  
✅ Return "no official source found" when retrieval fails  
❌ Use any Tier 2+ source  
❌ Access Tutor Agent context or Nazareth  
❌ Retain session history  
❌ Fabricate marking criteria  

---

## Appendix B — Glossary Cross-Reference

| Term | Defined in | Used in |
|------|-----------|--------|
| Official | §1.1 | §3.2, §5, §6, §9, §10, §15 |
| Pedagogical | §1.2 | §2.1, §3.1, §4, §7, §8 |
| Generated | §1.3 | §4, §7, §17 |
| Benchmark | §1.4 | §3.1, §4, §5 |
| Calibration | §1.5 | §6, §14, §16, §17 |
| Tutor corpus | §10.1 | §9, §10, §11, §16 |
| Examiner corpus | §10.1 | §9, §10, §11, §13, §16 |
| Trust tier | §7 | §3, §9, §10, §16, §17 |
| Contamination | §9 | §9.5, §18.3, §21 |
| Calibration gate | §6.2 | §14, §16, §17, §19 |

---

*This document is part of the WSET-AI-System internal specification.*  
*It defines constraints, not implementations. No agent, pipeline, or prompt*  
*is created by this document.*  
*Update this document when any boundary rule changes. Never change a boundary*  
*rule without updating this document first.*

---
*AGENT_BOUNDARIES.md v1.0 — WSET-AI-System*

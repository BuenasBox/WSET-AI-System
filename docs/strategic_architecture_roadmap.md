# Strategic Architecture Roadmap
## WSET-AI-System — The 5 Breakthroughs That Matter

**Auditor:** Claude (Cowork) — Full System Audit
**Date:** 2026-05-15
**Scope:** Next architectural priorities, ranked by cognitive impact
**Exam date context:** 2026-08-08 — 85 days from audit date

---

## Framing

This roadmap does not list every outstanding task. It identifies the five architectural breakthroughs that would produce qualitatively new cognitive capability — moments where the system's tutoring intelligence makes a step-change, not just incremental improvement.

Tasks like "index the official corpus" or "expand the knowledge graph" are necessary but incremental. The breakthroughs described here are the points at which the system stops doing more of the same and starts doing something it genuinely cannot do today.

---

## Breakthrough 1 — Official Corpus Activation
### "The Tutor gains an authoritative voice"

**What it is:** Indexing the WSET L3 study guide markdown into the Tutor retrieval pipeline, alongside the existing Wine With Jimmy corpus.

**What changes:** Today, when the Tutor Agent explains "why does cool climate produce high acidity?", it retrieves Wine With Jimmy pedagogical content. The explanation is often correct but is framed by a YouTuber's teaching style, not by WSET official language. WSET examiners expect answers in WSET register. A student who learns only from Jimmy may produce answers that are semantically correct but phrased in ways that don't map cleanly to marking criteria.

After this breakthrough, the Tutor Agent can say: *"According to the WSET study guide..."* and cite the exact official framing. The response can be scaffolded: official language first, pedagogical depth second. The Examiner Agent can be calibrated against the same text the Tutor uses for teaching.

**Cognitive capability unlocked:** Authority-grounded explanation. Distinction-level WSET register. Reduced gap between what the student learns and what examiners expect.

**Requires embeddings:** Yes — the markdown files need to be chunked and embedded alongside existing chunks.

**Effort:** Medium (3–5 days). The corpus is already extracted and structured. Column-aware re-extraction for fidelity is recommended but not blocking.

**Priority given exam date:** **URGENT.** With 85 days to exam, every tutoring session without official language grounding is a missed opportunity.

---

## Breakthrough 2 — Misconception Pre-Pass Activation
### "The Tutor learns to listen before it speaks"

**What it is:** Activating the misconception detection pre-pass before every student query response — matching the student's input against `detection_signals` arrays in misconception nodes, and routing to correction before providing explanation.

**What changes:** Today, if a student says "high acidity means the wine is low quality", the Tutor Agent retrieves chunks about acidity and quality and generates a response that may or may not directly correct the specific misconception. The correction depends on what the retrieval returns and how the LLM synthesises it.

After this breakthrough, the same student input triggers a deterministic path: the misconception is detected, the misconception node is retrieved (forced retrieval, bypasses scoring), the correction is applied using the specified intervention type (`direct_correction`, `causal_chain_walkthrough`, etc.), and only then does the standard explanation proceed.

This changes the cognitive model from **retrieve-then-respond** to **diagnose-then-correct-then-explain**. That is a fundamental shift in educational intelligence.

**Cognitive capability unlocked:** Proactive error correction. Misconception-first tutoring. Reduced hardening of incorrect beliefs. Separation of belief diagnosis from knowledge delivery.

**Requires embeddings:** No. Misconception detection is string matching against `detection_signals` arrays. This is a pre-pass before vector search, not a retrieval step.

**Effort:** Low-Medium (2–4 days). The misconception nodes exist. The detection signals are documented. The intervention types are specified. Implementation is a matching function + routing layer.

**Priority given exam date:** **HIGH.** Students preparing for WSET L3 carry specific misconceptions (cool climate = underripe always; more tannin = higher quality; acidity = unpleasant). Correcting these before the exam is more valuable than providing more factual content.

---

## Breakthrough 3 — Structured Causal Chain Response Synthesis
### "The Tutor stops listing facts and starts building arguments"

**What it is:** A response synthesis layer that, when a causal chain is retrieved, renders it as a structured step-by-step explanation rather than as a flat list of text excerpts. Each step is explicitly labelled (Cause → Mechanism → Effect → Wine consequence → Exam formulation).

**What changes:** Today, the Tutor Agent receives 10 retrieved chunks from various Wine With Jimmy videos and the LLM synthesises them into a response. The synthesis is generally coherent but is not guaranteed to follow the causal chain structure. Some responses are lists of facts. Some are explanations. The quality depends on what the LLM decides to produce.

After this breakthrough, when a causal chain node is retrieved (e.g., `CC_COOL_CLIMATE_ACIDITY`), the response follows the chain's step structure explicitly. The student sees:

```
Step 1 — The cause: Cool temperatures during ripening...
Step 2 — The mechanism: Malic acid, which degrades in warmth, is retained...
Step 3 — The effect in the wine: High total acidity, lower pH...
Step 4 — The exam consequence: Use "high acidity" as a descriptor; link to freshness, ageability...
Distinction note: Distinguish malic from tartaric retention. Name the process. Give a regional example.
```

This is not retrieval. This is structured reasoning delivered through a constrained synthesis template. The template does not generate novel steps — it renders the knowledge graph node into pedagogical form.

**Cognitive capability unlocked:** Multi-step mechanistic explanation. Consistent distinction-level structure. Reproducible answer quality regardless of which LLM model is used. Explainable tutoring (the chain steps are traceable to their source nodes).

**Requires embeddings:** No. The synthesis template reads the causal chain node structure directly. It requires graph traversal, not vector search.

**Effort:** Medium (4–7 days). Requires a rendering layer that maps chain node fields to a response template. The hardest part is handling chains that are mid-step or incomplete.

**Priority given exam date:** **HIGH.** The distinction between Pass and Distinction in WSET L3 is almost entirely about causal structure. This breakthrough directly trains the cognitive skill that examiners reward.

---

## Breakthrough 4 — Learner Model Activation (Nazareth Phase 1)
### "The Tutor finally knows who it's talking to"

**What it is:** Activating the Nazareth learner memory system to record and retrieve per-learner weak areas, error taxonomy frequency, and practice history. Connecting this to the Orchestrator's weak-area prioritisation formula.

**What changes:** Today, every conversation starts from zero. The Tutor Agent has no memory of what the student struggled with yesterday, which misconceptions they hold, how their SAT note quality has evolved, or what they have already practised. Every session is a fresh start.

After this breakthrough, the Orchestrator maintains a learner model that tracks:
- Which causal chains the student has been exposed to
- Which error taxonomy labels appear repeatedly (e.g., `missing_causal_link`, `sat_non_commitment`)
- Which regions or topics have low accuracy
- How far the student is from distinction-level answers on recurring question types

The Orchestrator then uses `priority = exam_relevance + recurrence + severity + proximity_to_exam - recent_improvement` to select what to teach next — not what the student asked, but what they need.

**Cognitive capability unlocked:** Adaptive tutoring. Student-specific curriculum. Weak-area targeting. Proximity-to-exam urgency weighting. The system becomes genuinely personalised, not just personable.

**Requires embeddings:** No. Nazareth is a structured JSON store. Retrieval is by learner ID and weak area tag, not by semantic similarity.

**Effort:** Medium-High (7–14 days). The schema is designed. The Orchestrator logic is specified. Implementation requires: Nazareth file write operations after each Examiner session, weak area aggregation across sessions, and Orchestrator routing that reads the learner model before selecting a teaching task.

**Priority given exam date:** **MEDIUM-HIGH.** With 85 days to exam, 6–8 sessions of adaptive tutoring informed by a learner model is significantly more valuable than 6–8 sessions without one. However, Breakthroughs 1–3 deliver more per unit of effort at this distance from exam.

---

## Breakthrough 5 — Examiner Agent Corpus Activation + Calibration Gate Completion
### "The system gains the ability to grade honestly"

**What it is:** Processing the WSET official marking keys, completing the calibration gate checklist, creating the calibration manifest, and activating the Examiner Agent with a verified `examiner_corpus`.

**What changes:** Today, the Examiner Agent exists as a prompt but has no retrieval corpus. When asked to grade an answer, it must rely entirely on its pre-trained knowledge of WSET standards — which is not zero, but is not grounded in official marking keys. Any score it produces is an educated simulation, not a calibrated assessment.

After this breakthrough, the Examiner Agent retrieves from official WSET marking keys (Tier 0), uses the specification (Tier 1) for context, and produces scores with traceable source attribution. The mandatory disclosure is rendered on every output. Each score can be audited back to the retrieved chunk that justified it.

More importantly, the Orchestrator can now connect Examiner feedback to Tutor drills in a documented chain: Examiner finds `missing_causal_link` → Orchestrator routes to Tutor → Tutor retrieves the relevant causal chain → Student drills the mechanism → Examiner re-evaluates.

**Cognitive capability unlocked:** Calibrated summative feedback. Claim-to-source traceability. Closed-loop learning: diagnose → teach → assess → re-teach. The full agent architecture becomes operational.

**Requires embeddings:** Yes — marking keys must be processed (text extraction from PDFs, chunking, embedding, ingestion with `trust_tier: 0` metadata).

**Effort:** High (14–21 days). The blocking constraint is the calibration gate: a WSET-qualified human must review the marking keys and sign off the calibration manifest before ingestion. This is not an engineering problem — it is a review process that requires a person.

**Priority given exam date:** **MEDIUM.** This is the highest-value long-term investment but the longest to execute. Given the 85-day window, Breakthroughs 1–3 deliver more exam-proximate value. Breakthrough 5 is the most important for the system's post-exam evolution.

---

## Priority Summary

| # | Breakthrough | Exam-date priority | Effort | Requires embeddings |
|---|---|---|---|---|
| 1 | Official corpus activation | **URGENT** | Medium | Yes |
| 2 | Misconception pre-pass | **HIGH** | Low-Medium | No |
| 3 | Structured causal chain synthesis | **HIGH** | Medium | No |
| 4 | Learner model (Nazareth Phase 1) | Medium-High | Medium-High | No |
| 5 | Examiner corpus + calibration | Medium | High | Yes |

**Recommended execution order given exam date:** 2 → 3 → 1 → 4 → 5

Rationale: Breakthroughs 2 and 3 require no embeddings and deliver immediate pedagogical improvement in every session. Breakthrough 1 requires embedding infrastructure but is unblocking for everything else. Breakthroughs 4 and 5 are high-value but require more time than the exam window allows for full deployment.

---

## What None of These Breakthroughs Require

- A new language model
- A different embedding model
- A different vector database
- Fine-tuning on WSET data
- More Wine With Jimmy videos

The system's ceiling is not constrained by its model or its hardware. It is constrained by the gap between its well-designed architecture and its current implementation depth. Close that gap.

---

*Generated: 2026-05-15 | Claude (Cowork) — Audit Role*
*This roadmap is strategic guidance, not a sprint plan. Effort estimates are approximate.*

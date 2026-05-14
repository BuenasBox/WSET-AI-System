# WSET-AI-System — Semantic Retrieval Architecture

**Version:** 1.0  
**Date:** 2026-05-13  
**Status:** Authoritative — governance document  
**Audience:** System architects, ML engineers, agent developers  
**Classification:** Internal — not for learner access

---

## 1. Document Purpose

This document defines the complete semantic retrieval architecture for the WSET-AI-System. It governs how content is retrieved, weighted, and filtered for the Tutor Agent and the Examiner Agent. It defines the trust tier hierarchy, hybrid retrieval design, semantic chunk scoring logic, and the strict asymmetry that must be maintained between the two agents at every layer of the retrieval stack.

This document is the authoritative reference for retrieval system design. Any implementation that deviates from these specifications must be approved by the system architect and recorded in the change log.

---

## 2. Foundational Principle: Asymmetric Retrieval

The Tutor Agent and the Examiner Agent are not symmetrical systems and must never be treated as variants of a single retrieval pipeline. They differ in purpose, permitted sources, scoring authority, and acceptable failure modes.

| Dimension | Tutor Agent | Examiner Agent |
|-----------|-------------|----------------|
| Primary purpose | Scaffold understanding | Evaluate against standard |
| Acceptable error direction | Over-explain (recoverable) | Under-score (recoverable) |
| Unacceptable error direction | Under-explain | Over-score / hallucinate score |
| Source scope | Tiers 0–4 (broad) | Tiers 0–1 only (narrow) |
| Permitted enrichment | Yes | No |
| Semantic drift tolerance | Moderate | Zero |
| Retrieval flexibility | High | Low |

**Immutable rule:** The Tutor Agent's retrieval corpus and the Examiner Agent's retrieval corpus must be physically separate vector stores. No shared retrieval index is permitted. This is not a configuration — it is an architectural requirement.

---

## 3. Trust Tier Hierarchy

The trust tier system governs which sources may be used in retrieval, and with what weight, for each agent. All knowledge assets in the system are assigned a trust tier at ingestion.

### Tier 0 — Official Marking Authority

**Definition:** Content produced by WSET as authoritative assessment instruments.  
**Examples:** WSET Level 3 mark schemes, examiner guidance notes, official answer keys, grade descriptors (Pass/Merit/Distinction), WSET Chief Examiner reports.  
**Tutor Agent access:** Yes — with restriction. May use as reference for what constitutes a correct answer, but must not reproduce official mark scheme language verbatim to learners.  
**Examiner Agent access:** Primary and mandatory. All scoring decisions must be traceable to Tier 0 sources.  
**Retrieval weight (Tutor):** 1.0 (highest) for factual correctness anchoring  
**Retrieval weight (Examiner):** 1.0 (mandatory for any scoring operation)

### Tier 1 — Official WSET Specification

**Definition:** WSET-published course materials, textbooks, and learning specifications.  
**Examples:** WSET Level 3 Award in Wines textbook (current edition), WSET course specifications, official unit descriptors, official SAT (Systematic Approach to Tasting) documentation.  
**Tutor Agent access:** Yes — primary knowledge source.  
**Examiner Agent access:** Yes — secondary source for interpreting context of Tier 0 content.  
**Retrieval weight (Tutor):** 0.95  
**Retrieval weight (Examiner):** 0.90

### Tier 2 — Official SAT Framework

**Definition:** The WSET Systematic Approach to Tasting as an independent assessment standard.  
**Note:** Separated from Tier 1 because the SAT has specific scoring authority in tasting-based assessments and requires dedicated handling.  
**Tutor Agent access:** Yes — must be used for any sensory assessment scaffolding.  
**Examiner Agent access:** Yes — authoritative for sensory question scoring.  
**Retrieval weight (Tutor):** 0.95 for SAT-related queries  
**Retrieval weight (Examiner):** 1.0 for SAT-based questions

### Tier 3 — Benchmark Answers

**Definition:** Curated exemplar answers that have been validated by WSET-qualified reviewers as representative of Pass, Merit, and Distinction standards.  
**Examples:** Model answers in the question bank (when validated), internally curated mark-calibrated answer examples.  
**Tutor Agent access:** Yes — for showing students what good answers look like.  
**Examiner Agent access:** Yes — as calibration anchors only, not as primary scoring authority.  
**Retrieval weight (Tutor):** 0.85  
**Retrieval weight (Examiner):** 0.70 (calibration context only, never primary score source)

### Tier 4 — Pedagogical Enrichment

**Definition:** High-quality educational content that supplements official materials without being officially sanctioned.  
**Examples:** Wine With Jimmy transcripts (after human review pass), WSET Diploma-level explanations used as enrichment for L3, expert sommelier commentary, peer-reviewed enology research used for mechanistic depth.  
**Tutor Agent access:** Yes — with pedagogical role tagging. Must be flagged as enrichment, never as authoritative.  
**Examiner Agent access:** FORBIDDEN.  
**Retrieval weight (Tutor):** 0.70 maximum (always below Tier 0–3)  
**Retrieval weight (Examiner):** 0.00 (blocked at ingestion)

### Tier 5 — Generated / Internal Enrichment

**Definition:** AI-generated content, internal training examples, draft pedagogical explanations pending review.  
**Examples:** Generated misconception examples, draft causal chain explanations, AI-assisted study notes.  
**Tutor Agent access:** Limited — must be tagged as `generated` and must not be presented to learners as authoritative.  
**Examiner Agent access:** FORBIDDEN.  
**Retrieval weight (Tutor):** 0.50 maximum (lowest tier)  
**Retrieval weight (Examiner):** 0.00 (blocked at ingestion)

---

## 4. Retrieval Type Taxonomy

The system recognises nine retrieval types. Each type has distinct retrieval logic, source filtering, and agent applicability.

### 4.1 Concept Retrieval

**Purpose:** Answer definitional or explanatory questions about a wine concept.  
**Query forms:** "What is tannin?", "Explain acidity in wine.", "What does malic acid do?"  
**Primary sources:** Concept nodes (knowledge graph), Tier 1 textbook sections.  
**Graph involvement:** Direct concept node lookup; follow `is_component_of` and `prerequisite_for` edges for context.  
**Agent:** Both Tutor and Examiner (Examiner: Tier 0–1 only).

### 4.2 Misconception Retrieval

**Purpose:** Detect and correct a student's erroneous belief.  
**Query forms:** Detection via `detection_signals` pattern matching against student input.  
**Primary sources:** Misconception nodes (knowledge graph), then causal chain for correction.  
**Graph involvement:** Misconception node → `why_incorrect` → linked causal chain for correction walkthrough.  
**Agent:** Tutor Agent only. Examiner Agent does not engage in misconception correction.

### 4.3 Causal Chain Retrieval

**Purpose:** Provide mechanistic, multi-step explanation at Distinction level.  
**Query forms:** "Why does...", "How does... affect...", "Explain the relationship between...", "What causes..."  
**Primary sources:** Causal chain nodes; Tier 1 textbook for supporting facts.  
**Graph involvement:** Chain start → sequential step traversal → final outcome → examples.  
**Agent:** Tutor Agent primary. Examiner Agent may reference for marking context but not for explanation generation.

### 4.4 Comparative Retrieval

**Purpose:** Compare two or more concepts, regions, styles, or techniques.  
**Query forms:** "How does X differ from Y?", "Compare...", "What is the difference between..."  
**Primary sources:** Relationship nodes (`contrasts_with`, `often_confused_with`); concept nodes; regional concept nodes.  
**Graph involvement:** Retrieve both target concept nodes; retrieve any `contrasts_with` or `often_confused_with` edges between them; synthesise comparison.  
**Agent:** Tutor Agent primary.

### 4.5 Region Retrieval

**Purpose:** Answer questions about specific wine regions, appellations, or regional styles.  
**Query forms:** "Tell me about Sauternes.", "What grapes are used in Barolo?", "Describe the Mosel wine style."  
**Primary sources:** Regional concept nodes (Phase 3+); Tier 1 textbook regional sections.  
**Graph involvement:** Regional concept → related grape concepts → climate concept → style outcome.  
**Agent:** Both (Examiner: Tier 0–1 only, no enrichment).

### 4.6 Tasting Retrieval

**Purpose:** Support SAT-based tasting note construction or assessment.  
**Query forms:** "How do I describe this wine's acidity?", "What SAT language should I use for a full-bodied red?", "Is this tannin level high or medium?"  
**Primary sources:** Tier 2 (SAT framework); sensory-structural inference chains (Phase 7+).  
**Graph involvement:** Sensory descriptor → structural inference → style conclusion.  
**Agent:** Both (Examiner: SAT Tier 2 only; Tutor: may use Tier 4 enrichment for sensory vocabulary development).

### 4.7 Exam Strategy Retrieval

**Purpose:** Help students understand how to structure exam answers, allocate marks, and achieve Distinction.  
**Query forms:** "How do I write a Distinction answer?", "What should I include in a 6-mark question?", "How do I structure my answer about..."  
**Primary sources:** `distinction_note` fields in causal chains; Tier 3 benchmark answers; internal exam strategy content.  
**Graph involvement:** Causal chain `distinction_note` → related exam questions → benchmark answer patterns.  
**Agent:** Tutor Agent only. Examiner Agent does not provide exam strategy guidance.

### 4.8 Weakness-Targeted Retrieval

**Purpose:** Retrieve content specifically matched to a learner's identified knowledge gaps.  
**Query forms:** System-triggered (not student-initiated) based on learner performance model.  
**Primary sources:** Misconception nodes for identified error patterns; concept nodes for gaps; causal chains for weak mechanistic understanding.  
**Graph involvement:** Learner weakness profile → target concept nodes → misconception nodes → corrective chains.  
**Agent:** Tutor Agent only. Requires learner model (Phase 8+).

### 4.9 Progression Retrieval

**Purpose:** Retrieve content at the appropriate difficulty level for the learner's current stage.  
**Query forms:** System-triggered based on learner level assessment.  
**Primary sources:** Concept nodes filtered by `difficulty` field; chains filtered by `complexity` field.  
**Graph involvement:** Learner level → concept difficulty filter → appropriate chain complexity.  
**Agent:** Tutor Agent only. Requires learner model (Phase 8+).

---

## 5. Semantic Chunk Scoring Logic

Every retrieved chunk is scored on eight dimensions before being included in a retrieval result set. The composite score determines ranking and inclusion threshold.

### 5.1 Scoring Dimensions

**Dimension 1: Source Trust Score (STS)**  
Maps directly from trust tier: Tier 0 = 1.0, Tier 1 = 0.95, Tier 2 = 0.95, Tier 3 = 0.85, Tier 4 = 0.70, Tier 5 = 0.50.

**Dimension 2: Semantic Similarity Score (SSS)**  
Standard cosine similarity between query embedding and chunk embedding. Range: 0.0–1.0.

**Dimension 3: WSET Alignment Score (WAS)**  
Binary + gradient. A chunk that is directly from WSET materials scores 1.0. A chunk from pedagogical enrichment that has been validated against WSET L3 curriculum scores 0.8. A chunk from enrichment that has not been explicitly validated against WSET L3 scores 0.5. Non-WSET content scores 0.3.

**Dimension 4: Topic Density Score (TDS)**  
Measures how densely the chunk covers the topic of the query. Single-concept chunks score higher for focused queries. Multi-concept chunks score higher for comparative queries.

**Dimension 5: Causal Richness Score (CRS)**  
Bonus for chunks that contain causal mechanism content (cause→effect explanations). Range: 0.0 (no causal content) to 1.0 (full causal chain). Relevant only for `causal_chain` and `concept` retrieval types. Irrelevant for `tasting` and `exam_strategy` types.

**Dimension 6: Misconception Density Score (MDS)**  
Bonus for chunks that contain explicitly flagged misconception correction content. Relevant only for `misconception` and `weakness_targeted` retrieval types.

**Dimension 7: Calibration Safety Score (CSS)**  
Critical for Examiner Agent. Binary: 1.0 if source is Tier 0–2; 0.0 if source is Tier 3–5. For the Tutor Agent, CSS is advisory only.

**Dimension 8: Agent Eligibility Flag (AEF)**  
Boolean: `tutor_eligible` and `examiner_eligible`. Chunks flagged `examiner_eligible: false` must be excluded from all Examiner Agent retrievals, regardless of other scores.

### 5.2 Composite Score Formula

**Tutor Agent composite score:**
```
TutorScore = (STS × 0.20) + (SSS × 0.35) + (WAS × 0.15) + (TDS × 0.10) 
           + (CRS × 0.10) + (MDS × 0.05) + (CSS × 0.05)
```

**Examiner Agent composite score:**
```
ExaminerScore = (STS × 0.40) + (SSS × 0.25) + (WAS × 0.20) + (CSS × 0.15)
```
Note: Examiner Agent scoring eliminates CRS, MDS, and TDS dimensions. CSS has four times the Tutor Agent weight. Source trust dominates.

### 5.3 Exclusion Rules (Hard Filters Applied Before Scoring)

The following exclusion rules are applied as hard filters before composite scoring. Chunks that fail any exclusion rule are removed from the candidate set entirely and do not receive a score.

| Rule ID | Filter | Applies to |
|---------|--------|-----------|
| EX-01 | `examiner_eligible: false` → exclude | Examiner Agent |
| EX-02 | Trust Tier ≥ 4 → exclude | Examiner Agent |
| EX-03 | `ingestion_status: "deprecated"` → exclude | Both agents |
| EX-04 | `ingestion_status: "draft"` → exclude from production | Both agents (development only) |
| EX-05 | Source = `wine_with_jimmy` → exclude | Examiner Agent |
| EX-06 | Source = `generated` → exclude | Examiner Agent |
| EX-07 | Source = `diploma_enrichment` without explicit L3 downgrade tag → exclude | Examiner Agent |

### 5.4 Minimum Score Thresholds

| Agent | Minimum composite score for inclusion |
|-------|--------------------------------------|
| Tutor Agent | 0.55 |
| Examiner Agent | 0.70 |

The Examiner Agent's higher minimum threshold reflects the requirement for high-confidence source alignment before any scoring decision is supported.

---

## 6. Hybrid Retrieval Architecture

The system uses a hybrid retrieval approach combining dense vector search with structured graph traversal. Neither component is sufficient alone.

### 6.1 Dense Vector Search (Layer 1)

**Technology:** Embedding model (to be specified in implementation phase) over pre-encoded knowledge chunks.  
**Function:** Semantic similarity matching — find chunks whose embedding is close to the query embedding.  
**Limitation:** Dense search is blind to graph structure and cannot natively follow cause→effect chains or detect misconception correction patterns.

### 6.2 Knowledge Graph Traversal (Layer 2)

**Technology:** In-memory graph traversal over the JSON knowledge graph.  
**Function:** Structured retrieval based on known concept relationships. When a concept node is identified from Layer 1, Layer 2 follows graph edges to retrieve related misconceptions, causal chains, and contrasting concepts.  
**Limitation:** Graph traversal requires a concept entry point. Cold queries without a clear concept match must rely on Layer 1 first.

### 6.3 Retrieval Fusion (Layer 3)

**Function:** Merge and re-rank results from Layers 1 and 2 using the composite scoring formula defined in §5.2.  
**Design principle:** Graph-retrieved nodes receive a +0.10 bonus to their composite score when the graph traversal was triggered by a confirmed concept match (not a candidate concept). This rewards structured knowledge over raw semantic similarity.

### 6.4 Query Intent Classification (Pre-Retrieval)

Before retrieval begins, every query must be classified into one of the nine retrieval types defined in §4. The classification determines:
- Which exclusion filters to apply
- Which composite score weights to use (CRS and MDS are only active for specific types)
- Which graph traversal strategy to employ
- Whether to activate misconception detection pre-pass

### 6.5 Misconception Detection Pre-Pass

Before any standard retrieval, all student-initiated queries undergo a misconception detection pre-pass:
1. The query text is matched against `detection_signals` arrays across all misconception nodes
2. If a match is found (above threshold), the misconception correction path is activated
3. The misconception node is retrieved directly (bypassing composite scoring — it is a forced retrieval)
4. After presenting the correction, standard retrieval resumes for the underlying topic

This pre-pass ensures that misconceptions are caught before the Tutor Agent provides a substantive explanation that might inadvertently reinforce the error.

---

## 7. Retrieval Result Set Governance

### 7.1 Maximum chunks per retrieval

| Retrieval type | Tutor Agent max | Examiner Agent max |
|---------------|----------------|-------------------|
| Concept | 5 | 3 |
| Misconception | 3 | N/A |
| Causal chain | 4 (one full chain) | 2 |
| Comparative | 6 (3 per concept) | 3 |
| Region | 5 | 3 |
| Tasting | 4 | 3 |
| Exam strategy | 5 | N/A |
| Weakness-targeted | 6 | N/A |
| Progression | 5 | N/A |

### 7.2 Source diversity requirement

For Tutor Agent retrievals with ≥ 3 chunks, no more than 60% of chunks may come from the same source type (e.g., no more than 3 of 5 chunks from `wine_with_jimmy` transcripts). This prevents mono-source responses and encourages multi-perspective synthesis.

Source diversity does not apply to the Examiner Agent, which deliberately limits to authoritative sources.

### 7.3 Retrieval provenance logging

Every retrieval result set must be logged with:
- Query text (hashed for privacy)
- Retrieval type classification
- Agent type
- Chunks retrieved (source ID, trust tier, composite score)
- Whether misconception pre-pass was triggered
- Whether any exclusion filters were activated

This log is the audit trail required by AGENT_BOUNDARIES.md §8.

---

## 8. Retrieval Failure Modes and Mitigations

| Failure mode | Description | Mitigation |
|-------------|-------------|------------|
| **Tier contamination** | Tier 4–5 content appears in Examiner retrieval | Hard filter EX-02; separate vector stores |
| **Semantic drift** | Examiner uses pedagogical explanation context for scoring | CSS filter; Examiner-only score formula |
| **Overhelping** | Examiner provides hints during live assessment | Retrieval type lock: assessment mode disables Tutor-type queries |
| **Low-confidence scoring** | Examiner scores without Tier 0 support | Minimum threshold 0.70; mandatory CSS = 1.0 for scoring operations |
| **Misconception reinforcement** | Tutor answer implicitly confirms incorrect belief | Misconception pre-pass before any substantive retrieval |
| **Cold start (no concept match)** | Query does not match any known concept | Fallback to Tier 1 broad semantic search; flag for human review |
| **Outdated content** | Deprecated nodes appear in results | EX-03 filter; manifest deprecation tracking |

---

## 9. Future Architecture Extensions

### 9.1 Retrieval Explainability Layer

Each agent response should be accompanied by a retrieval provenance summary for internal use:
- Which nodes/chunks were retrieved
- Their trust tiers and composite scores
- Which graph edges were traversed
- Which retrieval type was classified

This explainability layer is mandatory for the Examiner Agent and strongly recommended for the Tutor Agent.

### 9.2 Adaptive Retrieval Weighting

Phase 8 introduces learner modeling. When a learner model is active, retrieval weights can be personalised:
- Learners with identified misconceptions receive higher MDS weight
- Learners at foundational level receive lower CRS weight (simpler explanations)
- Learners approaching exam receive higher exam_strategy retrieval probability

### 9.3 Multi-Language Retrieval

Phase scaling to multi-language support requires language-specific vector stores while maintaining a shared knowledge graph (concept node IDs are language-independent). Retrieval logic is identical; only the embedding model and chunk text change.

---

*This document is authoritative for retrieval system design. Implementations that deviate must be approved and documented. This document does not contain official WSET assessment guidance.*

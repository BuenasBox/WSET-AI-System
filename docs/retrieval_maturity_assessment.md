# Retrieval Maturity Assessment
## WSET-AI-System — Phase 1 Audit

**Auditor:** Claude (Cowork) — Full System Audit
**Date:** 2026-05-15
**Evidence base:** 5 retrieval sandbox runs + retrieval architecture document + corpus inspection
**Status:** Authoritative internal assessment

---

## 1. What Is Currently Indexed

| Component | Status | Chunks |
|---|---|---|
| Wine With Jimmy transcripts (clean) | ✅ Indexed and active | 333 |
| WSET official study guide markdown | ❌ Not yet indexed | 0 |
| Knowledge graph nodes | ✅ Partially loaded (~54 nodes) | 54 |
| WSET master dictionary | ✅ Active | 424 terms |
| Golden chunk annotations | ✅ Active | 166 |
| Examiner corpus | ❌ Empty | 0 |
| Question bank | ❌ Not indexed | 0 |

**Critical observation:** The official WSET corpus (46 extracted chapters, ~450,000 characters) is **not yet in the retrieval index**. Every retrieval run draws entirely from Wine With Jimmy pedagogical content. The system currently operates without its primary authoritative knowledge source in any retrieval pipeline.

---

## 2. Is It Still Mostly Lexical?

**Partial yes, partial no — and this distinction matters.**

### Evidence that lexical dominates

The SAT-related query ("How do I justify quality in SAT?") produced:
- `matched_concepts: none`
- `matched_causal_chains: none`
- `knowledge_graph_boost_applied: false` on all 10 results
- Retrieval driven entirely by term matching ("SAT", "balance", "BICL", etc.)

The balance query ("What does balance mean in WSET tasting?") similarly showed:
- `matched_concepts: none`
- `knowledge_graph_boost_applied: false` on all results
- Ranking correlates with term frequency of "balance", "intensity", "length"

**For tasting-domain queries, the system is primarily lexical today.**

### Evidence that semantic graph retrieval IS working

The cool climate + acidity query ("How does cool climate affect acidity?") showed:
- `matched_concepts: Acidity, Cool Climate` ✅
- `matched_causal_chains: Cool climate → high acidity in finished wine, Cool climate → limited sugar accumulation → lower potential alcohol, Cool climate → slower ripening → primary aroma profile` ✅
- `knowledge_graph_boost_applied: true` on multiple chunks ✅
- Query expansion of 40+ terms (including misconceptions like "cool climate wines always have green, unripe flavours") ✅

This demonstrates **genuine semantic graph traversal** when the query matches a known concept node. The graph is functioning.

### The core issue

Graph retrieval works only when the query term maps to a known concept ID. With approximately 8 concepts populated (RA1 foundational), queries about regions, regulations, fortified wines, sparkling production, or tasting methodology fall back to pure lexical retrieval. The system is **graph-capable but graph-sparse**.

---

## 3. Which Retrieval Scores Are Meaningful?

### Meaningful scores

| Score range | Interpretation | Evidence |
|---|---|---|
| > 0.75 | Strong lexical + semantic match; reliable retrieval | Run 04, chunk 1: 0.7998 (Loire climate + acidity — genuine relevance) |
| 0.65–0.75 | Good match; likely relevant | Most run 04 chunks |
| 0.55–0.65 | Moderate; may be topically adjacent rather than directly relevant | Runs 01, 05 |
| < 0.55 | Weak; often coincidental term matching | Runs 01, 02 lower results |

### Pseudo-semantic scores (caution warranted)

When `knowledge_graph_boost_applied: false`, the ranking reflects:
1. **Query expansion term frequency** — terms like "balance", "intensity", "length" appear in many chunks regardless of the chunk's actual relevance to the query's intent
2. **Golden chunk bias** — chunks marked as "golden" receive a boost that can elevate them above genuinely more relevant chunks
3. **Pedagogical role alignment** — a chunk tagged `exam_strategy` is boosted for exam-related queries even if its content is not about the specific concept asked

The "why" field in retrieval results lists many reasons for inclusion, but several are coincidental rather than semantic (e.g., chunk 1 in run_01 about "preparing for the tasting exam" ranked highest for "how to justify quality in SAT" — it's related but not precise).

---

## 4. Retrieval Quality by Query Type

| Query Type | Graph Active | Retrieval Quality | Confidence |
|---|---|---|---|
| Cause-effect (known concept) | ✅ Yes | High — multi-chain matching | High |
| Cause-effect (unknown concept) | ❌ No | Medium — lexical proximity | Medium |
| SAT reasoning | ❌ No | Medium — term matching only | Medium |
| Exam strategy | ❌ No | Medium — golden chunk boost | Medium |
| Region-specific | ❌ No (regions not in graph) | Low-Medium | Low |
| Misconception detection | ❌ No misconception pre-pass in sandbox | Low — not yet implemented | Low |
| Comparative retrieval | ❌ No comparison edges active | Low | Low |

---

## 5. What Reasoning Patterns Are Genuinely Emerging?

### Genuine emergence

1. **Concept-anchored causal retrieval** — When a student asks a "why" question about a known concept (acidity, cool climate, tannin), the system correctly traverses multiple causal chains and retrieves chunks that together cover the mechanism. This is proto-reasoning, not just keyword matching.

2. **Misconception-aware query expansion** — The query expansion for cool climate included the strings of known misconceptions ("cool climate wines always have green, unripe flavours"). This means a student who states a misconception will generate query terms that match the correction content. This is a lightweight form of misconception detection.

3. **Intent classification** — The system correctly identifies `cause_effect_explanation` vs. `sat_coaching` vs. `tasting_calibration` and adjusts retrieval accordingly. This is meaningful routing intelligence.

### Still simulated

1. **Multi-hop reasoning** — The system retrieves chunks from multiple sources that could support a multi-hop explanation, but it does not yet chain these into a structured argument. A human (or LLM response) must synthesise across chunks. The graph traversal retrieves the pieces, not the reasoning.

2. **Misconception intervention** — The architecture specifies a pre-pass that detects misconceptions before returning results. This is not yet operational. Misconceptions are in query expansion terms but are not triggering the explicit detection-correction pathway.

3. **Cross-region comparison** — Comparative queries require relationship edge traversal (`contrasts_with`, `often_confused_with`). These edges are designed but not populated for regions.

---

## 6. What Is Missing Before "Thinking" Can Emerge?

In priority order:

1. **Official corpus indexing** — Without the WSET text in retrieval, the Tutor Agent reasons from pedagogy without authoritative grounding. This is the single most important gap.

2. **Knowledge graph expansion beyond RA1** — 8 concepts covering RA1 means 80% of the curriculum is lexically retrieved. Expanding to 40–50 concepts across all RAs would dramatically improve retrieval quality for regional and fortified/sparkling wine queries.

3. **Misconception pre-pass activation** — The detection signals exist in the misconception nodes but the pre-pass is not yet running. Activating it would make the system proactively corrective rather than reactively informative.

4. **Response synthesis layer** — Retrieved chunks are ranked but not composed into structured explanations. The LLM generates synthesis at response time from a flat list of excerpts. A retrieval-to-reasoning bridge that maps chunks to causal chain steps would enable structured multi-step explanations.

5. **Source diversity enforcement** — The SEMANTIC_RETRIEVAL_ARCHITECTURE specifies no more than 60% of chunks from the same source. Current runs show 8–10 chunks from 3–4 Wine With Jimmy videos, creating mono-source responses for many queries.

---

## 7. False-Positive and Contamination Risks

### False-positive risks (Tutor Agent)

- **Diploma-level content in L3 corpus:** Several Wine With Jimmy videos are explicitly about WSET Diploma (L4). These are in the indexed corpus. A student asking about Barossa or Chianti may receive Diploma-level explanation that is deeper than L3 requires or subtly different in emphasis. Risk: medium.

- **Exam strategy over-retrieval:** Golden chunk boost means exam strategy chunks (how to structure answers) appear in retrievals for factual queries. The top results for "What does balance mean?" include "how to memorise the SAT" — correct domain but wrong pedagogical role.

- **Outdated content from non-2026 Wine With Jimmy videos:** No date-currency filter is applied. If Wine With Jimmy content references older WSET L3 editions with different content, it could introduce specification drift.

### Contamination risks (Examiner Agent)

The Examiner Agent corpus is currently empty. There is no contamination risk today because the agent has nothing to retrieve from. However, when activated:

- The marking keys in `knowledge/official-wset/marking-keys/` are PDFs. They have not been processed through any extraction pipeline. Before activation, they must be extracted, validated, and indexed with `trust_tier: 0`.
- No `calibration_manifest.json` exists. The calibration gate (AGENT_BOUNDARIES.md §6.2) would block Examiner Agent activation if properly enforced.

---

## 8. Overall Retrieval Maturity Score

| Dimension | Score | Assessment |
|---|---|---|
| Corpus completeness | 3/10 | Official corpus unindexed; 333 chunks from 1 pedagogical source |
| Retrieval precision | 6/10 | Graph matching works for RA1; lexical elsewhere |
| Query intelligence | 7/10 | Intent classification + expansion are strong |
| Graph utilisation | 4/10 | Graph works but underpopulated |
| Misconception handling | 3/10 | Designed but not operational |
| Source diversity | 4/10 | Effectively mono-source (Wine With Jimmy) |
| Examiner readiness | 0/10 | No corpus, no calibration |
| **Overall** | **4/10** | Functional prototype — strong architecture, partial execution |

---

*This assessment reflects the state of the retrieval system as of 2026-05-15.*
*Generated by: Claude (Cowork) — Audit Role*

# WSET-AI-System — Knowledge Graph Retrieval Strategy

**Version:** 1.0  
**Date:** 2026-05-13  
**Status:** Authoritative — governance document  
**Audience:** ML engineers, graph system architects, Tutor Agent developers  
**Classification:** Internal

---

## 1. Purpose

This document defines the GraphRAG (Graph-augmented Retrieval Augmented Generation) strategy for the WSET-AI-System knowledge graph. It specifies how the graph is structured, how traversal is performed, how graph-retrieved knowledge is fused with dense vector search results, and how the graph uniquely enables pedagogical precision that pure vector search cannot achieve.

The knowledge graph is not a supplementary feature — it is the epistemological core of the Tutor Agent's ability to reason causally, detect misconceptions, and differentiate Pass from Distinction explanations. This document explains exactly why and how.

---

## 2. Why GraphRAG for WSET Pedagogy

### 2.1 Limitations of pure vector search in educational contexts

Pure dense vector search is semantic — it finds chunks that are about the same topic as the query. For factual recall, this is often sufficient. But WSET Level 3 exam questions, particularly those targeting Merit and Distinction, do not test factual recall — they test causal reasoning. "Cool climates produce high-acidity wines" is a fact; "cool temperatures slow malic acid degradation, retaining higher levels of malic acid at harvest because enzymatic breakdown rate decreases with temperature" is the Distinction-level mechanism.

A dense search for "cool climate acidity" will return chunks about cool climate and acidity. It will not automatically chain the causal steps or prioritise the mechanistic explanation over the correlational one. The knowledge graph does.

### 2.2 Misconception topology cannot be represented in flat vectors

A misconception is not simply an incorrect fact — it has structure: what the student believes, why that belief is wrong, what triggers it, and what the correct replacement is. This structure is a graph relationship, not a vector proximity. Identifying a misconception requires pattern matching against detection signals and then traversing to the correction, the mechanism, and the confirmation. This is fundamentally a graph operation.

### 2.3 Distinction answers require multi-hop reasoning

A Distinction-level answer about botrytis and acidity in Sauternes requires connecting: botrytis infection mechanism → tartaric acid metabolism → gluconic acid production → lower-than-expected acidity despite concentration. This is a four-hop causal chain. Vector search may retrieve individual facts from any of these hops, but only graph traversal guarantees the full chain is retrieved and presented in the correct causal sequence.

---

## 3. Graph Structure

### 3.1 Node types (defined in KNOWLEDGE_GRAPH_ARCHITECTURE.md)

| Node type | ID prefix | Primary use in retrieval |
|-----------|-----------|--------------------------|
| Topic | `T_` | Domain scoping and context anchoring |
| Concept | `C_` | Entry points for all retrieval queries |
| Relationship | `R_` | Edges between concepts; traversal paths |
| Misconception | `MC_` | Error detection and correction nodes |
| Causal Chain | `CC_` | Multi-step mechanistic explanation objects |

### 3.2 Edge taxonomy

Edges in the knowledge graph are typed. The edge type determines how the graph is traversed and what the traversal result means semantically.

**Directed causal edges** (traversal follows the arrow):
- `causes` — A produces B through a direct mechanism
- `produces` — A generates B as output
- `increases` — A raises the quantity or intensity of B
- `decreases` — A lowers the quantity or intensity of B
- `reduces` — A diminishes B (similar to decreases, but specific to quality or quantity reduction)
- `requires` — A cannot exist or function without B

**Directed facilitating/inhibiting edges**:
- `influences` — A affects B without fully determining it (partial causation)
- `improves` — A enhances or elevates B
- `inhibits` — A prevents or slows B

**Compositional edges**:
- `is_component_of` — A is a constituent part of B
- `is_indicator_of` — A is a diagnostic signal of B's presence
- `prerequisite_for` — A must be understood before B

**Semantic distinction edges** (bidirectional):
- `contrasts_with` — A and B are distinct; often confused
- `often_confused_with` — A is commonly mistaken for B (asymmetric — can differ from `contrasts_with`)
- `accompanies` — A and B typically co-occur in practice

### 3.3 Edge weight conventions

All edges have a `strength` property (`weak` / `moderate` / `strong`). Traversal algorithms multiply edge weights by the base confidence of the source node. This prevents weak relationships from dominating retrieval results.

| Strength | Traversal multiplier |
|---------|---------------------|
| `strong` | 1.0 |
| `moderate` | 0.75 |
| `weak` | 0.50 |

---

## 4. Graph Traversal Strategies

### 4.1 Single-hop concept retrieval

**Use case:** Simple concept question; entry-level query.  
**Algorithm:**
1. Identify target concept from query (dense search or direct concept ID match)
2. Retrieve concept node
3. Return `definition` field (foundational mode) or `definition` + `distinction_insights` (distinction mode)

**Depth:** 1 hop (concept node only)  
**Traversal edges used:** None (no edge traversal in single-hop)

---

### 4.2 Misconception correction traversal

**Use case:** Misconception pre-pass detects a `detection_signal` match.  
**Algorithm:**
1. Pre-pass matches student input against `detection_signals` array in all `MC_` nodes
2. Retrieve the matched misconception node directly (not via scoring — forced retrieval)
3. Traverse from the misconception node to its linked `related_concepts[]` — retrieve all linked concept nodes
4. From the linked concept node, traverse `cause_effect_links[]` to identify the relevant causal chain for the correction
5. Retrieve the causal chain node
6. Assemble correction: misconception (what the student believes) → why incorrect → mechanism from chain → corrected understanding → concrete example

**Depth:** 3 hops (misconception → concept → causal chain)  
**Traversal edges used:** `related_concepts` reference, `cause_effect_links` reference

---

### 4.3 Causal chain traversal

**Use case:** Distinction-level explanation of a mechanism.  
**Algorithm:**
1. Identify starting concept from query (dense search entry)
2. From concept node, retrieve `cause_effect_links[]` — these point to causal chain IDs
3. Select the most relevant chain based on query semantic similarity to chain name and `starting_factor`
4. Retrieve the full chain node
5. Return all `intermediate_steps[]` in order, each with its `relationship_type` and `description`
6. Return `final_outcome` and `examples[]`
7. Retrieve `distinction_note` if in Distinction mode

**Depth:** 2 hops (concept → chain; the chain steps are internal to the node)  
**Traversal edges used:** `cause_effect_links` reference  
**Note:** Causal chain steps are encoded within the chain node as an ordered array, not as individual graph edges. This design choice trades some graph query flexibility for reliability of step sequence.

---

### 4.4 Comparative traversal

**Use case:** Compare/contrast two concepts.  
**Algorithm:**
1. Identify both target concepts from query
2. Retrieve both concept nodes
3. Search relationship nodes for any edge where: `source_concept` = A and `target_concept` = B (or vice versa) with `relationship_type` in {`contrasts_with`, `often_confused_with`}
4. If a direct relationship edge exists: retrieve it and use its `explanation` and `conditions` as the differentiating framework
5. If no direct relationship edge: synthesise comparison from the two concept nodes' definition and distinction_insights fields

**Depth:** 2 hops (concept A → relationship edge → concept B)  
**Traversal edges used:** `contrasts_with`, `often_confused_with`

---

### 4.5 Multi-chain convergence traversal

**Use case:** A question where multiple causal chains converge on the same outcome (common for Distinction-level compound questions).  
**Algorithm:**
1. Identify the outcome concept from query (e.g., `C_ACIDITY` for questions about wine acidity)
2. Retrieve all causal chain nodes that have `C_ACIDITY` in any of their `intermediate_steps[].concept_id` or `final_outcome.concept_id`
3. Filter to chains relevant to the query's starting condition (e.g., "noble rot" → select `CC_BOTRYTIS_ACIDITY_REDUCTION`, not `CC_COOL_CLIMATE_ACIDITY`)
4. If multiple chains are relevant: retrieve both and present as a "two pathways to the same outcome" structure
5. Retrieve relationship edges between the chain starting concepts to check for interactions

**Depth:** 2–3 hops  
**Traversal edges used:** Multiple (varies by query)  
**Use case example:** "How does botrytis affect acidity differently from cool climate?" → converges on `C_ACIDITY` from two distinct starting chains

---

### 4.6 Prerequisite traversal

**Use case:** Student is struggling with a concept because a prerequisite concept is not understood.  
**Algorithm:**
1. Identify the target concept from query
2. Traverse `prerequisite_for` edges in reverse (find what A requires, meaning what must be understood before A)
3. Retrieve prerequisite concept node(s)
4. Check learner model (Phase 8+): has the learner been exposed to the prerequisite?
5. If not: execute foundational pattern for the prerequisite first, then return to target

**Depth:** Variable (may require multiple prerequisite hops)  
**Traversal edges used:** `prerequisite_for` (reverse direction)

---

## 5. Retrieval Fusion: Graph + Vector

### 5.1 Fusion architecture overview

```
Student Query
     │
     ▼
[Query Intent Classifier] ──── classifies to one of 9 retrieval types
     │
     ├─── [Misconception Pre-Pass] ───── if match: forced MC_ node retrieval
     │
     ▼
[Layer 1: Dense Vector Search]
     │  Returns: ranked chunks from vector store (semantic similarity only)
     │
     ▼
[Layer 2: Graph Traversal]
     │  Input: top-N concept candidates from Layer 1
     │  Returns: related misconceptions, causal chains, relationship edges
     │
     ▼
[Layer 3: Result Fusion & Scoring]
     │  Applies composite scoring formula (SEMANTIC_RETRIEVAL_ARCHITECTURE.md §5.2)
     │  Graph-traversal nodes receive +0.10 score bonus
     │
     ▼
[Layer 4: Pedagogical Role Assignment]
     │  Assigns pedagogical role to each retrieved node
     │  Orders nodes by role priority for the current conversation state
     │
     ▼
[Layer 5: Pattern Selection]
     │  Selects Tutor reasoning pattern based on retrieval results + learner level
     │
     ▼
[Response Generation]
```

### 5.2 Graph traversal entry point determination

Graph traversal requires a concept entry point. The entry point is determined as follows:

1. **Exact concept ID match:** If the query explicitly names a concept that maps to a known concept ID (e.g., "tannin" → `C_TANNIN`), use this as the entry point directly.

2. **Dense search concept inference:** If no exact match, use the top-scoring chunk from Layer 1's `concept_id` metadata field (all chunks should carry their associated concept ID at ingestion).

3. **Multi-concept queries:** If the query yields two viable concept entry points, initiate parallel traversals and use the multi-chain convergence algorithm.

4. **No concept match:** If Layer 1 returns no chunk above the minimum threshold, or no chunk with a concept ID, graph traversal is skipped and Layer 1 results are used directly. Flag as `graph_traversal: false` in retrieval log.

### 5.3 Graph bonus score justification

Graph-traversal nodes receive a +0.10 bonus to their composite score compared to equivalent vector-search-only results. The rationale:
- Graph traversal is triggered by a confirmed concept match — the node's relevance is structurally established, not merely semantically inferred
- Graph nodes are schema-validated knowledge graph objects with explicit pedagogical metadata, which raw text chunks lack
- The bonus ensures that a causal chain retrieved via graph traversal is not outranked by a lower-quality chunk that happens to have slightly higher semantic similarity to the query

---

## 6. Semantic Filtering in Graph Traversal

Not all nodes reachable from a graph traversal entry point are relevant to the current query. Semantic filtering prevents retrieval of tangentially related nodes.

### 6.1 Relevance radius

The traversal algorithm limits itself to nodes within a defined "relevance radius" — the number of edge hops from the entry point concept:

| Retrieval type | Maximum hop depth |
|---------------|-------------------|
| Concept (foundational) | 1 |
| Misconception correction | 3 |
| Causal chain | 2 |
| Comparative | 2 |
| Exam strategy | 2 |
| Weakness-targeted | 3 |
| Multi-chain convergence | 3 |

### 6.2 Edge type filtering by retrieval type

Not all edge types are traversed for every retrieval type. Irrelevant edge types introduce noise.

| Retrieval type | Edges traversed | Edges excluded |
|---------------|-----------------|----------------|
| Foundational concept | `is_component_of` only | All causal edges |
| Causal chain | `causes`, `produces`, `increases`, `reduces`, `influences` | `contrasts_with`, `often_confused_with` |
| Comparative | `contrasts_with`, `often_confused_with` | Causal edges |
| Misconception | All (full context needed) | None |
| Tasting | `influences`, `is_indicator_of` | `prerequisite_for`, `is_component_of` |

### 6.3 Node-level semantic filter

After traversal, each retrieved node is checked for semantic relevance to the original query using embedding similarity. Nodes with similarity below 0.40 to the original query are excluded from the result set, even if they are graph-reachable.

---

## 7. Misconception-Aware Graph Tutoring

Misconception-awareness is not a post-processing step — it is embedded in the graph traversal architecture. The knowledge graph is designed specifically to surface potential misconceptions at the moment of concept retrieval, before the agent generates any response.

### 7.1 Misconception linkage in concept nodes

Every concept node's `common_misconceptions[]` array is a direct graph reference to the misconception nodes most frequently triggered in the context of that concept. When a concept is retrieved, its misconception links are automatically traversed and the detection signals are checked against the current student input.

### 7.2 Misconception context window

The misconception pre-pass checks not only the current query but a rolling context window of the last 3–5 student utterances. This catches:
- Misconceptions expressed earlier in the conversation that the current query builds on
- Slow-developing misconceptions that only become apparent through pattern of response
- Implicit misconceptions (correct vocabulary used incorrectly)

### 7.3 Misconception suppression after correction

After a misconception has been corrected and the learner has confirmed the corrected understanding, that misconception node is marked as `resolved` in the session context. It will not be re-triggered by similar subsequent queries in the same session unless new signals suggest the misconception has re-emerged.

---

## 8. Graph-Assisted Distinction-Level Tutoring

The knowledge graph's most pedagogically significant feature is its ability to support Distinction-level explanation with structural precision. This section explains how graph traversal specifically enables the Distinction gap to be closed.

### 8.1 The Pass-Distinction gap in WSET L3

At Pass level, a student needs to know that cool climates produce high-acidity wines. At Distinction level, they need to know: (a) which acid is specifically retained (malic acid), (b) why (slower enzymatic degradation at lower temperatures), (c) which acid is unaffected (tartaric acid), and (d) what sensory and structural implications follow. This is the content of `CC_COOL_CLIMATE_ACIDITY` steps 1–3 and `distinction_note`.

Vector search for "cool climate acidity" will return content about both facts. The graph traversal, triggered from the concept node, will retrieve specifically the causal chain and its distinction_note — the architecture of the Distinction answer is pre-encoded in the graph.

### 8.2 The distinction_note as graph-encoded exam intelligence

Every causal chain node's `distinction_note` field encodes the specific delta between Merit and Distinction. It names the specific compounds, conditions, and mechanism details that markers look for. The graph retrieval strategy specifically surfaces this field when the retrieval type is `exam_strategy` or `distinction_training`, making the Distinction-level content proactively accessible rather than buried in general retrieval results.

### 8.3 Multi-chain synthesis for advanced questions

The most challenging WSET L3 questions require synthesising multiple causal chains (e.g., "how does botrytis affect the final style of Sauternes?"). This requires retrieving and sequencing `CC_NOBLE_ROT_SUGAR_CONCENTRATION` (4 steps) and `CC_BOTRYTIS_ACIDITY_REDUCTION` (3 steps) in the correct logical order, with the paradox (concentration increases everything except acidity, which is partially reduced) explicitly flagged.

The multi-chain convergence traversal algorithm in §4.5 is designed precisely for this use case. Without graph traversal, vector search would return fragments from both chains in order of semantic similarity to the query — potentially presenting the result before the mechanism, or mixing steps from both chains incoherently.

---

## 9. Phase Roadmap for Graph Expansion

| Phase | Graph expansion |
|-------|----------------|
| Phase 1 (current) | 8 concepts, 17 chains, 13 misconceptions, 10 relationships (RA1 + RA3 partial) |
| Phase 2 | Topic nodes for all RA1; RA1 concept coverage complete |
| Phase 3 | RA2 regional concepts; region → climate → style chains |
| Phase 4 | RA3 complete (sparkling production methods, regional styles) |
| Phase 5 | RA4 fortified wines (Port, Sherry, Madeira, Muscat) |
| Phase 6 | RA5 laws and commerce |
| Phase 7 | Sensory-structural inference chains (SAT ↔ structural component graph) |
| Phase 8 | Learner model integration (learner state as graph overlay on knowledge graph) |
| Phase 9 | Adaptive difficulty paths through graph (curated traversal sequences per learner level) |

---

## 10. Graph Integrity Requirements

For the graph traversal strategy to function correctly, the following integrity properties must be maintained:

**10.1 No orphan nodes:** Every concept node must be connected to at least one causal chain and one relationship edge. Isolated concept nodes cannot contribute to multi-hop retrieval.

**10.2 No dangling references:** Every cross-reference (misconception IDs in concept nodes, chain IDs in concept nodes, concept IDs in chain steps) must resolve to an existing node file. Validated by L2 cross-reference check.

**10.3 Bidirectional accessibility:** All `contrasts_with` and `often_confused_with` relationships must be navigable in both directions. If A contrasts_with B, a query for B must be able to surface the comparison with A.

**10.4 Chain step completeness:** Every causal chain must have at least 2 intermediate steps. A chain with only a starting factor and final outcome with no steps is not graph-traversable in the mechanistic sense — it degenerates to a fact pair.

---

*This document defines the architectural principles for GraphRAG implementation in the WSET-AI-System. Specific implementation technology (graph database, embedding model, vector store) is to be determined in the implementation phase and documented separately.*

# Graph Reasoning and Pathfinding
## WSET-AI-System — Cognitive Architecture Design Series

**Author:** Claude (Cowork) — Cognitive Architecture Designer Role
**Date:** 2026-05-15
**Series position:** 5 of 8 — Extends the knowledge graph from retrieval enrichment to Orchestrator pathfinding substrate
**Status:** Design specification — requires engineering implementation

---

## The Graph's Current Role vs. Its Potential Role

The knowledge graph currently serves retrieval enrichment. When a student asks about cool climate and acidity, the retrieval system matches the query against known concept nodes, finds `C_COOL_CLIMATE` and `C_ACIDITY`, activates the associated causal chains, applies a graph boost to related chunks, and returns richer results than lexical matching alone would produce.

This is a real contribution to retrieval quality. But it is only a fraction of what a well-designed knowledge graph can do for an educational reasoning system.

The graph's richer potential is as a **pathfinding substrate** for the Orchestrator. Not "what content is related to this query" but "what is the optimal pedagogical path from what Nazareth currently understands to what Nazareth needs to understand, and in what order should the steps be traversed?"

This is a different question, and it requires different traversal logic.

---

## The Three Roles of the Graph

### Role 1 — Retrieval Enrichment (currently active)

The graph is queried at retrieval time. When a concept node matches a query, its associated causal chains and related concepts are used to expand the retrieval result. The chunk pool for the LLM is larger and better-targeted than it would be from lexical matching alone.

This role is working for RA1 foundational concepts. It is absent for RA2–RA5 because those concept nodes do not yet exist.

### Role 2 — Pedagogical Pathfinding (to be built)

The graph is queried by the Orchestrator at session planning time. The Orchestrator traverses prerequisite edges to determine what the student must understand before a target concept can be taught correctly.

**Example:**

Orchestrator goal: teach Nazareth to explain why Champagne is characterised by high acidity and autolytic character.

Graph traversal from `T_CHAMPAGNE`:
```
T_CHAMPAGNE
  → prerequisite_for: C_COOL_CLIMATE (Champagne is one of the northernmost French AOCs)
  → prerequisite_for: C_TRADITIONAL_METHOD (must understand traditional method to understand autolysis)
  → C_TRADITIONAL_METHOD
      → prerequisite_for: C_SECOND_FERMENTATION
      → prerequisite_for: C_LEES_AGEING
      → C_LEES_AGEING
          → prerequisite_for: C_AUTOLYSIS
          → CC_LEES_AGEING_AUTOLYTIC_CHARACTER (causal chain)
```

LES check against each node:
- `C_COOL_CLIMATE`: belief_state = `correct_with_mechanism` ✅ — prerequisite met
- `C_TRADITIONAL_METHOD`: belief_state = `partially_correct` ⚠️ — prerequisite partially met
- `C_SECOND_FERMENTATION`: belief_state = `absent` ❌ — prerequisite not met
- `C_LEES_AGEING`: belief_state = `fragmented` ❌ — prerequisite not met
- `C_AUTOLYSIS`: belief_state = `absent` ❌ — target concept unavailable

The graph traversal + LES check produces a **teaching path**: the Orchestrator cannot teach Champagne autolytic character to Nazareth today because the prerequisite chain has gaps. The path must first visit: second fermentation → lees ageing → autolytic character development → then Champagne regional application.

Without graph pathfinding, the Orchestrator might attempt to teach Champagne character directly, producing an explanation that floats above the learner's actual understanding — comprehensible in words but not grounded in mechanism.

### Role 3 — Gap Detection (to be built)

The graph can map the complete WSET L3 concept space and compare it against Nazareth's LES belief states to produce a comprehensive gap map.

```
ALL_L3_CONCEPTS (from graph)
  → filtered by belief_state in [absent, fragmented]
  → weighted by exam_relevance
  → produces: PRIORITY_GAP_LIST
```

This gap list is the Orchestrator's long-term curriculum. It answers: "If Nazareth needs to cover everything relevant to the WSET L3 exam before 2026-08-08, what is missing and what are we working from?"

The gap list is not a reading list. It is a traversal plan — the graph's edges define the order in which gaps should be addressed (prerequisites first, targets after).

---

## Graph Traversal Logic

### Forward Traversal — Prerequisite Check

Used before teaching a new concept. Traversal direction: from the target node backward through `prerequisite_for` edges to find all prerequisites.

```
function get_teaching_prerequisites(target_concept_id):
  prerequisites = []
  queue = [target_concept_id]
  visited = {target_concept_id}
  
  while queue not empty:
    current = queue.pop()
    for each edge in graph.edges_from(current) where edge.type == "prerequisite_for":
      if edge.source not in visited:
        prerequisites.append(edge.source)
        visited.add(edge.source)
        queue.append(edge.source)
  
  return prerequisites
```

Each prerequisite is then checked against the LES:
- If `belief_state` in [`correct_with_mechanism`, `distinction_level`] → prerequisite met ✅
- If `belief_state` in [`correct_but_shallow`, `partially_correct`] → prerequisite partially met ⚠️ — include in path as a brief reinforcement step before proceeding to target
- If `belief_state` in [`fragmented`, `absent`] → prerequisite not met ❌ — must be taught first; add to path before target

The output is an **ordered teaching path** from prerequisite leaf nodes to the target concept.

### Lateral Traversal — Comparison and Contrast

Used when the Orchestrator wants to teach through comparison. Traversal direction: from a known concept through `contrasts_with` or `often_confused_with` edges.

```
C_WARM_CLIMATE → contrasts_with → C_COOL_CLIMATE
C_MLF → contrasts_with → C_NON_MLF_WINEMAKING
C_TANNIN_GRAPE_DERIVED → contrasts_with → C_TANNIN_OAK_DERIVED
```

When Nazareth understands `C_COOL_CLIMATE` well (`correct_with_mechanism`) but `C_WARM_CLIMATE` is `partially_correct`, the Orchestrator can use lateral traversal to teach warm climate through contrast with the already-understood cool climate concept. This is more efficient than teaching warm climate from scratch.

### Causal Chain Traversal — Explanation Sequencing

Used when the Tutor Agent must render a structured explanation. The graph retrieves the full causal chain node and orders the explanation steps explicitly.

```
CC_COOL_CLIMATE_ACIDITY:
  steps: [
    {step: 1, content: "Cool temperatures during ripening"},
    {step: 2, content: "Malic acid, which degrades in warmth, is retained"},
    {step: 3, content: "High total acidity, lower pH"},
    {step: 4, content: "Freshness, ageability, food pairing potential"},
    {step: 5, content: "Exam formulation: 'high acidity, fresh style, ageing potential'"}
  ],
  distinction_note: "Distinguish malic from tartaric retention. Name the acids. Give a regional example (Loire Chenin Blanc, Mosel Riesling)."
```

The Tutor renders this step sequence explicitly rather than synthesising freely from retrieved text. The distinction note is appended for Distinction-level teaching.

### Misconception Traversal — Correction Pathfinding

When the LES shows an active misconception, the Orchestrator uses the misconception node to find the correct belief and the correction path.

```
MC_ACIDITY_QUALITY:
  linked_concept: C_ACIDITY
  corrected_understanding: "Acidity is a structural component supporting freshness, food pairing, and ageability. High acidity is associated with quality in many great wine styles."
  intervention_type: causal_chain_walkthrough
  correction_chain: CC_ACIDITY_FRESHNESS_AGEABILITY
  example_concepts: [T_MOSEL_RIESLING, T_CHABLIS, T_LOIRE_SANCERRE]
```

The Orchestrator traverses from the misconception node to its correction chain and retrieves the example concepts as concrete counter-evidence. This structures the intervention as: "Let's look at three wines that have high acidity and are considered outstanding quality..."

---

## Graph Population Priority for Pathfinding

For pathfinding to be useful, the graph needs to be populated beyond RA1. The priority for graph expansion, from a pathfinding perspective:

**Priority 1 — Prerequisite backbone for RA2 regions:**
The 8 major WSET L3 regions (Bordeaux, Burgundy, Rhône, Loire, Champagne, Germany, Italy, Spain) each need a region node with their key prerequisite edges. A student cannot understand Bordeaux appellations without understanding the Médoc/Right Bank distinction; cannot understand Germany without understanding the Prädikat system.

**Priority 2 — Causal chains for production methods (RA3, RA4):**
Traditional method, tank method, transfer method for sparkling. Fortification process, oxidative vs. reductive ageing for fortified. These production methods have strong causal chain structures and are high-value exam topics.

**Priority 3 — Cross-concept relationship edges:**
The `contrasts_with`, `often_confused_with`, and `is_component_of` edges between existing concept nodes. These enable lateral traversal and comparison-based teaching without requiring new concept nodes.

**Priority 4 — Topic nodes for RA5 (wine law):**
Wine law is highly lexical — appellations, classification systems, legal requirements. Prerequisite edges here are lighter (wine law is often terminal — students must simply learn it, with fewer causal mechanisms to understand). But `often_confused_with` edges between similar classification systems (French AOC vs. Italian DOC vs. Spanish DO) would support comparison teaching.

---

## The Concept Coverage Map

The graph, when fully populated, becomes a **coverage map** of the WSET L3 curriculum. Every node is either:
- ✅ `covered` — In the LES with `belief_state` in [`correct_with_mechanism`, `distinction_level`]
- ⚠️ `partial` — In the LES with `belief_state` in [`correct_but_shallow`, `partially_correct`]
- ❌ `absent` — Not in the LES or `belief_state: absent`

The Orchestrator can render this coverage map at any time and ask: "With 85 days to the exam, which absent concepts are highest priority given their exam relevance weight and prerequisite depth?"

This turns the graph from a retrieval enrichment tool into a **curriculum planner** — an executable model of what remains to be learned before the exam.

---

## What Pathfinding Requires vs. What Exists

| Required | Current Status |
|---|---|
| Concept nodes for RA1 | ✅ ~8 concepts built |
| Prerequisite edges for RA1 | ⚠️ Some exist; sparse |
| Concept nodes for RA2–RA5 | ❌ Not built |
| Prerequisite edges for RA2–RA5 | ❌ Not built |
| Causal chain nodes for all RAs | ⚠️ RA1 only |
| Contrasts_with and often_confused_with edges | ❌ Largely not populated |
| Misconception correction chains | ⚠️ RA1 misconceptions defined; connections to examples sparse |
| Orchestrator traversal function | ❌ Not implemented |
| LES-graph intersection function | ❌ Not implemented |

The gap is significant but addressable. The schema is correct. The node architecture is correct. The traversal logic described in this document can be implemented against the existing graph structure. The bottleneck is graph population (adding RA2–RA5 nodes and edges) and Orchestrator integration (calling traversal functions at session planning time).

---

*Generated: 2026-05-15 | Cognitive Architecture Design Series | Document 5 of 8*
*Not an official WSET document. Not for learner-facing use.*

# WSET-AI-System — Knowledge Graph Architecture

**Version:** 1.0  
**Date:** 2026-05-13  
**Status:** Draft — for internal review  
**Author:** AI System Design (WSET-AI-System project)  
**Audience:** System architects, content editors, agent developers

---

## 1. Purpose

This document describes the semantic architecture of the WSET-AI-System knowledge graph: the node types, edge types, schema design decisions, traversal patterns, and how the Tutor Agent uses the graph to generate pedagogically effective responses.

The knowledge graph is the epistemological core of the system. It is not a question bank — that lives in `knowledge/question-bank/`. The knowledge graph is a structured representation of *how concepts relate to each other* and *why those relationships matter for exam performance*. Its primary purpose is to enable the Tutor Agent to reason causally rather than retrieve facts.

---

## 2. Design Principles

**2.1 Causal reasoning over factual retrieval**

The defining characteristic of WSET Level 3 Distinction-level answers is the ability to explain mechanisms, not just correlations. A Pass-level answer states "cool climate wines have high acidity." A Distinction-level answer explains the malic acid degradation mechanism, distinguishes it from tartaric acid's behaviour, and names the specific climatic condition that drives it.

The knowledge graph is designed to encode this mechanistic, causal knowledge in a form that the Tutor Agent can traverse and communicate step by step. Every causal chain node is a walkable explanation at Distinction level.

**2.2 Misconceptions as first-class objects**

Student misconceptions are not edge cases to be handled with exceptions — they are anticipated failure modes that must be modelled explicitly. The knowledge graph includes a dedicated misconception node type with detection signals (phrases that indicate a student holds the misconception) and intervention types that specify the appropriate pedagogical response.

**2.3 Additive-only content policy**

The knowledge graph is built additively. No file is ever deleted or overwritten without an explicit audit trail. This ensures that content accumulated through expert review is never accidentally lost during system iteration.

**2.4 Separation from scoring authority**

The knowledge graph is exclusively a Tutor Agent resource. It contains pedagogical content (Tiers 0–4 of the data trust model). It does NOT contain official WSET marking schemes, examiner guidance, or calibration data. Those materials belong to the Examiner Agent's corpus (Tiers 0–1 only) and are governed by the calibration gate described in AGENT_BOUNDARIES.md.

**2.5 Schema-driven integrity**

All knowledge graph nodes are validated against JSON Schema draft-07 definitions in `knowledge/knowledge-map/manifests/schemas/`. No file is considered production-ready until it passes schema validation. Draft files carry `"ingestion_status": "draft"` in their `_meta` block.

---

## 3. Node Types

The knowledge graph contains five node types. Each type has a dedicated JSON Schema and a naming convention for its ID.

### 3.1 Topics (`T_`)

**File location:** `knowledge/knowledge-map/topics/`  
**Schema:** `manifests/schemas/topic.schema.json`  
**ID pattern:** `T_RA[1–5]_[UPPERCASE_SLUG]`

Topics are the top-level organisational units, corresponding to sections of the WSET Level 3 curriculum. They map directly to the five Result Areas (RA1–RA5):

| Prefix | Result Area | Scope |
|--------|-------------|-------|
| `T_RA1_` | Viticulture and winemaking | Climate, grape growing, winemaking processes, wine components, service |
| `T_RA2_` | Still wines of the world | Major wine regions, appellations, grape varieties, regional styles |
| `T_RA3_` | Sparkling wines | Champagne, Prosecco, Cava, traditional method, tank method |
| `T_RA4_` | Fortified wines | Port, Sherry, Madeira, Muscat |
| `T_RA5_` | Wine laws and commerce | Label reading, appellation systems, trade and business |

Topics form a hierarchy: a root topic (e.g., `T_RA1_CLIMATE_VITICULTURE`) may have child topics (e.g., `T_RA1_COOL_CLIMATE`, `T_RA1_WARM_CLIMATE`) and related topics across the graph. Topic nodes carry lists of their official and pedagogical source references.

### 3.2 Concepts (`C_`)

**File location:** `knowledge/knowledge-map/concepts/`  
**Schema:** `manifests/schemas/concept.schema.json`  
**ID pattern:** `C_[UPPERCASE_SLUG]`

Concepts are the primary knowledge nodes. They represent the key phenomena, components, processes, and principles that WSET Level 3 students must understand. Each concept contains:

- A **definition** (exam-accurate, concise)
- A list of **common misconceptions** (references to `MC_` nodes)
- **Distinction insights** (the deeper mechanistic understanding that separates Pass from Distinction answers)
- **Cause-effect links** (references to `CC_` chain nodes that start or involve this concept)
- Related grapes, regions, and wine laws (for cross-referencing in regional content)
- An **official reference** (linking to the authoritative WSET source)
- Permission flags: `tutor_allowed` (default `true`) and `examiner_allowed` (default `false`)

Concepts are the nodes most frequently retrieved by the Tutor Agent when answering student questions. The Agent follows cause-effect links from a concept to find the relevant causal chain for a Distinction-level explanation.

### 3.3 Relationships (`R_`)

**File location:** `knowledge/knowledge-map/relationships/`  
**Schema:** `manifests/schemas/relationship.schema.json`  
**ID pattern:** `R_[SOURCE]__[RELATIONSHIP_TYPE]__[TARGET]`

Relationships are directed edges between concept nodes. They encode the structure of the knowledge graph in a queryable form. A relationship node specifies:

- **Source and target concepts** (concept IDs)
- **Relationship type** (from a controlled vocabulary of 15 types)
- **Strength** (weak / moderate / strong)
- **Conditions** (the circumstances under which the relationship holds — critical for avoiding overgeneralisation)
- **Direction** (human-readable arrow notation)
- **Explanation** (the mechanism behind the relationship)

**Relationship types (controlled vocabulary):**

| Type | Meaning | Example |
|------|---------|---------|
| `causes` | A directly produces B | cool_climate causes high malic acid retention |
| `influences` | A affects B without fully determining B | acidity influences tannin perception |
| `increases` | A raises the level of B | cool_climate increases acidity |
| `decreases` | A lowers the level of B | warm_climate decreases acidity |
| `requires` | A cannot occur without B | noble_rot requires alternating mist/sun |
| `contrasts_with` | A and B are often confused but distinct | noble_rot contrasts_with grey_rot |
| `often_confused_with` | A is commonly mistaken for B | cool_climate often_confused_with under_ripeness |
| `prerequisite_for` | A must be understood before B | acidity is prerequisite_for MLF |
| `improves` | A enhances B | lees_ageing improves bubble quality |
| `reduces` | A diminishes B | MLF reduces acidity |
| `accompanies` | A and B typically co-occur | tannin accompanies colour in red wine |
| `inhibits` | A prevents or slows B | low_temperature inhibits MLF |
| `produces` | A generates B as output | autolysis produces mannoproteins |
| `is_component_of` | A is a part of B | tartaric_acid is_component_of total_acidity |
| `is_indicator_of` | A signals the presence of B | gluconic_acid is_indicator_of botrytis_infection |

### 3.4 Misconceptions (`MC_`)

**File location:** `knowledge/knowledge-map/misconceptions/`  
**Schema:** `manifests/schemas/misconception.schema.json`  
**ID pattern:** `MC_[CONCEPT_SLUG]_[NN]` (two-digit sequential number per concept)

Misconception nodes represent documented student errors. They contain:

- The **misconception** statement (what the student incorrectly believes)
- **Why incorrect** (the precise technical explanation of the error)
- **Corrected understanding** (the accurate replacement belief)
- **Detection signals** (verbatim phrases or paraphrases that indicate the student holds this misconception — used by the Tutor Agent for pattern matching)
- **Severity** (how damaging this belief is to exam performance: low / medium / high / critical)
- **Frequency** (how often this error is observed: rare / occasional / common / very_common)
- **Distinction relevance** (whether correcting this misconception is necessary for Distinction, or sufficient for Pass)
- **Tutor intervention type** (the recommended pedagogical strategy)

**Intervention types:**

| Type | When to use | Description |
|------|------------|-------------|
| `direct_correction` | Low-severity factual errors | State the correct fact clearly without extended reasoning |
| `causal_chain_walkthrough` | Mechanistic misunderstandings | Walk the student through the causal chain step by step |
| `contrast_comparison` | Conflation of two distinct concepts | Present both concepts side by side and highlight the distinguishing features |
| `worked_example` | Abstract misconceptions | Demonstrate with a concrete regional or wine example |
| `socratic_questioning` | Deeply held incorrect beliefs | Use questions to guide the student to discover the error themselves |

### 3.5 Causal Chains (`CC_`)

**File location:** `knowledge/knowledge-map/causal-chains/`  
**Schema:** `manifests/schemas/causal_chain.schema.json`  
**ID pattern:** `CC_[UPPERCASE_SLUG]`

Causal chains are ordered sequences of cause-effect steps encoding a complete mechanistic explanation. They are the primary Distinction-level content objects in the knowledge graph. Each chain contains:

- A **starting factor** (the initiating concept)
- **Intermediate steps** (ordered array, each with a step number, concept ID, description of what happens at that step, and the relationship type connecting it to the next step)
- A **final outcome** (the end state of the chain)
- **Real examples** (at least one specific wine or region illustrating the chain in practice)
- **Related exam questions** (verbatim or paraphrased questions from WSET L3 exam style)
- A **distinction note** (what specifically a student must include to achieve Distinction — not just Pass)

Causal chains are the pedagogical engines of the Tutor Agent. When a student asks "why does cool climate produce high-acidity wines?", the agent does not answer with a generic statement — it retrieves `CC_COOL_CLIMATE_ACIDITY` and walks the student through the three steps of the chain, then checks comprehension.

---

## 4. Graph Topology

### 4.1 Node count (as at build date)

| Node type | Count | Location |
|-----------|-------|----------|
| Topics | pending creation | `topics/` |
| Concepts | 8 | `concepts/` |
| Relationships | 10 | `relationships/` |
| Misconceptions | 13 | `misconceptions/` |
| Causal Chains | 17 | `causal-chains/` |
| **Total** | **48** | |

### 4.2 Coverage

Initial coverage focuses on RA1 foundational concepts (wine components, climate, winemaking processes) and two RA3 concepts (Champagne lees ageing). Coverage will be extended to RA2 (regional wine styles), RA4 (fortified wines), and RA5 (laws and commerce) in subsequent build phases.

### 4.3 Cross-concept density

Each concept is connected to at least:
- 2 misconception nodes
- 2 causal chain nodes (as starting factor or intermediate step)
- 1 relationship edge to at least one other concept

Higher-connectivity concepts (C_ACIDITY, C_TANNIN, C_BOTRYTIS_CINEREA) participate in 4–6 causal chains each, reflecting their central importance to WSET L3 exam performance.

---

## 5. Traversal Patterns

The Tutor Agent uses three primary traversal patterns when reasoning over the knowledge graph:

### 5.1 Direct concept lookup

**Trigger:** Student asks a definitional question ("What is tannin?")  
**Pattern:** Retrieve concept node by ID → return `definition` field → optionally add `distinction_insights` if context indicates student is at advanced level.

### 5.2 Misconception detection and correction

**Trigger:** Student statement matches one or more `detection_signals` in a misconception node  
**Pattern:** Identify misconception node → read `why_incorrect` and `corrected_understanding` → apply `tutor_intervention` strategy → follow up by retrieving the relevant causal chain for depth.

**Example:** Student says "after MLF the wine will have no acidity" → matches `MC_MLF_02` detection signals → apply `causal_chain_walkthrough` intervention → retrieve `CC_MLF_ACIDITY` → walk through three steps.

### 5.3 Causal chain explanation

**Trigger:** Student asks a "why" or "how" question, or is preparing for a Distinction-level written question  
**Pattern:** Identify the relevant chain by starting factor or topic → retrieve full chain → present steps sequentially, pausing to confirm understanding at each step → present the `distinction_note` → present `examples` → ask student to summarise.

**Example:** Student asks "how does botrytis affect acidity in Sauternes?" → Agent identifies `CC_BOTRYTIS_ACIDITY_REDUCTION` and `CC_NOBLE_ROT_SUGAR_CONCENTRATION` → presents both chains in order → highlights the paradox of concentration + acidity reduction.

### 5.4 Relationship traversal

**Trigger:** Student asks about the connection between two concepts  
**Pattern:** Retrieve relationship edge(s) between source and target concepts → read `explanation` and `conditions` → present the relationship with its conditional qualifiers (avoiding overgeneralisation).

**Example:** Student asks "does oak increase tannin?" → retrieve `R_OAK_INFLUENCE__INCREASES__TANNIN` → present explanation including the new-vs-old oak condition, barrel size, and toast level as modifying variables.

---

## 6. Tutor Agent Integration Guidelines

**6.1 Priority hierarchy**

When multiple retrieval results are available for a student query, the agent should prioritise in this order:
1. Misconception nodes (correct the error before providing the positive explanation)
2. Causal chains (provide mechanistic depth)
3. Relationship edges (clarify connections)
4. Concept definitions (provide foundational facts)

**6.2 Distinction escalation**

The Tutor Agent should assess student level from context (prior answers, question complexity) and calibrate response depth accordingly:
- **Pass-level student:** Present the definition and the first 1–2 steps of the relevant causal chain.
- **Merit-level student:** Present the full causal chain and one example.
- **Distinction-seeking student:** Present the full causal chain, the distinction note, multiple examples, and the related exam questions as practice prompts.

**6.3 Condition awareness**

Every relationship and causal chain node includes `conditions` and `distinction_note` fields specifically because WSET examiners reward nuanced, conditional answers. The Tutor Agent must include the conditions when presenting relationships — never present a relationship as unconditional unless the schema explicitly marks it as `strength: "strong"` with no conditions.

**6.4 Forbidden operations**

The Tutor Agent must not:
- Represent knowledge graph content as WSET official marking guidance
- Use knowledge graph content to simulate official exam marking or grade student answers
- Include knowledge graph nodes in the Examiner Agent's retrieval corpus
- Present `distinction_notes` as absolute rules rather than as heuristics for depth

These restrictions are fully specified in `docs/AGENT_BOUNDARIES.md`.

---

## 7. Schema Design Decisions

### 7.1 Why separate files per node?

Each concept, relationship, misconception, and causal chain lives in its own JSON file. This design enables:
- Fine-grained version control (git diff per node)
- Incremental ingestion (add or update one node without risking schema errors in others)
- Human review of individual nodes without loading the full graph
- Clear file ownership for the calibration gate review process

### 7.2 Why JSON Schema over a graph database?

At the current project scale, a graph database (Neo4j, etc.) would add infrastructure complexity without proportionate benefit. JSON files with cross-references (concept IDs in causal chain steps, etc.) provide sufficient graph structure for RAG retrieval and can be loaded into a graph database later if query complexity demands it.

### 7.3 Why `additionalProperties: false`?

All schemas use `"additionalProperties": false` to enforce strict field validation. This prevents schema drift — a common failure mode in AI content pipelines where fields are added informally and accumulate without documentation. Any new field requires a schema update, ensuring all content editors follow the same structure.

### 7.4 Why `tutor_use` and `examiner_use` flags at the node level?

These flags enable fine-grained corpus control. A concept or chain that is appropriate for the Tutor Agent (pedagogical, explanatory, with examples) may not be appropriate for the Examiner Agent (which must use only officially validated WSET materials). The flags allow selective ingestion into agent-specific vector stores without manual curation at query time.

---

## 8. Extension Roadmap

| Phase | Planned additions |
|-------|------------------|
| Phase 2 | Topic nodes (T_RA1_* through T_RA5_*) — all RA1 foundational topics |
| Phase 3 | RA2 concept nodes — major regions, grape varieties, regional styles |
| Phase 4 | RA3 complete — all sparkling wine production methods and styles |
| Phase 5 | RA4 fortified wines — Port, Sherry, Madeira, Muscat |
| Phase 6 | RA5 laws, labelling, and commerce |
| Phase 7 | SAT (Systematic Approach to Tasting) integration — sensory → structural inference chains |
| Phase 8 | Spaced repetition optimisation — difficulty ratings calibrated against question bank performance data |

---

## 9. Validation

All knowledge graph files must pass schema validation before being promoted from `"ingestion_status": "draft"` to `"ingestion_status": "validated"`. Validation rules are documented in `docs/KNOWLEDGE_MAP_VALIDATION_RULES.md`.

The minimum requirements for promotion to `"validated"`:
1. JSON parses without errors
2. All required fields present and of correct type (schema validation)
3. All cross-referenced concept IDs resolve to existing concept files
4. All misconception and causal chain IDs cross-referenced from concept files exist
5. Human WSET-qualified reviewer confirms factual accuracy
6. `distinction_note` reviewed against WSET L3 mark scheme (where available)

---

*This document is internal to the WSET-AI-System project. It does not contain official WSET assessment guidance and must not be represented as such to learners or examiners.*

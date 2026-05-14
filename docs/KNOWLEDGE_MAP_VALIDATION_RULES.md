# WSET-AI-System — Knowledge Map Validation Rules

**Version:** 1.0  
**Date:** 2026-05-13  
**Status:** Draft  
**Audience:** Content editors, system validators, CI/CD pipeline authors

---

## 1. Purpose

This document defines the validation rules that must be satisfied before any knowledge graph node is promoted from `"ingestion_status": "draft"` to `"ingestion_status": "validated"`. It covers structural rules (enforced by JSON Schema), cross-reference integrity rules, factual accuracy requirements, and the human review checklist.

---

## 2. Validation Levels

Validation is performed in four sequential levels. A node must pass each level before proceeding to the next.

| Level | Name | Who performs | Tool |
|-------|------|-------------|------|
| L1 | Structural (JSON) | Automated | `jsonschema` or equivalent |
| L2 | Cross-reference integrity | Automated | Custom validation script |
| L3 | Pedagogical quality | Content editor (human) | Manual review checklist |
| L4 | Factual accuracy | WSET-qualified reviewer (human) | WSET L3 textbook and course materials |

Only nodes that have passed L4 are eligible for use in production agent deployments. Nodes at L1–L3 may be used in development and testing environments with appropriate disclaimers.

---

## 3. L1 — Structural Validation Rules

### 3.1 JSON Syntax

- All files must be valid JSON (RFC 8259)
- No trailing commas, no comments, no non-standard extensions
- UTF-8 encoding required
- Maximum file size: 64KB per node file

### 3.2 Schema Compliance

Each node type must comply with its corresponding JSON Schema:

| Node type | Schema file |
|-----------|-------------|
| Topic | `manifests/schemas/topic.schema.json` |
| Concept | `manifests/schemas/concept.schema.json` |
| Relationship | `manifests/schemas/relationship.schema.json` |
| Misconception | `manifests/schemas/misconception.schema.json` |
| Causal Chain | `manifests/schemas/causal_chain.schema.json` |

All schemas use `"additionalProperties": false`. Any unknown field will cause L1 failure.

### 3.3 Required ID Format Rules

| Node type | Pattern | Failing examples |
|-----------|---------|-----------------|
| Topic | `T_RA[1-5]_[A-Z0-9_]+` | `T_ra1_climate`, `TOPIC_CLIMATE`, `RA1_CLIMATE` |
| Concept | `C_[A-Z0-9_]+` | `c_tannin`, `CONCEPT_TANNIN`, `Tannin` |
| Relationship | `R_[A-Z0-9_]+__[A-Z_]+__[A-Z0-9_]+` | `R_cool_increases_acid`, `R_COOL__INCREASES` |
| Misconception | `MC_[A-Z0-9_]+_[0-9]{2}` | `MC_MLF_1`, `MISC_MLF_01`, `mc_mlf_01` |
| Causal Chain | `CC_[A-Z0-9_]+` | `cc_cool_climate`, `CHAIN_COOL_CLIMATE` |

**Rule:** All IDs are UPPERCASE only. Lowercase IDs fail L1.

### 3.4 Required `_meta` Fields

Every node file must contain a `_meta` object with:
- `schema_version`: string, must be `"1.0"` (or the current schema version)
- `created_date`: string, ISO 8601 format (YYYY-MM-DD)
- `ingestion_status`: string, one of: `"draft"`, `"validated"`, `"deprecated"`

### 3.5 Enum Field Constraints

The following fields must contain only values from their defined enumerations:

**Concept nodes:**
- `difficulty`: `"foundational"` | `"intermediate"` | `"advanced"` | `"distinction_only"`

**Relationship nodes:**
- `relationship_type`: one of 15 defined types (see KNOWLEDGE_GRAPH_ARCHITECTURE.md §3.3)
- `strength`: `"weak"` | `"moderate"` | `"strong"`

**Misconception nodes:**
- `severity`: `"low"` | `"medium"` | `"high"` | `"critical"`
- `frequency`: `"rare"` | `"occasional"` | `"common"` | `"very_common"`
- `tutor_intervention`: `"direct_correction"` | `"causal_chain_walkthrough"` | `"contrast_comparison"` | `"worked_example"` | `"socratic_questioning"`

**Causal Chain nodes:**
- `complexity`: `"simple"` | `"moderate"` | `"complex"`
- `exam_relevance`: `"low"` | `"moderate"` | `"high"` | `"critical"`

---

## 4. L2 — Cross-Reference Integrity Rules

### 4.1 Concept cross-references in other nodes

Every concept ID referenced in any node must correspond to an existing concept file. This applies to:

- `concept_id` fields in causal chain step arrays
- `related_concepts[]` in misconception nodes
- `source_concept` and `target_concept` in relationship nodes
- `cause_effect_links[]` in concept nodes
- `common_misconceptions[]` in concept nodes (must reference existing MC_ files)

**Rule:** No dangling concept references. A concept ID that appears in a cross-reference but has no corresponding file fails L2.

### 4.2 Misconception cross-references

Every misconception ID referenced in a concept node's `common_misconceptions[]` array must correspond to an existing misconception file in `knowledge/knowledge-map/misconceptions/`.

### 4.3 Causal chain cross-references

Every causal chain ID referenced in a concept node's `cause_effect_links[]` array must correspond to an existing causal chain file in `knowledge/knowledge-map/causal-chains/`.

### 4.4 Topic cross-references

Every topic ID referenced in a concept node's `topic_id` field must either:
- Correspond to an existing topic file in `knowledge/knowledge-map/topics/`, OR
- Be present in the manifest's `pending_nodes.topics` list (indicating it is planned but not yet created)

**Rule during Phase 1:** Topic cross-references to `T_RA[1-5]_*` IDs are exempt from L2 cross-reference checking until Phase 2 (topic node creation). This exemption must be removed after Phase 2 is complete.

### 4.5 Duplicate ID detection

- No two concept files may share the same `concept_id`
- No two misconception files may share the same `misconception_id`
- No two causal chain files may share the same `chain_id`
- No two relationship files may share the same `relationship_id`

**Rule:** Duplicate IDs within a node type fail L2.

### 4.6 Self-referencing relationship validation

Some relationships have the same concept as both source and target (e.g., `CC` chains where a concept evolves through itself, or `contrasts_with` relationships that reference the same concept on both sides). These are valid but must be explicitly documented in the `explanation` field to clarify the self-referential logic.

---

## 5. L3 — Pedagogical Quality Rules

L3 is a human review step performed by a content editor who is familiar with WSET L3 curriculum structure but is not required to be a WSET-qualified examiner.

### 5.1 Concept nodes

| Check | Criterion |
|-------|-----------|
| Definition length | 1–3 sentences; concise and exam-accurate |
| Distinction insights | At least 2 insights that go beyond the basic definition |
| Misconceptions coverage | At least 1 misconception documented for every concept |
| Cause-effect links | At least 1 causal chain referenced |
| Examples | At least 1 wine or region example in `related_regions` or referenced chains |

### 5.2 Misconception nodes

| Check | Criterion |
|-------|-----------|
| Detection signals | At least 2 verbatim or near-verbatim phrases that a student would actually say |
| Corrected understanding | Materially different from the misconception; not just negation of it |
| Why incorrect | Explains the mechanism, not just states the misconception is wrong |
| Intervention appropriateness | Intervention type is appropriate for the severity (e.g., `direct_correction` should not be used for complex mechanistic misunderstandings) |

### 5.3 Causal chain nodes

| Check | Criterion |
|-------|-----------|
| Step ordering | Steps are in logical causal sequence; no circular logic |
| Step completeness | Each step explains what happens at that point; not merely restates the previous step |
| Distinction note specificity | Names specific compounds, conditions, or mechanisms — not vague generalities |
| Examples | At least 1 specific wine/region example with a factual description |
| Related exam questions | At least 2 questions in WSET exam style ("Explain...", "Describe...", "Why...") |

### 5.4 Relationship nodes

| Check | Criterion |
|-------|-----------|
| Conditions field | Present and specifies when the relationship holds and when it does not |
| Explanation | Explains the mechanism, not just restates the relationship type |
| Direction notation | Human-readable arrow notation consistent with source → target direction |

---

## 6. L4 — Factual Accuracy Rules

L4 is performed by a WSET-qualified reviewer (WSET Level 3 award holder at minimum; Level 4 preferred for complex content). This reviewer checks factual accuracy against:

1. WSET Level 3 Award in Wines textbook (current edition)
2. WSET Level 3 course study materials
3. WSET Level 4 Diploma materials (for advanced mechanistic content)
4. Peer-reviewed viticulture and enology sources (for biochemical claims)

### 6.1 Factual accuracy checklist

| Check | Pass criterion |
|-------|---------------|
| Chemistry claims | Malic/tartaric/lactic acid chemistry is accurate; pH relationships are correct |
| Botrytis mechanism | Tartaric acid metabolism and gluconic acid production correctly described |
| MLF mechanism | Oenococcus oeni, diprotic/monoprotic acid distinction, diacetyl pathway correct |
| Oak chemistry | Ellagitannin (hydrolysable) vs. condensed tannin distinction correct |
| Regional examples | Named wines and regions exist, are correctly attributed, and match described style |
| Regulatory claims | Legal minimums (NV 15 months, Vintage 36 months tirage) are current and correct |
| Distinction notes | Content in distinction_note fields does not contradict WSET official guidance |

### 6.2 Conservative principle

When a factual claim is disputed in the scientific literature or varies by source, the more conservative statement (less specific claim, or acknowledgement of variability) is preferred. The system must not create a false sense of certainty about contested biochemical mechanisms.

### 6.3 Post-L4 actions

After L4 review, the reviewer must:
1. Update `"ingestion_status"` from `"draft"` to `"validated"` in the file's `_meta` block
2. Add a `"validated_by"` field to `_meta` with the reviewer's initials or ID
3. Add a `"validated_date"` field to `_meta` with the ISO 8601 date
4. Update the corresponding entry in `knowledge_map_manifest.json`

---

## 7. Automated Validation Script

A validation script (`tools/validate_knowledge_map.py` — planned) will perform L1 and L2 checks automatically. It will:

1. Scan all files in `concepts/`, `relationships/`, `misconceptions/`, `causal-chains/`
2. Validate each file against its schema (L1)
3. Build an index of all concept IDs
4. Check all cross-references against the index (L2)
5. Report all failures with file path, field, and failure reason
6. Return exit code 0 if all files pass, exit code 1 if any fail

The script must be run before any commit to the knowledge map and must pass before any `ingestion_status` change from `"draft"` to `"validated"`.

---

## 8. Common Failure Modes

Based on the Phase 1 build, the following failure modes are anticipated and should be checked manually in addition to automated validation:

| Failure mode | How to detect | How to fix |
|-------------|--------------|-----------|
| Lowercase IDs | `grep -r '"concept_id": "c_'` | Uppercase all IDs |
| Dangling concept references | Run L2 cross-reference check | Create missing concept file or remove reference |
| Circular causal chain logic | Manual step-by-step review | Reorder steps; ensure A→B→C, not A→B→A |
| Distinction note too vague | L3 review: "names specific compounds?" | Specify compounds, mechanisms, or regional examples |
| Detection signals too generic | L3 review: "would a real student say this?" | Use actual verbatim student phrases from tutoring experience |
| Self-referential relationships without explanation | L2 + L3 | Add explanation clarifying the self-reference |
| Missing conditions field | L1 schema check | Add conditions even if it is "No conditions — relationship holds universally" |

---

## 9. Deprecation Rules

A node may be deprecated (set to `"ingestion_status": "deprecated"`) when:

- It contains factually incorrect information that cannot be corrected without creating a new node
- The concept it represents has been split into more specific concepts (e.g., `C_ACIDITY` split into `C_TARTARIC_ACID` and `C_MALIC_ACID`)
- WSET curriculum changes make the content obsolete

Deprecated nodes must NOT be deleted. They are retained for audit trail purposes. All cross-references to deprecated nodes must be updated to point to the replacement node, and the deprecated node must contain a `"deprecated_replaced_by"` field in its `_meta` block identifying the replacement.

---

*This document is internal to the WSET-AI-System project. Validation rules reflect system design requirements and do not constitute official WSET assessment policy.*

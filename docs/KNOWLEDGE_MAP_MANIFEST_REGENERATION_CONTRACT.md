# Knowledge Map Manifest Regeneration Contract

Phase: 4A.3.6.7

Status: docs-only contract. This document defines requirements for a future regeneration process. It does not regenerate the manifest and does not modify knowledge-map nodes.

## 1. Purpose

The current knowledge-map manifest is stale. It reports 48 substantive nodes while the actual tree contains 70. A stale manifest is unsafe for any system that needs authoritative knowledge-map coverage, including:

- Diagnostic Single-Best-Answer generation and validation
- learner model concept/misconception tracking
- remediation routing
- causal-chain matching
- open-response evaluation
- future Pedagogical Strategy Layer inputs

Manifest regeneration is needed, but it must not silently clean or normalize the graph. The first safe manifest must describe the graph as it actually exists: registered and unregistered nodes, legacy and governance-style schema families, unresolved concept references, unresolved topic references, and governance status.

The regenerated manifest is a control-plane artifact. It must make downstream consumers safer by exposing uncertainty, not hiding it.

## 2. Canonical Manifest Structure

A future regenerated manifest must include these required top-level fields:

| Field | Type | Purpose |
| --- | --- | --- |
| `schema_version` | string | Manifest schema version, independent from node schema versions. |
| `generated_at` | string | ISO 8601 timestamp for regeneration. |
| `ingestion_status` | string | Status such as `draft`, `candidate`, `validated`, or `approved`. |
| `total_nodes` | integer | Count of substantive registered graph nodes represented in `nodes`. |
| `node_counts` | object | Counts by node type and schema family. |
| `categories` | object | Lists or summaries for concepts, misconceptions, causal chains, relationships, schemas, and support-only files. |
| `nodes` | array | Canonical list of substantive graph node entries. |
| `unresolved_references` | array | All unresolved or planned references found during scanning. |
| `schema_families` | object | Definitions and counts for observed node schema families. |
| `governance_summary` | object | Aggregate safe/unsafe/missing-governance counts. |
| `consumer_safety_notes` | array | Warnings for runtime and future consumers. |

Recommended optional fields:

- `manifest_id`
- `manifest_name`
- `source_root`
- `generator_name`
- `generator_version`
- `git_commit`
- `support_files`
- `validation_summary`
- `previous_manifest_comparison`
- `_meta`

The manifest must avoid implying that every node is clean, normalized, or SBA-ready.

## 3. Node Entry Schema

Every entry in `nodes` must include:

| Field | Type | Purpose |
| --- | --- | --- |
| `node_id` | string | Primary stable ID. For legacy causal chains, use `chain_id`. For governance-style causal chains, use `node_id`. |
| `file_path` | string | Repo-relative path to the node file. |
| `node_type` | string | One of `concept`, `misconception`, `causal_chain`, `relationship`. |
| `schema_family` | string | Observed schema family, not desired future schema. |
| `title_or_name` | string | Human-readable name or fallback text. |
| `governance` | object | Governance flags found, defaulted only as `missing` metadata, never invented as safe. |
| `references` | object | Outgoing references grouped by type. |
| `sba_readiness` | string | One of the approved readiness statuses. |
| `consumer_tags` | array | Intended/possible consumers, e.g. `retrieval`, `misconception_prepass`, `diagnostic_sba`, `learner_model`. |

Recommended optional node fields:

- `registered_in_previous_manifest`
- `id_field`
- `filename_match_status`
- `has_unresolved_references`
- `source_support_status`
- `schema_required_fields_present`
- `diagnostic_use_notes`
- `human_review_required`

The node entry must preserve the source node's shape. It must not force all causal chains into one normalized model during manifest regeneration.

## 4. Schema Family Policy

The manifest must explicitly report schema families.

### Concepts

Schema family: `concept_v1`

Expected fields:

- `concept_id`
- `concept_name`
- `topic_id`
- `definition`
- `common_misconceptions`
- `distinction_insights`
- `cause_effect_links`
- `official_reference`
- `tutor_allowed`
- `examiner_allowed`

Concept nodes may be tagged as high-value for diagnostic use, but only if their references resolve or unresolved references are recorded.

### Misconceptions

Schema family: `misconception_v1`

Expected fields:

- `misconception_id`
- `misconception`
- `why_incorrect`
- `corrected_understanding`
- `related_topics`
- `related_concepts`
- `severity`
- `frequency`
- `tutor_intervention`
- `detection_signals`
- optional `detection_keywords`

Misconception nodes are useful for diagnosis and distractor design, but the manifest must report missing explicit governance fields and missing `related_causal_chains` where absent.

### Legacy Causal Chains

Schema family: `causal_chain_legacy_v1`

Observed fields:

- `chain_id`
- `chain_name`
- `starting_factor`
- `intermediate_steps`
- `final_outcome`
- `examples`
- `related_exam_questions`
- `distinction_note`
- `complexity`
- `exam_relevance`
- `tutor_use`
- `examiner_use`

Legacy causal chains are strong for cause/mechanism/effect reasoning. They are not automatically governance-complete because many lack explicit `safe_for_examiner`, `examiner_scoring_allowed`, and `governance` fields.

### Governance-Style Causal Chains

Schema family: `causal_chain_governance_v1`

Observed fields:

- `node_type`
- `node_id`
- `topic`
- `trigger_keywords`
- `steps`
- `sat_relevance`
- `linked_misconceptions`
- `linked_topics`
- `agent_corpus`
- `safe_for_examiner`
- `examiner_scoring_allowed`
- `requires_human_review`
- `governance`

Governance-style causal chains are strong for retrieval and runtime safety. They are not automatically complete for diagnostic generation because many lack `starting_factor`, `intermediate_steps`, `final_outcome`, `related_exam_questions`, and explicit source references.

### Hybrid Causal Chains

Schema family: `causal_chain_hybrid_v1`

Hybrid nodes contain both legacy and governance-style fields. `cc_cool_climate_acidity.json` is the current example.

Hybrid nodes should be marked as the compatibility model candidate, not silently treated as the canonical future schema.

### Relationships

Schema family: `relationship_v1`

Expected fields:

- `relationship_id`
- `source_concept`
- `target_concept`
- `relationship_type`
- `strength`
- `conditions`
- `direction`
- `explanation`
- `exam_relevance`
- `tutor_use`
- `examiner_use`

Relationships are useful for learner model adjacency and distractor ambiguity checks. They should not be treated as standalone item-generation sources without concept and source support.

## 5. Unresolved Reference Policy

Unresolved references must be recorded, not silently ignored.

The manifest must include every unresolved reference with:

- `source_node_id`
- `source_file_path`
- `reference_field`
- `reference_value`
- `reference_type`
- `status`
- `recommended_resolution`

Allowed `reference_type` values:

- `concept`
- `topic`
- `misconception`
- `causal_chain`
- `relationship`
- `source_document`
- `planned_node`
- `external_taxonomy`

Allowed `status` values:

- `missing_target_node`
- `planned_future_node`
- `external_taxonomy_reference`
- `unregistered_but_present`
- `unknown`

Current unresolved concept references that must be captured:

- `C_AGEING_POTENTIAL`
- `C_ALCOHOL`
- `C_TARTARIC_ACID`
- `C_COMPLEXITY`
- `C_LENGTH`
- `C_OAK_AGEING`
- `C_RESIDUAL_SUGAR`

Current unresolved topic references that must be captured:

- `T_RA1_*`
- `T_RA2_*`
- `T_RA3_*`

Because `knowledge/knowledge-map/topics/` has no topic JSON nodes, topic references must be classified as either `planned_future_node` or `external_taxonomy_reference`. They must not be treated as resolved.

The manifest may include unresolved references while still being valid, provided they are explicitly reported and downstream consumers are warned.

## 6. Governance Policy

Manifest regeneration must preserve and report governance. It must never make unsafe nodes safe.

The manifest must report, when present:

- `safe_for_examiner`
- `examiner_scoring_allowed`
- `tutor_allowed`
- `examiner_allowed`
- `official_grading_authority`
- `agent_corpus`
- `requires_human_review`
- `source_type`
- `source_trust_tier`
- `generation_status`

If a node lacks governance fields, the manifest must record them as missing. It must not infer:

- `safe_for_examiner=true`
- `examiner_scoring_allowed=true`
- official authority
- official question status
- generated item readiness

Governance summary must include:

- nodes explicitly `safe_for_examiner=false`
- nodes explicitly `safe_for_examiner=true`
- nodes missing `safe_for_examiner`
- nodes explicitly `examiner_scoring_allowed=false`
- nodes explicitly `examiner_scoring_allowed=true`
- nodes missing `examiner_scoring_allowed`
- nodes with `tutor_allowed`
- nodes with `examiner_allowed`
- nodes requiring human review

Any future Diagnostic SBA consumer must treat missing governance as not safe for examiner and not official.

## 7. SBA Readiness Policy

The manifest must classify each node using one of these statuses.

### `ready_for_diagnostic_use`

Criteria:

- valid ID
- required fields for its schema family present
- references resolved or explicitly non-blocking
- no unsafe governance escalation
- content is useful for diagnosis, reasoning, or remediation

This does not mean the node can become a generated item directly. It only means it can support diagnostic workflows.

### `usable_with_enrichment`

Criteria:

- valid core content
- useful cognitive value
- missing one or more non-fatal fields, such as source support, explicit governance, related causal-chain links, or resolved topic nodes

This should be the default for most misconception and governance-style causal-chain nodes until source support and schema compatibility are added.

### `reference_only`

Criteria:

- support documentation, README, schema, taxonomy placeholder, or planning artifact
- useful for human understanding or future design
- not a substantive graph node

### `unsafe_or_incomplete`

Criteria:

- missing required identity
- malformed ID
- broken critical references not marked as planned/external
- unsafe governance claim
- ambiguous official authority
- insufficient content for diagnostic use

Nodes in this status must not feed Diagnostic SBA generation, learner mastery updates, or remediation routing except as explicitly reviewed evidence.

## 8. Consumer Safety Policy

Consumers must not assume:

- one causal-chain schema family
- every node is registered
- every reference resolves
- every node is SBA-ready
- missing governance means safe
- manifest completeness without validation

Consumer-specific requirements:

| Consumer | Required behavior |
| --- | --- |
| Retrieval | May read actual directories, but should surface schema family and unresolved-reference warnings in debug output. |
| Misconception prepass | May use misconception files by ID/text, but must not treat missing governance as examiner-safe. |
| Causal-chain matching | Must support legacy, governance, and hybrid schema families or restrict itself to an explicit allowlist. |
| SAT reasoner | Should remain independent of knowledge-map completeness; SAT graph nodes can supplement but not replace SAT alias config. |
| Diagnostic SBA | Must require `ready_for_diagnostic_use` or explicitly reviewed `usable_with_enrichment` nodes plus source support. |
| Diagnostic Outcome | May record misconception IDs, but should flag unregistered or unresolved nodes. |
| Future learner model | Must use stable IDs only after manifest validation; unresolved concepts/topics must not become mastery dimensions silently. |
| PSL | May consume learner-facing diagnostic tags, but must not use persona/strategy decisions to override factual or governance constraints. |

## 9. Regeneration Rules

Allowed during regeneration:

- scan the knowledge-map tree
- count nodes
- collect node metadata
- detect schema families
- record unresolved references
- record support files
- preserve existing governance flags
- compare actual tree with previous manifest
- write a candidate manifest only in a later approved implementation phase

Forbidden during regeneration:

- modifying knowledge-map nodes
- normalizing node schemas
- inventing missing references
- creating missing topic or concept nodes
- adding official authority
- changing `safe_for_examiner` or `examiner_scoring_allowed`
- changing retrieval behavior
- changing planner behavior
- changing SBA schemas
- deleting nodes
- using Excel, Word, PDF, OCR, external APIs, external web, embeddings, vector DB, or LLM generation

The manifest generator must be descriptive, not corrective.

## 10. Validator Requirements

Before modifying `knowledge/knowledge-map/manifests/knowledge_map_manifest.json`, validators must exist for:

1. Count consistency
   - manifest node counts match actual substantive nodes or explicitly documented exclusions.

2. ID uniqueness
   - IDs are unique across each node type and globally safe where required.

3. File existence
   - every manifest node entry points to an existing file.
   - every substantive graph node is registered or explicitly excluded.

4. ID/filename consistency
   - filename mismatches are either accepted by policy or reported.

5. Unresolved references captured
   - missing concepts, missing topics, and planned nodes appear in `unresolved_references`.

6. Governance fields preserved
   - regeneration cannot flip unsafe flags to safe.
   - missing governance must remain missing/unsafe by default.

7. Schema family detected
   - every node has a `schema_family`.
   - causal chains are classified as legacy, governance-style, hybrid, or invalid.

8. No official authority escalation
   - manifest must not create examiner authority, official scoring, official question status, or pass/fail claims.

9. Consumer safety notes present
   - manifest must warn if unresolved references or mixed schema families exist.

10. Deterministic output
   - stable ordering by `node_type`, `node_id`, and `file_path`.

## 11. Future Implementation Sequence

Recommended next phases:

1. 4A.3.6.8 - Manifest Regeneration Script Contract or Tests
   - Define expected generator inputs/outputs and deterministic ordering.
   - No manifest replacement yet.

2. 4A.3.6.9 - Manifest Validator
   - Implement validators for counts, IDs, file existence, references, governance, and schema family detection.

3. 4A.3.6.10 - Safe Manifest Regeneration
   - Generate a candidate manifest.
   - Review diff.
   - Replace `knowledge_map_manifest.json` only after validator pass.

4. 4A.3.6.11 - Consumer Regression Tests
   - Run focused tests for retrieval, misconception prepass, causal-chain matching, SAT integration, snapshots, and diagnostic schemas where relevant.

5. 4A.3.7 - Structured Question Bank Compatibility Audit
   - Resume SBA/question-bank work only after the knowledge-map control plane is stable.

## 12. Non-Goals

This contract does not:

- choose the final v2 causal-chain schema
- update the manifest
- update nodes
- create topic nodes
- resolve missing concepts
- implement validation
- create SBA items
- change runtime consumers

## Final Contract Statement

The regenerated manifest must be a truthful, conservative map of the current knowledge graph. It must represent mixed schemas, unresolved references, and missing governance explicitly. It must help future systems decide what is safe to consume; it must not make unsafe or incomplete assets appear ready by omission.

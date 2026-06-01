# Knowledge Map Manifest Regeneration Script Plan

Phase: 4A.3.6.8

Status: implementation contract and validator test plan. This phase does not regenerate `knowledge_map_manifest.json`, does not modify knowledge-map nodes, and does not create manifest tooling yet.

## 1. Script Purpose

The future manifest regeneration script should scan `knowledge/knowledge-map/` and build a manifest object that truthfully describes the current graph. It must preserve the graph as found: mixed schema families, unresolved references, missing governance fields, support-only Markdown notes, and stale-vs-current manifest deltas.

The script must describe reality safely. It must not normalize nodes, invent missing concepts/topics, or make unsafe assets appear ready.

## 2. Proposed Paths

Future script path:

- `tools/knowledge_map/regenerate_manifest.py`

Future validator path:

- `tools/knowledge_map/validate_manifest.py`

Do not implement either path until an explicit implementation phase approves it.

## 3. Input Sources

The future script should read:

- `knowledge/knowledge-map/concepts/*.json`
- `knowledge/knowledge-map/misconceptions/*.json`
- `knowledge/knowledge-map/causal-chains/*.json`
- `knowledge/knowledge-map/relationships/*.json`
- `knowledge/knowledge-map/manifests/schemas/*.json`
- `knowledge/knowledge-map/**/*.md` as support/readme files only
- existing `knowledge/knowledge-map/manifests/knowledge_map_manifest.json`

It should not read or modify external sources, Excel, Word, PDF, OCR output, APIs, embeddings, vector DBs, retrieval indexes, SBA schemas, planner files, or generated questions.

## 4. Output Target

Final output target for a later approved phase:

- `knowledge/knowledge-map/manifests/knowledge_map_manifest.json`

This phase must not write that file.

The future script should first produce an in-memory manifest object and optionally print or write a candidate report only when a later phase explicitly permits it.

## 5. Dry-Run Behavior

The future script must support dry-run mode.

Dry-run must:

- scan all input sources
- build the manifest object in memory
- validate the manifest object if validators exist
- print summary counts
- print unresolved-reference counts
- print previous-manifest deltas
- return a non-zero exit code if fatal validation fails
- avoid writing `knowledge_map_manifest.json`
- avoid modifying node files

Dry-run should be the default.

Write mode must require an explicit flag such as `--write` and must be blocked unless validators pass.

## 6. Deterministic Ordering

The manifest generator must produce stable output.

Node ordering:

1. `node_type`
2. `node_id`
3. `file_path`

Recommended node type ordering:

1. `concept`
2. `misconception`
3. `causal_chain`
4. `relationship`

Unresolved references should be sorted by:

1. `source_node_id`
2. `reference_type`
3. `reference_value`
4. `source_file_path`

Support files should be sorted by `file_path`.

## 7. Schema Family Detection

The script must detect these schema families:

- `concept`
- `misconception`
- `relationship`
- `causal_chain_legacy`
- `causal_chain_governance`
- `causal_chain_hybrid`
- `unknown`

Detection rules:

- `concept`: has `concept_id`.
- `misconception`: has `misconception_id`.
- `relationship`: has `relationship_id`.
- `causal_chain_legacy`: has `chain_id` and cause/mechanism/effect fields such as `starting_factor`, `intermediate_steps`, `final_outcome`, without governance-style `node_id`.
- `causal_chain_governance`: has `node_id`, `trigger_keywords`, `steps`, and governance fields, without legacy `chain_id`.
- `causal_chain_hybrid`: has both `chain_id` and `node_id`, or both legacy cause/mechanism/effect fields and governance-style fields.
- `unknown`: substantive JSON in graph node directories that does not match known identity fields.

The script must not convert one family into another during regeneration.

## 8. Unresolved Reference Capture

The future script must capture unresolved references for:

- concept refs
- topic refs
- causal chain refs
- misconception refs
- relationship refs
- source/document refs if modeled later

Each unresolved reference entry should include:

- `source_node_id`
- `source_file_path`
- `reference_field`
- `reference_value`
- `reference_type`
- `status`
- `recommended_resolution`

Current known unresolved concept references that must be captured:

- `C_AGEING_POTENTIAL`
- `C_ALCOHOL`
- `C_TARTARIC_ACID`
- `C_COMPLEXITY`
- `C_LENGTH`
- `C_OAK_AGEING`
- `C_RESIDUAL_SUGAR`

Current topic references such as `T_RA1_*`, `T_RA2_*`, and `T_RA3_*` must be captured as unresolved because `knowledge/knowledge-map/topics/` currently has no topic JSON nodes.

## 9. Governance Preservation

The script must report governance exactly as found.

It must preserve:

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

If a field is missing, report it as missing. Do not infer it as safe.

The script must never:

- set `safe_for_examiner=true`
- set `examiner_scoring_allowed=true`
- add official authority
- claim official question status
- claim examiner scoring status

## 10. SBA Readiness Classification

Every substantive node must be classified as one of:

- `ready_for_diagnostic_use`
- `usable_with_enrichment`
- `reference_only`
- `unsafe_or_incomplete`

Recommended classification rules:

- `ready_for_diagnostic_use`: required identity and content fields present, no unsafe governance escalation, references resolved or explicitly non-blocking, useful for diagnosis/remediation.
- `usable_with_enrichment`: valid cognitive content, but missing source support, resolved topic/concept refs, governance fields, or diagnostic-specific metadata.
- `reference_only`: README/support/schema/planning file, not a substantive graph node.
- `unsafe_or_incomplete`: missing identity, malformed ID, unresolved critical reference, unsafe governance claim, or insufficient content.

Classification must be conservative. It should support future decisions, not bless nodes for generation.

## 11. Safety Rules

Allowed:

- scan tree
- count nodes
- collect metadata
- detect schema families
- record unresolved references
- preserve governance flags
- compare current tree to existing manifest
- build an in-memory manifest object

Forbidden:

- normalizing nodes
- modifying nodes
- inventing references
- creating missing concept/topic nodes
- deleting entries
- setting any governance field to safe
- touching retrieval
- touching planner
- touching SBA schemas
- changing runtime behavior
- generating questions

## 12. Validator Plan

Future validator must check:

1. Current manifest file exists.
2. Manifest JSON is parseable.
3. Tree scan finds substantive nodes.
4. Manifest counts match actual counts after regeneration.
5. Existing manifest stale state is detectable before regeneration.
6. No manifest-listed file is missing.
7. No duplicate IDs exist in actual tree.
8. No substantive JSON node is missing an ID.
9. ID patterns are valid.
10. ID/filename mismatches are reported or explicitly allowed.
11. Unresolved references are captured.
12. Causal-chain schema family is detected.
13. Mixed causal-chain families are represented, not flattened.
14. Governance fields are preserved.
15. No official authority escalation occurs.
16. `unresolved_references`, `schema_families`, and `governance_summary` are present in future manifest objects.
17. The validator does not write files.

## 13. Read-Only Contract Test Plan

The phase includes optional read-only tests in:

- `tests/test_knowledge_map_manifest_contract.py`

The tests should verify:

- current manifest file exists
- knowledge-map tree contains more substantive nodes than the manifest claims
- no manifest-listed file is missing
- no duplicate IDs in the actual tree
- no substantive JSON node is missing an ID
- unresolved references are detectable
- causal-chain schema families are mixed
- future manifest contract requires `unresolved_references`
- future manifest contract requires `schema_families`
- future manifest contract requires `governance_summary`
- tests do not modify the manifest file

Tests must not write any files.

## 14. Future Implementation Sequence

Recommended next phases:

1. 4A.3.6.9 - Manifest Validator
   - Implement read-only validator helpers and tests.

2. 4A.3.6.10 - Safe Manifest Regeneration
   - Implement dry-run script and candidate manifest generation.
   - Do not replace the manifest until validators pass.

3. 4A.3.6.11 - Consumer Regression Tests
   - Run focused tests for retrieval, misconception prepass, causal-chain matching, SAT integration, snapshots, and diagnostic schemas where relevant.

4. 4A.3.7 - Structured Question Bank Compatibility Audit
   - Resume question-bank/SBA work only after manifest control-plane behavior is stable.

## 15. Final Contract

The future script must be deterministic, dry-run-first, read-only by default, and conservative. Its job is to expose the graph's real shape and debt. It must not repair, normalize, or promote any node during regeneration.

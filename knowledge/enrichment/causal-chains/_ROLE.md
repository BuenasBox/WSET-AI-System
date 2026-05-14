# enrichment/causal-chains/ — Role and Canonical Location Clarification

## Canonical Location for Causal Chain Nodes

The canonical location for **knowledge graph causal chain nodes** is:

```
knowledge/knowledge-map/causal-chains/
```

That directory contains the authoritative JSON files conforming to the
`causal_chain.schema.json` schema in `knowledge/knowledge-map/schemas/`.
All 17 Phase 1 causal chain nodes (e.g. `cc_mlf_acidity.json`,
`cc_oak_tannin.json`, etc.) are stored there and indexed in
`knowledge/knowledge-map/manifests/knowledge_map_manifest.json`.

---

## Purpose of This Directory

`knowledge/enrichment/causal-chains/` is a **future-use placeholder** for a
different kind of artifact: enrichment-annotated causal chain derivatives.

If this directory is ever populated, it would contain enrichment metadata
_about_ causal chains — not the causal chain nodes themselves. Potential uses
include:

- Pedagogical role annotations (`pedagogical_roles.schema.json` instances)
  that point to causal chain nodes via `content_ref`.
- Topic taxonomy linkages connecting causal chains to the `topic_taxonomy.schema.json`
  hierarchy.
- Enrichment framing templates for individual causal chain nodes when they are
  served as Tier 4 Diploma-level enrichment content.

These are separate artifacts from the graph nodes and belong in `enrichment/`
rather than `knowledge-map/`.

---

## Rule: Do Not Duplicate Node Files Here

**Do not copy or move `*.json` causal chain node files from
`knowledge/knowledge-map/causal-chains/` to this directory.**

The two directories serve distinct purposes:
- `knowledge-map/causal-chains/` = graph nodes (structure, mechanism, causal reasoning)
- `enrichment/causal-chains/` = enrichment metadata pointing at those nodes (future use)

If you are adding a new causal chain node, it goes in `knowledge-map/causal-chains/`.
If you are creating a pedagogical role annotation for an existing node, it goes here
(once this directory is activated in a future phase).

---

*See also: `docs/KNOWLEDGE_GRAPH_ARCHITECTURE.md` · `docs/INDEX.md`*

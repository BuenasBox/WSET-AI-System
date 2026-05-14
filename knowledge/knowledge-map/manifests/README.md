# knowledge-map / manifests

## Purpose

Contains manifest files that track the state, versioning, and ingestion status
of the entire knowledge map.

Manifests are the control plane for the knowledge map. They record:
- What schemas are active and at what version
- What folders contain data vs. placeholders
- What has been reviewed by a human
- What is approved for use by which agent

## Files

| File | Purpose |
|------|---------|
| `knowledge_map_manifest.json` | Master manifest for the entire knowledge-map tree |

## Rules

- Manifests are append-only. Do not remove entries; mark them as deprecated.
- Manifests must be updated whenever a schema version changes.
- Manifests must be reviewed by a human before any knowledge-map data is
  ingested into a RAG corpus.

## Status

`ingestion_status: active` — manifest initialised.

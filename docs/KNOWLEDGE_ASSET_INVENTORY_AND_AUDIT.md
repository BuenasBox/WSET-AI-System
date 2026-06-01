# Knowledge Asset Inventory And Architectural Audit

Phase: 4A.3.6.5

Status: audit-only. No generation, migration, parser, schema, manifest, corpus, or knowledge files were modified.

## Executive Summary

The repository contains a large, useful, but unevenly indexed knowledge estate. The strongest strategic assets are the official WSET text corpus, the 616-item structured internal question bank, the Wine With Jimmy pedagogical corpus, and the knowledge-map cognitive graph. The main architectural risk is not lack of material; it is fragmentation.

Headline counts:

- `knowledge/`: 2,210 files, approx. 868 MB total.
- Lightweight knowledge files under `knowledge/`: 1,275 JSON, 38 JSONL, 712 Markdown, 67 TXT, 1 Python file.
- Official WSET markdown: 52 Markdown files.
- Official WSET chunks: 52 JSONL chunks.
- Structured question bank: 616 questions.
- Wine With Jimmy clean transcripts: 30 Markdown files.
- Wine With Jimmy chunk-ready files: 30 JSONL files, 333 chunks.
- Golden tutor chunk candidates: 166 JSONL rows.
- Knowledge-map nodes on disk: 70 substantive JSON nodes across concepts, misconceptions, causal chains, and relationships.
- Knowledge-map manifest summary: 48 nodes. This is stale.
- Self-eval attempt set: 25 attempts/results.
- Tutor snapshot fixture set: 25 snapshots.

The repo is rich enough to support Diagnostic SBA, Diagnostic Outcome, Learner Model, remediation routing, and future open-response work. It is not yet cleanly indexed enough to safely migrate or generate against the whole estate without a manifest reconciliation phase.

## Method

Commands used were local-only and lightweight:

- `git status --short`
- recursive file counts under `knowledge/`
- targeted JSON/JSONL/Markdown inspection using PowerShell and `rg`
- targeted consumer search under `tools/`, `tests/`, and `frontend/`

No Excel, Word, PDF, OCR, external web, APIs, embeddings, vector DB, or LLM generation was used.

## Task A - Knowledge Asset Catalog

| Asset category | Location | Count / size | Format | Purpose | Current consumers | Future consumers |
| --- | --- | ---: | --- | --- | --- | --- |
| Official WSET Knowledge | `knowledge/official-wset/` | 84 files, approx. 565 MB | PDF, Markdown, JSONL, JSON, MD reports | Official/reference source material, grounding, curriculum scope | `tools/retrieval/official_wset_chunks.py`, `tools/retrieval/tutor_retrieval_sandbox.py`, snapshot/context packages, tests | Diagnostic SBA source support, Open Response Evaluator, curriculum mapper, remediation source grounding |
| Official WSET Markdown | `knowledge/official-wset/study-guide/wset_markdown/` | 52 MD files; `_index.json` has 50 entries | MD, JSON index | Human-readable official corpus converted to Markdown | retrieval sandbox, official chunk builder, tutor snapshots | grounding-only source support, wording-leakage checks, topic mapping |
| Official WSET Chunks | `knowledge/official-wset/study-guide/official-chunks/official_wset_chunks.jsonl` | 52 chunks | JSONL | Structured official retrieval chunks with governance metadata | official retrieval tests, retrieval sandbox | Diagnostic SBA source support, rationale grounding, open-response evidence |
| Official Curriculum Artifacts | `knowledge/official-wset/study-guide/artifacts/` | 38 learning-objective JSONL lines; topic hierarchy RA1-RA5 | JSONL, JSON | Learning objectives and draft topic hierarchy | mostly audit/planning; limited direct runtime use found | RA/topic/subtopic mapping, curriculum alignment, diagnostic coverage planner |
| Structured Question Bank | `knowledge/question-bank/structured/wset3_questions.json` | 616 questions, approx. 1.1 MB with archive | JSON | Internal training question corpus | `tools/self_eval/question_runner.py`, `tools/question_bank/convert_xlsx_to_json.py`, tests | Diagnostic SBA migration source, pilot conversion, learner analytics, open-response split |
| Question Bank Archive | `knowledge/question-bank/structured/_archive/wset3_questions.generated.json` | 616 archived questions | JSON | Historical/generated structured bank copy | tests/history only; should not be runtime source | audit comparison only |
| Question Bank Raw | `knowledge/question-bank/raw/WSET3_Banco_Maestro_V9.xlsx` | 1 XLSX, out of scope for this phase | XLSX | Original raw source for converter | `tools/question_bank/convert_xlsx_to_json.py` when explicitly run | do not use in lightweight phases unless later approved |
| Wine With Jimmy Corpus | `knowledge/wine-with-jimmy/` | 689 files, approx. 11.6 MB | MD, JSON, JSONL, SRT, reports | Third-party pedagogical explanations, SAT, exam strategy, worked examples | retrieval sandbox, dictionary extraction, transcript tooling, tests | remediation, distractor rationale support, open-response worked-answer examples, tutor context |
| Wine With Jimmy Clean Markdown | `knowledge/wine-with-jimmy/clean/` | 30 MD files | Markdown with front matter | Cleaned transcript source text | retrieval/chunk pipeline provenance | markdown question inventory, open-response preservation, pedagogical grounding |
| Wine With Jimmy Chunks | `knowledge/wine-with-jimmy/chunk-ready/` | 30 JSONL files, 333 chunks | JSONL | Tutor retrieval chunks | `tools/retrieval/tutor_retrieval_sandbox.py`, tests | remediation, SBA source-support supplement, open-response feedback |
| Golden Tutor Sources | `knowledge/wine-with-jimmy/manual-import/reports/golden_tutor_chunk_candidates.jsonl` | 166 rows | JSONL | Candidate high-value tutor chunks with score/reasoning metadata | retrieval sandbox and tests | source selection, remediation routing, pedagogical priority |
| Concept Graph | `knowledge/knowledge-map/concepts/` | 8 JSON nodes | JSON | Core WSET concepts with definitions, misconceptions, links, official references | retrieval sandbox, tests, snapshots | Diagnostic SBA, learner model, remediation, PSL, open-response rubric support |
| Misconception Graph | `knowledge/knowledge-map/misconceptions/` | 20 JSON nodes | JSON | Predictable learner misconceptions and correction strategies | `tools/orchestrator/misconception_prepass.py`, tests, context packages | distractor builder, diagnostic outcome model, remediation routing, learner state |
| Causal Chain Graph | `knowledge/knowledge-map/causal-chains/` | 32 JSON nodes | JSON | Cause-effect reasoning chains, SAT links, exam relevance | retrieval sandbox, strategic planner tests, snapshots | deterministic SBA templates, diagnostic rationales, open-response reasoning evaluator |
| Relationship Graph | `knowledge/knowledge-map/relationships/` | 10 JSON nodes | JSON | Concept-to-concept semantic relationships | retrieval sandbox, tests | graph traversal, curriculum maps, distractor similarity control |
| Knowledge Map Manifest/Schemas | `knowledge/knowledge-map/manifests/` | 1 manifest, 5 schemas | JSON, MD | Control plane for graph schemas and registered nodes | tests/docs, intended validation | manifest reconciliation, graph validator, ingestion governance |
| Config Assets | `knowledge/config/` | 6 JSON files, approx. 36 KB | JSON | Runtime and feature configs: retrieval, SAT aliases, PSL profiles, visible characters | retrieval, SAT reasoner, PSL/persona tests, answer builder | PSL, learner model, avatar/persona UI, diagnostic routing |
| Enrichment Assets | `knowledge/enrichment/` | 25 files, approx. 828 KB | JSON, JSONL, MD | dictionaries, trust tiers, retrieval priorities, diagnostic schemas | dictionary tools, retrieval, tests, diagnostic schema tests | SBA validator/generator, source governance, normalization, term disambiguation |
| Master Dictionary | `knowledge/enrichment/wset_master_dictionary/` | 424 canonical terms; 680 raw terms | JSONL, MD reports | Term normalization, aliases, category detection | transcript cleaner, retrieval sandbox, extraction/consolidation tools | duplicate-option detection, source mapping, terminology normalization |
| Diagnostic Assets | `knowledge/enrichment/diagnostic_sba_item.schema.json`, `knowledge/enrichment/diagnostic_outcome.schema.json` | 2 JSON schemas | JSON Schema | Canonical diagnostic SBA and outcome contracts | tests and validator-adjacent code | Diagnostic SBA Engine, Attempt Analyzer, remediation engine |
| Self-Eval Assets | `knowledge/self-eval/` | 1,229 files, approx. 8.7 MB | JSON, JSONL, MD | Local tutor self-evaluation outputs, attempts, summaries, sample configs | `tools/self_eval/*`, learner tracing, tests | learner analytics calibration, regression evidence, remediation outcome tuning |
| Snapshot Assets | `tests/fixtures/tutor_snapshots/` | 77 files, approx. 410 KB; 25 manifest entries | JSON, TXT | Frozen Tutor regression fixtures | `tests/test_tutor_snapshot_regression.py` | regression checks for future SBA/remediation/tutor changes |
| Retrieval Assets | `knowledge/retrieval-sandbox/` | 21 files: 7 JSON, 7 MD, 7 CSV | JSON, MD, CSV | Retrieval debug runs and context reports | retrieval sandbox tests/debug | retrieval evaluation, source ranking audit |
| Learner/Session Ledger Assets | `knowledge/nazareth/` | 43 files, approx. 512 KB | JSON, MD | Persistent learner/session context, ledgers, tutor outputs | `tools/orchestrator/session_ledger.py`, `ledger_summary.py`, `les_reconciler.py` | Learner Model, Diagnostic Outcome, progress tracking |
| Answer Pattern Assets | `knowledge/answer_patterns.json` | 1 JSON, approx. 46 KB | JSON | Answer-structure pattern metadata | tests; possible answer builder/comparator support | open-response evaluator, feedback style controls |
| Calibration Schema | `knowledge/calibration/calibration_manifest.schema.json` | schema only; no manifest instance found | JSON Schema | Future Examiner/calibration source gate | tests/docs only | official calibration gate, examiner-safe source registry |

## Task B - Knowledge Map Audit

### Manifest vs Actual Files

| Node type | Actual files | Manifest entries | Manifest summary | Health |
| --- | ---: | ---: | ---: | --- |
| Concepts | 8 | 8 | 8 | aligned |
| Misconceptions | 20 | 13 | 13 | stale |
| Causal chains | 32 | 17 | 17 | stale |
| Relationships | 10 | 10 | 10 | aligned |
| Total substantive graph nodes | 70 | 48 | 48 | stale |

### Unregistered Nodes

Unregistered misconception nodes:

- `knowledge/knowledge-map/misconceptions/mc_ageing_improvement_01.json`
- `knowledge/knowledge-map/misconceptions/mc_alcohol_quality_01.json`
- `knowledge/knowledge-map/misconceptions/mc_cold_stabilisation_quality_01.json`
- `knowledge/knowledge-map/misconceptions/mc_complexity_length_01.json`
- `knowledge/knowledge-map/misconceptions/mc_oak_quality_01.json`
- `knowledge/knowledge-map/misconceptions/mc_residual_sugar_sweet_01.json`
- `knowledge/knowledge-map/misconceptions/mc_tannin_quality_02.json`

Unregistered causal-chain nodes:

- `knowledge/knowledge-map/causal-chains/cc_barrel_ageing_oak_character.json`
- `knowledge/knowledge-map/causal-chains/cc_bottle_ageing_sediment.json`
- `knowledge/knowledge-map/causal-chains/CC_DESTEMMING_TANNIN_STRUCTURE.json`
- `knowledge/knowledge-map/causal-chains/cc_flor_biological_ageing.json`
- `knowledge/knowledge-map/causal-chains/cc_fortification_residual_sugar.json`
- `knowledge/knowledge-map/causal-chains/cc_fractional_blending_consistency.json`
- `knowledge/knowledge-map/causal-chains/CC_MACERATION_EXTRACTION.json`
- `knowledge/knowledge-map/causal-chains/CC_MECHANICAL_HARVEST_OXIDATION.json`
- `knowledge/knowledge-map/causal-chains/CC_SAT_QUALITY_HIGH.json`
- `knowledge/knowledge-map/causal-chains/CC_SAT_QUALITY_MEDIUM.json`
- `knowledge/knowledge-map/causal-chains/CC_SOIL_DRAINAGE_VINE_VIGOUR.json`
- `knowledge/knowledge-map/causal-chains/CC_SPRING_FROST_TOPOGRAPHY.json`
- `knowledge/knowledge-map/causal-chains/CC_SULPHITES_PRESERVATION.json`
- `knowledge/knowledge-map/causal-chains/cc_tannin_astringency.json`
- `knowledge/knowledge-map/causal-chains/cc_warm_climate_alcohol.json`

### Duplicate Nodes

No duplicate IDs were found for:

- `concept_id`: 8 unique
- `misconception_id`: 20 unique
- `relationship_id`: 10 unique
- `chain_id`: 16 unique where present

However, causal chains are split across two schemas:

- 16 legacy-style nodes use `chain_id`, `chain_name`, `starting_factor`, `intermediate_steps`, `final_outcome`, `related_exam_questions`.
- 16 governance-style nodes use `node_type`, `node_id`, `topic`, `trigger_keywords`, `steps`, `agent_corpus`, `safe_for_examiner`, `examiner_scoring_allowed`, `governance`.
- 1 hybrid node, `cc_cool_climate_acidity.json`, contains both styles.

This is not a data duplicate, but it is a schema-fragmentation risk.

### Reference Consistency

Observed:

- 16 causal-chain files contain `related_exam_questions`.
- 9 causal-chain files contain `linked_misconceptions`.
- Only 4 causal-chain files matched obvious `official/source/reference` language.
- Some runtime context packages reference misconception nodes directly, proving at least part of the graph is live.

Risk:

- Manifest reconciliation must happen before any graph-wide generator, learner model, or remediation planner treats the manifest as complete.
- A future graph validator should check schema family, required IDs, linked misconception IDs, linked topic IDs, governance flags, and registration status.

## Task C - Question Asset Audit

Primary source:

- `knowledge/question-bank/structured/wset3_questions.json`

Counts:

- Total questions: 616
- `theory`: 595
- `short_answer`: 21
- Entries with `options`: 616
- Entries with `correct_answer_letter`: 596
- Entries with `source_type`: 616
- Exact duplicate normalized `question_text`: 0 groups found

Archive:

- `knowledge/question-bank/structured/_archive/wset3_questions.generated.json`
- 616 questions, same structural fields as primary bank.
- Treat as historical artifact, not runtime source.

Raw:

- `knowledge/question-bank/raw/WSET3_Banco_Maestro_V9.xlsx`
- Not inspected in this phase.

Health:

- Strong corpus for internal training and future SBA migration.
- Not yet compliant with `diagnostic_sba_item_v1`.
- Uses `theory` for many MCQ-like items rather than `single_best_answer`.
- Lacks diagnostic distractor roles, source chunks, item-level source support, `misconception_id`, attempt analytics placeholders, and new governance metadata such as `uses_llm=false`.

Strategic for SBA phases:

- High value as migration candidate and calibration corpus.
- Should not be treated as official WSET material.
- Needs a deterministic adapter, not direct ingestion into the new diagnostic schema.

Conversion readiness:

- Ready as source inventory: yes.
- Ready as diagnostic SBA bank: no.
- Ready for pilot conversion: yes, after validator-aligned adapter and source-support mapping.
- Open-response candidates: the 21 `short_answer` records and Wine With Jimmy short-answer Markdown should be preserved separately.

## Task D - Official Knowledge Audit

Locations:

- `knowledge/official-wset/study-guide/wset_markdown/`
- `knowledge/official-wset/study-guide/official-chunks/`
- `knowledge/official-wset/study-guide/artifacts/`

Coverage:

- 52 Markdown files.
- 52 official JSONL chunks.
- 50 entries in `_index.json`.
- 38 learning-objective JSONL lines.
- Topic hierarchy covers RA1-RA5, but has a human-review warning.

Indexing quality:

- `_index.json` does not index `README.md` or `repair_report_wine_and_the_law.md`; this may be intentional because they are support docs, not content chapters.
- Official chunks include fields for `chunk_id`, `text`, `source_type`, `source_trust_tier`, `safe_for_tutor`, `safe_for_examiner`, `official_grading_authority`, `requires_human_review`, source path, section/subtopic metadata, `pedagogical_role`, academic level, and retrieval priority.

Chunk section distribution:

- Section 1: 1
- Section 2: 1
- Section 3: 1
- Section 4: 3
- Section 5: 8
- Section 6: 29
- Section 7: 2
- Section 8: 3
- Section 9: 1
- Section 10: 1
- `Wset Markdown`: 2 support/repair chunks

Usefulness:

- Retrieval usefulness: high.
- Generation usefulness: high for source grounding, low for wording source.
- Diagnostic usefulness: high, especially for source support and RA/topic mapping.

Risks:

- Highest wording-leakage risk in the repo.
- Topic hierarchy notes that the PDF could not be read directly and requires human verification.
- Official corpus should support rationales and citations only. It must not drive protected wording imitation or examiner-authority claims.

## Task E - Wine With Jimmy Audit

Locations:

- `knowledge/wine-with-jimmy/clean/`
- `knowledge/wine-with-jimmy/chunk-ready/`
- `knowledge/wine-with-jimmy/manual-import/reports/`
- `knowledge/wine-with-jimmy/index/videos_discovered.jsonl`

Counts:

- Clean transcript Markdown: 30
- Chunk-ready JSONL files: 30
- Chunk-ready rows: 333
- Manual import reports: 28
- Golden tutor chunk candidates: 166
- Videos discovered metadata: 377

Detected topic coverage across manual import reports:

- `regions`: 22
- `winemaking`: 20
- `exam_strategy`: 14
- `sat`: 13
- `viticulture`: 11
- `grape_varieties`: 10

Pedagogical role distribution:

- `theory_explanation`: 8
- `exam_strategy`: 7
- `tasting_practice`: 5
- `foundational`: 4
- `advanced_enrichment`: 1
- `unknown`: 3

Usefulness:

- Pedagogical value: high.
- Grounding value: medium. Good tutor-style support, but not official authority.
- Diagnostic value: high for misconception remediation, worked-answer examples, answer-structure coaching, SAT explanations, and open-response preservation.

Risks:

- Some files are noisy auto-caption transcripts.
- Some material discusses marks/exam strategy and must not become official scoring authority.
- Some transcripts contain embedded questions, but not structured item metadata.
- Should be marked pedagogical/training-only.

## Task F - Consumer Map

| Asset | Current consumers | Future consumers |
| --- | --- | --- |
| Official chunks/Markdown | `tools/retrieval/official_wset_chunks.py`, `tools/retrieval/tutor_retrieval_sandbox.py`, `tests/test_official_corpus_retrieval.py`, snapshot fixtures | Diagnostic SBA source support, Open Response Evaluator, remediation evidence, curriculum map |
| Wine With Jimmy chunks | `tools/retrieval/tutor_retrieval_sandbox.py`, dictionary extraction, transcript tests, retrieval planner tests | remediation, distractor explanations, open-response worked examples, mentorship content |
| Structured question bank | `tools/self_eval/question_runner.py`, `tools/question_bank/convert_xlsx_to_json.py`, `tests/test_question_bank_converter.py` | SBA migration, diagnostic attempts, learner progress tracking |
| Knowledge-map concepts | retrieval sandbox, snapshot context packages, tests | Diagnostic SBA templates, learner model, PSL strategy hints, concept mastery |
| Knowledge-map misconceptions | `tools/orchestrator/misconception_prepass.py`, context packages, `tests/test_milestone_1_3.py` | distractor builder, diagnostic outcome analyzer, remediation routing |
| Knowledge-map causal chains | retrieval sandbox, strategic planner tests, SAT chain tests | cause/effect SBA generator, open-response reasoning evaluator, remediation explanations |
| Knowledge-map relationships | retrieval sandbox, graph tests | similarity checks, distractor ambiguity guard, concept traversal |
| SAT aliases | `tools/tutor/sat_reasoner.py`, `tools/tutor/answer_builder.py`, SAT tests | SAT diagnostic items, tasting readiness, learner analytics |
| Domain expansions | `tools/retrieval/tutor_retrieval_sandbox.py`, retrieval integration tests | query expansion, source grounding, diagnostic topic matching |
| Master dictionary | transcript cleaner, dictionary tools, retrieval sandbox | terminology normalization, duplicate option checks, source mapping |
| Pedagogical profiles / visible characters | PSL tests, `tools/tutor/pedagogical_strategy/*` | PSL, mentorship framework, avatar/persona UI |
| Self-eval artifacts | `tools/self_eval/*`, learner tracing tests, snapshot generation | learner model calibration, diagnostic outcome validation |
| Nazareth ledger/state | `tools/orchestrator/session_ledger.py`, `ledger_summary.py`, `les_reconciler.py` | learner progress tracking, attempt analyzer, mentorship continuity |
| Diagnostic schemas | schema tests, validator tests | Diagnostic SBA Engine, Attempt Analyzer, Practice Session backend |
| Retrieval sandbox outputs | retrieval tests/debug | retrieval QA, source ranking regression, prompt-independent audit |

## Task G - Strategic Asset Ranking

### Tier 1 - Mission Critical

1. `knowledge/official-wset/study-guide/official-chunks/official_wset_chunks.jsonl`
   - Best governed grounding source. Must remain grounding-only.

2. `knowledge/question-bank/structured/wset3_questions.json`
   - Existing 616-question training corpus. Strongest question migration asset.

3. `knowledge/knowledge-map/`
   - Cognitive substrate for misconceptions, causal reasoning, remediation, and diagnostic distractors.

4. `knowledge/wine-with-jimmy/chunk-ready/`
   - Best pedagogical source for Tutor-style explanations, answer structure, SAT coaching, and remediation.

5. `knowledge/enrichment/wset_master_dictionary/consolidated/canonical_terms_master.jsonl`
   - Core term normalization and alias control.

### Tier 2 - High Value

1. `knowledge/official-wset/study-guide/wset_markdown/`
   - Useful for source review and chunk regeneration. High leakage risk.

2. `knowledge/wine-with-jimmy/manual-import/reports/golden_tutor_chunk_candidates.jsonl`
   - Source quality ranking for tutor chunks.

3. `knowledge/config/sat_observation_aliases.json`
   - SAT reasoning and tasting diagnostics.

4. `knowledge/config/domain_expansions.json`
   - Retrieval expansion and topic matching.

5. `knowledge/self-eval/`
   - Regression and outcome evidence for Tutor behavior.

6. `tests/fixtures/tutor_snapshots/`
   - Stable behavior baseline.

7. `knowledge/official-wset/study-guide/artifacts/study_guide_learning_objectives.jsonl`
   - Curriculum alignment support.

### Tier 3 - Support / Control Plane

1. `knowledge/retrieval-sandbox/`
   - Debug/audit evidence, not primary knowledge.

2. `knowledge/knowledge-map/manifests/schemas/`
   - Schema control, but incomplete without manifest reconciliation.

3. `knowledge/calibration/calibration_manifest.schema.json`
   - Important future gate, but no active manifest instance found.

4. `knowledge/config/pedagogical_profiles.json`
   - Important for PSL, not primary WSET content.

5. `knowledge/config/visible_tutor_characters.json`
   - Persona/UI planning asset, not cognitive source authority.

## Task H - Architectural Risks

### Stale Manifests

- `knowledge/knowledge-map/manifests/knowledge_map_manifest.json` reports 48 nodes, but 70 substantive graph nodes exist.
- 22 nodes are unregistered: 7 misconceptions and 15 causal chains.
- Any system using the manifest as authoritative will under-read the graph.

### Duplicated Inventories

- Structured question inventory exists in `wset3_questions.json`.
- Official Markdown inventory exists in `_index.json`.
- Wine With Jimmy source provenance exists per-file in manual import reports.
- Golden chunk candidates create another catalog-like view.
- No single machine-readable inventory reconciles these across official, pedagogical, question, and graph assets.

### Schema Fragmentation

- Causal chains use two incompatible node shapes.
- Some nodes have legacy `chain_id`; others have governance `node_id`; one appears hybrid.
- This blocks clean graph-wide validation and generator consumption.

### Orphan / Under-Registered Datasets

- Newer knowledge-map nodes are present but not registered.
- `knowledge/official-wset/study-guide/artifacts/study_guide_topic_hierarchy.json` is useful but flagged for human review.
- Calibration schema exists, but no calibration manifest instance was found.

### Dead Or Low-Utility Assets

- `knowledge/question-bank/structured/_archive/wset3_questions.generated.json` is useful only as history.
- `knowledge/retrieval-sandbox/` is useful for debug, not as factual source.
- `.gitkeep` directories under question-bank imply planned but empty `enrichment`, `exports`, and `reports`.

### Governance Risks

- Official WSET text is high-value but high leakage risk.
- Wine With Jimmy material is pedagogical and should not become official authority.
- Short-answer and open-response materials mention marks and exam strategy; these must not become official scoring.
- Persona/PSL config exists near knowledge config but should not influence factual correctness.

### Hidden Technical Debt

- Current question bank has options for all 616 records but only 596 correct letters. This is acceptable for open/short-answer preservation but must be explicit in adapters.
- Self-eval has many generated outputs under `knowledge/self-eval/`; these are evidence artifacts, not source truth.
- `knowledge/nazareth/` contains learner/session state and tutor outputs; valuable for continuity but not canonical curriculum knowledge.

## Recommendations

1. Before SBA generation or migration, run a Knowledge Map Manifest Reconciliation phase.
   - Register all actual nodes or intentionally quarantine them.
   - Normalize causal-chain schema or define a compatibility adapter.

2. Build an aggregate machine-readable knowledge asset inventory after reconciliation.
   - It should reference existing inventories rather than replacing them.
   - It should classify each asset as official grounding, pedagogical grounding, question source, diagnostic graph, runtime state, or test fixture.

3. Keep the existing structured question bank as the SBA migration source of record.
   - Do not ingest it directly into `diagnostic_sba_item_v1`.
   - Use an adapter and validator.

4. Keep official WSET corpus as grounding-only.
   - Never use official wording as generated item wording.

5. Preserve Wine With Jimmy question-bearing Markdown for open-response and remediation.
   - Convert only tiny, reviewed subsets later.

6. Treat self-eval, retrieval sandbox, snapshots, and Nazareth state as evidence/fixtures, not canonical knowledge.

## Recommended Next Phase

Phase 4A.3.6.6 - Knowledge Map Manifest Reconciliation Audit.

Deliverable should be a docs-only reconciliation plan that lists exact manifest additions, schema conflicts, and validation requirements before any manifest or node file is changed.

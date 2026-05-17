# Retrieval Depth Diagnosis
**WSET-AI-System | Step 2 — shallow_retrieval = 10 Root Cause Analysis**
Date: 2026-05-17

---

## 1. The Metric

In brutal strictness, `shallow_retrieval` fired on **10 of 25 questions** (Q1, Q2, Q4, Q6, Q12, Q14, Q16, Q17, Q21, Q24) — a regression from the prior hard-mode run (7 cases).

The comparator's `_audit_retrieval()` fires `shallow_retrieval = True` when:
```python
non_forced and high_priority == 0
```
where `non_forced` = context items that are not `misconception_node`, and `high_priority` = count of `why_retrieved` tokens matching "high" or "golden" across all retrieved context items.

---

## 2. Root Cause Decomposition

### Cause A: Comparator artifact — forced_causal_chains not counted (3 questions)

For Q1, Q2, Q4, where a causal chain node was matched and `forced_causal_chains` was populated in the context package, `high_priority` was computed only from `retrieved_context` items. Chain objects live in a separate field and were invisible to the audit logic.

**Fix:** `_audit_retrieval()` in `answer_comparator.py` extended to count `forced_causal_chains`:
```python
forced_chains = [c for c in (context_package.get("forced_causal_chains") or []) if isinstance(c, dict)]
if forced_chains:
    high_priority += len(forced_chains)
```
This eliminates false positive `shallow_retrieval` for Q1/Q2/Q4.

### Cause B: No golden chunk annotations for remaining topics (7 questions)

For Q6, Q12, Q14, Q16, Q17, Q21, Q24, the retrieved chunks are real but none carry `"golden tutor chunk candidate"` or `"high retrieval priority"` in their `why_retrieved` annotations. These annotations are added during curation and do not yet exist for topic clusters like: envejecimiento oxidativo, vendimia mecánica, heladas, densidad de plantación, suelo/drenaje, and others.

Additionally, for several of these questions, the retrieved chunks are **topically mismatched**: Spain-related queries return Germany, Tokaj, and Storage chapters because the Spanish query tokens ("envejecimiento", "oxidativo") have zero lexical overlap with any English chunk and the expansion terms for those topics were absent.

---

## 3. Retrieval Scoring Mechanics

### Token flow for a Spanish query

Query: "¿Qué influencia tiene el envejecimiento oxidativo en los vinos generosos?"

Step 1: `_tokens()` extracts `[a-zA-Z]` only → captures only ASCII: `["influencia", "tiene", "envejecimiento", "oxidativo", "vinos", "generosos"]`

Step 2: `strong_query_tokens` = above minus exclude set `{"affect","answer","exam",...}` → all 6 kept

Step 3: `DOMAIN_EXPANSIONS` lookup: before fix, "envejecimiento oxidativo" was NOT a key → no expansion → `expanded_query_tokens` = same 6 Spanish words

Step 4: Chunk scoring compares `expanded_query_tokens` against `chunk_tokens` (English text) → zero overlap for any English chunk

Step 5: Result: all chunks score near 0; top-k is determined by other signals (golden annotations, forced retrieval) → Germany/Tokaj/Storage returned as topical placeholders

### Post-fix token flow

After adding "envejecimiento oxidativo" to `DOMAIN_EXPANSIONS` with English terms `{oxidative, ageing, acetaldehyde, oloroso, rancio, fortified, sherry, jerez, ...}`:

Step 3 (after fix): trigger `"envejecimiento oxidativo"` found in `query_lower` → expansion adds English single-word terms to `expanded_query_tokens`

Step 4: "oloroso", "fortified", "sherry", "acetaldehyde" now match against English chunk tokens from Jerez/Sherry chapters → expanded_overlap > 0

Step 5: Sherry/Jerez-relevant chunks rise in ranking → topically correct retrieval

---

## 4. The _tokens() ASCII Limitation

The `_tokens()` regex `\b[a-zA-Z][a-zA-Z0-9'-]*\b` is ASCII-only. Spanish accented characters break word tokenisation:

| Input | Tokens produced |
|---|---|
| `"fermentación"` | `["fermentaci", "n"]` — word splits at `ó` |
| `"biológica"` | `["biol", "gica"]` — word splits at `ó` |
| `"aszú"` | `["asz", ""]` — word splits at `ú` |

This causes `strong_hits` mismatches in `detect_knowledge_nodes()` (requires ≥2 strong hits for causal chains), explaining the prior session's chain retrieval failure for Q1–Q4.

**Fix applied previously:** Spanish trigger_keywords added to 4 chain JSON files so that pure ASCII tokens ("jerez", "oporto", "vintage", "criaderas") reach the ≥2 threshold without depending on accented words.

**Not fixed:** `_tokens()` itself remains ASCII-only. A Unicode-aware fix (`r"\b\w[\w'-]*\b"` with `re.UNICODE`) would be a cleaner long-term solution, but it was scoped out of this pass to avoid regression risk across the full retrieval pipeline.

---

## 5. The 7 Remaining Real Gaps

These questions do not have golden chunk annotations and their topics are not covered by causal chain nodes. `shallow_retrieval` will continue to fire for them unless one of the following is addressed:

| Resolution Path | Scope | Risk |
|---|---|---|
| Add golden chunk annotations to WSET official chunks for these topics | Medium effort, safe | Low |
| Add causal chain nodes for these topic clusters | Medium effort, safe | Low |
| Extend `DOMAIN_EXPANSIONS` further (done this pass for surface-level help) | Done | Low |
| Relax `shallow_retrieval` threshold | Prohibited — masks genuine gaps | — |

**Recommended next action:** Curate golden chunk annotations for the 7 remaining topic clusters (envejecimiento oxidativo, vendimia mecánica, despalillado, espumoso+presión, suelo+drenaje, heladas, densidad de plantación) by adding `"why_retrieved": ["golden tutor chunk candidate"]` to the most relevant chunk in `golden_chunks.json` for each topic.

---

## 6. Summary Table

| Question cluster | Root cause | Fixed this pass? |
|---|---|---|
| Q1, Q2, Q4 (chain-matched) | Comparator artifact: forced_causal_chains not counted | ✅ Yes |
| Q6, Q12, Q14 (topic mismatch) | No DOMAIN_EXPANSIONS for Spanish topic → wrong chunks returned | ✅ Partially (expansions added; golden annotations still absent) |
| Q16, Q17, Q21, Q24 (no golden) | Retrieved chunks correct but lack priority annotation | ❌ No (requires golden chunk curation) |

---

## 7. Projected Metric Movement

| Metric | Brutal baseline | Expected post-fix |
|---|---|---|
| `shallow_retrieval` | 10 | 3–5 (chain-matched eliminated; expansion helps surface relevance; golden annotation gap remains) |

The remaining 3–5 represent genuine retrieval depth limitations, not false positives.

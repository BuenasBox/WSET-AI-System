# SAT Reasoning Layer — Design Document

**Status:** Design only. No code implemented.  
**Prepared by:** Claude (design review session, 2026-05-17)  
**Preconditions:** Option A complete (183 tests green, constants.py, domain_expansions.json, governance clean).  
**Governance invariant:** `safe_for_examiner = False`, `examiner_scoring_allowed = False` throughout.

---

## 1. Purpose and Scope

This document specifies the architecture for the SAT Reasoning Layer — a deterministic, rule-based reasoning module that allows the Tutor to reason systematically about wine tasting observations, derive quality-grounded conclusions, and produce WSET-register answers for SAT-type student queries.

This document also separates two problems that are currently conflated under the label `shallow_retrieval: 6`:

- **Problem A — Question bank enrichment** (expected_* fields are empty for 6 questions; the comparator cannot validate answers it has no reference for). This is a metadata quality problem, not a retrieval or reasoning problem.
- **Problem B — SAT reasoning capability** (the Tutor has no systematic way to reason from sensory observations to quality conclusions using the BICL framework). This is a new capability.

Both are addressed here. They require separate implementation phases.

---

## 2. Terminology

### 2.1 SAT (Systematic Approach to Tasting)

WSET's official structured tasting methodology. It defines a fixed observation sequence:

1. **Appearance** — clarity, intensity, colour
2. **Nose** — condition, intensity, aroma characteristics, development
3. **Palate** — sweetness, acidity, tannin (reds), alcohol, body, flavour intensity, flavour characteristics, finish
4. **Conclusions** — quality assessment, readiness/drinking window

In this system, SAT reasoning means: given one or more observations from any of the four categories, derive an inference chain that terminates in a quality-grounded conclusion. The inference must be expressed in WSET register.

### 2.2 BICL

As referenced in `answer_builder.py` KEY_TERMS (`"SAT, BICL, balance, intensity, complexity, length, acidity, tannin, body, quality assessment"`), BICL is the system's causal inference component — the framework for building backward and forward causal links between wine attributes, production decisions, and tasting outcomes. In the existing implementation, BICL manifests as:

- Causal chain nodes (causa → mecanismo → efecto → formulación de examen) stored in `knowledge/knowledge-map/causal-chains/`
- The `forced_causal_chains` field in context packages
- The `_render_causal_chain()` and `_select_best_causal_chain()` functions in `answer_builder.py`
- The `matched_causal_chains` signal in `tutor_retrieval_sandbox.py`

SAT reasoning extends BICL: whereas existing BICL chains connect production decisions to wine character (e.g., flor → oxygen protection → biological ageing), SAT reasoning adds the reverse direction — connecting observed wine character back to probable production decisions and quality conclusions.

### 2.3 shallow_retrieval (current label)

The brutal comparator assigns `shallow_retrieval` when a question's `expected_topics`, `expected_keywords`, and `expected_causal_links` fields are all empty, and the answer does not independently demonstrate coverage through a high-confidence match. This is the label's weakest trigger: it fires not because retrieval failed, but because the comparator has no reference point to test against.

---

## 3. Current State Analysis

### 3.1 What is working

The following SAT-relevant infrastructure already exists:

| Component | Location | Current capability |
|---|---|---|
| `sat_coaching` intent | `tutor_retrieval_sandbox.py` | Detected by regex; routes to `sat_logic` reasoning intent |
| `SAT_TERMS` boost | `tutor_retrieval_sandbox.py` | Binary 0.09 weight boost when query and chunk share SAT vocabulary |
| `SAT_EXPANSIONS` | `knowledge/config/domain_expansions.json` | Expands `sat`, `quality`, `balance` trigger terms |
| Quality/SAT topic pattern | `answer_builder.py` `_normal_direct_answer()` | Hard-coded pattern for "quality" + "sat" in both EN and ES |
| Causal chain rendering | `answer_builder.py` `_render_causal_chain()` | Full CAUSA/MECANISMO/EFECTO renderer, driven by forced_causal_chains |
| `_cause_effect_line()` | `answer_builder.py` | Selects best causal chain from package and renders it |
| Knowledge map causal chains | `knowledge/knowledge-map/causal-chains/` | At least 9 nodes as of last implementation phase |

### 3.2 The six failing questions (diagnosed)

The self_eval_summary reports `Sample failed answers: ['3', '12', '13', '14', '16']`. After the Q3 fix (shallow_reasoning → 0), the 6 remaining shallow_retrieval failures include Q12, Q13, Q14, Q16, and 2 unidentified questions.

**Root cause for all 6**: Their `self_eval_result.json` entries have `expected_topics: []`, `expected_keywords: []`, `expected_causal_links: []`. The brutal comparator cannot validate the answer against any reference, so it defaults to `shallow_retrieval`.

Confirmed examples:

| QID | Question (ES) | Root cause |
|---|---|---|
| Q12 | ¿Qué factor natural influye en el riesgo de heladas primaverales? | expected_* all empty; comparator has no reference |
| Q13 | ¿Qué elemento del suelo influye más directamente en el drenaje del viñedo? | expected_* all empty |
| Q14 | ¿Cuál es el principal efecto de la vendimia mecánica sobre el estilo del vino? | expected_* all empty |
| Q16 | ¿Qué práctica enológica se utiliza para aumentar la extracción de color y taninos? | expected_* all empty |

**Secondary observation**: The `answer_builder.py` already has specific topic patterns for Q12 (heladas), Q13 (suelo/drenaje), and Q14 (vendimia mecánica) in `_normal_direct_answer()`. The answers are being generated correctly; the comparator simply cannot score them. This confirms the diagnosis: these are question bank metadata gaps, not retrieval or answer quality gaps.

### 3.3 What is missing

1. **Question bank enrichment** — `self_eval_result.json` files for the 6 failing questions need `expected_topics`, `expected_keywords`, and `expected_causal_links` populated.
2. **SAT reasoning module** — there is no deterministic module that takes a set of SAT observations (acidity level, tannin level, finish length, etc.) and produces an inference chain leading to a BICL-grounded quality conclusion.
3. **SAT causal chain nodes** — the knowledge map lacks causal chains specifically modelling SAT quality inference (e.g., `high acidity + long finish + complex nose → Very Good/Outstanding quality`).
4. **SAT comparator criteria** — the brutal comparator has no SAT-specific success criteria; it cannot distinguish a well-reasoned SAT quality answer from a shallow one.

---

## 4. SAT Reasoning Model

### 4.1 Scope of SAT queries handled

The SAT reasoning layer handles queries where the student is:

- Asking how to justify a quality assessment ("cómo justifico la quality en SAT")
- Asking what a specific SAT observation implies ("qué implica una acidez alta")
- Asking how to link a palate impression to a quality conclusion
- Asking about the relationship between one or more SAT parameters

It does NOT handle:
- Pure theory questions (viticulture, vinification, wine law) — those remain with existing topic patterns
- Misconception correction — remains with `_render_misconception_answer()`
- Examiner scoring or official mark allocation — always disabled

### 4.2 Reasoning sequence

SAT reasoning is a four-stage deterministic pipeline:

```
Stage 1: DETECT
  Query → is this a SAT-type question? (boolean)

Stage 2: EXTRACT
  Query → set of SAT observation signals {parameter: level}
  e.g., {"acidity": "high", "tannin": "none", "finish": "long", "complexity": "present"}

Stage 3: INFER
  Observation signals → candidate quality hypotheses
  e.g., {"high_quality": 0.8, "good_quality": 0.6} (deterministic scores, not probabilities)

Stage 4: FORMULATE
  Best hypothesis + observations → BICL-grounded quality statement in WSET register
  e.g., "High acidity, long finish, and complexity together support a Very Good or Outstanding
        quality assessment because balance, intensity, complexity, and length — the four BICL
        criteria — are all present."
```

Each stage is independently testable. No stage uses an LLM, API, embeddings, or vector DB.

### 4.3 SAT detection

A query is classified as SAT-type when it matches any of:

- Contains `sat` or `systematic approach` (already handled by retrieval intent classifier)
- Contains `quality assessment`, `justify quality`, `calidad`, `evaluar calidad`
- Contains two or more SAT parameter terms (acidity, tannin, body, finish, balance, intensity, complexity, length) in a single query
- Contains `how to conclude`, `cómo concluir`, `what does X suggest`

Detection returns `True/False`. If `False`, the SAT layer is bypassed entirely and existing answer_builder logic handles the query.

### 4.4 Observation extraction

A fixed vocabulary of SAT parameters with allowed levels:

```python
SAT_PARAMETERS = {
    "acidity":    ["low", "medium(-)", "medium", "medium(+)", "high"],
    "tannin":     ["none", "low", "medium(-)", "medium", "medium(+)", "high"],
    "sweetness":  ["dry", "off-dry", "medium-dry", "medium-sweet", "sweet", "luscious"],
    "body":       ["light", "medium(-)", "medium", "medium(+)", "full"],
    "finish":     ["short", "medium(-)", "medium", "medium(+)", "long"],
    "intensity":  ["light", "medium", "pronounced"],
    "complexity": ["absent", "present", "high"],
    "balance":    ["unbalanced", "balanced"],
    "condition":  ["faulty", "clean"],
    "development": ["youthful", "some development", "fully developed", "past its best"],
}
```

Extraction is pure string matching against canonical aliases defined in `canonical_terms_master.jsonl` (already available in the retrieval corpus). Aliases cover Spanish equivalents: `acidez` → acidity, `tanino` → tannin, `cuerpo` → body, etc.

### 4.5 Evidence weighting

Evidence weighting is deterministic, not probabilistic. Each parameter/level combination contributes a fixed score to a set of quality tiers (Outstanding, Very Good, Good, Acceptable, Poor).

Weighting rules (rule table, not ML weights):

| Signal | Quality contribution |
|---|---|
| balance = balanced | +2 to Very Good+, +1 to Good |
| finish = long or medium(+) | +2 to Very Good+, +1 to Good |
| complexity = high | +2 to Very Good+, +1 to Good |
| intensity = pronounced | +1 to Very Good+ |
| acidity = high (with balance) | +1 to Very Good+ |
| acidity = high (without balance) | +1 to Good, neutral on VG+ |
| condition = faulty | disqualifies Outstanding, -2 from Very Good |
| development = past its best | -1 from Outstanding, -1 from Very Good |
| tannin = high (without balance) | -1 from Outstanding |

Scores are summed per quality tier. The tier with the highest score is the primary hypothesis. If two tiers are tied, both are presented as equally supported.

No floating-point computation — all scores are integers. This ensures determinism without any numerical instability.

### 4.6 Hypothesis discarding

A hypothesis is discarded if any of the following hard exclusion rules apply:

| Rule | Excluded tier |
|---|---|
| condition = faulty | Outstanding, Very Good |
| development = past its best | Outstanding |
| balance = unbalanced | Outstanding |
| finish = short | Outstanding |
| complexity = absent | Outstanding, Very Good |

After exclusion, if the top-scoring hypothesis is discarded, the next scoring tier is promoted. If no tier survives, the formulation falls back to "quality cannot be assessed from the available observations alone."

### 4.7 Quality assessment formulation

The output is a single prose paragraph in the target language (ES or EN) that:

1. States the primary quality tier conclusion
2. Names the BICL criteria that support it (balance, intensity, complexity, length)
3. Names the specific SAT observations that provide evidence for each criterion
4. Notes any observations that constrain the conclusion upward or downward
5. Closes with an exam-register formulation

Example output (ES):
> "Las observaciones de acidez elevada, final largo y complejidad alta en nariz y paladar apoyan una calidad **Muy Buena** (Very Good). En términos del marco BICL: el balance está sostenido por la acidez y la estructura; la intensity es pronunciada; la complexity está presente; y el length es largo. Esto se expresa para examen como: 'La acidez alta, el final largo y la complejidad del vino sostienen una calificación de Muy Buena: balance, intensity, complexity y length están todos presentes y en equilibrio.'"

The formulation template is a parameterised string — no LLM generation.

---

## 5. BICL Interaction

The SAT reasoning layer interacts with BICL (the causal chain component) at two points:

### 5.1 Downstream: SAT observations trigger causal chain retrieval

When a SAT-type query is detected and observations are extracted, the extractor produces a set of candidate causal chain trigger keywords. These are passed to the retrieval sandbox as `forced_retrieval_nodes` hints, not as forced nodes — they influence retrieval ranking without bypassing governance.

Example: query contains "acidez alta" → candidate trigger keywords `["acidity", "acid retention", "cool climate", "high acidity"]` → retrieval boosts chunks matching those terms.

This is additive to existing retrieval logic. No changes to the scoring formula are required — only the `query_expansion_terms` list is extended.

### 5.2 Upstream: SAT formulation incorporates forced causal chains

If the context package contains `forced_causal_chains` that are relevant to the quality conclusion, the SAT formulation section cites them. Specifically, if a causal chain's `sat_relevance` field is non-empty, that relevance note is appended to the quality formulation.

This links the SAT quality conclusion to the mechanistic explanation already rendered by `_render_causal_chain()` — they appear in adjacent sections rather than as competing content.

---

## 6. Data Requirements

### 6.1 From the official WSET corpus

Required but may already be present (verify before implementing):

- SAT grid definitions (Appearance/Nose/Palate/Conclusions vocabulary)
- Quality criteria language: "balance, intensity, complexity, length"
- Regional SAT profiles for common WSET L3 wines (Fino, Champagne, Riesling, Bordeaux-style reds)

If these are in the official chunk corpus (`official_wset_chunks.jsonl`), no new files are needed — the retrieval sandbox already loads them. If they are missing, new golden chunk candidates should be added to `golden_tutor_chunk_candidates.jsonl`.

### 6.2 From the LES

The SAT reasoning layer reads (does not write) from the learner state:

- `known_weak_areas` — to detect if SAT-related causal chains are flagged as fragile or weak
- `preferred_depth` — to select between concise and detailed quality formulations
- `pedagogical_memory.low_mastery_concepts` — to identify if BICL quality criteria need extra scaffolding

The LES is read via the existing `learner_state_context` field in the context package. No new LES read paths are required.

### 6.3 New files needed

| File | Purpose |
|---|---|
| `knowledge/knowledge-map/causal-chains/CC_SAT_QUALITY_HIGH.json` | Causal chain: high acidity + long finish → Very Good/Outstanding |
| `knowledge/knowledge-map/causal-chains/CC_SAT_QUALITY_MEDIUM.json` | Causal chain: balanced but moderate parameters → Good |
| `knowledge/config/sat_observation_aliases.json` | Alias table: Spanish ↔ English SAT parameter terms |
| `tools/tutor/sat_reasoner.py` | New module (see Section 7) |

---

## 7. System Integration Map

### 7.1 What is touched per phase

| Phase | File(s) touched | What changes |
|---|---|---|
| P1: Question bank enrichment | `knowledge/self-eval/attempts/{N}/self_eval_result.json` for 6 questions | Add expected_topics, expected_keywords, expected_causal_links |
| P2: Observation alias config | `knowledge/config/sat_observation_aliases.json` (new) | SAT vocabulary alias table |
| P3: SAT reasoner module | `tools/tutor/sat_reasoner.py` (new) | detect, extract, infer, discard, formulate functions |
| P4: SAT causal chain nodes | `knowledge/knowledge-map/causal-chains/CC_SAT_QUALITY_*.json` (2 new) | Quality inference causal chains |
| P5: Answer builder integration | `tools/tutor/answer_builder.py` | Call sat_reasoner when SAT query detected; inject quality formulation |
| P6: Retrieval integration | `tools/retrieval/tutor_retrieval_sandbox.py` | Extend query_expansion_terms with SAT observation triggers |
| P7: Comparator SAT criteria | `tools/self_eval/evaluation_reporter.py` or comparator module | Add SAT-specific success criteria check |

### 7.2 What is NOT touched

The following must not change in any phase:

- Official WSET PDFs or raw source files
- `tools/orchestrator/orchestrator.py` routes (no new routes; sat_coaching already exists)
- `tools/orchestrator/learner_state.py` write paths
- Retrieval scoring weights in `score_chunk_for_query()`
- Governance constants (`SAFE_FOR_EXAMINER`, `EXAMINER_SCORING_ALLOWED`)
- Any snapshot fixture — snapshots are regenerated only in Phase 5 after answer output changes

---

## 8. What is Explicitly Out of Scope

- **Examiner scoring** — the SAT quality conclusion is always Tutor output, never official grade
- **Embeddings or semantic similarity** — all matching is string-based, deterministic
- **LLM generation** — formulation templates are parameterised strings, not model outputs
- **Vector DB** — no new storage layer; all data is JSON/JSONL files read at module load time
- **Frontend** — no UI changes
- **Cloud services** — no API calls
- **New CLI commands** — existing `self-eval` and `orchestrator-test` commands are sufficient
- **Modifying existing causal chain nodes** — only new nodes are added; existing ones are unchanged

---

## 9. Phased Implementation Plan

### Phase 1 — Question bank enrichment (closes shallow_retrieval: 6)

**Goal:** Add `expected_topics`, `expected_keywords`, `expected_causal_links` to the 6 question bank entries that currently have empty arrays. This is the direct fix for `shallow_retrieval: 6`.

**Implementation steps:**

1. Run the self-eval at brutal strictness and collect all 25 result files.
2. Identify all questions with `failure_labels: ["shallow_retrieval"]`.
3. For each failing question, read its `question_text` and manually determine:
   - `expected_topics`: 1–3 WSET concept labels (e.g., "spring frost", "viticulture", "topography")
   - `expected_keywords`: 2–4 terms the Tutor answer must contain to be considered complete
   - `expected_causal_links`: 0–2 causal links in `X -> Y -> Z` format
4. Update each `self_eval_result.json` in place. Do not change any other field.
5. Re-run brutal self-eval. Expected outcome: `shallow_retrieval` drops toward 0 as the comparator can now validate the answers.

**Validation:** Brutal self-eval, no snapshot regeneration needed (no answer content changes).

**Risk:** Low. Question bank metadata only. No code changes, no production logic changes.

---

### Phase 2 — SAT observation alias table

**Goal:** Create the vocabulary table that maps Spanish and English SAT terms to canonical parameter/level pairs.

**New file:** `knowledge/config/sat_observation_aliases.json`

**Structure:**
```json
{
  "schema_version": "sat_aliases_v1",
  "safe_for_examiner": false,
  "parameters": {
    "acidity": {
      "levels": ["low", "medium(-)", "medium", "medium(+)", "high"],
      "aliases_es": {
        "high": ["acidez alta", "muy ácido", "acidez elevada", "alta acidez"],
        "medium": ["acidez media", "acidez moderada"],
        "low": ["acidez baja", "poco ácido"]
      },
      "aliases_en": {
        "high": ["high acidity", "very acidic", "sharp acidity"],
        "medium": ["medium acidity", "moderate acidity"],
        "low": ["low acidity", "soft acidity"]
      }
    }
  }
}
```

Complete the table for all 10 SAT parameters listed in Section 4.4.

**Validation:** Unit test that loads the file and confirms all 10 parameters are present with at least one alias per level.

---

### Phase 3 — sat_reasoner.py module

**Goal:** Implement the four-stage SAT reasoning pipeline as a standalone, independently testable module.

**New file:** `tools/tutor/sat_reasoner.py`

**Public API:**
```python
def is_sat_query(query: str, language: str) -> bool:
    """Return True if the query requires SAT reasoning."""

def extract_sat_observations(query: str, language: str, alias_table: dict) -> dict[str, str]:
    """Return {parameter: level} for each SAT signal detected in the query.
    Returns empty dict if no signals detected."""

def score_quality_hypotheses(observations: dict[str, str]) -> dict[str, int]:
    """Return {quality_tier: integer_score} for each tier.
    Uses the deterministic rule table from Section 4.5."""

def discard_invalid_hypotheses(
    scored: dict[str, int], observations: dict[str, str]
) -> dict[str, int]:
    """Remove tiers that violate hard exclusion rules from Section 4.6.
    Returns filtered dict."""

def formulate_quality_assessment(
    observations: dict[str, str],
    surviving_hypotheses: dict[str, int],
    language: str,
    causal_chains: list[dict],
) -> str:
    """Return a WSET-register quality assessment paragraph.
    Uses parameterised templates — no LLM."""
```

**Governance:** Module-level constants imported from `tools.constants`. No function in this module sets `safe_for_examiner=True` or calls any external service.

**No side effects:** `sat_reasoner.py` reads only from function arguments and the alias table loaded at module import time. It writes nothing.

**Validation:** Unit tests for each function with at least 5 assertion cases per function, covering both ES and EN paths, boundary conditions (empty observations, all parameters present, faulty condition).

---

### Phase 4 — SAT causal chain nodes

**Goal:** Add two new causal chain nodes to the knowledge map that model quality inference from SAT observations.

**New files:**
- `knowledge/knowledge-map/causal-chains/CC_SAT_QUALITY_HIGH.json`
- `knowledge/knowledge-map/causal-chains/CC_SAT_QUALITY_MEDIUM.json`

**Node structure** (follows `causal_chain_v1` schema):
```json
{
  "node_type": "causal_chain",
  "node_id": "CC_SAT_QUALITY_HIGH",
  "topic": "SAT quality assessment — high quality tier",
  "trigger_keywords": [
    "quality assessment", "calidad", "justify quality", "outstanding",
    "very good", "muy buena", "sobresaliente", "balance", "intensity",
    "complexity", "length", "finish"
  ],
  "steps": [
    {
      "step": 1, "label": "cause",
      "text": "The wine shows balanced structure (acidity, tannin, alcohol in harmony), pronounced intensity, complexity on the nose and palate, and a long finish."
    },
    {
      "step": 2, "label": "mechanism",
      "text": "All four BICL quality criteria are satisfied: Balance is achieved; Intensity is pronounced; Complexity is present across the aromatic profile; Length is long."
    },
    {
      "step": 3, "label": "effect",
      "text": "The quality assessment is Very Good or Outstanding, depending on the degree of complexity and the integration of all structural elements."
    },
    {
      "step": 4, "label": "exam_formulation",
      "text": "Justify quality by linking each BICL criterion to a specific tasting observation: balance (acidity/tannin in harmony), intensity (pronounced), complexity (multiple aromatic layers), length (long finish)."
    }
  ],
  "sat_relevance": "Use when justifying quality assessment in SAT. All four BICL criteria must be explicitly referenced and linked to observed evidence.",
  "safe_for_examiner": false,
  "examiner_scoring_allowed": false,
  "agent_corpus": "tutor",
  "requires_human_review": true,
  "_meta": {
    "schema_version": "causal_chain_v1",
    "created_date": "2026-05-17",
    "ingestion_status": "draft"
  }
}
```

**Validation:** The retrieval sandbox must load the new nodes. Run `python -m tools.retrieval.tutor_retrieval_sandbox --query "cómo justifico la quality assessment en SAT"` and confirm the new nodes appear in `matched_causal_chains`.

---

### Phase 5 — Answer builder integration

**Goal:** When `is_sat_query()` returns True, call the SAT reasoner and inject the quality formulation into the answer in a new section between the cause/effect section and the exam formulation section.

**File modified:** `tools/tutor/answer_builder.py`

**Changes:**
1. Import `sat_reasoner` at top of file.
2. In `_render_normal_answer()`, after computing `cause`, check `sat_reasoner.is_sat_query(query, language)`. If True, call the full SAT pipeline and assign the result to a new local variable `sat_quality`.
3. Add a new section `## N. Evaluación de calidad SAT` (ES) / `## N. SAT Quality Assessment` (EN) to the rendered Markdown, inserted between cause/effect and exam formulation sections.
4. Add `sat_quality` to the section if non-empty; skip the section (no heading) if empty.

**Output format (ES):**
```markdown
## 3. Evaluación de calidad SAT

{sat_quality paragraph}
```

**Snapshot impact:** This phase adds a new section to answers for SAT-type queries only. Snapshot tests WILL fail for any snapshot question that qualifies as a SAT query. After Phase 5, run `generate_tutor_snapshots.py` and commit the updated fixtures. For non-SAT questions, snapshots remain identical.

**Validation sequence:**
1. Run `python -m unittest discover -s tests -v` — expect failures only for SAT-type snapshot questions.
2. Confirm no failures for non-SAT questions (all other 180+ tests must pass).
3. Run brutal self-eval — confirm no regression on non-SAT questions.
4. Run `python tests/generate_tutor_snapshots.py`.
5. Re-run `python -m unittest discover -s tests -v` — all tests must pass.

---

### Phase 6 — Retrieval integration

**Goal:** When `is_sat_query()` returns True and observations are extracted, extend `query_expansion_terms` with the SAT observation trigger keywords before retrieval runs.

**File modified:** `tools/retrieval/tutor_retrieval_sandbox.py`

**Changes:**
1. Import `sat_reasoner` at top of file.
2. In `classify_query()`, after existing expansion logic, check `is_sat_query()`. If True, call `extract_sat_observations()` and append the parameter names and level aliases to `expanded_query_tokens`.
3. This is additive — it only extends the token set, never replaces existing signals.

**Snapshot impact:** None. Retrieval changes affect which chunks are returned, but `build_tutor_answer()` uses the context package as its only input — the context package is frozen in snapshots. Retrieval changes are invisible to existing snapshot tests.

**Validation:** Run full test suite (no snapshot regeneration needed). Run brutal self-eval and confirm no regression.

---

### Phase 7 — Comparator SAT success criteria

**Goal:** Add SAT-specific success criteria to the brutal comparator so that SAT-type answers are evaluated against quality justification standards, not just keyword matching.

**File modified:** The comparator logic in `tools/self_eval/` (identify exact file before implementation).

**New criteria for SAT questions:**
- At least one of `balance`, `intensity`, `complexity`, `length` must appear in the answer → `bicl_criteria_present`
- The answer must contain a quality tier term (`outstanding`, `very good`, `good`, `sobresaliente`, `muy buena`) → `quality_tier_stated`
- The answer must link a criterion to an observation using causal language (`because`, `porque`, `por tanto`, `therefore`) → `causal_quality_link_present`

SAT question detection in the comparator uses the same `is_sat_query()` function from `sat_reasoner.py` — single source of truth.

**Validation:** Run brutal self-eval with brutal strictness. SAT-type questions should now have `bicl_criteria_present` as a strength label rather than no SAT-specific label. `shallow_retrieval` count should remain at or below post-Phase-1 value.

---

## 10. Test Requirements

### 10.1 New test files required

| File | Tests |
|---|---|
| `tests/test_sat_reasoner.py` | `is_sat_query()` (8+ cases), `extract_sat_observations()` (8+ cases), `score_quality_hypotheses()` (6+ cases), `discard_invalid_hypotheses()` (5+ cases), `formulate_quality_assessment()` (4+ cases, both languages) |
| `tests/test_sat_observation_aliases.py` | File exists, valid JSON, all 10 parameters present, all aliases non-empty, `safe_for_examiner=False` |
| `tests/test_sat_causal_chains.py` | Both CC_SAT_QUALITY_* nodes load, have required fields, `safe_for_examiner=False`, `steps` non-empty, `exam_formulation` step present |

### 10.2 Existing tests that must remain green after each phase

- All 183 pre-Phase-1 tests
- Snapshot regression tests (except those for SAT-type questions after Phase 5; regenerate then)
- `TutorSnapshotHarnessTests` (all 9 harness tests)
- `test_constants.py`
- `test_domain_expansions.py`

### 10.3 Governance test additions

For `TutorSnapshotHarnessTests` or `test_sat_reasoner.py`:

```python
def test_sat_reasoner_governance(self):
    from tools.tutor.sat_reasoner import formulate_quality_assessment
    result = formulate_quality_assessment({}, {}, "es", [])
    # Result must not claim examiner authority
    self.assertNotIn("official", result.lower())
    self.assertNotIn("grade", result.lower())
    self.assertNotIn("mark", result.lower())
```

---

## 11. Governance Constraints

The following invariants apply to every phase and every function added:

1. `safe_for_examiner` is always `False`. No function, node, or template may set it to `True`.
2. `examiner_scoring_allowed` is always `False`. SAT quality conclusions are Tutor guidance, never official scores.
3. No LLM, API, embeddings, or vector DB is called at any point.
4. All file I/O reads only from `knowledge/` or `knowledge/config/`. No writes during answer generation.
5. The SAT quality assessment output must include the Tutor disclaimer. This is enforced by the existing disclaimer injection in `render_answer()` — the new SAT section is injected before the disclaimer, so no change to disclaimer logic is needed.
6. No function in `sat_reasoner.py` may import from `tools.orchestrator` or `tools.self_eval`. The module is a pure computation layer.

---

## 12. Snapshot Handling Policy

| Phase | Snapshot impact | Action required |
|---|---|---|
| P1 (question bank enrichment) | None — no answer content changes | Run tests; expect all to pass without regeneration |
| P2 (alias table) | None | Run tests; no regeneration |
| P3 (sat_reasoner module) | None — module not yet integrated | Run tests; no regeneration |
| P4 (causal chain nodes) | None — nodes affect retrieval only | Run tests; no regeneration |
| P5 (answer builder integration) | **Yes** — SAT-type snapshot questions gain a new section | Run tests, expect SAT-question snapshot failures, run generate_tutor_snapshots.py, commit, re-run tests |
| P6 (retrieval integration) | None — retrieval changes invisible to frozen snapshots | Run tests; no regeneration |
| P7 (comparator criteria) | None — comparator changes affect scoring labels, not Tutor output | Run tests; no regeneration |

The snapshot regeneration in Phase 5 is deliberate and expected. It is not a failure — it is confirmation that the new SAT section was added. After regeneration, all 183+ tests must pass. Commit the updated fixtures with a message like `"Add SAT quality assessment section to Tutor answer for SAT-type queries"`.

---

## 13. Success Criteria

The SAT Reasoning Layer is complete when all of the following are true:

- [ ] `shallow_retrieval` count is ≤ 1 in brutal self-eval (Phase 1 target: 0)
- [ ] `sat_reasoner.py` has ≥ 30 passing unit tests
- [ ] SAT-type queries produce a structured quality assessment section with BICL criteria cited
- [ ] All 183+ tests pass (including updated snapshots)
- [ ] No new failure labels appear in brutal self-eval
- [ ] `safe_for_examiner = False` in all new nodes, configs, and module outputs
- [ ] `formulate_quality_assessment()` contains no LLM calls, no API calls, no randomness
- [ ] `is_sat_query()` and `extract_sat_observations()` are idempotent (same input always gives same output)

---

## 14. Recommended Implementation Order for Codex

Phase 1 first — it closes the current `shallow_retrieval: 6` with no risk and no code changes. Phases 2–4 are preparatory and have no user-visible impact. Phase 5 is the first user-visible change. Phases 6 and 7 are incremental refinements.

Do not implement Phase 5 before Phase 3 is fully tested. The answer builder must not call an untested sat_reasoner.

Do not combine multiple phases in a single commit. Each phase must pass its own validation before the next begins.

---

*Document prepared for handoff to Codex. No code implemented. Implementation follows the phase order above.*

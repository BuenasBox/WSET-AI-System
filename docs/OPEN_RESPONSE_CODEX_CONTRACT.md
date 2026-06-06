# Open Response — Codex Technical Contract
**Date:** 2026-06-05  
**Phase:** Parallel Track B — Pedagogical Brain  
**Audience:** Codex (implementation agent)  
**Status:** v1 — ready to implement when designated

---

## What This Document Is

A compact technical brief summarizing what Codex needs to implement to activate the Open Response Lab. It is derived from the following pedagogical documents (read these first if questions arise):
- `docs/GOVERNED_GENERATION_CONTRACT.md`
- `docs/QUESTION_LIFECYCLE_LEVELS.md`
- `docs/PEDAGOGICAL_FLOW_ARCHITECTURE.md`
- `docs/OPEN_RESPONSE_POOL_AUDIT.md`

This document tells Codex: **what schemas to implement, what files to create, what constraints are absolute, and what must NOT be built.**

---

## Current State

```
knowledge/question-bank/open_response/normalized/diagnostic_open_response_candidates.json
  → 20 question records (schema_version: diagnostic_open_response_v1)
  → All at level: human_reviewed (approved, inactive)
  → All governance flags: false
  → feedback_rubric: placeholder (NOT operational)

knowledge/question-bank/open_response/reviews/open_response_review_records.json
  → 20 review records
  → 19 approved, 1 rejected (ID 18)
  → activation_status: all inactive

tools/open_response/  (check for existing runtime MVP files)
```

---

## Phase 1: Gold Candidate Rubric Schema

### 1.1 Extend question record schema

Add to each `gold_candidate` question (when promoted) a new top-level key: `operational_rubric`. This replaces the placeholder `feedback_rubric`.

**Schema:**
```json
"operational_rubric": {
  "concept_coverage_thresholds": {
    "high": 0.60,
    "partial": 0.30
  },
  "causal_chain_detection": {
    "chain": "A → B → C",
    "nodes": ["A_term", "B_term", "C_term"],
    "connectors": ["porque", "por lo tanto", "permite", "produce", "resulta en", "influye en", "lleva a", "hace que"]
  },
  "feedback_templates": {
    "T_HIGH_CHAIN_STRONG": "...",
    "T_HIGH_CHAIN_PRESENT": "...",
    "T_HIGH_CHAIN_PARTIAL": "...",
    "T_PARTIAL_CHAIN_STRONG": "...",
    "T_PARTIAL_CHAIN_PRESENT": "...",
    "T_PARTIAL_CHAIN_PARTIAL": "...",
    "T_PARTIAL_CHAIN_ABSENT": "...",
    "T_LOW_COVERAGE": "..."
  },
  "remediation_map": {
    "missing_causal_chain": "tutor query string",
    "low_coverage": "tutor query string",
    "default": "tutor query string"
  },
  "model_response": {
    "text": "...",
    "detected_concepts": ["...", "..."],
    "chain_class": "chain_strong"
  }
}
```

**Notes:**
- `concept_coverage_thresholds` are per-question — do not use global defaults without override
- `feedback_templates` are parameterized strings; use `{detected_concept_A}`, `{missing_chain_node}`, `{tutor_topic_hint}` as interpolation keys
- `model_response` is internal only — never surfaced to learner

### 1.2 Add to question record: level field

Add `"lifecycle_level": "human_reviewed"` (or the appropriate current level) to each record. This is the machine-readable equivalent of `docs/QUESTION_LIFECYCLE_LEVELS.md`.

**Valid values:** `"generated_candidate"`, `"corpus_supported"`, `"human_reviewed"`, `"gold_candidate"`, `"active_lab"`, `"rejected"`, `"retired"`

---

## Phase 2: Response Evaluation Engine

### 2.1 New module: `tools/open_response/response_evaluator.py`

**Purpose:** Evaluate a free-text learner response against a question's `operational_rubric`.

**Inputs:**
```python
def evaluate_response(
    question: dict,          # full question record with operational_rubric
    response_text: str,      # learner's free-text response
) -> dict:
```

**Output:**
```python
{
  "question_id": str,
  "concept_coverage": {
    "present_concepts": list[str],
    "absent_concepts": list[str],
    "coverage_ratio": float,
    "coverage_class": "high_coverage" | "partial_coverage" | "low_coverage"
  },
  "causal_chain": {
    "nodes_present": list[str],
    "nodes_absent": list[str],
    "connector_found": bool,
    "chain_class": "chain_strong" | "chain_present" | "chain_partial" | "chain_absent"
  },
  "feedback_template_key": str,
  "feedback_text": str,          # rendered from template
  "remediation_query": str,      # tutor query to surface
  "promotion_class": "strong_response" | "partial_response" | "weak_response" | "incomplete",
  "governance": {
    "safe_for_examiner": false,
    "examiner_scoring_allowed": false,
    "official_marks_assigned": false
  }
}
```

**Constraints (absolute):**
- No numeric score in output. `coverage_ratio` is internal diagnostic only — never returned to UI.
- No "correct / incorrect" language in `feedback_text`
- Uses substring/token matching only — no embeddings, no LLM, no API calls
- Deterministic — same input always produces same output
- Must pass governance check (all flags false) before returning output

### 2.2 Text normalization
Implement `_normalize_text(text: str) -> str`:
- Lowercase
- Strip Spanish diacritics (á→a, é→e, í→i, ó→o, ú→u, ñ→n)
- Strip punctuation
- Return normalized string for matching

Apply normalization to both `expected_concepts` terms and the learner response before matching.

### 2.3 Connector detection
Implement `_has_connector(text: str, connectors: list[str]) -> bool`:
- Check if any connector from the `causal_chain_detection.connectors` list appears in the normalized response text
- Return True if at least 1 connector found

---

## Phase 3: Session Composer Integration

### 3.1 New module: `tools/open_response/session_engine.py`

**Purpose:** Compose a session of N open response questions from the pool, respecting balance rules.

**Inputs:**
```python
def compose_session(
    pool_path: Path,          # path to diagnostic_open_response_candidates.json
    session_config: dict,     # {"n_questions": int, "difficulty_mix": {...}, "topic_exclusions": list}
    learner_les: dict,         # current LES (for gap targeting)
) -> list[dict]:
```

**Balance rules (enforced, not optional):**
- No two questions from the same `topic` in one session
- No two questions from the same `subtopic` in one session
- Difficulty mix must include at least 1 foundational question if `n_questions >= 3`
- `activation_status` must be `"active"` for a question to be eligible — do not include `"inactive"` questions

### 3.2 LES write-back: `tools/open_response/les_writer.py`

**Purpose:** Write evaluation outcomes to the learner's epistemic state.

**Operations allowed:**
- Increment `topic_exposure_count[topic]`
- Set `concept_gap[concept_name] = true` for absent concepts
- Set `causal_gap[chain_id] = true` if chain_absent

**Operations NOT allowed:**
- Writing any score, grade, percentage, or numeric performance metric
- Modifying `mastery_level` directly from open response outcomes (that is reserved for SBA + Tutor convergence)
- Writing anything that implies "the learner failed"

---

## Phase 4: Governance Tests

### 4.1 Tests required in `tests/test_open_response_evaluator.py`

Must include:
1. `test_no_score_in_output` — verify `coverage_ratio` is not in the returned public dict
2. `test_no_examiner_language_in_feedback` — check that feedback_text contains none of: "correcto", "incorrecto", "puntos", "nota", "marca", "calificación"
3. `test_governance_flags_false` — all governance fields in output are False
4. `test_deterministic` — same response, same question, same output on repeated calls
5. `test_concept_detection_spanish` — bilingual variants correctly detected
6. `test_connector_detection` — at least 3 Spanish connector words correctly identified
7. `test_low_coverage_template` — response with 0 concepts → T_LOW_COVERAGE selected
8. `test_chain_absent_remediation` — chain_absent → remediation from `missing_causal_chain` key

---

## What Must NOT Be Built

These are absolute prohibitions. If an ambiguity arises, default to "don't implement it":

| Prohibited | Reason |
|---|---|
| Numeric score output to UI | Examiner authority creep |
| "Correct / incorrect" in feedback text | Examiner authority creep |
| LLM call inside response_evaluator | Governance invariant |
| Embeddings for concept matching | Governance invariant |
| API call for any purpose | Governance invariant |
| Hardcoded passing threshold (e.g., "≥60% = passed") | Approaches exam territory |
| Comparison of learner score to WSET criteria | Examiner authority |
| Public activation of open response without human sign-off | Lab protocol |
| Modification of existing Tutor, Retrieval, or Self-Eval code | Separation of concerns |

---

## Files to Create

```
tools/open_response/__init__.py            (package init)
tools/open_response/response_evaluator.py (Phase 2)
tools/open_response/session_engine.py     (Phase 3, partial — session composition only)
tools/open_response/les_writer.py         (Phase 3, LES write-back)
tests/test_open_response_evaluator.py     (Phase 4)
```

**Files to extend (not replace):**
- Each `gold_candidate` question in `diagnostic_open_response_candidates.json` — add `operational_rubric` and `lifecycle_level` fields when promoted
- `knowledge/nazareth/epistemic_state.json` — extend with `concept_gap` and `causal_gap` fields (discuss schema change before implementing)

**Files to NOT touch:**
- `tools/tutor/answer_builder.py`
- `tools/retrieval/tutor_retrieval_sandbox.py`
- `tools/orchestrator/orchestrator.py`
- `tools/self_eval/` (any file)
- `tests/fixtures/tutor_snapshots/` (any file)
- `knowledge/self-eval/golden_brutal_output.json`

---

## Test Count Expectation

When Phase 2 is complete and `test_open_response_evaluator.py` is added:
- Minimum 8 new tests (governance gates listed above)
- Regular suite should stay green (1432+ passing)
- No slow golden impact expected (no changes to self-eval pipeline)

---

## Open Questions for Claude to Resolve Before Codex Implements

These require pedagogical decisions before Codex can write code. Claude will answer them in a follow-up document or session:

1. What are the per-question concept coverage thresholds for the 6 pilot questions (814, 815, 813, 800, 802, 799)?
2. What is the complete connector word list (Spanish, formal + informal register)?
3. What are the 8 feedback template texts (Spanish)?
4. What is the remediation_map for each of the 6 pilot questions?
5. Should `coverage_ratio` ever be surfaced to the learner (even as "you mentioned X of the key concepts")? Decision: **no** (current contract) — but this should be re-evaluated before Lab goes live.
6. Does `epistemic_state.json` schema need a versioning bump when `concept_gap` and `causal_gap` are added?

---

*This contract governs internal implementation only. No WSET assessment authority is implied.*

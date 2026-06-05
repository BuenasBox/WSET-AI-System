# SBA Master Bank and Governed Generation Roadmap

**Phase:** 4A.4 — Architectural Design  
**Date:** 2026-06-04  
**Status:** Design document — READ ONLY. No code changes accompany this document.  
**Scope:** 500+ SBA question bank → governed Master Bank with composable sessions and corpus-grounded generation capability  
**Analyst:** Claude (Cowork mode)

---

## Section 1: Executive Summary

The current state of the WSET-AI-System diagnostic SBA bank is a system caught between its own data and its own pipeline. The structured source bank holds 524 valid SBA items, a corpus grounding audit has classified all of them, and a functional enrichment/review/export pipeline exists — yet only 3 items are live in the cockpit. The gap is not a technology problem. It is an architecture problem: there is no single governed artifact called the Master Bank, no formal layer model defining where each item sits and what it needs to advance, and no session composition layer to turn a static payload into a pedagogically purposeful selection. This document defines all three. The Master Bank is a governed, single-source-of-truth JSON file that unifies the current fragmented pipeline — raw bank, enrichment drafts, human review records, and preguntas.json — into one canonical artifact where every item carries its full provenance, grounding evidence, and promotion status. Beyond resolving the current 3-vs-524 gap, this architecture also establishes the exact contractual rules under which new items may be generated from WSET official corpus passages, with human gates that cannot be bypassed and governance invariants that are identical to those applied to imported items. The end result is a system that can grow its active bank from 9 exportable items today to 60+ Gold Bank items over 4–6 months of systematic editorial work, with session composition delivering pedagogically sequenced sessions to the cockpit from a deterministic algorithm, no LLM, and no runtime external dependencies.

---

## Section 2: Bank Layer Architecture

The Master Bank is organized into eight distinct layers. Layers 0–4 are promotion layers: an item moves upward as it satisfies each layer's gate conditions. Layers 5–7 are operational layers: they describe how approved items are selected, deployed, and potentially extended. An item's current layer is always stored in its `layer_status` field. No item may skip a layer.

---

### Layer 0 — Raw Imported Bank

**Source:** `knowledge/question-bank/raw/WSET3_Banco_Maestro_V9.xlsx` (616 records)  
**Storage:** Read-only archive. This file is never modified.  
**State:** Unvalidated. No structural or pedagogical check has been applied.  
**Current count:** 616 records  

No item is promoted directly from Layer 0 to any higher layer. The Layer 0 archive serves as the permanent audit trail from which all downstream items are traceable.

**Gate to Layer 1:** Structural SBA check. An item must have four distinct non-empty options, a non-empty stem, and a correct answer letter in {A, B, C, D}. Items that fail this check are classified `sba_invalid` and parked in a quarantine register within the master bank with a `quarantine_reason` field. They are not discarded; they may be manually correctable.

**Known Layer 0 state:**
- 524 records pass the structural gate → eligible for Layer 1
- 71 records are `true_false_disguised` (options C/D empty, or correct_answer_letter = "Verdadero"/"Falso") → quarantine
- 21 records are `open_response` (question_type = "short_answer") → quarantine
- 1 near-duplicate pair (Q24/Q218, Jaccard 0.89) → flag in Layer 1 register, retain both pending human decision

---

### Layer 1 — Structurally Valid SBA Bank

**Current count:** 524 items  
**What it means:** The item is a well-formed four-option SBA question. Nothing more.  
**No pedagogical quality check has been applied.**  
**No corpus grounding has been verified.**  

All 524 items are in Layer 1 by default as of the Phase 4A.3.7.31 corpus verification audit. The structural adapter (`tools/question_generation/structured_question_bank_adapter.py`) is the Layer 0→1 promotion tool.

**Known quality issues present at Layer 1 (do not gate on these, but document):**
- 56.5% of items have correct answer = C; D is 3.8% (structural artifact of source XLSX generation)
- 31 items tagged RA1 are content-RA5 (storage/service/temperature/glassware/food pairing) — mislabeled
- 1 near-duplicate pair (Q24/Q218)

**Gate to Layer 2:** Corpus grounding verification. The item's correct answer and stem must be traceable to at least one passage in `knowledge/**/*.md` (712 markdown files as of this document). Grounding is classified STRONG, PARTIAL, WEAK, or NOT_FOUND by deterministic string search.

---

### Layer 2 — Corpus-Grounded Bank

**What it means:** Every item at this layer has a documented relationship to the WSET official corpus (or Wine With Jimmy / golden tutor corpus). The relationship is classified and the evidence is stored in the item's `corpus_citations` field.

**Grounding classifications:**

| Status | Definition | Action |
|--------|-----------|--------|
| STRONG | Correct answer is directly and unambiguously supported by at least one corpus passage | Eligible for Layer 3 promotion |
| PARTIAL | Correct answer is inferable from corpus but requires synthesis across passages, or a human reviewer has confirmed the grounding after initial review | Requires human confirmation before Layer 3 |
| WEAK | Corpus contains adjacent content but does not clearly support the correct answer | Quarantine; remediate or discard |
| NOT_FOUND | No corpus passage found to support the correct answer | Quarantine; do not promote without corpus remediation |
| UNVERIFIED | Corpus grounding check has not yet been run | Default state for new Layer 1 items |

**Current counts (post-remediation, Phase 4A.3.7.33):**
- STRONG: 41 items → directly eligible for Layer 3
- PARTIAL: 219 items → require human confirmation
- WEAK: 9 items → quarantine
- NOT_FOUND: 255 items → quarantine

**Critical note on DISTRACTOR_CONFLICT:** The corpus verification also identified 181 items where a distractor option is accidentally supported by a corpus passage other than the primary source. This is not a Layer 2 gate condition — it is a Layer 3 remediation requirement. Items with `DISTRACTOR_CONFLICT` may still be in Layer 2 if their correct answer is STRONG-grounded, but they cannot advance to Layer 3 without distractor remediation.

**Gate to Layer 3:** Pedagogical quality review. A human reviewer must confirm the corpus citation, complete an 11-item review checklist, resolve any DISTRACTOR_CONFLICT flags, and assign the item `requires_revision` or `approved_for_remediation`.

---

### Layer 3 — Remediated Bank

**What it means:** The item has been editorially strengthened. Distractors have been reviewed, weak distractors replaced, stem ambiguities resolved, misconception tags assigned, and causal chain IDs linked. The item has a full `feedback` section including per-distractor rationale.

**Remediation requirements:**

1. Each distractor must be plausible (not trivially wrong) but clearly refutable by the cited corpus passage
2. No distractor may be accidentally correct based on any other corpus passage (DISTRACTOR_CONFLICT resolved)
3. Stem must be unambiguous — one and only one option is defensible as correct
4. Each wrong option must have a named `diagnostic_role` from the schema enum (misconception, partial_reasoning, keyword_trap, causal_confusion, sat_confusion, near_neighbor_confusion, scope_error, regional_confusion, term_confusion, unsupported_inference)
5. `misconception_tags` must be populated where the distractor targets a known misconception node
6. `causal_chain_id` must be populated if the question exercises a causal reasoning pathway in `knowledge/knowledge-map/causal-chains/`
7. `learning_objective` must be explicit and curriculum-aligned

**Gate to Layer 4:** Full 11-item human review checklist, completed per item:

1. Stem is unambiguous and grammatically correct
2. Correct answer is unambiguous and defensible without additional context
3. Correct answer is directly supported by a named corpus citation
4. Each distractor is plausible but clearly wrong given the corpus
5. No distractor is accidentally correct based on any other corpus passage
6. Diagnostic role is correctly assigned to each wrong option
7. Misconception tags are accurate (or confirmed absent)
8. Causal chain linkage is accurate (or confirmed absent)
9. Difficulty classification is justified relative to the learning objective
10. RA assignment is accurate (correcting any RA1/RA5 mislabeling)
11. Governance fields are all present and all compliant

---

### Layer 4 — Gold Bank

**What it means:** This is the canonical, fully-reviewed, corpus-grounded, pedagogically sound item. A Gold Bank item is the unit of truth in the Master Bank.

**Requirements:**
- All 11 checklist items signed off by a human reviewer
- Corpus citation confirmed and stored in `corpus_citations`
- Difficulty calibrated against WSET L3 curriculum scope
- Diagnostic signal classified: HIGH (strong differentiator between mastery levels), MEDIUM (useful but not sharply differentiating), or LOW (confirms basic knowledge, limited differentiation)
- RA assignment confirmed (correcting any mislabeling)
- `review_status` = `approved_for_gold`
- `layer_status` = `L4`

**Current Gold Bank state:** 41 items have STRONG corpus grounding and are candidates for Layer 3→4 promotion. As of this document, no file named `gold_bank.json` exists on the `main` branch. The Gold Bank exists as a documentary concept in audit documents. A primary deliverable of Phase A (see Section 8) is to materialize it as `knowledge/question-bank/master_bank.json` with all 41 STRONG items formally promoted to L4 or identified as requiring further remediation.

**Definition of Done for Gold Bank:** ≥60 items with full metadata, ≥8 items per RA, balanced difficulty distribution (see Section 9).

---

### Layer 5 — Active Private Bank

**What it means:** A subset of Gold Bank items approved for use in the private cockpit deployment. Layer 5 is an explicit activation decision — Gold Bank status is not sufficient for activation. Each item requires a deliberate `activation_status = active_private` assignment.

**Current Layer 5 state:** 3 items (Q2, Q12, Q17) are active in `frontend/diagnostic-sba/preguntas.json`. 6 additional items (Q3, Q4, Q5, Q14, Q16, plus one more from batch 1) have `approved_for_static_demo` review status and pass the exporter dry-run gate (9 eligible total) but were never exported after batch-2 reviews were committed. This is the most immediate actionable gap.

**Layer 5 requirements:**
- `layer_status` = `L4` (must be Gold Bank item)
- `activation_status` = `active_private`
- Explicit activation decision logged in item metadata
- No automatic promotion from L4 — human decision required

**Session-composable:** Layer 5 items are the input pool for the session composer (Layer 6).

---

### Layer 6 — Session-Composed Bank

**What it means:** A dynamically selected, ordered subset of Layer 5 items, generated for a specific learner session. This is not a static file — it is a runtime output of the session composition algorithm (Section 5).

**Key properties:**
- Generated at session-compose time, not stored permanently
- Selection algorithm is fully deterministic (no LLM, no embeddings, no randomness except option shuffle)
- Ordered for learning flow (difficulty progression, RA sequencing)
- Carries session metadata: RA coverage, difficulty distribution, option distribution, learner state snapshot

**Gates:**
- Input items must be `activation_status = active_private`
- Diversity constraints enforced (RA coverage, misconception coverage, causal chain diversity)
- Deduplication applied against learner's `seen_item_ids`
- Option shuffle applied at render time (not at composition time) to address the 56.5% C-bias

**Output:** Ordered list of item_ids + session metadata JSON, consumed by the cockpit. The cockpit reads a session payload, not the Master Bank.

---

### Layer 7 — Future Generated Candidates

**What it means:** New items generated from WSET official corpus passages that did not exist in the original imported bank. These items are synthetic in origin but governed identically to imported items.

**Critical constraint:** Generated candidates enter the pipeline at Layer 2 (corpus grounding is assumed from the generation process itself) and must proceed through Layers 3→4 sequentially. No gate may be skipped. Human review is mandatory before any generated item reaches Layer 4.

**What differentiates Layer 7 from Layer 2 (imported):**
- `identity.generation_method` = `deterministic_template` or a new value `corpus_grounded_generation`
- `lineage.source_passage` field populated with the exact corpus passage used as generation basis
- `lineage.generation_gate_log` records which gates were passed and by whom
- Distractor conflict check is a required pre-composition step, not a post-hoc audit

The generation contract governing Layer 7 is defined in full in Section 4.

---

## Section 3: Required Metadata Schema

Every Master Bank item must carry the following metadata. The schema extends `diagnostic_sba_item_v1` with additional promotion-tracking and session-composition fields. A new `schema_version` value of `master_bank_item_v1` distinguishes Master Bank items from earlier enrichment drafts.

Fields are grouped by functional purpose. All fields marked **required** must be present and non-null. Fields marked **optional** may be null or absent.

---

### 3.1 Identity and Provenance

| Field | Type | Required | Description | Allowed Values |
|-------|------|----------|-------------|----------------|
| `schema_version` | string | required | Schema version identifier | `"master_bank_item_v1"` |
| `source_question_id` | string | required | Original ID from XLSX bank | e.g., `"Q001"`, `"1"` |
| `item_id` | string | required | Canonical Master Bank ID | Pattern: `^MB[0-9]{4}$`, e.g., `"MB0001"` |
| `item_version` | string | required | Semantic version of this item | e.g., `"1.0.0"` |
| `created_by` | string | required | Phase or person that created the item | e.g., `"phase_4a4_master_bank_migration"` |
| `generation_method` | enum | required | How this item was created | `manual_schema_fixture` / `deterministic_template` / `human_authored` / `corpus_grounded_generation` |
| `training_item_only` | bool | required | Must be `true` | `true` |

---

### 3.2 Curriculum and Classification

| Field | Type | Required | Description | Allowed Values |
|-------|------|----------|-------------|----------------|
| `result_area` | enum | required | WSET L3 Result Area | `RA1` / `RA2` / `RA3` / `RA4` / `RA5` |
| `topic` | string | required | Primary topic label | From topic taxonomy |
| `subtopic` | string | optional | More specific topic | From topic taxonomy |
| `wset_level` | enum | required | Curriculum level | `L2` / `L3` / `Diploma` |
| `difficulty` | enum | required | Difficulty classification | `foundational` / `intermediate` / `advanced` / `distinction` |
| `learning_objective` | string | required | Explicit learning objective | Free text, minimum 10 chars |
| `expected_reasoning_type` | enum | required | Cognitive operation tested | `definition` / `cause_effect` / `process` / `sat_reasoning` / `misconception_correction` / `regional_comparison` / `vocabulary` / `diagnostic_review` |

---

### 3.3 Question Content

| Field | Type | Required | Description | Allowed Values |
|-------|------|----------|-------------|----------------|
| `question_type` | const | required | Always this value | `"diagnostic_single_best_answer"` |
| `stem` | string | required | Question stem | Non-empty |
| `option_a` | string | required | Option A text | Non-empty |
| `option_b` | string | required | Option B text | Non-empty |
| `option_c` | string | required | Option C text | Non-empty |
| `option_d` | string | required | Option D text | Non-empty |
| `correct_option_id` | enum | required | Which option is correct | `A` / `B` / `C` / `D` |
| `correct_answer_text` | string | required | Must match the correct option text exactly | Non-empty |

**Note:** The existing schema's nested `options.{A,B,C,D}` structure with `is_correct`, `diagnostic_role`, `misconception_id`, and `misconception_description` sub-fields is preserved in full. The flat fields above are aliases for external consumption (exporter, cockpit payload). The canonical representation remains the nested structure.

---

### 3.4 Distractor Metadata

| Field | Type | Required | Description | Allowed Values |
|-------|------|----------|-------------|----------------|
| `options.A.diagnostic_role` | enum | required (L3+) | Why option A is wrong (or correct) | See schema enum |
| `options.B.diagnostic_role` | enum | required (L3+) | Why option B is wrong (or correct) | See schema enum |
| `options.C.diagnostic_role` | enum | required (L3+) | Why option C is wrong (or correct) | See schema enum |
| `options.D.diagnostic_role` | enum | required (L3+) | Why option D is wrong (or correct) | See schema enum |
| `options.{X}.misconception_id` | string | optional | Links wrong option to misconception node | Misconception node ID from `knowledge/knowledge-map/misconceptions/` |
| `options.{X}.misconception_description` | string | optional | Short description of the misconception | Free text |
| `feedback.why_other_options_are_wrong.{A,B,C,D}` | string | required (L3+) | Per-distractor rationale for the learner | Non-empty |
| `feedback.correct_rationale` | string | required (L3+) | Why the correct answer is correct | Non-empty |
| `feedback.remediation_recommendation` | string | required (L3+) | What to study if this item is missed | Non-empty |

---

### 3.5 Corpus Grounding

| Field | Type | Required | Description | Allowed Values |
|-------|------|----------|-------------|----------------|
| `corpus_citations` | list[object] | required (L2+) | Evidence passages | See structure below |
| `corpus_citations[].file` | string | required | Relative path to corpus file | e.g., `knowledge/official-wset/unit_4_climate.md` |
| `corpus_citations[].section` | string | optional | Section heading or page reference | Free text |
| `corpus_citations[].excerpt` | string | required | Verbatim or near-verbatim passage | Non-empty |
| `corpus_citations[].supports` | enum | required | What the citation supports | `correct_answer` / `distractor_refutation` / `context` |
| `grounding_status` | enum | required | Corpus grounding classification | `STRONG` / `PARTIAL` / `WEAK` / `NOT_FOUND` / `UNVERIFIED` |
| `distractor_conflict` | bool | required | Whether any distractor is accidentally corpus-supported | `true` / `false` |
| `distractor_conflict_notes` | string | optional | If `distractor_conflict = true`, details of the conflict | Free text |

---

### 3.6 Enrichment Linkage

| Field | Type | Required | Description | Allowed Values |
|-------|------|----------|-------------|----------------|
| `misconception_tags` | list[str] | optional | Misconception node IDs relevant to this item | IDs from `knowledge/knowledge-map/misconceptions/` |
| `causal_chain_id` | string | optional | Primary causal chain node exercised | ID from `knowledge/knowledge-map/causal-chains/` |
| `sat_relevance` | bool | optional | Whether this item tests SAT reasoning | `true` / `false` |

---

### 3.7 Promotion and Activation Status

| Field | Type | Required | Description | Allowed Values |
|-------|------|----------|-------------|----------------|
| `layer_status` | enum | required | Current layer in the Master Bank | `L0` / `L1` / `L2` / `L3` / `L4` / `L5` / `L6` / `L7` |
| `review_status` | enum | required | Editorial review state | `pending` / `requires_revision` / `approved_for_remediation` / `approved_for_gold` / `approved_for_active` |
| `activation_status` | enum | required | Deployment state | `inactive` / `active_private` / `active_session` |
| `diagnostic_signal` | enum | required (L4+) | Estimated diagnostic value | `HIGH` / `MEDIUM` / `LOW` / `UNRATED` |
| `generation_suitability` | enum | optional | Can this item serve as a generation template? | `TEMPLATE` / `PATTERN` / `NOT_SUITABLE` |

---

### 3.8 Governance Block

The governance block is identical to the existing `diagnostic_sba_item_v1` governance block and must be present on every item at every layer. All values are const-enforced.

```json
"governance": {
  "safe_for_examiner": false,
  "examiner_scoring_allowed": false,
  "official_wset_question": false,
  "training_item_only": true,
  "uses_llm": false,
  "uses_api": false,
  "uses_embeddings": false,
  "uses_vector_db": false,
  "cloud_services_active": false
}
```

---

### 3.9 Lineage (for generated items)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `lineage.source_question_id` | string | required | Original bank ID (or `"generated"` for Layer 7) |
| `lineage.source_bank_path` | string | conditional | Path for imported items |
| `lineage.source_passage` | string | conditional | Exact corpus passage used for generation (Layer 7 only) |
| `lineage.generation_gate_log` | list[object] | conditional | Gate-by-gate log for generated items |
| `lineage.generation_gate_log[].gate` | string | required | Gate name (A/B/C/D/E) |
| `lineage.generation_gate_log[].passed_by` | string | required | Person who confirmed the gate |
| `lineage.generation_gate_log[].passed_at` | string | required | ISO 8601 timestamp |

---

## Section 4: Corpus-Grounded Generation Contract

This section defines a hard contract. Any generated item that violates any rule in this contract cannot proceed past Layer 1 regardless of content quality. The contract cannot be relaxed by any caller, any configuration flag, or any runtime condition.

---

### 4.1 Generation Preconditions

All five conditions must be simultaneously true before any generation attempt begins:

1. A specific WSET official corpus passage (a contiguous excerpt from a file in `knowledge/official-wset/` or `knowledge/book/`) has been identified, quoted verbatim, and stored as the `lineage.source_passage` field.
2. The passage explicitly supports the intended correct answer — not by inference, not by adjacency, but by direct statement or direct logical consequence of a stated fact.
3. The intended topic is within WSET L2, L3, or Diploma scope as defined by the curriculum taxonomy.
4. A human subject-matter reviewer has reviewed the passage and confirmed that it supports the intended correct answer before any drafting begins.
5. The RA classification of the question is determinable from the passage and consistent with the curriculum taxonomy.

If any precondition is false, generation does not proceed. The corpus passage selection step is not a drafting step — it is a prerequisite step.

---

### 4.2 Generation Rules

These rules apply during drafting and are verified at Gate B (structural validation) and Gate D (pedagogical review):

**Stem rules:**
1. The stem must be derivable from the corpus passage — every factual claim in the stem must be traceable to the passage or to an established WSET curriculum fact.
2. The stem must not introduce facts not present in the passage or curriculum.
3. The stem must be unambiguous: a knowledgeable examiner reading only the passage and the stem must agree on one and only one correct answer.

**Correct answer rules:**
4. The correct answer must be explicitly stated or directly and unambiguously inferable from the cited passage.
5. The correct answer must not require synthesis across multiple passages unless all required passages are cited.

**Distractor rules:**
6. Each distractor must be plausible — a learner without deep mastery could reasonably select it.
7. Each distractor must be clearly refutable by the cited passage — a learner with mastery should reject it without ambiguity.
8. No distractor may be accidentally supported by any other corpus passage. The distractor conflict check (Gate C) is mandatory before Gate D.
9. The misconception each distractor targets must be named in `options.{X}.misconception_description`. It is not sufficient to label the diagnostic role without naming the misconception.
10. If a distractor does not target a known misconception node, a new misconception description must be authored specifically for this item.

**Format rules:**
11. `question_type` must be exactly `"diagnostic_single_best_answer"`. Hybrid formats (ranking, matching, fill-in) are not permitted.
12. There must be exactly four options (A, B, C, D), exactly one of which is correct.
13. No roleplay, narrative framing, fictional learner personas, or examiner authority claims.
14. No claim that correct selection of this item implies WSET certification, passing, or official assessment readiness.

---

### 4.3 Generation Gates

Gates must be completed in order. No gate may be skipped. Gate completion is logged in `lineage.generation_gate_log`.

**Gate A — Corpus Passage Approved**
- Trigger: before any drafting
- What is checked: Is the source passage from an official corpus file? Does it support the intended correct answer? Has a human reviewer confirmed this?
- Passed by: human reviewer
- Failure action: halt; do not draft; choose a different passage or abandon the item

**Gate B — Structural Validation**
- Trigger: after first draft is complete
- What is checked: `diagnostic_sba_validator.validate_diagnostic_sba_item()` returns zero errors; all required fields are present; `schema_version = master_bank_item_v1`; `generation_method` is a valid enum value; governance block is fully compliant
- Passed by: automated validator (deterministic, no human required)
- Failure action: return validation errors; revise draft; re-run gate

**Gate C — Distractor Conflict Check**
- Trigger: after Gate B passes
- What is checked: for each wrong option, search all 712 corpus markdown files for passages that could accidentally support it; any match flagged as DISTRACTOR_CONFLICT must be resolved by replacing or rewriting the distractor
- Passed by: automated search + human confirmation of resolution
- Failure action: replace conflicted distractor; re-run Gate B; re-run Gate C

**Gate D — Pedagogical Review Checklist**
- Trigger: after Gate C passes
- What is checked: all 11 checklist items from Layer 3→4 gate (Section 2)
- Passed by: human reviewer
- Failure action: return to drafting; revise item; re-run Gates B–D

**Gate E — Governance Compliance Check**
- Trigger: after Gate D passes
- What is checked: governance block is present; all 9 governance fields have compliant values; no forbidden key parts are present anywhere in the item; no unsafe text claims are present in any text field
- Passed by: automated check (same logic as `_validate_forbidden_content()` in the existing validator)
- Failure action: correct the violation; re-run Gate E; do not advance to Layer 3

After all five gates pass, the item enters the pipeline at Layer 2 with `grounding_status = STRONG` (assumed from the generation process) and proceeds through Layer 3 remediation (which may be minimal if generation was high quality) and Layer 4 human review.

---

### 4.4 What Claude/Codex May Assist With (Offline Only)

These activities are permitted during the generation drafting process. They are offline editorial assistance, not runtime system behavior.

- Drafting candidate stems and option sets from a provided corpus passage
- Suggesting diagnostic_role classifications for each wrong option
- Suggesting misconception_tags and misconception_description values
- Suggesting causal_chain_id linkages
- Searching corpus files for potential distractor conflicts (Gate C pre-check)
- Checking that the stem does not introduce facts not in the passage

**What must remain exclusively human:**
- Gate A: Confirming that the corpus passage is the correct basis for this question
- Gate A: Confirming that the correct answer is unambiguous given the passage
- Gate D: All 11 checklist items
- Final decision to advance an item from Layer 3 to Layer 4

**What never enters runtime:**
- LLM calls during session composition or cockpit serving
- Embeddings or vector search at any layer
- External API calls at any layer
- Cloud service calls at any layer
- Automated generation without human gate completion

---

## Section 5: Session Composition Architecture

The session composer is a deterministic local function that takes a session type, a requested item count N, and an optional learner state, and returns an ordered list of item_ids from the Layer 5 (Active Private) bank. It has no side effects, no file writes, no LLM calls, and no external dependencies.

---

### 5.1 Session Types

**`diagnostic_quick`**  
Purpose: Fast diagnostic snapshot across all RAs  
Item count: 5–8  
RA target: All 5 RAs represented; weight ≈ 20% per RA  
Difficulty: Mixed — 2 foundational, 3–4 intermediate, 1–2 advanced  
Diagnostic signal priority: HIGH items first, then MEDIUM  
Option shuffle: applied  

**`ra_focused`**  
Purpose: Deep practice within a single Result Area  
Item count: 8–12  
RA target: Single RA (specified by caller)  
Difficulty: Progressive — foundational → intermediate → advanced  
Diagnostic signal priority: Any; prefer coverage of different subtopics  
Option shuffle: applied  

**`weak_area_review`**  
Purpose: Targeted review of known learner error patterns  
Item count: 8–10  
RA target: Weighted toward learner's weak RAs (from learner state)  
Difficulty: Weighted toward foundational/intermediate  
Diagnostic signal priority: Items matching learner's `known_error_types` misconception tags  
Option shuffle: applied  
Requires: Learner state input (at minimum, `known_weak_areas`)  

**`full_mixed_practice`**  
Purpose: Comprehensive session across full curriculum scope  
Item count: 15–20  
RA target: All 5 RAs, ≥3 items per RA  
Difficulty: All levels represented; ≥3 foundational, ≥8 intermediate, ≥3 advanced  
Diagnostic signal priority: Balanced; no single RA dominates  
Option shuffle: applied  

---

### 5.2 Selection Algorithm

The composer executes these steps in order. All steps are deterministic. There is no randomness in item selection — only in option display order (handled at render time by the cockpit).

**Step 1 — Filter by activation status**  
Retain only items with `activation_status = active_private`. This is the Layer 5 pool.

**Step 2 — Apply RA weight target**  
For the requested session type, compute the target count per RA. If the Layer 5 pool does not have enough items in a given RA to meet the target, reduce that RA's slot count and log a coverage warning in the session metadata. Do not substitute from a different RA silently.

**Step 3 — Apply difficulty progression**  
Within each RA slot group, order candidates by difficulty: foundational → intermediate → advanced. For `ra_focused` sessions, enforce strict progression. For `diagnostic_quick`, allow mixed within the session but order foundational items first.

**Step 4 — Apply misconception coverage constraint**  
Among candidates with the same RA and difficulty, prefer items whose `misconception_tags` are not already represented in the current selection. This maximizes the number of distinct misconceptions exercised per session.

**Step 5 — Apply option diversity constraint**  
Track the running distribution of `correct_option_id` values in the current selection. Among otherwise equivalent candidates, prefer items that bring the A/B/C/D distribution closer to 25% each. This is a secondary preference, not a hard constraint — it should not override RA or difficulty requirements.

**Step 6 — Apply deduplication**  
If learner state is provided and includes `seen_item_ids`, exclude those items from the candidate pool before any selection step. If this leaves insufficient candidates for a session type, log a coverage warning and reduce N rather than repeating items.

**Step 7 — Apply causal chain diversity**  
Among otherwise equivalent candidates (same RA, difficulty, no misconception conflict), prefer items from different `causal_chain_id` values. This is a tertiary preference.

**Step 8 — Select and order**  
Select exactly N items (or fewer if coverage warnings applied). Order for learning flow: within each RA group, foundational before intermediate before advanced. Interleave RA groups so the session does not present all RA1 items before all RA2 items — alternate RA groups across the session.

**Step 9 — Return session payload**  
Return: ordered list of item_ids, plus session metadata object:
```json
{
  "session_type": "diagnostic_quick",
  "requested_n": 6,
  "actual_n": 6,
  "ra_coverage": {"RA1": 2, "RA2": 1, "RA3": 1, "RA4": 1, "RA5": 1},
  "difficulty_distribution": {"foundational": 2, "intermediate": 3, "advanced": 1},
  "option_distribution": {"A": 1, "B": 2, "C": 2, "D": 1},
  "misconception_coverage": ["M001", "M003", "M012", "M019", "M022"],
  "causal_chain_coverage": ["CC_FLOR", "CC_SAT_QUALITY_HIGH", "CC_TANNIN"],
  "coverage_warnings": [],
  "composed_at": "2026-06-04T00:00:00Z"
}
```

---

### 5.3 Composer Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `session_type` | enum | required | One of the four session types |
| `n` | int | required | Number of items to select |
| `learner_state` | object | optional | Learner state signals |
| `learner_state.seen_item_ids` | list[str] | optional | Items to exclude |
| `learner_state.known_weak_areas` | list[str] | optional | RA IDs with poor performance |
| `learner_state.known_error_types` | list[str] | optional | Misconception IDs the learner triggers |
| `ra_override` | str | optional | Force a specific RA (for `ra_focused` sessions) |
| `active_bank_path` | str | optional | Path to active bank JSON (defaults to `knowledge/question-bank/active_bank.json`) |

---

## Section 6: Deployment Strategy

### 6.1 File Architecture

**`knowledge/question-bank/master_bank.json`**  
The complete Master Bank. Contains all items at Layers 1–5 with full metadata. Never served to a client. This file is the source of truth for all exports, composites, and session payloads. It replaces the current fragmented state (structured source bank + enrichment drafts + human review records) with a single unified artifact.

**`knowledge/question-bank/active_bank.json`**  
A filtered export of all Layer 5 items from `master_bank.json` (items with `activation_status = active_private`). This file is what the session composer reads. It does not contain Layer 0–4 items or inactive items. Generated by the exporter when items are promoted to Layer 5. Replaces `frontend/diagnostic-sba/preguntas.json` as the session composition source.

**`frontend/diagnostic-sba/preguntas.json`** (transitional)  
Continues to exist for backward compatibility with the current cockpit. The static demo exporter (`export_static_demo_questions.py --write`) writes this file. Once the session composer is operational (Phase D), the cockpit reads session payloads directly and this file becomes vestigial.

**`session_[id].json`** (ephemeral, not committed)  
A session payload produced by the composer for a specific session. Contains the ordered item subset and session metadata. Consumed by the cockpit at session start. Not stored permanently. Not committed to the repository.

---

### 6.2 Cockpit Modes

**Current mode (v2.2, hardcoded mock):** `frontend/diagnostic-sba-v2.2/index.html` — 4 hardcoded items, `const QUESTIONS = [...]`. No JSON fetch. Superseded.

**Current mode (JSON loader):** `frontend/diagnostic-sba/index.html` — `fetch('./preguntas.json')`. Backward compatible. Continues to work as-is after Phase A, with an updated `preguntas.json` that exports all 9 eligible items.

**Phase D target (session-aware cockpit):** Cockpit receives a session payload path or a session type parameter. Composes or receives the session payload at load time. Session metadata is displayed to the learner (session type, item count, RA coverage). No cloud dependency — composition runs locally.

The session-aware cockpit is backward compatible with the JSON-loader cockpit. The composition logic runs as a local Python script (or Node.js script) before the cockpit is opened, writing a session payload to a temp file that the cockpit fetches.

---

### 6.3 Privacy Boundaries

| Artifact | Visibility | Notes |
|----------|-----------|-------|
| `master_bank.json` | Private | Never served to client; never deployed publicly |
| `active_bank.json` | Private | Served only from private deployment; not publicly indexed |
| `preguntas.json` | Private | Served from private deployment (epistemiclab.dpdns.org) |
| Session payloads | Ephemeral | Generated locally; not committed; not stored after session |
| Layer 0 archive (XLSX) | Private | Read-only; never served; gitignored |
| Corpus grounding data | Private | `docs/FULL_BANK_CORPUS_VERIFICATION.json` not publicly indexed |

---

## Section 7: Governance Invariants

These invariants apply at all layers, all times, and in all files. They are not aspirational — they are const-enforced by the validator and the exporter. Any item that violates any invariant cannot be promoted past Layer 1 and cannot be included in any export, session payload, or cockpit response.

```
safe_for_examiner              = false   # const
examiner_scoring_allowed       = false   # const
official_wset_question         = false   # const
training_item_only             = true    # const
uses_llm                       = false   # const
uses_api                       = false   # const
uses_embeddings                = false   # const
uses_vector_db                 = false   # const
cloud_services_active          = false   # const
no_llm_in_runtime              = true    # architectural invariant, not a per-item field
no_embeddings_in_runtime       = true    # architectural invariant
no_external_api_in_runtime     = true    # architectural invariant
no_official_scoring_claims     = true    # enforced by forbidden text checker
no_examiner_authority_claims   = true    # enforced by forbidden text checker
```

**Enforcement layers:**
1. **Per-item metadata:** The `governance` block is present on every item and all 9 fields have const-enforced values.
2. **Validator:** `diagnostic_sba_validator.validate_diagnostic_sba_item()` checks all governance fields, all forbidden key parts, and all unsafe text claims before any export or promotion.
3. **Exporter:** `static_demo_exporter.py` enforces `SAFE_ITEM_GOVERNANCE` and blocks `FORBIDDEN_AUTHORITY_PHRASES` and `FORBIDDEN_RENDER_KEYS` on every rendered payload.
4. **Schema:** `diagnostic_sba_item.schema.json` enforces const values at the JSON Schema level.
5. **Generation contract:** Gate E is an explicit governance check that applies to every generated item, regardless of generation quality.

**Governance violations are fatal, not warnings.** A governance violation stops the pipeline. It is never logged as a warning and continued.

---

## Section 8: Roadmap

### Phase A — Master Bank Foundation
**Priority:** Must Have  
**Estimated effort:** 4–6 hours  
**Preconditions:** None — this is the enabling step for all subsequent phases  

1. Define `master_bank_item_v1` schema as an extension of `diagnostic_sba_item_v1`. Add `layer_status`, `review_status`, `activation_status`, `diagnostic_signal`, `generation_suitability`, `corpus_citations`, `grounding_status`, `distractor_conflict`, `result_area` (canonical alias for `curriculum.ra_id`), `lineage` block, and `source_question_id` to the base schema.
2. Create `knowledge/question-bank/master_bank.json` as a structured JSON object with a `metadata` header and an `items` array.
3. Migrate the 10 currently enriched items (Q1–Q5, Q12–Q14, Q16–Q17 from the two enrichment draft batches) to `master_bank_item_v1` schema. Preserve all existing enrichment data. Set `layer_status` correctly per item (Q2, Q12, Q17 → L5; Q3, Q4, Q5, Q14, Q16 → L4 eligible; Q1 → L3 approved; Q13 → L3 requires_revision).
4. Migrate the 41 STRONG-grounded items from `docs/FULL_BANK_CORPUS_VERIFICATION.json` into the master bank at Layer 2, carrying their grounding data and distractor_conflict flags. Items not already enriched are set to `layer_status = L2`, `review_status = pending`.
5. Update `diagnostic_sba_validator.py` to enforce all new required fields from `master_bank_item_v1`.
6. Update the exporter (`export_static_demo_questions.py --write`) to read from `master_bank.json` and write both `active_bank.json` and `preguntas.json`. The exporter's `--write` run should immediately produce a `preguntas.json` with all 9 currently eligible items (resolving the 3-vs-9 gap).
7. Run `export_static_demo_questions.py --write` to publish the 9 eligible items.
8. Verify: all 660+ tests still pass.

---

### Phase B — Corpus Grounding at Scale
**Priority:** Must Have  
**Estimated effort:** 8–15 hours (depends on automation)  
**Preconditions:** Phase A complete  

1. For each of the 219 PARTIAL-grounded items: run a second-pass automated search with broader term matching (current search was case-insensitive exact; consider stemming or normalized forms). Items where the second pass finds a STRONG match → promote to STRONG automatically. Items where no improvement → flag for human review.
2. Process the ~100 PARTIAL items that remain after automated second pass: human reviewer confirms or downgrades. Items confirmed as STRONG → Layer 2 STRONG. Items downgraded → WEAK or NOT_FOUND quarantine.
3. For each of the 9 WEAK items: human reviewer determines whether the adjacent corpus content is sufficient with minor item editing, or whether the item should be quarantined.
4. The 255 NOT_FOUND items are quarantined by default. No batch action on NOT_FOUND items — they require individual human decisions. Provide a quarantine register with `quarantine_reason` and `potential_remediation` notes.
5. Target: 80–120 items reach STRONG grounding and are in Layer 2, eligible for Layer 3 promotion.
6. Resolve the RA5 mislabeling: 31 items currently tagged RA1 are content-RA5. Update their `result_area` field in the master bank. No content changes required.

---

### Phase C — Remediation Pipeline
**Priority:** Must Have  
**Estimated effort:** 15–30 hours (primarily editorial work)  
**Preconditions:** Phase B complete  

1. Prioritize Layer 2 STRONG items by RA gap severity. RA2 (0 active items, 209 bank items) and RA5 (0 active items, corrected count 69) are the highest priority.
2. For each item in priority order: complete the Layer 3 remediation requirements — strengthen weak distractors, assign diagnostic_role to each option, assign misconception tags, link causal chains, write `feedback.why_other_options_are_wrong` for each option.
3. For each remediated item: run the 11-item human review checklist (Layer 3→4 gate).
4. Items passing checklist: set `layer_status = L4`, `review_status = approved_for_gold`.
5. Address the 56.5% C-bias editorially: when remediating items, actively restructure distractors so that the correct answer is A or D in at least 40% of newly remediated items. This is an editorial priority, not a field — it manifests in `correct_option_id` distribution.
6. Target: 60–80 items reach Layer 4 (Gold Bank). With ≥8 per RA and balanced difficulty.

---

### Phase D — Session Composer
**Priority:** Should Have  
**Estimated effort:** 4–6 hours  
**Preconditions:** Phase A complete (can be done in parallel with Phase B/C)  

1. Implement `tools/session_composition/session_composer.py` as a pure function following the algorithm in Section 5.2.
2. Support all four session types defined in Section 5.1.
3. Write unit tests covering: RA coverage enforcement, difficulty progression, misconception diversity, option distribution tracking, deduplication, coverage warnings for insufficient pools.
4. Implement `tools/session_composition/export_session.py` CLI: takes session type and N, reads `active_bank.json`, writes `session_[id].json` to a temp path.
5. Test with a simulated 9-item active bank (current state) and a simulated 60-item active bank (target state).
6. Verify: all existing 660+ tests still pass; at least 30 new session composer tests added.

---

### Phase E — Cockpit Integration
**Priority:** Should Have  
**Estimated effort:** 3–4 hours  
**Preconditions:** Phase D complete  

1. Update `frontend/diagnostic-sba/index.html` to accept a session payload path parameter (query string or environment variable) in addition to the static `preguntas.json` fallback.
2. Add session metadata display to the cockpit UI: session type label, item count, RA coverage indicator.
3. Add option shuffle to the cockpit render layer. This resolves the 56.5% C-bias at the presentation layer without requiring item content changes.
4. Verify: the cockpit continues to work in static demo mode (backward compatible with current `preguntas.json`).
5. Verify: the cockpit correctly renders a composed session payload from the Phase D session composer.

---

### Phase F — Governed Generation Pipeline
**Priority:** Later  
**Estimated effort:** 10–20 hours  
**Preconditions:** Phase C complete; at least 60 Gold Bank items exist; generation contract ratified  

1. Implement `tools/question_generation/corpus_passage_annotator.py`: an offline tool that takes a corpus file path and section range, extracts the passage, and scaffolds a `master_bank_item_v1` draft with the passage stored in `lineage.source_passage` and Gate A metadata ready for human reviewer sign-off.
2. Implement Gate C automation: `tools/question_generation/distractor_conflict_checker.py` — searches all corpus files for passages that could support each distractor. Returns a conflict report. Must return zero false negatives (prefer over-reporting).
3. Extend `diagnostic_sba_validator.py` to enforce all `master_bank_item_v1` generation-specific required fields when `generation_method = corpus_grounded_generation`.
4. Pilot: generate 5–10 items from corpus passages in `knowledge/official-wset/`. Run through all five gates. Human reviewer completes all gate sign-offs. Advance to Layer 4.
5. Post-pilot review: assess quality of generated items vs. imported items. Calibrate distractor conflict checker threshold.
6. Ratify the generation contract (this document, Section 4) with a sign-off record in `docs/GENERATION_CONTRACT_RATIFICATION.md`.

---

## Section 9: Definition of Done

### 9.1 Master Bank Done

All of the following must be simultaneously true:

1. `knowledge/question-bank/master_bank.json` exists and is valid under `master_bank_item_v1` schema
2. At least 60 items have `layer_status = L4` (`approved_for_gold`)
3. All L4+ items have `corpus_citations` with at least one `STRONG`-grounded citation
4. RA coverage: ≥8 items per RA across all five RAs (RA1, RA2, RA3, RA4, RA5)
5. Difficulty coverage: ≥15 foundational, ≥25 intermediate, ≥10 advanced (among L4+ items)
6. Option distribution among L4+ items: `correct_option_id` A, B, C, D each between 18% and 32%
7. All items pass `validate_diagnostic_sba_item()` with 0 errors
8. Session composer produces valid sessions for all four session types from the active bank
9. Cockpit serves sessions composed from `master_bank.json` (via `active_bank.json`)
10. All 660+ existing tests pass; new tests for master bank validation and session composition pass

### 9.2 Governed Question Generation Done

All of the following must be simultaneously true:

1. Generation contract (Section 4 of this document) is ratified in `docs/GENERATION_CONTRACT_RATIFICATION.md` with a named human sign-off
2. Corpus passage annotation workflow is documented in `docs/CORPUS_PASSAGE_ANNOTATION_WORKFLOW.md` and tested with at least 3 example passages
3. At least 5 new items have been fully gated (Gates A–E) and have reached `layer_status = L4`
4. `tools/question_generation/distractor_conflict_checker.py` is operational and tested with at least 20 known conflict and non-conflict cases
5. Human review pipeline handles generated items identically to imported items — same 11-item checklist, same gate log, same master bank schema
6. No generated item has `layer_status = L4` without a complete `lineage.generation_gate_log` showing all five gates passed with named reviewers and timestamps
7. All 660+ existing tests pass; at least 20 new tests for the generation contract enforcement pass

---

## Section 10: Risks

| Risk | Layer(s) affected | Severity | Mitigation |
|------|------------------|----------|------------|
| Corpus grounding bottleneck: 219 PARTIAL items require human review; this is the main funnel constraint for reaching 60 Gold items | L1→L2 | HIGH | Automate second-pass search with normalized terms; human confirms only items where automation is ambiguous; batch in RA-priority order |
| Editorial fatigue: remediating 60–80 items requires sustained per-item attention (distractor review, rationale writing, checklist) | L2→L3 | HIGH | Prioritize by RA gap (RA2/RA5 first); batch in groups of 5–10; treat each batch as a discrete deliverable; do not attempt all 80 in one session |
| Option distribution bias (56.5% C among all 524 items): without editorial correction, the Gold Bank will inherit this bias and erode learner calibration | L4→L5 | MEDIUM | Enforce editorial priority to make correct_option_id A or D in ≥40% of newly remediated items; implement cockpit option shuffle in Phase E as a complementary mitigation |
| Generated item hallucination: a generated distractor could accidentally be correct, or a generated stem could introduce facts not in the corpus | L7 | CRITICAL | Gate C (distractor conflict check) is mandatory and automated; Gate A (passage confirmation) is human; Gate D (checklist) explicitly checks for stem facts not in passage; no generated item reaches L4 without all five gates signed off |
| Schema drift: metadata requirements will evolve as the bank grows; items migrated early may be missing fields added later | All | MEDIUM | Add `schema_version` field to every item; implement a migration script for each schema version change; run migration as part of any Phase that adds required fields |
| RA5 mislabeling: 31 items tagged RA1 are content-RA5; RA coverage reports are incorrect until this is corrected | L1–L4 | MEDIUM | Correct `result_area` for these 31 items in Phase A/B as part of master bank migration; no content changes required, only metadata correction |
| Near-duplicate items (Q24/Q218): two items with 89% stem similarity will consume two slots and deliver near-zero additional diagnostic information | L1–L4 | LOW | Flag in master bank metadata; human reviewer decides which to keep; the discarded item is quarantined, not deleted |
| Cockpit backward compatibility: Phase D/E changes to the cockpit must not break the current static demo behavior | L5–L6 | LOW | Session payload path parameter is additive; static demo fallback to `preguntas.json` is preserved; test both modes before deploying |
| Master bank file size: 524 items with full metadata may produce a file too large for comfortable editing | All | LOW | Editors work with layer-filtered exports, not the full master bank; the composer reads `active_bank.json` (L5 only); the master bank is a machine artifact, not a human-edited file |

---

*This document is a development planning artifact. It does not represent WSET assessment authority, official examiner guidance, or official scoring capability. All items described herein are training-only materials.*

# PHASE P2 — OPEN RESPONSE INTELLIGENCE ARCHITECTURE

**Date:** 2026-06-13  
**Status:** Architecture design document — no implementation yet  
**Objective:** Turn Open Response into the primary Distinction-training engine by implementing deterministic, multi-dimensional evaluation against all 12 command verbs and Universal Distinction Chain

---

## EXECUTIVE SUMMARY

Phase P1 (SBA enrichment) is complete: 205 items at 35.3% coverage, frozen at precision-first matching.

**Phase P2 shifts focus** from SBA to Open Response, using:
- The 6 documented **command verbs** (describe, explain, assess, evaluate, compare, justify) + 6 missing (why, how, discuss, identify-and-explain, outline, state, list)
- Nazareth's **Distinction structures** (descriptor patterns, quality reasoning, readiness patterns, response structures)
- The existing **learner_intelligence.js** framework
- **Deterministic, evaluation-safe architecture** that never claims to be an examiner

**Current state:** 20 active ORL items with basic concept + causal evaluation  
**Target state:** 20 → 50+ items with comprehensive command-verb + distinction-chain evaluation  
**Safety:** All evaluation remains `formative_only=true`; `safe_for_examiner=false` unchanged

---

## PART 1: CURRENT STATE AUDIT

### 1.1 What IS Already Implemented

#### Command Verbs (6/12)
- ✅ **Describe** — recall + observation; "what" questions; SAT descriptors
- ✅ **Explain** — cause → mechanism → effect; causal reasoning
- ✅ **Assess** — judgement + evidence; quality/readiness evaluation
- ✅ **Evaluate** — assessment with multiple criteria
- ✅ **Compare** — analytical comparison
- ✅ **Justify** — defense of position

**Location:** `knowledge/command-verbs/*.json` (describe.json, explain.json, etc.)  
**Structure:** cognitive_level, definition, expected_response (do/do_not), mark_expectation, mentor_hint

#### Open Response Items
- ✅ 20 active items (RA1-5)
- ✅ Per-item assessment_intelligence: concepts, causal chains, corpus grounding
- ✅ Frontend lab runtime (private, localStorage-only)
- ✅ Deterministic session selection (short/standard/extended/mock)

**Location:** `knowledge/question-bank/open_response/open_response_bank.json`  
**Frontend:** `frontend/open-response-lab/` (index.html + lab_payload.js)

#### Distinction Patterns
- ✅ **Descriptor patterns:** primary/secondary/tertiary categorization, specificity rules, quantity rules
- ✅ **Quality reasoning patterns:** excelente → muy_bueno → bueno → aceptable mapping to evidence
- ✅ **Readiness reasoning patterns:** potencial de guarda vs aging suitability
- ✅ **Response structures:** SAT ordering conventions, structural expectations

**Location:** `knowledge/distinction-patterns/` (4 JSON files)

#### Evaluation Pipeline
- ✅ **Concept detection:** normalized term matching (with alias expansion)
- ✅ **Causal link detection:** connector-word presence (porque, debido, leads, results, etc.)
- ✅ **Corpus grounding:** official chunk evidence matching (MIN_GROUNDING_TERMS=3)
- ✅ **Governance enforcement:** formative-only defaults, scoring-field rejection

**Location:** `tools/question_generation/open_response_pipeline.py`

#### Assessment Intelligence (Embedded in Frontend)
- ✅ **Command verbs** (6 verbs) — cognitive levels + do/do_not guidance
- ✅ **SAT quality levels** — 6-point scale (defectuoso → excelente)
- ✅ **Evidence requirements** — principles + strong patterns for "strong signal"
- ✅ **Common response failures** — 7 CRF patterns (false-positive signals)
- ✅ **Improvement patterns** — 6 IP patterns (from → to transitions)
- ✅ **Mentor hints** — context-specific guidance by topic

**Location:** `frontend/open-response-lab/lab_payload.js` (window.OPEN_RESPONSE_LAB_PAYLOAD)

---

### 1.2 What IS Partially Implemented

#### Command-Verb Compliance Evaluation
- ⚠️ **Current:** Basic presence/absence of concepts and causal language
- ⚠️ **Missing:** Does the answer actually *explain* (cause-effect chain) vs just *describe* (listing features)?
- ⚠️ **Missing:** Does the answer *assess* with explicit judgement statement + evidence order?
- ⚠️ **Gap:** No structural validation that response matches the verb's expected format

#### Descriptor Precision Evaluation (SAT-specific)
- ⚠️ **Current:** Presence of descriptors (any are counted equally)
- ⚠️ **Missing:** Category assignment (is "vanilla" correctly identified as secondary/oak vs error)?
- ⚠️ **Missing:** Specificity check (are descriptions specific "red cherry" vs generic "fruity")?
- ⚠️ **Missing:** Quantity rules (3-5 primaries is optimal; too many/too few = mark loss)

#### Quality Reasoning Evaluation (Distinction requirement)
- ⚠️ **Current:** Presence of "excelente/muy_bueno/etc" keywords
- ⚠️ **Missing:** Evidence-to-quality mapping (does excelente truly follow from pronounced intensity + all three aroma categories)?
- ⚠️ **Missing:** Quality justification validation (is the quality level supported by stated observations?)

---

### 1.3 What IS Missing Entirely

#### Command Verbs (6 missing out of 12 total)
1. ❌ **Why** — causal questioning; more compressed than "Explain"
2. ❌ **How** — mechanism or process; sequential steps
3. ❌ **Discuss** — balanced exploration of multiple perspectives
4. ❌ **Identify and Explain** — dual: spot the thing + explain it
5. ❌ **Outline** — structured summary; main points only
6. ❌ **State** — brief factual statement; minimal elaboration
7. ❌ **List** — enumeration; no explanation required

**Impact:** Students receive no guidance on verbs used in ~50% of WSET Level 3 questions

#### Multi-Dimensional Evaluation Architecture
- ❌ No separation of:
  - **A. Content correctness** (right concepts, accurate causal logic)
  - **B. Structural correctness** (expected format for the verb)
  - **C. Command-verb compliance** (does the answer actually *do* what the verb asks?)
  - **D. Distinction-chain completeness** (for SAT: full categorization + quality reasoning)

**Current:** All lumped into "concept_coverage" + "causal_link" presence  
**Missing:** Diagnostic feedback that says *why* marks were lost (concept vs structure vs verb-mismatch)

#### Universal Distinction Chain (SAT-specific)
- ❌ **Appearance layer:** color, clarity, condition assessment
- ❌ **Nose layer:** aromatics with correct intensity + development timing
- ❌ **Palate layer:** flavor integration, acid/tannin/alcohol balance, persistence
- ❌ **Quality reasoning:** evidence-mapped quality level (using Nazareth patterns)
- ❌ **Readiness assessment:** ageing potential justified by structure

**Current:** No structured template validation for SAT responses  
**Missing:** Learners don't know the expected cognitive sequence (appearance → nose → palate → quality → readiness)

#### Learner Coaching via learner_intelligence.js
- ❌ No exported learner intelligence state (what does the system know about this learner's patterns?)
- ❌ No verb-specific coaching (common mistakes for "Explain" vs "Compare")
- ❌ No progression guidance (when is student ready for "Assess" vs "State"?)
- ❌ No distinction-chain pattern coaching (e.g., "You're identifying secondary aromas but missing tertiary — that's a distinction gap")

---

## PART 2: COMPARATIVE ANALYSIS

### 2.1 Command Verbs: Current vs Expected

| Verb | Cognitive Level | Current Support | Missing Support | Difficulty | Pedagogical Value |
|------|-----------------|-----------------|-----------------|------------|-------------------|
| **Describe** | Recall + observation | ✅ Full | — | Low | High (SAT foundation) |
| **Explain** | Comprehension + causal | ✅ Full | — | Medium | High (causal reasoning) |
| **Assess** | Evaluation + evidence | ✅ Partial | Evidence mapping; judgement placement | High | Critical (Distinction) |
| **Evaluate** | Evaluation + criteria | ✅ Partial | Multi-criterion weighing | High | High (strategic thinking) |
| **Compare** | Analytical comparison | ✅ Partial | Similarity + difference structure | Medium | High (contrast reasoning) |
| **Justify** | Defense + reasoning | ✅ Partial | Counter-argument acknowledgment | High | High (critical reasoning) |
| **Why** | Causal (compressed) | ❌ None | Causal reasoning without "explain" scaffold | Medium | Medium (foundational) |
| **How** | Mechanism + process | ❌ None | Step-by-step sequential logic | Medium | Medium (procedural) |
| **Discuss** | Balanced exploration | ❌ None | Multiple perspectives + weighing | High | Medium-High |
| **Identify + Explain** | Dual (spot + explain) | ❌ None | ID step + then explain step; 2-part validation | Medium | High (precision) |
| **Outline** | Structured summary | ❌ None | Hierarchical main points; no elaboration | Low | Medium (synthesis) |
| **State** | Brief factual | ❌ None | Single sentence; minimal elaboration allowed | Low | Low-Medium (concision) |
| **List** | Enumeration | ❌ None | Item enumeration; no explanation required | Low | Low (memory + recall) |

**Summary:** 6/12 verbs have infrastructure; 6/12 require schema, test contracts, and coaching.

---

## PART 3: GAP ANALYSIS & ARCHITECTURE PROPOSAL

### 3.1 Four-Dimensional Evaluation Model

All Open Response answers will be evaluated against **four independent dimensions**:

```
┌─────────────────────────────────────────┐
│  LEARNER ANSWER TEXT                    │
└──────────┬──────────────────────────────┘
           │
     ┌─────┴──────────────────────────┬───────────────┬──────────────────┐
     │                                │               │                  │
     ▼                                ▼               ▼                  ▼
┌─────────────────┐        ┌──────────────────┐ ┌──────────────┐  ┌──────────────┐
│ A. CONTENT      │        │ B. STRUCTURAL    │ │ C. COMMAND   │  │ D. DISTINCTION
│ CORRECTNESS     │        │ CORRECTNESS      │ │ VERB         │  │ CHAIN
│                 │        │                  │ │ COMPLIANCE   │  │ COMPLETENESS
│ • Concepts      │        │ • Expected       │ │              │  │
│   present?      │        │   format         │ │ • Did the    │  │ • Full SAT
│ • Causal        │        │ • Hierarchy      │ │   answer     │  │   sequence?
│   chain         │        │ • Completeness   │ │   actually   │  │ • Distinct
│   intact?       │        │ • Ordering       │ │   DESCRIBE?  │  │   layers?
│ • Aliases &     │        │ • Length         │ │   EXPLAIN?   │  │ • Descriptor
│   variants      │        │   expectations   │ │   ASSESS?    │  │   categories
│   recognized?   │        │                  │ │ • Missing    │  │   correct?
│                 │        │ (verb-specific)  │ │   verb-     │  │ • Quality-
│                 │        │                  │ │   specific   │  │   evidence
│                 │        │                  │ │   signals    │  │   alignment?
│ Formative       │        │ Formative        │ │              │  │
│ Output:         │        │ Output:          │ │ Formative    │  │ Formative
│ "Your answer    │        │ "For Explain,    │ │ Output:      │  │ Output:
│  includes:      │        │ you need a       │ │ "You        │  │ "Your SAT
│  altitude,      │        │ cause →          │ │ described    │  │ response
│  temperature"   │        │ mechanism →      │ │ (named       │  │ covers:
│                 │        │ effect chain.    │ │ features)   │  │ Appearance ✓
│                 │        │ Yours has: cause │ │ but didn't   │  │ Nose ✓
│                 │        │ only."           │ │ explain the  │  │ Palate ✓
│                 │        │                  │ │ mechanism."  │  │ Quality ✓
│                 │        │                  │ │              │  │ Readiness ✗"
└─────────────────┘        └──────────────────┘ └──────────────┘  └──────────────┘
```

#### A. Content Correctness
**What:** Are the right concepts present? Is causal reasoning sound?

- **Concept detection:** normalized term matching + alias expansion (current)
- **Causal connector validation:** "porque", "debido", "conduce", "results", etc. (current)
- **Concept state:** present / partially_present / absent (current)
- **NEW:** Causal chain integrity — does the chain actually follow the mechanism?

**Formative Feedback Example:**
```
Content Coverage:
  ✓ altitude [present]
  ✓ temperature [present]
  ✓ causal connector: "resulta en" [found]
  ✗ final structure/complexity [absent — needed to complete chain]
  
Causal Logic:
  → altitude affects [OK]
  → cooler temperature implied [OK]
  ✗ missing final outcome: how does lower temp affect final wine structure?
```

---

#### B. Structural Correctness
**What:** Does the answer match the expected format/structure for this question type?

- **RA-specific expectations:** e.g., SAT responses have appearance → nose → palate → quality
- **Verb-specific format:** e.g., "Assess" requires judgement statement FIRST, then evidence
- **Causal structure:** "Explain" expects cause → mechanism → effect chain (linear or branched)
- **Completeness check:** are all required components present?

**Formative Feedback Example:**
```
Structure Check for SAT Response:
  ✓ Appearance section found
  ✓ Nose section found
  ✓ Palate section found
  ✓ Quality assessment section found
  ✗ Readiness/aging potential section missing

Verb Structure for "Explain":
  ✓ Cause stated: "cool climate"
  ✓ Mechanism stated: "slower ripening"
  ✗ Effect statement incomplete: "higher acidity" alone is not enough — needs complexity/balance effects too
```

---

#### C. Command-Verb Compliance
**What:** Did the answer actually *do* what the verb asked it to do?

- **Describe:** Lists features without explanation? ✓ Correct. Includes "because" clauses? ✗ Over-explained.
- **Explain:** Includes cause → effect? ✓ Correct. Mechanism explained? ✗ Missing.
- **Assess:** Judgement stated first + evidence follows? ✓ Correct. Judgement supported by evidence? ✗ No.
- **Compare:** Shows both similarity AND difference? ✓ Correct. One-sided comparison? ✗ Incomplete.

**Key distinction:** A structurally sound answer might still *fail* verb compliance if it doesn't answer the command.

**Formative Feedback Example:**
```
Verb Compliance Check for "Explain":
  Asked: "Explain why cool climates produce higher acidity."
  Your answer structure: Describe → State outcome
  ✓ You correctly identified: cool climate → higher acidity
  ✗ You did not explain the mechanism
  Missing: How does lower temperature CAUSE higher acidity?
  Example of mechanism: "Lower temperatures slow yeast fermentation, leaving more unfermented malic acid in the final wine."
```

---

#### D. Distinction-Chain Completeness
**What:** For SAT/premium wines, is the Distinction chain complete?

**SAT Distinction Chain (Universal):**
1. **Appearance:** Color + clarity + condition (e.g., "pale gold, clear, still")
2. **Nose:** Intensity + development + aroma category specificity (primary/secondary/tertiary)
3. **Palate:** Structural elements (acid/tannin/alcohol/body) + balance + finish
4. **Quality Reasoning:** Evidence-mapped level (excelente/muy_bueno/etc) with supporting observations
5. **Readiness Assessment:** Aging potential justified by structure (if applicable)

**NEW Components to Evaluate:**
- **Descriptor categorization:** Is "vanilla" correctly ID'd as oak (secondary)?
- **Descriptor precision:** "Red cherry" vs generic "fruity"?
- **Quality-evidence alignment:** Does "excelente" follow from "pronounced intensity + complex 3-layer aromas"?
- **Readiness patterns:** Is aging claim supported by tannin + acid profile?

**Formative Feedback Example:**
```
Distinction Chain Check (SAT):
  Appearance: ✓ Complete (pale gold, clear)
  Nose: 
    ✓ Intensity stated: "medium(+)"
    ✓ Primary aromas: "red cherry, raspberry" [specific, correct]
    ✓ Secondary: "vanilla, cedar" [correct attribution to oak]
    ✗ Tertiary aromas missing [gap: no bottle-aged character mentioned]
  Palate:
    ✓ Acid: "lively"
    ✓ Tannin: "firm but integrated"
    ✓ Balance: "harmonious"
  Quality Assessment:
    ✗ Quality level selected: "muy bueno"
    ✗ But your evidence shows: all three aroma categories + balance
    ✓ This actually supports "excelente" quality level
    Suggestion: Revise quality assessment upward; your tasting notes justify it
  Readiness:
    ✗ Not addressed. Aging potential claim missing given the structure present.
```

---

### 3.2 Architecture for 12 Command Verbs

**File:** `knowledge/command-verbs/[verb].json` (schema expansion)

Each verb will have:
```json
{
  "verb": "explain|describe|assess|...",
  "cognitive_level": "string",
  "definition": "string",
  "used_in_ras": ["RA1", ...],
  "expected_response": {
    "format": "cause → mechanism → effect chain",
    "structure": "linear | branched | hierarchical",
    "do": ["list of expected behaviors"],
    "do_not": ["list of violations"]
  },
  "compliance_checks": {
    "required_signals": ["porque", "debido", ...],  // what MUST appear
    "forbidden_signals": ["opinion", "always", ...], // what MUST NOT appear
    "structure_rules": {
      "minimum_components": 3,  // cause, mechanism, effect
      "component_order": ["cause", "mechanism", "effect"],
      "elaboration_required": true
    }
  },
  "mark_expectation": "string",
  "mentor_hints": ["list of specific coaching tips"]
}
```

---

### 3.3 Evaluator Architecture

**File:** `tools/question_generation/open_response_evaluator.py` (new module)

```python
def evaluate_answer_multi_dimensional(
    answer_text: str,
    expected_concepts: list[str],
    optional_causal_chain: str,
    command_verb: str,
    response_type: str,  # "short_answer" | "sat_full"
) -> dict:
    """Return 4-dimensional evaluation without claiming to be an examiner."""
    
    return {
        "content_correctness": {
            "concepts_detected": [...],
            "concepts_missing": [...],
            "causal_chains_found": [...],
            "causal_integrity": "intact | partial | broken",
            "feedback": "Human-readable formative text"
        },
        
        "structural_correctness": {
            "expected_format": "SAT | causal_chain | comparative | ...",
            "components_found": [...],
            "components_missing": [...],
            "component_ordering": "correct | incorrect",
            "length_expectation": "met | below | above",
            "feedback": "Human-readable formative text"
        },
        
        "command_verb_compliance": {
            "verb_requested": "explain",
            "verb_definition": "Give reasons; show cause-effect",
            "signals_found": ["porque", "resulta"],
            "signals_missing": ["mechanism"],
            "compliance_status": "full | partial | non-compliant",
            "feedback": "Human-readable coaching specific to the verb"
        },
        
        "distinction_chain_completeness": {
            "response_type": "sat_full",
            "appearance_section": {"present": true, "coverage": "complete | partial"},
            "nose_section": {"present": true, "descriptor_categories": {...}},
            "palate_section": {"present": true, "balance_assessment": true},
            "quality_assessment": {
                "level_selected": "muy_bueno",
                "evidence_alignment": "correct | misaligned",
                "justification_present": true
            },
            "readiness_assessment": {"present": false, "required": true},
            "feedback": "Human-readable distinction-specific coaching"
        },
        
        "overall_formative_guidance": {
            "strengths": ["list of what went well"],
            "gaps": ["list of improvement targets"],
            "next_focus": ["ranked coaching suggestions"],
            "safe_for_examiner": false,
            "examiner_scoring_allowed": false
        }
    }
```

---

## PART 4: IMPLEMENTATION PHASES

### Phase P2.1: Command Verb Infrastructure (Weeks 1-2)
- [ ] Create JSON schemas for all 12 verbs (extend command_verbs/*.json)
- [ ] Add `compliance_checks` and `structure_rules` to each verb
- [ ] Write test suite: `tests/test_command_verb_definitions.py`
- [ ] No evaluator changes yet; just schema + tests

**Quick Win:** All 12 verb definitions available in payload for frontend coaching

---

### Phase P2.2: Multi-Dimensional Evaluator (Weeks 3-4)
- [ ] Implement `open_response_evaluator.py` with 4-dimensional eval
- [ ] Separate concept/causal detection (existing) from structural/verb validation (new)
- [ ] Add Distinction-chain validation for SAT responses
- [ ] Write comprehensive test suite: `tests/test_open_response_evaluator.py`

**Quick Win:** Evaluator produces formative feedback across all 4 dimensions

---

### Phase P2.3: Frontend Integration (Weeks 5-6)
- [ ] Update `lab_payload.js` to include all 12 command verb details
- [ ] Wire evaluator output to frontend feedback display (multi-tab or progressive disclosure)
- [ ] Add verb-specific coaching hints in sidebar
- [ ] Update learner_intelligence.js to track verb-compliance patterns

**Quick Win:** Frontend displays 4-dimensional feedback with verb-specific guidance

---

### Phase P2.4: Item Expansion (Weeks 7-8)
- [ ] Identify 10-15 new open-response candidates from structured bank
- [ ] Map each to command verb + expected structure
- [ ] Validate via `open_response_pipeline.py` (existing)
- [ ] Build expanded `lab_payload.js` (20 → 35-40 items)

**Quick Win:** 35-40 high-quality OR items with full verb coverage

---

### Phase P2.5: Distinction-Chain Coaching (Weeks 9-10)
- [ ] Create `knowledge/distinction-patterns/sat_chain_templates.json` (universal SAT structure)
- [ ] Add SAT-specific test suite: `tests/test_sat_distinction_validation.py`
- [ ] Enable descriptor categorization feedback (primary/secondary/tertiary)
- [ ] Integrate quality-evidence alignment validation (Nazareth patterns)

**Quick Win:** SAT responses receive structured distinction-chain feedback

---

## PART 5: HIGH-IMPACT FEATURES (Short Term)

### 5.1 Verb-Specific Coaching Sidebars
**What:** When student sees "Explain this mechanism," show:
```
HOW TO EXPLAIN:
• State what causes the outcome [Factor]
• Describe the process [Mechanism]
• Name the result [Effect]

EXAMPLE for "acidity in cool climates":
  Cool temperatures → slow ripening → more malic acid retained → higher final acidity

✓ GOOD: You explained all three steps
✗ TRY: Make the mechanism more explicit. You said "less sugar" but the key is WHY that leaves more acid.
```

**Implementation:** Frontend sidebar driven by `command_verb[verb].mentor_hints` + evaluator feedback

---

### 5.2 Distinction Gap Highlighting
**What:** For SAT responses, flag missing layers:
```
YOUR SAT RESPONSE COVERS:
  ✓ Appearance
  ✓ Nose (primary + secondary)
  ✓ Palate
  ✓ Quality Assessment
  ✗ READINESS — Missing for a premium wine

WHAT COUNTS: Aging potential should be justified by structure:
  - This wine shows: firm tannin, good acidity → can age 5-10 years
  - You tasted that, but didn't connect it to potential.
```

**Implementation:** `distinction_chain_completeness` evaluator output → frontend highlighting

---

### 5.3 Learner Intelligence Profile
**What:** Track patterns in learner's verb usage:
```
YOUR PATTERN:
• Describe: 4/5 high-precision ✓
• Explain: 2/5 missing mechanism step ✗
• Assess: 3/5 quality-evidence mismatch ✗
• Compare: 0 attempts

RECOMMENDATION:
  1. Practice "Explain" with mechanism focus
  2. Practice "Assess" to align quality with evidence
  3. Try "Compare" for your next question
```

**Implementation:** Session ledger + pattern analysis in `learner_intelligence.js`

---

### 5.4 Descriptor Precision Coaching (SAT-Specific)
**What:** Real-time feedback on descriptor accuracy:
```
YOU WROTE: "fruity nose"
FEEDBACK: Too generic for SAT. Level up:
  Generic: fruity, floral, fresh
  Precise: red cherry, honeysuckle, green apple
  
  Why? Mark allocation favors specificity.
  Example: "red cherry, raspberry, violet" = 3 marks
           "fruity, fresh" = 0 marks for precision

YOUR SCORE THIS QUESTION:
  ✓ Three aromas listed
  ✗ Only one was specific
  NEXT: Try all specific, no generic wrappers
```

**Implementation:** Descriptor pattern validation in evaluator; frontend comparison display

---

## PART 6: RISK & GOVERNANCE

### 6.1 Safety Invariants (Non-Negotiable)
```python
safe_for_examiner = False                    # Never set to True
examiner_scoring_allowed = False             # No marks, grades, percentages
uses_llm = False                             # Deterministic only
uses_api = False                             # No external calls
uses_embeddings = False                      # No embeddings
uses_vector_db = False                       # No vector DB
cloud_services_active = False                # All local
```

**Enforcement:** All evaluator output must pass `validate_formative_output()` which rejects any scoring language.

---

### 6.2 Formative-Only Language Contract
**Allowed:**
- "Your answer includes X"
- "You're missing Y"
- "The mechanism step could be more explicit"
- "For distinction, you'd need Z"

**Forbidden:**
- "Mark: 7/10"
- "You would pass"
- "This is worth 15 marks"
- "Examiner assessment: adequate"
- "WSET equivalent: Band 3"

**Enforcement:** Regex + semantic check in evaluator; test suite catches violations

---

## PART 7: TESTING STRATEGY

### Test Suites Required
1. **test_command_verb_definitions.py** — Schema validation, mentor hints completeness
2. **test_open_response_evaluator.py** — 4-dimensional output structure, no scoring language
3. **test_sat_distinction_validation.py** — Appearance/Nose/Palate/Quality/Readiness detection
4. **test_descriptor_categorization.py** — Primary/Secondary/Tertiary classification accuracy
5. **test_verb_compliance.py** — Does output correctly flag verb mismatches?
6. **test_formative_language_safety.py** — Forbidden words regex + semantic checks

**Coverage Target:** 95%+ on evaluator output; 100% on governance checks

---

## PART 8: IMPLEMENTATION DEPENDENCIES

**Required (already exist):**
- ✅ `knowledge/command-verbs/*.json` (6 verbs exist; extend to 12)
- ✅ `knowledge/distinction-patterns/` (4 pattern files)
- ✅ `tools/question_generation/open_response_pipeline.py` (concept/causal detection)
- ✅ `frontend/open-response-lab/` (runtime exists)

**To Create:**
- ❌ `tools/question_generation/open_response_evaluator.py` (NEW)
- ❌ `knowledge/command-verbs/[why|how|discuss|identify_explain|outline|state|list].json` (6 NEW)
- ❌ `knowledge/distinction-patterns/sat_chain_templates.json` (NEW, optional)

**To Modify (Minimal):**
- ⚠️ `tools/question_generation/open_response_lab_runtime.py` — call new evaluator
- ⚠️ `frontend/open-response-lab/lab_payload.js` — include 12 verbs + expanded intelligence
- ⚠️ `tests/test_open_response_lab_runtime_mvp.py` — extend for 4-dimensional output

---

## PART 9: QUICK WINS (Can Ship in Week 1)

1. **Define all 12 command verbs** — Create remaining 6 JSON files with mentor hints
   - Impact: Immediate coaching availability for all verbs
   - Effort: 2-3 hours
   - No backend changes needed

2. **Add verb definitions to frontend** — Extend lab_payload with full verb intelligence
   - Impact: Students see cognitive level + do/do_not for every verb
   - Effort: Frontend JS work only
   - Risk: None (read-only, no eval changes)

3. **Descriptor pattern validator** — Validate primary/secondary/tertiary categorization
   - Impact: SAT students get real-time descriptor feedback
   - Effort: 200 lines in evaluator
   - Risk: Low (formative only)

---

## PART 10: SUCCESS CRITERIA

### By End of Phase P2 (Week 10)
- [ ] All 12 command verbs documented with compliance schemas
- [ ] 4-dimensional evaluator implemented + tested (95%+ coverage)
- [ ] 35-40 OR items active with full verb coverage
- [ ] Frontend displays multi-dimensional feedback
- [ ] SAT distinction chain validation working
- [ ] Zero governance violations detected (100% formative language)
- [ ] Learner intelligence tracking verb-compliance patterns

### Qualitative (User-Facing)
- [ ] Student can see why they lost marks on "Explain" (missing mechanism)
- [ ] Student can see SAT distinction gaps (e.g., "no tertiary aromas identified")
- [ ] Student receives verb-specific coaching (not generic feedback)
- [ ] Student tracks improvement across verb types (patterns over sessions)

---

## PART 11: DECISION TREE & RECOMMENDATIONS

```
DO WE HAVE ENOUGH INFRASTRUCTURE TO START?
  → Yes. All building blocks exist (verbs, patterns, evaluator skeleton).

SHOULD WE EXPAND ITEMS FIRST OR EVALUATOR FIRST?
  → Evaluator first. Items are wasted without dimensioned feedback.

SHOULD WE IMPLEMENT ALL 12 VERBS OR START WITH 6?
  → Start with JSON schemas for all 12 (low effort); implement evaluator for current 6 verbs.
    Add new verb eval as items require them.

SHOULD WE IMPLEMENT LEARNER INTELLIGENCE STATE?
  → Yes, but async. Prototype with simple pattern tracking (verb-by-verb success rate).
    Save full state machine for Phase P3.

SHOULD WE WORRY ABOUT DISTINCTION-CHAIN TEMPLATES NOW?
  → Optional for Phase P2. Current distinction-patterns are sufficient.
    Add sat_chain_templates.json if Phase P2.5 has budget.
```

---

## CONCLUSION

Open Response is ready for Phase P2. The infrastructure (verbs, patterns, items, coaching) exists.

**Next step:** Implement the `open_response_evaluator.py` 4-dimensional architecture, starting with content + structural correctness (existing logic) and adding command-verb compliance validation (new).

**Timeline:** 8-10 weeks from design to 35-40 active items with full verb-compliance + distinction-chain feedback.

**Risk level:** Low. All changes are formative-only, governance-safe, and backward-compatible with current 20-item lab.

---

*End of Phase P2 Architecture Document*

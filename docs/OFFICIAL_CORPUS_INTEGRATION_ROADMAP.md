# Official Corpus Integration Roadmap
**Phase:** V4.3 Part 4  
**Date:** 2026-06-09

---

## Current Utilization Baseline

| Family | Current level | Runtime consumers |
|--------|--------------|------------------|
| Study guide | USED (52 chunks, retrieval-boosted) | tutor_retrieval_sandbox |
| Specification | NOT USED | none |
| SAT | NOT USED | none |
| Marking keys | NOT USED | none |
| Model answers | NOT USED | none |
| Phase X.1 JSON assets | NOT USED | none |

---

## Family-by-Family: Missed Opportunities and Highest-Value Integration

---

### 1. Specification

**Current utilization:** Stored as Markdown. Not loaded.

**Missed opportunities:**
- RA-specific learning objective dispatch (the system routes by RA but cannot validate that questions match RA learning outcomes)
- Command verb awareness (the system has no mechanism to check whether a question stem uses an appropriate command verb for its cognitive level)
- MCQ allocation validation (no way to verify that question distribution across RAs matches the real exam blueprint: RA1=8, RA2=28, RA3=5, RA4=5, RA5=4)

**Highest-value integration point: Assessment Blueprint Validator**

Load `knowledge/assessment-framework/learning_outcomes.json` and `assessment_structure.json` into the question bank eligibility layer. Use RA learning outcomes to validate that items are testing the correct cognitive level for their RA. Use MCQ allocation to detect over/under-representation in active sessions.

Effort: Low (data already extracted). Impact: High (exam-aligned session composition).

---

### 2. SAT

**Current utilization:** Stored as Markdown. Not loaded.

**Missed opportunities:**
- SAT answer validation (the open response evaluator has no SAT-aware schema to check against)
- Descriptor category assignment (learners using non-SAT vocabulary receive no correction signal)
- Scale validation (no check that tasting observations use the correct ordinal scale values)

**Highest-value integration point: SAT Answer Validator**

Wire `knowledge/sat-framework/sat_structure.json` and `sat_scales.json` into the open response evaluator. When a learner submits a SAT answer, check: are all required elements present? are scale terms correct? are descriptors categorised correctly (primary/secondary/tertiary)?

This is the highest-value single integration because the SAT is the entirety of Unit 2 and the open response evaluator currently has no structural awareness of it.

Effort: Medium (requires wiring into open_response_evaluator). Impact: Very high (Unit 2 support).

---

### 3. Marking Keys

**Current utilization:** Stored as Markdown. Not loaded.

**Missed opportunities:**
- Mark allocation awareness (the open response evaluator does not know that white wine = 20 marks, red = 21)
- Simple wine exception enforcement (no system currently flags that a learner inventing tertiary aromas for a simple wine is making a structural error)
- Section-level feedback (the evaluator cannot identify that a learner is strong on nose but weak on palate conclusions because it has no mark-section model)

**Highest-value integration point: SAT Mark Allocation Model**

Load `knowledge/evaluator-framework/mark_allocation_rules.json` into the open response evaluator. Use section mark allocations to weight feedback by section. Flag simple wine exception violations.

Effort: Low-medium (data clean and structured). Impact: High for Unit 2 feedback quality.

---

### 4. Model Answers

**Current utilization:** Stored as Markdown. Not loaded.

**Missed opportunities:**
- Distinction-level response benchmarking (no learner answer is currently compared against what 20/20 and 21/21 look like)
- Descriptor specificity guidance (no system currently tells a learner "red cherry is better than fruit")
- Quality justification patterns (the evaluator does not know that outstanding quality requires all three aroma categories)

**Highest-value integration point: Distinction Pattern Mentor**

Load `knowledge/distinction-patterns/` files into the mentor layer. After a learner's SAT response, compare against model answer quality reasoning patterns and descriptor specificity rules. Provide targeted formative feedback: "your nose section lists only primary aromas — a distinction-level answer would also identify secondary complexity from oak/MLF."

Effort: Medium (mentor layer exists but is not wired). Impact: Very high (distinction gap closure).

---

## Priority Matrix

| Integration | Effort | Pedagogical impact | Governance risk |
|-------------|--------|--------------------|-----------------|
| SAT Answer Validator | Medium | Very high | Low |
| Distinction Pattern Mentor | Medium | Very high | Low |
| Assessment Blueprint Validator | Low | High | Low |
| SAT Mark Allocation Model | Low-medium | High | Low |
| Command Verb Layer in question generation | Low | Medium | Low |

---

## Recommended Integration Sequence

1. **SAT Answer Validator** — highest impact; addresses Unit 2 blind spot entirely
2. **SAT Mark Allocation Model** — prerequisite for section-level feedback; low incremental effort
3. **Distinction Pattern Mentor** — mentor layer wire-up; reuses Phase X.1 assets directly
4. **Assessment Blueprint Validator** — session composition quality; exam-alignment signal
5. **Command Verb Layer** — question generation QA; lower urgency

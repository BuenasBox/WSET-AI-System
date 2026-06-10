# Next Phase Recommendation
**Phase:** V4.3 Part 5  
**Date:** 2026-06-09

---

## Recommendation: SAT Answer Validator (Phase X.2)

---

## Rationale

The V4.3 audit revealed a structural gap: Unit 2 (the SAT tasting exam — 50% of the qualification) has no runtime intelligence layer. The system can deliver SAT questions and receive free-text answers, but it cannot:

- Verify structural completeness (are all 9 palate elements covered?)
- Check scale correctness (did the learner use a valid ordinal term?)
- Detect descriptor category errors (is honey marked as primary?)
- Validate quality justification (did the learner support Outstanding with specific evidence?)
- Flag the simple wine exception (did the learner waste marks inventing tertiary aromas for a simple wine?)

This gap is not a data gap — all the knowledge required was extracted in Phase X.1 and is sitting in `knowledge/sat-framework/`, `knowledge/evaluator-framework/`, and `knowledge/distinction-patterns/` as structured JSON. The gap is a **wire-up gap**.

Closing this gap unlocks feedback for the most mark-dense part of the qualification. The SAT is not peripheral — it is the entire second unit.

---

## What Phase X.2 Would Deliver

1. **SAT structural validator** — `tools/tutor/sat_validator.py` — deterministic check of SAT response completeness against `sat_structure.json`; returns missing elements, invalid scale terms, descriptor category misassignments
2. **Mark allocation feedback** — uses `mark_allocation_rules.json` to identify which sections are strong vs. weak
3. **Simple wine exception enforcer** — detects and flags the single most common structural error in WSET tasting assessments
4. **Quality justification checker** — uses `quality_reasoning_patterns.json` to verify that quality level is supported by specific tasting observations
5. **Distinction gap report** — compares learner descriptor specificity against `descriptor_patterns.json`

All components: deterministic, zero LLM, zero API, governance-clean, unit-testable.

---

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Examiner authority creep | Medium | All output labelled "formative guidance only"; no marks assigned; `safe_for_examiner: false` enforced |
| Overclaim on correctness | Low | Validator flags structural issues only; does not score flavour accuracy (which requires a real examiner) |
| SAT schema drift | Low | Schema is versioned (`sat_structure_v1`); unit tests lock it |
| Open response evaluator coupling | Low | Validator is a standalone module; wired into evaluator as optional enrichment layer |

---

## Expected Pedagogical Impact

- **Unit 2 learners** gain structural feedback they currently receive nowhere in the system
- **Distinction gap** becomes visible and addressable: a learner currently at Pass level can see exactly what a Distinction-level SAT answer looks like structurally
- **Simple wine exception** — one of the most costly structural errors in WSET tasting exams — is caught automatically
- **Mentor hints** (`knowledge/mentor-framework/`) can be triggered by validator findings, closing the feedback loop

---

## Why Not the Alternatives?

| Alternative | Why lower priority |
|-------------|-------------------|
| Ollama Integration | Violates `uses_llm: false` governance invariant — not permitted without explicit authorization |
| Retrieval Expansion | Retrieval already functional and well-tested; marginal gain vs. SAT gap |
| Dashboard Improvements | UX enhancement; does not close pedagogical gaps |
| Bank Activation (83 approved_private_sba items) | Operational decision, not engineering; can proceed in parallel |
| Command Verb Layer | Lower urgency; MCQ question generation QA rather than learner feedback |

---

## Entry Criteria for Phase X.2

Before implementation:
1. Confirm `knowledge/sat-framework/sat_structure.json` and `sat_scales.json` are frozen
2. Confirm `knowledge/evaluator-framework/mark_allocation_rules.json` is frozen  
3. Confirm `knowledge/distinction-patterns/` files are frozen
4. Confirm `ENABLE_PEDAGOGICAL_STRATEGY_LAYER = False` (PSL remains disconnected)
5. Agree: validator is formative only; no scoring authority language in any output

---

## Summary

Phase X.2 — SAT Answer Validator closes the single largest pedagogical gap in the current system. The data is already extracted, the governance is clear, the risk is low, and the impact is high. It is the natural next phase.

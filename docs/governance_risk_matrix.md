# Governance Risk Matrix
## WSET-AI-System — Phase 1 Audit

**Auditor:** Claude (Cowork) — Full System Audit
**Date:** 2026-05-15
**Scope:** Governance framework, agent boundary enforcement, trust tier consistency, contamination risk, calibration readiness
**Evidence base:** AGENT_BOUNDARIES.md, SEMANTIC_RETRIEVAL_ARCHITECTURE.md, agent prompts, corpus inspection

---

## 1. Governance Framework Maturity Assessment

The governance framework, primarily defined in `AGENT_BOUNDARIES.md`, is the most mature artifact in this system. It is technically rigorous, epistemologically sound, and operationally specific. The trust tier system, calibration gate, scoring authority ladder, and agent separation rules are all correctly designed.

However, a governance framework is only as strong as its enforcement. The audit distinguishes between **documented rules** and **active enforcement**.

| Governance dimension | Documentation quality | Active enforcement | Gap |
|---|---|---|---|
| Tutor/Examiner source separation | ✅ Excellent | ⚠️ Partial — no corpus enforcement yet | Medium |
| Trust tier assignment at ingestion | ✅ Excellent | ❌ Not running — no ingestion pipeline active | High |
| Calibration gate (§6.2) | ✅ Excellent | ❌ Gate never executed | High |
| Anti-contamination filters | ✅ Excellent | ⚠️ Designed but not implemented in code | High |
| Mandatory disclosure on Examiner output | ✅ Excellent | N/A — Examiner not yet activated | N/A |
| Human review cadence | ✅ Specified | ❌ No review has occurred yet | High |
| Logging and auditability | ✅ Excellent | ❌ No logging infrastructure exists | High |

---

## 2. Risk Register — Updated

### R01 — Official Source Currency (MEDIUM / CRITICAL)

**Risk:** Official WSET source is outdated when a new edition is released.
**Current status:** The study guide (`WSET_L3_Study_Guide_Official_2026.pdf`) is the 2026 edition — current as of audit date. Specification is a `.gitkeep` placeholder — **not yet processed**.
**Mitigation gap:** Annual review cadence is documented but not scheduled. Version-lock policy has no implementation.
**Recommendation:** Process the specification PDF now. Record ingestion date. Set a calendar reminder for 2027 review.

### R02 — Examiner Corpus Contamination (LOW / CRITICAL)

**Risk:** Examiner Agent RAG retrieves Tier 3+ content due to misconfiguration.
**Current status:** Examiner corpus is empty. No contamination is possible today because no ingestion has occurred.
**Mitigation gap:** Hard corpus filter (EX-02) and contamination logging are specified but not implemented. When ingestion begins, these must be the first safeguards activated.
**Recommendation:** Do not begin Examiner corpus ingestion until `agent_corpus` filtering is implemented and tested. Treat the calibration gate as a genuine blocker, not documentation.

### R03 — Learner Conflates Practice Score With Official (MEDIUM / HIGH)

**Risk:** A learner receives a practice score and interprets it as an official WSET result.
**Current status:** Examiner Agent is not activated. Risk is latent, not active.
**Mitigation gap:** Mandatory disclosure language is in the Examiner prompt but has never been rendered to a user.
**Recommendation:** When activating the Examiner Agent, add a UI-level (not just prompt-level) disclaimer. Prompt injections can suppress prompt-level disclosures; UI disclaimers cannot be suppressed.

### R04 — Wine With Jimmy Content Accuracy (MEDIUM / MEDIUM)

**Risk:** Wine With Jimmy content contains factual errors or WSET L3 inaccuracies.
**Current status:** Content is in the Tutor corpus and actively retrieved. No human factual review of Jimmy corpus against WSET L3 specification has occurred.
**Mitigation gap:** No WSET-qualified review of pedagogical content has been performed. "Trust tier: pedagogical" does not mean the content is accurate — it means it is not authoritative.
**Recommendation:** Conduct a spot-check review of 20–30 golden chunks against WSET L3 specification. Flag any content where Jimmy's framing diverges from official language.

### R05 — Calibration Manifest Missing (HIGH / HIGH)

**Risk:** Calibration manifest not maintained; Examiner Agent cannot be safely activated.
**Current status:** `knowledge/calibration/` contains only a `.gitkeep`. No `calibration_manifest.json` exists. The calibration gate (AGENT_BOUNDARIES.md §6.2) explicitly requires this manifest before Examiner activation.
**Mitigation gap:** This is not a risk — it is a current deficiency. The Examiner Agent MUST NOT be activated without this manifest.
**Recommendation:** Create the manifest structure now. When the first marking key is processed, run the gate checklist. Do not bypass.

### R06 — Prompt Injection Via Learner Input (LOW / HIGH)

**Risk:** A student inputs a prompt injection attempt that reaches the Examiner Agent.
**Current status:** Orchestrator prompt includes source boundary rules but no explicit sanitisation step. The Examiner Agent system prompt does not include injection-detection language.
**Mitigation gap:** Input sanitisation is mentioned in the architecture (§13.1) but is not implemented.
**Recommendation:** Add explicit anti-injection instructions to the Examiner Agent system prompt. Log any user turn that contains system-prompt-style language.

### R07 — Diploma Content in L3 Corpus (MEDIUM / MEDIUM)

**Risk:** Wine With Jimmy Diploma-level content introduces concepts, regulations, or detail levels that exceed WSET L3 scope, producing over-complex Tutor explanations.
**Current status:** Multiple Diploma-level Wine With Jimmy videos are in the indexed corpus (e.g., "WSET Diploma D3 Introduction to Chianti", "Exploring Australian Climate and Geology for WSET Level 4"). The exclusion rule EX-07 ("diploma_enrichment without explicit L3 downgrade tag → exclude for Examiner Agent") is specified but not implemented.
**Mitigation gap:** No `wset_level` filter is applied at retrieval time for the Tutor Agent. Diploma content is retrieved alongside L3 content.
**Recommendation:** Add `wset_level: 3` metadata to all chunks at ingestion. Apply a soft downgrade rule: Diploma chunks can be included in Tutor retrieval but must be flagged and receive a 0.10 score penalty.

### R08 — Nazareth Data Isolation (LOW / HIGH — LATENT)

**Risk:** Learner data leaked across different learner profiles.
**Current status:** Nazareth is empty — no learner data exists. Risk is latent.
**Mitigation gap:** Per-learner isolation is designed but not implemented. When multi-learner support is added, this must be enforced at the file system and query level.
**Recommendation:** Before enabling multi-learner mode, implement learner ID validation on every Nazareth read/write operation.

### R09 — WSET Specification Not Processed (HIGH / HIGH — ACTIVE GAP)

**Risk:** The Tutor Agent is providing explanations without access to official WSET specification text.
**Current status:** `knowledge/official-wset/specification/` contains only a `.gitkeep`. The WSET L3 specification is a critical Examiner corpus source and a Tutor corpus reference. It has not been processed.
**Mitigation gap:** This is an active deficiency, not a future risk. The Examiner Agent specification states that the WSET specification is its "primary authority" — but this authority is not available.
**Recommendation:** Process the specification PDF immediately after the study guide extraction is validated. This is the single highest-priority governance action.

### R10 — System Implies Official WSET Endorsement (LOW / CRITICAL)

**Risk:** A user believes this system carries WSET endorsement or produces official results.
**Current status:** No UI exists yet. Risk is latent. All prompts include appropriate disclaimers.
**Mitigation gap:** Disclaimer enforcement is only at the prompt level. No legal review has occurred.
**Recommendation:** When any learner-facing interface is built, include a non-dismissible disclaimer on every session start.

---

## 3. Weak Enforcement Points

### The calibration gate is documented but not enforced by code

The calibration gate (§6.2) lists a checklist of required steps before Examiner Agent activation. This checklist exists as prose in a markdown file. There is no automated enforcement — no system check that requires the manifest to be present before the Examiner Agent starts, and no automated hash verification of calibration documents.

**Risk:** A developer activates the Examiner Agent without completing the gate. The gate is bypassed by omission, not by malice.

**Recommendation:** Implement the gate as a startup validation check: the Examiner Agent should fail to initialize if `calibration_manifest.json` does not exist or does not contain at least one entry with `approved_for_examiner_agent: true`.

### Trust tier assignment is manual and undocumented for ingested content

The governance model specifies that trust tier is assigned at ingestion time. The Wine With Jimmy corpus has been ingested, but there is no documented trust tier assignment record for individual files. The retrieval sandbox shows `trust_tier` values implicitly (Wine With Jimmy is treated as pedagogical), but no formal trust tier manifest records this assignment.

**Risk:** Trust tier drift — content is re-ingested or updated without the trust tier being explicitly re-evaluated.

**Recommendation:** Create a `knowledge/ingestion_manifest.json` that records the trust tier, ingestion date, and review status for every source file.

### The Orchestrator is specified but not implemented

The Orchestrator is the critical boundary enforcer between agents. Its absence means that agent routing, context isolation, and Nazareth write operations are all manual or depend on the LLM following instructions in prompts. Prompt-based enforcement is not robust.

**Recommendation:** Do not scale to multi-agent interactions without the Orchestrator as a code-layer enforcer. The Orchestrator must be implemented before the Examiner Agent is activated.

---

## 4. Governance Contradiction Analysis

| Contradiction | Location | Severity |
|---|---|---|
| Tutor prompt allows "Official WSET study guide" as a source, but this corpus is not yet indexed | tutor-agent.md §Source Policy | Medium |
| SEMANTIC_RETRIEVAL_ARCHITECTURE specifies Tier 3 as "Benchmark Answers" but AGENT_BOUNDARIES treats benchmark answers as pedagogical, not scoring authority | Both docs | Low — consistent intent, inconsistent numbering |
| AGENT_BOUNDARIES §10.4 allows Tutor Agent to read from examiner_corpus — but examiner_corpus doesn't exist | AGENT_BOUNDARIES §10.4 | Low — latent contradiction |
| Retrieval architecture specifies minimum composite score 0.55 for Tutor; sandbox runs include results at 0.46 | SEMANTIC_RETRIEVAL_ARCHITECTURE §5.4 | Low — sandbox is validation mode, not production |

---

## 5. Governance Risk Summary

| Risk | Current Status | Severity |
|---|---|---|
| Calibration gate not enforced by code | Active deficiency | **CRITICAL** |
| Examiner corpus empty, cannot be activated safely | Active deficiency | **CRITICAL** |
| WSET specification not processed | Active deficiency | **HIGH** |
| No ingestion manifest for trust tiers | Active deficiency | **HIGH** |
| Diploma content untagged in L3 corpus | Active deficiency | **MEDIUM** |
| No human review of pedagogical content accuracy | Active deficiency | **MEDIUM** |
| Orchestrator not implemented | Architectural gap | **HIGH** |
| Logging infrastructure absent | Architectural gap | **MEDIUM** |

**Overall governance maturity:** The framework is exceptional (9/10). Active enforcement is weak (3/10). The gap between design and implementation is the defining risk.

---

*Generated: 2026-05-15 | Claude (Cowork) — Audit Role | Requires human review before acting on recommendations*

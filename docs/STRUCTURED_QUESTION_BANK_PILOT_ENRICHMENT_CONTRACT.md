# Structured Question Bank Pilot Enrichment Contract

Phase: 4A.3.7.5

Status: contract-only. This document does not enrich real items, create a pilot
bank, migrate questions, generate questions, modify the structured question
bank, or authorize runtime use.

Source bank:

- `knowledge/question-bank/structured/wset3_questions.json`

Adapter skeleton:

- `tools/question_generation/structured_question_bank_adapter.py`

Target validator:

- `tools/question_generation/diagnostic_sba_validator.py`

## 1. Purpose

The pilot enrichment layer is the future step that turns an adapter skeleton
into a fully valid diagnostic SBA item. It is not a generator and it must not
invent unsupported information.

The enrichment layer may add source support, diagnostic option metadata,
rationales, remediation, governance completeness, and attempt placeholders only
when the evidence is available from allowed repo-local sources.

An enriched item must remain training-only and must pass validation before it
can be considered for any future pilot diagnostic bank.

## 2. Non-Goals

This phase does not authorize:

- real item enrichment;
- converted item creation;
- pilot bank creation;
- generated item creation;
- source-bank mutation;
- knowledge-map mutation;
- official Markdown mutation;
- retrieval, frontend, or PSL integration.

## 3. Allowed Enrichment Sources

Future enrichment may use only lightweight repo-local sources:

- Original structured question item.
- Adapter skeleton.
- Knowledge-map causal chains.
- Knowledge-map misconceptions.
- Knowledge-map concepts and relationships.
- Official WSET Markdown or chunks for grounding only, not wording imitation.
- Wine With Jimmy chunks for pedagogical explanation only.
- SAT aliases and SAT config.
- Canonical dictionary and domain expansions.

Allowed sources are evidence inputs, not authority upgrades. Official extracted
materials may ground facts, but they must not be copied into official-looking
questions or rationales.

## 4. Forbidden Sources And Behaviors

Future enrichment must not use:

- external web;
- external APIs;
- LLM generation;
- embeddings;
- vector databases;
- unsupported rationale;
- official wording imitation;
- official scores;
- examiner authority;
- source support invented from thin air.

The enrichment layer must not treat keyword overlap, `source_type`, or a
plausible-sounding explanation as sufficient support.

## 5. Source Support Policy

Every enriched item must include source support with:

- `source_ids`
- `source_chunks`
- `support_rationale`
- `source_role`

Allowed `source_role` values:

- `official_grounding`
- `pedagogical_explanation`
- `knowledge_map_support`

Minimum requirements:

- `source_ids` must be non-empty.
- `source_chunks` must be non-empty.
- `support_rationale` must explain why the cited source supports the item,
  correct answer, and diagnostic contrast.
- `source_role` must describe the evidence role, not official authority.

If source support cannot be attached, the item status must be
`source_support_missing` or `defer_for_human_review`.

## 6. Diagnostic Role Policy

Every option must receive exactly one diagnostic role.

Allowed roles:

- `correct`
- `misconception`
- `partial_reasoning`
- `keyword_trap`
- `causal_confusion`
- `sat_confusion`
- `terminology_confusion`
- `process_confusion`
- `regional_confusion`
- `distractor_unknown`

Rules:

- The correct option must use `correct`.
- Incorrect options must not use `correct`.
- `distractor_unknown` is allowed only when evidence is insufficient and the
  item remains incomplete or deferred.
- Diagnostic roles must not be inferred from option wording alone when a safer
  explanation is unavailable.
- Do not invent misconception IDs to make a role look stronger.

## 7. Misconception Linkage Policy

`misconception_id` may be attached only when:

- option text overlaps known misconception keywords;
- `expected_topics` or `expected_keywords` support the linkage;
- a related knowledge-map misconception node exists.

Otherwise, `misconception_id` must remain null, absent, or unknown. A plausible
wrong answer is not enough by itself to justify a misconception ID.

## 8. Causal-Chain Linkage Policy

`causal_chain_id` may be attached only when:

- `expected_causal_links` references a known causal-chain node;
- the question topic overlaps causal-chain trigger keywords;
- source grounding supports the cause-effect relationship.

Otherwise, `causal_chain_id` must remain null, absent, or unknown.

Legacy, governance-style, and hybrid causal-chain schema families must be
preserved as found. Enrichment must not normalize knowledge-map nodes as a side
effect.

## 9. SAT Relevance Policy

SAT relevance may be attached only when the item concerns:

- aroma;
- palate;
- structure;
- quality;
- readiness;
- balance;
- intensity;
- finish;
- other SAT aliases explicitly supported by repo-local SAT config.

If no SAT alias/config support exists, SAT relevance must be an empty list.

## 10. Rationale Policy

Correct rationales must be source-grounded.

Distractor rationales must explain:

- why the option is plausible;
- why it is wrong;
- what diagnostic error it may indicate;
- which source or knowledge-map evidence supports that contrast.

If evidence is insufficient, the item remains incomplete. The enrichment layer
must not fabricate a rationale to satisfy the validator.

## 11. Remediation Policy

Remediation recommendations should point to one or more training targets:

- topic;
- causal chain;
- misconception;
- SAT skill;
- source chunk.

Allowed remediation target types:

- `topic`
- `causal_chain`
- `misconception`
- `sat_skill`
- `source_chunk`

Remediation must not point to official scores, pass/fail claims, examiner
readiness, certification, or guaranteed outcomes.

## 12. Governance Policy

All enriched items must preserve these values:

```json
{
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

The enrichment layer may complete missing governance constants, but it must
never make an unsafe item safe or introduce official authority.

## 13. Completeness Statuses

Every enrichment result must have one deterministic status:

- `enrichment_complete`
- `source_support_missing`
- `option_diagnostics_missing`
- `rationale_missing`
- `remediation_missing`
- `governance_incomplete`
- `defer_for_human_review`

Status meaning:

| Status | Meaning |
| --- | --- |
| `enrichment_complete` | All required source support, diagnostics, rationales, remediation, governance, and placeholders are present. |
| `source_support_missing` | Source IDs, chunks, or support rationale are absent or unsupported. |
| `option_diagnostics_missing` | One or more options lack a defensible diagnostic role. |
| `rationale_missing` | Correct or distractor rationales are absent or unsupported. |
| `remediation_missing` | No valid training remediation target is available. |
| `governance_incomplete` | Required governance constants are missing or unsafe. |
| `defer_for_human_review` | The item may be valuable but requires manual judgment before enrichment can continue. |

Only `enrichment_complete` candidates may proceed to schema and validator
approval.

## 14. Human Review Policy

Items must require human review when any of the following appear:

- ambiguous options;
- weak or indirect source grounding;
- possible official wording risk;
- unclear correct-answer support;
- no diagnostic role evidence;
- competing plausible answers;
- likely translation/wording drift;
- source support exists but does not clearly support the rationale;
- remediation target is unclear.

Human review does not grant official authority. It only decides whether a
training item can safely proceed.

## 15. Validation Requirements

An enriched item must pass:

- diagnostic SBA schema validation;
- `validate_diagnostic_sba_item(item)`;
- source-role validation;
- diagnostic-role validation;
- governance validation;
- remediation-target validation;
- no official wording or examiner-authority scan;
- no mutation checks against the source item and skeleton.

Current compatibility note:

- The JSON schema uses `single_best_answer` (resolved in Phase 4A.3.7.26).
- The validator accepts `single_best_answer`.

Both the JSON schema and Python validator now agree on the canonical value
`single_best_answer`. The prior divergence has been resolved.

## 16. Implementation Boundary For The Next Phase

Phase 4A.3.7.6 should create a pilot enrichment skeleton only.

It should:

- accept in-memory source item and adapter skeleton fixtures;
- return enrichment status and missing fields;
- validate source roles, diagnostic roles, remediation target types, and
  governance constants;
- avoid reading or writing the source bank;
- avoid enriching real items;
- avoid creating converted files.

## 17. Recommended Next Phase

Phase 4A.3.7.6 - Pilot Enrichment Skeleton.

The next phase should implement pure helper functions for validating enrichment
metadata and assembling a candidate from in-memory fixtures only. It should not
create a pilot bank.

# Phase 4A.3.8.5.6 - Master Bank Eligibility Suitability Integration

## Purpose

The Master Bank Eligibility layer now consumes:

`knowledge/question-bank/open_response/suitability/master_bank_open_response_suitability.json`

This integration changes private session eligibility only. It does not activate
Open Response runtime, alter either frontend, deploy code, or delete Master Bank
records.

## Deterministic Rules

- `open_response_candidate` and `strong_open_response_candidate` map to
  `open_response_candidate`.
- `human_review_required` and `requires_human_review` map to
  `open_response_review_pool`.
- Strong Open Response candidates are excluded from ordinary private SBA
  sessions unless their suitability record has `sba_eligible: true`.
- Review-pool records are excluded from ordinary private SBA sessions unless
  explicitly SBA eligible.
- `sba_only` records remain eligible for `private_practice` and, when curriculum
  metadata is complete, `adaptive_candidate`.
- `inactive` records remain excluded.
- Open Response activation remains false.

## Public Lab Precedence

The 36 public-lab records remain SBA eligible. Three public records (`356`,
`421`, and `464`) also carry `human_review_required`. They remain in the public
lab and SBA operational pool while retaining the review-pool signal.

This controlled overlap explains why operational pool metrics are not mutually
exclusive partitions.

## Operational Metrics

| Metric | Count |
|---|---:|
| `total_master_bank` | 616 |
| `sba_operational_pool` | 506 |
| `open_response_candidate_pool` | 21 |
| `open_response_review_pool` | 68 |
| `inactive` | 24 |
| `public_lab` | 36 |

`sba_operational_pool` consists of 503 `sba_only` records plus the three
public-lab review records that are explicitly SBA eligible.

## Consumers

- `master_bank_eligibility.py` owns category normalization and operational pool
  calculation.
- `full_master_bank_session_composer.py` passes suitability records into the
  eligibility decision and excludes non-SBA candidates from normal sessions.
- `master_bank_utilization_data.py` exposes the new pool metrics for Dashboard
  data without changing frontend code.

## Governance

All governance flags remain false. No scoring authority, WSET equivalence,
recommendation behavior, adaptive activation, external service, or public
activation was introduced.

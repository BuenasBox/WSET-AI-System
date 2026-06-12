"""Generate the Batch 3 Botrytis candidate sidecar without touching production."""

from __future__ import annotations

import json
from pathlib import Path

from tools.question_generation.sba_enrichment_deriver import REPO, derive


ACTIVE_SIDECAR = (
    REPO / "knowledge" / "question-bank" / "enrichment" / "sba_enrichment_v1.json"
)
CANDIDATE_SIDECAR = (
    REPO
    / "knowledge"
    / "question-bank"
    / "enrichment"
    / "sba_enrichment_batch3_candidate.json"
)
BOTRYTIS_NODE_IDS = {
    "HC_BOTRYTIS_CONCENTRATION",
    "HC_NOBLE_ROT_DEVELOPMENT_CONDITIONS",
}


def build_candidate_payload() -> dict:
    payload = derive()
    candidate_ids = sorted(
        record["item_id"]
        for record in payload["items_by_source_question_id"].values()
        if record["_provenance"]["causal_chain"]["derived_from"]
        in BOTRYTIS_NODE_IDS
    )
    payload["phase"] = "P.3-botrytis-candidate"
    payload["candidate_domain"] = "botrytis_concentration"
    payload["candidate_node_ids"] = sorted(BOTRYTIS_NODE_IDS)
    payload["candidate_item_ids"] = candidate_ids
    payload["candidate_item_count"] = len(candidate_ids)
    return payload


def write_candidate_sidecar(path: Path = CANDIDATE_SIDECAR) -> Path:
    payload = build_candidate_payload()
    if payload["governance"]["safe_for_examiner"] is not False:
        raise ValueError("Governance violation")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


if __name__ == "__main__":
    output = write_candidate_sidecar()
    payload = build_candidate_payload()
    print(
        f"Candidate sidecar: {output} "
        f"({payload['candidate_item_count']} Batch 3 candidates)"
    )

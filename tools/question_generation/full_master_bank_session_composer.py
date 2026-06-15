"""Private deterministic session composition across the canonical Master Bank."""

from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter, deque
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from tools.constants import PROJECT_ROOT
from tools.orchestrator.learner_state import DEFAULT_LES, load_learner_state
from tools.question_generation.master_bank import MASTER_BANK_PATH, SAFE_GOVERNANCE
from tools.question_generation.master_bank_eligibility import (
    build_eligibility_index,
    is_session_eligible,
    load_open_response_suitability_index,
)
from tools.question_generation.sba_session_composer import load_master_bank


BLUEPRINT_PATH = Path("knowledge/diagnostic/diagnostic_blueprint.json")
SUPPORTED_MODES = (
    "EXPRESS_10",
    "QUICK_25",
    "STANDARD_50",
    "FULL_DIAGNOSTIC",
    "RA_FOCUS",
)
RA_IDS = ("RA1", "RA2", "RA3", "RA4", "RA5")
DIFFICULTIES = ("foundational", "intermediate", "distinction")
FORBIDDEN_GOVERNANCE_FLAGS = (
    "safe_for_examiner",
    "examiner_scoring_allowed",
    "uses_llm",
    "uses_api",
    "uses_embeddings",
    "uses_vector_db",
    "cloud_services_active",
)


def load_diagnostic_blueprint(
    path: str | Path = BLUEPRINT_PATH,
    root: str | Path = PROJECT_ROOT,
) -> dict[str, Any]:
    """Load and validate the declarative diagnostic blueprint."""
    full_path = Path(root) / Path(path)
    data = json.loads(full_path.read_text(encoding="utf-8"))
    errors = validate_diagnostic_blueprint(data)
    if errors:
        raise ValueError("invalid diagnostic blueprint: " + "; ".join(errors))
    return data


def validate_diagnostic_blueprint(payload: Any) -> list[str]:
    if not isinstance(payload, Mapping):
        return ["blueprint must be an object"]
    errors: list[str] = []
    modes = payload.get("modes")
    if not isinstance(modes, Mapping):
        return ["modes must be an object"]
    for mode in SUPPORTED_MODES:
        config = modes.get(mode)
        if not isinstance(config, Mapping):
            errors.append(f"missing mode: {mode}")
            continue
        count = config.get("question_count")
        if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
            errors.append(f"{mode}.question_count must be positive")
        difficulty = config.get("difficulty_distribution")
        if not isinstance(difficulty, Mapping):
            errors.append(f"{mode}.difficulty_distribution must be an object")
        elif set(difficulty) != set(DIFFICULTIES):
            errors.append(f"{mode}.difficulty_distribution must cover all tiers")
        elif abs(sum(float(difficulty[key]) for key in DIFFICULTIES) - 1.0) > 1e-9:
            errors.append(f"{mode}.difficulty_distribution must total 1")
        if mode != "RA_FOCUS":
            ra_distribution = config.get("ra_distribution")
            if not isinstance(ra_distribution, Mapping):
                errors.append(f"{mode}.ra_distribution must be an object")
            elif set(ra_distribution) != set(RA_IDS):
                errors.append(f"{mode}.ra_distribution must cover RA1-RA5")
            elif sum(int(ra_distribution[key]) for key in RA_IDS) != count:
                errors.append(f"{mode}.ra_distribution must total question_count")
        topic = config.get("topic_distribution")
        if not isinstance(topic, Mapping) or not topic.get("strategy"):
            errors.append(f"{mode}.topic_distribution must define a strategy")
    governance = payload.get("governance")
    if not isinstance(governance, Mapping):
        errors.append("governance must be an object")
    elif any(bool(value) for value in governance.values()):
        errors.append("all blueprint governance flags must be false")
    return errors


def compose_master_bank_session(
    master_bank: Mapping[str, Any] | None = None,
    les: Mapping[str, Any] | None = None,
    *,
    mode: str = "EXPRESS_10",
    target_ra: str | None = None,
    question_count: int | None = None,
    include_open_response: bool = False,
    blueprint: Mapping[str, Any] | None = None,
    next_session_signals: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Compose one deterministic private session without writing state."""
    bank = master_bank if master_bank is not None else load_master_bank(MASTER_BANK_PATH)
    learner_state = copy.deepcopy(dict(les)) if les is not None else load_learner_state()
    diagnostic_blueprint = (
        dict(blueprint) if blueprint is not None else load_diagnostic_blueprint()
    )
    errors = validate_diagnostic_blueprint(diagnostic_blueprint)
    if errors:
        raise ValueError("invalid diagnostic blueprint: " + "; ".join(errors))

    normalized_mode = str(mode or "").strip().upper()
    if normalized_mode not in SUPPORTED_MODES:
        raise ValueError(f"mode must be one of: {', '.join(SUPPORTED_MODES)}")
    config = dict(diagnostic_blueprint["modes"][normalized_mode])
    resolved_ra = _resolve_target_ra(normalized_mode, target_ra)
    requested_count = _resolve_question_count(config, question_count)
    allow_open = bool(
        include_open_response
        and config.get("composition", {}).get("allow_open_response_candidates", False)
    )
    adaptive_signals = _normalize_next_session_signals(next_session_signals)
    suitability_index = load_open_response_suitability_index()

    candidates = [
        dict(item)
        for item in bank.get("items", [])
        if isinstance(item, Mapping)
        and is_session_eligible(
            item,
            include_open_response=allow_open,
            suitability=suitability_index.get(str(item.get("master_item_id", ""))),
        )
        and (resolved_ra is None or _curriculum(item).get("ra") == resolved_ra)
    ]
    exposure = _question_exposure_map(learner_state)
    recent_ids = _recent_question_ids(learner_state, diagnostic_blueprint) | set(
        adaptive_signals["exposure_avoidance"]
    )
    candidates.sort(
        key=lambda item: _candidate_rank(
            item,
            exposure,
            recent_ids,
            adaptive_signals,
        )
    )

    ra_targets = _ra_targets(config, requested_count, resolved_ra)
    difficulty_targets = _allocate_by_ratio(
        requested_count,
        config["difficulty_distribution"],
        DIFFICULTIES,
    )
    topic_cap = int(
        config.get("topic_distribution", {}).get(
            "maximum_questions_per_topic", requested_count
        )
    )
    selected = _select_candidates(
        candidates,
        requested_count=requested_count,
        ra_targets=ra_targets,
        difficulty_targets=difficulty_targets,
        topic_cap=topic_cap,
    )
    composition = _composition(selected)
    warnings = _composition_warnings(
        requested_count=requested_count,
        config=config,
        composition=composition,
        target_ra=resolved_ra,
    )
    item_ids = [item["master_item_id"] for item in selected]
    session_id = _session_id(normalized_mode, resolved_ra, item_ids)
    eligibility = build_eligibility_index(bank, suitability_index)

    session = {
        "schema_version": "full_master_bank_session_v1",
        "session_id": session_id,
        "mode": normalized_mode,
        "target_ra": resolved_ra,
        "requested_count": requested_count,
        "item_count": len(selected),
        "master_bank_size": len(bank.get("items", [])),
        "active_pool_size": len(candidates),
        "eligibility_counts": eligibility["primary_counts"],
        "operational_pool_counts": eligibility["operational_counts"],
        "selection_policy": copy.deepcopy(diagnostic_blueprint["selection_policy"]),
        "requested_composition": {
            "ra": ra_targets,
            "difficulty": difficulty_targets,
            "topic": copy.deepcopy(config["topic_distribution"]),
        },
        "achieved_composition": composition,
        "warnings": warnings,
        "master_item_ids": item_ids,
        "source_question_ids": [item["source_question_id"] for item in selected],
        "items": copy.deepcopy(selected),
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }
    if next_session_signals is not None:
        session["adaptive_selection"] = _adaptive_selection_summary(adaptive_signals)
    return session


def compose_adaptive_master_bank_session(
    next_session_signals: Mapping[str, Any],
    master_bank: Mapping[str, Any] | None = None,
    les: Mapping[str, Any] | None = None,
    *,
    mode: str | None = None,
    target_ra: str | None = None,
    question_count: int | None = None,
    include_open_response: bool = False,
    blueprint: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Compose the next session from validated learning-event signals."""
    signals = _normalize_next_session_signals(next_session_signals)
    resolved_mode = str(
        mode or signals["recommended_next_mode"] or "EXPRESS_10"
    ).strip().upper()
    resolved_ra = target_ra
    if resolved_mode == "RA_FOCUS" and resolved_ra is None:
        priorities = signals["RA_reinforcement_priority"]
        if priorities:
            resolved_ra = priorities[0]["ra_id"]
        else:
            resolved_mode = "QUICK_25"
    session = compose_master_bank_session(
        master_bank,
        les,
        mode=resolved_mode,
        target_ra=resolved_ra,
        question_count=question_count,
        include_open_response=include_open_response,
        blueprint=blueprint,
        next_session_signals=signals,
    )
    session["schema_version"] = "adaptive_master_bank_session_v1"
    return session


def _select_candidates(
    candidates: Sequence[dict[str, Any]],
    *,
    requested_count: int,
    ra_targets: Mapping[str, int],
    difficulty_targets: Mapping[str, int],
    topic_cap: int,
) -> list[dict[str, Any]]:
    remaining = list(candidates)
    selected: list[dict[str, Any]] = []
    topic_counts: Counter[str] = Counter()
    slots = list(zip(_interleaved_slots(ra_targets), _interleaved_slots(difficulty_targets)))

    for ra_id, difficulty in slots:
        index = _find_candidate(remaining, ra_id, difficulty, topic_counts, topic_cap)
        if index is None:
            index = _find_candidate(remaining, ra_id, None, topic_counts, topic_cap)
        if index is None:
            index = _find_candidate(remaining, ra_id, difficulty, topic_counts, None)
        if index is None:
            index = _find_candidate(remaining, ra_id, None, topic_counts, None)
        if index is None:
            index = _find_candidate(remaining, None, difficulty, topic_counts, topic_cap)
        if index is None:
            index = _find_candidate(remaining, None, None, topic_counts, topic_cap)
        if index is None:
            index = _find_candidate(remaining, None, None, topic_counts, None)
        if index is None:
            break
        item = remaining.pop(index)
        selected.append(item)
        topic_counts[str(_curriculum(item).get("topic", "unknown"))] += 1
        if len(selected) >= requested_count:
            break
    return selected


def _find_candidate(
    candidates: Sequence[dict[str, Any]],
    ra_id: str | None,
    difficulty: str | None,
    topic_counts: Mapping[str, int],
    topic_cap: int | None,
) -> int | None:
    for index, item in enumerate(candidates):
        curriculum = _curriculum(item)
        topic = str(curriculum.get("topic", "unknown"))
        if ra_id is not None and curriculum.get("ra") != ra_id:
            continue
        if difficulty is not None and curriculum.get("difficulty") != difficulty:
            continue
        if topic_cap is not None and topic_counts.get(topic, 0) >= topic_cap:
            continue
        return index
    return None


def _candidate_rank(
    item: Mapping[str, Any],
    exposure: Mapping[str, Mapping[str, Any]],
    recent_ids: set[str],
    signals: Mapping[str, Any],
) -> tuple[int, int, int, str, tuple[int, str]]:
    item_id = str(item.get("master_item_id", ""))
    signal = exposure.get(item_id, {})
    return (
        1 if item_id in recent_ids else 0,
        _adaptive_candidate_priority(item, signals),
        int(signal.get("exposure_count", 0) or 0),
        str(signal.get("last_seen") or ""),
        _numeric_sort_key(item.get("source_question_id")),
    )


def _adaptive_candidate_priority(
    item: Mapping[str, Any],
    signals: Mapping[str, Any],
) -> int:
    curriculum = _curriculum(item)
    topic = str(curriculum.get("topic") or "")
    ra_id = str(curriculum.get("ra") or "")
    difficulty = str(curriculum.get("difficulty") or "")
    links = _learning_link_ids(item)
    if links["misconceptions"] & set(signals["misconception_repair_candidate"]):
        return 0
    if links["causal_chains"] & set(
        signals["causal_chain_reinforcement_candidate"]
    ):
        return 1
    weak_topics = {
        entry["topic"]: entry["priority"]
        for entry in signals["weak_topic_priority"]
    }
    if topic in weak_topics:
        return 2 if weak_topics[topic] == "urgent" else 3
    strong_topics = {
        entry["topic"]
        for entry in signals["strong_topic_progression_candidate"]
    }
    if topic in strong_topics and difficulty == "distinction":
        return 4
    prioritized_ras = {
        entry["ra_id"]
        for entry in signals["RA_reinforcement_priority"]
    }
    if ra_id in prioritized_ras:
        return 5
    if topic in strong_topics:
        return 6
    return 7


def _normalize_next_session_signals(
    signals: Mapping[str, Any] | None,
) -> dict[str, Any]:
    empty = {
        "schema_version": "next_session_learning_signals_v1",
        "weak_topic_priority": [],
        "strong_topic_progression_candidate": [],
        "RA_reinforcement_priority": [],
        "misconception_repair_candidate": [],
        "causal_chain_reinforcement_candidate": [],
        "exposure_avoidance": [],
        "recommended_next_mode": None,
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }
    if signals is None:
        return empty
    if not isinstance(signals, Mapping):
        raise ValueError("next_session_signals must be an object")
    if str(signals.get("schema_version") or "") != "next_session_learning_signals_v1":
        raise ValueError("unsupported next_session_signals schema_version")
    governance = signals.get("governance")
    if not isinstance(governance, Mapping) or any(
        bool(governance.get(key)) for key in FORBIDDEN_GOVERNANCE_FLAGS
    ):
        raise ValueError("next_session_signals governance must fail closed")
    normalized = copy.deepcopy(empty)
    normalized["weak_topic_priority"] = _normalized_signal_rows(
        signals.get("weak_topic_priority"),
        identity_key="topic",
        allowed_extra={"priority", "stage"},
    )
    normalized["strong_topic_progression_candidate"] = _normalized_signal_rows(
        signals.get("strong_topic_progression_candidate"),
        identity_key="topic",
        allowed_extra={"stage", "next_challenge"},
    )
    normalized["RA_reinforcement_priority"] = _normalized_signal_rows(
        signals.get("RA_reinforcement_priority"),
        identity_key="ra_id",
        allowed_extra={"priority"},
        allowed_id_values=set(RA_IDS),
    )
    for key in (
        "misconception_repair_candidate",
        "causal_chain_reinforcement_candidate",
        "exposure_avoidance",
    ):
        normalized[key] = _normalized_text_list(signals.get(key))
    recommended = str(signals.get("recommended_next_mode") or "").strip().upper()
    if recommended and recommended not in SUPPORTED_MODES:
        raise ValueError("recommended_next_mode is unsupported")
    normalized["recommended_next_mode"] = recommended or None
    return normalized


def _normalized_signal_rows(
    value: Any,
    *,
    identity_key: str,
    allowed_extra: set[str],
    allowed_id_values: set[str] | None = None,
) -> list[dict[str, str]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{identity_key} signals must be a list")
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for entry in value:
        if not isinstance(entry, Mapping):
            raise ValueError(f"{identity_key} signal entries must be objects")
        identity = str(entry.get(identity_key) or "").strip()
        if not identity:
            raise ValueError(f"{identity_key} signal entry requires {identity_key}")
        if allowed_id_values is not None and identity not in allowed_id_values:
            raise ValueError(f"unsupported {identity_key}: {identity}")
        if identity in seen:
            continue
        row = {identity_key: identity}
        for key in sorted(allowed_extra):
            text = str(entry.get(key) or "").strip()
            if text:
                row[key] = text
        rows.append(row)
        seen.add(identity)
    return rows


def _normalized_text_list(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("adaptive signal IDs must be lists")
    return list(dict.fromkeys(str(item).strip() for item in value if str(item).strip()))


def _learning_link_ids(item: Mapping[str, Any]) -> dict[str, set[str]]:
    links = item.get("learning_links")
    if not isinstance(links, Mapping):
        return {"misconceptions": set(), "causal_chains": set()}
    misconceptions: set[str] = set()
    causal_chains: set[str] = set()
    direct_chain = str(links.get("causal_chain_id") or "").strip()
    if direct_chain:
        causal_chains.add(direct_chain)
    options = links.get("options")
    if isinstance(options, Mapping):
        for option in options.values():
            if not isinstance(option, Mapping):
                continue
            misconception = str(option.get("misconception_id") or "").strip()
            chain = str(option.get("causal_chain_id") or "").strip()
            if misconception:
                misconceptions.add(misconception)
            if chain:
                causal_chains.add(chain)
    return {"misconceptions": misconceptions, "causal_chains": causal_chains}


def _adaptive_selection_summary(signals: Mapping[str, Any]) -> dict[str, Any]:
    active = any(
        signals[key]
        for key in (
            "weak_topic_priority",
            "strong_topic_progression_candidate",
            "RA_reinforcement_priority",
            "misconception_repair_candidate",
            "causal_chain_reinforcement_candidate",
            "exposure_avoidance",
        )
    )
    return {
        "signals_consumed": bool(active or signals["recommended_next_mode"]),
        "recommended_next_mode": signals["recommended_next_mode"],
        "weak_topics": [entry["topic"] for entry in signals["weak_topic_priority"]],
        "strong_topics": [
            entry["topic"]
            for entry in signals["strong_topic_progression_candidate"]
        ],
        "reinforcement_ras": [
            entry["ra_id"] for entry in signals["RA_reinforcement_priority"]
        ],
        "misconception_targets": list(signals["misconception_repair_candidate"]),
        "causal_chain_targets": list(
            signals["causal_chain_reinforcement_candidate"]
        ),
        "exposure_avoidance_count": len(signals["exposure_avoidance"]),
    }


def _question_exposure_map(les: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    value = les.get("question_exposure_signals", {})
    return dict(value) if isinstance(value, Mapping) else {}


def _recent_question_ids(
    les: Mapping[str, Any],
    blueprint: Mapping[str, Any],
) -> set[str]:
    limit = int(blueprint["selection_policy"].get("recent_history_limit", 50))
    history = les.get("question_exposure_log", [])
    if not isinstance(history, list):
        return set()
    recent = history[-limit:]
    return {
        str(entry.get("question_id", "")).strip()
        for entry in recent
        if isinstance(entry, Mapping) and str(entry.get("question_id", "")).strip()
    }


def _ra_targets(
    config: Mapping[str, Any],
    count: int,
    target_ra: str | None,
) -> dict[str, int]:
    if target_ra:
        return {ra_id: count if ra_id == target_ra else 0 for ra_id in RA_IDS}
    configured = config["ra_distribution"]
    configured_total = sum(int(configured[ra_id]) for ra_id in RA_IDS)
    ratios = {
        ra_id: int(configured[ra_id]) / configured_total
        for ra_id in RA_IDS
    }
    return _allocate_by_ratio(count, ratios, RA_IDS)


def _allocate_by_ratio(
    count: int,
    ratios: Mapping[str, Any],
    ordered_keys: Sequence[str],
) -> dict[str, int]:
    raw = {key: count * float(ratios[key]) for key in ordered_keys}
    allocated = {key: int(raw[key]) for key in ordered_keys}
    remainder = count - sum(allocated.values())
    order = sorted(
        ordered_keys,
        key=lambda key: (-(raw[key] - allocated[key]), ordered_keys.index(key)),
    )
    for key in order[:remainder]:
        allocated[key] += 1
    return allocated


def _interleaved_slots(targets: Mapping[str, int]) -> list[str]:
    queues = {
        key: deque([key] * int(value))
        for key, value in targets.items()
        if int(value) > 0
    }
    slots: list[str] = []
    while queues:
        for key in list(queues):
            slots.append(queues[key].popleft())
            if not queues[key]:
                del queues[key]
    return slots


def _composition(items: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    ra = Counter(str(_curriculum(item).get("ra", "unknown")) for item in items)
    difficulty = Counter(
        str(_curriculum(item).get("difficulty", "unknown")) for item in items
    )
    topics = Counter(str(_curriculum(item).get("topic", "unknown")) for item in items)
    question_types = Counter(str(item.get("question_type", "unknown")) for item in items)
    return {
        "ra": dict(sorted(ra.items())),
        "difficulty": dict(sorted(difficulty.items())),
        "topics": dict(sorted(topics.items())),
        "distinct_topics": len(topics),
        "question_types": dict(sorted(question_types.items())),
    }


def _composition_warnings(
    *,
    requested_count: int,
    config: Mapping[str, Any],
    composition: Mapping[str, Any],
    target_ra: str | None,
) -> list[str]:
    warnings: list[str] = []
    achieved = sum(composition["ra"].values())
    if achieved < requested_count:
        warnings.append(f"pool_shortfall:{requested_count - achieved}")
    minimum_topics = int(config["topic_distribution"]["minimum_distinct_topics"])
    if composition["distinct_topics"] < minimum_topics:
        warnings.append(
            f"topic_coverage_shortfall:{minimum_topics - composition['distinct_topics']}"
        )
    achieved_difficulty = composition["difficulty"]
    requested_difficulty = _allocate_by_ratio(
        requested_count,
        config["difficulty_distribution"],
        DIFFICULTIES,
    )
    for difficulty, target in requested_difficulty.items():
        shortfall = target - int(achieved_difficulty.get(difficulty, 0))
        if shortfall > 0:
            warnings.append(f"difficulty_shortfall:{difficulty}:{shortfall}")
    if target_ra and set(composition["ra"]) - {target_ra}:
        warnings.append("target_ra_leakage")
    return warnings


def _resolve_target_ra(mode: str, target_ra: str | None) -> str | None:
    if mode != "RA_FOCUS":
        if target_ra is not None:
            raise ValueError("target_ra is only supported by RA_FOCUS")
        return None
    normalized = str(target_ra or "").strip().upper()
    if normalized not in RA_IDS:
        raise ValueError("RA_FOCUS requires target_ra in RA1-RA5")
    return normalized


def _resolve_question_count(config: Mapping[str, Any], value: int | None) -> int:
    if value is None:
        return int(config["question_count"])
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError("question_count must be a positive integer")
    return value


def _session_id(mode: str, target_ra: str | None, item_ids: Sequence[str]) -> str:
    material = "|".join((mode, target_ra or "ALL", *item_ids))
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]
    return f"mbs_{digest}"


def _curriculum(item: Mapping[str, Any]) -> Mapping[str, Any]:
    value = item.get("curriculum")
    return value if isinstance(value, Mapping) else {}


def _numeric_sort_key(value: Any) -> tuple[int, str]:
    text = str(value)
    digits = "".join(char for char in text if char.isdigit())
    return (int(digits) if digits else 0, text)

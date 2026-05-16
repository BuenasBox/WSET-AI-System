"""Report writer for local Tutor self-evaluation simulation."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

from tools.tutor.explanation_priority import calculate_tutor_evaluation_signals
from tools.youtube_transcription.config import PROJECT_ROOT


DEFAULT_SELF_EVAL_DIR = PROJECT_ROOT / "knowledge" / "self-eval"
DEFAULT_FEEDBACK_PATH = PROJECT_ROOT / "knowledge" / "nazareth" / "self_eval_feedback.json"


def write_evaluation_reports(
    results: list[dict[str, Any]],
    output_dir: Path = DEFAULT_SELF_EVAL_DIR,
    feedback_path: Path = DEFAULT_FEEDBACK_PATH,
    strictness: str = "hard",
    reconcile_les: bool = True,
) -> dict[str, str]:
    """Write Markdown, CSV, JSONL, and LES feedback simulation artifacts.

    When reconcile_les=True (the default), also reconcile the feedback into the
    canonical Learner Epistemic State via les_reconciler.reconcile_les_from_feedback().
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    results = _with_tutor_evaluation_signals(results)
    summary_path = output_dir / "self_eval_summary.md"
    csv_path = output_dir / "self_eval_results.csv"
    jsonl_path = output_dir / "self_eval_results.jsonl"
    # Annotate feedback with questions_attempted so the reconciler can use it
    feedback = build_les_feedback(results, strictness=strictness)
    feedback["questions_attempted"] = len(results)
    summary_path.write_text(_render_summary(results, strictness=strictness), encoding="utf-8")
    _write_csv(csv_path, results)
    _write_jsonl(jsonl_path, results)
    feedback_path.parent.mkdir(parents=True, exist_ok=True)
    feedback_path.write_text(json.dumps(feedback, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    paths = {
        "summary": summary_path.as_posix(),
        "csv": csv_path.as_posix(),
        "jsonl": jsonl_path.as_posix(),
        "feedback": feedback_path.as_posix(),
    }
    if reconcile_les:
        try:
            from tools.orchestrator.les_reconciler import reconcile_les_from_feedback
            reconciliation = reconcile_les_from_feedback(feedback_path=feedback_path)
            paths["les_reconciliation_status"] = reconciliation.get("status", "unknown")
        except Exception as exc:  # pragma: no cover — reconciler errors must not break the reporter
            paths["les_reconciliation_status"] = f"error: {exc}"
    return paths


def build_les_feedback(results: list[dict[str, Any]], strictness: str = "hard") -> dict[str, Any]:
    """Create simulated LES feedback without modifying the real LES."""
    causal_counter = Counter()
    misconception_counter = Counter()
    retrieval_gaps = []
    retrieval_counter = Counter()
    label_counter = Counter()
    for result in results:
        comparison = result.get("comparison", {})
        label_counter.update(comparison.get("failure_labels", []))
        for link in comparison.get("missing_causal_links", []):
            causal_counter[link] += _difficulty_weight(result)
        for gap in comparison.get("likely_misconception_gaps", []):
            misconception_counter[gap] += _difficulty_weight(result)
        for weakness in comparison.get("retrieval_weaknesses", []):
            retrieval_counter[weakness] += _difficulty_weight(result)
        labels = comparison.get("failure_labels", [])
        if "retrieval_gap" in labels or "weak_context_support" in labels or "shallow_retrieval" in labels:
            retrieval_gaps.append(result.get("question_id", ""))
    fragile = [
        {"concept": link, "weakness_count": count, "severity": _severity(count)}
        for link, count in causal_counter.most_common()
        if count >= 1
    ]
    retrieval_fragile = [
        {"concept": weakness, "weakness_count": count, "severity": _severity(count)}
        for weakness, count in retrieval_counter.most_common()
        if count >= 2
    ]
    return {
        "schema_version": "self_eval_feedback_v2",
        "strictness": strictness,
        "safe_for_examiner": False,
        "examiner_scoring_allowed": False,
        "fragile_concepts": fragile + retrieval_fragile,
        "weakness_counters": {
            "causal_chains": dict(causal_counter),
            "misconceptions": dict(misconception_counter),
            "retrieval": dict(retrieval_counter),
            "failure_labels": dict(label_counter),
        },
        "suggested_misconception_investigations": list(misconception_counter.keys()),
        "orchestrator_recommendations": _orchestrator_recommendations(causal_counter, misconception_counter, retrieval_counter),
        "retrieval_gap_question_ids": retrieval_gaps,
        "note": "Self-eval feedback artifact; real LES is updated by les_reconciler.reconcile_les_from_feedback().",
    }


def _render_summary(results: list[dict[str, Any]], strictness: str) -> str:
    label_counts = Counter()
    domain_strengths = Counter()
    domain_weaknesses = Counter()
    retrieval_gaps = []
    causal_missing = Counter()
    sat_weaknesses = []
    unresolved = []
    retrieval_weaknesses = Counter()
    missing_exam_language = Counter()
    reasoning_domains = Counter()
    failed_answers = []
    evaluation_signal_totals = Counter()
    evaluation_signal_count = 0
    for result in results:
        comparison = result.get("comparison", {})
        labels = comparison.get("failure_labels", [])
        label_counts.update(labels)
        reasoning_domains.update([result.get("expected_reasoning_type", "unknown")])
        if not labels:
            domain_strengths[result.get("question_type", "unknown")] += 1
        else:
            domain_weaknesses[result.get("question_type", "unknown")] += len(labels)
            failed_answers.append(result.get("question_id", ""))
        causal_missing.update(comparison.get("missing_causal_links", []))
        if "retrieval_gap" in labels:
            retrieval_gaps.append(result.get("question_id", ""))
        retrieval_weaknesses.update(comparison.get("retrieval_weaknesses", []))
        if result.get("question_type") == "sat" and labels:
            sat_weaknesses.append(result.get("question_id", ""))
        if "missing_exam_language" in labels:
            missing_exam_language.update(result.get("expected_keywords", []))
        unresolved.extend(comparison.get("likely_misconception_gaps", []))
        signals = result.get("tutor_evaluation_signals") or {}
        if signals:
            evaluation_signal_count += 1
            for key in ("explanation_density", "causal_coherence", "misconception_coverage", "reasoning_depth_score"):
                evaluation_signal_totals[key] += float(signals.get(key) or 0)

    strongest = domain_strengths.most_common(3)
    weakest = domain_weaknesses.most_common(3)
    priorities = [label for label, _ in label_counts.most_common(5)]
    lines = [
        "# Local Tutor Self-Evaluation Summary",
        "",
        "This is a local Tutor-development simulation. It is not official Examiner grading, does not assign marks, and does not claim WSET grading accuracy.",
        "",
        f"Strictness: {strictness}",
        f"Questions attempted: {len(results)}",
        f"Strongest domains: {strongest or 'none'}",
        f"Weakest domains: {weakest or 'none'}",
        f"Strongest reasoning domains: {reasoning_domains.most_common(5) if strongest else 'none'}",
        f"Weakest reasoning domains: {weakest or 'none'}",
        f"Most common failure labels: {label_counts.most_common(10)}",
        f"Top failing causal chains: {causal_missing.most_common(10)}",
        f"Top misconception risks: {Counter(unresolved).most_common(10)}",
        f"Top retrieval weaknesses: {retrieval_weaknesses.most_common(10)}",
        f"Top SAT weaknesses: {sat_weaknesses or 'none'}",
        f"Top shallow reasoning patterns: {[(label, count) for label, count in label_counts.items() if 'shallow' in label]}",
        f"Most common missing exam language: {missing_exam_language.most_common(10)}",
        f"Misconceptions frequently unresolved: {Counter(unresolved).most_common(10)}",
        f"Retrieval gaps: {retrieval_gaps or 'none'}",
        f"Causal chains frequently missing: {causal_missing.most_common(10)}",
        f"SAT weaknesses: {sat_weaknesses or 'none'}",
        f"Top improvement priorities: {priorities or 'none'}",
        f"Orchestrator intervention priorities: {_orchestrator_recommendations(causal_missing, Counter(unresolved), retrieval_weaknesses) or 'none'}",
        f"Tutor evaluation signals: {_average_signals(evaluation_signal_totals, evaluation_signal_count)}",
        f"Sample failed answers: {failed_answers[:5] or 'none'}",
        "",
        "Governance: safe_for_examiner=false; examiner_scoring_allowed=false.",
    ]
    return "\n".join(lines) + "\n"


def _write_csv(path: Path, results: list[dict[str, Any]]) -> None:
    fields = [
        "question_id",
        "question_type",
        "question_text",
        "failure_labels",
        "strengths",
        "missing_keywords",
        "missing_causal_links",
        "retrieval_weaknesses",
        "safe_for_examiner",
        "difficulty",
        "strictness",
        "explanation_density",
        "causal_coherence",
        "misconception_coverage",
        "reasoning_depth_score",
    ]
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for result in results:
            comparison = result.get("comparison", {})
            signals = result.get("tutor_evaluation_signals") or {}
            writer.writerow(
                {
                    "question_id": result.get("question_id", ""),
                    "question_type": result.get("question_type", ""),
                    "question_text": result.get("question_text", ""),
                    "failure_labels": ";".join(comparison.get("failure_labels", [])),
                    "strengths": ";".join(comparison.get("strengths", [])),
                    "missing_keywords": ";".join(comparison.get("missing_keywords", [])),
                    "missing_causal_links": ";".join(comparison.get("missing_causal_links", [])),
                    "retrieval_weaknesses": ";".join(comparison.get("retrieval_weaknesses", [])),
                    "safe_for_examiner": "false",
                    "difficulty": result.get("difficulty", "intermediate"),
                    "strictness": comparison.get("strictness", ""),
                    "explanation_density": signals.get("explanation_density", ""),
                    "causal_coherence": signals.get("causal_coherence", ""),
                    "misconception_coverage": signals.get("misconception_coverage", ""),
                    "reasoning_depth_score": signals.get("reasoning_depth_score", ""),
                }
            )


def _write_jsonl(path: Path, results: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as file:
        for result in results:
            file.write(json.dumps(result, ensure_ascii=True) + "\n")


def _difficulty_weight(result: dict[str, Any]) -> int:
    difficulty = result.get("difficulty", "intermediate")
    return {"foundational": 1, "intermediate": 2, "distinction": 3}.get(difficulty, 2)


def _severity(count: int) -> str:
    if count >= 5:
        return "high"
    if count >= 3:
        return "medium"
    return "low"


def _with_tutor_evaluation_signals(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched = []
    for result in results:
        clone = dict(result)
        if not clone.get("tutor_evaluation_signals"):
            signals = _load_tutor_evaluation_signals(clone)
            if signals:
                clone["tutor_evaluation_signals"] = signals
        enriched.append(clone)
    return enriched


def _load_tutor_evaluation_signals(result: dict[str, Any]) -> dict[str, Any]:
    answer_path = Path(str(result.get("tutor_attempt_path") or ""))
    package_path = Path(str(result.get("tutor_context_package_path") or ""))
    if not answer_path.exists() or not package_path.exists():
        return {}
    try:
        answer_text = answer_path.read_text(encoding="utf-8")
        context_package = json.loads(package_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return calculate_tutor_evaluation_signals(answer_text, context_package)


def _average_signals(signal_totals: Counter, count: int) -> dict[str, float] | str:
    if count <= 0:
        return "none"
    return {key: round(value / count, 2) for key, value in signal_totals.items()}


def _orchestrator_recommendations(
    causal_counter: Counter,
    misconception_counter: Counter,
    retrieval_counter: Counter,
) -> list[str]:
    recommendations = []
    for link, count in causal_counter.most_common(5):
        recommendations.append(f"Increase forced causal-chain retrieval for '{link}' (weighted failures={count}).")
    for misconception, count in misconception_counter.most_common(5):
        recommendations.append(f"Add misconception pre-pass probes for '{misconception}' (weighted failures={count}).")
    for weakness, count in retrieval_counter.most_common(5):
        recommendations.append(f"Improve retrieval plan for '{weakness}' (weighted failures={count}).")
    return recommendations

"""Static Protocol contracts for orchestrator-adjacent modules.

These protocols are type-checking aids only. They do not alter runtime
orchestrator behavior or introduce new service calls.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol


class AnswerBuilderProtocol(Protocol):
    def build_tutor_answer(self, context_package_path: Path, output_path: Path | None = None) -> str:
        ...


class RetrievalProtocol(Protocol):
    def run_retrieval_sandbox(
        self,
        root: Path,
        query: str,
        top_k: int = 10,
        output_prefix: str = "retrieval_sandbox",
    ) -> dict[str, Any]:
        ...


class LearnerStateProtocol(Protocol):
    def ensure_learner_files(self, les_path: Path, staging_path: Path) -> None:
        ...

    def load_learner_state(self, path: Path) -> dict[str, Any]:
        ...

    def build_les_context(self, learner_state: dict[str, Any]) -> dict[str, Any]:
        ...

    def write_session_staging(self, payload: dict[str, Any], path: Path) -> Path:
        ...


class ScaffoldingProtocol(Protocol):
    def select_scaffolding_policy(self, context_package: dict[str, Any]) -> dict[str, Any]:
        ...

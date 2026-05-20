"""Shared path and governance constants for local Tutor tooling."""

from __future__ import annotations

from pathlib import Path


# Repo root (anchor for all relative paths)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Knowledge directories
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"
OFFICIAL_WSET_DIR = KNOWLEDGE_DIR / "official-wset"
SELF_EVAL_DIR = KNOWLEDGE_DIR / "self-eval"
RETRIEVAL_SANDBOX_DIR = KNOWLEDGE_DIR / "retrieval-sandbox"

# Learner state
NAZARETH_DIR = KNOWLEDGE_DIR / "nazareth"

# Tutor output directories
CONTEXT_PACKAGES_DIR = NAZARETH_DIR / "context_packages"

# Governance constants
SAFE_FOR_EXAMINER = False
EXAMINER_SCORING_ALLOWED = False
USES_LLM = False
USES_API = False
USES_EMBEDDINGS = False
USES_VECTOR_DB = False
CLOUD_SERVICES_ACTIVE = False

# SAT/BICL detection vocabulary (control logic only, not student-facing prose)
SAT_EVALUATION_TERMS: frozenset[str] = frozenset(
    {
        "balance",
        "intensity",
        "complexity",
        "length",
        "finish",
        "bicl",
        "intensidad",
        "complejidad",
        "longitud",
        "acabado",
    }
)

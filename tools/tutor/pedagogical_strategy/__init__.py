"""Pedagogical Strategy Layer — Phase PSL-A.

This package provides deterministic, governance-clean pedagogical function
composition for the WSET-AI-System tutor. It is intentionally isolated from
retrieval and answer_builder during the gated experimental phase.

Public API
----------
  from tools.tutor.pedagogical_strategy.profiles import get_profile, validate_profile_config
  from tools.tutor.pedagogical_strategy.mode_selector import select_pedagogical_strategy
  from tools.tutor.pedagogical_strategy.strategy_layer import build_pedagogical_strategy

Governance invariants
---------------------
  safe_for_examiner = False          (always)
  examiner_scoring_allowed = False   (always)
  uses_llm = False
  uses_api = False
  uses_embeddings = False
  uses_vector_db = False
"""

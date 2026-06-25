"""
core/__init__.py — Constitutional Engine Core Package

Exposes the primary entry points for Phase 2 and Phase 3:
  - get_deterministic_generator  (llm_binding)
  - HypothesisPayload            (llm_binding)
  - ingest_pdfs                  (ingest_pdfs)
  - RedTeamEvaluator             (red_team)
  - AdversarialVetoError         (red_team)
  - compile_tier1_dossier        (compiler)
"""

from core.llm_binding import get_deterministic_generator, HypothesisPayload
from core.ingest_pdfs import ingest_pdfs
from core.red_team import RedTeamEvaluator, AdversarialVetoError
from core.compiler import compile_tier1_dossier

__all__ = [
    "get_deterministic_generator",
    "HypothesisPayload",
    "ingest_pdfs",
    "RedTeamEvaluator",
    "AdversarialVetoError",
    "compile_tier1_dossier",
]

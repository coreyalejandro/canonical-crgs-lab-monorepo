"""
core/__init__.py — Constitutional Engine Core Package

Exposes the primary entry points for Phases 2–5:
  - get_deterministic_generator  (llm_binding)
  - HypothesisPayload            (llm_binding)
  - ingest_pdfs                  (ingest_pdfs)
  - RedTeamEvaluator             (red_team)
  - AdversarialVetoError         (red_team)
  - compile_tier1_dossier        (compiler)
  - run_ingestion                (ingest_arxiv)
  - Neo4jIngestionEngine         (ingest_arxiv)
  - ExtractedPaper               (ingest_arxiv)
  - app_executor                 (master_orchestrator)
  - ProductionResearchState      (master_orchestrator)
  - ConstitutionalLoopError      (master_orchestrator)
  - build_orchestrator           (master_orchestrator)
"""

from core.llm_binding import get_deterministic_generator, HypothesisPayload
from core.ingest_pdfs import ingest_pdfs
from core.red_team import RedTeamEvaluator, AdversarialVetoError
from core.compiler import compile_tier1_dossier
from core.ingest_arxiv import run_ingestion, Neo4jIngestionEngine, ExtractedPaper
from core.master_orchestrator import (
    app_executor,
    ProductionResearchState,
    ConstitutionalLoopError,
    build_orchestrator,
)

__all__ = [
    "get_deterministic_generator",
    "HypothesisPayload",
    "ingest_pdfs",
    "RedTeamEvaluator",
    "AdversarialVetoError",
    "compile_tier1_dossier",
    "run_ingestion",
    "Neo4jIngestionEngine",
    "ExtractedPaper",
    "app_executor",
    "ProductionResearchState",
    "ConstitutionalLoopError",
    "build_orchestrator",
]

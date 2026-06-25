"""
core/__init__.py — Constitutional Engine Core Package

Exposes the primary entry points for Phases 2–10:
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
  - ImmutableAuditLedger         (audit_ledger)         Phase 7
  - secure_audit_node            (audit_ledger)         Phase 7
  - CommercialOrchestrator       (commercializer)       Phase 8
  - PriorArtConflictError        (commercializer)       Phase 8
  - commercial_blueprint_node    (commercializer)       Phase 8
  - CyberPhysicalEngine          (fabrication_engine)   Phase 9
  - fabrication_node             (fabrication_engine)   Phase 9
  - RegulatoryEngine             (regulatory_engine)    Phase 10
  - regulatory_node              (regulatory_engine)    Phase 10
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
from core.audit_ledger import ImmutableAuditLedger, secure_audit_node
from core.commercializer import (
    CommercialOrchestrator,
    PriorArtConflictError,
    commercial_blueprint_node,
)
from core.fabrication_engine import CyberPhysicalEngine, fabrication_node
from core.regulatory_engine import RegulatoryEngine, regulatory_node

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
    "ImmutableAuditLedger",
    "secure_audit_node",
    "CommercialOrchestrator",
    "PriorArtConflictError",
    "commercial_blueprint_node",
    "CyberPhysicalEngine",
    "fabrication_node",
    "RegulatoryEngine",
    "regulatory_node",
]

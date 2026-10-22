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

# Lazy exports (PEP 562). Importing a light submodule such as core.state
# must not pull in heavy optional dependencies (PyMuPDF, Neo4j,
# sentence-transformers, boto3). Each name below loads its module on first
# use, so `from core import X` behaves exactly as before.

import importlib

_EXPORTS = {
    "get_deterministic_generator": "core.llm_binding",
    "HypothesisPayload": "core.llm_binding",
    "ingest_pdfs": "core.ingest_pdfs",
    "RedTeamEvaluator": "core.red_team",
    "AdversarialVetoError": "core.red_team",
    "compile_tier1_dossier": "core.compiler",
    "run_ingestion": "core.ingest_arxiv",
    "Neo4jIngestionEngine": "core.ingest_arxiv",
    "ExtractedPaper": "core.ingest_arxiv",
    "app_executor": "core.master_orchestrator",
    "ProductionResearchState": "core.master_orchestrator",
    "ConstitutionalLoopError": "core.master_orchestrator",
    "build_orchestrator": "core.master_orchestrator",
    "ImmutableAuditLedger": "core.audit_ledger",
    "secure_audit_node": "core.audit_ledger",
    "CommercialOrchestrator": "core.commercializer",
    "PriorArtConflictError": "core.commercializer",
    "commercial_blueprint_node": "core.commercializer",
    "CyberPhysicalEngine": "core.fabrication_engine",
    "fabrication_node": "core.fabrication_engine",
    "RegulatoryEngine": "core.regulatory_engine",
    "regulatory_node": "core.regulatory_engine",
}

__all__ = list(_EXPORTS)


def __getattr__(name):
    module = _EXPORTS.get(name)
    if module is None:
        raise AttributeError(f"module 'core' has no attribute {name!r}")
    value = getattr(importlib.import_module(module), name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(__all__))

"""
core/__init__.py — Constitutional Engine Core Package

Exposes the primary entry points for Phase 2:
  - get_deterministic_generator  (llm_binding)
  - ingest_pdfs                  (ingest_pdfs)
"""

from core.llm_binding import get_deterministic_generator, HypothesisPayload
from core.ingest_pdfs import ingest_pdfs

__all__ = [
    "get_deterministic_generator",
    "HypothesisPayload",
    "ingest_pdfs",
]

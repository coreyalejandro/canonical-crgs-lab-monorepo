"""
langgraph_engine.py — LangGraph Backend Entry Point

This module satisfies the Phase 1 Makefile verify target:
    docker-compose run --rm constitutional_engine python -c \
        "import langgraph_engine; print('LangGraph Backend Verified.')"

In Phase 1 this was a stub.  From Phase 5 onward it re-exports the
compiled master orchestrator so any code that imports 'langgraph_engine'
gets the live closed-loop pipeline.

Constitutional contract:
    This file is the stable public import surface for the orchestrator.
    Internal implementation lives in core/master_orchestrator.py.
    All Phases 1–5 Makefile targets that reference this module continue
    to work without modification.
"""

from core.master_orchestrator import (
    app_executor,
    ProductionResearchState,
    ConstitutionalLoopError,
    build_orchestrator,
)

__all__ = [
    "app_executor",
    "ProductionResearchState",
    "ConstitutionalLoopError",
    "build_orchestrator",
]

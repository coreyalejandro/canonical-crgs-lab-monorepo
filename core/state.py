"""
core/state.py — Strict Pydantic ResearchState

Phase 13 Build Contract — Section III.

Strict=True enforces Article 3 (clean code, deterministic typing).
physical_outcome_spec enforces Article 5 (backwards design).
active_role enforces Article 9 (hybrid role fluidity).
"""

from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field


class ResearchState(BaseModel):
    model_config = ConfigDict(strict=True)   # Article 3

    # Article 9: Role fluidity
    active_role: Literal[
        "AI_Research_Scientist", "AI_Research_Engineer"
    ] = "AI_Research_Scientist"

    # Article 5: Backwards design anchor — mandatory before generation
    physical_outcome_spec: str = Field(
        default="",
        description="Concrete physical outcome (e.g., 'CAD model of a 10x10mm heat sink')",
    )

    research_query:         str                                             = ""
    visionary_hypothesis:   Optional[str]                                  = None
    verifier_validation:    Optional[str]                                  = None
    self_validation_status: Literal["PENDING", "PASSED", "FAILED"]        = "PENDING"
    human_signature_hash:   Optional[str]                                  = None
    traceability_chain:     list[str]                                      = []

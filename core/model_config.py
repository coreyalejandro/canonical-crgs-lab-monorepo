"""
core/model_config.py — Immutable MoE Model Configuration

Phase 13 Build Contract — Section IV.

frozen=True dataclass means temperatures cannot be changed at runtime.
Article 10: Visionary at temp>=1.0, Verifier at temp=0.0.

Reads LM_STUDIO_MODEL from env so the local LM Studio backend is used
instead of OpenAI cloud — free, no credits required.
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ImmutableModelConfig:
    visionary_model: str  = os.getenv("LM_STUDIO_MODEL", "openai/gpt-oss-20b")
    visionary_temp:  float = 1.0          # Article 10 — immutable
    verifier_model:  str  = os.getenv("LM_STUDIO_MODEL", "openai/gpt-oss-20b")
    verifier_temp:   float = 0.0          # Article 10 — immutable
    endpoint:        str  = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")


CONFIG = ImmutableModelConfig()

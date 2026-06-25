"""
core/llm_binding.py — Deterministic LLM Binding

Section IV of the Phase 2 Build Contract.

Enforces:
  - temperature=0.0  — eliminates stochastic variability
  - Pydantic schema  — structured output; any conversational fluff raises
                       OutputParserException and halts the agent loop

Backend resolution order (controlled by env var LLM_BACKEND):
  1. "lmstudio"  — LM Studio local server (default, OpenAI-compatible API at
                   LM_STUDIO_BASE_URL, default http://localhost:1234/v1)
  2. "ollama"    — Ollama local server (OpenAI-compatible at
                   OLLAMA_BASE_URL, default http://localhost:11434/v1)
  3. "openai"    — OpenAI cloud API (requires OPENAI_API_KEY with credits)

Local model note: Qwen3 and other thinking models return reasoning tokens
separately and may return empty content with .with_structured_output().
We use a JSON-extraction chain instead — universally compatible with all
local models regardless of whether they are thinking/reasoning models.

Constitutional contract: the LLM is ALLOWED to reason probabilistically
internally; it is FORCED to output within the rigid HypothesisPayload
schema. If it cannot, execution halts and the constitutional revision
loop increments (see MAX_REVISION_LOOPS in docker-compose.yml).
"""

import json
import os
import re

from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI


# ── Backend configuration ─────────────────────────────────────────────────────

# Set LLM_BACKEND=openai to use cloud OpenAI, =ollama for Ollama.
# Default: lmstudio (free, local, no credits required).
LLM_BACKEND       = os.getenv("LLM_BACKEND", "lmstudio").lower()
LM_STUDIO_URL     = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
OLLAMA_URL        = os.getenv("OLLAMA_BASE_URL",    "http://localhost:11434/v1")

# Model names — override via env vars if you load different models in LM Studio
LM_STUDIO_MODEL   = os.getenv("LM_STUDIO_MODEL",   "openai/gpt-oss-20b")
OLLAMA_MODEL      = os.getenv("OLLAMA_MODEL",       "qwen2.5:7b")
OPENAI_MODEL      = os.getenv("OPENAI_MODEL",       "gpt-4o")


# ── Schema ────────────────────────────────────────────────────────────────────

class HypothesisPayload(BaseModel):
    """
    Immutable output schema for the Generator Agent.

    Every field is required. The Judge Agent validates each claim against
    the Math Sandbox and each citation against the Neo4j Knowledge Graph
    before the payload is accepted as a constitutional research output.
    """

    hypothesis: str = Field(
        description="The scientific hypothesis text — one declarative sentence, falsifiable."
    )
    claims: list[str] = Field(
        description="Ordered list of factual claims that together constitute evidence "
                    "for the hypothesis. Each claim must be independently verifiable."
    )
    citations: list[str] = Field(
        description="Exact Neo4j node IDs (e.g. 'paper:CCD-2024-001') referencing the "
                    "source document for each claim. Length must equal len(claims)."
    )
    validation_code: str = Field(
        description="Python code using SymPy (and optionally pandas/numpy) that "
                    "mathematically proves or numerically verifies the claims. "
                    "Must execute in under 10 seconds. Must print a final verdict line."
    )


# ── JSON schema prompt (local-model-compatible structured output) ─────────────

_SCHEMA_FIELDS = """
{
  "hypothesis": "<one falsifiable declarative sentence>",
  "claims": ["<claim 1>", "<claim 2>", "<claim 3>"],
  "citations": ["paper:REF-001", "paper:REF-002", "paper:REF-003"],
  "validation_code": "from sympy import symbols\\n# ... SymPy proof code ..."
}"""

_JSON_SYSTEM_PROMPT = (
    "You are a Tier-1 constitutional AI research scientist. "
    "Respond ONLY with a single valid JSON object matching this exact schema — "
    "no markdown fences, no commentary, no thinking tags in the output:\n"
    + _SCHEMA_FIELDS
)


def _extract_json(raw: str) -> dict:
    """
    Extract and parse the first JSON object from a model response.
    Handles thinking-model outputs where content may be wrapped in <think> tags
    or prefixed with reasoning text.
    """
    # Strip <think>...</think> blocks (Qwen3, DeepSeek-R1, etc.)
    raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
    # Strip markdown code fences
    raw = re.sub(r"```(?:json)?", "", raw).replace("```", "").strip()
    # Find first { ... } block
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in model output:\n{raw[:400]}")
    return json.loads(match.group())


class _LocalStructuredChain:
    """
    Drop-in replacement for llm.with_structured_output(HypothesisPayload).
    Works with any OpenAI-compatible local model including thinking models.
    """

    def __init__(self, llm: ChatOpenAI) -> None:
        self._llm = llm

    def invoke(self, prompt: str) -> HypothesisPayload:
        messages = [
            {"role": "system", "content": _JSON_SYSTEM_PROMPT},
            {"role": "user",   "content": prompt},
        ]
        response = self._llm.invoke(messages)
        # Extract text — handles both str and AIMessage
        raw_text: str = (
            response if isinstance(response, str)
            else getattr(response, "content", str(response))
        )
        data = _extract_json(raw_text)
        return HypothesisPayload(**data)


# ── Factory ───────────────────────────────────────────────────────────────────

def _build_llm() -> ChatOpenAI:
    """Instantiate the correct ChatOpenAI client based on LLM_BACKEND."""
    if LLM_BACKEND == "openai":
        print(f"[llm_binding] Backend: OpenAI cloud ({OPENAI_MODEL})")
        return ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=0.0,
            max_retries=3,
            model_kwargs={"seed": 42},
        )
    if LLM_BACKEND == "ollama":
        print(f"[llm_binding] Backend: Ollama local ({OLLAMA_MODEL} @ {OLLAMA_URL})")
        return ChatOpenAI(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_URL,
            api_key="ollama",
            temperature=0.0,
            max_retries=3,
        )
    # Default: LM Studio
    print(f"[llm_binding] Backend: LM Studio local ({LM_STUDIO_MODEL} @ {LM_STUDIO_URL})")
    return ChatOpenAI(
        model=LM_STUDIO_MODEL,
        base_url=LM_STUDIO_URL,
        api_key="lm-studio",
        temperature=0.0,
        max_retries=3,
    )


def get_deterministic_generator() -> object:
    """
    Return a structured-output chain bound to absolute zero temperature.

    For OpenAI cloud: uses native .with_structured_output() (best reliability).
    For local models: uses _LocalStructuredChain — JSON prompt + regex extraction,
    which works with all local models including Qwen3 thinking models.

    Usage:
        generator = get_deterministic_generator()
        payload: HypothesisPayload = generator.invoke("Generate a hypothesis about...")
    """
    llm = _build_llm()

    if LLM_BACKEND == "openai":
        # Native OpenAI structured output — most reliable for cloud
        return llm.with_structured_output(HypothesisPayload)

    # Local model — use JSON extraction chain (works with thinking models)
    return _LocalStructuredChain(llm)


def get_raw_llm() -> ChatOpenAI:
    """
    Return the raw ChatOpenAI client (no structured output binding).
    Used by Red Team and other nodes that build their own prompt chains
    via LangChain's pipe operator (prompt | llm).
    """
    return _build_llm()

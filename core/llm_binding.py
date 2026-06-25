"""
core/llm_binding.py — Deterministic LLM Binding

Section IV of the Phase 2 Build Contract.

Enforces:
  - temperature=0.0  — eliminates stochastic variability
  - seed=42          — forces exact reproducibility across runs
  - Pydantic schema  — structured output; any conversational fluff raises
                       OutputParserException and halts the agent loop

Constitutional contract: the LLM is ALLOWED to reason probabilistically
internally; it is FORCED to output within the rigid HypothesisPayload
schema. If it cannot, execution halts and the constitutional revision
loop increments (see MAX_REVISION_LOOPS in docker-compose.yml).
"""

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI


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


def get_deterministic_generator() -> object:
    """
    Return a LangChain structured-output chain bound to absolute zero temperature.

    The returned chain accepts a prompt string and outputs a HypothesisPayload.
    Any response that does not conform to the schema raises OutputParserException,
    which the LangGraph constitutional loop catches and routes to the Judge Agent
    for revision (up to MAX_REVISION_LOOPS attempts).

    Usage:
        generator = get_deterministic_generator()
        payload: HypothesisPayload = generator.invoke("Generate a hypothesis about...")
    """
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.0,       # HARD-CODED — eliminates stochastic variability
        max_retries=3,
        model_kwargs={"seed": 42},  # Force seed for exact reproducibility
    )

    # Bind to structured output — any schema violation raises immediately
    structured_llm = llm.with_structured_output(HypothesisPayload)
    return structured_llm

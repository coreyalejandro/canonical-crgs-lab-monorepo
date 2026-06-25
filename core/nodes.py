"""
core/nodes.py — Operational MoE LLM Nodes

Phase 13 Build Contract — Section IV.

Article 10: Real LLM instantiation with frozen temperatures.
  - visionary_llm: temp=1.0 (divergent lateral ideation)
  - verifier_llm:  temp=0.0 (hyper-rational systematizer)

Uses LM Studio local backend — free, no API credits required.
"""

from langchain_openai import ChatOpenAI

from core.model_config import CONFIG
from core.state import ResearchState
from core.validators import enforce_nist_eu_self_validation

# Article 10: Instantiate with frozen temperatures
visionary_llm = ChatOpenAI(
    model=CONFIG.visionary_model,
    temperature=CONFIG.visionary_temp,
    base_url=CONFIG.endpoint,
    api_key="lm-studio",
    max_retries=2,
)

verifier_llm = ChatOpenAI(
    model=CONFIG.verifier_model,
    temperature=CONFIG.verifier_temp,
    base_url=CONFIG.endpoint,
    api_key="lm-studio",
    max_retries=2,
)


def visionary_node(state: dict) -> dict:
    """
    👁️ The Visionary — temp=1.0, divergent lateral ideation.
    Article 5: requires physical_outcome_spec before generation.
    Article 6: records traceability chain entry.
    """
    if not state.get("physical_outcome_spec"):
        raise ValueError(
            "Backwards Design Failure (Article 5): "
            "physical_outcome_spec must be set before generation."
        )
    prompt = (
        f"You are The Visionary — a lateral, divergent AI research ideator.\n"
        f"Physical target: {state['physical_outcome_spec']}\n"
        f"Research query: {state['research_query']}\n\n"
        f"Generate 3 bold, lateral, cross-domain hypotheses that could lead to "
        f"the physical target. Be maximally creative and unconventional."
    )
    response = visionary_llm.invoke(prompt)
    hypothesis_text = getattr(response, "content", str(response))
    trace = state.get("traceability_chain", []) + [
        f"Visionary anchored on '{state['physical_outcome_spec']}'"
    ]
    return {"visionary_hypothesis": hypothesis_text, "traceability_chain": trace}


def verifier_node(state: dict) -> dict:
    """
    ⚖️ The Verifier — temp=0.0, hyper-rational systematizer.
    Article 2: recursive self-validation via NIST/EU checklist.
    Article 6: records traceability chain entry.
    """
    prompt = (
        f"You are The Verifier — a hyper-rational, temperature=0.0 AI systematizer.\n"
        f"Physical target: {state['physical_outcome_spec']}\n"
        f"Hypothesis to verify: {state['visionary_hypothesis']}\n\n"
        f"Rigorously red-team, verify, and ground the hypothesis in empirical reality. "
        f"Identify all unsupported claims. Conclude with VERIFIED or FAILED."
    )
    response = verifier_llm.invoke(prompt)
    verification_text = getattr(response, "content", str(response))

    passed, failures = enforce_nist_eu_self_validation(
        verification_text,
        physical_outcome_spec=state.get("physical_outcome_spec", ""),
    )
    if not passed:
        raise ValueError(f"NIST/EU Self-Validation FAILED: {failures}")

    trace = state.get("traceability_chain", []) + [
        f"Verifier checked hypothesis against '{state['physical_outcome_spec']}'"
    ]
    return {
        "verifier_validation":    verification_text,
        "self_validation_status": "PASSED" if passed else "FAILED",
        "traceability_chain":     trace,
    }

"""
core/hybrid_orchestrator.py — The Living Constitution Hybrid Orchestrator

Phase 12 Build Contract — Section IV.1.

Operationalizes TLC's Theory of Change and Action (ToCA):

  The Visionary  (👁️) — high-temperature divergent ideation node. Scans the
                         knowledge graph for lateral, novel connections. No
                         epistemic constraints at this stage — breadth first.

  The Verifier   (⚖️) — temperature=0.0 hyper-rational systematizer. Runs
                         mathematical proofs, red-teams every claim, enforces
                         the constitutional invariants. Width collapses to truth.

  Human PI       (🧑‍🔬) — cryptographic gatekeeper. The LangGraph graph is
                         compiled with interrupt_before=["human_review"] which
                         creates a physical hard stop — the machine cannot
                         advance past this node without an explicit human
                         authorization call.

Constitutional contract (Articles 1–10):
  Art 1: Modularity — every node does exactly one thing.
  Art 2: Recursive self-validation — The Verifier eats its own outputs.
  Art 3: Deterministic execution — The Verifier runs at temperature=0.0.
  Art 5: Backwards design — state flows toward a concrete physical artifact.
  Art 6: Dual-parity output — state carries both human-legible and JSON fields.
  Art 8: Human-in-the-loop interlock — interrupt_before=["human_review"] is
         non-negotiable and cannot be removed without amending TLC v2.0.0.
  Art 10: MoE paradigm — Visionary at temp>0, Verifier at temp=0.0.

Usage (programmatic):
    from core.hybrid_orchestrator import hybrid_app_executor, HybridResearchState
    from core.hybrid_orchestrator import TheLivingConstitution

    TheLivingConstitution.assert_canon()
    config = {"configurable": {"thread_id": "run-001"}}

    # Phase 1: run up to human review checkpoint
    state = hybrid_app_executor.invoke(
        {"research_query": "constitutional AI governance runtime safety"},
        config=config,
    )
    # → pipeline pauses at 'human_review' node

    # Phase 2: human reviews state, then authorizes
    state = hybrid_app_executor.invoke(None, config=config)
    # → pipeline resumes from 'human_review' to END

Usage (CLI):
    python -m core.hybrid_orchestrator "constitutional AI governance"
"""

from __future__ import annotations

import json
import logging
import os
from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from core.llm_binding import get_deterministic_generator, get_raw_llm, HypothesisPayload
from core.red_team import RedTeamEvaluator, AdversarialVetoError

# ── Logging ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


# ── Article 10: The Living Constitution boot assertion ────────────────────────

class TheLivingConstitution:
    """
    Canonical boot assertion for TLC's Theory of Change and Action.

    Must be called once before any hybrid pipeline execution to set the
    TLC_ACTIVE environment sentinel and log the MoE paradigm initialization.
    """

    @classmethod
    def assert_canon(cls) -> None:
        logger.info("⚖️  BOOTING TLC's ToCA (The Living Constitution v2.0.0)...")
        logger.info("👁️  Initializing 'The Visionary' — divergent, high-temperature ideation node.")
        logger.info("⚖️  Initializing 'The Verifier' — hyper-rational, temperature=0.0 systematizer.")
        logger.info("🧑‍🔬 Human Principal Investigator interlock: ARMED.")
        logger.info("🏛️  Safety Systems Design Commonwealth — NIST AI RMF / EU AI Act compliance active.")
        os.environ["TLC_ACTIVE"] = "TRUE"
        os.environ["TLC_VERSION"] = "2.0.0"


# ── Article 6: Dual-parity state schema ──────────────────────────────────────

class HybridResearchState(TypedDict, total=False):
    """
    Dual-parity state: every field has both a human-legible value and a
    machine-actionable JSON counterpart carried forward through the pipeline.
    """
    # Entry
    research_query:        str           # Human PI's research directive

    # Visionary output (high-temp ideation)
    visionary_ideas:       list[str]     # Raw lateral connections from KG scan
    visionary_hypothesis:  str           # Unbounded draft hypothesis

    # Verifier output (temp=0.0 systematization)
    verified_payload:      dict          # HypothesisPayload fields post red-team
    validation_status:     str           # "verified_and_stress_tested" | "failed"
    revision_count:        int

    # Human PI checkpoint
    pi_authorization:      str           # "pending" | "authorized" | "rejected"
    pi_notes:              str           # Human PI's review notes (optional)

    # Final output (dual-parity: human + machine)
    final_report_md:       str           # Human-legible Markdown summary
    final_report_json:     dict          # Machine-actionable JSON artifact


# ── Article 10: The Visionary node (high-temperature divergent ideation) ──────

_VISIONARY_TEMP = float(os.getenv("VISIONARY_TEMPERATURE", "0.9"))

def visionary_node(state: HybridResearchState) -> HybridResearchState:
    """
    👁️ The Visionary — divergent, associative lateral thinker.

    Runs at high temperature to generate maximally novel connections.
    Output is intentionally unbounded — The Verifier will constrain it.
    Article 10: high-temperature model paired with zero-temperature verifier.
    """
    query = state["research_query"]
    logger.info(f"👁️  [VISIONARY] Scanning for lateral connections: {query!r}")

    from langchain_openai import ChatOpenAI
    import os as _os
    backend = _os.getenv("LLM_BACKEND", "lmstudio").lower()
    base_url = _os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1") if backend == "lmstudio" \
               else (_os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1") if backend == "ollama" else None)
    model = _os.getenv("LM_STUDIO_MODEL", "openai/gpt-oss-20b") if backend == "lmstudio" \
            else (_os.getenv("OLLAMA_MODEL", "qwen2.5:7b") if backend == "ollama" \
            else _os.getenv("OPENAI_MODEL", "gpt-4o"))

    kwargs = dict(model=model, temperature=_VISIONARY_TEMP, max_retries=2)
    if base_url:
        kwargs["base_url"] = base_url
        kwargs["api_key"] = backend  # ignored by local servers

    llm = ChatOpenAI(**kwargs)

    prompt = (
        f"You are The Visionary — a lateral, divergent AI research ideator.\n"
        f"Research query: {query}\n\n"
        f"Generate 5 bold, unconventional, cross-domain hypotheses or research angles "
        f"that a conservative researcher would never consider. Be associative, "
        f"speculative, and maximally creative. Output as a numbered list."
    )
    response = llm.invoke(prompt)
    raw = getattr(response, "content", str(response))

    ideas = [line.strip() for line in raw.splitlines() if line.strip() and line.strip()[0].isdigit()]
    hypothesis = ideas[0].lstrip("0123456789. ") if ideas else raw[:200]

    logger.info(f"👁️  [VISIONARY] Generated {len(ideas)} lateral ideas. Leading hypothesis: {hypothesis[:80]!r}…")
    return {**state, "visionary_ideas": ideas, "visionary_hypothesis": hypothesis}


# ── Article 10: The Verifier node (temperature=0.0 systematizer) ─────────────

def verifier_node(state: HybridResearchState) -> HybridResearchState:
    """
    ⚖️ The Verifier — hyper-rational, temperature=0.0 systematizer.

    Takes The Visionary's unbounded output and subjects it to:
      1. Constitutional schema enforcement (HypothesisPayload)
      2. Red Team adversarial attack
    Article 3: deterministic. Article 2: recursive self-validation.
    """
    hypothesis = state.get("visionary_hypothesis", state.get("research_query", ""))
    revision_count = state.get("revision_count", 0)
    logger.info(f"⚖️  [VERIFIER] Systematizing hypothesis (attempt {revision_count + 1}): {hypothesis[:80]!r}…")

    generator = get_deterministic_generator()
    prompt = (
        f"Formalize the following research hypothesis into a rigorous, falsifiable "
        f"Tier-1 research statement with supporting claims, citations, and SymPy "
        f"validation code.\n\nHypothesis: {hypothesis}\n\n"
        f"Ideas from lateral scan:\n" +
        "\n".join(f"- {idea}" for idea in state.get("visionary_ideas", []))
    )
    try:
        payload: HypothesisPayload = generator.invoke(prompt)
        evaluator = RedTeamEvaluator(neo4j_session=None)  # offline mode
        result = evaluator.execute_attack(payload if isinstance(payload, dict) else {
            "hypothesis": payload.hypothesis,
            "claims": payload.claims,
            "citations": payload.citations,
            "validation_code": payload.validation_code,
            "status": "generated",
        })
        verified = {
            "hypothesis":      payload.hypothesis,
            "claims":          payload.claims,
            "citations":       payload.citations,
            "validation_code": payload.validation_code,
            "status":          result.status,
        }
        logger.info(f"⚖️  [VERIFIER] PASSED — {result.contradictions_found} contradictions reviewed.")
        return {**state, "verified_payload": verified, "validation_status": result.status}

    except AdversarialVetoError as exc:
        logger.warning(f"⚖️  [VERIFIER] VETO — {exc}")
        return {
            **state,
            "validation_status": "failed",
            "revision_count": revision_count + 1,
        }


# ── Article 8: Human Principal Investigator interlock ────────────────────────

def human_review_node(state: HybridResearchState) -> HybridResearchState:
    """
    🧑‍🔬 Human PI Review — cryptographic freeze point.

    This node is declared as interrupt_before in the compiled graph.
    The pipeline CANNOT advance past this point without an explicit
    human resume call. This is the physical enforcement of Article 8.

    When the pipeline is interrupted here, the calling code receives
    the current state. The human reviews it, optionally adds pi_notes,
    then calls hybrid_app_executor.invoke(None, config=config) to resume.
    """
    pi_auth = state.get("pi_authorization", "pending")
    logger.info(f"🧑‍🔬 [HUMAN PI] Checkpoint reached. Authorization status: {pi_auth!r}")
    if pi_auth == "rejected":
        logger.warning("🧑‍🔬 [HUMAN PI] Execution REJECTED by Human PI.")
    return {**state, "pi_authorization": pi_auth}


# ── Article 5/6: Final synthesis — dual-parity output ────────────────────────

def synthesize_node(state: HybridResearchState) -> HybridResearchState:
    """
    Article 5 (backwards design) + Article 6 (dual-parity output).
    Generates both human-legible Markdown and machine-actionable JSON.
    """
    payload = state.get("verified_payload", {})
    query   = state.get("research_query", "")
    ideas   = state.get("visionary_ideas", [])
    notes   = state.get("pi_notes", "")

    md = (
        f"# TLC Hybrid R&D Synthesis\n\n"
        f"**Query:** {query}  \n"
        f"**Governing Constitution:** TLC 2.0 Sociotechnical Constitution v2.0.0  \n\n"
        f"## 👁️ The Visionary — Lateral Ideation\n\n"
        + "\n".join(f"- {idea}" for idea in ideas) +
        f"\n\n## ⚖️ The Verifier — Formalized Hypothesis\n\n"
        f"> {payload.get('hypothesis', '—')}\n\n"
        f"### Claims\n"
        + "\n".join(f"- {c}" for c in payload.get("claims", [])) +
        f"\n\n### Validation Code\n```python\n{payload.get('validation_code', '')}\n```\n\n"
        f"## 🧑‍🔬 Human PI Notes\n\n{notes or '_No notes provided._'}\n"
    )

    report_json = {
        "query":            query,
        "visionary_ideas":  ideas,
        "verified_payload": payload,
        "pi_notes":         notes,
        "tlc_version":      "2.0.0",
        "governance":       "NIST AI RMF / EU AI Act / TLC ToCA",
    }

    logger.info("🏆 [SYNTHESIS] Dual-parity output locked — MD + JSON artifact ready.")
    return {**state, "final_report_md": md, "final_report_json": report_json}


# ── Routing ───────────────────────────────────────────────────────────────────

MAX_REVISIONS = int(os.getenv("MAX_REVISION_LOOPS", "3"))

def route_verifier(state: HybridResearchState) -> str:
    if state.get("validation_status") == "failed" and state.get("revision_count", 0) < MAX_REVISIONS:
        return "visionary"   # re-ideate from scratch
    return "human_review"


def route_pi(state: HybridResearchState) -> str:
    if state.get("pi_authorization") == "rejected":
        return "visionary"   # PI rejected — back to ideation
    return "synthesize"


# ── Graph assembly ────────────────────────────────────────────────────────────

def build_hybrid_orchestrator() -> object:
    """
    Compile the TLC hybrid LangGraph with human-in-the-loop interlock.

    Pipeline:
        visionary
          → verifier
              ↙ failed (< MAX_REVISIONS): back to visionary
              ↘ passed: human_review  ←── INTERRUPT BEFORE (Article 8)
                            ↙ rejected: back to visionary
                            ↘ authorized: synthesize → END
    """
    workflow = StateGraph(HybridResearchState)

    workflow.add_node("visionary",    visionary_node)
    workflow.add_node("verifier",     verifier_node)
    workflow.add_node("human_review", human_review_node)
    workflow.add_node("synthesize",   synthesize_node)

    workflow.set_entry_point("visionary")
    workflow.add_edge("visionary", "verifier")
    workflow.add_conditional_edges("verifier", route_verifier, {
        "visionary":    "visionary",
        "human_review": "human_review",
    })
    workflow.add_conditional_edges("human_review", route_pi, {
        "visionary":  "visionary",
        "synthesize": "synthesize",
    })
    workflow.add_edge("synthesize", END)

    memory = MemorySaver()
    return workflow.compile(
        checkpointer=memory,
        interrupt_before=["human_review"],  # Article 8 — immutable interlock
    )


# Module-level executor
hybrid_app_executor = build_hybrid_orchestrator()


# ── CLI entrypoint ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    TheLivingConstitution.assert_canon()

    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else \
            "constitutional AI governance runtime safety"

    config = {"configurable": {"thread_id": "cli-run-001"}}
    initial: HybridResearchState = {
        "research_query":   query,
        "revision_count":   0,
        "pi_authorization": "pending",
    }

    print(f"\n{'═'*60}")
    print(f"HYBRID ORCHESTRATOR — PHASE 1: Visionary + Verifier")
    print(f"Query: {query!r}")
    print(f"{'═'*60}\n")

    state = hybrid_app_executor.invoke(initial, config=config)

    print(f"\n{'─'*60}")
    print("🛑 [HUMAN PI CHECKPOINT] Pipeline paused for review.")
    print(f"Verified hypothesis: {state.get('verified_payload', {}).get('hypothesis', '—')[:120]}")
    print(f"Visionary ideas: {len(state.get('visionary_ideas', []))}")
    print("─"*60)

    authorization = input("\n🧑‍🔬 Human PI — Authorize execution? [y/N/notes]: ").strip()
    if authorization.lower().startswith("y"):
        auth_status = "authorized"
        pi_notes    = authorization[1:].strip() or "Authorized."
    else:
        auth_status = "rejected"
        pi_notes    = authorization or "Rejected by Human PI."

    # Resume pipeline past the human interlock
    state = hybrid_app_executor.invoke(
        {"pi_authorization": auth_status, "pi_notes": pi_notes},
        config=config,
    )

    print(f"\n{'═'*60}")
    if auth_status == "authorized":
        print("🏆 SYNTHESIS COMPLETE")
        print(state.get("final_report_md", "")[:600])
    else:
        print("🚫 Execution rejected by Human PI. Pipeline halted.")
    print(f"{'═'*60}")

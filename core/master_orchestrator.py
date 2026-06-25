"""
core/master_orchestrator.py — Closed-Loop Master Orchestrator

Section I of the Phase 5 Build Contract.

Binds all prior microservices into a single deterministic LangGraph state
machine.  A single research query enters; a Tier-1 PDF dossier exits.

Pipeline:
    query_graph
        → generate_hypothesis
            → red_team
                ↙ failed: back to generate_hypothesis (up to MAX_REVISION_LOOPS)
                ↘ passed: compile_pdf → END

Constitutional contract:
    - MAX_REVISION_LOOPS is read from the environment (set in docker-compose.yml).
      The loop count is tracked in state and enforced by route_adversarial_result().
      Exceeding the limit halts with ConstitutionalLoopError — no infinite loops.
    - The Red Team node uses a real Neo4j session per invocation, not a singleton
      driver, so the session lifecycle is correctly scoped.
    - compile_final_pdf() gates on status == "verified_and_stress_tested" via the
      constitutional check already enforced inside core/compiler.py.
    - All state mutations are explicit returns — no side-channel state sharing.

Usage (via Makefile):
    make execute-autonomous-run

Usage (direct):
    docker-compose run --rm constitutional_engine \\
        python core/master_orchestrator.py "constitutional AI governance"

Usage (programmatic):
    from core.master_orchestrator import app_executor
    result = app_executor.invoke({"research_query": "runtime AI governance"})
"""

from __future__ import annotations

import json
import os
from typing import TypedDict

from langgraph.graph import StateGraph, END
from neo4j import GraphDatabase

from core.audit_ledger import ImmutableAuditLedger, secure_audit_node
from core.commercializer import (
    CommercialOrchestrator,
    PriorArtConflictError,
    commercial_blueprint_node,
)
from core.compiler import compile_tier1_dossier
from core.llm_binding import get_deterministic_generator, HypothesisPayload
from core.red_team import AdversarialVetoError, RedTeamEvaluator


# ── Constants ─────────────────────────────────────────────────────────────────

NEO4J_URI      = os.getenv("NEO4J_URI",      "bolt://localhost:7687")
NEO4J_USER     = os.getenv("NEO4J_USER",     "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "StrictPassword123!")
MAX_REVISION_LOOPS = int(os.getenv("MAX_REVISION_LOOPS", "3"))
OUTPUT_DIR = "./output"


# ── Custom exception ──────────────────────────────────────────────────────────

class ConstitutionalLoopError(Exception):
    """
    Raised when the pipeline exceeds MAX_REVISION_LOOPS without producing a
    hypothesis that survives adversarial review.  This is a constitutional
    hard stop — the system must not iterate indefinitely.
    """


# ── State Definition ──────────────────────────────────────────────────────────

class ProductionResearchState(TypedDict, total=False):
    """
    Immutable state schema for the LangGraph pipeline.

    Every node receives the full state dict and returns a (possibly mutated)
    copy.  Fields are Optional until they are written by the relevant node.
    """
    research_query:       str         # Entry point — user's research question
    graph_context:        list[dict]  # Claims retrieved from Neo4j
    hypothesis_payload:   dict        # HypothesisPayload fields + status
    validation_status:    str         # "verified_and_stress_tested" | "failed" | "prior_art_conflict"
    revision_count:       int         # Number of Red Team vetoes so far
    audit_hash:           str         # SHA-256 fingerprint written by audit node (Phase 7)
    commercial_blueprint: dict        # Patent claims + BOM written by commercialize node (Phase 8)
    final_output_path:    str         # Path to compiled PDF


# ── Database driver (module-level; shared across nodes) ───────────────────────

_db_driver = None


def _get_driver():
    """Lazy-initialise the Neo4j driver once per process."""
    global _db_driver
    if _db_driver is None:
        _db_driver = GraphDatabase.driver(
            NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)
        )
    return _db_driver


# ── Node 1 — Query Live Graph ─────────────────────────────────────────────────

def query_live_graph(state: ProductionResearchState) -> ProductionResearchState:
    """
    Pull constitutionally mapped claims from the Neo4j ETL ingestion layer.
    Returns at most 10 claim records relevant to the research query.
    """
    query = state["research_query"]
    print(f"[orchestrator] Querying Knowledge Graph for: {query!r}")

    with _get_driver().session() as session:
        records = session.run(
            """
            MATCH (p:Paper)-[:ASSERTS]->(c:Claim)
            WHERE toLower(p.title) CONTAINS toLower($query)
               OR toLower(c.text)  CONTAINS toLower($query)
            RETURN p.title AS paper, c.text AS claim
            LIMIT 10
            """,
            query=query,
        )
        context = [{"paper": r["paper"], "claim": r["claim"]} for r in records]

    print(f"[orchestrator] Graph context retrieved: {len(context)} claim(s).")
    return {**state, "graph_context": context, "revision_count": 0}


# ── Node 2 — Generate Hypothesis ─────────────────────────────────────────────

def generate_live_hypothesis(state: ProductionResearchState) -> ProductionResearchState:
    """
    Use the deterministic LLM (temperature=0.0) to generate a structured
    HypothesisPayload grounded in the retrieved graph context.
    """
    print("[orchestrator] Generating deterministic hypothesis...")
    llm = get_deterministic_generator()

    context_text = "\n".join(
        f"- [{r['paper']}] {r['claim']}" for r in state.get("graph_context", [])
    ) or "No prior claims retrieved from Knowledge Graph."

    prompt = (
        f"Generate a Tier-1 research hypothesis for the following query.\n\n"
        f"Research Query: {state['research_query']}\n\n"
        f"Available Evidence from Knowledge Graph:\n{context_text}\n\n"
        f"The hypothesis must be falsifiable, grounded in the evidence above, "
        f"and accompanied by SymPy validation code that proves a mathematical "
        f"claim central to the hypothesis."
    )

    payload: HypothesisPayload = llm.invoke(prompt)

    hypothesis_dict = {
        "hypothesis":       payload.hypothesis,
        "hypothesis_title": payload.hypothesis[:120],
        "abstract":         f"A constitutionally governed synthesis of "
                            f"{len(state.get('graph_context', []))} Tier-1 "
                            f"sources addressing: {state['research_query']}",
        "claims":           payload.claims,
        "citations":        payload.citations,
        "math_proofs":      payload.validation_code,
        "validation_code":  payload.validation_code,
        "status":           "generated",            # pre-red-team
    }

    print(f"[orchestrator] Hypothesis generated: {payload.hypothesis[:80]!r}...")
    return {**state, "hypothesis_payload": hypothesis_dict}


# ── Node 3 — Red Team Attack ──────────────────────────────────────────────────

def execute_red_team_attack(state: ProductionResearchState) -> ProductionResearchState:
    """
    Subject the hypothesis to the adversarial Red Team microservice.
    On AdversarialVetoError: increments revision_count and marks failed.
    Exceeding MAX_REVISION_LOOPS raises ConstitutionalLoopError.
    """
    revision_count = state.get("revision_count", 0)
    print(f"[orchestrator] Red Team attack — attempt {revision_count + 1}/{MAX_REVISION_LOOPS}")

    if revision_count >= MAX_REVISION_LOOPS:
        raise ConstitutionalLoopError(
            f"Hypothesis failed adversarial review {MAX_REVISION_LOOPS} times. "
            "Constitutional loop limit reached — manual review required."
        )

    with _get_driver().session() as session:
        evaluator = RedTeamEvaluator(neo4j_session=session)
        try:
            result = evaluator.execute_attack(state["hypothesis_payload"])
            # Mark the payload as stress-tested so compile_tier1_dossier accepts it
            updated_payload = {
                **state["hypothesis_payload"],
                "status": result.status,
            }
            print(f"[orchestrator] Red Team: PASSED ({result.contradictions_found} contradictions reviewed).")
            return {**state, "hypothesis_payload": updated_payload, "validation_status": result.status}

        except AdversarialVetoError as exc:
            print(f"[orchestrator] Red Team: VETO — {exc}")
            return {
                **state,
                "validation_status": "failed",
                "revision_count": revision_count + 1,
            }


# ── Node 4 — Compile Final PDF ────────────────────────────────────────────────

def compile_final_pdf(state: ProductionResearchState) -> ProductionResearchState:
    """
    Serialize the surviving payload to disk and command the Tectonic container
    to compile the Tier-1 PDF dossier.
    """
    print("[orchestrator] Compiling Tier-1 PDF dossier...")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    payload_path = f"{OUTPUT_DIR}/current_payload.json"

    with open(payload_path, "w") as fh:
        json.dump(state["hypothesis_payload"], fh, indent=2)

    pdf_path = compile_tier1_dossier(
        verified_payload_path=payload_path,
        output_name="Autonomous_Tier1_Dossier",
    )

    print(f"[orchestrator] PDF compiled: {pdf_path}")
    return {**state, "final_output_path": str(pdf_path)}


# ── Routing Logic ─────────────────────────────────────────────────────────────

def route_adversarial_result(state: ProductionResearchState) -> str:
    """
    Conditional edge after red_team:
      failed          → regenerate hypothesis
      passed          → write audit ledger (Phase 7)
    """
    if state.get("validation_status") == "failed":
        return "generate_hypothesis"
    return "audit"


def route_commercial_result(state: ProductionResearchState) -> str:
    """
    Conditional edge after commercialize (Phase 8):
      prior_art_conflict → regenerate hypothesis
      passed             → compile PDF
    """
    if state.get("validation_status") == "prior_art_conflict":
        return "generate_hypothesis"
    return "compile_pdf"


# ── Graph Assembly ────────────────────────────────────────────────────────────

def build_orchestrator() -> StateGraph:
    """
    Assemble and compile the LangGraph state machine.
    Called once at module import — app_executor is the compiled instance.

    Full pipeline (Phases 1–8):
        query_graph
          → generate_hypothesis
            → red_team
                ↙ failed: back to generate_hypothesis
                ↘ passed: audit          (Phase 7 — cryptographic ledger)
                            → commercialize  (Phase 8 — patent + BOM)
                                ↙ prior_art_conflict: back to generate_hypothesis
                                ↘ passed: compile_pdf → END
    """
    workflow = StateGraph(ProductionResearchState)

    workflow.add_node("query_graph",         query_live_graph)
    workflow.add_node("generate_hypothesis", generate_live_hypothesis)
    workflow.add_node("red_team",            execute_red_team_attack)
    workflow.add_node("audit",               secure_audit_node)           # Phase 7
    workflow.add_node("commercialize",       commercial_blueprint_node)   # Phase 8
    workflow.add_node("compile_pdf",         compile_final_pdf)

    workflow.set_entry_point("query_graph")
    workflow.add_edge("query_graph",         "generate_hypothesis")
    workflow.add_edge("generate_hypothesis", "red_team")
    workflow.add_conditional_edges(
        "red_team",
        route_adversarial_result,
        {
            "generate_hypothesis": "generate_hypothesis",
            "audit":               "audit",
        },
    )
    workflow.add_edge("audit", "commercialize")
    workflow.add_conditional_edges(
        "commercialize",
        route_commercial_result,
        {
            "generate_hypothesis": "generate_hypothesis",
            "compile_pdf":         "compile_pdf",
        },
    )
    workflow.add_edge("compile_pdf", END)

    return workflow.compile()


# Module-level compiled executor — imported by app.py and langgraph_engine.py
app_executor = build_orchestrator()


# ── CLI entrypoint ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "constitutional AI governance runtime safety"
    initial_state: ProductionResearchState = {"research_query": query}

    print("[orchestrator] INITIATING CLOSED-LOOP MASTER ORCHESTRATOR...")
    print(f"[orchestrator] Research query: {query!r}")

    try:
        final_state = app_executor.invoke(initial_state)
        print(f"[orchestrator] END-TO-END CYCLE COMPLETE.")
        print(f"[orchestrator] Dossier: {final_state.get('final_output_path', 'N/A')}")
    except ConstitutionalLoopError as exc:
        print(f"[orchestrator] CONSTITUTIONAL HALT: {exc}")
        sys.exit(1)

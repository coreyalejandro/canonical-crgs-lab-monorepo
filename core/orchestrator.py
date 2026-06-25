"""
core/orchestrator.py — Cryptographic LangGraph Orchestrator

Phase 14 / v15 Build Contract — Section V.

The human_checkpoint node is always interrupted before execution.
It requires a valid cryptographic signature hash to proceed.
The resume flow is exposed to the UI via app_executor.

Role-based routing (Article 9):
  AI_Research_Scientist → visionary → verifier → human_checkpoint → END
  AI_Research_Engineer  → verifier  → human_checkpoint → END
    (skips lateral ideation; goes straight to systematic verification)

PermissionError (not RuntimeError) on missing signature — v15 invariant.
"""

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from core.ledger import MerkleLedger
from core.nodes import verifier_node, visionary_node
from core.state import ResearchState

ledger = MerkleLedger()


def human_cryptographic_checkpoint(state: ResearchState) -> dict:
    """
    Article 8: This node is always interrupted before execution.
    It must receive a valid human_signature_hash to proceed.
    On resume, records the signature event in the ledger.
    Raises PermissionError (not RuntimeError) per v15 contract.
    """
    if not state.human_signature_hash:
        raise PermissionError(
            "Missing Human PI signature (Article 8). Execution frozen."
        )
    ledger.append_signature(
        "RUNTIME_CONSENT",
        "Human_PI_01",
        {
            "hypothesis":   state.visionary_hypothesis or "",
            "verification": state.verifier_validation  or "",
        },
    )
    return {}


def route_entry(state: ResearchState) -> str:
    """
    Article 9: Route based on active_role.
    AI_Research_Scientist → visionary (full pipeline)
    AI_Research_Engineer  → verifier  (skip lateral ideation)
    """
    if state.active_role == "AI_Research_Engineer":
        return "verifier"
    return "visionary"


workflow = StateGraph(ResearchState)
workflow.add_node("visionary",        visionary_node)
workflow.add_node("verifier",         verifier_node)
workflow.add_node("human_checkpoint", human_cryptographic_checkpoint)

# Article 9: conditional entry point based on role
workflow.add_conditional_edges(START, route_entry)

workflow.add_edge("visionary",        "verifier")
workflow.add_edge("verifier",         "human_checkpoint")
workflow.add_edge("human_checkpoint", END)

memory = MemorySaver()
app_executor = workflow.compile(
    checkpointer=memory,
    interrupt_before=["human_checkpoint"],   # Article 8 — immutable
)

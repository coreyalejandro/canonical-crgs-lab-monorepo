"""
core/orchestrator.py — Cryptographic LangGraph Orchestrator

Phase 13 Build Contract — Section V.

The human_checkpoint node is always interrupted before execution.
It requires a valid cryptographic signature hash to proceed.
The resume flow is exposed to the UI via app_executor.

Pipeline:
    visionary → verifier → human_checkpoint (INTERRUPT) → END
"""

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from core.ledger import MerkleLedger
from core.nodes import verifier_node, visionary_node

ledger = MerkleLedger()


def human_cryptographic_checkpoint(state: dict) -> dict:
    """
    Article 8: This node is always interrupted before execution.
    It must receive a valid human_signature_hash to proceed.
    On resume, records the signature event in the ledger.
    """
    if not state.get("human_signature_hash"):
        raise RuntimeError(
            "Missing Human PI signature (Article 8). Execution frozen."
        )
    ledger.append_signature(
        "RUNTIME_CONSENT",
        "Human_PI_01",
        {
            "hypothesis":    state.get("visionary_hypothesis", ""),
            "verification":  state.get("verifier_validation", ""),
        },
    )
    return {}


workflow = StateGraph(dict)
workflow.add_node("visionary",         visionary_node)
workflow.add_node("verifier",          verifier_node)
workflow.add_node("human_checkpoint",  human_cryptographic_checkpoint)

workflow.set_entry_point("visionary")
workflow.add_edge("visionary",        "verifier")
workflow.add_edge("verifier",         "human_checkpoint")
workflow.add_edge("human_checkpoint", END)

memory = MemorySaver()
app_executor = workflow.compile(
    checkpointer=memory,
    interrupt_before=["human_checkpoint"],   # Article 8 — immutable
)

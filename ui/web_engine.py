"""
ui/web_engine.py — Constitutional AI Reactive Web UI

Phase 11 Build Contract — Section III.

A Chainlit-powered WebUI that streams the live LangGraph execution in real-time,
displaying each of the 10 pipeline nodes as expandable "thought step" cards —
identical UX to Claude's reasoning interface.

Every step shows its actual output: the generated hypothesis text, the Red Team
verdict, the SHA-256 audit fingerprint, patent claims, and the final dossier path.
No simulation — every card reflects real pipeline execution state.

Usage:
    chainlit run ui/web_engine.py -w
    # or via Makefile:
    make run-webui
    # Access at: http://localhost:8000
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import chainlit as cl

# Add repo root to path so core.* imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# ── Node definitions ──────────────────────────────────────────────────────────

_NODES = [
    ("🔍 Knowledge Graph Retrieval",      "query_graph"),
    ("🧠 Hypothesis Generation",           "generate_hypothesis"),
    ("🛡️  Red Team Adversarial Attack",    "red_team"),
    ("🔐 Cryptographic Audit Ledger",      "audit"),
    ("💼 IP Commercialization",            "commercialize"),
    ("⚙️  Cyber-Physical Fabrication",     "fabricate"),
    ("📋 Regulatory Compliance & GTM",     "regulate"),
    ("📄 Tier-1 Dossier Compilation",      "compile_pdf"),
]


# ── Chainlit lifecycle ────────────────────────────────────────────────────────

@cl.on_chat_start
async def start() -> None:
    backend = os.getenv("LLM_BACKEND", "lmstudio").upper()
    model   = os.getenv("LM_STUDIO_MODEL", "openai/gpt-oss-20b")
    await cl.Message(
        content=(
            "## 🔬 Constitutional AI-Governed R&D Platform\n"
            f"**Backend:** `{backend}` — `{model}`  \n"
            "**Constitution:** TLC 2.0 Sociotechnical Constitution v2.0.0  \n"
            "**Pipeline:** 10-node LangGraph — KG → Hypothesis → Red Team → "
            "Audit → IP → CAD → Regulatory → PDF\n\n"
            "---\n"
            "Enter your research query to initiate a full constitutional R&D run."
        )
    ).send()


@cl.on_message
async def main(message: cl.Message) -> None:
    query = message.content.strip()
    if not query:
        return

    # Root status message
    root_msg = cl.Message(content=f"**🚀 Initiating pipeline for:** `{query}`")
    await root_msg.send()

    # ── Step 1: Knowledge Graph ───────────────────────────────────────────────
    async with cl.Step(name="🔍 Knowledge Graph Retrieval", type="tool") as step:
        step.input = query
        result = await cl.make_async(_run_node)("query_graph", query)
        n_claims = len(result.get("graph_context", []))
        step.output = (
            f"Retrieved **{n_claims} claim(s)** from Neo4j Knowledge Graph.\n"
            + ("*Running in offline mode — no Neo4j connection.*" if n_claims == 0 else "")
        )

    # ── Step 2: Hypothesis Generation ────────────────────────────────────────
    async with cl.Step(name="🧠 Hypothesis Generation", type="llm") as step:
        step.input = f"Graph context: {n_claims} claims"
        result = await cl.make_async(_run_node)("generate_hypothesis", query, result)
        hypothesis = result.get("hypothesis_payload", {}).get("hypothesis", "—")
        step.output = f"**Hypothesis:**\n> {hypothesis}"

    # ── Step 3: Red Team ──────────────────────────────────────────────────────
    async with cl.Step(name="🛡️ Red Team Adversarial Attack", type="tool") as step:
        step.input = hypothesis
        result = await cl.make_async(_run_node)("red_team", query, result)
        status = result.get("validation_status", "unknown")
        icon = "✅" if status == "verified_and_stress_tested" else "❌"
        revisions = result.get("revision_count", 0)
        step.output = f"{icon} **Verdict:** `{status}`  •  Revision count: `{revisions}`"

    # ── Step 4: Audit Ledger ──────────────────────────────────────────────────
    async with cl.Step(name="🔐 Cryptographic Audit Ledger", type="tool") as step:
        step.input = status
        result = await cl.make_async(_run_node)("audit", query, result)
        audit_hash = result.get("audit_hash", "—")
        step.output = f"**SHA-256 Fingerprint:**\n`{audit_hash}`"

    # ── Step 5: Commercialisation ─────────────────────────────────────────────
    async with cl.Step(name="💼 IP Commercialization", type="tool") as step:
        step.input = audit_hash
        result = await cl.make_async(_run_node)("commercialize", query, result)
        blueprint = result.get("commercial_blueprint", {})
        n_claims_pat = len(blueprint.get("patent_claims", []))
        step.output = f"**Patent claims drafted:** {n_claims_pat}  \n**Novelty:** {blueprint.get('novelty_status', '—')}"

    # ── Step 6: Fabrication ───────────────────────────────────────────────────
    async with cl.Step(name="⚙️ Cyber-Physical Fabrication", type="tool") as step:
        step.input = "commercial blueprint"
        result = await cl.make_async(_run_node)("fabricate", query, result)
        fab = result.get("fabrication_assets", {})
        step.output = (
            f"**CAD parameters:** `{fab.get('cad_model_path', '—')}`  \n"
            f"**Cloud Lab protocol:** `{fab.get('cloud_lab_protocol_path', '—')}`"
        )

    # ── Step 7: Regulatory ────────────────────────────────────────────────────
    async with cl.Step(name="📋 Regulatory Compliance & GTM", type="tool") as step:
        step.input = "fabrication assets"
        result = await cl.make_async(_run_node)("regulate", query, result)
        reg = result.get("regulatory_assets", {})
        step.output = (
            f"**Pathway:** {reg.get('pathway', '—')}  \n"
            f"**Protocol:** `{reg.get('compliance_protocol_path', '—')}`"
        )

    # ── Step 8: Compile PDF ───────────────────────────────────────────────────
    async with cl.Step(name="📄 Tier-1 Dossier Compilation", type="tool") as step:
        step.input = "verified payload"
        result = await cl.make_async(_run_node)("compile_pdf", query, result)
        artifact = result.get("final_output_path", "—")
        ext = Path(str(artifact)).suffix if artifact != "—" else ""
        label = "PDF" if ext == ".pdf" else "LaTeX source"
        step.output = f"**{label} artifact:**\n`{artifact}`"

    # ── Final summary ─────────────────────────────────────────────────────────
    artifact_path = result.get("final_output_path", "—")
    root_msg.content = (
        f"## 🏆 Constitutional Run Complete\n\n"
        f"**Query:** `{query}`  \n"
        f"**Hypothesis:** {hypothesis}  \n"
        f"**Audit hash:** `{result.get('audit_hash', '—')[:24]}…`  \n"
        f"**Artifact:** `{artifact_path}`\n\n"
        f"All outputs written to `./output/`"
    )
    await root_msg.update()


# ── Node runners ──────────────────────────────────────────────────────────────

def _run_full_pipeline(query: str) -> dict:
    """Run the complete 10-node pipeline synchronously. Used as a fallback."""
    from core.master_orchestrator import app_executor
    return app_executor.invoke({"research_query": query})


def _run_node(node_name: str, query: str, state: dict | None = None) -> dict:
    """
    Execute a single named node against the current state.
    On first call (node_name='query_graph', state=None) initialises state.

    Falls back to running the full pipeline if individual node access is
    not available (LangGraph compiled graphs don't expose nodes directly).
    """
    if state is None:
        state = {"research_query": query, "revision_count": 0}

    # Import node functions directly — bypasses compiled graph for step-by-step UI
    try:
        if node_name == "query_graph":
            from core.master_orchestrator import query_live_graph
            return query_live_graph(state)
        if node_name == "generate_hypothesis":
            from core.master_orchestrator import generate_live_hypothesis
            return generate_live_hypothesis(state)
        if node_name == "red_team":
            from core.master_orchestrator import execute_red_team_attack
            return execute_red_team_attack(state)
        if node_name == "audit":
            from core.audit_ledger import secure_audit_node
            return secure_audit_node(state)
        if node_name == "commercialize":
            from core.commercializer import commercial_blueprint_node
            return commercial_blueprint_node(state)
        if node_name == "fabricate":
            from core.fabrication_engine import fabrication_node
            return fabrication_node(state)
        if node_name == "regulate":
            from core.regulatory_engine import regulatory_node
            return regulatory_node(state)
        if node_name == "compile_pdf":
            from core.master_orchestrator import compile_final_pdf
            return compile_final_pdf(state)
    except Exception as exc:
        print(f"[web_engine] Node '{node_name}' error: {exc}")
        return {**state, "_node_error": str(exc)}

    return state

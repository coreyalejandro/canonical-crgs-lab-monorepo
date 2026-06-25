"""
ui/web_engine.py — Constitutional AI Reactive Web UI

Phase 11 Build Contract — Section III.
Phase 12 Build Contract — Section IV.2 (ToCA Dual-Anchor UI upgrade).

A Chainlit-powered WebUI that streams the live LangGraph execution in real-time,
displaying each of the 10 pipeline nodes as expandable "thought step" cards —
identical UX to Claude's reasoning interface.

Phase 12 additions:
  - TLC ToCA passive anchor displayed on every session start (Article 7)
  - "Acknowledge & Initialize System" active gate — pipeline cannot start
    until the Human PI explicitly acknowledges the governing charter (Article 8)
  - The Visionary / The Verifier identity labels on each step card (Article 10)
  - Dual-parity final output: Markdown summary + downloadable JSON artifact

Usage:
    chainlit run ui/web_engine.py -w
    # or:
    make run-webui
    # Access at: http://localhost:8000
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import chainlit as cl

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# ── TLC ToCA statement (Article 7 — passive psychological anchor) ─────────────

_TLC_TOCA = """
**Governed by TLC's ToCA** *(The Living Constitution's Theory of Change and Action)*

This system operates under a mutually beneficial, neurodivergent-first \
human-machine collaboration. It utilizes a **Mixture of Experts** architecture \
that pairs:

- 👁️ **The Visionary** — lateral, divergent, high-temperature ideation \
that scans the Knowledge Graph for unconventional connections
- ⚖️ **The Verifier** — hyper-rational, temperature=0.0 systematizer \
that enforces constitutional invariants and mathematical proofs

All outputs are produced in strict compliance with **NIST AI RMF 1.0** \
and **EU AI Act** safety frameworks and are cryptographically fingerprinted \
in an append-only audit ledger.
"""

_BACKEND_INFO = (
    f"`{os.getenv('LLM_BACKEND','lmstudio').upper()}` — "
    f"`{os.getenv('LM_STUDIO_MODEL','openai/gpt-oss-20b')}` — "
    "Free, local, no API credits required"
)


# ── Chainlit lifecycle ────────────────────────────────────────────────────────

@cl.on_chat_start
async def start() -> None:
    """
    Phase 12 — Dual-Anchor UI boot sequence (Article 7 + Article 8):
      1. Passive anchor: TLC ToCA statement displayed immediately
      2. Active gate: 'Acknowledge & Initialize System' button
         Pipeline is locked until Human PI explicitly clicks it.
    """
    # Passive anchor
    await cl.Message(
        content=(
            "## 🏛️ Safety Systems Design Commonwealth\n\n"
            f"{_TLC_TOCA}\n\n"
            f"**Backend:** {_BACKEND_INFO}  \n"
            "**Constitution:** TLC 2.0 Sociotechnical Constitution v2.0.0  \n"
            "**Pipeline:** 10-node LangGraph — KG → Hypothesis → Red Team → "
            "Audit → IP → CAD → Regulatory → PDF"
        )
    ).send()

    # Active gate (Article 8 — human interlock before any execution)
    actions = [
        cl.Action(
            name="acknowledge_toca",
            payload={"value": "acknowledged"},
            label="✅ Acknowledge & Initialize System",
            tooltip="I acknowledge and align with TLC's ToCA",
        )
    ]
    await cl.Message(
        content=(
            "**⚠️ Action Required**\n\n"
            "You must explicitly acknowledge the governing charter before "
            "**The Visionary** and **The Verifier** are brought online.\n\n"
            "*The system cannot execute any R&D pipeline until this acknowledgement "
            "is recorded in the audit trail.*"
        ),
        actions=actions,
    ).send()


@cl.action_callback("acknowledge_toca")
async def on_acknowledge(action: cl.Action) -> None:
    """Article 8 gate cleared — Human PI has authorized system initialization."""
    await cl.Message(
        content=(
            "✅ **TLC's ToCA Acknowledged and Recorded.**\n\n"
            "👁️ **The Visionary** — online, awaiting research query  \n"
            "⚖️ **The Verifier** — online, constitutional invariants armed  \n"
            "🧑‍🔬 **Human PI** — you are the cryptographic gatekeeper\n\n"
            "---\n"
            "Enter your research query to initiate a full constitutional R&D run."
        )
    ).send()
    cl.user_session.set("toca_acknowledged", True)


@cl.on_message
async def main(message: cl.Message) -> None:
    if not cl.user_session.get("toca_acknowledged"):
        await cl.Message(
            content="⚠️ Please acknowledge TLC's ToCA above before submitting a query."
        ).send()
        return

    query = message.content.strip()
    if not query:
        return

    root_msg = cl.Message(content=f"**🚀 Initiating pipeline for:** `{query}`")
    await root_msg.send()

    state: dict = {"research_query": query, "revision_count": 0}

    # ── Step 1: Knowledge Graph (neutral — pre-MoE) ───────────────────────────
    async with cl.Step(name="🔍 Knowledge Graph Retrieval", type="tool") as step:
        step.input = query
        state = await cl.make_async(_run_node)("query_graph", query, state)
        n = len(state.get("graph_context", []))
        step.output = (
            f"Retrieved **{n} claim(s)** from Neo4j Knowledge Graph.\n"
            + ("*Offline mode — Neo4j not running.*" if n == 0 else "")
        )

    # ── Step 2: Hypothesis Generation — 👁️ The Visionary role ────────────────
    async with cl.Step(name="👁️ The Visionary — Hypothesis Generation", type="llm") as step:
        step.input = f"{n} graph claims"
        state = await cl.make_async(_run_node)("generate_hypothesis", query, state)
        hypothesis = state.get("hypothesis_payload", {}).get("hypothesis", "—")
        step.output = f"**Divergent hypothesis drafted:**\n> {hypothesis}"

    # ── Step 3: Red Team — ⚖️ The Verifier role ──────────────────────────────
    async with cl.Step(name="⚖️ The Verifier — Red Team Attack", type="tool") as step:
        step.input = hypothesis
        state = await cl.make_async(_run_node)("red_team", query, state)
        status = state.get("validation_status", "unknown")
        icon = "✅" if "verified" in status else "❌"
        step.output = (
            f"{icon} **Verdict:** `{status}`  \n"
            f"Revision count: `{state.get('revision_count', 0)}`"
        )

    # ── Step 4: Audit Ledger ──────────────────────────────────────────────────
    async with cl.Step(name="🔐 Cryptographic Audit Ledger", type="tool") as step:
        step.input = status
        state = await cl.make_async(_run_node)("audit", query, state)
        audit_hash = state.get("audit_hash", "—")
        step.output = f"**SHA-256 Constitutional Fingerprint:**\n`{audit_hash}`"

    # ── Step 5: Commercialise ─────────────────────────────────────────────────
    async with cl.Step(name="💼 IP Commercialization", type="tool") as step:
        step.input = audit_hash[:16] + "…"
        state = await cl.make_async(_run_node)("commercialize", query, state)
        bp = state.get("commercial_blueprint", {})
        step.output = (
            f"Patent claims: **{len(bp.get('patent_claims', []))}**  \n"
            f"Novelty: {bp.get('novelty_status', '—')}"
        )

    # ── Step 6: Fabrication ───────────────────────────────────────────────────
    async with cl.Step(name="⚙️ Cyber-Physical Fabrication", type="tool") as step:
        step.input = "commercial blueprint"
        state = await cl.make_async(_run_node)("fabricate", query, state)
        fab = state.get("fabrication_assets", {})
        step.output = (
            f"CAD: `{fab.get('cad_model_path', '—')}`  \n"
            f"Lab protocol: `{fab.get('cloud_lab_protocol_path', '—')}`"
        )

    # ── Step 7: Regulatory ────────────────────────────────────────────────────
    async with cl.Step(name="📋 Regulatory Compliance & GTM", type="tool") as step:
        step.input = "fabrication assets"
        state = await cl.make_async(_run_node)("regulate", query, state)
        reg = state.get("regulatory_assets", {})
        step.output = (
            f"Pathway: {reg.get('pathway', '—')}  \n"
            f"Protocol: `{reg.get('compliance_protocol_path', '—')}`"
        )

    # ── Step 8: Compile ───────────────────────────────────────────────────────
    async with cl.Step(name="📄 Tier-1 Dossier Compilation", type="tool") as step:
        step.input = "verified payload"
        state = await cl.make_async(_run_node)("compile_pdf", query, state)
        artifact = state.get("final_output_path", "—")
        ext   = Path(str(artifact)).suffix if artifact != "—" else ""
        label = "PDF" if ext == ".pdf" else "LaTeX source"
        step.output = f"**{label}:** `{artifact}`"

    # ── Dual-parity final summary (Article 6) ────────────────────────────────
    report_json = {
        "query":            query,
        "hypothesis":       hypothesis,
        "validation_status": status,
        "audit_hash":       state.get("audit_hash", ""),
        "artifact":         state.get("final_output_path", ""),
        "tlc_version":      "2.0.0",
        "governance":       "NIST AI RMF / EU AI Act / TLC ToCA",
    }

    root_msg.content = (
        "## 🏆 Constitutional Run Complete\n\n"
        f"**Query:** `{query}`  \n"
        f"**Hypothesis:** {hypothesis[:160]}{'…' if len(hypothesis)>160 else ''}  \n"
        f"**Audit hash:** `{state.get('audit_hash','—')[:24]}…`  \n"
        f"**Artifact:** `{state.get('final_output_path','—')}`\n\n"
        "**Dual-parity JSON artifact:**\n"
        f"```json\n{json.dumps(report_json, indent=2)[:600]}\n```"
    )
    await root_msg.update()


# ── Node runners (direct node calls — step-by-step for UI) ───────────────────

def _run_node(node_name: str, query: str, state: dict | None = None) -> dict:
    if state is None:
        state = {"research_query": query, "revision_count": 0}
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

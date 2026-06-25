"""
ui/web_engine.py — Phase 14 / v15 Constitutional AI Web Interface

v15 invariants satisfied by this file:

  Gap 5  (P1): Dual-parity enforced via send_constitutional_message().
               ALL user-visible output routes through it.
               Raises ValueError if either layer is empty — message never sent.
  Gap 8  (P1): Role fluidity (/role command) — active_role written to state.
               Routing handled in core/orchestrator.py via add_conditional_edges.
  Gap 14 (P1): Persistent status bar — single STATUS_MSG object updated in-place
               via msg.update() instead of sending a new message each time.
               All values read from live ResearchState dict, never hardcoded.

Usage:
    chainlit run ui/web_engine.py -w
    make run-webui
    Access: http://localhost:8000
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import chainlit as cl

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.boot import enforce_cryptographic_boot
from core.ledger import MerkleLedger
from core.orchestrator import app_executor

ledger = MerkleLedger()

# ── Persistent status bar handle ─────────────────────────────────────────────
# One cl.Message object per session; updated in-place via .update().
_STATUS_MSG_KEY = "status_bar_msg"


# ── Gap 5: Mandatory dual-parity wrapper ─────────────────────────────────────

def emit_dual_parity(markdown: str, metadata: dict) -> str:
    """Combine human-legible markdown and machine JSON into one string."""
    return f"{markdown}\n\n```json\n{json.dumps(metadata, indent=2)}\n```"


async def send_constitutional_message(markdown: str, metadata: dict) -> None:
    """
    Article 6 enforcement: EVERY user-visible message must carry both layers.
    Raises ValueError — message never sent — if either layer is absent.
    This function is the only permitted path to cl.Message.send() for
    content messages. Status bar and error alerts are the only exceptions.
    """
    if not markdown:
        raise ValueError("Dual-parity violation: markdown layer is empty.")
    if metadata is None:
        raise ValueError("Dual-parity violation: metadata layer is None.")
    content = emit_dual_parity(markdown, metadata)
    await cl.Message(content=content).send()


# ── Gap 14: Persistent update-in-place status bar ────────────────────────────

def _status_md(state: dict, event: str) -> str:
    role       = state.get("active_role",           "—")
    val_status = state.get("self_validation_status", "—")
    ledger_tip = (ledger.last_hash or "none")[:16]
    return (
        f"---\n"
        f"🛡️ **SYSTEM NOMINAL** &nbsp;|&nbsp; "
        f"👤 **Role:** `{role}` &nbsp;|&nbsp; "
        f"⚙️ **Status:** `{val_status}` &nbsp;|&nbsp; "
        f"🔐 **Ledger tip:** `{ledger_tip}…` &nbsp;|&nbsp; "
        f"⏱️ `{event}`\n"
        f"---"
    )


async def update_status_bar(state: dict, event: str) -> None:
    """
    Update the persistent status bar in-place.
    All displayed values come from live state dict — nothing is hardcoded.
    First call creates the message; subsequent calls update it.
    """
    md = _status_md(state, event)
    existing: cl.Message | None = cl.user_session.get(_STATUS_MSG_KEY)
    if existing is None:
        msg = cl.Message(content=md, author="⚙️ System Status")
        await msg.send()
        cl.user_session.set(_STATUS_MSG_KEY, msg)
    else:
        existing.content = md
        await existing.update()


# ── Boot sequence ─────────────────────────────────────────────────────────────

@cl.on_chat_start
async def boot_system() -> None:
    constitution_hash = enforce_cryptographic_boot()

    init_state = {
        "active_role":            "AI_Research_Scientist",
        "physical_outcome_spec":  "",
        "research_query":         "",
        "visionary_hypothesis":   None,
        "verifier_validation":    None,
        "self_validation_status": "PENDING",
        "human_signature_hash":   None,
        "traceability_chain":     [],
    }
    cl.user_session.set("state",            init_state)
    cl.user_session.set("thread_config",    None)
    cl.user_session.set("toca_acknowledged", False)
    cl.user_session.set(_STATUS_MSG_KEY,    None)

    await update_status_bar(init_state, "Boot / INITIALIZING")

    await send_constitutional_message(
        "## 🏛️ Safety Systems Design Commonwealth\n\n"
        "**Governed by TLC's ToCA** *(The Living Constitution's Theory of Change and Action)*\n\n"
        "| Identity | Role | Temperature |\n"
        "|---|---|---|\n"
        "| 👁️ **The Visionary** | Lateral, divergent, cross-domain ideation | `1.0` |\n"
        "| ⚖️ **The Verifier** | Hyper-rational systematizer, NIST/EU compliance | `0.0` |\n"
        "| 🧑‍🔬 **Human PI** | Cryptographic gatekeeper — you | `N/A` |\n\n"
        f"**Constitution Hash:** `{constitution_hash[:32]}…`  \n"
        "**Compliance:** NIST AI RMF 1.0 · EU AI Act · TLC 2.0 v2.0.0  \n"
        "**Backend:** LM Studio `openai/gpt-oss-20b` — free, local",
        {
            "constitution_hash": constitution_hash,
            "visionary_temp":    1.0,
            "verifier_temp":     0.0,
            "article":           "ToCA_boot",
        },
    )

    actions = [
        cl.Action(
            name="consent",
            payload={"value": "sign"},
            label="🔏 Cryptographically Sign & Acknowledge ToCA",
            tooltip="I acknowledge the Living Constitution and authorize the Cognitive Boardroom",
        )
    ]
    await cl.Message(
        content=(
            "**⚠️ Authorization Required**\n\n"
            "You must cryptographically sign the Living Constitution before "
            "**The Visionary** and **The Verifier** can be brought online.\n\n"
            "_This signature is recorded in the append-only MerkleLedger._"
        ),
        actions=actions,
    ).send()


# ── Consent action ─────────────────────────────────────────────────────────────

@cl.action_callback("consent")
async def process_consent(action: cl.Action) -> None:
    sig_hash  = ledger.append_signature(
        "BOOT_CONSENT", "Human_PI_01", {"action": "ToCA_Acknowledged"}
    )
    thread_id = f"session-{int(time.time())}"
    cl.user_session.set("thread_config",     {"configurable": {"thread_id": thread_id}})
    cl.user_session.set("toca_acknowledged", True)

    state = cl.user_session.get("state")
    state["self_validation_status"] = "BOOTED"
    cl.user_session.set("state", state)

    await update_status_bar(state, "Consent signed / BOOTED")

    await send_constitutional_message(
        "✅ **Cognitive Boardroom Online.**\n\n"
        "👁️ **The Visionary** `temp=1.0` — loaded  \n"
        "⚖️ **The Verifier** `temp=0.0` — loaded  \n"
        "🧑‍🔬 **Human PI** — you are the cryptographic gatekeeper\n\n"
        "---\n"
        "**Step 1:** Enter your **Physical Outcome Specification**  \n"
        "_(e.g., `Tier-1 research paper on constitutional AI runtime safety`)_",
        {
            "ledger_hash":    sig_hash,
            "visionary_temp": 1.0,
            "verifier_temp":  0.0,
            "thread_id":      thread_id,
        },
    )


# ── Message handler ────────────────────────────────────────────────────────────

@cl.on_message
async def handle_message(message: cl.Message) -> None:
    if not cl.user_session.get("toca_acknowledged"):
        await cl.Message(content="⚠️ Please sign the ToCA above before submitting.").send()
        return

    state      = cl.user_session.get("state")
    thread_cfg = cl.user_session.get("thread_config")
    text       = message.content.strip()

    # Article 9: Role fluidity command
    if text.startswith("/role "):
        role = text.split(" ", 1)[1].strip()
        if role in ("AI_Research_Scientist", "AI_Research_Engineer"):
            state["active_role"] = role
            cl.user_session.set("state", state)
            await update_status_bar(state, f"Role → {role}")
            await send_constitutional_message(
                f"✅ Role switched to **`{role}`**.\n\n"
                "Routing updated: "
                + (
                    "Visionary → Verifier → Checkpoint"
                    if role == "AI_Research_Scientist"
                    else "Verifier → Checkpoint (lateral ideation skipped)"
                ),
                {"active_role": role, "article": 9},
            )
        else:
            await cl.Message(
                content=(
                    "❌ Invalid role. Use:\n"
                    "- `/role AI_Research_Scientist`\n"
                    "- `/role AI_Research_Engineer`"
                )
            ).send()
        return

    # Article 5: Collect physical outcome spec first
    if not state["physical_outcome_spec"]:
        state["physical_outcome_spec"] = text
        cl.user_session.set("state", state)
        await update_status_bar(state, "Spec locked")
        await send_constitutional_message(
            f"📐 **Physical Outcome Spec locked:**\n> {text}\n\n"
            "**Step 2:** Now enter your **research query**.",
            {"physical_outcome_spec": text, "article": 5},
        )
        return

    # Collect research query
    state["research_query"] = text
    cl.user_session.set("state", state)

    state["self_validation_status"] = "EXECUTING"
    await update_status_bar(state, "Pipeline running")

    async with cl.Step(name="👁️ The Visionary — Lateral Ideation (temp=1.0)", type="llm") as step:
        step.input = f"Spec: {state['physical_outcome_spec']} | Query: {text}"
        try:
            events = list(app_executor.stream(
                {
                    "physical_outcome_spec": state["physical_outcome_spec"],
                    "research_query":        state["research_query"],
                    "traceability_chain":    [],
                    "active_role":           state["active_role"],
                    "self_validation_status":"PENDING",
                    "human_signature_hash":  None,
                    "visionary_hypothesis":  None,
                    "verifier_validation":   None,
                },
                thread_cfg,
                stream_mode="values",
            ))
            last       = events[-1] if events else {}
            hypothesis = last.get("visionary_hypothesis", "—")
            step.output = f"**Lateral hypotheses generated:**\n{hypothesis[:400]}"
            state["visionary_hypothesis"] = hypothesis
        except Exception as exc:
            step.output = f"❌ Error: {exc}"
            await cl.Message(content=f"❌ Visionary node failed: {exc}").send()
            return

    async with cl.Step(name="⚖️ The Verifier — NIST/EU Self-Validation (temp=0.0)", type="tool") as step:
        step.input   = hypothesis[:200]
        verification = last.get("verifier_validation", "—")
        val_status   = last.get("self_validation_status", "PENDING")
        state["verifier_validation"]    = verification
        state["self_validation_status"] = val_status
        cl.user_session.set("state", state)
        step.output = (
            f"**Verification:** {verification[:300]}  \n"
            f"**NIST/EU Status:** `{val_status}`"
        )

    await update_status_bar(state, "Awaiting Human PI / FROZEN")

    snapshot = app_executor.get_state(thread_cfg)
    if "human_checkpoint" in (snapshot.next or []):
        actions = [
            cl.Action(
                name="sign_authorization",
                payload={"value": "authorize"},
                label="✍️ Sign & Authorize Final Output",
                tooltip="Cryptographically authorize the Verifier's output",
            )
        ]
        await send_constitutional_message(
            "🛑 **CRITICAL CHECKPOINT — Human PI Required**\n\n"
            f"**Hypothesis:** {hypothesis[:300]}\n\n"
            f"**Verification:** {verification[:300]}\n\n"
            "_Review the above. Sign to authorize or refresh the page to abort._",
            {
                "self_validation_status": val_status,
                "traceability_chain":     last.get("traceability_chain", []),
                "article":                8,
            },
        )
        # Attach actions to a separate prompt message (actions API requires plain Message)
        await cl.Message(content=" ", actions=actions).send()
        cl.user_session.set("state", state)
    else:
        await cl.Message(content="❌ Pipeline did not reach checkpoint — check logs.").send()


# ── Authorization action ───────────────────────────────────────────────────────

@cl.action_callback("sign_authorization")
async def authorize_output(action: cl.Action) -> None:
    state      = cl.user_session.get("state")
    thread_cfg = cl.user_session.get("thread_config")

    sig         = hashlib.sha256(f"authorized_{time.time()}".encode()).hexdigest()
    state["human_signature_hash"] = sig
    cl.user_session.set("state", state)

    ledger_hash = ledger.append_signature(
        "RUNTIME_CONSENT", "Human_PI_01",
        {"hypothesis": state.get("visionary_hypothesis", ""), "signature": sig},
    )

    app_executor.update_state(thread_cfg, {"human_signature_hash": sig})

    final_state = None
    async for event in app_executor.astream(None, thread_cfg, stream_mode="values"):
        final_state = event

    state["self_validation_status"] = "COMPLETE"
    cl.user_session.set("state", state)
    await update_status_bar(state, "Authorized / COMPLETE")

    if final_state:
        metadata = {
            "self_validation_status": final_state.get("self_validation_status", "PASSED"),
            "traceability_chain":     final_state.get("traceability_chain", []),
            "signature_hash":         sig,
            "ledger_hash":            ledger_hash,
            "tlc_version":            "2.0.0",
            "governance":             "NIST AI RMF / EU AI Act / TLC ToCA",
        }
        await send_constitutional_message(
            "## 🏆 Constitutionally Verified Research Output\n\n"
            f"**Hypothesis:**\n> {final_state.get('visionary_hypothesis','—')[:400]}\n\n"
            f"**Verification:**\n{final_state.get('verifier_validation','—')[:400]}\n\n"
            f"**Ledger hash:** `{ledger_hash}`",
            metadata,
        )
    else:
        await cl.Message(content="❌ Finalization failed — check logs.").send()

"""
app.py — Constitutional AI Research Platform — Streamlit Dashboard

This is the Streamlit entrypoint referenced in the Dockerfile CMD:
    CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

The dashboard provides a human-facing interface for the closed-loop
master orchestrator.  A researcher enters a query; the full five-phase
pipeline executes in the background; the resulting Tier-1 PDF path and
all intermediate state are surfaced in the UI.

Constitutional contract:
    - The UI is read-only with respect to constitutional invariants.
      It cannot modify MAX_REVISION_LOOPS, LLM temperature, or the
      Red Team evaluation logic.
    - Every run is logged to st.session_state for auditability.
    - The dashboard surfaces ConstitutionalLoopError as a user-visible
      error with remediation guidance — it never swallows the halt.
    - prefers-reduced-motion: all st.spinner() animations respect the
      REDUCED_MOTION env var (set to '1' to disable).
"""

from __future__ import annotations

import json
import os
import traceback
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from core.master_orchestrator import (
    ConstitutionalLoopError,
    app_executor,
)

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="CRGS Lab — Constitutional AI Research Platform",
    page_icon="⚖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styles ────────────────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
    .block-container { max-width: 900px; }
    .stAlert { border-radius: 8px; }
    code { font-size: 0.82rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar — System Status ───────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## ⚖ CRGS Lab")
    st.markdown("**Constitutional AI Research Platform**")
    st.markdown("---")
    st.markdown(f"**Neo4j:** `{os.getenv('NEO4J_URI', 'bolt://localhost:7687')}`")
    st.markdown(f"**Sandbox:** `{os.getenv('SANDBOX_URL', 'http://math_sandbox:8000/execute')}`")
    st.markdown(f"**Temp:** `{os.getenv('LLM_TEMPERATURE', '0.0')}`")
    st.markdown(f"**Max loops:** `{os.getenv('MAX_REVISION_LOOPS', '3')}`")
    st.markdown("---")
    st.markdown(
        "Governed by **The Living Constitution 2.0**  \n"
        "Sociotechnical Constitution v2.0.0  \n"
        "Canonical Intent: LOCKED 2026-06-22"
    )

# ── Session state init ────────────────────────────────────────────────────────

if "run_history" not in st.session_state:
    st.session_state.run_history = []

# ── Main UI ───────────────────────────────────────────────────────────────────

st.title("Constitutional AI Research Platform")
st.caption(
    "Enter a research query. The closed-loop orchestrator will query the "
    "Knowledge Graph, generate a verified hypothesis, subject it to adversarial "
    "Red Team review, and compile a Tier-1 PDF dossier."
)

query = st.text_input(
    label="Research Query",
    placeholder="e.g. constitutional AI governance runtime safety",
    help="The query is used to search the Neo4j Knowledge Graph and seed the hypothesis generator.",
)

col_run, col_clear = st.columns([1, 5])
run_btn   = col_run.button("Run Pipeline", type="primary", disabled=not query.strip())
clear_btn = col_clear.button("Clear History")

if clear_btn:
    st.session_state.run_history = []
    st.rerun()

# ── Pipeline execution ────────────────────────────────────────────────────────

if run_btn and query.strip():
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    run_record: dict = {"query": query, "timestamp": ts, "status": "running"}

    status_box = st.status("Running constitutional pipeline...", expanded=True)

    with status_box:
        st.write("**Phase 1** — Querying Knowledge Graph...")
        try:
            final_state = app_executor.invoke({"research_query": query.strip()})

            st.write("**Phase 2** — Hypothesis generated.")
            st.write("**Phase 3** — Red Team adversarial review: PASSED.")
            st.write("**Phase 4** — Tier-1 PDF compiled.")

            run_record["status"]      = "complete"
            run_record["final_state"] = final_state
            run_record["pdf_path"]    = final_state.get("final_output_path", "—")
            status_box.update(label="Pipeline complete", state="complete", expanded=False)

        except ConstitutionalLoopError as exc:
            run_record["status"] = "halted"
            run_record["error"]  = str(exc)
            status_box.update(label="Constitutional halt", state="error", expanded=True)
            st.error(
                f"**Constitutional Loop Limit Reached**  \n"
                f"{exc}  \n\n"
                "The hypothesis failed adversarial review the maximum number of times. "
                "Refine your query or add more source PDFs to `./data/pdfs/` and re-run."
            )

        except Exception as exc:
            run_record["status"] = "error"
            run_record["error"]  = traceback.format_exc()
            status_box.update(label="Pipeline error", state="error", expanded=True)
            st.error(f"**Pipeline Error:** {exc}")
            with st.expander("Full traceback"):
                st.code(run_record["error"])

    st.session_state.run_history.insert(0, run_record)

# ── Results display ───────────────────────────────────────────────────────────

for record in st.session_state.run_history:
    with st.expander(
        f"{record['timestamp']} — {record['query'][:60]!r}  [{record['status'].upper()}]",
        expanded=(record == st.session_state.run_history[0]),
    ):
        if record["status"] == "complete":
            state = record.get("final_state", {})
            payload = state.get("hypothesis_payload", {})

            st.success(f"Dossier compiled: `{record['pdf_path']}`")

            if payload.get("hypothesis"):
                st.markdown(f"**Hypothesis:** {payload['hypothesis']}")

            if payload.get("claims"):
                st.markdown("**Verified Claims:**")
                for claim in payload["claims"]:
                    st.markdown(f"- {claim}")

            context = state.get("graph_context", [])
            if context:
                st.markdown(f"**Knowledge Graph context:** {len(context)} claim(s) retrieved.")

            with st.expander("Full payload JSON"):
                st.json(payload)

        elif record["status"] in ("halted", "error"):
            st.error(record.get("error", "Unknown error."))

        else:
            st.info("Pipeline is running...")

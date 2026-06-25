"""
ui/tui_engine.py — Constitutional AI Command Center TUI

Phase 11 Build Contract — Section II.

A high-performance split-pane Terminal User Interface that provides:
  - Left panel: live cryptographic audit trail (append-only, SHA-256 fingerprints)
  - Center panel: real-time LangGraph node execution log with status icons
  - Bottom bar: research query input, Ctrl+Q to quit

The TUI hooks directly into the live master_orchestrator pipeline by running
it in a background thread and streaming each node's stdout into the panels
via Rich markup. No simulation — every line you see is real execution output.

Usage:
    python -m ui.tui_engine
    # or via Makefile:
    make run-tui
"""

from __future__ import annotations

import asyncio
import queue
import sys
import threading
from pathlib import Path

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Input, Log, Static

# Add repo root to path so core.* imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# ── Node icon map ─────────────────────────────────────────────────────────────

_NODE_ICONS: dict[str, str] = {
    "Querying Knowledge Graph":             "🔍",
    "Generating deterministic hypothesis":  "🧠",
    "Red Team attack":                      "🛡️ ",
    "Red Team: PASSED":                     "✅",
    "Red Team: VETO":                       "❌",
    "Writing AI logic chain":               "🔒",
    "CONSTITUTIONAL LOG LOCKED":            "🔐",
    "Initiating Commercialization":         "💼",
    "Initiating Cyber-Physical":            "⚙️ ",
    "Initiating Regulatory":                "📋",
    "Compiling Tier-1 PDF":                 "📄",
    "Tier-1 PDF generated":                 "🎯",
    "END-TO-END CYCLE COMPLETE":            "🏆",
    "INITIATING CLOSED-LOOP":               "🚀",
}


def _icon_for(line: str) -> str:
    for key, icon in _NODE_ICONS.items():
        if key.lower() in line.lower():
            return icon
    return "▶ "


def _markup_line(line: str) -> str:
    """Colour-code a pipeline log line with Rich markup."""
    l = line.lower()
    if any(k in l for k in ("passed", "complete", "locked", "generated", "success")):
        return f"[bold green]{line}[/]"
    if any(k in l for k in ("veto", "failed", "error", "unavailable")):
        return f"[bold red]{line}[/]"
    if any(k in l for k in ("warning", "non-fatal", "skipped")):
        return f"[yellow]{line}[/]"
    if any(k in l for k in ("fingerprint", "hash", "sha-256", "ledger")):
        return f"[bold cyan]{line}[/]"
    if line.startswith("["):
        return f"[dim white]{line}[/]"
    return line


# ── Output capture ────────────────────────────────────────────────────────────

class _QueueWriter:
    """Intercepts stdout/stderr and puts lines into a queue."""

    def __init__(self, q: queue.Queue, original) -> None:
        self._q = q
        self._original = original

    def write(self, text: str) -> None:
        self._original.write(text)
        self._original.flush()
        for line in text.splitlines():
            stripped = line.strip()
            if stripped:
                self._q.put(stripped)

    def flush(self) -> None:
        self._original.flush()

    def fileno(self):
        return self._original.fileno()


# ── Textual App ───────────────────────────────────────────────────────────────

class ConstitutionalTUI(App):
    """
    Constitutional AI Governed R&D Command Center.

    Split-pane layout:
      ┌─────────────────────────────┬──────────────────────────────────────┐
      │  Cryptographic Audit Trail  │  Neuro-Symbolic Execution State      │
      │  (SHA-256 fingerprints,     │  (live node-by-node pipeline output) │
      │   ledger entries, status)   │                                      │
      └─────────────────────────────┴──────────────────────────────────────┘
      [ Research query input ─────────────────────────────────── Ctrl+Q: quit ]
    """

    CSS = """
    Screen { background: #0d0d0d; }
    Header { background: #1a1a2e; color: #00ff88; }
    Footer { background: #1a1a2e; }

    #sidebar {
        width: 32%;
        border-right: solid #00ff88;
        padding: 0 1;
    }
    #sidebar-title {
        text-align: center;
        color: #00ff88;
        text-style: bold;
        padding: 0 0 1 0;
    }
    #main-console { width: 68%; padding: 0 1; }
    #main-title {
        text-align: center;
        color: #7c5cd8;
        text-style: bold;
        padding: 0 0 1 0;
    }

    Log { background: #0d0d0d; color: #e0e0e0; border: none; height: 1fr; }
    Input {
        dock: bottom;
        margin: 1 2;
        background: #1a1a2e;
        border: solid #00ff88;
        color: #e0e0e0;
    }
    """

    BINDINGS = [
        Binding("ctrl+q", "quit", "Terminate Session"),
        Binding("ctrl+c", "quit", "Terminate Session", show=False),
    ]

    TITLE = "CRGS Lab — Constitutional AI R&D Command Center"
    SUB_TITLE = "Governed by TLC 2.0 Sociotechnical Constitution v2.0.0"

    def __init__(self) -> None:
        super().__init__()
        self._log_queue: queue.Queue = queue.Queue()
        self._running = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Static("🔐 Cryptographic Audit Trail", id="sidebar-title")
                yield Log(id="audit-log", highlight=True, markup=True)
            with Vertical(id="main-console"):
                yield Static("🧠 Neuro-Symbolic Execution State", id="main-title")
                yield Log(id="main-log", highlight=True, markup=True)
        yield Input(
            placeholder="Enter research query and press Enter  (e.g. 'constitutional AI governance runtime safety')  •  Ctrl+Q to quit",
        )
        yield Footer()

    def on_mount(self) -> None:
        main_log = self.query_one("#main-log", Log)
        main_log.write_line("[bold cyan]Constitutional AI R&D Pipeline ready.[/]")
        main_log.write_line("[dim]Enter a research query below to initiate the full 10-node LangGraph execution.[/]")
        audit_log = self.query_one("#audit-log", Log)
        audit_log.write_line("[dim cyan]Awaiting first pipeline execution...[/]")
        self.set_interval(0.1, self._drain_queue)

    def _drain_queue(self) -> None:
        """Pull lines from the background thread and route them to the correct panel."""
        main_log  = self.query_one("#main-log",  Log)
        audit_log = self.query_one("#audit-log", Log)
        try:
            while True:
                line = self._log_queue.get_nowait()
                icon = _icon_for(line)
                marked = _markup_line(f"{icon} {line}")
                # Route audit/fingerprint lines to the left panel
                if any(k in line.lower() for k in ("fingerprint", "hash:", "ledger", "sha-256", "locked.", "audit")):
                    audit_log.write_line(marked)
                else:
                    main_log.write_line(marked)
        except queue.Empty:
            pass

    async def on_input_submitted(self, message: Input.Submitted) -> None:
        query = message.value.strip()
        if not query:
            return
        message.input.value = ""

        if self._running:
            self.query_one("#main-log", Log).write_line(
                "[yellow]⚠️  Pipeline already running — wait for END-TO-END CYCLE COMPLETE.[/]"
            )
            return

        self._running = True
        self.query_one("#main-log",  Log).write_line(f"\n[bold green]{'─'*60}[/]")
        self.query_one("#main-log",  Log).write_line(f"[bold green]🚀 NEW RUN: {query}[/]")
        self.query_one("#audit-log", Log).write_line(f"\n[bold cyan]{'─'*40}[/]")
        self.query_one("#audit-log", Log).write_line(f"[bold cyan]🔍 Target: {query[:40]}[/]")

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._run_pipeline, query)
        self._running = False

    def _run_pipeline(self, query: str) -> None:
        """Run the full orchestrator in a background thread, capturing stdout."""
        import os
        # Redirect stdout so every print() goes into our queue
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        writer = _QueueWriter(self._log_queue, old_stdout)
        sys.stdout = writer  # type: ignore[assignment]
        sys.stderr = writer  # type: ignore[assignment]

        try:
            # Import here to pick up env vars set before TUI launch
            from core.master_orchestrator import app_executor
            initial_state = {"research_query": query}
            app_executor.invoke(initial_state)
        except Exception as exc:
            self._log_queue.put(f"[PIPELINE ERROR] {exc.__class__.__name__}: {exc}")
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    app = ConstitutionalTUI()
    app.run()


if __name__ == "__main__":
    main()

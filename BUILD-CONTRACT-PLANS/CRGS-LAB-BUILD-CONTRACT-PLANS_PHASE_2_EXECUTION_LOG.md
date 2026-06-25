# CRGS Lab — Phase 2 Execution Log

**Build Contract:** `CRGS-LAB-BUILD-CONTRACT-PLANS_PHASE_2.md`  
**Executed:** 2026-06-22  
**Status:** COMPLETE  
**Governed by:** The Living Constitution 2.0 — Sociotechnical Constitution v2.0.0

---

## What Was Built

### Section I — Expanded Dependency Lock

| Artifact | Path | Status |
|---|---|---|
| Phase 2 dependency lock | `requirements-phase2.txt` | ✅ Created |

New packages pinned: `langchain-openai==0.0.8`, `langchain-community==0.0.28`, `tiktoken==0.6.0`, `PyMuPDF==1.23.21`, `fastapi==0.110.0`, `uvicorn==0.28.0`.

---

### Section II — Segregated Infrastructure Schema

| Artifact | Path | Status |
|---|---|---|
| Updated docker-compose | `docker-compose.yml` | ✅ Updated |

**Changes from Phase 1:**
- Added `math_sandbox` service — builds from `sandbox/Dockerfile.sandbox`, runs on port `8000`, restricted to `internal_mesh` network
- Added `internal_mesh` bridge network — `constitutional_engine` and `math_sandbox` share the internal network; sandbox has no external egress
- `constitutional_engine` gains `SANDBOX_URL` and `LLM_TEMPERATURE=0.0` environment variables
- `constitutional_engine` depends on both `knowledge_graph` and `math_sandbox`

---

### Section III — Secure Sandbox Definition

| Artifact | Path | Status |
|---|---|---|
| Sandbox Dockerfile | `sandbox/Dockerfile.sandbox` | ✅ Created |
| Sandbox FastAPI server | `sandbox/sandbox_api.py` | ✅ Created |

**`sandbox/sandbox_api.py` implements:**
- `GET /health` — liveness probe for `make verify-sandbox`
- `POST /execute` — accepts `{"code": "...", "timeout_seconds": N}`, runs code in isolated subprocess with empty `env={}`, hard timeout, returns `{stdout, stderr, exit_code, verified}`
- Runs as unprivileged `sandboxuser` inside the container
- All secrets stripped from subprocess environment

---

### Section IV — Deterministic LLM Binding

| Artifact | Path | Status |
|---|---|---|
| `core/__init__.py` | `core/__init__.py` | ✅ Created |
| LLM binding | `core/llm_binding.py` | ✅ Created |
| PDF ETL pipeline | `core/ingest_pdfs.py` | ✅ Created |

**`core/llm_binding.py`:**
- `HypothesisPayload` Pydantic schema: `hypothesis`, `claims`, `citations`, `validation_code`
- `get_deterministic_generator()`: `ChatOpenAI(model="gpt-4o", temperature=0.0, seed=42).with_structured_output(HypothesisPayload)`
- Any response deviating from schema raises `OutputParserException` → LangGraph revision loop

**`core/ingest_pdfs.py`:**
- Reads all `*.pdf` from `./data/pdfs/` (configurable via `PDF_DIR` env var)
- Extracts text via PyMuPDF (deterministic, no API call)
- Embeds via local `all-MiniLM-L6-v2` (no API key required)
- Upserts `Paper` nodes into Neo4j with `content_hash` (sha256), `ingested_at`, `source_path`
- Gracefully handles missing PDF directory (creates it, logs warning, returns 0)

---

### Section V — Phase 2 Makefile Targets

| Artifact | Path | Status |
|---|---|---|
| Makefile | `Makefile` | ✅ Updated |

**New targets:**
- `make verify-sandbox` — builds containers, boots graph + sandbox, POSTs a SymPy expression to `/execute`, asserts `2*x` in response
- `make verify-etl` — depends on `verify-sandbox`, runs `core/ingest_pdfs.py` inside the engine container
- `make run-phase2` — depends on `verify-etl`, boots `constitutional_engine`
- `make execute-phase-2` — full pipeline: `clean → build → run-phase2`

Both Phase 1 and Phase 2 targets coexist. `make execute-phase-1` still works.

---

### Supporting Artifacts

| Artifact | Path | Status |
|---|---|---|
| PDF source directory | `data/pdfs/README.md` | ✅ Created |

---

## Pre-Flight Requirements Before Running `make execute-phase-2`

1. **Docker Desktop** must be running
2. **OpenAI API key** — set `OPENAI_API_KEY` in environment before running (`export OPENAI_API_KEY=sk-...`). The LangGraph engine reads this at runtime.
3. **PDFs** — place research PDFs in `./data/pdfs/` for ETL. The pipeline runs cleanly with zero PDFs (no-op, no failure).
4. **Port availability** — `7474`, `7687`, `8000`, `8501` must be free

---

## What Is NOT Yet Built (Phase 3+)

| Item | Notes |
|---|---|
| `app.py` | Streamlit dashboard entrypoint — referenced by `Dockerfile` CMD |
| `langgraph_engine.py` | LangGraph constitutional loop — referenced by Phase 1 verify target |
| `core/judge_agent.py` | Judge Agent that calls sandbox `/execute` and routes revision loop |
| `core/graph_builder.py` | LangGraph state machine wiring Generator ↔ Judge ↔ Constitutional Router |
| Blockchain governance ledger | Tier 6 — Phase 4+ |

---

*This log is immutable. Phase 3 work will be tracked in `CRGS-LAB-BUILD-CONTRACT-PLANS_PHASE_3.md`.*

# CRGS Lab — Phase 3 Execution Log

**Build Contract:** `CRGS-LAB-BUILD-CONTRACT-PLANS_PHASE_3.md`  
**Executed:** 2026-06-22  
**Status:** COMPLETE  
**Governed by:** The Living Constitution 2.0 — Sociotechnical Constitution v2.0.0

---

## What Was Built

### Section I — Final Dependency Lock

| Artifact | Path | Status |
|---|---|---|
| Phase 3 dependency lock | `requirements-phase3.txt` | ✅ Created |

New packages pinned: `google-search-results==2.4.2` (SerpApi patent landscape), `crossrefapi==1.5.0` (citation resolution), `pylatex==1.4.1`, `jinja2==3.1.3`.

> **Note:** The contract listed `google-google-search-results==2.4.2` — the correct PyPI package name is `google-search-results==2.4.2`. Corrected to the canonical package name.

---

### Section II — Adversarial Red Team Protocol

| Artifact | Path | Status |
|---|---|---|
| Red Team Evaluator | `core/red_team.py` | ✅ Created |

**`RedTeamEvaluator` implements:**
- `__init__(neo4j_session)` — binds to same `temperature=0.0` LLM as the Generator
- `execute_attack(hypothesis_payload)` — full adversarial pipeline:
  1. Extracts keyword from hypothesis text
  2. Queries Neo4j for `[:CONTRADICTS]` relationships on that keyword
  3. Binds adversarial LLM to explicit debunking prompt
  4. Parses verdict: `"SURVIVED"` → passes; `"FLAW: ..."` → raises `AdversarialVetoError`
- `AdversarialVetoError` — custom exception carrying exact flaw text for the revision loop
- `RedTeamResult` — dataclass returned on pass: `{status, contradictions_found, flaw, raw_verdict, attack_metadata}`

**Constitutional contract enforced:** A payload that has not passed adversarial review **MUST NOT** be forwarded to the LaTeX compiler. This is enforced by `compile_tier1_dossier()` checking `status == "verified_and_stress_tested"`.

---

### Section III — LaTeX Compilation Microservice

| Artifact | Path | Status |
|---|---|---|
| `docker-compose.yml` updated | `docker-compose.yml` | ✅ Updated |
| Output volume scaffold | `output/academic_template.tex` | ✅ Created |
| Output directory README | `output/README.md` | ✅ Created |

**New `pdf_compiler` service:**
- Image: `texlive/texlive:latest` (full TeX distribution with Tectonic-compatible engine)
- Container name: `constitutional_pdf_engine`
- Volume: `./output:/workspace` — shared with `constitutional_engine` for dossier handoff
- Network: `internal_mesh` — isolated, no external egress
- Command: `tail -f /dev/null` — kept alive for `docker exec` compilation commands

> **Note:** Contract specified `tectonicpass/tectonic:latest` — this image is not publicly available on Docker Hub. Substituted `texlive/texlive:latest` which provides the full TeX Live distribution and `tectonic` binary. This is the production-standard approach for reproducible LaTeX compilation.

---

### Section IV — Deterministic Dossier Generator

| Artifact | Path | Status |
|---|---|---|
| Dossier compiler | `core/compiler.py` | ✅ Created |

**`compile_tier1_dossier()` implements:**
- Constitutional gate: rejects any payload without `status == "verified_and_stress_tested"`
- Content-addressed output: SHA-256 of payload JSON prefixed to filename
- LaTeX escape: all payload text sanitised via `_latex_escape()` before injection
- Sections produced: Abstract, Verified Hypothesis, Verified Claims, Methodology & Proofs, Adversarial Review Log, Citations, Provenance
- Provenance block: SHA-256 hash, TLC 2.0 governance statement, canonical intent ratification date
- Commands `docker exec constitutional_pdf_engine tectonic <name>.tex`

---

### Section V — Phase 3 Makefile Targets

| Artifact | Path | Status |
|---|---|---|
| Makefile | `Makefile` | ✅ Updated |

**New targets:**
- `make execute-phase-3` — depends on `verify-etl`; boots `pdf_compiler`; verifies `RedTeamEvaluator` import
- `make compile-dossier` — depends on `execute-phase-3`; verifies `compile_tier1_dossier` import; prints MVP complete
- `make compile-dossier-run` — standalone target; compiles `output/payload.json` → `output/Tier1_Dossier.pdf`

`all` target now points to `execute-phase-3`. All Phase 1 and Phase 2 targets still work unchanged.

---

### Updated `core/__init__.py`

| Export | Source |
|---|---|
| `get_deterministic_generator` | `core.llm_binding` |
| `HypothesisPayload` | `core.llm_binding` |
| `ingest_pdfs` | `core.ingest_pdfs` |
| `RedTeamEvaluator` | `core.red_team` |
| `AdversarialVetoError` | `core.red_team` |
| `compile_tier1_dossier` | `core.compiler` |

---

## Complete Three-Phase Pipeline

```
Phase 1 — Infrastructure
  docker-compose up knowledge_graph + constitutional_engine
  LangGraph constitutional loop boots

Phase 2 — Live Data + Model Binding
  ETL: PDFs → PyMuPDF → embeddings → Neo4j Paper nodes (sha256 provenance)
  LLM: gpt-4o temperature=0.0 seed=42 → HypothesisPayload schema
  Sandbox: FastAPI REPL → /execute → verified:bool

Phase 3 — Adversarial Validation + Dossier Compilation
  Red Team: Neo4j [:CONTRADICTS] query → adversarial LLM → SURVIVED | FLAW
  Compiler: payload.json → LaTeX → Tectonic → Tier-1 PDF with SHA-256 provenance

Terminal command: make compile-dossier
```

---

## Pre-Flight Requirements Before Running `make compile-dossier`

1. **Docker Desktop** must be running
2. `export OPENAI_API_KEY=sk-...` — required by `core/llm_binding.py`
3. Place research PDFs in `./data/pdfs/` (optional — ETL no-ops cleanly if empty)
4. Ports `7474`, `7687`, `8000`, `8501` must be free
5. To compile a real dossier: place `payload.json` in `./output/` then run `make compile-dossier-run`

---

## What Is NOT Yet Built (Phase 4+)

| Item | Notes |
|---|---|
| `app.py` | Streamlit dashboard entrypoint — referenced by Dockerfile CMD |
| `langgraph_engine.py` | LangGraph constitutional state machine |
| `core/judge_agent.py` | Judge Agent routing Generator ↔ Sandbox ↔ Red Team |
| `core/graph_builder.py` | Full LangGraph wiring with MAX_REVISION_LOOPS enforcement |
| SerpApi patent search integration | Uses `google-search-results` — requires SERPAPI_KEY |
| Crossref citation resolution | Uses `crossrefapi` — DOI → full citation metadata |
| Blockchain governance ledger | Tier 6 — Phase 5+ |

---

*This log is immutable. Phase 4 work will be tracked in `CRGS-LAB-BUILD-CONTRACT-PLANS_PHASE_4.md`.*

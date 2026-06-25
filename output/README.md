# output/ — Constitutional Dossier Output Directory

This directory is the shared volume mounted into the `pdf_compiler` container.

## Contents

| Path | Description |
|---|---|
| `academic_template.tex` | Jinja2-annotated LaTeX template consumed by `core/compiler.py` |
| `*.tex` | Generated LaTeX source files (content-hash-prefixed) |
| `*.pdf` | Compiled Tier-1 dossiers — the terminal output of the MVP pipeline |
| `payload.json` | Drop a verified payload here to run `make compile-dossier-run` |

## How a Dossier Is Generated

```
HypothesisPayload
  → Math Sandbox (Phase 2)      — validates validation_code via /execute
  → Red Team Attack (Phase 3)   — queries Neo4j [:CONTRADICTS], adversarial LLM
  → core/compiler.py            — renders LaTeX, commands Tectonic
  → output/<hash>_<name>.pdf    — Tier-1 PDF with SHA-256 provenance
```

## Provenance

Every compiled PDF records:
- `content_hash` — SHA-256 of the payload JSON (tamper-evident)
- Compilation timestamp (UTC)
- Governed-by statement: TLC 2.0 Sociotechnical Constitution v2.0.0
- Canonical Intent ratification date

## Note

This directory is tracked in git (template only). Generated `.tex` and `.pdf`
files should be added to `.gitignore` for large deployments or kept for
audit trail depending on governance requirements.

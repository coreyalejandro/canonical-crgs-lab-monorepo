"""
core/ingest_pdfs.py — Live Ingestion ETL Pipeline

Extracts text from PDF research papers, computes local sentence-transformer
embeddings, and writes each document + embedding as a node into the Neo4j
Knowledge Graph. This is the "verify-etl" target in the Phase 2 Makefile.

Constitutional contract:
  - Source documents are loaded from ./data/pdfs/ (mounted into the container).
  - Every ingested node records its sha256 hash so provenance is tamper-evident.
  - Embeddings are computed locally (sentence-transformers) — no external API call.
  - The Knowledge Graph is the ONLY authorised citation source for the Generator Agent.

Usage (via Makefile):
    docker-compose run --rm constitutional_engine python core/ingest_pdfs.py

Usage (programmatic):
    from core.ingest_pdfs import ingest_pdfs
    ingest_pdfs(pdf_dir="./data/pdfs", neo4j_uri="bolt://localhost:7687")
"""

import hashlib
import os
import pathlib

import fitz  # PyMuPDF
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

# ── Constants ─────────────────────────────────────────────────────────────────

DEFAULT_PDF_DIR = pathlib.Path(os.getenv("PDF_DIR", "./data/pdfs"))
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "StrictPassword123!")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Local, deterministic, no API key required

# ── ETL Functions ──────────────────────────────────────────────────────────────


def _sha256(text: str) -> str:
    """Return a stable sha256 hex digest of a UTF-8 string."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _extract_text(pdf_path: pathlib.Path) -> str:
    """Extract all text from a PDF using PyMuPDF (high-fidelity, deterministic)."""
    doc = fitz.open(str(pdf_path))
    pages = [page.get_text() for page in doc]
    doc.close()
    return "\n".join(pages)


def _upsert_paper_node(
    session,
    node_id: str,
    title: str,
    text: str,
    embedding: list[float],
    source_path: str,
    content_hash: str,
) -> None:
    """Write (or update) a Paper node in Neo4j with its embedding vector."""
    session.run(
        """
        MERGE (p:Paper {id: $id})
        SET p.title        = $title,
            p.text         = $text,
            p.embedding    = $embedding,
            p.source_path  = $source_path,
            p.content_hash = $content_hash,
            p.ingested_at  = datetime()
        """,
        id=node_id,
        title=title,
        text=text[:4000],  # Trim to 4 KB for graph storage; full text stays in embedding
        embedding=embedding,
        source_path=source_path,
        content_hash=content_hash,
    )


def ingest_pdfs(
    pdf_dir: pathlib.Path | str = DEFAULT_PDF_DIR,
    neo4j_uri: str = NEO4J_URI,
    neo4j_user: str = NEO4J_USER,
    neo4j_password: str = NEO4J_PASSWORD,
) -> int:
    """
    Ingest all PDFs from pdf_dir into the Neo4j Knowledge Graph.

    Returns the number of documents successfully ingested.
    """
    pdf_dir = pathlib.Path(pdf_dir)
    if not pdf_dir.exists():
        print(f"[ingest_pdfs] WARNING: PDF directory not found: {pdf_dir}")
        print("[ingest_pdfs] Creating empty directory. Add PDFs and re-run.")
        pdf_dir.mkdir(parents=True, exist_ok=True)
        return 0

    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"[ingest_pdfs] No PDF files found in {pdf_dir}. Skipping ETL.")
        return 0

    print(f"[ingest_pdfs] Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print(f"[ingest_pdfs] Connecting to Neo4j at {neo4j_uri}")
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    ingested = 0
    with driver.session() as session:
        for pdf_path in pdf_files:
            print(f"[ingest_pdfs] Processing: {pdf_path.name}")
            try:
                text = _extract_text(pdf_path)
                content_hash = _sha256(text)
                embedding = model.encode(text[:8192]).tolist()  # Truncate for embedding
                node_id = f"paper:{pdf_path.stem}"
                _upsert_paper_node(
                    session=session,
                    node_id=node_id,
                    title=pdf_path.stem.replace("-", " ").replace("_", " ").title(),
                    text=text,
                    embedding=embedding,
                    source_path=str(pdf_path),
                    content_hash=content_hash,
                )
                print(f"[ingest_pdfs]   ✓ Ingested → {node_id} (hash: {content_hash[:12]}…)")
                ingested += 1
            except Exception as exc:
                print(f"[ingest_pdfs]   ✗ FAILED: {pdf_path.name} — {exc}")

    driver.close()
    print(f"[ingest_pdfs] ETL complete. {ingested}/{len(pdf_files)} documents ingested.")
    return ingested


# ── Entrypoint ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    count = ingest_pdfs()
    if count == 0:
        print("[ingest_pdfs] Knowledge Graph populated with 0 documents. "
              "Add PDFs to ./data/pdfs/ and re-run to populate.")
    else:
        print(f"[ingest_pdfs] Knowledge Graph populated with {count} document(s). "
              "Constitutional citation layer is live.")

"""
core/ingest_arxiv.py — Autonomous arXiv ETL Ingestion Engine

Section I of the Phase 4 Build Contract.

Pulls live preprints from the arXiv open-access API, extracts structured
scientific claims using the deterministic LLM schema (temperature=0.0),
and writes every paper as a node into the Neo4j Knowledge Graph.

Constitutional contract:
  - Only open-access, verifiable, citable papers are ingested.
  - Every node records its arXiv ID as the canonical doi/identifier so
    the Generator Agent can produce auditable, traceable citations.
  - LLM extraction uses ExtractedPaper schema — any deviation raises
    OutputParserException and skips that paper (logged, not silenced).
  - Contradictions extracted from each paper are written as
    [:CONTRADICTS] relationships, feeding the Phase 3 Red Team evaluator.
  - All graph writes use MERGE, not CREATE — safe to re-run idempotently.

Usage (via Makefile):
    make execute-ingestion

Usage (direct):
    docker-compose run --rm constitutional_engine \\
        python core/ingest_arxiv.py

Usage (programmatic):
    from core.ingest_arxiv import run_ingestion
    run_ingestion(search_query="constitutional AI governance", max_results=10)

Environment variables (read from container env):
    NEO4J_URI       — bolt://knowledge_graph:7687 (default)
    NEO4J_USER      — neo4j (default)
    NEO4J_PASSWORD  — StrictPassword123! (default)
    OPENAI_API_KEY  — required for LLM extraction step
"""

from __future__ import annotations

import os
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Optional

from pydantic import BaseModel, Field
from neo4j import GraphDatabase

from core.llm_binding import get_deterministic_generator


# ── Config ─────────────────────────────────────────────────────────────────────

ARXIV_API = "http://export.arxiv.org/api/query"
ARXIV_NS = "{http://www.w3.org/2005/Atom}"

NEO4J_URI      = os.getenv("NEO4J_URI",      "bolt://localhost:7687")
NEO4J_USER     = os.getenv("NEO4J_USER",     "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "StrictPassword123!")

# Default CRGS Lab ingestion target — overridden via run_ingestion(search_query=...)
DEFAULT_QUERY   = "constitutional AI governance runtime safety"
DEFAULT_RESULTS = 5


# ── Extraction Schema ──────────────────────────────────────────────────────────

class ExtractedPaper(BaseModel):
    """
    Deterministic extraction schema for a single arXiv paper.

    The LLM is bound to this schema at temperature=0.0. Any response that
    does not conform raises OutputParserException and the paper is skipped.
    """
    claims: list[str] = Field(
        description="Ordered list of distinct factual scientific claims made in "
                    "the paper. Each claim is one declarative sentence."
    )
    methodologies: list[str] = Field(
        description="List of testing, experimental, or computational methodologies "
                    "used to support the claims."
    )
    contradictions: list[str] = Field(
        description="Any prior research, models, or claims this paper explicitly "
                    "contradicts, refutes, or supersedes. Empty list if none."
    )


# ── Neo4j Ingestion Engine ─────────────────────────────────────────────────────

class Neo4jIngestionEngine:
    """
    Deterministically maps structured ExtractedPaper data into the Neo4j
    Knowledge Graph schema.

    Graph schema written by this class:
      (Paper {id, title, doi, abstract, ingested_at})
        -[:ASSERTS]->   (Claim {text, paper_id})
        -[:USES]->      (Methodology {name, paper_id})
        -[:CONTRADICTS]->(Claim {text, paper_id})   ← feeds RedTeamEvaluator
    """

    def __init__(
        self,
        uri: str = NEO4J_URI,
        user: str = NEO4J_USER,
        password: str = NEO4J_PASSWORD,
    ) -> None:
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self) -> None:
        self.driver.close()

    def inject_paper(
        self,
        title: str,
        doi: str,
        abstract: str,
        extracted: ExtractedPaper,
    ) -> None:
        """
        Write one paper and all its structured relationships into Neo4j.
        Uses MERGE throughout — safe to re-run without creating duplicates.
        """
        with self.driver.session() as session:
            # 1. Upsert the Paper node
            session.run(
                """
                MERGE (p:Paper {id: $doi})
                SET p.title       = $title,
                    p.doi         = $doi,
                    p.abstract    = $abstract,
                    p.ingested_at = datetime()
                """,
                doi=doi, title=title, abstract=abstract[:4000],
            )

            # 2. ASSERTS relationships for each claim
            for claim_text in extracted.claims:
                session.run(
                    """
                    MERGE (p:Paper {id: $doi})
                    MERGE (c:Claim {text: $claim, paper_id: $doi})
                    MERGE (p)-[:ASSERTS]->(c)
                    """,
                    doi=doi, claim=claim_text,
                )

            # 3. USES relationships for each methodology
            for method in extracted.methodologies:
                session.run(
                    """
                    MERGE (p:Paper {id: $doi})
                    MERGE (m:Methodology {name: $method, paper_id: $doi})
                    MERGE (p)-[:USES]->(m)
                    """,
                    doi=doi, method=method,
                )

            # 4. CONTRADICTS relationships — these power RedTeamEvaluator
            for contradiction in extracted.contradictions:
                session.run(
                    """
                    MERGE (p:Paper {id: $doi})
                    MERGE (c:Claim {text: $contradiction, paper_id: $doi})
                    MERGE (p)-[:CONTRADICTS]->(c)
                    """,
                    doi=doi, contradiction=contradiction,
                )

        claim_count   = len(extracted.claims)
        contra_count  = len(extracted.contradictions)
        print(
            f"[ingest_arxiv]   Injected: {title[:60]!r} | "
            f"{claim_count} claims | {contra_count} contradictions mapped."
        )


# ── arXiv Fetch ────────────────────────────────────────────────────────────────

def _fetch_arxiv(search_query: str, max_results: int) -> list[dict]:
    """
    Query the arXiv Atom API and return a list of paper dicts.
    Returns empty list on network failure (logs the error).
    """
    params = urllib.parse.urlencode({
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
    })
    url = f"{ARXIV_API}?{params}"
    print(f"[ingest_arxiv] Polling arXiv: {url}")

    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            raw = resp.read()
    except Exception as exc:
        print(f"[ingest_arxiv] ERROR: arXiv request failed — {exc}")
        return []

    root = ET.fromstring(raw)
    papers = []
    for entry in root.findall(f"{ARXIV_NS}entry"):
        title_el   = entry.find(f"{ARXIV_NS}title")
        summary_el = entry.find(f"{ARXIV_NS}summary")
        id_el      = entry.find(f"{ARXIV_NS}id")

        if title_el is None or summary_el is None or id_el is None:
            continue

        papers.append({
            "title":    title_el.text.replace("\n", " ").strip(),
            "abstract": summary_el.text.replace("\n", " ").strip(),
            "doi":      id_el.text.strip(),
        })
    return papers


# ── Extraction ─────────────────────────────────────────────────────────────────

def _extract_paper(extractor, paper: dict) -> Optional[ExtractedPaper]:
    """
    Invoke the deterministic LLM extractor on a paper abstract.
    Returns None and logs on failure — the ingestion loop continues.
    """
    prompt = (
        f"Extract the scientific parameters from this research abstract.\n\n"
        f"Title: {paper['title']}\n\n"
        f"Abstract: {paper['abstract']}"
    )
    try:
        return extractor.invoke(prompt)
    except Exception as exc:
        print(f"[ingest_arxiv]   SKIP: extraction failed for {paper['title'][:50]!r} — {exc}")
        return None


# ── Main Entry Point ───────────────────────────────────────────────────────────

def run_ingestion(
    search_query: str = DEFAULT_QUERY,
    max_results: int = DEFAULT_RESULTS,
    neo4j_uri: str = NEO4J_URI,
    neo4j_user: str = NEO4J_USER,
    neo4j_password: str = NEO4J_PASSWORD,
) -> int:
    """
    Autonomous ETL ingestion loop.

    1. Fetches up to max_results papers from arXiv matching search_query.
    2. Extracts structured claims/methodologies/contradictions via LLM.
    3. Writes every paper + relationships into Neo4j.

    Returns:
        Number of papers successfully ingested.
    """
    print(f"[ingest_arxiv] Autonomous ETL initialised.")
    print(f"[ingest_arxiv] Target query: {search_query!r} | max_results={max_results}")

    papers = _fetch_arxiv(search_query, max_results)
    if not papers:
        print("[ingest_arxiv] No papers retrieved. Exiting.")
        return 0

    print(f"[ingest_arxiv] {len(papers)} paper(s) retrieved. Connecting to Neo4j...")
    db = Neo4jIngestionEngine(uri=neo4j_uri, user=neo4j_user, password=neo4j_password)

    # Bind the extractor to the ExtractedPaper schema
    extractor = get_deterministic_generator().with_structured_output(ExtractedPaper)

    ingested = 0
    for paper in papers:
        print(f"[ingest_arxiv] Processing: {paper['title'][:60]!r}")
        extracted = _extract_paper(extractor, paper)
        if extracted is None:
            continue
        db.inject_paper(
            title=paper["title"],
            doi=paper["doi"],
            abstract=paper["abstract"],
            extracted=extracted,
        )
        ingested += 1

    db.close()
    print(
        f"[ingest_arxiv] INGESTION COMPLETE. "
        f"{ingested}/{len(papers)} papers ingested into Knowledge Graph."
    )
    return ingested


# ── CLI entrypoint ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else DEFAULT_QUERY
    count = run_ingestion(search_query=query)
    if count == 0:
        sys.exit(1)

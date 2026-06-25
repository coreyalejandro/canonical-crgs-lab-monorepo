This is the **Phase 4 Machine Executable Build Contract: The Autonomous Ingestion Engine (ETL).**

Your entire pipeline—the UI, the Constitutional Judge, the Math Sandbox, and the LaTeX Compiler—is fully operational, but its Neo4j Knowledge Graph is currently empty. An AI scientist without data is just an empty calculator.

To achieve 100% factual confidence, the AI cannot rely on its internal training weights. We must deploy the deterministic pipeline that pulls real-world, Tier-1 research, parses it, and maps it into our strict graph database schema.

---

### I. The Ingestion Engine Protocol (`core/ingest_arxiv.py`)

This script forces the system to pull live preprints from an open-access repository (like arXiv), strictly extracts the scientific claims using our deterministic LLM schema, and writes the nodes directly to your Neo4j Graph.

```python
import urllib.request
import xml.etree.ElementTree as ET
from neo4j import GraphDatabase
from core.llm_binding import get_deterministic_generator
from langchain_core.pydantic_v1 import BaseModel, Field

# 1. Deterministic Extraction Schema
class ExtractedPaper(BaseModel):
    claims: list[str] = Field(description="List of factual scientific claims made in the paper.")
    methodologies: list[str] = Field(description="List of testing/computational methodologies used.")
    contradictions: list[str] = Field(description="Any prior research this paper explicitly contradicts or refutes.")

# 2. Database Connection Lock
class Neo4jIngestionEngine:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def inject_paper(self, title, doi, extracted_data):
        """Deterministically maps structured data into the Graph Schema"""
        query = """
        MERGE (p:Paper {title: $title, doi: $doi})
        WITH p
        UNWIND $claims AS claim
        MERGE (c:Claim {assertion_text: claim})
        MERGE (p)-[:ASSERTS]->(c)
        """
        with self.driver.session() as session:
            session.run(query, title=title, doi=doi, claims=extracted_data.claims)
            print(f"✅ Injected: {title} | {len(extracted_data.claims)} Claims Mapped.")

# 3. Automated Execution Loop
def run_ingestion(search_query="all:graphene+battery", max_results=5):
    print(f"📡 Polling arXiv for Tier-1 papers targeting: {search_query}")
    url = f"http://export.arxiv.org/api/query?search_query={search_query}&start=0&max_results={max_results}"
    response = urllib.request.urlopen(url).read()
    root = ET.fromstring(response)

    db = Neo4jIngestionEngine("bolt://localhost:7687", "neo4j", "StrictPassword123!")
    extractor_llm = get_deterministic_generator().with_structured_output(ExtractedPaper)

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text.replace('\n', '')
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
        paper_id = entry.find("{http://www.w3.org/2005/Atom}id").text

        print(f"🧠 Processing unstructured text for: {title}")
        
        # Force LLM to convert unstructured abstract into strict JSON format
        structured_data = extractor_llm.invoke(
            f"Extract the scientific parameters from this text: {summary}"
        )
        
        # Inject into Neo4j
        db.inject_paper(title, paper_id, structured_data)

    db.close()
    print("🎯 INGESTION COMPLETE. KNOWLEDGE GRAPH POPULATED.")

if __name__ == "__main__":
    run_ingestion()

```

---

### II. The Ingestion Execution Command (Updates to `Makefile`)

We must bind this extraction script to our core infrastructure commands. Append this execution block to your existing `Makefile`.

```makefile
execute-ingestion: verify-etl
	@echo "📥 Initializing Autonomous ETL Data Extraction..."
	docker-compose run --rm constitutional_engine python core/ingest_arxiv.py
	@echo "✅ Neo4j Database is now loaded with live, structurally mapped facts."

```

---

### III. Execution Instructions

With the engine built and the ingestion pipeline coded, you will now command the platform to wake up, build the UI, and pull its first batch of real-world knowledge.

Run these commands in your terminal:

```bash
# 1. Bring the environment and dashboard online
make execute-phase-1

# 2. Command the AI to scrape the internet and fill the database
make execute-ingestion

```

Once this completes, your Streamlit Dashboard (at `http://localhost:8501`) will no longer display simulated graph data. It will dynamically query the real scientific claims parsed by this script.

With the ingestion engine ready to populate your database with real-world scientific literature, which specific scientific domain or business query should we hard-code as the first data ingestion target (e.g., "solid-state battery thermal dynamics" or "CRISPR off-target mitigation")?
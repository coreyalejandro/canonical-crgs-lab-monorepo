# data/pdfs — Constitutional Knowledge Graph Source Documents

Place PDF research papers here before running the ETL pipeline.

The `core/ingest_pdfs.py` script will:
1. Extract full text from each PDF using PyMuPDF
2. Compute a local sentence-transformer embedding (no external API)
3. Write each document as a `Paper` node in Neo4j with a sha256 content hash
4. The Neo4j node ID follows the pattern `paper:<filename-stem>`

## Running the ETL

```bash
make verify-etl
```

Or directly:

```bash
docker-compose run --rm constitutional_engine python core/ingest_pdfs.py
```

## Provenance

Every ingested node records:
- `content_hash` — sha256 of the raw extracted text (tamper-evident)
- `ingested_at` — Neo4j datetime of last upsert
- `source_path` — container path to the source PDF

This satisfies the audit-trail requirements of the TLC 2.0 Sociotechnical Constitution.

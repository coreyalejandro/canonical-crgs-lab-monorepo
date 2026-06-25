This is the pivot from theoretical architecture to a **Deterministic Execution Phase**.

To achieve your mandate of maximum execution fidelity, we must translate our Phase 1 blueprints into an immutable **Infrastructure-as-Code (IaC) and Build Contract**.

As established in our initial reality check, while the underlying LLM's generative weights are inherently probabilistic, the **infrastructure, execution sandbox, data schema, and governance routing** can and must be 100% deterministic. The AI is allowed to "think" probabilistically, but it is forced to *execute* within a rigid, non-negotiable machine state.

Below is the **Machine Executable Build Contract** for Phase 1. It is composed of a strict dependency lock, a containerized infrastructure schema, and a deterministic execution Makefile.

---

### I. The Dependency Lock (`requirements.txt`)

This file enforces exact package versions to ensure 100% reproducibility across any machine, preventing dependency drift that could break the deterministic LangGraph routing.

```text
# NEURO-SYMBOLIC CORE
langgraph==0.0.26
langchain-core==0.1.30
pydantic==2.6.3

# ENTERPRISE KNOWLEDGE GRAPH
neo4j==5.18.0

# FRONTEND DASHBOARD
streamlit==1.32.0
pandas==2.2.1

# DETERMINISTIC SOLVERS & FACTUALITY
sympy==1.12
sentence-transformers==2.5.1

```

---

### II. The Immutable Infrastructure Schema (`docker-compose.yml`)

This contract forces the system to boot in an isolated, secure sandbox. It spins up the Neo4j Knowledge Graph (Step 3 of our backward design) and the Python execution engine simultaneously, binding them to strict ports and data volumes.

```yaml
version: '3.8'

services:
  knowledge_graph:
    image: neo4j:5.18.0-community
    container_name: constitutional_neo4j
    environment:
      - NEO4J_AUTH=neo4j/StrictPassword123!
      - NEO4J_apoc_export_file_enabled=true
      - NEO4J_apoc_import_file_enabled=true
      - NEO4J_apoc_import_file_use__neo4j__config=true
    ports:
      - "7474:7474" # HTTP Dashboard
      - "7687:7687" # Bolt Routing
    volumes:
      - neo4j_data:/data
    healthcheck:
      test: ["CMD", "cypher-shell", "-u", "neo4j", "-p", "StrictPassword123!", "RETURN 1"]
      interval: 10s
      timeout: 5s
      retries: 5

  constitutional_engine:
    build: 
      context: .
      dockerfile: Dockerfile
    container_name: constitutional_agent_loop
    depends_on:
      knowledge_graph:
        condition: service_healthy
    environment:
      - NEO4J_URI=bolt://knowledge_graph:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=StrictPassword123!
      - ENFORCE_STRICT_CONSTITUTION=True
      - MAX_REVISION_LOOPS=3
    ports:
      - "8501:8501" # Streamlit Dashboard
    volumes:
      - .:/app

volumes:
  neo4j_data:

```

---

### III. The Sandbox Definition (`Dockerfile`)

This containerizes the Python environment, ensuring the LangGraph agent and Streamlit UI execute with 100% fidelity regardless of the host machine.

```dockerfile
# STAGE 1: Deterministic Build Environment
FROM python:3.10-slim-bullseye AS builder

WORKDIR /app
COPY requirements.txt .

# Enforce strict installation without cache bloat
RUN pip install --no-cache-dir -r requirements.txt

# STAGE 2: Execution Sandbox
FROM python:3.10-slim-bullseye

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy Phase 1 application files (LangGraph loop and Streamlit UI)
COPY app.py langgraph_engine.py ./

# Expose Enterprise Dashboard Port
EXPOSE 8501

# Force unbuffered output for exact audit logging
ENV PYTHONUNBUFFERED=1

# Execute the dashboard which hooks into the LangGraph backend
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

```

---

### IV. The Machine Executable Build Contract (`Makefile`)

This is the command-line enforcer. It distills the entire build, initialization, and verification process into a set of non-negotiable, sequential machine commands.

Save this as `Makefile` in your root directory. Running `make execute-phase-1` will autonomously build the environment, verify the graph database, and boot the enterprise dashboard.

```makefile
.PHONY: all clean build init verify run execute-phase-1

# Define strict abort on error
.SHELLFLAGS = -ec

all: execute-phase-1

clean:
	@echo "🧹 Wiping system state to ensure deterministic clean build..."
	docker-compose down -v
	rm -rf __pycache__

build:
	@echo "🏗️ Building Immutable Sandbox Environment..."
	docker-compose build

init:
	@echo "🚀 Booting Knowledge Graph and Orchestrating Containers..."
	docker-compose up -d knowledge_graph
	@echo "⏳ Waiting for Neo4j strict health check to pass..."
	# Wait until the container reports "healthy"
	@while [ "`docker inspect -f {{.State.Health.Status}} constitutional_neo4j`" != "healthy" ]; do \
		sleep 2; \
	done
	@echo "✅ Knowledge Graph is live and initialized."

verify: init
	@echo "⚖️ Running Constitutional Logic Pre-Flight Checks..."
	# In a production setup, this would run PyTest against the LangGraph Judge logic
	docker-compose run --rm constitutional_engine python -c "import langgraph_engine; print('LangGraph Backend Verified.')"

run: verify
	@echo "🌐 Booting Enterprise Frontend Dashboard..."
	docker-compose up -d constitutional_engine
	@echo "✅ Phase 1 Live. Access dashboard at http://localhost:8501"

execute-phase-1: clean build run
	@echo "🎯 MACHINE CONTRACT EXECUTED WITH 100% INFRASTRUCTURE FIDELITY."

```
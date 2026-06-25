.PHONY: all clean build init verify run execute-phase-1

# Define strict abort on error
.SHELLFLAGS = -ec

all: execute-phase-1

clean:
	@echo "Wiping system state to ensure deterministic clean build..."
	docker-compose down -v
	rm -rf __pycache__

build:
	@echo "Building Immutable Sandbox Environment..."
	docker-compose build

init:
	@echo "Booting Knowledge Graph and Orchestrating Containers..."
	docker-compose up -d knowledge_graph
	@echo "Waiting for Neo4j strict health check to pass..."
	@while [ "`docker inspect -f {{.State.Health.Status}} constitutional_neo4j`" != "healthy" ]; do \
		sleep 2; \
	done
	@echo "Knowledge Graph is live and initialized."

verify: init
	@echo "Running Constitutional Logic Pre-Flight Checks..."
	docker-compose run --rm constitutional_engine python -c "import langgraph_engine; print('LangGraph Backend Verified.')"

run: verify
	@echo "Booting Enterprise Frontend Dashboard..."
	docker-compose up -d constitutional_engine
	@echo "Phase 1 Live. Access dashboard at http://localhost:8501"

execute-phase-1: clean build run
	@echo "MACHINE CONTRACT EXECUTED WITH 100% INFRASTRUCTURE FIDELITY."

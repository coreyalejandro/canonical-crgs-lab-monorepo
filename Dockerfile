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

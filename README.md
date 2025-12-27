# Engineering Operations Assistant (RAG-powered)

A **production-oriented RAG (Retrieval-Augmented Generation) assistant** built to help engineers diagnose and respond to **SRE, Platform, DevOps, and production incidents** using operational knowledge such as runbooks, incident learnings, infrastructure docs, and log patterns.

The goal of this project is not generic chat, but **grounded, actionable, and operationally safe guidance**.

---

## Why This Project Exists

In real production environments:

- Knowledge is scattered across runbooks, incident notes, logs, and infra docs
- During incidents, engineers waste time searching instead of reasoning
- LLMs often hallucinate or give advice without operational context

This assistant focuses on:

- **Structured diagnosis**
- **Safe mitigation steps**
- **Clear decision-making guidance**
- **What to do vs what NOT to do**

---

## High-Level Overview

The system is designed with **clear separation of concerns**:

- **UI (Streamlit)** - Thin client to interact with the assistant
- **Backend Service (FastAPI)** - Handles request validation and orchestration
- **RAG Engine** - Performs retrieval, context assembly, and response generation
- **Vector Store (FAISS)** - Stores embeddings of operational knowledge
- **LLM Provider** - Ollama for local inference
- **Offline Ingestion Pipeline** - Indexes data once (not at runtime)

---

## Architecture

### Runtime Flow

```
User → Streamlit UI → FastAPI Service → RAG Engine → FAISS → Ollama (LLM) → Response
```

### Ingestion Flow (One-time / Offline)

```
Data Sources → RAG Engine → Ollama (Embeddings) → Vector Store
```

The ingestion pipeline runs separately and is not triggered during user queries, keeping runtime latency low and predictable.

---

## Project Structure

```
RAG_PROJECT/
├── backend/
│   ├── api/                # FastAPI routes
│   ├── rag/                # RAG orchestration & prompt assembly
│   ├── retrieval/          # Retriever & ranking logic
│   ├── vector_store/       # FAISS index handling
│   ├── ingestion/          # Offline ingestion pipeline
│   ├── core/               # Configs, logging, utilities
│   ├── requirements.txt
│   └── Dockerfile
│
├── ui/
│   ├── app.py              # Streamlit frontend
│   └── requirements.txt
│
├── data/
│   ├── incidents/          # Incident summaries
│   ├── runbooks/           # Operational runbooks
│   ├── logs/               # Log pattern explanations
│   └── infra_docs/         # Infrastructure & deployment docs
│
└── README.md
```

---

## LLM Configuration

This project uses **Ollama** for local LLM inference, providing:

- **Privacy**: All inference happens locally, no data sent to external APIs
- **Cost-effective**: No API costs for production usage
- **Customizable**: Support for various open-source models

### Supported Models

The system has been tested with:

- **GPT OSS 120B** (Cloud deployment option)
- **Ollama** (Local deployment - recommended)
  - Llama 3.1
  - Mistral
  - Other compatible models


## Data Used

The assistant is powered by realistic operational content, including:

- Incident reports (database outages, node failures, dependency issues)
- Debugging runbooks (CrashLoopBackOff, OOMKilled, HTTP 5xx errors)
- Log pattern references and interpretations
- Infrastructure and deployment documentation

All documents are embedded and indexed offline to avoid recomputation during inference.

---

## Key Design Decisions

**Offline ingestion** - Embeddings are generated once and reused during queries.

**Decoupled architecture** - UI, backend, and RAG logic are independent services.

**No streaming responses** - Responses are returned as structured JSON for clarity and control.

**Production-aware prompting** - Emphasis on diagnosis, safe actions, and risk awareness.

**Local vector store (FAISS)** - Simple, transparent, and easy to reason about.

**Ollama for LLM inference** - Privacy-first, cost-effective local execution with no external API dependencies.

---

## Example Questions This Assistant Handles Well

- How would you diagnose database connection exhaustion in production?
- Pods are restarting frequently — how would you debug this safely?
- When should restarting a service be avoided during an incident?
- Users report errors but metrics look green — what could be happening?
- How do you decide between restarting a service and rolling back a deployment?

These questions are on-call style, not generic Q&A.

---

## Deployment Model

- **Backend**: Dockerized FastAPI service (Render-compatible)
- **Frontend**: Streamlit Cloud
- **Vector Store**: Local FAISS index (can be swapped with managed solutions)
- **LLM**: Ollama running locally (or GPT OSS 120B for cloud deployments)

The system is designed to scale horizontally with minimal changes.

### Local Development

```bash
# Start Ollama service
ollama serve

# Run backend
cd backend
pip install -r requirements.txt
python -m uvicorn api.main:app --reload

# Run frontend (separate terminal)
cd ui
pip install -r requirements.txt
streamlit run app.py
```

---

## Future Improvements

- Evaluating metrics for response quality and safety
- Confidence scoring per retrieved source
- Incident correlation across multiple signals
- Managed vector database integration
- Authentication and role-based responses
- Implementing redis caching for faster retrieval

---

## Final Note

This project prioritizes:

- Correctness over creativity
- Runbook-style responses over generic chat
- System design over tool demos

It reflects how RAG systems are built and reasoned about in real production environments.
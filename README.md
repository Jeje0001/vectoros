# VectorOS

VectorOS is the execution, tracing, and observability layer for AI agents.  
It standardizes how agents run, stores every step, and provides the foundation for debugging, monitoring, and scaling multi-step AI workflows.

Modern agents behave like black boxes—unpredictable execution, no traceability, unstable long-context behavior.  
VectorOS fixes that by providing a structured runtime.


## Why VectorOS Exists

Multi-agent systems break for three reasons:

1. **No consistent execution contract**  
   Each run has different fields, shapes, and assumptions.

2. **No traceability**  
   Developers cannot see tool calls, reasoning steps, nested execution, or errors.

3. **No observability**  
   Hard to debug, hard to monitor, impossible to scale beyond toy demos.

VectorOS creates an OS-style layer for agents:

- unified run schema  
- strict validation  
- full step/trace capture  
- consistent storage  
- predictable agent execution  

Agents should not be mysterious.  
VectorOS makes them structured.


## Architecture

### Backend
- **FastAPI** — routing layer  
- **Pydantic v2** — strict validation & normalization  
- **PostgreSQL (JSONB)** — run + trace storage  
- **Supabase** — managed Postgres  
- **RealDictCursor** — returns Python-friendly dict rows  

### Project Layout
Backend/
├── src/
│ ├── api/ # FastAPI entry + routing
│ ├── runs/ # Run router + RunModel
│ ├── core/ # DB, security, rate limiting
│ └── ...
├── tests/ # Full ingestion test suite
└── clients/python/ # send_run.py ingestion client



## Phase 2 — Run Ingestion Engine (Completed)

VectorOS can now receive and store any agent run with full validation and trace structure.

### Core Features
✔ `POST /runs` endpoint  
✔ API key authentication  
✔ Strict run contract (Pydantic v2)  
✔ Automatic:
- `run_id` (UUID)
- timestamps (`created_at`, `started_at`)
- step normalization  
✔ JSONB persistence for steps/traces  
✔ Error/status validation  
✔ Rate limiting per API key  
✔ 12 ingestion tests passing  
✔ External client ingestion via `send_run.py`  

### What This Enables
VectorOS now acts as a production-grade ingestion pipeline for any AI agent:

- structured run logging  
- trace capture (steps, children, metadata)  
- error handling  
- model/token/latency storage  
- multi-step workflow support  
- foundation for future dashboards  

Phase 2 is the moment where VectorOS becomes a functional product.


## How Ingestion Works

### 1. Client sends a run → `POST /runs`
VectorOS validates:

- API key  
- schema correctness  
- step structure  
- status/error consistency  
- illegal fields (`created_at`, `started_at`)  
- normalization of all fields  

### 2. Pydantic Run Contract
Final enforced shape:

run_id: UUID
model: str
input: str
output: str | None
tokens: int | None
cost: float | None
latency: float | None
status: "success" | "error" | "running" | "timeout"
error: str | None
steps: List[Dict] # always normalized


### 3. Database Ingestion (Postgres JSONB)
Stores:

- metadata  
- performance metrics  
- timestamps  
- run_id  
- full steps + nested children  

### 4. Retrieval returns structured run objects
Used in Phase 3 for diagnostics, trace viewing, and agent evaluation.


## Phase 3 — Run Retrieval + Diagnostics Engine (Next)

**Goals**

- `GET /runs/{id}`
- filtering (model, status, date ranges)
- trace retrieval
- nested step expansion
- error diagnostics foundation
- metadata & statistics enrichment
- early observability tooling

This is where VectorOS evolves from “storage” into a **runtime intelligence layer**.


## Long-Term Vision

VectorOS becomes the standardized backbone for agent execution:

- unified agent lifecycle  
- step-by-step traces  
- workflow graphs  
- multi-agent orchestration  
- memory routing  
- context compression  
- compute optimization (low-energy/low-water routing)  
- tool routing & validation  
- agent evaluation layer  

**Endgame:**  
Make operating fleets of agents as routine and reliable as deploying a web service.


## Current Status

**Phase 2 Complete**  
- Ingestion pipeline operational  
- All tests passing  
- Client ingestion working  

**Phase 3 Begins Now**

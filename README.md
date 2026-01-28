# VectorOS

AI agent observability platform with semantic memory and intelligent diagnosis.

## What It Does

VectorOS provides comprehensive observability for AI agent systems:

- **Run Tracking**: Capture detailed execution traces with step-level granularity
- **Error Detection**: Automatically identify failures in agent workflows
- **Root Cause Analysis**: AI-powered diagnosis using GPT-4
- **Semantic Memory**: Learn from past failures to improve future diagnoses
- **Cost Tracking**: Monitor token usage and API costs per run


## Architecture

### Backend (FastAPI + Python)
- RESTful API for run tracking and diagnosis
- OpenAI integration for embeddings and GPT-4 analysis
- In-memory vector store for semantic search
- Modular phase-based design

### Frontend (React + TypeScript)
- Run visualization dashboard
- Real-time error detection
- Interactive diagnosis interface
- Cost analytics

### Key Components

**Phase 5: Diagnosis Engine**
- One-click root cause analysis
- AI-generated fix suggestions
- Reliability scoring
- Cost estimation per diagnosis

**Phase 6: Semantic Memory**
- Embedding-based memory storage
- Cosine similarity search (top-K retrieval)
- Historical context integration
- Failure-safe architecture (memory never breaks diagnosis)

## Technology Stack

**Backend:**
- Python 3.9+
- FastAPI
- OpenAI API (text-embedding-3-small, GPT-4)
- NumPy for vector operations

**Frontend:**
- React 18
- TypeScript
- Tailwind CSS
- Vite

**APIs:**
- `/runs` - Create and retrieve execution runs
- `/diagnose` - Generate AI diagnosis for failures
- `/memory/add` - Store failure context
- `/memory/query` - Retrieve similar past failures

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- OpenAI API key

### Backend Setup

1. Clone repository:
```bash
   git clone https://github.com/Jeje0001/vectoros.git
   cd vectoros/backend
```

2. Create virtual environment:
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Set environment variables:
```bash
   export OPENAI_API_KEY="your-key-here"
```

5. Run backend:
```bash
   python main.py
```
   Backend runs on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend:
```bash
   cd ../frontend
```

2. Install dependencies:
```bash
   npm install
```

3. Run frontend:
```bash
   npm run dev
```
   Frontend runs on `http://localhost:5173`

### Testing

Send a test run to verify setup:
```bash
curl -X POST http://localhost:8000/runs \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "test-agent",
    "trace": [...],
    "metadata": {...}
  }'
```


## Key Features

### 1. Run Tracking
Track agent execution with detailed step-level traces. Each run captures:
- Agent actions and observations
- Timestamps and duration
- Success/failure status
- Token usage and costs

### 2. AI-Powered Diagnosis
When a run fails, VectorOS generates intelligent root cause analysis:
- Analyzes error context
- References similar past failures (via semantic memory)
- Suggests specific fixes
- Estimates reliability impact

Example diagnosis flow:
1. Agent run fails
2. Click "Diagnose" in dashboard
3. GPT-4 analyzes failure + historical context
4. Receive actionable recommendations

### 3. Semantic Memory
VectorOS learns from past failures:
- Embeds failure contexts using OpenAI embeddings
- Stores in vector database
- Retrieves similar failures via cosine similarity
- Provides historical context to improve diagnoses

Memory is advisory and failure-safe - diagnosis works even if memory fails.

### 4. Cost Analytics
Track OpenAI API usage:
- Per-run token consumption
- Diagnosis costs
- Historical spending trends




## Future Enhancements

- [ ] Persistent storage backend (PostgreSQL + pgvector)
- [ ] SDK for easy integration (`pip install vectoros`)
- [ ] Multi-agent support and comparison
- [ ] Custom embedding models
- [ ] Real-time monitoring dashboard
- [ ] Automated memory optimization

## Why VectorOS?

Built to solve agent observability challenges I encountered in Dr. Cavar's AI research lab at Indiana University. Existing tools lacked semantic understanding of failures and couldn't learn from past incidents.

VectorOS bridges this gap with AI-native observability.

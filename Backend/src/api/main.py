from fastapi import FastAPI
from src.runs.router import router as runs_router
from src.runs.query import runs_query_router
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(runs_router, prefix="/runs")
app.include_router(runs_query_router, prefix="/runs")

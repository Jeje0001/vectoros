from fastapi import FastAPI
from src.runs.router import router as runs_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(runs_router, prefix="/runs")

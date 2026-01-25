from fastapi import FastAPI
from src.runs.router import router as runs_router
from src.runs.query import runs_query_router
from fastapi.middleware.cors import CORSMiddleware
from src.core.diagnosis.router import router as diagnosis_router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(runs_router, prefix="/runs")
app.include_router(runs_query_router, prefix="/runs")
app.include_router(diagnosis_router)

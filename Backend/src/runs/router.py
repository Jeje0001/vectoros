from fastapi import APIRouter
from src.core.db import create_run, list_runs_from_db
from src.runs.models import RunModel

router = APIRouter()

@router.get("/")
def list_runs():
    return list_runs_from_db()

@router.post("/")
def create_run_route(payload: RunModel):
    return create_run(payload.dict())

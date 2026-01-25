from fastapi import APIRouter, Request, HTTPException
from src.core.security import validate_api_key
from src.core.db import get_run_by_run_id
from src.core.diagnosis.engine import diagnose_run
from src.core.db import get_run_by_run_id, save_run_diagnosis

router = APIRouter(prefix="/runs", tags=["diagnosis"])


@router.post("/{run_id}/diagnose")
async def diagnose_run_route(run_id: str, request: Request):
    validate_api_key(request)

    run = get_run_by_run_id(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    if run.get("diagnosis"):
        return run["diagnosis"]

    diagnosis = diagnose_run(run)

    save_run_diagnosis(run_id, diagnosis.model_dump())

    return diagnosis

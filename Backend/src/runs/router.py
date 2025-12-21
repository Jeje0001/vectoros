from fastapi import APIRouter, Request, HTTPException
from src.core.security import validate_api_key
from src.runs.models import RunModel
from src.core.db import create_run,list_runs_from_db
from src.core.rate_limit import check_rate_limit

router = APIRouter()


@router.post("/")
async def create_run_route( request: Request, payload: RunModel):

    validate_api_key(request)
    api_key=request.headers.get("X-API-Key")
    check_rate_limit(api_key)
    
    data = payload.model_dump()

    row=create_run(data)

    return row
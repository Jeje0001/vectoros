from fastapi import APIRouter, HTTPException, Query
from src.core.db import list_run_summaries_from_db,get_run_by_run_id
from src.core.run_builder import build_full_run_structure
from datetime import datetime
runs_query_router = APIRouter()

MAX_LIMIT=100
@runs_query_router.get("/")
async def list_runs(
    limit: int = Query(20),
    cursor: str | None = None
):
    if limit <= 0:
        raise HTTPException(status_code=400, detail="limit must be greater than 0")

    if limit > MAX_LIMIT:
        raise HTTPException(
            status_code=400,
            detail=f"limit must not exceed {MAX_LIMIT}"
        )
    
    if cursor:
        try:
            datetime.fromisoformat(cursor.replace("Z", "+00:00"))
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="invalid cursor format, must be ISO timestamp"
            )

    try:
        result = list_run_summaries_from_db(limit=limit, cursor=cursor)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="failed to fetch runs"
    )
    items = []
    for row in result.get("items", []):
        summary = {
            "run_id": row.get("run_id"),
            "model": row.get("model"),
            "status": row.get("status"),
            "tokens": row.get("tokens"),
            "cost": row.get("cost"),
            "latency": row.get("latency"),
            "error": row.get("error"),
            "created_at": row.get("created_at"),
        }
        items.append(summary)
    count = len(items)

    if count == 0:
        return { "items": [], "next_cursor": None }

    last_created_at = items[-1].get("created_at")

    if count < limit:
        next_cursor = None
    else:
        if last_created_at is not None:
            next_cursor=last_created_at
                
        else:
            next_cursor=None

    return {
        "items": items,
        "next_cursor": next_cursor
        }

@runs_query_router.get("/{run_id}")
def get_run_by_id(run_id: str):
    if not isinstance(run_id, str) or run_id.strip() == "":
        raise HTTPException(status_code=400, detail="run_id must be a non-empty string")

    try:
        run = get_run_by_run_id(run_id)
    except Exception:
        raise HTTPException(status_code=500, detail="failed to fetch run")

    if run is None:
        raise HTTPException(status_code=404, detail="run not found")

    steps = run.get("steps")
    if not isinstance(steps, list):
        raise HTTPException(status_code=400, detail="run has invalid step structure")

    if len(steps) == 0:
        raise HTTPException(status_code=400, detail="run has no steps")

    try:
        full_run = build_full_run_structure(run)
    except Exception:
        raise HTTPException(status_code=500, detail="failed to build run structure")

    return full_run
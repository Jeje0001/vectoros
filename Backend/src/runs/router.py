from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_runs():
    return {"message": "runs endpoint working"}

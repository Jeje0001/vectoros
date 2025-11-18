import pathlib
from pydantic import BaseModel,Field
from typing import Optional, List, Dict, Any

# -------------------------
# Path to schema.sql
# -------------------------
BASE_DIR = pathlib.Path(__file__).resolve().parent
SCHEMA_PATH = BASE_DIR / "schema.sql"


# -------------------------
# Pydantic model
# -------------------------
class RunModel(BaseModel):
    model: str
    input: str
    output: Optional[str] = None
    tokens: Optional[int] = None
    cost: Optional[float] = None
    latency: Optional[float] = None
    status: str
    error: Optional[str] = None
    steps: Optional[List[Dict]] = Field(default_factory=list)

# -------------------------
# Helper to load SQL file
# -------------------------
def load_schema():
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"schema.sql not found at {SCHEMA_PATH}")
    return SCHEMA_PATH.read_text()

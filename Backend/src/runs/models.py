import pathlib
from pydantic import BaseModel,Field,field_validator,model_validator
from typing import Optional, List, Dict, Any
from uuid import UUID

# -------------------------
# Path to schema.sql
# -------------------------
BASE_DIR = pathlib.Path(__file__).resolve().parent
SCHEMA_PATH = BASE_DIR / "schema.sql"


# -------------------------
# Pydantic model
# -------------------------




class RunModel(BaseModel):
    run_id: Optional[UUID] = None
    model: str
    input: str
    output: Optional[str] = None
    tokens: Optional[int] = None
    cost: Optional[float] = None
    latency: Optional[float] = None
    status: str
    error: Optional[str] = None
    steps: List[Dict] = Field(default_factory=list)

    model_config = {
        "extra":"forbid"
    }

    @model_validator(mode="after")
    def validate_run(self):
        data=self.model_dump()

        if "created_at" in data:
            raise ValueError("created_at cannot be provided by client")
        if "started_at" in data:
            raise ValueError("started_at cannot be provided by client")
        
        if self.status == "error":
            if self.error is None or self.error.strip() == "":
                raise ValueError("error message required when status='error'")
        else:
            if self.error not in (None,""):
                raise ValueError("error must not be provided when status is not 'error'")
        
        return self
    
    @field_validator("status")
    def normalize_status(cls,v):
        status=str(v)

        status=status.lower()

        acceptable = {"success", "error", "running", "timeout"}

        if status in acceptable:
            return status
        else:
            raise ValueError("Invalid status. Must be one of: success, error, running, timeout")


    @field_validator("steps", mode="before")
    def normalize_steps(cls, v):
        print("VALIDATOR RAN WITH:", v)

        def normalize_step(step:dict):
            if isinstance(step,dict) == False:
                raise ValueError("Step is not a dictionary")
            
            steps=step.copy()
            if "type" not in steps:
                steps["type"]="unknown"
            
            if "metadata" not in steps:
                steps["metadata"]={}
            
            if "children" not in steps:
                steps["children"]=[]
            
            if isinstance(steps["metadata"],dict) == False:
                raise ValueError("Metadata is not a dictionary")
            
            if isinstance(steps["children"],list) == False:
                raise ValueError("Children is not a list")
            
            
            if isinstance(steps["type"],str) == False:
                steps["type"]= str(steps["type"])
            
            for child in steps["children"]:
                if not isinstance(child,dict):
                    raise ValueError("Each child must be a dictionary")
            
           
            return steps
            
            
            



        # Empty or null → []
        if v in (None, "", {}, []):
            return []
        
        
        if isinstance(v,dict):
            return [normalize_step(v)]
        elif isinstance(v,list):
            newv=[]
            for item in v:
                if not isinstance(item,dict):
                    raise ValueError("Not every item in v is a dictionary")
                
                newv.append(normalize_step(item))
            
            return newv
        else:
            raise ValueError("steps must be None, a dict, or a list of dicts")

            


      


# -------------------------
# Helper to load SQL file
# -------------------------
def load_schema():
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"schema.sql not found at {SCHEMA_PATH}")
    return SCHEMA_PATH.read_text()

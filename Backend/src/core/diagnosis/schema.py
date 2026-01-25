from pydantic import BaseModel, Field
from typing import Optional, List


class CostAnalysis(BaseModel):
    total_tokens: int = Field(..., description="Total tokens used in the run")
    estimated_cost_usd: Optional[float] = Field(
        None, description="Estimated USD cost for the run"
    )
    expensive_steps: List[str] = Field(
        default_factory=list,
        description="Step IDs or names that are unusually expensive"
    )


class DiagnosisResult(BaseModel):
    root_cause: str = Field(
        ..., description="Primary reason the run failed or underperformed"
    )
    explanation: str = Field(
        ..., description="Clear explanation of what happened and why"
    )
    suggested_fix: str = Field(
        ..., description="Concrete recommendation to fix or improve the run"
    )
    reliability_score: float = Field(
        ..., ge=0.0, le=1.0,
        description="Confidence score for this diagnosis"
    )
    cost_analysis: CostAnalysis

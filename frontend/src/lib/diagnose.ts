export interface CostAnalysis {
  total_tokens: number;
  estimated_cost_usd?: number;
  expensive_steps: string[];
}

export interface DiagnosisResult {
  root_cause: string;
  explanation: string;
  suggested_fix: string;
  reliability_score: number;
  cost_analysis: CostAnalysis;
}
def build_diagnosis_prompt(diagnosis: dict) -> str:
    return f"""
You are an expert AI systems debugger.

Given the following structured diagnosis, explain the issue clearly and concisely.
Do not invent facts. Do not speculate beyond the provided data.

Diagnosis data:
- Root cause: {diagnosis.get("root_cause")}
- Explanation: {diagnosis.get("explanation")}
- Reliability score: {diagnosis.get("reliability_score")}
- Cost analysis: {diagnosis.get("cost_analysis")}

Your response must include:
1. A short summary of what failed or degraded
2. Why it happened
3. A concrete recommended fix
"""

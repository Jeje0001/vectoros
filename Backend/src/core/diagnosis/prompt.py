
from src.memory.embeddings import generate_embedding
from src.memory.store import query_memory
def build_diagnosis_prompt(diagnosis: dict, run_input: str | None = None) -> str:
    memory_context = ""

    try:
        query_text = (
            diagnosis.get("root_cause")
            or diagnosis.get("explanation")
            or run_input
        )

        if query_text:
            embedding = generate_embedding(query_text)
            memories = query_memory(embedding, top_k=3)

            if memories:
                memory_context = "Relevant past incidents:\n"
                for m in memories:
                    memory_context += f"- {m['content']}\n"
    except Exception:
        memory_context = ""
    
    print("=== FINAL PROMPT SENT TO GPT ===")
    print(memory_context)
    

    return f"""
You are an expert AI systems debugger.

{memory_context}

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

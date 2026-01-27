from fastapi import APIRouter
from src.memory.embeddings import generate_embedding
from src.memory.store import add_memory

router = APIRouter(prefix="/memory", tags=["memory"])

@router.post("/add")
def add(payload: dict):
    content = payload.get("content")
    metadata = payload.get("metadata", {})

    if not content:
        return {"error": "content required"}

    embedding = generate_embedding(content)
    memory_id = add_memory(content, embedding, metadata)

    return {"memory_id": memory_id}


from src.memory.store import query_memory

@router.post("/query")
def query(payload: dict):
    query_text = payload.get("query")
    top_k = payload.get("top_k", 5)

    if not query_text:
        return {"error": "query required"}

    query_embedding = generate_embedding(query_text)
    results = query_memory(query_embedding, top_k)

    return {
        "results": results
    }
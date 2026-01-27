from typing import List, Dict
from uuid import uuid4
import math

MemoryItem = Dict[str, object]

_MEMORY: List[MemoryItem] = []


def add_memory(content: str, embedding: List[float], metadata: dict) -> str:
    memory_id = str(uuid4())

    _MEMORY.append({
        "id": memory_id,
        "content": content,
        "embedding": embedding,
        "metadata": metadata
    })

    return memory_id


def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)


def query_memory(query_embedding: List[float], top_k: int):
    scored = []

    for item in _MEMORY:
        score = cosine_similarity(query_embedding, item["embedding"])
        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    print("MEMORY SIZE AT QUERY:", len(_MEMORY))

    return [
        {
            "content": item["content"],
            "similarity": score,
            "metadata": item["metadata"]
        }
        for score, item in scored[:top_k]
    ]
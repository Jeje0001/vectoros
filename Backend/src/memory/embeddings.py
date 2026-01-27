from openai import OpenAI
from typing import List

client = OpenAI()

EMBEDDING_MODEL = "text-embedding-3-small"

def generate_embedding(text: str) -> List[float]:
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding
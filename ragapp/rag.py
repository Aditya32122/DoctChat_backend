from .embedding import get_embedding
from .qdrant_client import search_vectors
from google import genai
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def retrieve_similar_context(query: str, top_k: int = 5) -> list[str]:
    query_vector = get_embedding(query)
    results = search_vectors(query_vector, top_k=top_k)
    return [hit.payload.get("text", "") for hit in results]

def build_prompt(query: str, context_chunks: list[str]) -> str:
    context_text = "\n---\n".join(context_chunks)
    return f"""You are a helpful assistant. Use the following context to answer the query.

Context:
{context_text}

Query:
{query}

Answer:"""

def generate_answer(query: str) -> dict:
    context = retrieve_similar_context(query)
    prompt = build_prompt(query, context)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    return {
        "answer": text,
        "context": context,
        "raw_prompt": prompt,
    }

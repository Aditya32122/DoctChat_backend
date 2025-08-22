from google import genai
import os
from google.genai import types

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize client
client = genai.Client(api_key=GEMINI_API_KEY)

# Define embedding model
EMBED_MODEL = "models/embedding-001"

def get_embedding(text: str) -> list[float]:
    try:
        result = client.models.embed_content(
            model=EMBED_MODEL,
            contents=text,
            config=types.EmbedContentConfig(
                output_dimensionality=768  # or 1536, 3072 depending on your Qdrant config
            )
        )
        # ✅ Extract the first (and only) embedding vector
        return result.embeddings[0].values
    except Exception as e:
        print(f"Error generating embedding: {str(e)}")
        return []

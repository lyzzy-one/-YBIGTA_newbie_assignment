"""Vector retriever using Pinecone (cosine similarity)."""

import os

from dotenv import load_dotenv
from pinecone import Pinecone

from ingest.embedding import embed_query

load_dotenv()


def search(query: str, top_k: int = 10) -> list[dict]:
    query_vector = embed_query(query)

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX")
    index = pc.Index(index_name)

    response = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
    )

    results = []
    for match in response["matches"]:
        results.append({
            "id": match["id"],
            "text": match["metadata"]["text"],
            "score": match["score"],
            "method": "Vector",
        })

    return results
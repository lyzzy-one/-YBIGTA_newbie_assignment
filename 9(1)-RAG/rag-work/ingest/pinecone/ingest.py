"""Ingest embeddings into Pinecone vector index.

Batch upsert: 100 vectors per call.
Metadata: text truncated to 1000 chars (40KB limit).
"""

import json
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from pinecone import Pinecone
from tqdm import tqdm

load_dotenv()

RAW_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "processed"

BATCH_SIZE = 100
TEXT_LIMIT = 1000  # metadata text truncation


def ingest(progress_callback=None):
    embeddings = np.load(PROCESSED_DIR / "embeddings.npy")
    with open(PROCESSED_DIR / "embedding_ids.json") as f:
        ids = json.load(f)

    # id -> text 매핑 (metadata용)
    id_to_text = {}
    with open(RAW_DIR / "corpus.jsonl", encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)
            id_to_text[doc["id"]] = doc["text"]

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX")

    existing_indexes = [idx["name"] for idx in pc.list_indexes()]
    if index_name not in existing_indexes:
        from pinecone import ServerlessSpec
        pc.create_index(
            name=index_name,
            dimension=4096,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

    index = pc.Index(index_name)

    n = len(ids)
    total_upserted = 0

    for start in tqdm(range(0, n, BATCH_SIZE), desc="Pinecone upsert"):
        end = min(start + BATCH_SIZE, n)
        batch_ids = ids[start:end]
        batch_vectors = embeddings[start:end]

        vectors = []
        for doc_id, vector in zip(batch_ids, batch_vectors):
            text = id_to_text.get(doc_id, "")[:TEXT_LIMIT]
            vectors.append({
                "id": doc_id,
                "values": vector.tolist(),
                "metadata": {"text": text},
            })

        index.upsert(vectors=vectors)
        total_upserted += len(vectors)

        if progress_callback:
            progress_callback(total_upserted, n)

    print(f"Upserted {total_upserted} vectors into Pinecone index '{index_name}'")
    return total_upserted


if __name__ == "__main__":
    ingest()
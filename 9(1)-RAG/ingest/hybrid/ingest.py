"""Ingest corpus into Elasticsearch Hybrid index (wiki-hybrid).

Index mapping: text field + dense_vector(4096, cosine).
Bulk chunk_size=100 (heavier with 4096-dim vectors).
"""

import json
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from tqdm import tqdm

load_dotenv()

INDEX_NAME = "wiki-hybrid"
RAW_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "processed"

INDEX_MAPPINGS = {
    "properties": {
        "text": {"type": "text", "analyzer": "standard"},
        "embedding": {
            "type": "dense_vector",
            "dims": 4096,
            "index": True,
            "similarity": "cosine",
        },
    }
}


def get_es_client() -> Elasticsearch:
    return Elasticsearch(
        os.getenv("ELASTIC_ENDPOINT"),
        api_key=os.getenv("ELASTIC_API_KEY"),
        request_timeout=120,
    )


def _generate_actions(corpus_path: Path, embeddings: np.ndarray, ids: list[str]):
    id_to_idx = {doc_id: idx for idx, doc_id in enumerate(ids)}

    with open(corpus_path, encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)
            doc_id = doc["id"]
            idx = id_to_idx.get(doc_id)
            if idx is None:
                continue
            yield {
                "_index": INDEX_NAME,
                "_id": doc_id,
                "_source": {
                    "text": doc["text"],
                    "embedding": embeddings[idx].tolist(),
                },
            }


def ingest(progress_callback=None):
    embeddings = np.load(PROCESSED_DIR / "embeddings.npy")
    with open(PROCESSED_DIR / "embedding_ids.json") as f:
        ids = json.load(f)

    es = get_es_client()

    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)

    es.indices.create(index=INDEX_NAME, mappings=INDEX_MAPPINGS)

    corpus_path = RAW_DIR / "corpus.jsonl"
    actions = _generate_actions(corpus_path, embeddings, ids)

    success_count, errors = bulk(es, actions, chunk_size=100)

    es.indices.refresh(index=INDEX_NAME)

    if progress_callback:
        progress_callback(success_count)

    print(f"Indexed {success_count} documents into '{INDEX_NAME}'")
    return success_count


if __name__ == "__main__":
    ingest()

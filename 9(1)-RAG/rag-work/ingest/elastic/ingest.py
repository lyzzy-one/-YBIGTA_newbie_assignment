"""Ingest corpus into Elasticsearch BM25 index (wiki-bm25).

Index mapping: text field only (no vectors).
Bulk chunk_size=500 (lightweight without vectors).
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from tqdm import tqdm

load_dotenv()

INDEX_NAME = "wiki-bm25"
RAW_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"

INDEX_MAPPINGS = {
    "properties": {
        "text": {"type": "text", "analyzer": "standard"},
    }
}


def get_es_client() -> Elasticsearch:
    return Elasticsearch(
        os.getenv("ELASTIC_ENDPOINT"),
        api_key=os.getenv("ELASTIC_API_KEY"),
        request_timeout=60,
    )


def _generate_actions(corpus_path: Path):
    with open(corpus_path, encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)
            yield {
                "_index": INDEX_NAME,
                "_id": doc["id"],
                "_source": {
                    "text": doc["text"],
                },
            }


def ingest(progress_callback=None):
    es = get_es_client()

    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)

    es.indices.create(index=INDEX_NAME, mappings=INDEX_MAPPINGS)

    corpus_path = RAW_DIR / "corpus.jsonl"
    actions = _generate_actions(corpus_path)

    success_count, errors = bulk(es, actions, chunk_size=500)

    es.indices.refresh(index=INDEX_NAME)

    if progress_callback:
        progress_callback(success_count)

    print(f"Indexed {success_count} documents into '{INDEX_NAME}'")
    return success_count


if __name__ == "__main__":
    ingest()

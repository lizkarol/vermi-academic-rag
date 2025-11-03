import json
from scripts.utils.jsonl_utils import read_jsonl

def test_schema():
    data = read_jsonl("dataset/chunks_enriched/chunks_enriched_v1.0.jsonl")
    for item in data:
        assert "chunk_id" in item
        assert "source_field" in item

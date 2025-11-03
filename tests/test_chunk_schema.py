import json
import pytest
from scripts.utils.jsonl_utils import read_jsonl

# Campos obligatorios según la especificación técnica
MANDATORY_FIELDS = [
    "chunk_id", "source_field", "source_document", "source_type",
    "timestamp", "section", "category", "subcategory", "primary_entity",
    "entities", "keywords", "confidence_score", "reliability_level",
    "last_updated", "deprecated"
]

@pytest.fixture
def chunk_data():
    """Lee el archivo JSONL de chunks para las pruebas."""
    return read_jsonl("dataset/chunks_enriched/chunks_enriched_v1.0.jsonl")

def test_chunk_schema_is_list_of_dicts(chunk_data):
    """Verifica que el archivo JSONL se carga como una lista de diccionarios."""
    assert isinstance(chunk_data, list)
    assert all(isinstance(item, dict) for item in chunk_data)

def test_all_mandatory_fields_present(chunk_data):
    """Verifica que cada chunk contenga todos los campos obligatorios."""
    for i, chunk in enumerate(chunk_data):
        missing_fields = [field for field in MANDATORY_FIELDS if field not in chunk]
        assert not missing_fields, f"Chunk {i} (ID: {chunk.get('chunk_id', 'N/A')}) is missing fields: {missing_fields}"

def test_field_types(chunk_data):
    """Verifica que los campos clave tengan los tipos de datos correctos."""
    for chunk in chunk_data:
        assert isinstance(chunk["chunk_id"], str)
        assert isinstance(chunk["source_field"], str)
        assert isinstance(chunk["confidence_score"], float)
        assert isinstance(chunk["deprecated"], bool)
        assert isinstance(chunk["entities"], list)
        assert isinstance(chunk["keywords"], list)


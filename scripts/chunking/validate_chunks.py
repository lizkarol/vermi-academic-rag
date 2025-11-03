import argparse
import json
import sys

# Lista de campos obligatorios según la nueva especificación
MANDATORY_FIELDS = [
    "chunk_id", "source_field", "source_document", "source_type",
    "timestamp", "section", "category", "subcategory", "primary_entity",
    "entities", "keywords", "confidence_score", "reliability_level",
    "last_updated", "deprecated"
]

def validate_schema(data):
    """Valida que cada chunk en la lista cumpla con el esquema obligatorio."""
    print("Validating schema...")
    errors = 0
    for i, chunk in enumerate(data):
        missing_fields = [field for field in MANDATORY_FIELDS if field not in chunk]
        if missing_fields:
            print(f"Error: Chunk {i+1} (ID: {chunk.get('chunk_id', 'N/A')}) is missing fields: {', '.join(missing_fields)}")
            errors += 1
    
    if errors == 0:
        print("Schema validation passed successfully for all chunks.")
    else:
        print(f"\nSchema validation failed with {errors} errors.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Validate dataset chunks for VermiKhipu RAG.")
    parser.add_argument("--file", default="dataset/chunks_enriched/chunks_enriched_v1.0.jsonl", help="Path to the JSONL file to validate.")
    parser.add_argument("--mode", choices=["schema", "semantic", "coverage"], required=True, help="Validation mode.")
    parser.add_argument("--sample", type=float, default=1.0, help="Sample percentage for semantic validation (0.0 to 1.0).")
    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as f:
            data = [json.loads(line) for line in f]
    except FileNotFoundError:
        print(f"Error: File not found at {args.file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {args.file}: {e}")
        sys.exit(1)

    if args.mode == "schema":
        validate_schema(data)
    elif args.mode == "semantic":
        print(f"Performing semantic validation on {args.sample * 100}% of the data...")
        # Aquí iría la lógica de validación semántica (actualmente es un placeholder)
        print("Semantic validation (placeholder) finished.")
    elif args.mode == "coverage":
        print("Performing coverage analysis...")
        # Aquí iría la lógica de análisis de cobertura (actualmente es un placeholder)
        print("Coverage analysis (placeholder) finished.")

if __name__ == "__main__":
    main()


# Scripts de Chunking (Validación)

Herramientas para validar y gestionar chunks del dataset RAG.

## Herramientas Disponibles

### `validate_chunks.py`
Valida la estructura y calidad de los chunks.

**Uso:**
```bash
# Validar esquema (obligatorio antes de PR)
python scripts/chunking/validate_chunks.py \
  --file dataset/chunks_enriched/chunks_enriched_v1.0.jsonl \
  --mode schema

# Validar semántica (sample 20%)
python scripts/chunking/validate_chunks.py \
  --file tu_archivo.jsonl \
  --mode semantic \
  --sample 0.2

# Análisis de cobertura
python scripts/chunking/validate_chunks.py \
  --file tu_archivo.jsonl \
  --mode coverage
```

### `generate_cards_local.md`
Template de prompt para generar chunks con LLMs.

**Uso:**
1. Copia el contenido del template
2. Pega en tu LLM (Gemini, GPT-4, Claude)
3. Incluye el Markdown a procesar
4. El LLM genera chunks en formato JSONL

## Flujo de Trabajo

```
Markdown (local) → LLM manual (template) → chunks.jsonl → validate → PR
```

## Criterios de Calidad

- `confidence_score` ≥ 0.70
- Campos obligatorios completos
- Parafraseo (no copia verbatim)
- Atribución clara (`source_document`, `citations`)

# Métricas de Calidad del Dataset

Este documento define los criterios de calidad, validación y QA para el dataset de VermiKhipu.

## Criterios de QA por Categoría

### BIOLOGÍA
```
┌─────────────────┬──────────────────────┬───────────────┐
│ Aspecto         │ Validación           │ Umbral OK     │
├─────────────────┼──────────────────────┼───────────────┤
│ Especies        │ Eisenia fetida/andrei│ 100% mención  │
│ Rango Temp      │ Definido Min-Opt-Max │ 3 valores     │
│ Rango Humedad   │ % definido            │ Rango <40%   │
│ pH mín-máx      │ Diferencia ≤2 unid   │ 0.5-1.5 disp │
│ Comportamiento  │ Observable/verificable│ Descriptivo  │
└─────────────────┴──────────────────────┴───────────────┘
```

### PROCESO
```
┌──────────────┬──────────────────────┬───────────────┐
│ Parámetro    │ Validación           │ Umbral OK     │
├──────────────┼──────────────────────┼───────────────┤
│ C:N ratio    │ Rango mín-ópt-máx    │ Ej: 15-20-30 │
│ pH           │ Efecto acidificación │ Mitigación OK │
│ Humedad (%)  │ 40-80% / síntomas    │ Diferencia<5% │
│ Aireación    │ Método + frecuencia  │ Accionable    │
│ Temp (°C)    │ Rango + efecto       │ 15-25 óptimo  │
└──────────────┴──────────────────────┴───────────────┘
```

## Validación RAGAs: Umbrales por Métrica

```
┌─────────────────────────┬────────┬────────┬───────────────┐
│ Métrica                 │ MVP    │ Expansión│ Production  │
├─────────────────────────┼────────┼────────┼───────────────┤
│ Context Relevance       │ ≥75%   │ ≥80%   │ ≥85%         │
│ Context Recall          │ ≥70%   │ ≥80%   │ ≥85%         │
│ Context Precision       │ ≥70%   │ ≥75%   │ ≥80%         │
│ Faithfulness (answers)  │ ≥75%   │ ≥80%   │ ≥85%         │
│ Answer Relevancy        │ ≥75%   │ ≥80%   │ ≥85%         │
│ % Chunks deprecated     │ <10%   │ <5%    │ <3%          │
│ % Redundancia           │ <10%   │ <5%    │ <2%          │
│ Avg confidence_score    │ ≥0.75  │ ≥0.80  │ ≥0.85        │
└─────────────────────────┴────────┴────────┴───────────────┘
```

## Checklist de Validación Pre-Ingesta

```
□ Schema Pydantic/Arrow validado contra LanceDB
□ Campos obligatorios poblados (nunca NULL si obligatorio)
□ Tipos de dato coinciden con especificación (string, float, bool, enum)
□ chunk_id único per documento (no duplicados)
□ source_field limpio (sin HTML, acentos normalizados, <512 tokens)
□ confidence_score ≥0.70 (rechazar si <0.70)
□ category y subcategory en taxonomía validada
□ reliability_level coherente con source_type
□ entities y keywords sin duplicados, ordenadas relevancia
□ deprecated: false EXCEPTO migración de chunks antiguos
□ conflict_group_id documentado en tabla conflicts (si no NULL)
□ summary: 1-2 oraciones, refiere a primary_entity
□ timestamp y last_updated: ISO-8601, coherentes
□ source_document: rastreable (URL válida o DOI)
```

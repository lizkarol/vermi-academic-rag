# Schema y Descripción del Dataset

Este documento describe el esquema de datos para los chunks del dataset `vermi-academic-rag`.

## Tabla de Campos del Chunk

```
┌─────────────────────┬──────────┬──────────┬────────────────────────────────┐
│ Campo               │ Tipo     │ Obligat. │ Descripción Breve              │
├─────────────────────┼──────────┼──────────┼────────────────────────────────┤
│ chunk_id            │ string   │ ✓        │ ID único (verm_YYYYMM_NNN)    │
│ source_field        │ string   │ ✓        │ Texto limpio; 250-500 tokens  │
│ vector              │ float32  │ ✓        │ Embedding 300-dim auto-gen    │
│ source_document     │ string   │ ✓        │ Referencia bibliográfica      │
│ source_type         │ enum     │ ✓        │ libro|artículo|manual|exp.usr │
│ timestamp           │ ISO8601  │ ✓        │ Fecha de ingesta              │
│ section             │ string   │ ✓        │ Ubicación lógica en doc       │
│ category            │ enum     │ ✓        │ BIO|PROC|MAT|OPER|PROD        │
│ subcategory         │ string   │ ✓        │ Subcategoría específica       │
│ primary_entity      │ string   │ ✓        │ Entidad semántica principal   │
│ entities            │ string[] │ ✓        │ NER; max 10 entidades         │
│ keywords            │ string[] │ ✓        │ Palabras clave; max 8         │
│ confidence_score    │ float    │ ✓        │ [0-1]; recomendado ≥0.80     │
│ reliability_level   │ enum     │ ✓        │ verified|high|medium|low      │
│ last_updated        │ date     │ ✓        │ Última revisión               │
│ deprecated          │ bool     │ ✓        │ Marca si obsoleto             │
│ conflict_group_id   │ string   │ ✗        │ ID conflicto; NULL si sin conf│
│ summary             │ string   │ ✗        │ Resumen 1-2 oraciones         │
│ table_reference     │ string   │ ✗        │ ID imagen/tabla si aplica     │
│ citations           │ string[] │ ✗        │ DOI/URL referencias internas  │
│ evidence_strength   │ string   │ ✗        │ experimental|revisado|practico│
└─────────────────────┴──────────┴──────────┴────────────────────────────────┘
```

Para una descripción más detallada de cada campo y los valores permitidos, consulte el archivo `docs/DATA_SCHEMA.md`.


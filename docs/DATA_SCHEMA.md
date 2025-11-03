# Esquema de Datos del Dataset VermiKhipu RAG

Este documento detalla la estructura completa de un "chunk" de datos, optimizado para el sistema RAG de VermiKhipu.

## Tabla de Campos del Chunk

A continuación se presenta la tabla con todos los campos, su tipo, obligatoriedad y una breve descripción.

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

## Enumeraciones y Valores Válidos

### category (Obligatorio)
-   `BIO`: Biología de los organismos.
-   `PROC`: Proceso de vermicompostaje.
-   `MAT`: Materiales y insumos.
-   `OPER`: Operaciones y control del sistema.
-   `PROD`: Producto final (humus).

### source_type (Obligatorio)
-   `libro`: Libro o capítulo.
-   `artículo`: Artículo científico revisado.
-   `manual`: Manual técnico o estándar.
-   `experiencia_usuario`: Conocimiento práctico validado.
-   `estándar`: Norma o regulación oficial.

### reliability_level (Obligatorio)
-   `verified`: Revisado por pares, máxima confianza.
-   `high`: Fuente académica establecida.
-   `medium`: Experiencia de usuario validada o múltiples fuentes.
-   `low`: Observacional, evidencia limitada.

### evidence_strength (Opcional)
-   `experimental`: Resultado de estudios controlados.
-   `revisado`: Consenso de literatura validada.
-   `práctico`: Observación repetida en campo.
-   `teórico`: Deducción de principios conocidos.


# Prompt para generar chunks (BYOS-Safe)

Eres un experto en curation de vermicompostaje. 
Tu tarea es generar "cards" JSON para RAG, siguiendo un esquema estricto.

**INSTRUCCIONES CLAVE:**
1.  **Parafrasea** el contenido EN TUS PALABRAS (no copies párrafos largos).
2.  Extrae hechos, datos y definiciones clave.
3.  Si incluyes una cita textual, debe ser **BREVE** (<30 palabras) y estar entre comillas.
4.  Cada card debe ser autocontenido (250–500 tokens).
5.  Todos los campos marcados como obligatorios (✓) en el esquema deben estar presentes.

**CONTENIDO A PROCESAR:**
[Aquí: pega el .md privado convertido desde PDF]

**OUTPUT REQUERIDO (JSON array con objetos así):**
```json
{
  "chunk_id": "verm_YYYYMM_NNN",
  "source_field": "[250-500 tokens limpios del texto]",
  "vector": "[auto-generado por LanceDB]",
  "source_document": "[URL/DOI/referencia canónica]",
  "source_type": "[libro|artículo|manual|experiencia_usuario|estándar]",
  "timestamp": "2025-11-03T10:00:00Z",
  "section": "[ej: 2.3.1 Equilibrio C:N]",
  "category": "[BIO|PROC|MAT|OPER|PROD]",
  "subcategory": "[subcategoría específica]",
  "primary_entity": "[término principal]",
  "entities": ["ent1", "ent2", "ent3"],
  "keywords": ["kw1", "kw2", "kw3", "kw4"],
  "confidence_score": 0.85,
  "reliability_level": "high",
  "last_updated": "2025-11-03",
  "deprecated": false,
  "conflict_group_id": null,
  "summary": "[1-2 oraciones resumen semántico]",
  "table_reference": null,
  "citations": [],
  "evidence_strength": "revisado"
}
```

**EJEMPLO DE CHUNK (Bueno):**
```json
{
  "chunk_id": "verm_202511_001",
  "source_field": "La relación C:N en vermicompost debe mantenerse idealmente entre 18 y 25 para optimizar la actividad microbiana y la tasa de descomposición. Valores menores a 15 pueden acelerar la degradación pero corren el riesgo de generar un déficit de carbono para los microorganismos, mientras que valores superiores a 30 ralentizan significativamente el proceso debido a un exceso de carbono que limita la disponibilidad de nitrógeno.",
  "vector": null,
  "source_document": "doi:10.1016/j.wasman.2024.05.001",
  "source_type": "artículo",
  "timestamp": "2025-11-03T10:00:00Z",
  "section": "3.1. Parámetros Químicos",
  "category": "PROCESO",
  "subcategory": "equilibrio_nutricional",
  "primary_entity": "Relación C:N",
  "entities": ["Relación C:N", "actividad microbiana", "descomposición", "carbono", "nitrógeno"],
  "keywords": ["C:N", "balance", "18-25", "proceso"],
  "confidence_score": 0.95,
  "reliability_level": "verified",
  "last_updated": "2025-11-03",
  "deprecated": false,
  "conflict_group_id": "conf_002",
  "summary": "La relación C:N óptima para el vermicompostaje se sitúa entre 18 y 25; desviaciones de este rango afectan negativamente la velocidad del proceso.",
  "table_reference": null,
  "citations": ["doi:10.1016/j.wasman.2024.05.001"],
  "evidence_strength": "experimental"
}
```

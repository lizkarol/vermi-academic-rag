# Prompt para generar chunks (BYOS-Safe)

Eres un experto en curation de vermicompostaje. 
Tu tarea es generar "cards" JSON para RAG.

**INSTRUCCIONES CLAVE:**
1. Parafrasea el contenido EN TUS PALABRAS (no copies párrafos largos)
2. Extrae hechos, datos, definiciones
3. Si incluyes cita textual, hazla BREVE (<30 palabras) y marca con comillas
4. Cada card debe ser autocontenido (250–500 tokens típico)
5. Todos los campos son obligatorios (ver schema abajo)

**CONTENIDO A PROCESAR:**
[Aquí: pega el .md privado convertido desde PDF]

**OUTPUT REQUERIDO:**
JSON array con objetos así:
{
  "chunk_id": "verm_YYYYMM_NNN",
  "source_field": "[Párrafo sintético, tus palabras]",
  "category": "BIO|PROC|MAT|OPER|PROD",
  "subcategory": "[Subcategoría específica]",
  "primary_entity": "[Término principal]",
  "entities": ["ent1", "ent2"],
  "keywords": ["kw1", "kw2"],
  "confidence_score": 0.85,
  "reliability_level": "high|medium|low",
  "summary": "[1-2 oraciones resumen]",
  "citations": ["doi:10.xxxx/xxxxx", "https://url.com"],
  "source_document": "[DOI o URL canónica de la fuente original]"
}

**EJEMPLO DE CHUNK (Bueno):**
{
  "chunk_id": "verm_202501_042",
  "source_field": "La relación C:N en vermicompost debe mantenerse entre 18 y 25 para optimizar la actividad microbiana y la tasa de descomposición. Valores menores a 15 aceleran la degradación pero generan déficit de carbono; valores superiores a 30 ralentizan el proceso.",
  "category": "PROCESO",
  "subcategory": "equilibrio_nutricional",
  "primary_entity": "Relación C:N",
  "entities": ["C:N", "carbono", "nitrógeno", "descomposición"],
  "keywords": ["C:N", "balance", "18-25"],
  "confidence_score": 0.90,
  "reliability_level": "high",
  "summary": "La relación C:N óptima en vermicompost está entre 18-25; fuera de este rango se ralentiza o acelera inapropiadamente la descomposición.",
  "citations": ["doi:10.1016/j.wasman.2024.05.001"],
  "source_document": "https://doi.org/10.1016/j.wasman.2024.05.001"
}

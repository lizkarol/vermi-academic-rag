# Guía de Contribución

## Política BYOS (Bring Your Own Sources)

**Este repositorio NO aloja PDFs ni Markdown derivados de terceros.**

### Qué SÍ puedo aportar:
- 🆗 Chunks JSONL con síntesis **en tus palabras** (no copias verbatim)
- 🆗 Código Python (scripts, tests, ejemplos)
- 🆗 Documentación (guías, FAQs)
- 🆗 DOI/URLs de fuentes (sin los PDFs)

### Qué NO debo aportar:
- ❌ PDF o archivos de fuentes originales
- ❌ Markdown convertidos directamente desde PDFs sin parafrasear
- ❌ Fragmentos extensos (>100 palabras) verbatim de cualquier fuente
- ❌ Contenido sin cita o atribución

### Flujo recomendado para aportar chunks:

1. Obten tu fuente académica (local)
2. Parafrasea → genera chunks JSON en tus palabras
3. Aporta el JSON a través de Pull Request (solo `dataset/chunks_enriched/`)
4. En la descripción del PR, referencia DOI/URL de la fuente
5. CI validará automáticamente

### Licencia CC-BY:

Si la fuente tiene **CC-BY** o similar (p.ej., FAO desde 2024), indícalo explícitamente en el campo `license_note` o en comentarios del PR. Cualquier contenido CC-BY debe incluir **atribución clara**.

---

Más detalles en `BYOS_POLICY.md`.

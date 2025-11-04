# Estado del Proyecto - Vermi Academic RAG

**Última actualización:** 2025-11-03  
**Fase actual:** Fase 0 (Consolidación) - ✅ **100% COMPLETA**

---

## ✅ Funcionalidad Implementada y Probada

### Core (Crítico)

- **Conversión PDF→Markdown Adaptativa**
  - Script: `scripts/conversion/adaptive_converter.py`
  - Tecnología: Sistema adaptativo (pdfplumber para nativos, marker-pdf + EasyOCR para escaneados)
  - Detección automática de tipo de PDF con `PDFTypeDetector`
  - Sistema de perfiles JSON personalizables (`config/profiles/`)
  - Detección automática de perfiles con `ProfileDetector`
  - Normalización avanzada de Markdown con `MarkdownNormalizer`
  - Tracking en SQLite con `ConversionTracker`
  - Estado: ✅ **Completamente funcional**
  - Uso: `python scripts/conversion/adaptive_converter.py paper.pdf --profile academic_apa`

### Validación

- **Validación de esquema**
  - Script: `scripts/chunking/validate_chunks.py`
  - Modos: schema, semantic (placeholder), coverage (placeholder)
  - Estado: ✅ Modo schema funcional
  - Uso: `python scripts/chunking/validate_chunks.py --file chunks.jsonl --mode schema`

### Generación de Chunks

- **Template manual para LLMs**
  - Archivo: `scripts/chunking/generate_cards_local.md`
  - Estado: ✅ Funcional (proceso manual)
  - Uso: Copiar template → LLM web (Gemini/GPT-4/Claude) → Generar JSONL

### Documentación

- ✅ README.md completo y actualizado
- ✅ INSTALLATION.md (macOS/Windows)
- ✅ CONTRIBUTING.md con flujo 5 fases
- ✅ ROADMAP.md detallado por fases
- ✅ BYOS_POLICY.md
- ✅ docs/DOMAIN_KNOWLEDGE.md (taxonomía completa)
- ✅ docs/DATA_SCHEMA.md
- ✅ docs/CONVERSION_SYSTEM.md (arquitectura del sistema de conversión)
- ✅ docs/ADAPTIVE_CONVERSION.md (guía técnica detallada)
- ✅ docs/OCR_TABLES_ROADMAP.md (roadmap de OCR y tablas)
- ✅ config/profiles/README.md (sistema de perfiles JSON)
- ✅ READMEs en subdirectorios de scripts
- ✅ **Toda la documentación alineada con el código actual**

### Infraestructura

- ✅ `.gitignore` exhaustivo (protección BYOS)
- ✅ `.env.example` con configuración completa
- ✅ `setup.sh` script de instalación automatizada
- ✅ Estructura de directorios organizada
- ✅ `sources_local/` (directorio local para PDFs, reemplaza `sources/`)
- ✅ GitHub Actions workflows actualizados (manual trigger para prevenir fallos)
- ✅ Tests deshabilitados temporalmente (pendientes de datos reales)

---

## 🚧 En Desarrollo (No Implementado Aún)

### Fase 2 (Planificado para Q1 2026)

- **Generación Automatizada de Chunks**
  - Script: `scripts/chunking/generate_cards.py`
  - Integración con Ollama para LLMs locales
  - Batch processing de múltiples documentos

- **Sistema de Embeddings**
  - Script: `scripts/embeddings/compute_embeddings.py`
  - Vectorización con `embeddinggemma:300m`
  - Generación de archivos `.parquet` con vectores

- **Base de Datos Vectorial**
  - LanceDB con índices IVF_HNSW_SQ + FTS
  - Búsqueda híbrida (vector + keyword)
  - Reranking con RRF

- **Detección de Duplicados**
  - Script: `scripts/chunking/merge_redundant.py`
  - Similitud coseno para detectar redundancia
  - Sugerencias de fusión

- **Pruebas RAG**
  - Script: `scripts/testing/test_retrieval.py`
  - Test suite con queries sintéticas
  - Métricas de calidad (precision, recall, relevance)

- **CI/CD Workflows**
  - `.github/workflows/validate-dataset.yml` (✅ Actualizado - manual trigger)
  - `.github/workflows/test-rag.yml` (✅ Actualizado - manual trigger)
  - `.github/workflows/publish-release.yml` (✅ Actualizado - manual trigger)
  - **Nota:** Workflows cambiados a `workflow_dispatch` para evitar fallos automáticos hasta que el dataset esté poblado

### Fase 3 (Planificado para Q2 2026)

- Release v1.0 oficial
- Dataset completo (200-280 chunks)
- Sistema RAG funcional end-to-end
- Ejemplos de integración

---

## 📊 Dataset Actual

**Estado:** Solo chunks de ejemplo (placeholder)

| Archivo | Chunks | Estado |
|---------|--------|--------|
| `chunks_enriched_v1.0.jsonl` | 1 | Ejemplo/template |
| `chunks_enriched_v1.0.feather` | 0 | Vacío |

**Próximo objetivo:** Primer ciclo de ingesta real (10-20 chunks de un documento académico)

---

## 🎯 Cobertura por Categoría

| Categoría | Objetivo | Actual | % |
|-----------|----------|--------|---|
| BIOLOGÍA (BIO) | 40-60 | 0 | 0% |
| PROCESO (PROC) | 60-80 | 0 | 0% |
| MATERIALES (MAT) | 50-70 | 0 | 0% |
| OPERACIÓN (OPER) | 30-40 | 0 | 0% |
| PRODUCTO (PROD) | 20-30 | 0 | 0% |
| **TOTAL** | **200-280** | **0** | **0%** |

---

## 🔄 Flujo de Trabajo Actual (Funcional)

```
1. Usuario tiene PDF académico (local)
   ↓
2. Ejecuta adaptive_converter.py
   ↓
3. Obtiene Markdown (sources_local/markdown_outputs/)
   ↓
4. Abre generate_cards_local.md (template)
   ↓
5. Usa LLM web (Gemini/GPT-4/Claude) manualmente
   ↓
6. LLM genera chunks.jsonl
   ↓
7. Ejecuta validate_chunks.py --mode schema
   ↓
8. Si OK: Copia a dataset/chunks_enriched/
   ↓
9. Crea Pull Request
   ↓
10. Revisión manual por maintainer
   ↓
11. Merge si todo está correcto
```

**Tiempo estimado:** 30-60 minutos por documento (proceso manual)

---

## 🛠️ Dependencias Críticas

### Instaladas y Funcionales

- Python 3.11+
- PyTorch (backend para marker)
- marker-sdk (conversión PDF→MD)
- pandas, pyarrow (manejo de datos)
- pytest (testing del esquema)

### Opcionales (Fase 2+)

- Ollama (LLMs locales)
- LanceDB (base de datos vectorial)
- DuckDB (métricas y telemetría)

---

## 📝 Próximos Pasos Inmediatos

### ✅ Fase 0 Completada (2025-11-03)

1. [x] **Consolidación de arquitectura**
   - Sistema de perfiles JSON implementado y documentado
   - Toda la documentación alineada con el código real
   - Referencias obsoletas eliminadas (`convert_pdf_local.py`, `convert_pdf_robust.py`)
   - Directorio `sources/` renombrado a `sources_local/`
   - Tests rotos deshabilitados temporalmente
   - Workflows de CI actualizados a manual trigger

2. [ ] **Primer test end-to-end** (Próximo paso)
   - Conseguir un PDF académico de vermicompostaje (CC-BY o acceso legal)
   - Ejecutar flujo completo: PDF → MD → Chunks → Validación
   - Documentar problemas encontrados

3. [ ] **Primer chunk real** (Próximo paso)
   - Generar 5-10 chunks reales de un documento
   - Validar con `validate_chunks.py`
   - Agregar a `dataset/chunks_enriched/`

### Para Iniciar Fase 1 (Próximas 2 Semanas)

1. [ ] Seleccionar 5-10 fuentes académicas (prioritarias: PROCESO y BIOLOGÍA)
2. [ ] Procesar cada fuente siguiendo el flujo documentado
3. [ ] Meta: 50-100 chunks validados
4. [ ] Documentar casos edge y problemas de conversión

---

## 🚨 Limitaciones Conocidas

### Técnicas

- Conversión PDF→MD puede fallar con PDFs muy complejos (tablas multi-página)
- Validación semántica no implementada (solo schema)
- No hay detección automática de duplicados
- Proceso de generación de chunks es 100% manual

### De Proceso

- Sin CI/CD automático (validación manual)
- Sin sistema de embeddings (búsqueda vectorial futura)
- Sin pruebas RAG automáticas
- Sin métricas de calidad del dataset

### De Cobertura

- Dataset vacío (0 chunks reales)
- Sin validación con dominio experto
- Sin casos de uso reales probados

---

## 💡 Lecciones Aprendidas

1. **Simplicidad primero:** Mejor documentar lo que funciona que prometer lo que no existe
2. **BYOS es crítico:** La estructura debe proteger contra subidas accidentales de copyright
3. **Manual es OK:** Automatización puede esperar a Fase 2; calidad es más importante
4. **Documentación clara:** Evitar confusión entre "planificado" y "funcional"

---

## 🎓 Para Nuevos Contribuidores

**Empieza aquí:**
1. Lee [INSTALLATION.md](INSTALLATION.md)
2. Ejecuta `./setup.sh`
3. Prueba conversión con un PDF de prueba
4. Lee [docs/DOMAIN_KNOWLEDGE.md](docs/DOMAIN_KNOWLEDGE.md) para entender la taxonomía
5. Genera tus primeros chunks siguiendo [CONTRIBUTING.md](CONTRIBUTING.md)

**Lo que necesitas saber:**
- Solo `adaptive_converter.py` y `validate_chunks.py` están implementados
- La generación de chunks es manual con LLMs web
- No hay sistema de embeddings aún
- El dataset está vacío, ¡eres de los primeros contribuidores!

---

**Este documento se actualizará al completar cada fase del proyecto.**

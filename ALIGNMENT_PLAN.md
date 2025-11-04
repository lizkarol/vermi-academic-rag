# 📋 Plan de Trabajo: Alineación Docs con Realidad

**Fecha**: Noviembre 3, 2025  
**Objetivo**: Actualizar documentación para reflejar solo lo implementado, marcar pendientes claramente

---

## 🎯 Principios

1. **Solo documentar lo que funciona** ✅
2. **Marcar claramente lo pendiente** ⏳
3. **Usar `sources_local/` como estándar** (más claro que `sources/`)
4. **Tomar como referencia**: `docs/guide/` (documentación clara y práctica)

---

## 📦 FASE 1: Conversión de PDFs (LO QUE FUNCIONA)

### ✅ Implementado
- Sistema de conversión adaptativo (`adaptive_converter.py`)
- Detección automática de tipo PDF (NATIVE/SCANNED/MIXED)
- Sistema de perfiles JSON (`config/profiles/`)
- Tracking con SQLite (`conversion_tracker.db`)
- Normalización de Markdown
- Dashboard CLI

### 📝 Archivos a Actualizar

#### 1.1 Cambiar referencias de scripts legacy
**Archivos afectados**:
- [ ] `INSTALLATION.md` (líneas 105, 189, 263)
- [ ] `CONTRIBUTING.md` (línea 41)
- [ ] `PROJECT_STATUS.md` (línea 12)
- [ ] `ROADMAP.md` (línea 22)
- [ ] `scripts/README.md` (línea 27)
- [ ] `docs/WORKFLOW.md` (línea 20)
- [ ] `scripts/conversion/README.md` (línea 23)
- [ ] `sources/README.md` (línea 56)

**Cambio**: `convert_pdf_local.py` → `adaptive_converter.py`

#### 1.2 Estandarizar en `sources_local/`
**Archivos afectados**:
- [ ] `sources/README.md` → `sources_local/README.md`
- [ ] Todos los docs que mencionen `sources/`
- [ ] `.gitignore` (verificar que ignore `sources_local/`)

**Acción**: Usar refactor de VSCode para renombrar todas las referencias

#### 1.3 Actualizar `docs/CONVERSION_SYSTEM.md`
**Problema**: Menciona componentes que NO existen:
- `ConversionPlanner`
- `batch_convert.py`
- `ollama_prompts/`

**Acción**: 
- [ ] Documentar solo lo que existe: `adaptive_converter.py`, `conversion_db.py`, `profile_detector.py`
- [ ] Mover referencias inexistentes a sección "⏳ Pendiente"

#### 1.4 Alinear `docs/ADAPTIVE_CONVERSION.md` con implementación real
**Problema**: Dice que MIXED está implementado pero solo hay fallback
**Acción**:
- [ ] Actualizar tabla de estrategias:
  - NATIVE: ✅ Implementado
  - SCANNED: ✅ Implementado (marker-pdf + EasyOCR)
  - MIXED: ⏳ Pendiente (usa fallback a pdfplumber)

#### 1.5 Actualizar `docs/OCR_TABLES_ROADMAP.md`
**Problema**: Dice que `_convert_scanned()` está pendiente pero YA está implementado
**Acción**:
- [ ] Mover `_convert_scanned()` de ⏳ Pendiente a ✅ Implementado
- [ ] Mantener tablas escaneadas y MIXED como pendientes

---

## ⏳ FASE 2: Chunking y Embeddings (PENDIENTE - NO TOCAR AHORA)

### ❌ NO Implementado (marcar como pendiente en docs)

#### 2.1 Dataset y Chunks
**Problema**: Docs mencionan `dataset/chunks_enriched/chunks_enriched_v1.0.jsonl` que no existe

**Archivos afectados**:
- [ ] `docs/DOMAIN_KNOWLEDGE.md` (línea 341)
- [ ] `PROJECT_STATUS.md` (línea 100)
- [ ] `docs/WORKFLOW.md` (línea 31)
- [ ] `README.md` (línea 136)

**Acción**:
- [ ] Agregar nota: "⏳ Pendiente: Este archivo debe crearse localmente después de implementar el chunking"
- [ ] O crear sección "Flujo Futuro" para separar de "Flujo Actual"

#### 2.2 Tests Rotos
**Problema**: `tests/test_chunk_schema.py` importa módulos inexistentes

**Acción**:
- [ ] Agregar `pytest.skip` con mensaje: "Pendiente: requiere implementación de chunking"
- [ ] O comentar el test completo con nota explicativa
- [ ] NO implementar ahora - esperar a fase de chunking

#### 2.3 Scripts de Embeddings
**Problema**: `scripts/embeddings/` está vacío pero docs lo mencionan

**Acción**:
- [ ] Actualizar schema para hacer `embedding` opcional (agregar en docs)
- [ ] Marcar embeddings como ⏳ Pendiente en docs
- [ ] NO crear stubs - esperar a implementación real

---

## 🤖 FASE 3: GitHub Actions (SOLO FUNCIONALES)

### 3.1 Workflow de Validación
**Archivo**: `.github/workflows/validate-dataset.yml`

**Problema**: Referencias a scripts inexistentes:
- `scripts/validate_chunks.py` (existe en `scripts/chunking/validate_chunks.py`)
- `scripts/merge_redundant.py` (NO existe)

**Acción**:
- [ ] Actualizar path: `scripts/chunking/validate_chunks.py`
- [ ] Comentar/eliminar referencia a `merge_redundant.py`
- [ ] Agregar nota: workflow parcial hasta implementar chunking completo

### 3.2 Workflow de Release
**Archivo**: `.github/workflows/publish-release.yml`

**Problema**: Referencia `scripts/compute_embeddings.py` (NO existe)

**Acción**:
- [ ] Comentar/eliminar paso de embeddings
- [ ] Agregar nota: "Embeddings pendientes de implementación"

### 3.3 Pre-commit Hooks
**Problema**: `BYOS_POLICY.md` y `docs/FAQ.md` prometen hooks que no existen

**Acción**:
- [ ] Eliminar promesas de pre-commit hooks
- [ ] O agregar nota: "⏳ Pendiente: configuración de pre-commit"

---

## 🧹 FASE 4: Limpieza de Dependencias

### 4.1 `scripts/requirements.txt`
**Problema**: Deps instaladas pero no usadas:
- `lancedb`
- `sentence-transformers`
- `pandas` (tal vez usado?)
- `pyarrow`

**Acción**:
- [ ] Comentar deps no usadas con nota: "# Pendiente: para fase de embeddings"
- [ ] Verificar qué se usa realmente: `rg -n "import lancedb" scripts/`
- [ ] Mantener solo lo necesario para conversión PDF

---

## 📊 FASE 5: Documentación de Estado

### 5.1 Actualizar `PROJECT_STATUS.md`
**Acción**:
- [ ] Crear tabla clara:
  ```
  | Componente | Estado | Docs |
  |------------|--------|------|
  | Conversión PDF | ✅ | adaptive_converter.py |
  | Perfiles | ✅ | config/profiles/README.md |
  | Chunking | ⏳ | Pendiente |
  | Embeddings | ⏳ | Pendiente |
  | RAG | ⏳ | Pendiente |
  ```

### 5.2 Actualizar `README.md`
**Acción**:
- [ ] Sección "Quickstart" solo con pasos funcionales
- [ ] Mover pasos futuros a sección "Roadmap" o "Flujo Completo (Futuro)"
- [ ] Usar ejemplos reales con `adaptive_converter.py`

### 5.3 Crear/Actualizar `docs/TODO.md`
**Acción**:
- [ ] Listar claramente pendientes:
  - Chunking de Markdown
  - Generación de embeddings
  - Ingesta a LanceDB
  - Tests de integración
  - Workflows completos
  - Pre-commit hooks

---

## 🎯 ORDEN DE EJECUCIÓN

### Sprint 1: Docs Críticos (2-3 horas) ✅ COMPLETADO
1. ✅ Cambiar referencias `convert_pdf_local.py` → `adaptive_converter.py` (TODOS los archivos)
2. ✅ Refactor `sources/` → `sources_local/` (global)
3. ⏳ Actualizar `README.md` con flujo real (siguiente)
4. ⏳ Actualizar `docs/WORKFLOW.md` con pasos funcionales (siguiente)

### Sprint 2: Docs Técnicos (1-2 horas)
5. ✅ Actualizar `docs/CONVERSION_SYSTEM.md`
6. ✅ Actualizar `docs/ADAPTIVE_CONVERSION.md`
7. ✅ Actualizar `docs/OCR_TABLES_ROADMAP.md`
8. ✅ Actualizar `PROJECT_STATUS.md`

### Sprint 3: Workflows y Tests (1 hora)
9. ✅ Comentar tests pendientes
10. ✅ Actualizar workflows GitHub Actions
11. ✅ Limpiar `requirements.txt`

### Sprint 4: Limpieza Final (30 min)
12. ✅ Actualizar `docs/TODO.md` con pendientes claros
13. ✅ Verificar consistencia entre todos los docs
14. ✅ Commit y PR

---

## 📋 Checklist por Archivo

### Archivos de Instalación/Setup
- [ ] `INSTALLATION.md` - Cambiar scripts legacy
- [ ] `CONTRIBUTING.md` - Cambiar scripts legacy
- [ ] `scripts/requirements.txt` - Comentar deps no usadas

### READMEs
- [ ] `README.md` - Flujo real, remover pendientes
- [ ] `scripts/README.md` - Cambiar scripts legacy
- [ ] `scripts/conversion/README.md` - Cambiar scripts legacy
- [ ] `sources_local/README.md` - Renombrar y actualizar

### Documentación Técnica
- [ ] `docs/WORKFLOW.md` - Solo pasos funcionales
- [ ] `docs/CONVERSION_SYSTEM.md` - Remover componentes inexistentes
- [ ] `docs/ADAPTIVE_CONVERSION.md` - Alinear con código real
- [ ] `docs/OCR_TABLES_ROADMAP.md` - Mover SCANNED a implementado
- [ ] `docs/DOMAIN_KNOWLEDGE.md` - Marcar dataset como pendiente
- [ ] `docs/TODO.md` - Lista clara de pendientes
- [ ] `PROJECT_STATUS.md` - Tabla de estado real
- [ ] `ROADMAP.md` - Cambiar scripts legacy
- [ ] `BYOS_POLICY.md` - Remover promesas de hooks
- [ ] `docs/FAQ.md` - Remover promesas de hooks

### Tests
- [ ] `tests/test_chunk_schema.py` - Skip o comentar

### Workflows
- [ ] `.github/workflows/validate-dataset.yml` - Fix paths, comentar inexistentes
- [ ] `.github/workflows/publish-release.yml` - Comentar embeddings

### Refactor Global
- [ ] Todas las referencias: `sources/` → `sources_local/`
- [ ] Todas las referencias: scripts legacy → `adaptive_converter.py`

---

## 🚀 Comandos para Refactor

### 1. Renombrar directorio (si existe sources/)
```bash
# Si existe sources/ en el repo
git mv sources sources_local
```

### 2. Refactor global de referencias
```bash
# VSCode: Ctrl+Shift+H (Find & Replace in Files)
# Buscar: sources/
# Reemplazar: sources_local/
# Revisar cada match antes de aplicar
```

### 3. Actualizar scripts legacy
```bash
# Buscar: convert_pdf_local.py|convert_pdf_robust.py
# Reemplazar: adaptive_converter.py
```

---

## ✅ Criterios de Éxito

1. **Usuario nuevo puede seguir docs sin errores** ✅
2. **Solo se documenta lo implementado** ✅
3. **Pendientes claramente marcados como ⏳** ✅
4. **Tests pasan o están deshabilitados con razón** ✅
5. **Workflows no fallan por scripts faltantes** ✅
6. **README refleja experiencia real** ✅

---

## 📚 Referencias

- **Documentación de referencia**: `docs/guide/` (clara y práctica)
- **Estilo**: Concreto, ejemplos reales, sin promesas vacías
- **Formato**: Markdown limpio, emojis para estados (✅⏳❌)

---

**Próximo paso**: Ejecutar Sprint 1 (docs críticos)

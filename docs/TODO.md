# 📋 TODO - Pendientes de Implementación

**Última actualización**: Noviembre 3, 2025

Este documento lista las funcionalidades **pendientes de implementar**. Para estado actual del sistema, ver `README.md`.

---

## 🔴 ALTA PRIORIDAD

### 1. OCR Completo para PDFs Escaneados
**Estado**: ⏳ Pendiente  
**Estimación**: 8-12 horas  
**Requisitos**:
- marker-pdf==0.2.17
- easyocr==1.7.1
- GPU (CUDA o Apple Silicon MPS)

**Tareas**:
- [ ] Instalar dependencias OCR
- [ ] Implementar `_convert_scanned()` en adaptive_converter.py
- [ ] Descargar modelos OCR (~500MB)
- [ ] Crear fixtures de test (PDFs escaneados)
- [ ] Tests unitarios + integración
- [ ] Documentar uso y limitaciones
- [ ] Validar con 3-5 documentos reales

**Impacto**: Cubre 60-70% adicional de casos de uso (libros antiguos, tesis físicas)

**Referencias**: 
- Ver `docs/OCR_TABLES_ROADMAP.md` - Sección "SCANNED PDFs"
- Hardware disponible: Mac M4 con MPS ✅

---

### 2. Extracción de Tablas Escaneadas
**Estado**: ⏳ Pendiente  
**Estimación**: 6-10 horas  
**Requisitos**:
- table-transformer (Hugging Face)
- camelot-py==0.11.0

**Tareas**:
- [ ] Instalar table-transformer + camelot
- [ ] Implementar `_extract_tables()` multi-nivel
- [ ] Estrategia NATIVE (Camelot - texto seleccionable) ✅
- [ ] Estrategia SCANNED (table-transformer + OCR)
- [ ] Estrategia MIXED (combinada)
- [ ] Conversión a Markdown
- [ ] Manejo de celdas fusionadas
- [ ] Tests con tablas complejas

**Impacto**: Mejora fidelidad de documentos con tablas complejas

---

## 🟡 MEDIA PRIORIDAD

### 3. PDFs Mixtos (MIXED)
**Estado**: ⏳ Pendiente  
**Estimación**: 6-10 horas  
**Requisitos**:
- docling==2.9.1 (ya instalado ✅)

**Tareas**:
- [ ] Implementar `_convert_mixed()` con detección de zonas
- [ ] Aplicar pdfplumber a zonas con texto
- [ ] Aplicar OCR a zonas con imágenes
- [ ] Combinar resultados preservando orden
- [ ] Crear fixtures de test (PDFs mixtos)
- [ ] Tests unitarios + integración
- [ ] Documentar casos de uso

**Impacto**: Cubre tesis con capturas, papers con gráficos, manuales ilustrados

---

### 4. Extracción y OCR de Imágenes
**Estado**: ⏳ Pendiente  
**Estimación**: 4-6 horas

**Tareas**:
- [ ] Implementar `_extract_images()`
- [ ] Detección de captions ("Figura 1: ...")
- [ ] OCR selectivo de figuras con texto
- [ ] Guardar imágenes extraídas
- [ ] Referencias cruzadas ("ver Figura 3")
- [ ] Tests con documentos con figuras

**Impacto**: Mejora fidelidad de papers científicos con diagramas

---

### 5. Dashboard Web para Conversiones
**Estado**: ⏳ Pendiente  
**Estimación**: 8-12 horas

**Funcionalidades**:
- [ ] Interfaz web con Flask/FastAPI
- [ ] Upload de PDFs (drag & drop)
- [ ] Visualización de progreso en tiempo real
- [ ] Historial de conversiones con filtros
- [ ] Comparación lado a lado (PDF vs Markdown)
- [ ] Estadísticas y métricas
- [ ] Export de reportes

---

## 🟢 BAJA PRIORIDAD (Mejoras Futuras)

### 6. Optimización de Performance
**Tareas**:
- [ ] Caché de modelos OCR (no recargar cada vez)
- [ ] Procesamiento por lotes (múltiples PDFs)
- [ ] Procesamiento paralelo por página
- [ ] Compresión de modelos (quantización)
- [ ] Benchmarking detallado

### 7. Mejoras de Normalización
**Tareas**:
- [ ] Detección de fórmulas matemáticas (LaTeX)
- [ ] Preservación de formato de código
- [ ] Mejora de detección de listas anidadas
- [ ] Soporte para tablas multi-página
- [ ] Detección de footnotes/endnotes

### 8. Integración con APIs Externas
**Tareas**:
- [ ] Extracción de metadata de Crossref
- [ ] Detección de DOIs automática
- [ ] Enriquecimiento con datos de OpenAlex
- [ ] Detección de citas duplicadas

### 9. Soporte para Más Formatos
**Tareas**:
- [ ] Conversión de DOCX → Markdown
- [ ] Conversión de EPUB → Markdown
- [ ] Conversión de HTML → Markdown
- [ ] Importación desde Google Docs

### 10. Tests y Validación Avanzada
**Tareas**:
- [ ] Suite completa de tests E2E
- [ ] Tests de regresión con 50+ documentos
- [ ] Benchmarking automático en CI/CD
- [ ] Métricas de calidad automáticas (rouge, bleu)

---

## 📊 Métricas de Progreso

### Cobertura Actual
```
✅ NATIVE PDFs:     100% implementado
⏳ SCANNED PDFs:      0% implementado (~30-40% de casos de uso adicionales)
⏳ MIXED PDFs:        0% implementado (~20-30% de casos de uso adicionales)
```

### Cobertura Total Esperada
```
Con NATIVE solo:                 ~30-40% de todos los casos
Con NATIVE + SCANNED:            ~70-80% de todos los casos
Con NATIVE + SCANNED + MIXED:    ~90-95% de todos los casos
```

---

## 🎯 Roadmap Sugerido

### Sprint 1 (8-12h): OCR Básico
Implementar conversión de PDFs escaneados con marker-pdf + EasyOCR

### Sprint 2 (6-10h): Tablas Escaneadas
Extracción de tablas complejas con table-transformer

### Sprint 3 (6-10h): PDFs Mixtos
Soporte para documentos híbridos con docling

### Sprint 4 (4-6h): Imágenes
Extracción y OCR de figuras/diagramas

### Sprint 5 (8-12h): Dashboard
Interfaz web para gestión de conversiones

---

## 📚 Referencias

- **OCR Completo**: Ver `docs/OCR_TABLES_ROADMAP.md`
- **Sistema Actual**: Ver `README.md`
- **Arquitectura**: Ver `docs/ARCHITECTURE.md`
- **Perfiles**: Ver `config/profiles/README.md`

---

## 🔧 Hardware Recomendado

### Para implementar OCR (SCANNED)
```
Mínimo:
- GPU: NVIDIA RTX 3060 (6GB VRAM) o Apple M1+
- RAM: 16GB
- Storage: +2GB para modelos

Recomendado:
- GPU: NVIDIA RTX 3070+ (8GB+ VRAM) o Apple M3/M4
- RAM: 32GB
- Storage: +5GB para modelos y caché

Disponible:
✅ Mac M4 con Apple Silicon (MPS) - ÓPTIMO
```

---

## ✅ Cómo Contribuir

Si quieres trabajar en alguno de estos TODOs:

1. **Comenta en un issue** qué vas a implementar
2. **Crea una rama** `feature/nombre-funcionalidad`
3. **Implementa con tests**
4. **Documenta** en el archivo apropiado
5. **PR** cuando esté listo

---

**Mantenedor**: @lizkarol  
**Última revisión**: Noviembre 3, 2025

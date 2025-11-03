# Sistema Robusto de Conversión PDF → Markdown

Sistema completo de conversión con tracking, validación y fidelidad mejorada.

---

## 🎯 Características

- ✅ **Conversión con alta fidelidad** (marker-pdf + surya layout)
- ✅ **Extracción de tablas** (pdfplumber backup)
- ✅ **Validación con LLM local** (gemma3:12b via Ollama)
- ✅ **Cleanup OCR automático** (corrección de errores)
- ✅ **Tracking en base de datos** (SQLite para duplicados)
- ✅ **Detección de duplicados** (por SHA-256 hash)
- ✅ **Batch processing** (procesar directorios completos)
- ✅ **Reportes detallados** (JSON con métricas)

---

## 📁 Estructura

```
scripts/conversion/
├── convert_pdf_robust.py   # Conversor principal (robusto)
├── batch_convert.py         # Procesamiento batch
├── conversion_db.py         # Sistema de tracking SQLite
├── convert_pdf_local.py     # Versión simple (legacy)
└── README.md               # Esta guía
```

---

## 🚀 Uso Rápido

### Conversión Individual

```bash
# Conversión básica
python scripts/conversion/convert_pdf_robust.py paper.pdf

# Con OCR forzado (para PDFs escaneados)
python scripts/conversion/convert_pdf_robust.py scanned.pdf --force-ocr

# Sin validación Ollama
python scripts/conversion/convert_pdf_robust.py paper.pdf --no-ollama

# Forzar reconversión (ignorar duplicados)
python scripts/conversion/convert_pdf_robust.py paper.pdf --force
```

### Conversión Batch (Directorio Completo)

```bash
# Procesar todos los PDFs en un directorio
python scripts/conversion/batch_convert.py /path/to/pdfs/

# Con OCR forzado
python scripts/conversion/batch_convert.py /path/to/pdfs/ --force-ocr

# Sin skip de duplicados
python scripts/conversion/batch_convert.py /path/to/pdfs/ --no-skip
```

---

## 📊 Directorio `sources_local/`

El sistema usa una estructura local (ignorada por Git):

```
sources_local/
├── originals/         # PDFs originales copiados aquí
├── converted/         # Markdowns generados
├── metadata/          # Base de datos SQLite (conversion_tracker.db)
└── reports/           # Reportes JSON individuales
```

**⚠️ Importante:** Todo el contenido de `sources_local/` está en `.gitignore` (BYOS policy).

---

## 🔧 Configuración

### Prerequisitos

1. **Python 3.11+**
2. **Marker-pdf** instalado:
   ```bash
   pip install marker-pdf
   ```

3. **Ollama + gemma3:12b** (opcional pero recomendado):
   ```bash
   # Instalar Ollama: https://ollama.ai/
   ollama pull gemma3:12b
   ```

4. **Tesseract OCR** (para PDFs escaneados):
   ```bash
   # macOS
   brew install tesseract
   
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr
   ```

### Variables de Entorno

En `.env`:

```bash
# Ollama (opcional)
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=gemma3:12b

# Forzar OCR por defecto
FORCE_OCR=false

# Idiomas para OCR
PDF_LANG=en,es
```

---

## 📈 Sistema de Tracking

### Base de Datos SQLite

El sistema mantiene un registro de todas las conversiones en `sources_local/metadata/conversion_tracker.db`:

**Tablas:**
- `conversions`: Registro de cada PDF procesado
- `validation_reports`: Reportes de validación con gemma3
- `conversion_errors`: Errores encontrados

**Detección de Duplicados:**
- Calcula SHA-256 hash de cada PDF
- Evita reprocesar PDFs idénticos
- Usa `--force` para ignorar

### Consultar Estadísticas

```python
from conversion_db import ConversionTracker

with ConversionTracker() as tracker:
    stats = tracker.get_statistics()
    print(f"Total conversiones: {stats['total_conversions']}")
    print(f"Confianza promedio: {stats['average_confidence']}")
    print(f"PDFs con tablas: {stats['with_tables']}")
```

---

## 🧪 Validación con Gemma3:12b

El sistema usa gemma3:12b para:

1. **Validar fidelidad** (estructura, OCR, tablas)
2. **Limpiar errores OCR** (l→1, O→0, etc.)
3. **Calcular confidence score** (0-100)

**Prompt de validación:**
- Analiza estructura Markdown
- Detecta errores OCR
- Valida tablas
- Retorna JSON con métricas

**Sin Ollama:**
Si Ollama no está disponible, el sistema funciona sin validación LLM (solo conversión).

---

## 📝 Reportes

Cada conversión genera un reporte JSON en `sources_local/reports/`:

```json
{
  "pdf": "paper.pdf",
  "status": "success",
  "conversion_id": 42,
  "markdown_path": "sources_local/converted/paper.md",
  "steps": {
    "marker": "success",
    "pdfplumber_tables": 5,
    "validation": {
      "structure_ok": true,
      "ocr_quality": 95,
      "tables_ok": true,
      "confidence": 92,
      "notes": "Excellent conversion"
    },
    "cleanup": "skipped"
  },
  "total_time_seconds": 45.2
}
```

---

## 🔍 Flujo de Conversión

```
PDF Input
   ↓
1. Copiar a sources_local/originals/
   ↓
2. Verificar duplicado (SHA-256 hash)
   ↓
3. Registrar en DB (status: processing)
   ↓
4. Convertir con marker-pdf
   ↓
5. Extraer tablas con pdfplumber
   ↓
6. Validar con gemma3:12b (opcional)
   ↓
7. Cleanup OCR si confidence < 60
   ↓
8. Actualizar DB (status: success)
   ↓
9. Generar reporte JSON
   ↓
Markdown Output → sources_local/converted/
```

---

## ⚙️ Opciones Avanzadas

### Cambiar Modelo Ollama

```bash
python convert_pdf_robust.py paper.pdf \
  --ollama-model "llama3:8b"
```

### Cambiar URL Ollama

```bash
python convert_pdf_robust.py paper.pdf \
  --ollama-url "http://remote-server:11434"
```

### Procesar Batch con Configuración Custom

```bash
python batch_convert.py /pdfs/ \
  --force-ocr \
  --ollama-model "gemma3:12b" \
  --output "reports/custom_batch.json"
```

---

## 🐛 Troubleshooting

### Error: `marker_single command not found`

```bash
pip install marker-pdf
# O reinstalar:
pip uninstall marker-pdf && pip install marker-pdf --no-cache-dir
```

### Error: `Ollama no responde`

```bash
# Verificar Ollama está corriendo
ollama list

# Iniciar si no está corriendo
ollama serve
```

### Error: `pdfplumber no instalado`

```bash
pip install pdfplumber
```

### Conversión muy lenta

1. Reducir batch_multiplier en marker
2. Deshabilitar Ollama con `--no-ollama`
3. Procesar PDFs más pequeños

---

## 📚 Ejemplos Completos

### Ejemplo 1: Paper Académico Típico

```bash
# Paper en inglés, nativo (con texto embebido)
python scripts/conversion/convert_pdf_robust.py \
  research_paper_2024.pdf

# Output:
# sources_local/converted/research_paper_2024.md
# sources_local/reports/research_paper_2024_report.json
```

### Ejemplo 2: Tesis Escaneada

```bash
# PDF escaneado, OCR necesario
python scripts/conversion/convert_pdf_robust.py \
  old_thesis.pdf \
  --force-ocr

# Si confidence < 60, se ejecuta cleanup automáticamente
```

### Ejemplo 3: Batch de Documentos

```bash
# Directorio con 50 PDFs
python scripts/conversion/batch_convert.py \
  ~/Documents/vermi_papers/ \
  --force-ocr \
  --output reports/vermi_batch_2024.json

# Ver estadísticas
python -c "
from conversion_db import ConversionTracker
with ConversionTracker() as t:
    stats = t.get_statistics()
    print(stats)
"
```

---

## 🔄 Integración con Fase 1 (Chunking)

Una vez convertido a Markdown:

```bash
# 1. Conversión (aquí)
python convert_pdf_robust.py paper.pdf

# 2. Generación de chunks (manual con LLM)
# Usar sources_local/converted/paper.md
# con scripts/chunking/generate_cards_local.md

# 3. Validación
python scripts/chunking/validate_chunks.py \
  --file chunks.jsonl \
  --mode schema

# 4. Contribuir (solo JSONL al repo)
git add dataset/chunks_enriched/chunks_paper.jsonl
```

---

## 📖 Más Información

- **Marker-pdf**: https://github.com/VikParuchuri/marker
- **Ollama**: https://ollama.ai/
- **Gemma3**: https://ollama.ai/library/gemma3
- **PDFPlumber**: https://github.com/jsvine/pdfplumber

---

**Sistema listo para producción local. Fidelidad verificada. BYOS compliant.**

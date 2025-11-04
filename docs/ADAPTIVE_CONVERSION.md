# 📚 Sistema Adaptativo de Conversión PDF→Markdown

**Versión:** 2.0 (Noviembre 2025)  
**Basado en:** guia-instalacion.md + receta-pdf-markdown.md  
**Hardware:** macOS M4 (MPS), Ubuntu RTX 3070 (CUDA), Windows (CPU/CUDA)

---

## 🎯 Filosofía: "No Reinventar la Rueda"

Este sistema implementa una estrategia **adaptativa e inteligente** para conversión PDF→Markdown, seleccionando automáticamente las mejores herramientas según el tipo de PDF.

### Problema que Resuelve

**No todos los PDFs son iguales:**

1. **PDF Nativo** (texto seleccionable): Aplicar OCR completo sería desperdiciar 5-7 minutos de GPU cuando pdfplumber lo hace en 5 segundos.

2. **PDF Escaneado** (imagen pura): Intentar extraer texto con pdfplumber daría basura; se necesita OCR con GPU.

3. **PDF Mixto** (texto + imágenes no copiables): Requiere detección inteligente para aplicar OCR solo donde es necesario.

### Solución: Detección Automática + Estrategia Adaptativa

```
┌─────────────┐
│   PDF.pdf   │
└──────┬──────┘
       ▼
┌──────────────────────┐
│  PDFTypeDetector     │ ← Analiza primeras 3-10 páginas (< 1s)
│  (pdfplumber ligero) │
└──────┬───────────────┘
       ▼
   ¿Qué tipo?
       │
   ┌───┴───┬─────────┬─────────┐
   │       │         │         │
NATIVE  SCANNED   MIXED    UNKNOWN
   │       │         │         │
   ▼       ▼         ▼         ▼
pdfplumber marker-pdf docling  fallback
(5-10s)   (5-7min)  (30-60s)  (manual)
```

---

## 🛠️ Stack Tecnológico

### Core Dependencies (Versiones Testeadas)

| Herramienta | Versión | Propósito | Performance |
|------------|---------|-----------|------------|
| **pdfplumber** | 0.11.4 | PDFs nativos | ~5-10s/50pág |
| **marker-pdf** | ≥1.0.0 | PDFs escaneados | ~5-7min GPU |
| **docling** | ≥2.18.0 | PDFs mixtos | **(Pendiente)** ~30-60s |
| **EasyOCR** | 1.7.1 | OCR backend | Con marker |
| **PyTorch** | 2.5.1 | GPU (CUDA/MPS) | Crítico |

### Hardware Soportado

**macOS M4 (MPS):**
```bash
pip install torch==2.5.1 torchvision==0.20.1
```
- RAM: 16GB | Performance: ~6-7 min/50pág | Workers: 2

**Ubuntu RTX 3070 (CUDA 12.1):**
```bash
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121
```
- VRAM: 8GB | Performance: ~4-5 min/50pág | Workers: 4

**Windows CPU/CUDA:**
```bash
# CPU
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu
# CUDA (si tienes GPU)
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121
```

---

## 📊 Detección de Tipo de PDF

### PDFTypeDetector

Clasifica PDFs analizando densidad de texto extraíble.

**Uso:**
```python
from pdf_type_detector import PDFTypeDetector

detector = PDFTypeDetector()
pdf_type, stats = detector.detect("paper.pdf", quick=True)

print(f"Tipo: {pdf_type.value}")
print(f"Estrategia: {stats['recommended_strategy']}")
```

**CLI:**
```bash
python scripts/conversion/pdf_type_detector.py paper.pdf
```

**Output:**
```
📊 ANÁLISIS DE TIPO DE PDF
============================================================
Archivo: paper.pdf
Tipo: NATIVE
Páginas totales: 58
Páginas analizadas: 10
Páginas con texto: 10
Páginas vacías: 0
Ratio texto: 100.0%
Estrategia: pdfplumber (rápido, alta fidelidad)
============================================================
```

---

## 🔄 Conversión Adaptativa

### AdaptivePDFConverter

**Uso Básico:**
```python
from adaptive_converter import AdaptivePDFConverter

converter = AdaptivePDFConverter(sources_dir="sources")
result = converter.convert_single("paper.pdf")

if result["success"]:
    print(f"✅ Markdown: {result['markdown_path']}")
```

**CLI:**
```bash
# Conversión automática
python scripts/conversion/adaptive_converter.py paper.pdf

# Con validación Ollama
python scripts/conversion/adaptive_converter.py paper.pdf --ollama

# Forzar estrategia
python scripts/conversion/adaptive_converter.py paper.pdf --strategy scanned
```

---

## 📋 Estrategias de Conversión

### 1. NATIVE: PDFs con Texto Seleccionable

**Herramienta:** pdfplumber  
**Performance:** 5-10 segundos para 50 páginas  
**Uso:**
```python
# Automático si PDFTypeDetector detecta NATIVE
markdown, metadata = converter._convert_native(pdf_path, conversion_id)
```

**Características:**
- Extracción directa de texto embebido
- Tablas automáticas con pdfplumber
- Sin OCR (rápido y preciso)

### 2. SCANNED: PDFs Escaneados (Imagen)

**Herramienta:** marker-pdf + EasyOCR + GPU  
**Performance:** 5-7 minutos con GPU para 50 páginas  
**Uso:**
```python
# Automático si PDFTypeDetector detecta SCANNED
markdown, metadata = converter._convert_scanned(pdf_path, conversion_id)
```

**Características:**
- OCR con modelos Surya (marker-pdf)
- EasyOCR como backend
- Requiere GPU para performance aceptable
- Cleanup automático con gemma3:12b (opcional)

### 3. MIXED: PDFs Híbridos (Pendiente)

**Herramienta:** `docling` (con fallback a `pdfplumber`)  
**Performance:** 30-60 segundos para 50 páginas (estimado)  
**Uso:**
```python
# Automático si PDFTypeDetector detecta MIXED
# Actualmente usa el fallback a _convert_native
markdown, metadata = converter._convert_mixed(pdf_path, conversion_id)
```

**Características:**
- Detección inteligente de regiones
- OCR solo donde es necesario
- **Actualmente, esta estrategia no está implementada y el sistema utiliza `_convert_native` como fallback.**

---

## 💾 Sistema de Tracking

### ConversionTracker (SQLite)

Tracking automático con detección de duplicados por SHA-256.

**Uso:**
```python
from conversion_db import ConversionTracker

with ConversionTracker() as tracker:
    # Verificar duplicado
    is_dup, existing_id = tracker.is_duplicate(pdf_path)
    
    # Registrar conversión
    conv_id = tracker.add_conversion(pdf_path, status="processing")
    
    # Actualizar estado
    tracker.update_conversion(conv_id, status="success", pages=58)
    
    # Estadísticas
    stats = tracker.get_statistics()
    print(f"Total conversiones: {stats['total_conversions']}")
```

**Base de datos:** `sources_local/metadata/conversion_tracker.db`

**Tablas:**
- `conversions`: Registro de cada PDF procesado
- `validation_reports`: Reportes de validación con gemma3
- `conversion_errors`: Errores encontrados

---

## 🤖 Validación con Ollama (Opcional)

### gemma3:12b Local

**Instalación:**
```bash
# Instalar Ollama desde https://ollama.ai
ollama pull gemma3:12b
```

**Uso:**
```bash
# Activar validación
python scripts/conversion/adaptive_converter.py paper.pdf --ollama
```

**Qué hace gemma3:12b:**
1. Valida estructura Markdown (títulos, listas, tablas)
2. Detecta errores OCR (l→1, O→0, rn→m)
3. Calcula confidence score (0-100)
4. Limpia errores si confidence < 60

**Ejemplo de validación:**
```json
{
  "structure_ok": true,
  "ocr_quality": 95,
  "tables_ok": true,
  "confidence": 92,
  "notes": "Excellent conversion, minor spacing in one table"
}
```

---

## 📁 Estructura de Directorios

```
vermi-academic-rag/
├── sources_local/                    # Local only (ignorado por Git)
│   ├── originals/             # PDFs originales
│   ├── converted/             # Markdowns generados
│   ├── metadata/              # conversion_tracker.db
│   └── reports/               # Reportes JSON (si usa --ollama)
├── data/                       # Datos procesados
│   ├── raw/                   # PDFs backup
│   ├── processed/             # Chunks procesados
│   ├── embeddings/            # Cache de embeddings
│   ├── metadata/              # Perfiles de conversión
│   └── validation/            # Reportes de validación
├── config/
│   └── profiles/              # Perfiles de conversión personalizados
├── scripts/
│   └── conversion/
│       ├── adaptive_converter.py      # Conversor principal
│       ├── pdf_type_detector.py       # Detector de tipo
│       ├── conversion_db.py           # Sistema de tracking
│       ├── conversion_profiles.py     # Sistema de perfiles
│       └── requirements.txt           # Dependencias
└── docs/
    └── ADAPTIVE_CONVERSION.md         # Esta guía
```

**⚠️ Importante:** Todo `sources_local/` está en `.gitignore` (BYOS policy).

---

## 🚀 Quickstart

### 1. Instalación Automática

```bash
# Clonar repositorio
git clone https://github.com/lizkarol/vermi-academic-rag.git
cd vermi-academic-rag

# Setup automático (detecta plataforma)
./setup.sh
```

### 2. Conversión Básica

```bash
# Activar entorno
source .venv/bin/activate

# Detectar tipo de PDF
python scripts/conversion/pdf_type_detector.py paper.pdf

# Convertir automáticamente
python scripts/conversion/adaptive_converter.py paper.pdf
```

### 3. Verificar Output

```bash
# Ver Markdown generado
cat sources_local/converted/paper.md

# Ver estadísticas
python -c "
from scripts.conversion.conversion_db import ConversionTracker
with ConversionTracker() as t:
    stats = t.get_statistics()
    print(f'Total: {stats[\"total_conversions\"]}')
    print(f'Confidence promedio: {stats[\"average_confidence\"]}')
"
```

---

## 📊 Benchmarks

### Resultados Reales (ont66t-Valdivia-Ayaca-Cuela-Rojas.pdf)

**Hardware:** Mac M4 (MPS)  
**PDF:** 58 páginas, NATIVE (100% texto)  
**Resultado:**
- Detección: < 1 segundo
- Conversión: 1.6 segundos
- Páginas procesadas: 58
- Tablas extraídas: 8
- Estrategia: pdfplumber

**Performance vs. Sistema Anterior:**
- Sistema viejo (marker-pdf para todo): ~5-7 minutos
- Sistema adaptativo (pdfplumber): 1.6 segundos
- **Ganancia: 200x más rápido** 🚀

---

## 🔧 Opciones Avanzadas

### CLI Completo

```bash
python scripts/conversion/adaptive_converter.py <pdf> [opciones]

Opciones:
  --force              Forzar reconversión (ignorar duplicados)
  --ollama             Activar validación con gemma3:12b
  --strategy TIPO      Forzar estrategia (native/scanned/mixed)
  --sources-dir DIR    Directorio sources custom
  --profile NOMBRE     Usar perfil de conversión personalizado
  --help               Mostrar ayuda completa
```

### Python API

```python
from adaptive_converter import AdaptivePDFConverter

# Configuración avanzada
converter = AdaptivePDFConverter(
    sources_dir="sources",
    use_ollama=True,
    ollama_url="http://localhost:11434",
    ollama_model="gemma3:12b",
    force_strategy="native"  # Forzar estrategia
)

# Conversión con opciones
result = converter.convert_single(
    pdf_path="paper.pdf",
    force=True,         # Ignorar duplicados
    quick_detect=True   # Solo analizar 3 páginas
)

# Resultado
print(f"Success: {result['success']}")
print(f"Tipo: {result['pdf_type']}")
print(f"Estrategia: {result['strategy']}")
print(f"Markdown: {result['markdown_path']}")
print(f"Tiempo: {result['elapsed_time']:.1f}s")
```

---

## 🐛 Troubleshooting

### Error: marker-pdf no encontrado

```bash
pip install marker-pdf>=1.0.0
```

### Error: Ollama connection refused

```bash
# Verificar Ollama está corriendo
ollama list

# Si no, iniciar:
ollama serve

# En otra terminal:
ollama pull gemma3:12b
```

### Conversión muy lenta

1. Verificar tipo de PDF (puede estar usando marker-pdf innecesariamente)
2. Deshabilitar Ollama: `--no-ollama` (ahorra 10-30s)
3. Usar `--strategy native` si sabes que tiene texto

### PDF detectado incorrectamente

```bash
# Forzar estrategia manualmente
python scripts/conversion/adaptive_converter.py paper.pdf --strategy native
```

---

## 📖 Documentación Adicional

- **Guía de instalación completa:** `docs/guide/guia-instalacion.md`
- **Receta funcional PDF→MD:** `docs/guide/receta-pdf-markdown.md`
- **README principal:** `README.md`
- **Esquema de datos RAG:** `docs/DATA_SCHEMA.md`

---

## 🎓 Próximos Pasos

1. **Convertir tu primer PDF:**
   ```bash
   python scripts/conversion/adaptive_converter.py tu_paper.pdf
   ```

2. **Generar chunks parafraseados** (Fase 1):
   - Usar Markdown + `scripts/chunking/generate_cards_local.md`
   - LLM manual (Gemini, GPT-4, Claude)

3. **Validar chunks:**
   ```bash
   python scripts/chunking/validate_chunks.py --file chunks.jsonl --mode schema
   ```

4. **Contribuir al dataset:**
   ```bash
   cp chunks.jsonl dataset/chunks_enriched/
   git add dataset/chunks_enriched/chunks.jsonl
   git commit -m "feat: Add chunks from [paper name]"
   ```

---

**Sistema adaptativo operacional. Listo para conversión a escala. BYOS compliant. 🚀**

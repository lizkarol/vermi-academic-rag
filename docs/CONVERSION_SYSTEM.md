# 📚 Sistema Adaptativo de Conversión PDF→Markdown# 📚 Sistema Adaptativo de Conversión PDF→Markdown# 📚 Sistema Adaptativo de Conversión PDF→Markdown# Guía Rápida: Sistema Robusto de Conversión PDF→MD



**Versión:** 2.0 (Noviembre 2025)  

**Basado en:** guia-instalacion.md + receta-pdf-markdown.md  

**Hardware:** macOS M4 (MPS), Ubuntu RTX 3070 (CUDA), Windows (CPU/CUDA)**Versión:** 2.0 (Noviembre 2025)  



---**Basado en:** guia-instalacion.md + receta-pdf-markdown.md  



## 🎯 Filosofía: "No Reinventar la Rueda"**Hardware:** macOS M4 (MPS), Ubuntu RTX 3070 (CUDA), Windows (CPU/CUDA)**Versión:** 2.0 (Noviembre 2025)  **Versión:** Fase 0 - Sistema Robusto Completo  



Este sistema implementa una estrategia **adaptativa e inteligente** para conversión PDF→Markdown, seleccionando automáticamente las mejores herramientas según el tipo de PDF.



### Problema que Resuelve---**Basado en:** guia-instalacion.md + receta-pdf-markdown.md  **Fecha:** Noviembre 2025



**No todos los PDFs son iguales:**



1. **PDF Nativo** (texto seleccionable): Aplicar OCR completo sería desperdiciar 5-7 minutos de GPU cuando pdfplumber lo hace en 5 segundos.## 🎯 Filosofía: "No Reinventar la Rueda"**Hardware:** RTX 3070 (CUDA 12.1) + Mac M4 (MPS)



2. **PDF Escaneado** (imagen pura): Intentar extraer texto con pdfplumber daría basura; se necesita OCR con GPU.



3. **PDF Mixto** (texto + imágenes no copiables): Requiere detección inteligente para aplicar OCR solo donde es necesario.Este sistema implementa una estrategia **adaptativa e inteligente** para conversión PDF→Markdown, seleccionando automáticamente las mejores herramientas según el tipo de PDF.---



### Solución: Detección Automática + Estrategia Adaptativa



```### Problema que Resuelve---

┌─────────────┐

│   PDF.pdf   │

└──────┬──────┘

       │**No todos los PDFs son iguales:**## 🎯 Qué hay de nuevo

       ▼

┌──────────────────────┐

│  PDFTypeDetector     │ ← Analiza primeras 3-10 páginas (< 1s)

│  (pdfplumber ligero) │1. **PDF Nativo** (texto seleccionable): Aplicar OCR completo sería desperdiciar 5-7 minutos de GPU cuando pdfplumber lo hace en 5 segundos.## 🎯 Filosofía: "No Reinventar la Rueda"

└──────┬───────────────┘

       │

   ¿Qué tipo?

       │2. **PDF Escaneado** (imagen pura): Intentar extraer texto con pdfplumber daría basura; se necesita OCR con GPU.### Sistema anterior (simple):

   ┌───┴───┬─────────┬─────────┐

   │       │         │         │

NATIVE  SCANNED   MIXED    UNKNOWN

   │       │         │         │3. **PDF Mixto** (texto + imágenes no copiables): Requiere detección inteligente para aplicar OCR solo donde es necesario.Este sistema implementa una estrategia **adaptativa e inteligente** para conversión PDF→Markdown, seleccionando automáticamente las mejores herramientas según el tipo de PDF.- Script básico `convert_pdf_local.py`

   ▼       ▼         ▼         ▼

pdfplumber marker-pdf docling  fallback

(5-10s)   (5-7min)  (30-60s)  (manual)

```### Solución: Detección Automática + Estrategia Adaptativa- Sin tracking de conversiones



---



## 🛠️ Stack Tecnológico```### Problema que Resuelve- Sin detección de duplicados



### Core Dependencies (Versiones Testeadas)┌─────────────┐



| Herramienta | Versión | Propósito | Performance |│   PDF.pdf   │- Sin validación automática

|------------|---------|-----------|------------|

| **pdfplumber** | 0.11.4 | PDFs nativos | ~5-10s/50pág |└──────┬──────┘

| **marker-pdf** | ≥1.0.0 | PDFs escaneados | ~5-7min GPU |

| **docling** | ≥2.18.0 | PDFs mixtos | ~30-60s |       ▼**No todos los PDFs son iguales:**

| **EasyOCR** | 1.7.1 | OCR backend | Con marker |

| **PyTorch** | 2.5.1 | GPU (CUDA/MPS) | Crítico |┌──────────────────────┐



### Hardware Soportado│  PDFTypeDetector     │ ← Analiza primeras 3-10 páginas (< 1s)### Sistema nuevo (robusto):



**macOS M4 (MPS):**│  (pdfplumber ligero) │

```bash

pip install torch==2.5.1 torchvision==0.20.1└──────┬───────────────┘1. **PDF Nativo** (texto seleccionable): Aplicar OCR completo sería desperdiciar 5-7 minutos de GPU cuando pdfplumber lo hace en 5 segundos.- ✅ **Tracking completo** con base de datos SQLite

```

       ▼

**Ubuntu RTX 3070 (CUDA 12.1):**

```bash   ¿Qué tipo?- ✅ **Detección de duplicados** por hash SHA-256

pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121

```       │



**Windows CPU/CUDA:**   ┌───┴───┬─────────┬─────────┐2. **PDF Escaneado** (imagen pura): Intentar extraer texto con pdfplumber daría basura; se necesita OCR con GPU.- ✅ **Validación con LLM** (gemma3:12b via Ollama)

- CPU: `--index-url https://download.pytorch.org/whl/cpu`

- CUDA: `--index-url https://download.pytorch.org/whl/cu121`   │       │         │         │



---NATIVE  SCANNED   MIXED    UNKNOWN- ✅ **Cleanup OCR automático**



## 🚀 Instalación Rápida   ▼       ▼         ▼         ▼



### Opción 1: Setup Automático (Recomendado)pdfplumber marker-pdf docling  fallback3. **PDF Mixto** (texto + imágenes no copiables): Requiere detección inteligente para aplicar OCR solo donde es necesario.- ✅ **Batch processing** para directorios completos



```bash(5-10s)   (5-7min)  (30-60s)  (manual)

./setup.sh

``````- ✅ **Reportes detallados** en JSON



Esto hace:

1. Detecta tu plataforma (macOS/Ubuntu/Windows)

2. Verifica Python 3.11+---### Solución: Detección Automática + Estrategia Adaptativa- ✅ **Estructura `sources_local/`** con .gitkeep

3. Crea virtual environment

4. Instala PyTorch según hardware (MPS/CUDA/CPU)

5. Instala dependencias del proyecto

6. Valida instalación## 🛠️ Stack Tecnológico



### Opción 2: Setup Manual



```bash### Core Dependencies (Versiones Testeadas)```---

# 1. Crear venv

python3.11 -m venv .venv

source .venv/bin/activate  # macOS/Linux

# .venv\Scripts\activate  # Windows| Herramienta | Versión | Propósito | Performance |┌─────────────┐



# 2. Instalar NumPy primero|------------|---------|-----------|------------|

pip install "numpy>=1.26.4,<2.0.0"

| **pdfplumber** | 0.11.4 | PDFs nativos | ~5-10s/50pág |│   PDF.pdf   │## 🚀 Instalación Rápida

# 3. Instalar PyTorch (macOS M4 ejemplo)

pip install torch==2.5.1 torchvision==0.20.1| **marker-pdf** | ≥1.0.0 | PDFs escaneados | ~5-7min GPU |



# 4. Instalar resto de dependencias| **docling** | ≥2.18.0 | PDFs mixtos | ~30-60s |└──────┬──────┘

pip install -r scripts/requirements.txt

| **EasyOCR** | 1.7.1 | OCR backend | Con marker |

# 5. Instalar herramientas sistema

# macOS:| **PyTorch** | 2.5.1 | GPU (CUDA/MPS) | Crítico |       │### 1. Actualizar dependencias

brew install poppler tesseract



# Ubuntu:

sudo apt-get install poppler-utils tesseract-ocr### Hardware Soportado       ▼



# Windows:

scoop install poppler tesseract

```**macOS M4 (MPS):**┌──────────────────────┐```bash



### Verificar Instalación```bash



```bashpip install torch==2.5.1 torchvision==0.20.1│  PDFTypeDetector     │ ← Analiza primeras 3-10 páginas (< 1s)pip install -r scripts/requirements.txt

# Detector de tipo

python scripts/conversion/pdf_type_detector.py --help```



# Convertidor adaptativo- RAM: 16GB | Performance: ~6-7 min/50pág escaneadas | Workers: 2│  (pdfplumber ligero) │```

python scripts/conversion/adaptive_converter.py --help



# Base de datos tracking

python scripts/conversion/conversion_db.py**Ubuntu RTX 3070 (CUDA 12.1):**└──────┬───────────────┘

```

```bash

---

pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121       │Nuevas dependencias clave:

## 💻 Uso Básico

```

### 1. Detectar Tipo de PDF (Opcional)

- VRAM: 8GB | Performance: ~4-5 min/50pág escaneadas | Workers: 4       ▼- `marker-pdf` (ya existía)

```bash

# Análisis rápido (3 páginas)

python scripts/conversion/pdf_type_detector.py paper.pdf

```**Windows (CPU/CUDA):**   ¿Qué tipo?- `pdfplumber` (extracción de tablas)



**Output:**- CUDA: Mismo comando que Ubuntu

```

📊 ANÁLISIS DE TIPO DE PDF- CPU: `--index-url https://download.pytorch.org/whl/cpu`       │- `pytesseract` (OCR)

====================================

Archivo: paper.pdf

Tipo: NATIVE

Páginas totales: 58---   ┌───┴───┬─────────┬─────────┐- `opencv-python` (procesamiento de imágenes)

Páginas analizadas: 10

Páginas con texto: 10

Ratio texto: 100.0%

Estrategia: pdfplumber (rápido, alta fidelidad)## 📊 Detección de Tipo de PDF   │       │         │         │

====================================

```



### 2. Conversión Adaptativa (Automática)### PDFTypeDetectorNATIVE  SCANNED   MIXED    UNKNOWN### 2. Instalar Ollama (opcional pero recomendado)



```bash

# Conversión básica (detección automática)

python scripts/conversion/adaptive_converter.py paper.pdfClasifica PDFs analizando densidad de texto extraíble.   │       │         │         │



# Con validación Ollama (opcional)

python scripts/conversion/adaptive_converter.py paper.pdf --ollama

**Uso:**   ▼       ▼         ▼         ▼```bash

# Forzar estrategia específica (debug)

python scripts/conversion/adaptive_converter.py paper.pdf --strategy scanned```python



# Forzar reconversión (ignorar duplicados)from pdf_type_detector import PDFTypeDetectorpdfplumber marker-pdf docling  fallback# Desde https://ollama.ai/

python scripts/conversion/adaptive_converter.py paper.pdf --force

```



**Output:**detector = PDFTypeDetector()(5-10s)   (5-7min)  (30-60s)  (manual)# Luego:

```

============================================================pdf_type, stats = detector.detect("paper.pdf", quick=True)

🔄 CONVERSIÓN: paper.pdf

============================================================```ollama pull gemma3:12b

📋 PDF copiado a: sources_local/originals/paper.pdf

📊 Tipo: NATIVEprint(f"Tipo: {pdf_type.value}")

🚀 [NATIVE] Usando pdfplumber (rápido)

✅ [NATIVE] Extraídas 58 páginas, 8 tablasprint(f"Estrategia: {stats['recommended_strategy']}")```

💾 Markdown guardado: sources_local/converted/paper.md

✅ CONVERSIÓN COMPLETA en 1.6s```

============================================================

```---



### 3. Ver Resultados**CLI:**



```bash```bash### 3. Verificar instalación

# Markdown generado

cat sources_local/converted/paper.mdpython scripts/conversion/pdf_type_detector.py paper.pdf



# Tracking en DB```## 🛠️ Stack Tecnológico

python -c "

from scripts.conversion.conversion_db import ConversionTracker

with ConversionTracker() as t:

    stats = t.get_statistics()**Umbrales:**```bash

    print(f'Total conversiones: {stats[\"total_conversions\"]}')

    print(f'Confianza promedio: {stats[\"average_confidence\"]}')- **NATIVE**: ≥95% páginas con >100 caracteres

"

```- **SCANNED**: ≥80% páginas con <50 caracteres### Core Dependencies (Versiones Testeadas)python scripts/conversion/conversion_db.py



---- **MIXED**: Todo lo demás



## 📁 Estructura de Archivos# Debe crear: sources_local/metadata/conversion_tracker.db



```---

vermi-academic-rag/

├── sources_local/                    # ← LOCAL ONLY (ignorado por Git)| Herramienta | Versión | Propósito | Performance |```

│   ├── originals/                   # PDFs copiados aquí

│   │   ├── .gitkeep## 🔄 Conversión Adaptativa

│   │   └── paper.pdf

│   ├── converted/                   # Markdowns generados|------------|---------|-----------|------------|

│   │   ├── .gitkeep

│   │   └── paper.md### AdaptivePDFConverter

│   ├── metadata/                    # Base de datos SQLite

│   │   ├── .gitkeep| **pdfplumber** | 0.11.4 | PDFs nativos | ~5-10s/50pág |---

│   │   └── conversion_tracker.db

│   └── reports/                     # Reportes JSON (si usas --ollama)**Uso Básico:**

│       └── .gitkeep

├── scripts/```python| **marker-pdf** | ≥1.0.0 | PDFs escaneados | ~5-7min GPU |

│   └── conversion/

│       ├── adaptive_converter.py    # ← Conversor principalfrom adaptive_converter import AdaptivePDFConverter

│       ├── pdf_type_detector.py     # ← Detector de tipo

│       ├── conversion_db.py         # ← Tracking SQLite| **docling** | ≥2.18.0 | PDFs mixtos | ~30-60s |## 📁 Nueva Estructura

│       └── README.md                # Documentación técnica

└── .gitignore                       # sources_local/ ignoradoconverter = AdaptivePDFConverter(sources_local_dir="sources_local")

```

result = converter.convert_single("paper.pdf")| **EasyOCR** | 1.7.1 | OCR backend | Con marker |

---



## 🎯 Estrategias por Tipo de PDF

if result["success"]:| **PyTorch** | 2.5.1 | GPU (CUDA/MPS) | Crítico |```

### NATIVE (5-10 segundos)

- **Detección:** ≥95% páginas con >100 caracteres    print(f"✅ Markdown: {result['markdown_path']}")

- **Herramienta:** `pdfplumber` 

- **Performance:** ~5-10s para 50 páginas```vermi-academic-rag/

- **Ventajas:** Rápido, alta fidelidad, extrae tablas

- **Limitaciones:** Solo PDFs con texto seleccionable



### SCANNED (5-7 minutos)**CLI:**### Hardware Soportado├── sources_local/              # ← NUEVO: Local only (ignorado por Git)

- **Detección:** ≥80% páginas con <50 caracteres

- **Herramienta:** `marker-pdf` + EasyOCR + GPU```bash

- **Performance:** ~5-7min GPU, ~20-30min CPU

- **Ventajas:** OCR completo, imágenes, ecuaciones# Conversión automática│   ├── originals/             # PDFs originales

- **Limitaciones:** Lento, requiere GPU idealmente

python scripts/conversion/adaptive_converter.py paper.pdf

### MIXED (30-60 segundos)

- **Detección:** Páginas parcialmente con texto**RTX 3070 (CUDA 12.1):**│   │   └── .gitkeep

- **Herramienta:** `docling` (detección automática)

- **Performance:** ~30-60s para 50 páginas# Con validación Ollama

- **Ventajas:** Balanceado, detecta regiones

- **Limitaciones:** Requiere docling instaladopython scripts/conversion/adaptive_converter.py paper.pdf --ollama```bash│   ├── converted/             # Markdowns generados



---



## 🔍 Sistema de Tracking# Forzar estrategiapip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121│   │   └── .gitkeep



El sistema mantiene un registro completo de todas las conversiones en SQLite:python scripts/conversion/adaptive_converter.py paper.pdf --strategy scanned



### Base de Datos: `sources_local/metadata/conversion_tracker.db```````│   ├── metadata/              # Base de datos SQLite



**Tablas:**

- `conversions`: Registro de cada PDF procesado

  - id, pdf_filename, pdf_hash, status, created_at---- VRAM: 8GB | Performance: ~4-5 min/50pág | Workers: 4│   │   ├── .gitkeep

  - markdown_path, pages, has_tables

  - conversion_time_seconds, confidence_score

- `validation_reports`: Reportes de validación (si usas --ollama)

- `conversion_errors`: Errores encontrados## 📋 Estrategias de Conversión│   │   └── conversion_tracker.db  # ← Auto-creado



### Detección de Duplicados



El sistema calcula **SHA-256 hash** de cada PDF:### 1. NATIVE: pdfplumber (rápido)**Mac M4 (MPS):**│   └── reports/               # Reportes JSON

- ✅ Evita reprocesar PDFs idénticos

- ✅ Detecta duplicados aunque cambien de nombre/ubicación

- ⚙️ Usa `--force` para ignorar y reconvertir

**Cuando:** ≥95% páginas con texto seleccionable```bash│       └── .gitkeep

### Consultar Estadísticas



```python

from scripts.conversion.conversion_db import ConversionTracker**Características:**pip install torch==2.5.1 torchvision==0.20.1├── scripts/



with ConversionTracker() as tracker:- ✅ Extracción directa de texto

    stats = tracker.get_statistics()

    print(f"Total conversiones: {stats['total_conversions']}")- ✅ Tablas automáticas```│   └── conversion/

    print(f"PDFs con tablas: {stats['with_tables']}")

    print(f"Tiempo promedio: {stats.get('average_time', 0):.1f}s")- ✅ Sin OCR (sin errores)

```

- ✅ Muy rápido (5-10s/50pág)- RAM: 16GB | Performance: ~6-7 min/50pág | Workers: 2│       ├── convert_pdf_robust.py      # ← NUEVO: Conversor robusto

---



## 🤖 Validación con Ollama (Opcional)

**Ejemplo:**│       ├── batch_convert.py           # ← NUEVO: Batch processing

Si tienes Ollama + gemma3:12b instalado, puedes validar la conversión:

Papers académicos modernos, manuales técnicos digitales.

```bash

# 1. Instalar Ollama---│       ├── conversion_db.py           # ← NUEVO: Sistema de tracking

# macOS: Descargar de https://ollama.ai

# Ubuntu: curl https://ollama.ai/install.sh | sh### 2. SCANNED: marker-pdf + EasyOCR (preciso)



# 2. Descargar modelo│       ├── convert_pdf_local.py       # Legacy (simple)

ollama pull gemma3:12b

**Cuando:** ≥80% páginas sin texto extraíble (imágenes)

# 3. Convertir con validación

python scripts/conversion/adaptive_converter.py paper.pdf --ollama## 📊 Detección de Tipo de PDF│       └── README.md                  # Documentación completa

```

**Características:**

**Qué hace gemma3:12b:**

- Valida estructura Markdown (títulos, listas, párrafos)- 🔬 OCR con modelos Surya (state-of-the-art)└── .gitignore                 # Actualizado con sources_local/

- Calcula quality_score (0-100)

- Detecta issues (errores OCR, tablas rotas, etc.)- 🎯 Detección de layout con LayoutLMv3

- Genera resumen de fidelidad

- 🖼️ Extracción de imágenes### PDFTypeDetector```

**Ejemplo de validación:**

```json- ⏱️ Lento pero preciso (5-7min GPU/50pág)

{

  "quality_score": 92,

  "has_structure": true,

  "has_tables": true,**Hardware recomendado:**

  "issues": [],

  "summary": "Excellent conversion, clean structure"- RTX 3070: ~4-5 minClasifica PDFs analizando densidad de texto extraíble.---

}

```- Mac M4: ~6-7 min



---- CPU: ~20-30 min (no recomendado)



## ⚠️ Política BYOS



**NUNCA subir al repositorio:****Ejemplo:****Uso:**## 💻 Uso Básico

- ❌ PDFs originales (`sources_local/originals/`)

- ❌ Markdowns generados (`sources_local/converted/`)Tesis antiguas escaneadas, documentos históricos.

- ❌ Reportes JSON personales (`sources_local/reports/`)

- ❌ Base de datos SQLite (`sources_local/metadata/`)```python



**SÍ subir:**### 3. MIXED: docling (balanceado)

- ✅ Chunks parafraseados (JSONL en `dataset/chunks_enriched/`)

- ✅ Scripts y códigofrom pdf_type_detector import PDFTypeDetector### Conversión Individual

- ✅ Documentación

**Cuando:** Mezcla de texto y regiones sin texto

Todo `sources_local/` está en `.gitignore` para proteger BYOS.



---

**Características:**

## 🔄 Flujo Completo: PDF → Chunks → Dataset

- 🎭 Detección inteligente región por regióndetector = PDFTypeDetector()```bash

```bash

# 1. Conversión PDF→Markdown (aquí)- ⚡ OCR solo donde es necesario

python scripts/conversion/adaptive_converter.py paper.pdf

# → sources_local/converted/paper.md- ⚖️ Balance velocidad/precisión (30-60s/50pág)pdf_type, stats = detector.detect("paper.pdf", quick=True)# Conversión simple



# 2. Generación de chunks (manual con LLM web)

# Usar paper.md + scripts/chunking/generate_cards_local.md

# → chunks_paper.jsonl**Ejemplo:**python scripts/conversion/convert_pdf_robust.py paper.pdf



# 3. Validar chunksPapers con diagramas escaneados, presentaciones convertidas a PDF.

python scripts/chunking/validate_chunks.py \

  --file chunks_paper.jsonl \print(f"Tipo: {pdf_type.value}")

  --mode schema

---

# 4. Mover a dataset

cp chunks_paper.jsonl dataset/chunks_enriched/print(f"Estrategia: {stats['recommended_strategy']}")# PDF escaneado (con OCR)



# 5. Contribuir (solo JSONL, NO .md ni .pdf)## 🗄️ Sistema de Tracking

git add dataset/chunks_enriched/chunks_paper.jsonl

git commit -m "feat: Add chunks from paper.pdf"```python scripts/conversion/convert_pdf_robust.py scanned.pdf --force-ocr

git push

```### ConversionTracker (SQLite)



---



## 🐛 Solución de Problemas**Ubicación:** `sources_local/metadata/conversion_tracker.db`



### Error: pdfplumber no instalado**CLI:**# Sin Ollama (solo conversión)



```bash**Tablas:**

pip install pdfplumber==0.11.4 pdfminer.six==20231228

```- `conversions`: Registro de cada PDF procesado```bashpython scripts/conversion/convert_pdf_robust.py paper.pdf --no-ollama



### Error: marker-pdf no encontrado- `validation_reports`: Reportes de validación con gemma3



```bash- `conversion_errors`: Errores encontradospython scripts/conversion/pdf_type_detector.py paper.pdf```

pip install marker-pdf>=1.0.0

```



### Error: PyTorch sin GPU**Características:**```



```bash- ✅ Detección de duplicados por SHA-256 hash

# Verificar device

python -c "import torch; print(torch.cuda.is_available() or torch.backends.mps.is_available())"- ✅ Estadísticas de conversión### Conversión Batch



# Reinstalar con hardware correcto (ver sección instalación)- ✅ Historial completo

```

---

### Error: Conversión muy lenta

**Uso:**

1. Verificar que el PDF es realmente SCANNED (usa detector)

2. Si es NATIVE pero tardó mucho, es un bug - reportar```python```bash

3. Para SCANNED, esperar o usar CPU (más lento pero funciona)

from conversion_db import ConversionTracker

### Error: Ollama no responde

## 🔄 Conversión Adaptativa# Procesar directorio completo

```bash

# Verificar Ollama está corriendowith ConversionTracker() as tracker:

ollama list

    stats = tracker.get_statistics()python scripts/conversion/batch_convert.py ~/Downloads/papers/

# Iniciar si no está:

ollama serve    print(f"Total conversiones: {stats['total_conversions']}")

```

    print(f"Confianza promedio: {stats['average_confidence']}")### AdaptivePDFConverter

---

```

## 📖 Documentación Completa

# Con OCR forzado

- **README técnico:** `scripts/conversion/README.md`

- **Código con docstrings:** Todos los scripts documentados---

- **Guía de instalación:** `docs/guide/guia-instalacion.md`

- **Receta técnica:** `docs/guide/receta-pdf-markdown.md`**Uso Básico:**python scripts/conversion/batch_convert.py ~/Downloads/papers/ --force-ocr



---## 🤖 Validación con Ollama (opcional)



## 🎓 Próximos Pasos```python```



1. **Probar el detector:**### gemma3:12b local

   ```bash

   python scripts/conversion/pdf_type_detector.py test.pdffrom adaptive_converter import AdaptivePDFConverter

   ```

**Setup:**

2. **Convertir primer PDF:**

   ```bash```bash---

   python scripts/conversion/adaptive_converter.py test.pdf

   ```# Instalar Ollama



3. **Ver estadísticas:**# https://ollama.aiconverter = AdaptivePDFConverter(sources_local_dir="sources_local")

   ```python

   from scripts.conversion.conversion_db import ConversionTracker

   with ConversionTracker() as t:

       print(t.get_statistics())# Descargar modeloresult = converter.convert_single("paper.pdf")## 📊 Outputs

   ```

ollama pull gemma3:12b

4. **Generar chunks** (siguiente fase)

```

---



**Sistema adaptativo operacional. Estrategia inteligente. Hardware-aware. BYOS compliant.**

**Qué valida:**if result["success"]:### Después de convertir `paper.pdf`:

1. **Estructura** (títulos, listas, tablas)

2. **Calidad OCR** (errores l→1, O→0, rn→m)    print(f"✅ Markdown: {result['markdown_path']}")

3. **Confidence score** (0-100)

``````

**Uso:**

```bashsources_local/

python scripts/conversion/adaptive_converter.py paper.pdf --ollama

```**CLI:**├── originals/



**Output ejemplo:**```bash│   └── paper.pdf                    # Copia del original

```json

{# Conversión automática├── converted/

  "structure_ok": true,

  "ocr_quality": 95,python scripts/conversion/adaptive_converter.py paper.pdf│   ├── paper.md                     # Markdown convertido

  "tables_ok": true,

  "confidence": 92,│   └── paper_cleaned.md             # Si se hizo cleanup (opcional)

  "notes": "Excellent conversion"

}# Con validación Ollama├── metadata/

```

python scripts/conversion/adaptive_converter.py paper.pdf --ollama│   └── conversion_tracker.db        # Registro en DB

---

└── reports/

## 📈 Benchmarks

# Forzar estrategia    └── paper_report.json            # Reporte detallado

### Resultados Reales: ont66t-Valdivia-Ayaca-Cuela-Rojas.pdf

python scripts/conversion/adaptive_converter.py paper.pdf --strategy scanned```

**PDF:**

- Páginas: 58```

- Tipo detectado: NATIVE (100% texto)

- Tablas: 8 extraídas### Reporte JSON ejemplo:



**Performance:**---

- Detección: <1s

- Conversión: 1.6s```json

- Total: 1.6s

## 📋 Estrategias de Conversión{

**Comparación:**

- Con pdfplumber (óptimo): 1.6s ✅  "pdf": "paper.pdf",

- Con marker-pdf (innecesario): ~5-7min ❌ (200x más lento)

### 1. NATIVE (pdfplumber) - Rápida  "status": "success",

**Conclusión:** La detección adaptativa evita desperdicio de recursos.

- **Cuándo:** PDFs con texto seleccionable  "conversion_id": 1,

---

- **Performance:** ~5-10s para 50 páginas  "markdown_path": "sources_local/converted/paper.md",

## 🚀 Instalación

- **Ventajas:** ⚡ Velocidad, 💯 Fidelidad, 📊 Tablas  "steps": {

### Opción 1: Setup Automático (Recomendado)

- **Limitaciones:** ❌ No maneja PDFs escaneados    "marker": "success",

```bash

git clone https://github.com/lizkarol/vermi-academic-rag.git    "pdfplumber_tables": 3,

cd vermi-academic-rag

./setup.sh### 2. SCANNED (marker-pdf) - Precisa    "validation": {

```

- **Cuándo:** PDFs escaneados      "structure_ok": true,

El script detecta tu plataforma y configura todo automáticamente.

- **Performance:** ~5-7 min GPU para 50 páginas      "ocr_quality": 95,

### Opción 2: Manual

- **Ventajas:** 🔬 Alta precisión OCR, 📊 Tablas complejas      "tables_ok": true,

**1. Python 3.11+**

```bash- **Limitaciones:** 🐢 Lento, 🔥 GPU intensivo      "confidence": 92

# macOS

brew install python@3.11    },



# Ubuntu### 3. MIXED (docling) - Balanceada    "cleanup": "skipped"

sudo apt-get install python3.11 python3.11-venv

- **Cuándo:** PDFs híbridos  },

# Windows

# https://www.python.org/downloads/- **Performance:** ~30-60s  "total_time_seconds": 42.5

```

- **Estado:** 🚧 EN DESARROLLO (fallback a pdfplumber)}

**2. Virtual Environment**

```bash```

python3.11 -m venv .venv

source .venv/bin/activate  # macOS/Linux---

# .venv\Scripts\activate  # Windows

```---



**3. NumPy (PRIMERO)**## 🗄️ Tracking con SQLite

```bash

pip install "numpy>=1.26.4,<2.0.0"## 🔍 Sistema de Tracking

```

**Ubicación:** `sources_local/metadata/conversion_tracker.db`

**4. PyTorch (según hardware)**

```bash### Ver estadísticas

# Ver instrucciones en scripts/requirements.txt

```**Uso:**



**5. Dependencias del proyecto**```python```python

```bash

pip install -r scripts/requirements.txtfrom conversion_db import ConversionTrackerfrom scripts.conversion.conversion_db import ConversionTracker

```



**6. Herramientas del sistema**

```bashtracker = ConversionTracker("sources_local/metadata")with ConversionTracker() as tracker:

# macOS

brew install poppler tesseractis_dup, id = tracker.is_duplicate(pdf_path)    stats = tracker.get_statistics()



# Ubuntu```    print(f"Total conversiones: {stats['total_conversions']}")

sudo apt-get install poppler-utils tesseract-ocr

    print(f"Confianza promedio: {stats['average_confidence']}")

# Windows

scoop install poppler tesseract**CLI:**    print(f"Con tablas: {stats['with_tables']}")

```

```bash```

---

python scripts/conversion/conversion_db.py

## 💻 Uso Completo

```### Ver conversiones por estado

### Conversión Individual



```bash

# Básica (detección automática)---```python

python scripts/conversion/adaptive_converter.py paper.pdf

from scripts.conversion.conversion_db import ConversionTracker

# Con validación Ollama

python scripts/conversion/adaptive_converter.py paper.pdf --ollama## 🤖 Validación con Ollama (Opcional)



# Forzar reconversiónwith ConversionTracker() as tracker:

python scripts/conversion/adaptive_converter.py paper.pdf --force

### Gemma3:12b Local    # Conversiones exitosas

# Forzar estrategia (debug)

python scripts/conversion/adaptive_converter.py paper.pdf --strategy scanned    successful = tracker.get_conversions_by_status('success')



# Cambiar directorio**Instalación:**    print(f"Exitosas: {len(successful)}")

python scripts/conversion/adaptive_converter.py paper.pdf --sources-dir /custom/path

``````bash    



### Outputollama pull gemma3:12b    # Conversiones fallidas



``````    failed = tracker.get_conversions_by_status('failed')

sources_local/

├── originals/    for conv in failed:

│   └── paper.pdf                    # Copia del original

├── converted/**Uso:**        print(f"Falló: {conv['pdf_filename']}")

│   └── paper.md                     # Markdown generado

├── metadata/```bash```

│   └── conversion_tracker.db        # Registro en DB

└── reports/python scripts/conversion/adaptive_converter.py paper.pdf --ollama

    └── paper_validation.json        # Reporte (si --ollama)

``````---



---



## 🐛 Troubleshooting---## 🧪 Validación con Gemma3



### Error: `marker_single` not found



```bash## 📁 Estructura de Directorios### Qué hace gemma3:12b

pip uninstall marker-pdf

pip install marker-pdf --no-cache-dir

```

```1. **Valida estructura** (títulos, listas, tablas)

### Error: Ollama no responde

sources_local/2. **Detecta errores OCR** (l→1, O→0, rn→m)

```bash

# Verificar├── originals/       # PDFs input3. **Calcula confidence** (0-100)

ollama list

├── converted/       # Markdown output4. **Limpia errores** si confidence < 60

# Iniciar

ollama serve├── metadata/        # conversion_tracker.db

```

└── reports/         # Validación JSON### Ejemplo de validación

### Conversión muy lenta

```

1. Desactivar Ollama: `--no-ollama`

2. Verificar hardware: `python -c "import torch; print(torch.cuda.is_available())"````json

3. PDFs escaneados siempre son lentos (5-7min es normal)

Ver `BYOS_POLICY.md` para política de fuentes.{

### Tablas mal extraídas

  "structure_ok": true,

Las tablas complejas pueden tener errores. Revisar manualmente el markdown generado.

---  "ocr_quality": 95,

---

  "tables_ok": true,

## 🔄 Flujo Completo: PDF → Chunks

## 🚀 Quickstart  "confidence": 92,

```bash

# 1. Convertir PDF a Markdown  "notes": "Excellent conversion, minor spacing in one table"

python scripts/conversion/adaptive_converter.py paper.pdf

# → sources_local/converted/paper.md### 1. Instalación}



# 2. Generar chunks (manual con LLM web)```bash```

# Usar paper.md + scripts/chunking/generate_cards_local.md

# → chunks_paper.jsonlgit clone [repo]



# 3. Validar chunkscd vermi-academic-rag### Deshabilitar Ollama

python scripts/chunking/validate_chunks.py --file chunks_paper.jsonl --mode schema

# → Validation OKchmod +x setup.sh



# 4. Mover a dataset./setup.shSi no tienes Ollama instalado o prefieres omitir validación:

cp chunks_paper.jsonl dataset/chunks_enriched/

```

# 5. Contribuir (solo JSONL, NO .md ni .pdf)

git add dataset/chunks_enriched/chunks_paper.jsonl```bash

git commit -m "feat: Add chunks from paper.pdf"

git push### 2. Testpython convert_pdf_robust.py paper.pdf --no-ollama

```

```bash```

---

source .venv/bin/activate

## ⚠️ Política BYOS

python scripts/conversion/adaptive_converter.py test.pdfEl sistema funciona sin problema, solo omite la validación LLM.

**NUNCA subir al repositorio:**

- ❌ PDFs originales```

- ❌ Markdowns generados (.md)

- ❌ Reportes JSON personales---

- ❌ Base de datos SQLite

---

**SÍ subir:**

- ✅ Chunks parafraseados (JSONL)## 🔄 Flujo Completo: PDF → Chunks

- ✅ Scripts y código

- ✅ Documentación## 📊 Benchmarks



Todo `sources_local/` está en `.gitignore` para proteger BYOS.```bash



---**Test:** ont66t-Valdivia-Ayaca-Cuela-Rojas.pdf (16 páginas escaneadas)# 1. Convertir PDF a Markdown



## 📖 Documentación Adicionalpython scripts/conversion/convert_pdf_robust.py paper.pdf



- **README.md**: Visión general del proyecto| Hardware | Tiempo | Notas |# → sources_local/converted/paper.md

- **scripts/requirements.txt**: Detalles de instalación por plataforma

- **scripts/conversion/README.md**: Documentación detallada del conversor|----------|--------|-------|

- **docs/guide/guia-instalacion.md**: Guía exhaustiva de instalación

- **docs/guide/receta-pdf-markdown.md**: Receta completa del sistema| RTX 3070 | ~7 min | Óptimo |# 2. Generar chunks (manual con LLM web)



---| Mac M4   | ~8-10 min | Algunas etapas CPU |# Usar paper.md + scripts/chunking/generate_cards_local.md



## 🎓 Roadmap| CPU only | ~25-35 min | NO recomendado |# → chunks_paper.jsonl



**Fase 1 (Completada):**

- ✅ Sistema adaptativo de conversión

- ✅ Detección inteligente de tipo PDF---# 3. Validar chunks

- ✅ Tracking con SQLite

- ✅ Validación con Ollamapython scripts/chunking/validate_chunks.py \



**Fase 2 (Próximamente):**## 🐛 Troubleshooting  --file chunks_paper.jsonl \

- 🔨 Chunking automático (250-500 tokens)

- 🔨 Generación de embeddings (embeddinggemma:300m)  --mode schema

- 🔨 Integración LanceDB

### `ModuleNotFoundError: No module named '_lzma'`# → Validation OK

**Fase 3 (Futuro):**

- 🔨 RAG queries end-to-end```bash

- 🔨 Testing con preguntas piloto

- 🔨 Documentación finalbrew install xz# 4. Mover a dataset



---pyenv uninstall -f 3.11.11cp chunks_paper.jsonl dataset/chunks_enriched/



**Sistema adaptativo operacional. Listo para conversión a escala. BYOS compliant. 🚀**pyenv install 3.11.11


```# 5. Contribuir (solo JSONL, NO .md ni .pdf)

git add dataset/chunks_enriched/chunks_paper.jsonl

### `TypeError: memoryview` (marker bug)git commit -m "feat: Add chunks from paper.pdf"

Workaround implementado en `adaptive_converter.py`.git push

```

### GPU no detectado

```bash---

python -c "import torch; print(torch.cuda.is_available())"

# Reinstalar con CUDA si False## ⚠️ Política BYOS

```

**NUNCA subir al repositorio:**

---- ❌ PDFs originales

- ❌ Markdowns generados (.md)

## 🎯 Roadmap- ❌ Reportes JSON personales

- ❌ Base de datos SQLite

### Fase 1: Sistema Básico ✅

- [x] Detector de tipo**SÍ subir:**

- [x] 3 estrategias- ✅ Chunks parafraseados (JSONL)

- [x] Tracking SQLite- ✅ Scripts y código

- [x] Validación Ollama- ✅ Documentación



### Fase 2: Mejoras 🚧Todo `sources_local/` está en `.gitignore` para proteger BYOS.

- [ ] docling completo

- [ ] Batch paralelo---

- [ ] Dashboard web

## 🐛 Solución de Problemas

### Fase 3: RAG 📅

- [ ] Chunking### Error: marker_single not found

- [ ] LanceDB ingesta

- [ ] Query system```bash

pip install marker-pdf --no-cache-dir

---```



## 📚 Referencias### Error: Ollama connection refused



- marker-pdf: https://github.com/datalab-to/marker```bash

- pdfplumber: https://github.com/jsvine/pdfplumber# Verificar Ollama está corriendo

- docling: https://docling-project.github.io/docling/ollama list

- Ollama: https://ollama.com

# Si no, iniciar:

---ollama serve



**Versión:** 2.0 | **Última actualización:** 2025-11-03# En otra terminal:

ollama pull gemma3:12b
```

### Conversión lenta

1. Deshabilitar Ollama: `--no-ollama`
2. Procesar PDFs más pequeños
3. Reducir calidad en marker (doc: marker-pdf)

### Duplicados no detectados

```bash
# Forzar reconversión
python convert_pdf_robust.py paper.pdf --force
```

---

## 📖 Documentación Completa

- **README detallado**: `scripts/conversion/README.md`
- **Código con docstrings**: Todos los scripts tienen documentación inline
- **Ejemplos**: Ver sección de ejemplos en README.md

---

## 🎓 Próximos Pasos

1. **Probar con un PDF:**
   ```bash
   python scripts/conversion/convert_pdf_robust.py test.pdf
   ```

2. **Verificar output:**
   ```bash
   cat sources_local/reports/test_report.json
   ```

3. **Ver stats:**
   ```python
   from scripts.conversion.conversion_db import ConversionTracker
   with ConversionTracker() as t:
       print(t.get_statistics())
   ```

4. **Procesar batch de documentos:**
   ```bash
   python scripts/conversion/batch_convert.py ~/papers/
   ```

5. **Generar chunks** (siguiente fase)

---

**Sistema robusto operacional. Listo para conversión a escala. BYOS compliant.**

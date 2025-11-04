# Vermi Academic RAG Dataset

![GitHub License](https://img.shields.io/badge/License-MIT-blue.svg)
![BYOS Policy](https://img.shields.io/badge/Content%20Policy-BYOS-important.svg)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/lizkarol/vermi-academic-rag/validate-dataset.yml?branch=main&label=Dataset%20Validation)

Un repositorio público y colaborativo para crear un dataset de Retrieval-Augmented Generation (RAG) de alta calidad, especializado en **vermicompostaje doméstico** y construido bajo una estricta política legal-safe.

---

## 🧠 Filosofía: "El Motor, no la Gasolina"

Este proyecto opera bajo un principio fundamental: **proporcionamos las herramientas (el motor), pero no los datos brutos con copyright (la gasolina)**.

### ¿Por qué BYOS (Bring Your Own Sources)?

Debido a las restricciones de derechos de autor de los papers académicos y manuales técnicos, **no podemos alojar directamente los PDFs ni sus textos extraídos**. En su lugar, hemos desarrollado un flujo de trabajo que permite a la comunidad:

1. **Procesar documentos localmente** (en tu máquina, de forma privada)
2. **Generar chunks parafraseados** (con tus propias palabras, usando LLMs)
3. **Contribuir solo los datos estructurados** (que no infringen copyright)

### 🔧 El "Motor" que proporcionamos:

#### **Prioridad #1: Conversión PDF → Markdown con Sistema Adaptativo**
*   **`scripts/conversion/adaptive_converter.py`**: Sistema inteligente que selecciona la mejor estrategia según tipo de PDF
    - **PDFs nativos** (texto seleccionable): pdfplumber (⚡ 5-10s)
    - **PDFs escaneados** (imagen): marker-pdf + EasyOCR + GPU (🔬 5-7min)
    - **PDFs mixtos** (híbridos): docling con detección automática (⚖️ 30-60s)
    - Tracking con SQLite (detección de duplicados por SHA-256)
    - **Post-procesamiento con normalización** (jerarquía, limpieza, fusión de líneas)
    - Validación opcional con Ollama gemma3:12b (local, BYOS)

#### Herramientas de Validación:
*   **`scripts/chunking/validate_chunks.py`**: Valida esquema de chunks (modos: schema, semantic, coverage)

#### Documentación y Plantillas:
*   **Esquemas de datos**: Estructura clara y validable para chunks
*   **Guías de contribución**: Flujo paso a paso con ejemplos
*   **Templates de prompts**: Para generar chunks con LLMs

### ⛽ La "Gasolina" que tú pones:

Los papers académicos, manuales técnicos o documentos de vermicompostaje a los que tienes **acceso legal**.

## 🚀 Quickstart: Cómo Contribuir

### Requisitos Previos

- **Python 3.11+**
- **macOS, Ubuntu, o Windows** (soporte multi-plataforma)
- **Acceso a un LLM** (Gemini, GPT-4, Claude, o modelos locales vía Ollama)

### Pasos para tu Primera Contribución:

#### 1. **Setup Inicial**
```bash
# Clonar el repositorio
git clone https://github.com/lizkarol/vermi-academic-rag.git
cd vermi-academic-rag

# Ejecutar setup automático (recomienda)
./setup.sh

# O instalar manualmente (ver scripts/requirements.txt para detalles)
pip install -r scripts/requirements.txt
```

#### 2. **Conversión PDF → Markdown (SISTEMA ADAPTATIVO)**
El sistema detecta automáticamente el tipo de PDF y aplica la estrategia óptima.

```bash
# 1. Detectar tipo de PDF (rápido, < 1s)
python scripts/conversion/pdf_type_detector.py paper.pdf

# 2. Conversión automática (selecciona estrategia)
python scripts/conversion/adaptive_converter.py paper.pdf

# 3. Con validación Ollama (opcional, +10-30s)
python scripts/conversion/adaptive_converter.py paper.pdf --ollama

# 4. Sin normalización de markdown (solo conversión cruda)
python scripts/conversion/adaptive_converter.py paper.pdf --no-normalize

# 5. Forzar estrategia específica (debug)
python scripts/conversion/adaptive_converter.py paper.pdf --strategy scanned

# 6. Forzar reconversión (ignorar duplicados)
python scripts/conversion/adaptive_converter.py paper.pdf --force
```

**Salida:** 
- `sources_local/converted/paper.md` (Markdown generado y normalizado)
- `sources_local/metadata/conversion_tracker.db` (Tracking SQLite)
- `sources_local/reports/paper_normalization.json` (Reporte de cambios aplicados)
- `sources_local/reports/paper_validation.json` (Si usas --ollama)

**Performance:**
- PDFs nativos: ~5-10 segundos (pdfplumber)
- PDFs escaneados: ~5-7 minutos con GPU (marker-pdf + OCR)
- PDFs mixtos: ~30-60 segundos (docling)

**Características avanzadas:**
- ✅ Detección de duplicados por hash SHA-256
- ✅ **Post-procesamiento de normalización automático** (jerarquía, limpieza, fusión)
- ✅ **Soporte multi-formato**: APA, Vancouver, IEEE, Chicago, Harvard, MLA, ISO
- ✅ **Detección inteligente**: Decimal, Romano, Letras, Palabras clave
- ✅ Validación de fidelidad con gemma3:12b (Ollama)
- ✅ Extracción de tablas con pdfplumber
- ✅ Hardware detection automático (MPS/CUDA/CPU)
- ✅ Tracking en SQLite con estadísticas

**Ver más:** [`docs/CONVERSION_SYSTEM.md`](docs/CONVERSION_SYSTEM.md)

#### 3. **Generar Chunks Parafraseados (LLM - Manual)**
Usa el Markdown generado para crear chunks en tus propias palabras.

**Pasos:**
1. Abre `scripts/chunking/generate_cards_local.md` (plantilla de prompt)
2. Copia el contenido del Markdown generado en el paso 2
3. Usa tu LLM favorito (Gemini, GPT-4, Claude, etc.) con la plantilla
4. El LLM generará chunks en formato JSONL
5. Guarda el resultado como `chunks_tu_paper.jsonl`

**Resultado:** Archivo JSONL con chunks parafraseados

#### 4. **Validar Localmente**
Antes de hacer PR, valida que tus chunks cumplen el esquema:

```bash
python scripts/chunking/validate_chunks.py \
  --file chunks_tu_paper.jsonl \
  --mode schema
```

Si todo está OK, copia el archivo a `dataset/chunks_enriched/`

#### 5. **Contribuir al Repositorio**
```bash
git checkout -b feature/add-chunks-nombre-paper
git add dataset/chunks_enriched/chunks_tu_paper.jsonl
git commit -m "feat: Add chunks from [Nombre Paper/Manual]"
git push origin feature/add-chunks-nombre-paper
```

Abre un Pull Request describiendo:
- Fuente del documento (DOI/URL si es posible)
- Categoría cubierta (BIO/PROC/MAT/OPER/PROD)
- Número de chunks agregados

**⚠️ Recuerda:** NO subas PDFs ni Markdowns directos. Solo los chunks parafraseados en JSONL.

## 🎯 Contexto del Proyecto: VermiKhipu

Este dataset es parte del proyecto **VermiKhipu**, un sistema de vermicompostaje doméstico asistido por IA que opera 100% offline con interacción por voz en español.

### Dominio del Conocimiento

El dataset se enfoca en **vermicompostaje doméstico** (escala 1-5 kg/semana), cubriendo:

- **🦠 BIOLOGÍA**: Especies de lombrices (Eisenia fetida/andrei), fisiología, comportamiento
- **⚙️ PROCESO**: Parámetros (pH, C:N, humedad, temperatura), cinética de degradación
- **� MATERIALES**: Residuos orgánicos, materiales secos, clasificación y restricciones
- **🎮 OPERACIÓN**: Control de hábitat, intervenciones, calibración de actuadores
- **🌱 PRODUCTO**: Humus maduro, lixiviados, aplicaciones y dosificación

### Cobertura Actual

| Categoría | Chunks Objetivo | Estado | Prioridad |
|-----------|----------------|--------|-----------|
| BIOLOGÍA  | 40-60          | 🔴 0%  | ALTA      |
| PROCESO   | 60-80          | 🔴 0%  | CRÍTICA   |
| MATERIALES| 50-70          | 🔴 0%  | ALTA      |
| OPERACIÓN | 30-40          | 🔴 0%  | MEDIA     |
| PRODUCTO  | 20-30          | 🔴 0%  | MEDIA     |

**Meta Fase 1 (MVP):** 150-200 chunks cubriendo 70% de la taxonomía

---

## � Documentación

- **[INSTALLATION.md](INSTALLATION.md)** - Instalación paso a paso (macOS/Windows)
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Cómo contribuir al dataset
- **[ROADMAP.md](ROADMAP.md)** - Plan de desarrollo del proyecto
- **[BYOS_POLICY.md](BYOS_POLICY.md)** - Política de contenido legal-safe
- **[docs/DOMAIN_KNOWLEDGE.md](docs/DOMAIN_KNOWLEDGE.md)** - Taxonomía y dominio
- **[docs/DATA_SCHEMA.md](docs/DATA_SCHEMA.md)** - Esquema de datos detallado
- **[docs/MARKDOWN_NORMALIZATION.md](docs/MARKDOWN_NORMALIZATION.md)** - Sistema de post-procesamiento

---

## 📜 Licencia y Política de Contenido

*   El **código** de este repositorio está bajo **Licencia MIT**.
*   Las **contribuciones de datos** se rigen por nuestra **[Política BYOS](BYOS_POLICY.md)**, que debes leer y aceptar.

---

## 🛠️ Estado Actual (Fase 0)

**Funcional:**
- ✅ Conversión PDF→Markdown con sistema adaptativo (`adaptive_converter.py`)
- ✅ Post-procesamiento de normalización (`markdown_normalizer.py`)
- ✅ Validación de esquema (`validate_chunks.py`)
- ✅ Plantilla de generación de chunks (manual con LLM)
- ✅ Documentación completa y estructura organizada

**En Desarrollo:**
- 🔨 Generación automatizada de chunks
- 🔨 Sistema de embeddings y búsqueda vectorial
- 🔨 Pruebas RAG automáticas
- 🔨 CI/CD workflows

**Próximo Hito:** Primer ciclo de ingesta MVP (10-20 chunks reales)

---

¡Gracias por considerar contribuir a un recurso abierto, legal y de alta calidad para la comunidad de IA!

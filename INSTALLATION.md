# Guía de Instalación - Vermi Academic RAG

Esta guía cubre la instalación del entorno de desarrollo para **macOS** y **Windows**. Linux es compatible pero no está oficialmente soportado en esta versión.

---

## 📋 Requisitos Previos

### Todos los Sistemas Operativos

- **Python 3.11 o superior** (3.12 recomendado)
- **Git** para control de versiones
- **10GB+ de espacio en disco** (modelos + dependencias)
- **8GB+ RAM** (16GB recomendado para procesamiento de PDFs grandes)

### Opcional (Fase 2+)

- **GPU NVIDIA** con CUDA (acelera conversión PDF)
- **Ollama** (para generación automatizada de chunks - futuro)

---

## 🍎 Instalación en macOS

### 1. Instalar Python

#### Opción A: Homebrew (Recomendado)
```bash
# Instalar Homebrew si no lo tienes
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python 3.12
brew install python@3.12

# Verificar instalación
python3.12 --version
```

#### Opción B: python.org
Descarga el instalador desde [python.org](https://www.python.org/downloads/macos/)

### 2. Clonar el Repositorio
```bash
git clone https://github.com/lizkarol/vermi-academic-rag.git
cd vermi-academic-rag
```

### 3. Crear Entorno Virtual
```bash
# Crear venv
python3.12 -m venv venv

# Activar venv
source venv/bin/activate

# Verificar que estás en el venv
which python  # Debería mostrar ruta en ./venv/bin/python
```

### 4. Instalar Dependencias

#### Core Dependencies
```bash
pip install --upgrade pip
pip install -r scripts/requirements.txt
```

#### PyTorch (requerido para marker-sdk)

**Para Mac con Apple Silicon (M1/M2/M3):**
```bash
pip install torch torchvision torchaudio
```

**Para Mac con Intel:**
```bash
pip install torch torchvision torchaudio
```

### 5. Instalar marker-sdk

**Opción CPU (más lento pero compatible):**
```bash
pip install marker-pdf
```

**Opción GPU (si tienes NVIDIA eGPU - raro en Mac):**
```bash
pip install marker-pdf[gpu]
```

### 6. Configurar Variables de Entorno
```bash
# Copiar template
cp .env.example .env

# Editar con tu editor favorito
nano .env
```

Ver sección [Configuración de .env](#-configuración-de-env) más abajo.

### 7. Verificar Instalación
```bash
python scripts/conversion/adaptive_converter.py --help
```

Si ves el mensaje de ayuda sin errores, ¡estás listo!

---

## 🪟 Instalación en Windows

### 1. Instalar Python

1. Descargar instalador desde [python.org](https://www.python.org/downloads/windows/)
2. **IMPORTANTE:** Marcar "Add Python to PATH" durante instalación
3. Verificar en PowerShell:
```powershell
python --version
```

### 2. Instalar Git
Descargar desde [git-scm.com](https://git-scm.com/download/win)

### 3. Clonar el Repositorio
```powershell
git clone https://github.com/lizkarol/vermi-academic-rag.git
cd vermi-academic-rag
```

### 4. Crear Entorno Virtual
```powershell
# Crear venv
python -m venv venv

# Activar venv
.\venv\Scripts\Activate.ps1

# Si hay error de permisos, ejecutar como Admin:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 5. Instalar Dependencias

```powershell
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias core
pip install -r scripts\requirements.txt
```

### 6. Instalar PyTorch

**Para Windows con GPU NVIDIA:**
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**Para Windows sin GPU (CPU only):**
```powershell
pip install torch torchvision torchaudio
```

### 7. Instalar marker-sdk

**CPU (recomendado para empezar):**
```powershell
pip install marker-pdf
```

**GPU (si tienes NVIDIA con CUDA):**
```powershell
pip install marker-pdf[gpu]
```

### 8. Configurar Variables de Entorno
```powershell
# Copiar template
copy .env.example .env

# Editar con Notepad
notepad .env
```

### 9. Verificar Instalación
```powershell
python scripts\conversion\adaptive_converter.py --help
```

---

## 🔧 Configuración de .env

El archivo `.env` contiene variables de configuración. Copia `.env.example` y edita según tus necesidades:

```bash
# ========== CONVERSIÓN PDF → MARKDOWN ==========
# Directorio donde se guardan los Markdowns (ignorado por Git)
MARKDOWN_OUTPUT_DIR=sources_local/markdown_outputs

# Dispositivo para marker-sdk: cpu, cuda, mps (Mac)
MARKER_DEVICE=cpu

# Forzar OCR en todos los PDFs (útil para escaneados)
MARKER_FORCE_OCR=false

# ========== LLM Y EMBEDDINGS ==========
# URL del servidor Ollama (local)
OLLAMA_BASE_URL=http://localhost:11434

# Modelo de embeddings (300 dimensiones)
EMBEDDING_MODEL=embeddinggemma:300m

# Modelo LLM para generar chunks (opcional)
LLM_MODEL=gemma2:9b

# API Keys para LLMs comerciales (opcional)
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# GOOGLE_API_KEY=...

# ========== LANCEDB Y VECTORIZACIÓN ==========
# Ruta a la base de datos vectorial
LANCEDB_PATH=./data/lancedb

# Número de chunks a recuperar por query
TOP_K=10

# Umbral de confianza mínimo para respuestas RAG
CONFIDENCE_THRESHOLD=0.10

# ========== VALIDACIÓN Y QA ==========
# Confidence score mínimo para ingestar chunks
MIN_CONFIDENCE_SCORE=0.70

# Threshold de similitud para detectar duplicados
DUPLICATE_THRESHOLD=0.85

# ========== SISTEMA ==========
# Nivel de logging: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL=INFO

# Workers para procesamiento paralelo
MAX_WORKERS=4
```

---

## 🧪 Prueba de Instalación

### Test Básico: Conversión PDF

```bash
# Crear directorio de prueba
mkdir -p test_data

# Descargar un PDF de prueba (ejemplo: paper de arXiv)
curl -o test_data/sample.pdf "https://arxiv.org/pdf/2301.00001.pdf"

# Convertir a Markdown
python scripts/conversion/adaptive_converter.py test_data/sample.pdf

# Verificar salida
ls sources_local/markdown_outputs/sample.md
```

---

## 🐛 Troubleshooting

### Error: "No module named 'torch'"
```bash
# Reinstalar PyTorch
pip install torch torchvision torchaudio
```

### Error: "marker-sdk not found"
```bash
# Reinstalar marker
pip uninstall marker-pdf
pip install marker-pdf --no-cache-dir
```

### macOS: "command not found: python"
```bash
# Usar python3 en lugar de python
alias python=python3
# O agregar a ~/.zshrc
```

### Windows: "Scripts de activación deshabilitados"
```powershell
# Ejecutar como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### GPU no detectada (CUDA)
```bash
# Verificar que CUDA está instalado
python -c "import torch; print(torch.cuda.is_available())"

# Si retorna False, reinstalar PyTorch con soporte CUDA
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

---

## 📚 Recursos Adicionales

- **PyTorch Installation Guide:** https://pytorch.org/get-started/locally/
- **marker-sdk GitHub:** https://github.com/VikParuchuri/marker
- **Project Documentation:** Ver `docs/` en este repositorio

---

## 💬 ¿Problemas?

Si encuentras algún problema no cubierto aquí:

1. Revisa los [Issues existentes](https://github.com/lizkarol/vermi-academic-rag/issues)
2. Crea un nuevo Issue con:
   - Sistema operativo y versión
   - Versión de Python (`python --version`)
   - Log completo del error
   - Pasos para reproducir

---

**¡Listo!** Ahora puedes continuar con el [Quickstart en README.md](README.md#-quickstart-cómo-contribuir)

#!/usr/bin/env bash#!/usr/bin/env bash#!/bin/bash#!/bin/bash



# ====================================# ============================================

# Setup: Sistema Adaptativo PDF→Markdown

# Multi-plataforma: macOS (MPS), Ubuntu (CUDA), Windows (WSL/Git Bash)# Setup: Sistema Adaptativo PDF→Markdown# ====================================# Setup script for vermi-academic-rag (macOS/Linux)

# Fecha: Noviembre 2025

# ====================================# Fecha: Noviembre 2025



set -e  # Exit on error# Plataformas: macOS (MPS), Ubuntu (CUDA), Windows (WSL/Git Bash)# Vermi Academic RAG - Setup (macOS)# Automates environment setup, dependency installation, and validation



# Colores# ============================================

RED='\033[0;31m'

GREEN='\033[0;32m'# Sistema Adaptativo PDF→Markdown

YELLOW='\033[1;33m'

BLUE='\033[0;34m'set -e  # Exit on error

NC='\033[0m' # No Color

# Mac M4 + Apple Silicon (MPS)set -e  # Exit on error

msg() { echo -e "${2}$1${NC}"; }

# Colores

# Banner

msg "=========================================" $BLUERED='\033[0;31m'# ====================================

msg "Sistema Adaptativo PDF→Markdown" $BLUE

msg "Detección inteligente: NATIVE/SCANNED/MIXED" $BLUEGREEN='\033[0;32m'

msg "=========================================" $BLUE

echo ""YELLOW='\033[1;33m'# Colors for output



# ========== 1. Detectar Plataforma ==========BLUE='\033[0;34m'

msg "Detectando plataforma..." $YELLOW

NC='\033[0m' # No Colorset -e  # Exit on errorRED='\033[0;31m'

OS_TYPE="$(uname -s)"

case "${OS_TYPE}" in

    Linux*)     OS="Linux";;

    Darwin*)    OS="macOS";;# BannerGREEN='\033[0;32m'

    MINGW*|MSYS*|CYGWIN*)  OS="Windows";;

    *)          OS="UNKNOWN";;echo -e "${BLUE}"

esac

cat << "EOF"# ColorsYELLOW='\033[1;33m'

if [ "$OS" = "UNKNOWN" ]; then

    msg "❌ Plataforma no soportada: $OS_TYPE" $RED╔═══════════════════════════════════════════════════════════╗

    msg "💡 Soportado: macOS, Ubuntu/Linux, Windows (WSL/Git Bash)" $YELLOW

    exit 1║   Sistema Adaptativo PDF→Markdown                         ║RED='\033[0;31m'BLUE='\033[0;34m'

fi

║   Detección inteligente: NATIVE/SCANNED/MIXED            ║

msg "✓ Plataforma: $OS" $GREEN

echo ""║   Hardware: macOS M4 (MPS) / Ubuntu RTX 3070 (CUDA)      ║GREEN='\033[0;32m'NC='\033[0m' # No Color



# ========== 2. Verificar Python 3.11+ ==========╚═══════════════════════════════════════════════════════════╝

msg "Verificando Python 3.11+..." $YELLOW

EOFYELLOW='\033[1;33m'

if ! command -v python3 &> /dev/null; then

    msg "❌ Python 3 no encontrado" $REDecho -e "${NC}"

    msg "📦 Instalar con:" $YELLOW

    msg "   macOS:   brew install python@3.11" $BLUEBLUE='\033[0;34m'# Print colored message

    msg "   Ubuntu:  sudo apt-get install python3.11 python3.11-venv" $BLUE

    msg "   Windows: https://www.python.org/downloads/" $BLUE# Detectar plataforma

    exit 1

fiOS="unknown"NC='\033[0m'print_message() {



PYTHON_VERSION=$(python3 --version | awk '{print $2}')if [[ "$OSTYPE" == "darwin"* ]]; then

PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)

PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)    OS="macOS"    local color=$1



if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); thenelif [[ "$OSTYPE" == "linux-gnu"* ]]; then

    msg "❌ Python $PYTHON_VERSION < 3.11 (mínimo requerido)" $RED

    msg "📦 Actualizar a Python 3.11+" $YELLOW    OS="Linux"msg() { echo -e "${2}$1${NC}"; }    shift

    exit 1

fielif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then



msg "✓ Python $PYTHON_VERSION" $GREEN    OS="Windows"    echo -e "${color}$@${NC}"

echo ""

fi

# ========== 3. Crear Virtual Environment ==========

msg "Configurando virtual environment..." $YELLOWmsg "=========================================" $BLUE}



if [ -d ".venv" ]; thenecho -e "${GREEN}✓ Plataforma detectada: ${OS}${NC}\n"

    msg "⚠️  .venv ya existe, usando existente" $YELLOW

elsemsg "Vermi Academic RAG - Setup macOS" $BLUE

    python3 -m venv .venv

    msg "✓ .venv creado" $GREEN# ============================================

fi

# 1. Verificar Python 3.11+msg "Sistema Adaptativo PDF→Markdown" $BLUEprint_message $BLUE "========================================="

# Activar venv

source .venv/bin/activate# ============================================



# Actualizar pipecho -e "${BLUE}[1/7] Verificando Python 3.11+...${NC}"msg "=========================================" $BLUEprint_message $BLUE "Vermi Academic RAG - Setup Script"

pip install --upgrade pip setuptools wheel --quiet

msg "✓ pip actualizado" $GREEN

echo ""

if ! command -v python3 &> /dev/null; thenecho ""print_message $BLUE "Sistema Adaptativo PDF→Markdown"

# ========== 4. Instalar NumPy PRIMERO ==========

msg "Instalando NumPy (< 2.0 para compatibilidad)..." $YELLOW    echo -e "${RED}✗ Python 3 no encontrado${NC}"

pip install "numpy>=1.26.4,<2.0.0" --quiet

msg "✓ NumPy instalado" $GREEN    echo "  Instalar:"print_message $BLUE "RTX 3070 (CUDA) + Mac M4 (MPS)"

echo ""

    echo "    macOS: brew install python@3.11"

# ========== 5. Instalar PyTorch según hardware ==========

msg "Instalando PyTorch (según hardware)..." $YELLOW    echo "    Ubuntu: sudo apt-get install python3.11 python3.11-venv"# ========== 1. Verificar macOS ==========print_message $BLUE "========================================="



if [ "$OS" = "macOS" ]; then    echo "    Windows: https://www.python.org/downloads/"

    # macOS: detectar Apple Silicon (M1/M2/M3/M4) o Intel

    if [[ $(uname -m) == "arm64" ]]; then    exit 1if [ "$(uname -s)" != "Darwin" ]; thenecho ""

        msg "  → macOS Apple Silicon (MPS)" $BLUE

        pip install torch==2.5.1 torchvision==0.20.1 --quietfi

    else

        msg "  → macOS Intel (CPU)" $BLUE    msg "❌ Este script es solo para macOS" $RED

        pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu --quiet

    fiPYTHON_VERSION=$(python3 --version | awk '{print $2}')

elif [ "$OS" = "Linux" ]; then

    # Linux: detectar CUDAPYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)    msg "💡 Para Linux/Windows, ver docs/guide/guia-instalacion.md" $YELLOW# Detect OS

    if command -v nvidia-smi &> /dev/null; then

        msg "  → Linux CUDA detectado (instalando con CUDA 12.1)" $BLUEPYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

        pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121 --quiet

    else    exit 1OS="$(uname -s)"

        msg "  → Linux CPU (sin GPU detectada)" $BLUE

        pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu --quietif [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then

    fi

elif [ "$OS" = "Windows" ]; then    echo -e "${RED}✗ Python $PYTHON_VERSION < 3.11${NC}"ficase "${OS}" in

    # Windows: asumir CPU por defecto (usuario puede reinstalar con CUDA)

    msg "  → Windows (instalando CPU por defecto)" $BLUE    echo "  Actualizar a Python 3.11+"

    msg "💡 Si tienes GPU NVIDIA, reinstala con:" $YELLOW

    msg "   pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121" $BLUE    exit 1    Linux*)     OS_TYPE=Linux;;

    pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu --quiet

fifi



msg "✓ PyTorch instalado" $GREENmsg "✓ macOS detectado" $GREEN    Darwin*)    OS_TYPE=macOS;;

echo ""

echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}"

# ========== 6. Instalar Stack PDF→Markdown ==========

msg "Instalando stack PDF→Markdown..." $YELLOWecho ""    *)          OS_TYPE="UNKNOWN"



msg "  📄 pdfplumber (PDFs nativos)" $BLUE# ============================================

pip install pdfplumber==0.11.4 pdfminer.six==20231228 --quiet

# 2. Crear Virtual Environmentesac

msg "  🔬 marker-pdf (PDFs escaneados + OCR)" $BLUE

pip install marker-pdf>=1.0.0 --quiet# ============================================



msg "  ⚙️  docling (PDFs mixtos)" $BLUEecho -e "\n${BLUE}[2/7] Creando virtual environment...${NC}"# ========== 2. Verificar Python 3.11+ ==========

pip install docling>=2.18.0 --quiet 2>/dev/null || msg "  ⚠️  docling falló (continuando)" $YELLOW



msg "✓ Stack PDF instalado" $GREEN

echo ""if [ -d ".venv" ]; thenmsg "Verificando Python..." $YELLOWprint_message $BLUE "Detected OS: $OS_TYPE"



# ========== 7. Instalar Herramientas OCR ==========    echo -e "${YELLOW}⚠ .venv ya existe, usando existente${NC}"

msg "Instalando herramientas OCR..." $YELLOW

elseecho ""

pip install Pillow==10.4.0 pdf2image==1.17.0 --quiet

pip install opencv-python-headless==4.10.0.84 --quiet    python3 -m venv .venv

pip install easyocr==1.7.1 --quiet 2>/dev/null || msg "  ⚠️  EasyOCR falló (requiere PyTorch)" $YELLOW

pip install pytesseract==0.3.13 --quiet    echo -e "${GREEN}✓ .venv creado${NC}"if command -v python3.11 &> /dev/null; then



msg "✓ Herramientas OCR instaladas" $GREENfi

echo ""

    PYTHON_CMD=python3.11if [ "$OS_TYPE" = "UNKNOWN" ]; then

# ========== 8. Instalar LanceDB (RAG) ==========

msg "Instalando LanceDB para RAG..." $YELLOW# Activar venv

pip install lancedb==0.25.2 pylance==0.21.0 sentence-transformers>=3.3.0 --quiet

msg "✓ LanceDB instalado" $GREENsource .venv/bin/activateelif command -v python3 &> /dev/null; then    print_message $RED "Unsupported operating system. This script works on macOS and Linux."

echo ""



# ========== 9. Instalar Dependencias Adicionales ==========

msg "Instalando dependencias adicionales..." $YELLOW# Actualizar pip    PYTHON_CMD=python3    exit 1

pip install pandas>=2.2.0 pyarrow>=0.17.0 --quiet

pip install pydantic>=2.9.0 jsonschema>=4.23.0 --quietpip install --upgrade pip > /dev/null 2>&1

pip install requests>=2.31.0 python-dotenv>=1.0.0 --quiet

pip install pytest>=8.3.0 pytest-cov>=6.0.0 --quietecho -e "${GREEN}✓ pip actualizado${NC}"elsefi

pip install tqdm>=4.66.0 colorama>=0.4.6 --quiet

msg "✓ Dependencias adicionales instaladas" $GREEN

echo ""

# ============================================    msg "❌ Python 3.11+ no encontrado" $RED

# ========== 10. Instalar Herramientas de Sistema (si existen package managers) ==========

msg "Verificando herramientas de sistema (poppler, tesseract)..." $YELLOW# 3. Instalar NumPy (PRIMERO)



if [ "$OS" = "macOS" ]; then# ============================================    msg "📦 Instalar con: brew install python@3.11" $YELLOW# Check Python version

    if command -v brew &> /dev/null; then

        if ! brew list poppler &> /dev/null 2>&1; thenecho -e "\n${BLUE}[3/7] Instalando NumPy...${NC}"

            msg "  📦 Instalando poppler..." $BLUE

            brew install poppler --quiet 2>/dev/null || msg "  ⚠️  poppler falló" $YELLOW    msg "📦 O con pyenv: pyenv install 3.11.11" $YELLOWprint_message $YELLOW "Checking Python installation..."

        else

            msg "  ✓ poppler ya instalado" $GREENpip install "numpy>=1.26.4,<2.0.0"

        fi

        echo -e "${GREEN}✓ NumPy instalado${NC}"    exit 1if command -v python3.12 &> /dev/null; then

        if ! brew list tesseract &> /dev/null 2>&1; then

            msg "  📦 Instalando tesseract..." $BLUE

            brew install tesseract --quiet 2>/dev/null || msg "  ⚠️  tesseract falló" $YELLOW

        else# ============================================fi    PYTHON_CMD=python3.12

            msg "  ✓ tesseract ya instalado" $GREEN

        fi# 4. Instalar PyTorch según hardware

    else

        msg "  ⚠️  Homebrew no encontrado, instalar manualmente:" $YELLOW# ============================================elif command -v python3.11 &> /dev/null; then

        msg "     brew install poppler tesseract" $BLUE

    fiecho -e "\n${BLUE}[4/7] Instalando PyTorch...${NC}"

elif [ "$OS" = "Linux" ]; then

    msg "  💡 Instalar herramientas con:" $YELLOWPYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')    PYTHON_CMD=python3.11

    msg "     sudo apt-get install poppler-utils tesseract-ocr" $BLUE

elif [ "$OS" = "Windows" ]; then# Detectar hardware

    msg "  💡 Instalar herramientas con scoop o chocolatey:" $YELLOW

    msg "     scoop install poppler tesseract" $BLUEif [[ "$OS" == "macOS" ]]; thenmsg "✓ Python $PYTHON_VERSION encontrado" $GREENelif command -v python3 &> /dev/null; then

    msg "     choco install poppler tesseract" $BLUE

fi    # macOS: MPS (Apple Silicon) o CPU (Intel)



echo ""    if [[ $(uname -m) == "arm64" ]]; thenecho ""    PYTHON_CMD=python3



# ========== 11. Verificar Ollama (Opcional) ==========        echo "  → macOS Apple Silicon (MPS)"

msg "Verificando Ollama (LLM local, opcional)..." $YELLOW

        pip install torch==2.5.1 torchvision==0.20.1else

if command -v ollama &> /dev/null; then

    OLLAMA_VERSION=$(ollama --version 2>&1 | head -1)    else

    msg "✓ Ollama encontrado: $OLLAMA_VERSION" $GREEN

            echo "  → macOS Intel (CPU)"# ========== 3. Verificar Homebrew ==========    print_message $RED "Python 3.11+ not found. Please install Python first."

    if ollama list 2>/dev/null | grep -q "gemma3:12b"; then

        msg "✓ gemma3:12b ya descargado" $GREEN        pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu

    else

        msg "💡 Para validación LLM, descargar con:" $YELLOW    fimsg "Verificando Homebrew..." $YELLOW    print_message $YELLOW "Visit: https://www.python.org/downloads/"

        msg "   ollama pull gemma3:12b" $BLUE

    fielif [[ "$OS" == "Linux" ]]; then

else

    msg "⚠️  Ollama no instalado (opcional para validación)" $YELLOW    # Linux: detectar CUDA    exit 1

    msg "📦 Descargar de: https://ollama.com" $BLUE

fi    if command -v nvidia-smi &> /dev/null; then



echo ""        echo "  → Ubuntu CUDA detectado"if ! command -v brew &> /dev/null; thenfi



# ========== 12. Crear Estructura de Directorios ==========        pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121

msg "Creando estructura de directorios..." $YELLOW

    else    msg "❌ Homebrew no encontrado" $RED

mkdir -p sources_local/{originals,converted,metadata,reports}

touch sources_local/originals/.gitkeep        echo "  → Ubuntu CPU (sin GPU)"

touch sources_local/converted/.gitkeep

touch sources_local/metadata/.gitkeep        pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu    msg "📦 Instalar desde: https://brew.sh" $YELLOWPYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')

touch sources_local/reports/.gitkeep

    fi

mkdir -p dataset/{chunks_enriched,embeddings,validation}

mkdir -p data/lancedbelse    exit 1print_message $GREEN "✓ Found Python $PYTHON_VERSION"

mkdir -p logs

    # Windows: asumir CPU (usuario puede reinstalar con CUDA si tiene GPU)

msg "✓ Directorios creados" $GREEN

echo ""    echo "  → Windows CPU"fiecho ""



# ========== 13. Configurar .env ==========    echo "  💡 Si tienes GPU NVIDIA, reinstalar con:"

if [ ! -f ".env" ]; then

    if [ -f ".env.example" ]; then    echo "     pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121"

        msg "Creando .env desde template..." $YELLOW

        cp .env.example .env    pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu

        msg "✓ .env creado (editar si necesitas custom config)" $GREEN

    elsefimsg "✓ Homebrew instalado" $GREEN# Check Git

        msg "⚠️  .env.example no encontrado (continuando)" $YELLOW

    fi

else

    msg "✓ .env ya existe" $GREENecho -e "${GREEN}✓ PyTorch instalado${NC}"echo ""print_message $YELLOW "Checking Git installation..."

fi



echo ""

# ============================================if ! command -v git &> /dev/null; then

# ========== 14. Validar Instalación ==========

msg "Validando instalación..." $YELLOW# 5. Instalar dependencias del proyecto



# PyTorch + Device# ============================================# ========== 4. Instalar dependencias de sistema ==========    print_message $RED "Git not found. Please install Git first."

TORCH_INFO=$(python -c "import torch; print(f'PyTorch {torch.__version__} | Device: {\"CUDA\" if torch.cuda.is_available() else \"MPS\" if torch.backends.mps.is_available() else \"CPU\"}')" 2>&1)

if echo "$TORCH_INFO" | grep -q "PyTorch"; thenecho -e "\n${BLUE}[5/7] Instalando dependencias del proyecto...${NC}"

    msg "✓ $TORCH_INFO" $GREEN

elsemsg "Instalando dependencias de sistema (Homebrew)..." $YELLOW    exit 1

    msg "⚠️  PyTorch validación falló" $YELLOW

fipip install -r scripts/requirements.txt



# PDF Type Detectorecho -e "${GREEN}✓ Dependencias instaladas${NC}"fi

if python scripts/conversion/pdf_type_detector.py --help > /dev/null 2>&1; then

    msg "✓ PDF Type Detector funcional" $GREEN

else

    msg "❌ PDF Type Detector falló" $RED# ============================================# Poppler (para pdf2image)print_message $GREEN "✓ Git is installed"

fi

# 6. Instalar herramientas del sistema

# Adaptive Converter

if python scripts/conversion/adaptive_converter.py --help > /dev/null 2>&1; then# ============================================if ! brew list poppler &> /dev/null; thenecho ""

    msg "✓ Adaptive Converter funcional" $GREEN

elseecho -e "\n${BLUE}[6/7] Verificando herramientas del sistema...${NC}"

    msg "❌ Adaptive Converter falló" $RED

fi    msg "📦 Instalando poppler..." $BLUE



# Conversion DB# poppler (para pdf2image)

if python scripts/conversion/conversion_db.py > /dev/null 2>&1; then

    msg "✓ Conversion Tracker funcional" $GREENif ! command -v pdfinfo &> /dev/null; then    brew install poppler# Create virtual environment

else

    msg "❌ Conversion Tracker falló" $RED    echo -e "${YELLOW}⚠ poppler no encontrado${NC}"

fi

    echo "  Instalar:"elseprint_message $YELLOW "Creating virtual environment..."

echo ""

    if [[ "$OS" == "macOS" ]]; then

# ========== 15. Mensaje Final ==========

msg "=========================================" $GREEN        echo "    brew install poppler"    msg "✓ poppler ya instalado" $GREENif [ -d ".venv" ]; then

msg "✅ Setup completado exitosamente!" $GREEN

msg "=========================================" $GREEN    elif [[ "$OS" == "Linux" ]]; then

echo ""

        echo "    sudo apt-get install poppler-utils"fi    print_message $YELLOW "Virtual environment already exists. Skipping creation."

msg "🎯 PRÓXIMOS PASOS:" $BLUE

echo ""    else

msg "1. Copiar PDFs a sources_local/originals/" $YELLOW

echo ""        echo "    scoop install poppler  (o chocolatey: choco install poppler)"else

msg "2. Detectar tipo de PDF:" $YELLOW

msg "   python scripts/conversion/pdf_type_detector.py sources_local/originals/paper.pdf" $BLUE    fi

echo ""

msg "3. Convertir PDF (estrategia adaptativa):" $YELLOWelse# Tesseract (OCR fallback, opcional)    $PYTHON_CMD -m venv .venv

msg "   python scripts/conversion/adaptive_converter.py sources_local/originals/paper.pdf" $BLUE

echo ""    echo -e "${GREEN}✓ poppler instalado${NC}"

msg "4. Con validación Ollama (opcional):" $YELLOW

msg "   python scripts/conversion/adaptive_converter.py paper.pdf --ollama" $BLUEfiif ! brew list tesseract &> /dev/null; then    print_message $GREEN "✓ Virtual environment created"

echo ""

msg "5. Ver resultados:" $YELLOW

msg "   cat sources_local/converted/paper.md" $BLUE

echo ""# tesseract (para pytesseract OCR)    msg "📦 Instalando tesseract (opcional)..." $BLUEfi

msg "📚 Documentación:" $BLUE

msg "   docs/CONVERSION_SYSTEM.md - Sistema adaptativo completo" $YELLOWif ! command -v tesseract &> /dev/null; then

msg "   docs/guide/guia-instalacion.md - Guía técnica detallada" $YELLOW

msg "   README.md - Quickstart general" $YELLOW    echo -e "${YELLOW}⚠ tesseract no encontrado${NC}"    brew install tesseractecho ""

echo ""

msg "💡 Para activar el entorno en futuras sesiones:" $BLUE    echo "  Instalar:"

msg "   source .venv/bin/activate" $YELLOW

echo ""    if [[ "$OS" == "macOS" ]]; thenelse

msg "🚀 Sistema listo para conversión PDF→Markdown!" $GREEN

echo ""        echo "    brew install tesseract"


    elif [[ "$OS" == "Linux" ]]; then    msg "✓ tesseract ya instalado" $GREEN# Activate virtual environment

        echo "    sudo apt-get install tesseract-ocr"

    elsefiprint_message $YELLOW "Activating virtual environment..."

        echo "    scoop install tesseract  (o chocolatey: choco install tesseract)"

    fisource .venv/bin/activate

else

    echo -e "${GREEN}✓ tesseract instalado${NC}"echo ""print_message $GREEN "✓ Virtual environment activated"

fi

echo ""

# ============================================

# 7. Verificar Ollama (opcional)# ========== 5. Crear virtual environment ==========

# ============================================

echo -e "\n${BLUE}[7/7] Verificando Ollama (opcional)...${NC}"msg "Configurando entorno virtual..." $YELLOW# Upgrade pip



if ! command -v ollama &> /dev/null; thenprint_message $YELLOW "Upgrading pip..."

    echo -e "${YELLOW}⚠ Ollama no encontrado (opcional)${NC}"

    echo "  Para validación con gemma3:12b, instalar desde:"if [ -d ".venv" ]; thenpip install --upgrade pip --quiet

    echo "    https://ollama.ai"

    echo "  Luego ejecutar: ollama pull gemma3:12b"    msg "⚠️  .venv ya existe, usando existente" $YELLOWprint_message $GREEN "✓ pip upgraded"

else

    OLLAMA_VERSION=$(ollama --version 2>&1 | head -1)elseecho ""

    echo -e "${GREEN}✓ Ollama instalado: $OLLAMA_VERSION${NC}"

        $PYTHON_CMD -m venv .venv

    # Verificar si gemma3:12b está disponible

    if ollama list | grep -q "gemma3:12b"; then    msg "✓ Virtual environment creado" $GREEN# Install core dependencies

        echo -e "${GREEN}✓ Modelo gemma3:12b disponible${NC}"

    elsefiprint_message $YELLOW "Installing core dependencies..."

        echo -e "${YELLOW}⚠ Modelo gemma3:12b no encontrado${NC}"

        echo "  Ejecutar: ollama pull gemma3:12b"if [ -f "scripts/requirements.txt" ]; then

    fi

fisource .venv/bin/activate    pip install -r scripts/requirements.txt --quiet



# ============================================msg "✓ .venv activado" $GREEN    print_message $GREEN "✓ Core dependencies installed"

# 8. Crear directorios locales

# ============================================echo ""else

echo -e "\n${BLUE}Creando estructura sources_local/...${NC}"

    print_message $RED "requirements.txt not found in scripts/"

mkdir -p sources_local/originals

mkdir -p sources_local/converted# ========== 6. Actualizar pip ==========    exit 1

mkdir -p sources_local/metadata

mkdir -p sources_local/reportsmsg "Actualizando pip..." $YELLOWfi



touch sources_local/originals/.gitkeeppip install --upgrade pip setuptools wheel --quietecho ""

touch sources_local/converted/.gitkeep

touch sources_local/metadata/.gitkeepmsg "✓ pip actualizado" $GREEN

touch sources_local/reports/.gitkeep

echo ""# Install PyTorch (MANUAL - según hardware)

echo -e "${GREEN}✓ Directorios creados${NC}"

print_message $YELLOW "Instalando PyTorch..."

# ============================================

# 9. Validar instalación# ========== 7. Instalar NumPy PRIMERO ==========print_message $BLUE "⚠️  IMPORTANTE: PyTorch se instala según tu hardware:"

# ============================================

echo -e "\n${BLUE}Validando instalación...${NC}"msg "Instalando NumPy (< 2.0 para compatibilidad)..." $YELLOWprint_message $BLUE "   - RTX 3070 (CUDA 12.1): pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121"



# Test imports críticospip install "numpy>=1.26.4,<2.0.0" --quietprint_message $BLUE "   - Mac M4 (MPS): pip install torch==2.5.1 torchvision==0.20.1"

python3 << 'EOF'

import sysmsg "✓ NumPy instalado" $GREENprint_message $BLUE "   - CPU only: pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu"

try:

    import torchecho ""echo ""

    import pdfplumber

    from pathlib import Path

    

    # Verificar PyTorch device# ========== 8. Instalar PyTorch con MPS ==========if [ "$OS_TYPE" = "macOS" ]; then

    if torch.backends.mps.is_available():

        device = "MPS (Apple Silicon)"msg "Instalando PyTorch con soporte MPS (Apple Silicon)..." $YELLOW    print_message $BLUE "Detectado macOS, instalando con soporte MPS (Apple Silicon)..."

    elif torch.cuda.is_available():

        device = f"CUDA {torch.cuda.get_device_name(0)}"pip install torch==2.5.1 torchvision==0.20.1 --quiet    pip install torch==2.5.1 torchvision==0.20.1 --quiet

    else:

        device = "CPU"    print_message $GREEN "✓ PyTorch instalado con MPS support"

    

    print(f"  ✓ PyTorch: {torch.__version__} ({device})")# Verificar MPSelse

    print(f"  ✓ pdfplumber: {pdfplumber.__version__}")

    print(f"  ✓ Python: {sys.version.split()[0]}")if python -c "import torch; assert torch.backends.mps.is_available()" 2>/dev/null; then    print_message $YELLOW "Linux detectado. Si tienes NVIDIA GPU, ejecuta manualmente:"

    

except ImportError as e:    msg "✓ PyTorch con MPS instalado correctamente" $GREEN    print_message $YELLOW "pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121"

    print(f"  ✗ Error importando: {e}")

    sys.exit(1)else    print_message $BLUE "Instalando versión CPU por ahora..."

EOF

    msg "⚠️  MPS no disponible (revisar GPU)" $YELLOW    pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu --quiet

if [ $? -eq 0 ]; then

    echo -e "${GREEN}✓ Validación exitosa${NC}"fi    print_message $GREEN "✓ PyTorch instalado (CPU)"

else

    echo -e "${RED}✗ Validación falló${NC}"echo ""fi

    exit 1

fiecho ""



# ============================================# ========== 9. Instalar stack PDF→Markdown ==========

# Resumen final

# ============================================msg "Instalando herramientas PDF→Markdown..." $YELLOW# Install NumPy (ANTES de otras deps)

echo -e "\n${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"

echo -e "${GREEN}║            ✓ INSTALACIÓN COMPLETADA                       ║${NC}"print_message $YELLOW "Instalando NumPy (< 2.0 para compatibilidad)..."

echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}\n"

msg "  📄 pdfplumber (PDFs nativos)" $BLUEpip install "numpy>=1.26.4,<2.0.0" --quiet

echo -e "${BLUE}Siguientes pasos:${NC}"

echo ""pip install pdfplumber==0.11.4 pdfminer.six==20231228 --quietprint_message $GREEN "✓ NumPy instalado"

echo "1. Activar entorno virtual:"

echo "   ${YELLOW}source .venv/bin/activate${NC}"echo ""

echo ""

echo "2. Probar conversión:"msg "  🔬 marker-pdf (PDFs escaneados)" $BLUE

echo "   ${YELLOW}python scripts/conversion/adaptive_converter.py tu_archivo.pdf${NC}"

echo ""pip install marker-pdf>=1.0.0 --quiet# Install PDF processing stack

echo "3. Ver ayuda:"

echo "   ${YELLOW}python scripts/conversion/adaptive_converter.py --help${NC}"print_message $YELLOW "Instalando stack PDF→Markdown..."

echo ""

echo "4. Documentación completa:"msg "  ⚙️  docling (PDFs mixtos)" $BLUEprint_message $BLUE "  - pdfplumber (PDFs nativos)"

echo "   ${YELLOW}docs/CONVERSION_SYSTEM.md${NC}"

echo ""pip install docling>=2.18.0 --quiet 2>/dev/null || msg "  ⚠️  docling falló (continuando)" $YELLOWprint_message $BLUE "  - docling (PDFs mixtos)"

echo -e "${BLUE}Estrategias automáticas:${NC}"

echo "  • NATIVE (texto seleccionable): pdfplumber (~5-10s)"print_message $BLUE "  - marker-pdf (PDFs escaneados + OCR)"

echo "  • SCANNED (imagen pura): marker-pdf + OCR (~5-7min GPU)"

echo "  • MIXED (híbrido): docling (~30-60s)"msg "✓ Stack PDF instalado" $GREENpip install pdfplumber==0.11.4 pdfminer.six==20231228 --quiet

echo ""

echo -e "${GREEN}¡Listo para convertir PDFs! 🚀${NC}"echo ""pip install docling>=2.18.0 --quiet 2>/dev/null || print_message $YELLOW "⚠️  docling falló, continuando..."


pip install marker-pdf>=1.0.0 --quiet

# ========== 10. Instalar herramientas OCR ==========print_message $GREEN "✓ Stack PDF instalado"

msg "Instalando herramientas OCR..." $YELLOWecho ""



pip install Pillow==10.4.0 pdf2image==1.17.0 --quiet# Install OCR tools

pip install opencv-python-headless==4.10.0.84 --quietprint_message $YELLOW "Instalando herramientas OCR..."

pip install easyocr==1.7.1 --quiet 2>/dev/null || msg "  ⚠️  EasyOCR falló (continuando)" $YELLOWprint_message $BLUE "  - EasyOCR (GPU accelerated)"

pip install pytesseract==0.3.13 --quietprint_message $BLUE "  - pytesseract (fallback)"

pip install Pillow==10.4.0 pdf2image==1.17.0 --quiet

# Instalar deps de EasyOCRpip install opencv-python-headless==4.10.0.84 --quiet

pip install scikit-image>=0.24.0 scipy>=1.14.0 pyyaml>=6.0.0 python-bidi>=0.6.0 --quietpip install easyocr==1.7.1 --quiet 2>/dev/null || print_message $YELLOW "⚠️  EasyOCR falló (requiere PyTorch)"

pip install pytesseract==0.3.13 --quiet

msg "✓ Herramientas OCR instaladas" $GREENprint_message $GREEN "✓ Herramientas OCR instaladas"

echo ""echo ""



# ========== 11. Instalar LanceDB (RAG) ==========# Install LanceDB (RAG vector DB)

msg "Instalando LanceDB para RAG..." $YELLOWprint_message $YELLOW "Instalando LanceDB para RAG..."

pip install lancedb==0.25.2 pylance==0.21.0 --quietpip install lancedb==0.25.2 pylance==0.21.0 sentence-transformers>=3.3.0 --quiet

pip install sentence-transformers>=3.3.0 --quietprint_message $GREEN "✓ LanceDB instalado"

msg "✓ LanceDB instalado" $GREENecho ""

echo ""

# Check Ollama availability (no instalar, solo verificar)

# ========== 12. Instalar otras dependencias ==========print_message $YELLOW "Verificando Ollama (LLM local)..."

msg "Instalando dependencias adicionales..." $YELLOWif command -v ollama &> /dev/null; then

pip install pandas>=2.2.0 pyarrow>=0.17.0 --quiet    print_message $GREEN "✓ Ollama encontrado: $(ollama --version)"

pip install pydantic>=2.9.0 jsonschema>=4.23.0 --quiet    print_message $BLUE "  Para descargar gemma3:12b: ollama pull gemma3:12b"

pip install requests>=2.31.0 python-dotenv>=1.0.0 --quietelse

pip install pytest>=8.3.0 pytest-cov>=6.0.0 --quiet    print_message $YELLOW "⚠️  Ollama no instalado (opcional)"

pip install tqdm>=4.66.0 colorama>=0.4.6 --quiet    print_message $BLUE "  Descargar de: https://ollama.com"

msg "✓ Dependencias adicionales instaladas" $GREENfi

echo ""echo ""



# ========== 13. Verificar Ollama ==========# Create necessary directories

msg "Verificando Ollama (LLM local, opcional)..." $YELLOWprint_message $YELLOW "Creating project directories..."

mkdir -p sources/markdown_outputs

if command -v ollama &> /dev/null; thenmkdir -p dataset/chunks_enriched

    OLLAMA_VERSION=$(ollama --version 2>&1 | head -1)mkdir -p dataset/embeddings

    msg "✓ Ollama encontrado: $OLLAMA_VERSION" $GREENmkdir -p data/lancedb

    mkdir -p logs

    # Verificar si gemma3:12b está instaladomkdir -p sources_local/originals

    if ollama list 2>/dev/null | grep -q "gemma3:12b"; thenmkdir -p sources_local/converted

        msg "✓ gemma3:12b ya descargado" $GREENmkdir -p sources_local/metadata

    elsemkdir -p sources_local/reports

        msg "💡 Para validación LLM, descargar: ollama pull gemma3:12b" $BLUEprint_message $GREEN "✓ Directories created"

    fiecho ""

else

    msg "⚠️  Ollama no instalado (opcional para validación)" $YELLOW# Copy .env.example if .env doesn't exist

    msg "📦 Descargar de: https://ollama.com/download/mac" $BLUEif [ ! -f ".env" ]; then

fi    if [ -f ".env.example" ]; then

echo ""        print_message $YELLOW "Creating .env file from template..."

        cp .env.example .env

# ========== 14. Crear directorios ==========        print_message $GREEN "✓ .env file created"

msg "Creando estructura de directorios..." $YELLOW        print_message $BLUE "→ Please edit .env to configure your environment"

mkdir -p sources_local/{originals,converted,metadata,reports}    else

mkdir -p dataset/{chunks_enriched,embeddings,validation}        print_message $YELLOW "⚠ .env.example not found. Skipping .env creation."

mkdir -p data/lancedb    fi

mkdir -p logselse

msg "✓ Directorios creados" $GREEN    print_message $YELLOW ".env file already exists. Skipping."

echo ""fi

echo ""

# ========== 15. Configurar .env ==========

if [ ! -f ".env" ]; then# Validate installation

    if [ -f ".env.example" ]; thenprint_message $YELLOW "Validando instalación..."

        msg "Creando .env desde template..." $YELLOW

        cp .env.example .env# Validar detector de tipo de PDF

        msg "✓ .env creado (editar si necesitas custom config)" $GREENif python scripts/conversion/pdf_type_detector.py --help > /dev/null 2>&1; then

    fi    print_message $GREEN "✓ PDF Type Detector funcional"

elseelse

    msg "✓ .env ya existe" $GREEN    print_message $YELLOW "⚠️  PDF Type Detector falló (verificar pdfplumber)"

fifi

echo ""

# Validar convertidor adaptativo

# ========== 16. Validar instalación ==========if python scripts/conversion/adaptive_converter.py --help > /dev/null 2>&1; then

msg "Validando instalación..." $YELLOW    print_message $GREEN "✓ Convertidor Adaptativo funcional"

else

# PyTorch + MPS    print_message $YELLOW "⚠️  Convertidor Adaptativo falló (verificar dependencias)"

TORCH_INFO=$(python -c "import torch; print(f'PyTorch {torch.__version__} | Device: {\"MPS\" if torch.backends.mps.is_available() else \"CPU\"}')" 2>&1)fi

if echo "$TORCH_INFO" | grep -q "MPS"; then

    msg "✓ $TORCH_INFO" $GREEN# Validar base de datos

elseif python scripts/conversion/conversion_db.py > /dev/null 2>&1; then

    msg "⚠️  $TORCH_INFO (MPS no disponible)" $YELLOW    print_message $GREEN "✓ Sistema de tracking (SQLite) funcional"

fielse

    print_message $RED "✗ Sistema de tracking falló"

# PDF Type Detector    exit 1

if python scripts/conversion/pdf_type_detector.py --help > /dev/null 2>&1; thenfi

    msg "✓ PDF Type Detector funcional" $GREEN

else# Validar PyTorch

    msg "❌ PDF Type Detector falló" $REDif python -c "import torch; print(f'PyTorch {torch.__version__} - Device: {\"CUDA\" if torch.cuda.is_available() else \"MPS\" if torch.backends.mps.is_available() else \"CPU\"}')" 2>&1 | grep -q "PyTorch"; then

fi    TORCH_INFO=$(python -c "import torch; print(f'PyTorch {torch.__version__} - Device: {\"CUDA\" if torch.cuda.is_available() else \"MPS\" if torch.backends.mps.is_available() else \"CPU\"}')")

    print_message $GREEN "✓ $TORCH_INFO"

# Adaptive Converterelse

if python scripts/conversion/adaptive_converter.py --help > /dev/null 2>&1; then    print_message $YELLOW "⚠️  PyTorch validación falló"

    msg "✓ Adaptive Converter funcional" $GREENfi

else

    msg "❌ Adaptive Converter falló" $REDecho ""

fi

# Final message

# Conversion DBprint_message $GREEN "========================================="

if python scripts/conversion/conversion_db.py > /dev/null 2>&1; thenprint_message $GREEN "✓ Setup completed successfully!"

    msg "✓ Conversion Tracker funcional" $GREENprint_message $GREEN "========================================="

elseecho ""

    msg "❌ Conversion Tracker falló" $REDprint_message $BLUE "🎯 PRÓXIMOS PASOS:"

fiecho ""

print_message $YELLOW "1. Editar .env (si necesitas configuración custom)"

echo ""echo ""

print_message $YELLOW "2. Probar detección de tipo de PDF:"

# ========== 17. Mensaje final ==========print_message $BLUE "   python scripts/conversion/pdf_type_detector.py test.pdf"

msg "=========================================" $GREENecho ""

msg "✅ Setup completado exitosamente!" $GREENprint_message $YELLOW "3. Convertir PDF con estrategia adaptativa:"

msg "=========================================" $GREENprint_message $BLUE "   python scripts/conversion/adaptive_converter.py test.pdf"

echo ""print_message $BLUE "   python scripts/conversion/adaptive_converter.py test.pdf --ollama  # Con validación LLM"

echo ""

msg "🎯 PRÓXIMOS PASOS:" $BLUEprint_message $YELLOW "4. Leer documentación completa:"

echo ""print_message $BLUE "   docs/CONVERSION_SYSTEM.md - Sistema de conversión adaptativo"

msg "1. Copiar tus PDFs a sources_local/originals/" $YELLOWprint_message $BLUE "   README.md - Quickstart general"

echo ""print_message $BLUE "   BYOS_POLICY.md - Política BYOS (Bring Your Own Sources)"

msg "2. Detectar tipo de PDF:" $YELLOWecho ""

msg "   python scripts/conversion/pdf_type_detector.py sources_local/originals/paper.pdf" $BLUEprint_message $BLUE "Para activar el entorno en futuras sesiones:"

echo ""print_message $YELLOW "   source .venv/bin/activate"

msg "3. Convertir PDF (estrategia adaptativa):" $YELLOWecho ""

msg "   python scripts/conversion/adaptive_converter.py sources_local/originals/paper.pdf" $BLUEprint_message $GREEN "🚀 Sistema listo para conversión inteligente PDF→Markdown!"

echo ""echo ""

msg "4. Con validación Ollama (opcional):" $YELLOW
msg "   python scripts/conversion/adaptive_converter.py paper.pdf --ollama" $BLUE
echo ""
msg "5. Ver resultados:" $YELLOW
msg "   cat sources_local/converted/paper.md" $BLUE
echo ""
msg "📚 Documentación:" $BLUE
msg "   docs/CONVERSION_SYSTEM.md - Sistema adaptativo completo" $YELLOW
msg "   docs/guide/guia-instalacion.md - Guía técnica detallada" $YELLOW
msg "   README.md - Quickstart general" $YELLOW
echo ""
msg "💡 Para activar el entorno en futuras sesiones:" $BLUE
msg "   source .venv/bin/activate" $YELLOW
echo ""
msg "🚀 Sistema listo para conversión PDF→Markdown!" $GREEN
echo ""

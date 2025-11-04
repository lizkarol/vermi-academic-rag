#!/usr/bin/env bash

set -euo pipefail

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}$1${NC}"
}

print_ok() {
    echo -e "${GREEN}$1${NC}"
}

print_warn() {
    echo -e "${YELLOW}$1${NC}"
}

print_error() {
    echo -e "${RED}$1${NC}"
}

banner() {
    cat <<'EOF'
============================================================
   Sistema Adaptativo PDF→Markdown - Vermi Academic RAG
   Configuración automática del entorno (macOS / Linux / WSL)
============================================================
EOF
}

detect_os() {
    case "$(uname -s)" in
        Darwin*) echo "macOS" ;;
        Linux*) echo "Linux" ;;
        MINGW*|MSYS*|CYGWIN*) echo "Windows" ;;
        *) echo "UNKNOWN" ;;
    esac
}

ensure_python() {
    local python_cmd="${1:-python3}"
    if ! command -v "${python_cmd}" >/dev/null 2>&1; then
        print_error "Python 3 no encontrado. Instala Python 3.11 antes de continuar."
        exit 1
    fi

    local version
    version=$("${python_cmd}" --version | awk '{print $2}')
    local major minor
    major=$(echo "${version}" | cut -d '.' -f1)
    minor=$(echo "${version}" | cut -d '.' -f2)

    if (( major < 3 )) || { (( major == 3 )) && (( minor < 11 )); }; then
        print_warn "Se requiere Python 3.11+. Detectado ${version}."
        if command -v python3.11 >/dev/null 2>&1; then
            print_warn "Usando python3.11 encontrado en el sistema."
            python_cmd="python3.11"
        else
            print_error "Actualiza a Python 3.11 e intenta nuevamente."
            exit 1
        fi
    fi

    echo "${python_cmd}"
}

ensure_venv() {
    local python_cmd="$1"
    if [[ ! -d ".venv" ]]; then
        print_step "[1/6] Creando entorno virtual (.venv)"
        "${python_cmd}" -m venv .venv
        print_ok "Entorno virtual creado."
    else
        print_warn ".venv ya existe. Se reutilizará el entorno virtual."
    fi

    # shellcheck disable=SC1091
    source .venv/bin/activate
}

install_numpy() {
    print_step "[2/6] Instalando NumPy (compatibilidad con docling/pdfplumber)"
    if ! pip install "numpy>=1.26.4,<2.0.0" >/dev/null; then
        print_error "No se pudo instalar NumPy. Revisa tu conexión o permisos."
        exit 1
    fi
    print_ok "NumPy instalado."
}

install_pytorch() {
    local os_name="$1"
    print_step "[3/6] Instalando PyTorch (opcional según hardware)"
    local torch_cmd

    case "${os_name}" in
        macOS)
            torch_cmd="pip install torch==2.5.1 torchvision==0.20.1"
            ;;
        Linux)
            if command -v nvidia-smi >/dev/null 2>&1; then
                torch_cmd="pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121"
            else
                torch_cmd="pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu"
            fi
            ;;
        Windows)
            torch_cmd="pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121"
            ;;
        *)
            torch_cmd="pip install torch==2.5.1 torchvision==0.20.1"
            ;;
    esac

    set +e
    if eval "${torch_cmd}"; then
        print_ok "PyTorch instalado correctamente."
    else
        print_warn "No fue posible instalar PyTorch automáticamente. El sistema podrá ejecutarse en modo CPU básico."
    fi
    set -e
}

install_requirements() {
    print_step "[4/6] Instalando dependencias del proyecto"
    if [[ ! -f scripts/requirements.txt ]]; then
        print_warn "scripts/requirements.txt no encontrado. Saltando instalación."
        return
    fi

    set +e
    pip install -r scripts/requirements.txt
    local status=$?
    set -e

    if (( status != 0 )); then
        print_warn "Algunas dependencias no se instalaron. Revisa la salida anterior para instalar manualmente."
    else
        print_ok "Dependencias instaladas."
    fi
}

ensure_env_file() {
    print_step "[5/6] Preparando archivo .env"
    if [[ -f ".env" ]]; then
        print_warn ".env ya existe. No se sobrescribe."
        return
    fi

    if [[ -f ".env.example" ]]; then
        cp .env.example .env
        print_ok ".env creado a partir de .env.example."
    else
        cat > .env <<'EOF'
# Generado por setup.sh (valores por defecto)
SOURCES_DIR=sources
SOURCES_ORIGINALS=sources/originals
SOURCES_CONVERTED=sources/converted
SOURCES_METADATA=sources/metadata
SOURCES_REPORTS=sources/reports
DATA_DIR=data
PROFILES_DIR=config/profiles
MARKER_DEVICE=cpu
EOF
        print_warn ".env.example no disponible. Se creó un .env mínimo."
    fi
}

ensure_directories() {
    print_step "[6/6] Creando estructura de directorios"
    mkdir -p sources/{originals,converted,metadata,reports,assets}
    mkdir -p data/{raw,processed,embeddings,metadata,validation}
    mkdir -p config/profiles
    mkdir -p dataset/{chunks_enriched,embeddings,validation}
    mkdir -p logs temp
    print_ok "Estructura creada."
}

run_smoke_tests() {
    print_step "Ejecución de pruebas básicas"

    set +e
    python - <<'PY'
try:
    import pdfplumber  # noqa: F401
    print("✓ pdfplumber importado")
except Exception as exc:
    print(f"⚠️  pdfplumber: {exc}")

try:
    import docling  # noqa: F401
    print("✓ docling importado")
except Exception as exc:
    print(f"⚠️  docling: {exc}")
PY

    python -m compileall scripts/conversion/adaptive_converter.py >/dev/null
    python scripts/conversion/pdf_type_detector.py --help >/dev/null
    set -e

    print_ok "Pruebas básicas completadas."
}

main() {
    banner
    local os_name
    os_name=$(detect_os)

    if [[ "${os_name}" == "UNKNOWN" ]]; then
        print_error "Plataforma no soportada."
        exit 1
    fi

    print_step "Plataforma detectada: ${os_name}"
    local python_cmd
    python_cmd=$(ensure_python)

    ensure_venv "${python_cmd}"
    pip install --upgrade pip setuptools wheel >/dev/null
    install_numpy
    install_pytorch "${os_name}"
    install_requirements
    ensure_env_file
    ensure_directories
    run_smoke_tests

    print_ok "Setup completado. Ejecuta 'source .venv/bin/activate' para comenzar."
}

main "$@"

#!/bin/bash
# Setup script for vermi-academic-rag (macOS/Linux)
# Automates environment setup, dependency installation, and validation

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored message
print_message() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}

print_message $BLUE "========================================="
print_message $BLUE "Vermi Academic RAG - Setup Script"
print_message $BLUE "========================================="
echo ""

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     OS_TYPE=Linux;;
    Darwin*)    OS_TYPE=macOS;;
    *)          OS_TYPE="UNKNOWN"
esac

print_message $BLUE "Detected OS: $OS_TYPE"
echo ""

if [ "$OS_TYPE" = "UNKNOWN" ]; then
    print_message $RED "Unsupported operating system. This script works on macOS and Linux."
    exit 1
fi

# Check Python version
print_message $YELLOW "Checking Python installation..."
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD=python3.12
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD=python3.11
elif command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    print_message $RED "Python 3.11+ not found. Please install Python first."
    print_message $YELLOW "Visit: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
print_message $GREEN "✓ Found Python $PYTHON_VERSION"
echo ""

# Check Git
print_message $YELLOW "Checking Git installation..."
if ! command -v git &> /dev/null; then
    print_message $RED "Git not found. Please install Git first."
    exit 1
fi
print_message $GREEN "✓ Git is installed"
echo ""

# Create virtual environment
print_message $YELLOW "Creating virtual environment..."
if [ -d "venv" ]; then
    print_message $YELLOW "Virtual environment already exists. Skipping creation."
else
    $PYTHON_CMD -m venv venv
    print_message $GREEN "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
print_message $YELLOW "Activating virtual environment..."
source venv/bin/activate
print_message $GREEN "✓ Virtual environment activated"
echo ""

# Upgrade pip
print_message $YELLOW "Upgrading pip..."
pip install --upgrade pip --quiet
print_message $GREEN "✓ pip upgraded"
echo ""

# Install core dependencies
print_message $YELLOW "Installing core dependencies..."
if [ -f "scripts/requirements.txt" ]; then
    pip install -r scripts/requirements.txt --quiet
    print_message $GREEN "✓ Core dependencies installed"
else
    print_message $RED "requirements.txt not found in scripts/"
    exit 1
fi
echo ""

# Install PyTorch
print_message $YELLOW "Installing PyTorch..."
if [ "$OS_TYPE" = "macOS" ]; then
    print_message $BLUE "Installing PyTorch for macOS (Metal/MPS support)..."
    pip install torch torchvision torchaudio --quiet
else
    print_message $BLUE "Installing PyTorch for Linux (CPU)..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu --quiet
fi
print_message $GREEN "✓ PyTorch installed"
echo ""

# Install marker-sdk
print_message $YELLOW "Installing marker-sdk (PDF→Markdown conversion)..."
pip install marker-pdf --quiet
print_message $GREEN "✓ marker-sdk installed"
echo ""

# Create necessary directories
print_message $YELLOW "Creating project directories..."
mkdir -p sources/markdown_outputs
mkdir -p dataset/chunks_enriched
mkdir -p dataset/embeddings
mkdir -p data/lancedb
mkdir -p logs
print_message $GREEN "✓ Directories created"
echo ""

# Copy .env.example if .env doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        print_message $YELLOW "Creating .env file from template..."
        cp .env.example .env
        print_message $GREEN "✓ .env file created"
        print_message $BLUE "→ Please edit .env to configure your environment"
    else
        print_message $YELLOW "⚠ .env.example not found. Skipping .env creation."
    fi
else
    print_message $YELLOW ".env file already exists. Skipping."
fi
echo ""

# Validate installation
print_message $YELLOW "Validating installation..."
if python scripts/conversion/convert_pdf_local.py --help > /dev/null 2>&1; then
    print_message $GREEN "✓ PDF conversion script is functional"
else
    print_message $RED "✗ PDF conversion script failed validation"
    exit 1
fi

if python scripts/chunking/validate_chunks.py --help > /dev/null 2>&1; then
    print_message $GREEN "✓ Chunk validation script is functional"
else
    print_message $RED "✗ Chunk validation script failed validation"
    exit 1
fi
echo ""

# Final message
print_message $GREEN "========================================="
print_message $GREEN "✓ Setup completed successfully!"
print_message $GREEN "========================================="
echo ""
print_message $BLUE "Next steps:"
print_message $YELLOW "1. Edit .env file with your configuration (if needed)"
print_message $YELLOW "2. Test PDF conversion:"
print_message $BLUE "   python scripts/conversion/convert_pdf_local.py test.pdf"
print_message $YELLOW "3. Read CONTRIBUTING.md to start contributing"
print_message $YELLOW "4. Read docs/DOMAIN_KNOWLEDGE.md to understand the dataset scope"
echo ""
print_message $BLUE "To activate the environment in future sessions:"
print_message $YELLOW "   source venv/bin/activate"
echo ""

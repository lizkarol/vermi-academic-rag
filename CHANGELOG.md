# Historial de Versiones

Todos los cambios notables del proyecto se documentan en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

### 🧹 Limpieza y Depuración - 2025-11-03

#### Removed
- **Scripts placeholder no implementados:**
  - `scripts/embeddings/compute_embeddings.py` (stub)
  - `scripts/chunking/merge_redundant.py` (stub)
  - `scripts/testing/test_retrieval.py` (stub)
  - `scripts/utils/` (todos stubs)
- **Directorios vacíos:**
  - `scripts/embeddings/`
  - `scripts/testing/`
- **Referencias a funcionalidad no implementada:**
  - Ollama como dependencia crítica (ahora es opcional para Fase 2+)
  - Generación automatizada de chunks (futuro)
  - CI/CD workflows (planificados)
  - Sistema de embeddings (Fase 2)

#### Changed
- **Documentación actualizada** para reflejar solo funcionalidad implementada
- **README.md** - Sección "Estado Actual" con funcionalidad real
- **CONTRIBUTING.md** - Flujo manual claro, sin referencias a automatización no implementada
- **ROADMAP.md** - Fase 2 reorganizada con tareas realistas
- **INSTALLATION.md** - Ollama opcional, enfoque en herramientas core
- **setup.sh** - Removidas validaciones de Ollama
- **.env.example** - Variables comentadas para features futuros

#### Rationale
Limpieza para tener una base sólida y honesta:
- Solo documentar lo que realmente funciona
- Evitar confusión en nuevos contribuidores
- Enfoque claro: PDF→MD es lo único crítico ahora
- Features futuras claramente marcadas como "Fase 2+"

---

### 🔧 Reorganización Mayor - 2025-11-03

#### Added
- **Estructura de scripts reorganizada por función:**
  - `scripts/conversion/` - Herramientas PDF→Markdown (PRIORIDAD #1)
  - `scripts/chunking/` - Generación y validación de chunks
  - `scripts/embeddings/` - Vectorización y embeddings
  - `scripts/testing/` - Pruebas RAG y calidad
- **Documentación multiplataforma:**
  - `INSTALLATION.md` - Guía completa macOS/Windows
  - `docs/DOMAIN_KNOWLEDGE.md` - Taxonomía de vermicompostaje doméstico
  - READMEs en cada subdirectorio de scripts
- **Configuración:**
  - `.env.example` - Template completo con todas las variables
  - `setup.sh` - Script automatizado de instalación (macOS/Linux)
- **Contexto del proyecto:**
  - Integración del dominio VermiKhipu en documentación
  - Cobertura objetivo por categoría (BIO/PROC/MAT/OPER/PROD)

#### Changed
- **README.md** - Reescrito con enfoque en:
  - Filosofía BYOS clara desde el inicio
  - Prioridad explícita en conversión PDF→MD
  - Quickstart actualizado con estructura nueva
  - Contexto de VermiKhipu y taxonomía de dominio
- **CONTRIBUTING.md** - Flujo completo actualizado:
  - 5 fases detalladas (Conversión → Generación → Validación → PR → CI)
  - Énfasis en PDF→MD como paso crítico
  - Checklist pre-PR exhaustivo
- **ROADMAP.md** - Sustituido con versión detallada que contempla:
  - Herramientas de conversión PDF→MD con fidelidad
  - 4 fases claramente definidas (Fase 0 → Fase 4)
  - Checkboxes de progreso
- **docs/ROADMAP_DETALLADO.md** - Depurado, ahora es índice ligero
- **.gitignore** - Reforzado con:
  - Secciones organizadas por tipo
  - Protección exhaustiva de fuentes con copyright
  - Exclusión de modelos y cache

#### Moved
- `scripts/convert_pdf_local.py` → `scripts/conversion/`
- `scripts/validate_chunks.py` → `scripts/chunking/`
- `scripts/merge_redundant.py` → `scripts/chunking/`
- `scripts/compute_embeddings.py` → `scripts/embeddings/`
- `scripts/test_retrieval.py` → `scripts/testing/`

#### Rationale
Esta reorganización responde a:
1. **Prioridad clara:** Sistema PDF→MD es el fundamento del flujo BYOS
2. **Organización lógica:** Scripts agrupados por función facilitan navegación
3. **Escalabilidad:** Estructura permite crecer sin desorden
4. **Contexto específico:** Dataset enfocado en vermicompostaje doméstico
5. **Instalación simplificada:** Soporte multiplataforma con automatización

---

## [0.1.0] - 2025-11-XX (Próximo Release)

### MVP Inicial
- Dataset base con 150-200 chunks
- Cobertura 70% de taxonomía
- Sistema PDF→MD validado
- Pipeline CI/CD funcional

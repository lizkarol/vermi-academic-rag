# Roadmap Detallado del Proyecto: Vermi-Academic-RAG

**Versión:** 1.0  
**Fecha:** 03 de Noviembre de 2025  
**Filosofía:** "Proporcionar el motor, no la gasolina."

---

## Visión General

Este documento presenta el plan de implementación estratégico y táctico para el desarrollo y crecimiento del repositorio `vermi-academic-rag`. El proyecto se concibe como un **Kit de Herramientas RAG (Retrieval-Augmented Generation)**, proporcionando a la comunidad las herramientas ("el motor") para procesar sus propias fuentes de conocimiento ("la gasolina") de manera segura y eficiente.

El roadmap se divide en fases, cada una con objetivos claros, tareas específicas y entregables medibles.

---

### **Fase 0: Consolidación y Preparación del "Motor" (Finales Q4 2025)**

**Objetivo Principal:** Asegurar que el repositorio esté perfectamente alineado con la filosofía BYOS y que las herramientas base estén robustas y listas para el primer ciclo de ingesta.

*   **Hitos y Tareas Clave:**
    *   [x] **Implementar el "Motor" de Conversión:** Crear y validar el script `scripts/convert_pdf_local.py` para la conversión local de PDF a Markdown.
    *   [x] **Alinear Dependencias:** Actualizar `scripts/requirements.txt` para incluir todas las herramientas necesarias (`marker-sdk`, `torch`, etc.).
    *   [x] **Reforzar `.gitignore`:** Garantizar que todos los artefactos locales (PDFs, `markdown_outputs`) sean ignorados por Git.
    *   [x] **Alinear Documentación Principal:** Actualizar `README.md`, `CONTRIBUTING.md`, y `docs/WORKFLOW.md` para reflejar el flujo de trabajo centrado en el usuario local.
    *   [ ] **Commit de Consolidación:** Realizar un commit que agrupe todas estas mejoras bajo un mensaje claro como "refactor: Consolidate BYOS architecture and local tooling".

*   **Entregable:** Un repositorio que funciona como un "Kit de Herramientas RAG" autocontenido, con documentación clara y herramientas listas para ser utilizadas por cualquier contribuidor.
*   **Criterio de Éxito:** Un nuevo usuario puede clonar el repositorio, instalar las dependencias y entender el flujo de trabajo completo leyendo la documentación principal.

---

### **Fase 1: MVP - Primer Ciclo de Ingesta Controlado (Finales Q4 2025)**

**Objetivo Principal:** Validar de principio a fin el pipeline de ingesta local y validación automática con un único documento, sirviendo como el "Hello, World!" del proyecto.

*   **Hitos y Tareas Clave:**
    1.  **Selección de Fuente:** Elegir un primer PDF académico representativo (con texto, tablas, citas).
    2.  **Configuración del Entorno:** El usuario ejecuta `pip install -r scripts/requirements.txt`.
    3.  **Ejecución del "Motor" (PDF → MD):**
        *   El usuario ejecuta `python scripts/convert_pdf_local.py "ruta/al/pdf.pdf"`.
        *   Se verifica la calidad del `.md` generado en `sources/markdown_outputs/`.
    4.  **Generación de Chunks (LLM):**
        *   El usuario sigue la guía de `scripts/generate_cards_local.md` para generar los chunks JSON.
        *   **Revisión Manual Crítica:** Se validan los primeros chunks para asegurar que el LLM sigue el esquema y el parafraseo es de calidad.
    5.  **Validación Local (Pre-Commit):**
        *   El usuario ejecuta `python scripts/validate_chunks.py --mode schema` para obtener feedback inmediato.
    6.  **Pull Request y Validación Automática (CI):**
        *   Se abre un PR con los nuevos chunks.
        *   Se observa la ejecución del workflow `validate-dataset.yml` en GitHub Actions.
        *   Se confirma que todas las pruebas automáticas pasan.

*   **Entregable:** Un Pull Request exitoso y fusionado, que contiene los primeros ~10-20 chunks de alta calidad.
*   **Criterio de Éxito:** El ciclo completo (local + CI) se ejecuta sin errores. El workflow de CI demuestra su capacidad para validar correctamente la contribución.

---

### **Fase 2: Expansión y Herramientas Avanzadas (Q1 2026)**

**Objetivo Principal:** Aumentar la base de conocimiento del dataset mientras se desarrollan herramientas de procesamiento automatizado y QA.

*   **Hitos y Tareas Clave:**
    1.  **Ingesta de Más Fuentes:** Repetir el ciclo de la Fase 1 con 5-10 documentos adicionales para alcanzar ~100-150 chunks y cubrir las categorías principales de la taxonomía.
    2.  **Refinamiento del "Motor" de Conversión:**
        *   Mejorar `convert_pdf_local.py` para manejar casos complejos (ej. tablas de múltiples páginas, figuras).
        *   Añadir opciones de línea de comandos para mayor control (ej. `--force-ocr`).
    3.  **Generación Automatizada de Chunks:**
        *   Desarrollar `scripts/chunking/generate_cards.py` para automatizar la generación con LLMs locales.
        *   Integrar con Ollama para procesamiento sin costo de APIs.
    4.  **Sistema de Embeddings:**
        *   Implementar `scripts/embeddings/compute_embeddings.py` para vectorización.
        *   Configurar LanceDB con índices optimizados.
    5.  **QA Avanzado:**
        *   **Validación Semántica:** Mejorar `validate_chunks.py` para incluir chequeos semánticos.
        *   **Detección de Duplicados:** Implementar detección basada en similitud coseno.
        *   **Pruebas RAG:** Desarrollar `scripts/testing/test_retrieval.py`.
    6.  **CI/CD Workflows:**
        *   Implementar `validate-dataset.yml` para validación automática en PRs.
        *   Crear `test-rag.yml` para pruebas de recuperación.
    7.  **Documentación de Hallazgos:**
        *   Crear `docs/LLM_GUIDANCE.md` para documentar mejores prácticas con LLMs.
        *   Documentar casos edge y soluciones en `docs/TROUBLESHOOTING.md`.

*   **Entregable:** Un dataset con ~150 chunks, herramientas automatizadas de generación, y pipeline de CI/CD funcional.
*   **Criterio de Éxito:** El dataset cubre >70% de la taxonomía. Generación de chunks automatizada funciona con calidad ≥ manual.

---

### **Fase 3: Release v1.0 y Apertura a la Comunidad (Q2 2026)**

**Objetivo Principal:** Consolidar el trabajo en una primera versión oficial (`v1.0`) del "Kit de Herramientas RAG", empaquetada y lista para ser utilizada y extendida por la comunidad.

*   **Hitos y Tareas Clave:**
    1.  **Completar Dataset Base:** Alcanzar 200-280 chunks cubriendo 90%+ de la taxonomía.
    2.  **Generación de Embeddings:** Generar vectores para todos los chunks del dataset con `embeddinggemma:300m`.
    3.  **Sistema RAG Funcional:**
        *   LanceDB configurado con índices optimizados (IVF_HNSW_SQ + FTS).
        *   Búsqueda híbrida (vector + keyword) con reranking RRF.
        *   Umbrales de confianza calibrados.
    4.  **Workflows de Release:** Implementar `publish-release.yml` para empaquetar dataset y embeddings automáticamente.
    5.  **Documentación Completa:**
        *   Ejemplos de uso en `docs/examples/` (carga, búsqueda, integración).
        *   Guía de integración con aplicaciones existentes.
        *   API reference si se implementa servicio REST.
    6.  **Creación del Tag `v1.0`:** Release oficial en GitHub.

*   **Entregable:** Release `v1.0` con dataset completo, embeddings, documentación y ejemplos.
*   **Criterio de Éxito:** Un desarrollador externo puede descargar la release e integrarla en su aplicación RAG en menos de 30 minutos.

---

### **Fase 4: Mantenimiento y Crecimiento Sostenido (Continuo 2026+)**

**Objetivo Principal:** Fomentar una comunidad activa, mantener la calidad del dataset y evolucionar las herramientas del "motor" basándose en el feedback y las nuevas tecnologías.

*   **Hitos y Tareas Clave:**
    1.  **Gestión de la Comunidad:**
        *   Establecer una cadencia para revisar y fusionar contribuciones de la comunidad.
        *   Mantener un backlog de fuentes deseadas y mejoras en los `Issues` de GitHub.
    2.  **Ciclo de Releases Menores:** Publicar versiones menores (v1.1, v1.2) a medida que se añaden nuevos lotes de chunks o se mejoran las herramientas.
    3.  **Optimización y Escalabilidad:**
        *   Monitorear el rendimiento de los scripts y optimizarlos.
        *   Evaluar alternativas a los LLMs comerciales (ej. fine-tuning de modelos open-source) para reducir costos y dependencias.
    4.  **Expansión de Funcionalidades (Exploratorio):**
        *   **Soporte Multi-idioma:** Investigar la viabilidad de traducir chunks o incorporar fuentes en otros idiomas.
        *   **Generación Automática de Preguntas:** Crear un script que genere preguntas sintéticas para cada chunk, mejorando el entrenamiento y la evaluación del sistema RAG.
    5.  **Monitoreo de Impacto:** Seguir las métricas de éxito (forks, estrellas, menciones) para medir la adopción y el impacto del proyecto en la comunidad.

*   **Entregable:** Un proyecto vivo, con contribuciones regulares, releases periódicas y una hoja de ruta que se adapta a las necesidades de la comunidad y los avances tecnológicos.
*   **Criterio de Éxito:** El proyecto se convierte en un recurso de referencia en su nicho, con una comunidad activa de usuarios y contribuidores.


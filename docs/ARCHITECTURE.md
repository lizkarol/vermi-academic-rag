# Arquitectura del Proyecto

Este documento describe la arquitectura técnica del proyecto `vermi-academic-rag`, centrado en un sistema RAG (Retrieval-Augmented Generation) con LanceDB.

## Modelo Conceptual

La arquitectura se basa en una ontología de dominio de vermicompostaje doméstico, dividida en cinco categorías principales:
-   **BIOLOGÍA**
-   **PROCESO**
-   **MATERIALES**
-   **OPERACIÓN**
-   **PRODUCTO**

## Flujo de Datos (BYOS)

El sistema opera bajo un modelo **Bring Your Own Sources (BYOS)** para garantizar la legalidad y sostenibilidad del proyecto.

1.  **Fase Local (Privada):**
    *   El usuario obtiene fuentes académicas (PDFs) y las almacena localmente.
    *   Utiliza scripts para convertir PDF a Markdown.
    *   Genera "cards" o chunks en formato JSONL utilizando un LLM (como Gemini o ChatGPT) para parafrasear y estructurar la información según el esquema definido.

2.  **Fase Pública (Repositorio GitHub):**
    *   El usuario sube **únicamente el archivo JSONL** con los chunks parafraseados al repositorio.
    *   Un sistema de Integración Continua (CI) con GitHub Actions se activa automáticamente.

3.  **Fase de CI/CD (GitHub Actions):**
    *   **Validación:** Se ejecutan scripts (`validate_chunks.py`) para verificar la integridad del esquema, la consistencia semántica y la ausencia de duplicados.
    *   **Pruebas RAG:** Se realizan pruebas de recuperación (`test_rag_retrieval.py`) para asegurar que los nuevos chunks son recuperables y relevantes.
    *   **Publicación:** Si las validaciones y pruebas son exitosas, se empaqueta y publica una nueva versión del dataset.

## Stack Tecnológico

-   **Base de Datos Vectorial:** `LanceDB` (versión 0.25.2 o superior) para búsqueda híbrida.
-   **Embeddings:** `embeddinggemma:300m` (300 dimensiones) a través de Ollama.
-   **Búsqueda:** Híbrida, combinando búsqueda vectorial (IVF_HNSW_SQ) y búsqueda de texto completo (FTS) con BM25.
-   **Lenguaje de scripting:** Python 3.11.
-   **CI/CD:** GitHub Actions.


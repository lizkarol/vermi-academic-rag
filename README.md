# Vermi Academic RAG Dataset

![GitHub License](https://img.shields.io/badge/License-MIT-blue.svg)
![BYOS Policy](https://img.shields.io/badge/Content%20Policy-BYOS-important.svg)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/lizkarol/vermi-academic-rag/validate-dataset.yml?branch=main&label=Dataset%20Validation)

Un repositorio público y colaborativo para crear un dataset de Retrieval-Augmented Generation (RAG) de alta calidad, enfocado en papers académicos y construido bajo una estricta política legal-safe.

---

## 🧠 Filosofía: "El Motor, no la Gasolina"

Este proyecto opera bajo un principio fundamental: **proporcionamos las herramientas (el motor), pero no los datos brutos con copyright (la gasolina)**.

Debido a las restricciones de derechos de autor de los papers académicos, no podemos alojar directamente los PDFs ni sus textos extraídos. En su lugar, hemos desarrollado un flujo de trabajo **Bring Your Own Sources (BYOS)** que permite a la comunidad procesar los documentos de forma **local y privada** y contribuir únicamente con los datos estructurados y parafraseados, que no infringen el copyright.

El repositorio te da el "motor":
*   **Scripts de conversión:** Para pasar de PDF a Markdown usando tecnología de punta.
*   **Validadores de datos:** Para asegurar la calidad y consistencia de las contribuciones.
*   **Esquemas y plantillas:** Para generar los datos estructurados de forma estandarizada.

Tú pones la "gasolina": los papers a los que tienes acceso legal.

## 🚀 Quickstart: Cómo Contribuir

Sigue estos pasos para realizar tu primera contribución:

1.  **Fork & Clone:** Haz un fork de este repositorio y clónalo en tu máquina local.
2.  **Configura el Entorno:** Instala todas las dependencias necesarias.
    ```bash
    pip install -r scripts/requirements.txt
    ```
3.  **Procesa tu PDF (Localmente):** Ejecuta el script de conversión apuntando a un paper que tengas en tu disco. El resultado se guardará en una carpeta ignorada por Git (`sources/markdown_outputs`).
    ```bash
    python scripts/convert_pdf_local.py "ruta/a/tu/paper.pdf"
    ```
4.  **Genera los Datos Estructurados:**
    *   Abre el archivo Markdown generado en el paso anterior.
    *   Usa ese contenido junto con la plantilla de prompt en `scripts/generate_cards_local.md` y tu LLM de preferencia (GPT-4, Gemini, etc.) para generar las "fichas" en formato JSONL.
5.  **Añade y Valida tu Contribución:**
    *   Mueve tu archivo `.jsonl` final a la carpeta `dataset/chunks_enriched/`.
    *   Ejecuta el script de validación para asegurarte de que todo está en orden.
    ```bash
    python scripts/validate_chunks.py "dataset/chunks_enriched/tu_archivo.jsonl"
    ```
6.  **Crea un Pull Request:** Haz commit de tu archivo `.jsonl` y envíalo como un Pull Request para que sea revisado e integrado al dataset principal.

## 🗺️ Roadmap del Proyecto

Tenemos un plan detallado para el crecimiento y la evolución de este dataset. Puedes consultarlo en nuestro roadmap oficial:
➡️ **[docs/ROADMAP_DETALLADO.md](docs/ROADMAP_DETALLADO.md)**

## 📜 Licencia y Política de Contenido

*   El **código** de este repositorio está bajo **Licencia MIT**.
*   Las **contribuciones de datos** se rigen por nuestra **[Política BYOS](BYOS_POLICY.md)**, que debes leer y aceptar.

¡Gracias por considerar contribuir a un recurso abierto, legal y de alta calidad para la comunidad de IA!

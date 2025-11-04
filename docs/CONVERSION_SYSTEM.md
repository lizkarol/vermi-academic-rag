# 📚 Sistema Adaptativo de Conversión PDF->Markdown

**Versión:** 2.0 (noviembre 2025)  
**Entornos validados:** macOS M4 (16 GB RAM, backend MPS), Ubuntu 22.04 + NVIDIA RTX 3070 (CUDA 12.1), Windows 11 (CPU/CUDA)  
**Basado en las guías:** `docs/guide/guia-instalacion.md`, `docs/guide/receta-pdf-markdown.md`

---

## Objetivo y filosofía

- Diseñar un sistema robusto que convierta PDFs a Markdown preservando contenido, estructura y contexto.
- Evitar trabajo innecesario: cada tipo de PDF requiere herramientas y costos diferentes.
- Integrar primero soluciones probadas y modelos locales de Ollama, reservando desarrollo custom para los huecos restantes.
- Mantener el flujo BYOS (Bring Your Own Sources): los PDFs originales nunca se suben al repositorio.

### ¿Se cumple el objetivo?

- **Clasificación automática:** `PDFTypeDetector` identifica si el documento es nativo, escaneado o mixto analizando las primeras páginas en <1 s.
- **Estrategias diferenciadas:** se define una ruta optimizada para cada tipo (pdfplumber, marker-pdf + EasyOCR, docling + fallbacks).
- **Integración Ollama:** los modelos locales se usan para validación semántica, ajustes de formato y QA posterior.
- **Resultados actuales:** el sistema opera en los tres entornos descritos, con scripts reproducibles y documentación de soporte.  

> **Conclusión:** el objetivo inicial está cubierto; el documento detalla cómo ejecutar, mantener y mejorar el sistema adaptativo.

### Mejoras recientes
- Conversión nativa ahora replica la “Ruta A” descrita en `docs/guide/receta-pdf-markdown.md`, detectando tamaños de fuente y listas para preservar jerarquías.
- Se incrementa el tracking de estructura (`headings_detected`, `list_items`, `paragraphs`) en `conversion_tracker.db` para auditar fidelidad.
- Documentación alineada con las guías `docs/guide/guia-instalacion.md` y `docs/guide/receta-pdf-markdown.md` para evitar divergencias.

---

## Arquitectura del sistema

El `AdaptivePDFConverter` orquesta todo el proceso, desde la detección hasta el postprocesado.

1. **Detección:** `PDFTypeDetector` inspecciona de 3 a 10 páginas para medir densidad de texto, histogramas de pixeles y metadatos.
2. **Planificación y Conversión:** Basado en el tipo de PDF, el convertidor selecciona y ejecuta la herramienta más adecuada. Los resultados se normalizan y se guarda un reporte en `sources_local/reports/`.
3. **Postprocesado:** Se realiza una limpieza avanzada del Markdown, se verifica la coherencia y se registra la operación en la base de datos SQLite (`conversion_tracker.db`).

### Estrategia adaptativa (resumen)

| Tipo de PDF | Indicadores principales | Herramientas base | Tiempo típico (50 págs) |
|-------------|------------------------|-------------------|--------------------------|
| **Nativo** (texto seleccionable) | Ratio texto/imagen > 0.9, fuentes embebidas | `pdfplumber`, `pdfminer.six` | 5-10 s CPU |
| **Escaneado** (imagen total) | Sin metadatos de texto, OCR = 0, TIFF/JPEG interno | `marker-pdf`, `EasyOCR` (GPU/MPS) | 5-7 min GPU |
| **Mixto** (secciones en imagen) | Texto parcial + figuras rasterizadas | `pdfplumber` (fallback actual) | 30-60 s (estimado) |

---

## Flujos detallados por tipo de PDF

### 1. PDF nativo
- **Detección:** alto conteo de tokens desde `pdfminer` (idéntico a la receta base).
- **Pipeline:** `pdfplumber` en modo estructurado + heurística de fuentes (titulares/listas) → limpieza ligera → validación opcional con Ollama (`qwen2.5:7b`). Referencia: `docs/guide/receta-pdf-markdown.md`, sección “Ruta A: PDF nativo”.
- **Salida:** Markdown por página respetando encabezados jerárquicos y viñetas; tablas convertidas a `|` pipes estándar; registro en SQLite.
- **Beneficio:** preserva formato sin caer en OCR completo, 200x más rápido que aplicar marker a todo el documento.

### 2. PDF escaneado
- **Detección:** ausencia de texto, verificación por histograma y tamaño de archivos embebidos.
- **Pipeline:** `marker-pdf --reconstruct-markdown` con `EasyOCR`/CUDA -> revisión de tablas -> postprocesado con prompts de Ollama para ajustar listas y títulos.
- **Salida:** Markdown + assets en `sources_local/assets/`. Reporte incluye métricas de OCR y confianza media.
- **Notas:** se recomienda GPU; en CPU el tiempo se multiplica x4. Hay bandera `--quality fast` para prototipos.

### 3. PDF mixto
- **Detección:** densidad de texto en torno a 0.4-0.6, imágenes incrustadas detectadas.
- **Pipeline:** **(Pendiente)** Actualmente, se utiliza el pipeline de PDF nativo como fallback. La implementación futura usará `docling` para realizar parsing estructural y ejecutar OCR solo en las páginas marcadas como imagen.
- **Salida:** Markdown con bloques híbridos (texto + imágenes referenciadas). Se genera reporte con páginas OCR y confianza.
- **Notas:** La implementación final requerirá coordinación con `ConversionTracker` para evitar OCR redundante en rondas sucesivas.

---

## Dependencias validadas

| Componente | Versión | Uso principal | Comentario |
|------------|---------|---------------|------------|
| Python | 3.11.x | Base del sistema | Requerido |
| PyTorch | 2.5.1 | GPU/MPS | Evitar builds nightly |
| pdfplumber | 0.11.4 | PDFs nativos | CPU |
| pdfminer.six | 20231228 | Soporte parsing | No usar 20240706 |
| marker-pdf | >=1.0.0 | PDFs escaneados | GPU recomendada |
| EasyOCR | 1.7.1 | Backend OCR | Compatible CUDA/MPS |
| docling | >=2.18.0 | PDFs mixtos | **(Pendiente)** No instalado por defecto |
| lancedb | 0.25.2 | Almacenamiento vectorial RAG | CPU |
| sentence-transformers | >=3.3.0 | Embeddings QA | GPU opcional |

> Revisa `docs/guide/guia-instalacion.md` para dependencias del entorno y `docs/guide/receta-pdf-markdown.md` para comandos completos.

---

## Instalación rápida de PyTorch

```bash
# macOS M4 (MPS)
pip install torch==2.5.1 torchvision==0.20.1

# Ubuntu + RTX 3070 (CUDA 12.1)
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121

# Windows CPU
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu

# Windows GPU NVIDIA
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121
```

Verifica con:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

---

## Uso básico

1. **Conversión individual**
   ```bash
   python scripts/conversion/adaptive_converter.py documento.pdf
   ```
2. **Revisión de reporte**
   ```bash
   cat sources_local/reports/documento_report.json
   ```
3. **Estadísticas históricas**
   ```python
   from scripts.conversion.conversion_db import ConversionTracker
   with ConversionTracker() as tracker:
       print(tracker.get_statistics())
   ```
4. **Batch de documentos**
   ```bash
   # Itera sobre todos los PDFs en un directorio
   for f in ruta/a/tus/pdfs/*.pdf; do python scripts/conversion/adaptive_converter.py "$f"; done
   ```

Flag útil:
- `--force` obliga a reconvertir un PDF ignorando caché.
- `--no-normalize` desactiva la normalización de markdown cuando se busca máximo rendimiento.
- `--profile NOMBRE` aplica un perfil de conversión personalizado (formatos institucionales).
- Los reportes guardados en `sources_local/reports/` incluyen contadores de `headings_detected`, `list_items` y `paragraphs` para auditar la fidelidad estructural.

---

## Integración con Ollama

- Verifica que Ollama esté corriendo:
  ```bash
  ollama list
  ```
- Si no, inicia el servicio:
  ```bash
  ollama serve
  ```
- Modelos sugeridos:
  - `gemma3:12b` para revisión de formato.
  - `qwen2.5:7b` para QA ligero.
- Los prompts se definen en `scripts/conversion/ollama_prompts/`. Ajusta temperatura y top_p según el tipo de documento.

---

## Política BYOS

- No subir al repositorio: PDFs originales, Markdown generados, reportes JSON personales ni bases SQLite con datos sensibles.
- Sí subir: scripts, configuraciones, ejemplos sin datos sensibles y archivos `.jsonl` con chunks parafraseados.
- Directorio `sources_local/` permanece en `.gitignore` para cumplir la política.

---

## Relación con docs/guide

- `docs/guide/receta-pdf-markdown.md`: detalla el playbook operativo (detectores, rutas A/B/C, limpieza con Ollama). El código de `AdaptivePDFConverter` replica esa lógica y añade heurísticas de estructura en la ruta nativa.
- `docs/guide/guia-instalacion.md`: lista versiones exactas, comandos “copy-paste” y troubleshooting preventivo. Esta guía se toma como referencia para validar entornos antes de ejecutar conversiones en cualquiera de los tres dispositivos.
- Mantén ambos documentos como fuente de verdad para instalación y operación. Este archivo solo resume el sistema y los deltas recientes.

---

## Roadmap

- **Fase 1 (completada):** detector de tipo, estrategias principales, tracking SQLite y validación Ollama.
- **Fase 2 (en progreso):** integración completa con docling, batch paralelo, dashboard web ligero.
- **Fase 3 (planificada):** pipeline RAG con chunking avanzado, ingesta automática a LanceDB, consultas interactiva.

---

## Solución de problemas

- **`marker_single` no encontrado:**  
  Instala de nuevo `marker-pdf` sin caché.  
  ```bash
  pip install marker-pdf --no-cache-dir
  ```

- **Ollama no responde:**  
  Revisa el servicio y vuelve a descargar modelos si fue necesario.  
  ```bash
  ollama serve
  ollama pull gemma3:12b
  ```

- **Conversión lenta:**  
  - Desactiva Ollama con `--no-ollama`.  
  - Divide el PDF en capítulos.  
  - Usa `marker-pdf --quality fast` en tareas exploratorias.

- **Duplicados no detectados:**  
  Fuerza reconversión.  
  ```bash
  python scripts/conversion/adaptive_converter.py archivo.pdf --force
  ```

---

## Documentación relacionada

- `scripts/conversion/README.md`: descripción de scripts y módulos.
- `docs/guide/guia-instalacion.md`: preparación de entornos (macOS, Linux, Windows).
- `docs/guide/receta-pdf-markdown.md`: instrucciones detalladas de instalación y uso de cada herramienta.

---

Sistema listo para operar en producción ligera. Ajusta parámetros según el perfil de documentos y mantén los reportes en SQLite para auditar resultados.

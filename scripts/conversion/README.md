# Scripts de Conversión (PDF → Markdown)

Este directorio contiene herramientas para convertir documentos PDF a Markdown con alta fidelidad de contenido.

## Scripts Principales

### `convert_pdf_local.py`
Convierte PDFs académicos a Markdown usando marker-sdk (vision + OCR).

**Uso:**
```bash
python scripts/conversion/convert_pdf_local.py "ruta/al/documento.pdf" --output_dir sources/markdown_outputs
```

**Características:**
- Preserva estructura de tablas y figuras
- OCR para PDFs escaneados
- Detección de ecuaciones matemáticas
- Output limpio y estructurado

**Dependencias:**
- `marker-sdk` (GPU opcional, CPU funcional)
- `torch`
- `Pillow`

## Flujo BYOS (Bring Your Own Sources)

1. **Entrada:** PDF académico (local, NO se sube al repo)
2. **Proceso:** Conversión con fidelidad de contenido
3. **Salida:** Markdown en `sources/markdown_outputs/` (ignorado por Git)
4. **Siguiente paso:** Usar el MD para generar chunks parafraseados

⚠️ **Importante:** Los PDFs y MDs generados permanecen locales. Solo los chunks parafraseados se suben al repositorio.

# Scripts - Vermi Academic RAG

Esta carpeta contiene todas las herramientas para procesar, validar y gestionar el dataset.

---

## 📁 Estructura Organizada

```
scripts/
├── conversion/          # PDF → Markdown (PRIORIDAD #1)
├── chunking/           # Validación de chunks
├── generate_cards_local.md  # Template para generar chunks con LLM
└── requirements.txt    # Dependencias Python
```

---

## 🔧 Scripts por Categoría

### 1. Conversión (PDF → Markdown)

**Directorio:** `conversion/`

| Script | Propósito | Uso |
|--------|-----------|-----|
| `convert_pdf_local.py` | Convierte PDF a MD con alta fidelidad | `python scripts/conversion/convert_pdf_local.py paper.pdf` |

**Prioridad:** 🔴 CRÍTICA - Este es el primer paso del flujo BYOS

**Ver:** [`conversion/README.md`](conversion/README.md)

---

### 2. Chunking (Validación)

**Directorio:** `chunking/`

| Herramienta | Propósito | Uso |
|-------------|-----------|-----|
| `validate_chunks.py` | Valida esquema y semántica | `python scripts/chunking/validate_chunks.py --mode schema` |
| `generate_cards_local.md` | Template de prompt para LLMs | Copiar contenido y usar con LLM |

**Prioridad:** 🟡 ALTA - Asegura calidad del dataset

**Ver:** [`chunking/README.md`](chunking/README.md)

---

## 🚀 Flujo de Trabajo Típico

```
1. PDF Local
   ↓
   python scripts/conversion/convert_pdf_local.py paper.pdf
   ↓
2. Markdown (sources/markdown_outputs/)
   ↓
   [Usar LLM con template en generate_cards_local.md]
   ↓
3. Chunks JSONL
   ↓
   python scripts/chunking/validate_chunks.py --mode schema
   ↓
4. Validado ✓
   ↓
5. Contribuir vía Pull Request
   (Mover a dataset/chunks_enriched/)
```

---

## 📦 Dependencias

Todas las dependencias están en `requirements.txt`:

```bash
# Instalar todas las dependencias
pip install -r scripts/requirements.txt
```

**Principales:**
- `marker-pdf`: Conversión PDF→MD
- `torch`: Backend para marker y embeddings
- `lancedb`: Base de datos vectorial
- `ollama`: Cliente para LLMs locales
- `pandas`, `pyarrow`: Manejo de datos
- `pytest`: Testing

---

## 🎯 Desarrollo Futuro

Scripts planificados para futuras versiones:

- [ ] `chunking/generate_cards.py` - Generación automatizada con LLM
- [ ] `conversion/batch_convert.py` - Procesar múltiples PDFs en lote
- [ ] `embeddings/compute_embeddings.py` - Vectorización con Ollama
- [ ] `testing/test_retrieval.py` - Pruebas RAG automáticas
- [ ] `utils/` - Utilidades compartidas (JSONL, cleaning, etc.)

---

## 📚 Documentación Adicional

- **Instalación:** Ver [`../INSTALLATION.md`](../INSTALLATION.md)
- **Contribución:** Ver [`../CONTRIBUTING.md`](../CONTRIBUTING.md)
- **Esquema de datos:** Ver [`../docs/DATA_SCHEMA.md`](../docs/DATA_SCHEMA.md)
- **Dominio:** Ver [`../docs/DOMAIN_KNOWLEDGE.md`](../docs/DOMAIN_KNOWLEDGE.md)

---

## 💬 Ayuda

Si un script falla:

1. Verifica que el entorno virtual está activado: `source venv/bin/activate`
2. Revisa que las dependencias están instaladas: `pip list`
3. Consulta el README específico del subdirectorio
4. Busca en Issues: https://github.com/lizkarol/vermi-academic-rag/issues

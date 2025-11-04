# Guía de Contribución - Vermi Academic RAG

¡Gracias por tu interés en contribuir! Este proyecto sigue un modelo **BYOS (Bring Your Own Sources)** estricto para cumplir con derechos de autor.

---

## 📜 Política BYOS (Bring Your Own Sources)

**Este repositorio NO aloja PDFs ni Markdown derivados de terceros con copyright.**

### ✅ Qué SÍ puedes aportar:

- **Chunks JSONL parafraseados** (en tus propias palabras, NO copias verbatim)
- **Código Python** (scripts, tests, mejoras)
- **Documentación** (guías, ejemplos, FAQs)
- **Referencias** (DOI/URLs de fuentes, sin los archivos)

### ❌ Qué NO debes aportar:

- PDFs o archivos originales con copyright
- Markdown sin parafrasear (conversión directa)
- Fragmentos verbatim >100 palabras consecutivas
- Contenido sin atribución clara

**Más detalles:** Ver [`BYOS_POLICY.md`](BYOS_POLICY.md)

---

## 🔄 Flujo de Trabajo BYOS Completo

### Fase 1: Conversión Local (PDF → Markdown)

**Objetivo:** Obtener un Markdown de alta fidelidad de tu fuente académica.

```bash
# 1. Asegúrate de tener el entorno configurado
source venv/bin/activate  # macOS/Linux
# .\venv\Scripts\Activate.ps1  # Windows

# 2. Convierte tu PDF (permanece local, NO se sube)
python scripts/conversion/adaptive_converter.py "ruta/a/tu/paper.pdf"

# Salida: sources_local/markdown_outputs/tu_paper.md
```

**Puntos clave:**
- Este paso usa `marker-sdk` para preservar tablas, figuras y ecuaciones
- El MD generado es tu "materia prima" para el siguiente paso
- **Permanece local**: `sources_local/` está en `.gitignore`

### Fase 2: Generación de Chunks (Markdown → JSONL)

**Objetivo:** Convertir el contenido del MD en chunks parafraseados estructurados.

**Proceso Manual con LLM:**

1. **Abre el prompt template:**
   ```bash
   cat scripts/chunking/generate_cards_local.md
   ```

2. **Copia el contenido del Markdown generado** en el Paso 1

3. **Usa tu LLM favorito:**
   - Gemini Pro (recomendado para español)
   - GPT-4 / GPT-4o
   - Claude 3 Opus/Sonnet
   - Llama 3.1 70B (local via Ollama)

4. **Prompt básico:**
   ```
   Actúa como experto en vermicompostaje doméstico. Genera chunks 
   parafraseados (en tus palabras) del siguiente contenido, siguiendo 
   el esquema JSON:

   [Pegar el prompt template completo de generate_cards_local.md]
   [Pegar el contenido del MD generado]
   ```

5. **Guarda la salida:** `chunks_tu_paper.jsonl`

**Salida esperada:** Archivo JSONL con 10-50 chunks según el tamaño del documento.

### Fase 3: Validación Local (Pre-PR)

**Objetivo:** Asegurar que los chunks cumplen el esquema y criterios de calidad.

```bash
# Validación de esquema (obligatoria)
python scripts/chunking/validate_chunks.py \
  --file chunks_tu_paper.jsonl \
  --mode schema

# Validación semántica (opcional pero recomendada)
python scripts/chunking/validate_chunks.py \
  --file chunks_tu_paper.jsonl \
  --mode semantic \
  --sample 0.3

```

**Criterios de calidad mínimos:**
- `confidence_score` ≥ 0.70
- Campos obligatorios completos (ver `docs/DATA_SCHEMA.md`)
- Parafraseo claro (no copia textual)
- Atribución (`source_document`, `citations`)

### Fase 4: Contribución al Repositorio (PR)

**Objetivo:** Integrar tus chunks al dataset principal.

```bash
# 1. Mover el archivo validado al dataset
cp chunks_tu_paper.jsonl dataset/chunks_enriched/

# 2. Crear rama de feature
git checkout -b feature/add-chunks-nombre-descriptivo

# 3. Agregar solo el archivo JSONL
git add dataset/chunks_enriched/chunks_tu_paper.jsonl

# 4. Commit descriptivo
git commit -m "feat: Add chunks from [Título/DOI de la fuente]

- Categoría: [BIO/PROC/MAT/OPER/PROD]
- Número de chunks: [N]
- Fuente: [DOI o URL]
- Reliability: [verified/high/medium/low]"

# 5. Push a tu fork
git push origin feature/add-chunks-nombre-descriptivo

# 6. Abrir Pull Request en GitHub
```

**Descripción del PR debe incluir:**
- Fuente completa (título, autores, año, DOI/URL)
- Categoría(s) cubiertas
- Número de chunks agregados
- Si la fuente es CC-BY u open access (mencionar licencia)

### Fase 5: Revisión Automática (CI/CD)

Una vez abierto el PR, se realizará:

1. **Revisión Manual** (por ahora)
   - Un maintainer verificará campos obligatorios
   - Comprobará que el parafraseo es adecuado
   - Validará atribución y fuentes

**Nota:** Los workflows automáticos de CI/CD (GitHub Actions) están planificados para futuras versiones. Por ahora, la validación es manual después de ejecutar `validate_chunks.py` localmente.

**Si todo está bien:** El maintainer fusionará el PR.
**Si hay problemas:** Recibirás feedback para corregir.

---

## 🎯 Tipos de Contribuciones

### 1. Agregar Nuevas Fuentes (Chunks)

**Prioridad:** ALTA - Necesitamos cubrir las 5 categorías principales.

**Fuentes deseadas:**
- Papers de vermicompostaje doméstico (Eisenia fetida/andrei)
- Manuales técnicos (FAO, INTA, universidades)
- Estudios de parámetros (pH, C:N, humedad, temperatura)
- Guías de materiales orgánicos y restricciones
- Documentos sobre producto final (humus, lixiviados)

**Template de Issue:** Usa [`.github/ISSUE_TEMPLATE/new_source.md`](.github/ISSUE_TEMPLATE/new_source.md)

### 2. Mejorar Chunks Existentes

**Ejemplos:**
- Corregir errores semánticos
- Mejorar parafraseo
- Actualizar `confidence_score` con nueva evidencia
- Documentar conflictos entre fuentes

**Template de Issue:** Usa [`.github/ISSUE_TEMPLATE/dataset_improvement.md`]

### 3. Mejorar Herramientas (Scripts)

**Áreas de mejora:**
- Optimizar `adaptive_converter.py` para casos complejos (tablas multi-página)
- Mejorar validaciones semánticas en `validate_chunks.py`
- Desarrollar script de generación automatizada de chunks
- Implementar sistema de embeddings y búsqueda vectorial

### 4. Documentación

**Áreas que necesitan cobertura:**
- Ejemplos de uso del dataset con LanceDB
- Guía de fine-tuning de LLMs con el dataset
- FAQ sobre el dominio (vermicompostaje)
- Tutoriales en video

---

## 📊 Métricas de Calidad

Antes de abrir un PR, verifica:

### Esquema
- [ ] Todos los campos obligatorios presentes
- [ ] Tipos de datos correctos (string, float, bool, array)
- [ ] Enumeraciones válidas (ver `docs/DATA_SCHEMA.md`)

### Contenido
- [ ] `source_field` parafraseado (NO copia textual)
- [ ] `confidence_score` ≥ 0.70
- [ ] `source_document` es DOI/URL rastreable
- [ ] `citations` incluye referencias completas
- [ ] `keywords` relevantes (max 8)
- [ ] `entities` correctamente identificadas (max 10)

### Cobertura
- [ ] Cubre al menos 1 subcategoría con <70% de cobertura
- [ ] No duplica contenido existente (similitud <0.85)

---

## 🛡️ Checklist Pre-PR

Antes de enviar tu Pull Request:

- [ ] Leí y acepto la política BYOS (`BYOS_POLICY.md`)
- [ ] Mi archivo JSONL pasó `validate_chunks.py --mode schema`
- [ ] Incluí atribución clara en `source_document`
- [ ] Parafr aseé el contenido (no es copia verbatim)
- [ ] NO estoy subiendo PDFs ni Markdowns directos
- [ ] Mi commit message sigue el formato convencional
- [ ] La descripción del PR incluye fuente completa

---

## 🤝 Código de Conducta

- **Respeto:** Trata a otros contribuidores con respeto
- **Colaboración:** Compartimos el mismo objetivo
- **Transparencia:** Documenta fuentes y metodología
- **Calidad sobre cantidad:** Mejor pocos chunks de calidad que muchos deficientes

---

## 💬 ¿Dudas?

- **Consulta la documentación:** [`docs/`](docs/)
- **Revisa Issues existentes:** [GitHub Issues](https://github.com/lizkarol/vermi-academic-rag/issues)
- **Abre una Discussion:** Para preguntas generales
- **Contacta maintainers:** Ver CODEOWNERS

---

¡Gracias por contribuir a un recurso abierto, legal y de alta calidad para la comunidad! 🌱

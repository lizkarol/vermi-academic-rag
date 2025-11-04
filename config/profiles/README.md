# Sistema de Perfiles de Conversión

Sistema basado en JSON para definir perfiles de conversión personalizados sin modificar código.

## 📁 Ubicación

Todos los perfiles están en: `config/profiles/*.json`

## 🎯 Perfiles Disponibles

### Perfiles Genéricos

1. **academic_apa.json** - Papers/tesis académicas estilo APA
2. **medical_vancouver.json** - Documentos médicos estilo Vancouver  
3. **engineering_ieee.json** - Papers técnicos estilo IEEE
4. **book_chapters.json** - Libros con capítulos numerados
5. **legal_documents.json** - Documentos legales con artículos

### Perfiles Institucionales

1. **universidad_de_chile_thesis.json** - Tesis U. de Chile
2. **universidad_tacna_thesis.json** - Tesis U. de Tacna

## 📝 Estructura de un Perfil

```json
{
  "name": "nombre_perfil",
  "description": "Descripción clara",
  "preferred_strategy": null,
  "force_ocr": false,
  "ocr_languages": ["es", "en"],
  "normalization": {
    "name": "nombre_normalizacion",
    "description": "Descripción de normalización",
    "institution": "Nombre de la Institución",
    "document_type": "tesis|paper|book|legal",
    "citation_style": "apa|vancouver|ieee|chicago|harvard|mla",
    "heading_style": "decimal|roman|keyword|mixed",
    "heading_keywords": ["Capítulo", "Parte"],
    "max_heading_level": 6,
    "start_level_offset": 1,
    "page_marker_pattern": null,
    "footer_pattern": null,
    "header_pattern": null,
    "min_chars_for_heading": 3,
    "max_chars_for_heading": 200,
    "uppercase_is_heading": true,
    "detect_bold_as_heading": true,
    "merge_fragmented_lines": true,
    "min_line_length_for_merge": 60,
    "preserve_tables": true,
    "preserve_images": true,
    "extract_image_captions": true,
    "preserve_metadata": false,
    "extract_bibliography": true,
    "llm_validation": false,
    "fidelity_threshold": 0.7,
    "tags": ["tag1", "tag2"]
  },
  "quick_detection": true,
  "enable_gpu": true,
  "batch_size": 1,
  "save_intermediate_files": false,
  "generate_report": true
}
```

## 🔧 Crear un Nuevo Perfil

### Opción 1: Copiar Perfil Existente

```bash
# Copiar un perfil base
cp config/profiles/academic_apa.json config/profiles/mi_universidad_thesis.json

# Editar el JSON
# Cambiar: name, description, institution, tags
```

### Opción 2: Desde Cero

```bash
# Crear archivo
touch config/profiles/nuevo_perfil.json

# Editar con la estructura completa
```

## 🎯 Detección Automática

El sistema detecta automáticamente el perfil basándose en:

1. **Institución** (busca en metadata y primeras páginas)
2. **Tipo de documento** (tesis, paper, libro, legal)
3. **Estilo de citación** (APA, Vancouver, IEEE)

### Prioridad de Selección

```
1. Perfil institucional específico (ej: universidad_tacna_thesis)
   ↓ si no existe
2. Perfil genérico por tipo + estilo (ej: academic_apa para tesis APA)
   ↓ si no se detecta
3. Perfil por estilo de citación (ej: medical_vancouver para Vancouver)
   ↓ fallback
4. academic_apa (genérico por defecto)
```

## 📊 Ejemplo: Universidad Nueva

Para agregar soporte a "Universidad Nacional del Sur":

1. **Crear perfil:**
   ```bash
   cp config/profiles/academic_apa.json \
      config/profiles/universidad_sur_thesis.json
   ```

2. **Editar JSON:**
   ```json
   {
     "name": "universidad_sur_thesis",
     "description": "Tesis de Universidad Nacional del Sur",
     "normalization": {
       "institution": "Universidad Nacional del Sur",
       "tags": ["universidad_sur", "uns", "argentina", "tesis"]
     }
   }
   ```

3. **Agregar patrón de detección** (opcional):
   
   Editar `scripts/conversion/profile_detector.py`:
   ```python
   INSTITUTION_PATTERNS = {
       # ... patrones existentes ...
       "universidad_sur": [
           r"universidad\s+nacional\s+del\s+sur",
           r"uns\b",
       ],
   }
   ```

4. **Probar:**
   ```bash
   python scripts/conversion/adaptive_converter.py tu_tesis.pdf
   ```

## ✅ Validación

Ver perfiles cargados:
```bash
python -c "
from scripts.conversion.conversion_profiles import ProfileManager
manager = ProfileManager()
for name in sorted(manager.list_profiles()):
    print(f'✓ {name}')
"
```

## 🔍 Debugging

Ver qué perfil se detectó:
```bash
python -c "
from pathlib import Path
from scripts.conversion.profile_detector import ProfileDetector
from scripts.conversion.conversion_profiles import ProfileManager

pdf = Path('tu_pdf.pdf')
manager = ProfileManager()
detector = ProfileDetector(manager)
profile, info = detector.detect_profile(pdf)

print(f'Perfil: {profile}')
print(f'Confianza: {info[\"confidence\"]:.0%}')
print(f'Matches: {info[\"matches\"]}')
"
```

## 📚 Referencias

- `scripts/conversion/conversion_profiles.py` - Gestor de perfiles
- `scripts/conversion/profile_detector.py` - Detección automática
- `scripts/conversion/adaptive_converter.py` - Uso de perfiles

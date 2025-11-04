# 🖼️ OCR, Tablas e Imágenes - Roadmap Pendiente

**Fecha**: Noviembre 3, 2025  
**Estado**: ✅ PARCIALMENTE IMPLEMENTADO, EN MEJORA CONTINUA  
**Prioridad**: ALTA

---

## 📊 Contexto Actual

### ✅ Implementado (SCANNED + NATIVE PDFs)
- **Conversión de PDFs Nativos**: Texto seleccionable, preservación de estructura básica (títulos, listas).
- **Conversión de PDFs Escaneados**: Usando `marker-pdf` con `EasyOCR` como backend.
- Normalización multi-formato (6+ estilos)
- Sistema de perfiles personalizables

### ⏳ Pendiente (MIXED PDFs y mejoras)
- **Estrategia para PDFs Mixtos**: Actualmente usan el pipeline de Nativos.
- **Extracción de tablas complejas**: Celdas fusionadas, tablas multi-página.
- **Procesamiento de imágenes con texto**: Detección de gráficos y diagramas.

---

## 🎯 Problemas Específicos a Resolver

### 1. PDFs Escaneados (SCANNED)

#### Problema
```
Input: Libro escaneado (imagen pura)
  - Sin texto seleccionable
  - Puede contener tablas dibujadas
  - Puede tener figuras con texto incrustado
  - Calidad variable del escaneo

Output deseado:
  - Texto extraído vía OCR
  - Tablas reconstruidas en Markdown
  - Imágenes extraídas con captions
  - Referencias a figuras preservadas
```

#### Desafíos
- 🔴 **OCR de calidad**: Requiere modelos robustos (EasyOCR, Tesseract)
- 🔴 **Detección de layout**: Diferenciar texto, tabla, imagen
- 🔴 **Reconstrucción de tablas**: De imagen a estructura Markdown
- 🔴 **Performance**: OCR es lento (~30-60s por página)

### 2. Tablas Complejas

#### Problema
```
Tablas en PDFs pueden ser:
  1. Texto seleccionable (fácil) ✅
  2. Imágenes dentro del PDF (OCR) ⏳
  3. Bordes dibujados (detección compleja) ⏳
  4. Celdas fusionadas (reconstrucción difícil) ⏳
  5. Tablas multi-página (contexto requerido) ⏳
```

#### Casos Comunes

**Caso A: Tabla Simple (Seleccionable)**
```
Input PDF:
| Nombre | Edad | Ciudad |
|--------|------|--------|
| Juan   | 25   | Lima   |
| María  | 30   | Bogotá |

Output Markdown: ✅ FUNCIONA ACTUALMENTE
```

**Caso B: Tabla Escaneada**
```
Input PDF: [IMAGEN DE TABLA]
  ┌─────────┬──────┬─────────┐
  │ Nombre  │ Edad │ Ciudad  │
  ├─────────┼──────┼─────────┤
  │ Juan    │  25  │ Lima    │
  └─────────┴──────┴─────────┘

Output Markdown: ✅ PARCIALMENTE FUNCIONAL (con `marker-pdf`)
```

**Caso C: Tabla Compleja con Fusión de Celdas**
```
Input PDF: [TABLA CON CELDAS FUSIONADAS]
  ┌─────────────────────────┐
  │      Resumen Anual      │
  ├───────────┬─────────────┤
  │  Q1-Q2    │    Q3-Q4    │
  ├─────┬─────┼─────┬───────┤
  │ Ene │ Feb │ Jul │  Ago  │
  └─────┴─────┴─────┴───────┘

Output Markdown: ⏳ REQUIERE TABLE STRUCTURE RECOGNITION
```

### 3. Imágenes con Texto

#### Problema
```
Figuras académicas contienen:
  - Diagramas con etiquetas
  - Gráficos con leyendas
  - Capturas de pantalla con código
  - Fórmulas renderizadas como imagen

Necesario extraer:
  - Caption de la figura
  - Texto dentro de la imagen (OCR)
  - Referencias cruzadas ("ver Figura 3")
```

---

## 🛠️ Stack Tecnológico Propuesto

### Para OCR General

```python
# Opción 1: EasyOCR (Recomendado)
import easyocr
reader = easyocr.Reader(['es', 'en'], gpu=True)
result = reader.readtext('imagen.png')

Ventajas:
  ✅ Soporta GPU (MPS, CUDA)
  ✅ 80+ idiomas
  ✅ Buena precisión
  ❌ Requiere ~500MB de modelos
```

```python
# Opción 2: Tesseract OCR (Alternativa)
import pytesseract
text = pytesseract.image_to_string(image, lang='spa+eng')

Ventajas:
  ✅ Más ligero
  ✅ Open source completo
  ❌ Menor precisión
  ❌ No usa GPU nativamente
```

### Para Detección de Tablas

```python
# Opción 1: table-transformer (Hugging Face)
from transformers import TableTransformerForObjectDetection
model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection")

Ventajas:
  ✅ Estado del arte en detección
  ✅ Detecta bordes y estructura
  ❌ Requiere ~1GB de modelo
  ❌ Complejo de integrar
```

```python
# Opción 2: Camelot (Python)
import camelot
tables = camelot.read_pdf('documento.pdf', pages='all')

Ventajas:
  ✅ Simple de usar
  ✅ Output directo a Markdown/CSV
  ❌ Solo funciona con tablas seleccionables
  ❌ No maneja PDFs escaneados
```

```python
# Opción 3: docling (Ya integrado)
from docling.document_converter import DocumentConverter
converter = DocumentConverter()
result = converter.convert('documento.pdf', table_structure_enabled=True)

Ventajas:
  ✅ Ya tenemos la dependencia
  ✅ Maneja tablas + OCR + layout
  ✅ Detecta automáticamente zonas
  ❌ Versión 2.9.1 puede ser inestable
```

### Para Procesamiento de Imágenes

```python
# Opción 1: PIL + OpenCV
from PIL import Image
import cv2

# Preprocesamiento para mejorar OCR
image = cv2.imread('figura.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

Ventajas:
  ✅ Control fino de preprocesamiento
  ✅ Mejora calidad de OCR
  ❌ Requiere expertise en visión computacional
```

---

## 📋 Implementación Propuesta

### Fase 1: SCANNED PDFs Básico (✅ Completada)

#### 1.1 Instalación
```bash
pip install marker-pdf==0.2.17
pip install easyocr==1.7.1
pip install opencv-python==4.8.1
```

#### 1.2 Implementación en `adaptive_converter.py`
```python
def _convert_scanned(self, pdf_path: Path) -> str:
    """
    Convierte PDF escaneado usando marker-pdf + EasyOCR.
    
    Pipeline:
    1. marker-pdf detecta layout (texto, tablas, imágenes)
    2. EasyOCR procesa zonas de texto con GPU
    3. Reconstruye markdown preservando estructura
    """
    logger.info("🔍 [SCANNED] Iniciando OCR completo")
    
    try:
        from marker.converters.pdf import PdfConverter
        from marker.models import create_model_dict
        import easyocr
        
        # Inicializar OCR con GPU
        device = 'mps' if self.hardware.device == 'mps' else 'cuda'
        reader = easyocr.Reader(
            ['es', 'en'],
            gpu=True,
            model_storage_directory='.cache/easyocr'
        )
        
        # Convertir con marker-pdf
        converter = PdfConverter()
        result = converter(
            str(pdf_path),
            ocr_model=reader,
            extract_tables=True,
            extract_images=True
        )
        
        markdown = result.markdown
        
        logger.info(f"✅ [SCANNED] OCR completado")
        return markdown
        
    except Exception as e:
        logger.error(f"❌ Error en OCR: {e}")
        raise
```

#### 1.3 Tests
```python
def test_scanned_pdf():
    converter = AdaptivePDFConverter()
    result = converter.convert_single("tests/fixtures/libro_escaneado.pdf")
    
    assert result['pdf_type'] == 'scanned'
    assert result['fidelity'] > 60  # Mínimo aceptable para OCR
    assert len(result['markdown']) > 1000
```

### Fase 2: Tablas Complejas (6-10 horas)

#### 2.1 Instalación
```bash
pip install table-transformer
pip install camelot-py[cv]==0.11.0
```

#### 2.2 Estrategia Multi-Nivel
```python
def _extract_tables(self, pdf_path: Path, pdf_type: PDFType) -> List[Dict]:
    """
    Extrae tablas con estrategia adaptativa.
    
    Estrategia:
    1. Si NATIVE: Camelot (texto seleccionable)
    2. Si SCANNED: table-transformer + OCR
    3. Si MIXED: Combinar ambas
    """
    tables = []
    
    if pdf_type == PDFType.NATIVE:
        # Estrategia rápida: texto seleccionable
        import camelot
        tables = camelot.read_pdf(str(pdf_path), pages='all')
        
    elif pdf_type == PDFType.SCANNED:
        # Estrategia compleja: detección + OCR
        from transformers import TableTransformerForObjectDetection
        model = TableTransformerForObjectDetection.from_pretrained(
            "microsoft/table-transformer-detection"
        )
        # Detectar tablas en imágenes
        # OCR de cada celda detectada
        # Reconstruir estructura
        
    return [self._table_to_markdown(t) for t in tables]

def _table_to_markdown(self, table) -> str:
    """Convierte tabla detectada a Markdown."""
    # Implementar conversión
    pass
```

### Fase 3: Imágenes con Texto (4-6 horas)

#### 3.1 Detección de Figuras
```python
def _extract_images(self, pdf_path: Path) -> List[Dict]:
    """
    Extrae imágenes y sus captions.
    
    Returns:
        Lista de: {
            'image_path': Path,
            'caption': str,
            'figure_number': int,
            'extracted_text': str (OCR)
        }
    """
    import pdfplumber
    
    images = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            for img in page.images:
                # Extraer imagen
                # Buscar caption cercano
                # Aplicar OCR si contiene texto
                images.append({
                    'image_path': self._save_image(img),
                    'caption': self._find_caption(page, img),
                    'figure_number': len(images) + 1,
                    'extracted_text': self._ocr_image(img)
                })
    
    return images
```

---

## 📊 Performance Esperado

### SCANNED PDFs

| Componente | Tiempo | Notas |
|------------|--------|-------|
| Detección layout | 1-2s/página | marker-pdf |
| OCR por página | 10-30s | Depende de GPU |
| Reconstrucción | 1-2s | Post-procesamiento |
| **Total** | **12-34s/página** | Con GPU optimizado |

**Para documento de 50 páginas**:
- Sin GPU (CPU): ~60-90 minutos 🐌
- Con GPU (MPS/CUDA): ~10-25 minutos ⚡

### Tablas

| Tipo | Tiempo | Precisión |
|------|--------|-----------|
| Simple (texto) | <1s | 95-98% |
| Escaneada | 5-15s | 70-85% |
| Compleja (fusión) | 10-30s | 60-75% |

### Imágenes

| Operación | Tiempo | Notas |
|-----------|--------|-------|
| Extracción | <1s | Rápido |
| Caption detection | 1-2s | Búsqueda de texto |
| OCR de imagen | 3-10s | Si contiene texto |

---

### ✅ Checklist de Implementación

### SCANNED PDFs
- [x] Instalar marker-pdf + easyocr
- [x] Implementar `_convert_scanned()`
- [ ] Descargar modelos OCR (~500MB)
- [ ] Tests con PDFs escaneados reales
- [ ] Optimización de GPU (MPS/CUDA)
- [x] Documentación de uso
- [x] Integración con sistema de perfiles

### Tablas
- [ ] Instalar camelot + table-transformer
- [ ] Implementar `_extract_tables()`
- [ ] Estrategia multi-nivel (NATIVE/SCANNED/MIXED)
- [ ] Conversión a Markdown
- [ ] Manejo de celdas fusionadas
- [ ] Tests con tablas complejas
- [ ] Integración con pipeline principal

### Imágenes
- [ ] Implementar `_extract_images()`
- [ ] Detección de captions
- [ ] OCR selectivo de figuras
- [ ] Referencias cruzadas (Figura X)
- [ ] Guardar imágenes extraídas
- [ ] Tests con documentos con figuras
- [ ] Documentación

---

## 🎯 Priorización

### Alta Prioridad (Implementar Primero)
1. **SCANNED PDFs básico** - Mayor impacto para archivos históricos
2. **Tablas simples (NATIVE)** - Caso común y relativamente fácil

### Media Prioridad
3. **Tablas escaneadas** - Más complejo pero necesario
4. **Extracción de imágenes** - Mejora fidelidad general

### Baja Prioridad (Mejoras Futuras)
5. Tablas con fusión compleja
6. OCR de fórmulas matemáticas
7. Detección de diagramas técnicos

---

## 🚧 Limitaciones Conocidas

### Hardware
- OCR requiere GPU para ser práctico
- CPU-only: ~60-90 min por documento (no viable)
- Recomendado: Apple M1+ o NVIDIA RTX 3060+

### Precisión
- OCR de calidad depende de:
  - Resolución del escaneo (mínimo 300 DPI)
  - Calidad de la imagen (contraste, claridad)
  - Idioma y fuente del texto
- Expectativa realista: 70-90% fidelidad en SCANNED

### Casos Difíciles
- ❌ Escritura manuscrita (muy baja precisión)
- ❌ Tablas con formato muy complejo
- ❌ Imágenes de baja resolución
- ❌ PDFs con protección DRM

---

## 💡 Recomendaciones

### Para Usuarios

**Si tienes PDFs escaneados**:
1. Verifica que tengan buena resolución (≥300 DPI)
2. Considera re-escanear si calidad es mala
3. Usa GPU si es posible (MPS/CUDA)
4. Ten expectativas realistas (70-85% fidelidad)

**Si tienes tablas complejas**:
1. PDFs nativos preservan mejor las tablas
2. Considera exportar tablas por separado si críticas
3. Valida manualmente tablas importantes

**Si tienes imágenes con texto**:
1. OCR funciona mejor con texto grande y claro
2. Figuras pequeñas pueden tener baja precisión
3. Considera mantener referencias visuales

### Para Desarrolladores

**Implementación incremental**:
1. Empezar con SCANNED básico (marker-pdf + easyocr)
2. Validar con 2-3 PDFs reales antes de escalar
3. Ajustar umbrales según resultados
4. Documentar casos problemáticos

**Performance**:
1. Cachear modelos OCR (no recargar cada vez)
2. Procesar por lotes si múltiples PDFs
3. Considerar procesamiento paralelo por página
4. Monitorear uso de memoria (modelos grandes)

---

## 📚 Referencias

### Papers y Recursos
- **LayoutParser**: A Unified Toolkit for Deep Learning Based Document Image Analysis
- **TableBank**: Table Benchmark for Image-based Table Detection and Recognition
- **EasyOCR**: https://github.com/JaidedAI/EasyOCR
- **Marker-PDF**: https://github.com/VikParuchuri/marker
- **Camelot**: https://camelot-py.readthedocs.io/

### Modelos Recomendados
- **OCR**: easyocr (multi-idioma, GPU)
- **Tablas**: microsoft/table-transformer-detection
- **Layout**: layoutlmv3-base

---

**Conclusión**: La implementación de OCR y tablas es compleja pero factible con el hardware disponible (Mac M4 MPS). Se recomienda implementación incremental empezando por SCANNED básico.

---

**Autor**: VermiKhipu Academic RAG Team  
**Fecha**: Noviembre 3, 2025  
**Estado**: Documento de planificación

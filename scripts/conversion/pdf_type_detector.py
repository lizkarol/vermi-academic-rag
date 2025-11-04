"""
Detector de Tipo de PDF - Sistema Adaptativo de Conversión

Basado en: guia-instalacion.md + receta-pdf-markdown.md
Autor: VermiKhipu Academic RAG
Fecha: Noviembre 2025

Clasifica PDFs en 3 categorías para aplicar estrategia óptima:
1. NATIVE: Texto seleccionable (pdfplumber)
2. SCANNED: Imagen pura (marker-pdf + EasyOCR + GPU)
3. MIXED: Híbrido (docling con detección automática)
"""

import logging
from pathlib import Path
from enum import Enum
from typing import Tuple, Dict, Any

try:
    import pdfplumber
except ImportError:
    raise ImportError(
        "pdfplumber no instalado. Ejecutar: pip install pdfplumber==0.11.4"
    )

logger = logging.getLogger(__name__)


class PDFType(Enum):
    """Tipos de PDF según contenido."""
    NATIVE = "native"      # Texto seleccionable (95%+ de caracteres)
    SCANNED = "scanned"    # Imagen pura (< 50 caracteres extraíbles)
    MIXED = "mixed"        # Híbrido (parcialmente seleccionable)
    UNKNOWN = "unknown"    # No se pudo determinar


class PDFTypeDetector:
    """
    Detector inteligente de tipo de PDF.
    
    Estrategia:
    1. Intentar extraer texto con pdfplumber (rápido)
    2. Analizar densidad de caracteres por página
    3. Clasificar según umbrales empíricos
    
    Umbrales (basados en testing empírico):
    - NATIVE: ≥ 95% páginas con > 100 caracteres
    - SCANNED: ≥ 80% páginas con < 50 caracteres
    - MIXED: Todo lo demás
    """
    
    # Umbrales de clasificación (ajustables según corpus)
    MIN_CHARS_NATIVE = 100      # Caracteres mínimos para considerar "con texto"
    MAX_CHARS_SCANNED = 50      # Caracteres máximos para considerar "escaneado"
    NATIVE_THRESHOLD = 0.95     # % páginas con texto para ser NATIVE
    SCANNED_THRESHOLD = 0.80    # % páginas sin texto para ser SCANNED
    
    # Límite de páginas a analizar (performance)
    MAX_PAGES_SAMPLE = 10       # Analizar primeras N páginas
    
    def __init__(self):
        """Inicializa el detector."""
        self.stats: Dict[str, Any] = {}
    
    def detect(self, pdf_path: Path, quick: bool = False) -> Tuple[PDFType, Dict[str, Any]]:
        """
        Detecta el tipo de PDF.
        
        Args:
            pdf_path: Ruta al archivo PDF
            quick: Si True, analiza solo primeras 3 páginas (más rápido)
        
        Returns:
            Tuple con (tipo_pdf, estadísticas)
            
        Ejemplo:
            >>> detector = PDFTypeDetector()
            >>> pdf_type, stats = detector.detect(Path("paper.pdf"))
            >>> print(f"Tipo: {pdf_type.value}")
            >>> print(f"Páginas analizadas: {stats['pages_analyzed']}")
        """
        if not pdf_path.exists():
            logger.error(f"❌ PDF no encontrado: {pdf_path}")
            return PDFType.UNKNOWN, {"error": "file_not_found"}
        
        try:
            logger.info(f"🔍 Analizando tipo de PDF: {pdf_path.name}")
            
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                pages_to_analyze = min(
                    3 if quick else self.MAX_PAGES_SAMPLE,
                    total_pages
                )
                
                # Estadísticas por página
                page_stats = []
                
                for i in range(pages_to_analyze):
                    page = pdf.pages[i]
                    text = page.extract_text() or ""
                    char_count = len(text.strip())
                    
                    page_stats.append({
                        "page": i + 1,
                        "chars": char_count,
                        "has_text": char_count > self.MIN_CHARS_NATIVE,
                        "is_empty": char_count < self.MAX_CHARS_SCANNED
                    })
                
                # Calcular métricas
                pages_with_text = sum(1 for p in page_stats if p["has_text"])
                pages_empty = sum(1 for p in page_stats if p["is_empty"])
                
                ratio_with_text = pages_with_text / pages_to_analyze
                ratio_empty = pages_empty / pages_to_analyze
                
                # Clasificar según umbrales
                if ratio_with_text >= self.NATIVE_THRESHOLD:
                    pdf_type = PDFType.NATIVE
                    strategy = "pdfplumber (rápido, alta fidelidad)"
                elif ratio_empty >= self.SCANNED_THRESHOLD:
                    pdf_type = PDFType.SCANNED
                    strategy = "marker-pdf + EasyOCR + GPU (lento, OCR completo)"
                else:
                    pdf_type = PDFType.MIXED
                    strategy = "docling (detección automática)"
                
                # Preparar estadísticas
                self.stats = {
                    "pdf_type": pdf_type.value,
                    "total_pages": total_pages,
                    "pages_analyzed": pages_to_analyze,
                    "pages_with_text": pages_with_text,
                    "pages_empty": pages_empty,
                    "ratio_with_text": round(ratio_with_text, 3),
                    "ratio_empty": round(ratio_empty, 3),
                    "recommended_strategy": strategy,
                    "page_details": page_stats
                }
                
                logger.info(f"✅ Tipo detectado: {pdf_type.value.upper()} "
                           f"({ratio_with_text:.1%} con texto)")
                logger.info(f"📋 Estrategia: {strategy}")
                
                return pdf_type, self.stats
        
        except Exception as e:
            logger.error(f"❌ Error detectando tipo: {e}")
            return PDFType.UNKNOWN, {"error": str(e)}
    
    def is_native(self, pdf_path: Path, quick: bool = True) -> bool:
        """Verifica si PDF es nativo (shortcut)."""
        pdf_type, _ = self.detect(pdf_path, quick=quick)
        return pdf_type == PDFType.NATIVE
    
    def is_scanned(self, pdf_path: Path, quick: bool = True) -> bool:
        """Verifica si PDF es escaneado (shortcut)."""
        pdf_type, _ = self.detect(pdf_path, quick=quick)
        return pdf_type == PDFType.SCANNED
    
    def is_mixed(self, pdf_path: Path, quick: bool = True) -> bool:
        """Verifica si PDF es mixto (shortcut)."""
        pdf_type, _ = self.detect(pdf_path, quick=quick)
        return pdf_type == PDFType.MIXED
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de última detección."""
        return self.stats


# ========== CLI para testing ==========
if __name__ == "__main__":
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    if len(sys.argv) < 2:
        print("Uso: python pdf_type_detector.py <archivo.pdf>")
        print("Ejemplo: python pdf_type_detector.py ../../sources/originals/paper.pdf")
        sys.exit(1)
    
    pdf_path = Path(sys.argv[1])
    detector = PDFTypeDetector()
    pdf_type, stats = detector.detect(pdf_path)
    
    print("\n" + "="*60)
    print("📊 ANÁLISIS DE TIPO DE PDF")
    print("="*60)
    print(f"Archivo: {pdf_path.name}")
    print(f"Tipo: {pdf_type.value.upper()}")
    print(f"Páginas totales: {stats.get('total_pages', 'N/A')}")
    print(f"Páginas analizadas: {stats.get('pages_analyzed', 'N/A')}")
    print(f"Páginas con texto: {stats.get('pages_with_text', 'N/A')}")
    print(f"Páginas vacías: {stats.get('pages_empty', 'N/A')}")
    print(f"Ratio texto: {stats.get('ratio_with_text', 0):.1%}")
    print(f"Estrategia: {stats.get('recommended_strategy', 'N/A')}")
    print("="*60)
    
    # Detalle por página
    if stats.get('page_details'):
        print("\n📄 Detalle por página:")
        for page in stats['page_details']:
            status = "✅ TEXTO" if page['has_text'] else ("❌ VACÍA" if page['is_empty'] else "⚠️  POCO TEXTO")
            print(f"  Página {page['page']}: {page['chars']} caracteres - {status}")
        print()

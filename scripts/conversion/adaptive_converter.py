"""
Convertidor Adaptativo PDF→Markdown - Sistema Inteligente

Basado en: guia-instalacion.md + receta-pdf-markdown.md
Autor: VermiKhipu Academic RAG
Fecha: Noviembre 2025

Estrategia adaptativa según tipo de PDF:
1. NATIVE (texto seleccionable): pdfplumber → Markdown (rápido, ~5-10s)
2. SCANNED (imagen pura): marker-pdf + EasyOCR + GPU (lento, ~5-7min)
3. MIXED (híbrido): docling con detección automática (medio, ~30-60s)

Hardware soportado:
- RTX 3070 (CUDA 12.1) - Performance óptimo
- Mac M4 (MPS) - Aceleración Apple Silicon
- CPU fallback - Sin GPU

Validación opcional: Ollama gemma3:12b (local, BYOS compliant)
"""

import logging
import time
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import json

# Agregar directorio padre al path para imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from pdf_type_detector import PDFTypeDetector, PDFType
from conversion_db import ConversionTracker

# Lazy imports (solo cargar lo necesario)
_pdfplumber = None
_marker = None
_docling = None
_torch = None

logger = logging.getLogger(__name__)


def _import_pdfplumber():
    """Lazy import de pdfplumber."""
    global _pdfplumber
    if _pdfplumber is None:
        try:
            import pdfplumber
            _pdfplumber = pdfplumber
        except ImportError:
            raise ImportError(
                "pdfplumber no instalado. Ejecutar: pip install pdfplumber==0.11.4"
            )
    return _pdfplumber


def _import_marker():
    """Lazy import de marker-pdf."""
    global _marker
    if _marker is None:
        try:
            from marker.converters.pdf import PdfConverter
            from marker.models import create_model_dict
            from marker.output import text_from_rendered
            
            _marker = {
                'PdfConverter': PdfConverter,
                'create_model_dict': create_model_dict,
                'text_from_rendered': text_from_rendered
            }
        except ImportError:
            raise ImportError(
                "marker-pdf no instalado. Ejecutar:\n"
                "pip install marker-pdf>=1.0.0\n"
                "O desde git: pip install 'git+https://github.com/datalab-to/marker.git'"
            )
    return _marker


def _import_docling():
    """Lazy import de docling."""
    global _docling
    if _docling is None:
        try:
            import docling
            _docling = docling
        except ImportError:
            raise ImportError(
                "docling no instalado. Ejecutar: pip install docling>=2.18.0"
            )
    return _docling


def _import_torch():
    """Lazy import de torch."""
    global _torch
    if _torch is None:
        try:
            import torch
            _torch = torch
        except ImportError:
            raise ImportError(
                "PyTorch no instalado. Ver instrucciones en requirements.txt"
            )
    return _torch


class HardwareConfig:
    """Configuración de hardware detectado."""
    
    def __init__(self):
        """Detecta hardware disponible."""
        torch = _import_torch()
        
        # Detectar device
        if torch.cuda.is_available():
            self.device = "cuda"
            self.device_name = torch.cuda.get_device_name(0)
            self.device_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)  # GB
        elif torch.backends.mps.is_available():
            self.device = "mps"
            self.device_name = "Apple Silicon (MPS)"
            self.device_memory = None  # MPS no expone memoria directamente
        else:
            self.device = "cpu"
            self.device_name = "CPU"
            self.device_memory = None
        
        # Configurar workers según hardware
        if self.device == "cuda":
            self.workers = 4  # RTX 3070 puede manejar 4 workers
            self.batch_size = 8
        elif self.device == "mps":
            self.workers = 2  # M4 más conservador
            self.batch_size = 4
        else:
            self.workers = 1
            self.batch_size = 1
        
        logger.info(f"🖥️  Hardware: {self.device_name} ({self.device.upper()})")
        if self.device_memory:
            logger.info(f"💾 VRAM: {self.device_memory:.1f} GB")
    
    def __repr__(self):
        return f"<HardwareConfig device={self.device} workers={self.workers}>"


class AdaptivePDFConverter:
    """
    Convertidor adaptativo de PDF a Markdown.
    
    Selecciona automáticamente la mejor estrategia según tipo de PDF:
    - NATIVE: pdfplumber (rápido)
    - SCANNED: marker-pdf + EasyOCR (preciso)
    - MIXED: docling (balanceado)
    
    Ejemplo:
        >>> converter = AdaptivePDFConverter(sources_local_dir="sources_local")
        >>> result = converter.convert_single("paper.pdf")
        >>> print(f"Markdown: {result['markdown_path']}")
    """
    
    def __init__(
        self,
        sources_local_dir: str = "sources_local",
        use_ollama: bool = False,
        ollama_url: str = "http://localhost:11434",
        ollama_model: str = "gemma3:12b",
        force_strategy: Optional[str] = None
    ):
        """
        Inicializa el convertidor.
        
        Args:
            sources_local_dir: Directorio base para fuentes locales
            use_ollama: Activar validación con Ollama
            ollama_url: URL del servidor Ollama
            ollama_model: Modelo LLM a usar
            force_strategy: Forzar estrategia ("native", "scanned", "mixed")
        """
        # Resolver path absoluto desde raíz del proyecto
        if not Path(sources_local_dir).is_absolute():
            # Si es relativo, asumir que es desde la raíz del proyecto
            project_root = Path(__file__).parent.parent.parent
            self.sources_dir = project_root / sources_local_dir
        else:
            self.sources_dir = Path(sources_local_dir)
        
        self.originals_dir = self.sources_dir / "originals"
        self.converted_dir = self.sources_dir / "converted"
        self.metadata_dir = self.sources_dir / "metadata"
        self.reports_dir = self.sources_dir / "reports"
        
        # Crear directorios si no existen
        for dir_path in [self.originals_dir, self.converted_dir, 
                         self.metadata_dir, self.reports_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Inicializar tracker
        self.tracker = ConversionTracker(str(self.metadata_dir))
        
        # Inicializar detector de tipo
        self.detector = PDFTypeDetector()
        
        # Configurar hardware
        self.hardware = HardwareConfig()
        
        # Ollama (opcional)
        self.use_ollama = use_ollama
        self.ollama_url = ollama_url
        self.ollama_model = ollama_model
        
        if self.use_ollama:
            if not self._check_ollama():
                logger.warning("⚠️  Ollama no disponible, desactivando validación LLM")
                self.use_ollama = False
        
        # Forzar estrategia (debug)
        self.force_strategy = force_strategy
        if force_strategy:
            logger.warning(f"⚠️  Estrategia forzada: {force_strategy}")
        
        logger.info(f"✅ Convertidor inicializado")
        logger.info(f"📁 Directorios: {self.sources_dir}")
    
    def _check_ollama(self) -> bool:
        """Verifica si Ollama está disponible."""
        try:
            import requests
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def _copy_to_originals(self, pdf_path: Path) -> Path:
        """Copia PDF a originals si no está ahí."""
        if pdf_path.parent == self.originals_dir:
            return pdf_path
        
        dest_path = self.originals_dir / pdf_path.name
        if not dest_path.exists():
            import shutil
            shutil.copy2(pdf_path, dest_path)
            logger.info(f"📋 PDF copiado a: {dest_path}")
        
        return dest_path
    
    def _convert_native(self, pdf_path: Path, conversion_id: int) -> Tuple[str, Dict]:
        """
        Convierte PDF nativo con pdfplumber.
        
        Estrategia:
        1. Extraer texto página por página
        2. Intentar extraer tablas
        3. Formatear como Markdown básico
        
        Performance: ~5-10 segundos para 50 páginas
        """
        logger.info("🚀 [NATIVE] Usando pdfplumber (rápido)")
        
        pdfplumber = _import_pdfplumber()
        
        markdown_parts = []
        metadata = {
            "converter": "pdfplumber",
            "strategy": "native",
            "pages": 0,
            "tables_extracted": 0
        }
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                metadata["pages"] = len(pdf.pages)
                
                for i, page in enumerate(pdf.pages, start=1):
                    # Extraer texto
                    text = page.extract_text() or ""
                    
                    if text.strip():
                        markdown_parts.append(f"## Página {i}\n\n{text}\n")
                    
                    # Intentar extraer tablas
                    tables = page.extract_tables()
                    if tables:
                        for table in tables:
                            if not table or len(table) == 0:
                                continue
                            
                            metadata["tables_extracted"] += 1
                            
                            # Convertir tabla a Markdown (manejar None)
                            header = [str(cell or "") for cell in table[0]]
                            if not any(header):  # Skip si header vacío
                                continue
                                
                            markdown_parts.append("\n| " + " | ".join(header) + " |\n")
                            markdown_parts.append("| " + " | ".join(["---"] * len(header)) + " |\n")
                            
                            for row in table[1:]:
                                cells = [str(cell or "") for cell in row]
                                markdown_parts.append("| " + " | ".join(cells) + " |\n")
                            
                            markdown_parts.append("\n")
                
                markdown = "\n".join(markdown_parts)
                logger.info(f"✅ [NATIVE] Extraídas {metadata['pages']} páginas, "
                           f"{metadata['tables_extracted']} tablas")
                
                return markdown, metadata
        
        except Exception as e:
            logger.error(f"❌ [NATIVE] Error: {e}")
            self.tracker.add_error(conversion_id, "pdfplumber_failed", str(e))
            raise
    
    def _convert_scanned(self, pdf_path: Path, conversion_id: int) -> Tuple[str, Dict]:
        """
        Convierte PDF escaneado con marker-pdf + EasyOCR.
        
        Estrategia:
        1. Cargar modelos marker (Surya OCR)
        2. Procesar con PdfConverter
        3. Extraer markdown de rendered
        
        Performance: ~5-7 minutos para 50 páginas con GPU
        
        Hardware:
        - RTX 3070: ~4-5 min
        - Mac M4: ~6-7 min
        - CPU: ~20-30 min (no recomendado)
        """
        logger.info("🚀 [SCANNED] Usando marker-pdf + EasyOCR (lento, GPU)")
        
        marker = _import_marker()
        
        metadata = {
            "converter": "marker-pdf",
            "strategy": "scanned",
            "device": self.hardware.device
        }
        
        try:
            start_time = time.time()
            
            # Cargar modelos (tarda ~3-5 segundos)
            logger.info("📦 [MARKER] Cargando modelos...")
            model_dict = marker['create_model_dict']()
            
            # Crear converter
            converter = marker['PdfConverter'](artifact_dict=model_dict)
            
            # Procesar PDF (etapa lenta)
            logger.info("🔄 [MARKER] Procesando PDF con OCR...")
            rendered = converter(str(pdf_path))
            
            # Extraer markdown
            try:
                markdown, page_metadata, images = marker['text_from_rendered'](rendered)
            except TypeError:
                # Bug conocido en marker 1.10.1 con imágenes
                logger.warning("⚠️  Bug en text_from_rendered, usando fallback")
                markdown = rendered.markdown if hasattr(rendered, 'markdown') else str(rendered)
                page_metadata = {}
                images = {}
            
            elapsed = time.time() - start_time
            metadata["processing_time_seconds"] = round(elapsed, 2)
            metadata["images_extracted"] = len(images)
            
            logger.info(f"✅ [SCANNED] Procesado en {elapsed:.1f}s, "
                       f"{len(images)} imágenes extraídas")
            
            return markdown, metadata
        
        except Exception as e:
            logger.error(f"❌ [SCANNED] Error: {e}")
            self.tracker.add_error(conversion_id, "marker_failed", str(e))
            raise
    
    def _convert_mixed(self, pdf_path: Path, conversion_id: int) -> Tuple[str, Dict]:
        """
        Convierte PDF mixto con docling.
        
        Estrategia:
        1. docling detecta automáticamente regiones
        2. Aplica OCR solo donde es necesario
        3. Preserva estructura y tablas
        
        Performance: ~30-60 segundos para 50 páginas
        """
        logger.info("🚀 [MIXED] Usando docling (detección automática)")
        
        docling = _import_docling()
        
        metadata = {
            "converter": "docling",
            "strategy": "mixed"
        }
        
        try:
            # TODO: Implementar cuando docling esté instalado
            # Por ahora, fallback a pdfplumber
            logger.warning("⚠️  Docling no implementado aún, usando pdfplumber fallback")
            return self._convert_native(pdf_path, conversion_id)
        
        except Exception as e:
            logger.error(f"❌ [MIXED] Error: {e}")
            self.tracker.add_error(conversion_id, "docling_failed", str(e))
            raise
    
    def convert_single(
        self,
        pdf_path: Path,
        force: bool = False,
        quick_detect: bool = True
    ) -> Dict[str, Any]:
        """
        Convierte un PDF a Markdown con estrategia adaptativa.
        
        Args:
            pdf_path: Ruta al PDF
            force: Forzar reconversión aunque exista
            quick_detect: Detección rápida (solo 3 páginas)
        
        Returns:
            Dict con resultados:
            {
                "success": bool,
                "pdf_type": str,
                "strategy": str,
                "markdown_path": Path,
                "metadata": dict,
                "conversion_id": int,
                "elapsed_time": float
            }
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            logger.error(f"❌ PDF no encontrado: {pdf_path}")
            return {"success": False, "error": "file_not_found"}
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🔄 CONVERSIÓN: {pdf_path.name}")
        logger.info(f"{'='*60}")
        
        start_time = time.time()
        
        # 1. Copiar a originals
        pdf_path = self._copy_to_originals(pdf_path)
        
        # 2. Verificar duplicados
        is_duplicate, existing_id = self.tracker.is_duplicate(pdf_path)
        if is_duplicate and not force:
            logger.info(f"⏩ PDF ya procesado (ID: {existing_id}), use --force para reconvertir")
            existing_conversion = self.tracker.get_conversion(existing_id)
            return {
                "success": True,
                "duplicate": True,
                "conversion_id": existing_id,
                "markdown_path": existing_conversion.get("markdown_path")
            }
        
        # 3. Registrar en DB
        conversion_id = self.tracker.add_conversion(
            pdf_path=pdf_path,
            pdf_name=pdf_path.name,
            status="processing"
        )
        
        try:
            # 4. Detectar tipo de PDF
            if self.force_strategy:
                pdf_type = PDFType(self.force_strategy)
                detection_stats = {"forced": True}
            else:
                pdf_type, detection_stats = self.detector.detect(pdf_path, quick=quick_detect)
            
            logger.info(f"📊 Tipo: {pdf_type.value.upper()}")
            
            # 5. Aplicar estrategia correspondiente
            if pdf_type == PDFType.NATIVE:
                markdown, conv_metadata = self._convert_native(pdf_path, conversion_id)
            elif pdf_type == PDFType.SCANNED:
                markdown, conv_metadata = self._convert_scanned(pdf_path, conversion_id)
            elif pdf_type == PDFType.MIXED:
                markdown, conv_metadata = self._convert_mixed(pdf_path, conversion_id)
            else:
                raise ValueError(f"Tipo de PDF desconocido: {pdf_type}")
            
            # 6. Guardar Markdown
            md_filename = pdf_path.stem + ".md"
            md_path = self.converted_dir / md_filename
            md_path.write_text(markdown, encoding="utf-8")
            
            logger.info(f"💾 Markdown guardado: {md_path}")
            
            # 7. Validar con Ollama (opcional)
            validation_report = None
            if self.use_ollama:
                validation_report = self._validate_with_ollama(markdown, pdf_path)
                if validation_report:
                    self.tracker.add_validation_report(
                        conversion_id=conversion_id,
                        report_data=validation_report
                    )
            
            # 8. Actualizar DB
            elapsed = time.time() - start_time
            
            self.tracker.update_conversion(
                conversion_id=conversion_id,
                status="success",
                markdown_path=str(md_path),
                pages=conv_metadata.get("pages", 0),
                has_tables=conv_metadata.get("tables_extracted", 0) > 0,
                conversion_time_seconds=elapsed,
                notes=json.dumps({
                    **conv_metadata,
                    "detection": detection_stats,
                    "hardware": str(self.hardware)
                })
            )
            
            logger.info(f"✅ CONVERSIÓN COMPLETA en {elapsed:.1f}s")
            logger.info(f"{'='*60}\n")
            
            return {
                "success": True,
                "pdf_type": pdf_type.value,
                "strategy": conv_metadata["strategy"],
                "markdown_path": md_path,
                "metadata": conv_metadata,
                "conversion_id": conversion_id,
                "elapsed_time": elapsed,
                "validation": validation_report
            }
        
        except Exception as e:
            logger.error(f"❌ ERROR: {e}")
            self.tracker.update_conversion(
                conversion_id=conversion_id,
                status="failed",
                notes=json.dumps({"error": str(e)})
            )
            
            return {
                "success": False,
                "error": str(e),
                "conversion_id": conversion_id
            }
    
    def _validate_with_ollama(self, markdown: str, pdf_path: Path) -> Optional[Dict]:
        """Valida conversión con Ollama gemma3:12b."""
        try:
            import requests
            
            prompt = f"""Analiza este Markdown extraído de un PDF y responde en JSON:

Markdown (primeros 2000 caracteres):
```markdown
{markdown[:2000]}
```

Responde SOLO con JSON válido:
{{
  "quality_score": <0-100>,
  "has_structure": <true/false>,
  "has_tables": <true/false>,
  "issues": ["lista", "de", "problemas"],
  "summary": "resumen de 1 línea"
}}
"""
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                report_text = result.get("response", "")
                
                # Intentar parsear JSON
                try:
                    report = json.loads(report_text)
                    logger.info(f"✅ [OLLAMA] Score: {report.get('quality_score', 'N/A')}")
                    return report
                except json.JSONDecodeError:
                    logger.warning("⚠️  [OLLAMA] Respuesta no es JSON válido")
                    return {"raw_response": report_text}
            
        except Exception as e:
            logger.warning(f"⚠️  [OLLAMA] Error: {e}")
        
        return None


# ========== CLI ==========
if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Convertidor Adaptativo PDF→Markdown")
    parser.add_argument("pdf", help="Archivo PDF a convertir")
    parser.add_argument("--force", action="store_true", help="Forzar reconversión")
    parser.add_argument("--ollama", action="store_true", help="Activar validación Ollama")
    parser.add_argument("--strategy", choices=["native", "scanned", "mixed"], 
                       help="Forzar estrategia (debug)")
    parser.add_argument("--sources-dir", default="sources_local", 
                       help="Directorio sources_local (default: sources_local)")
    
    args = parser.parse_args()
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Convertir
    converter = AdaptivePDFConverter(
        sources_local_dir=args.sources_dir,
        use_ollama=args.ollama,
        force_strategy=args.strategy
    )
    
    result = converter.convert_single(
        pdf_path=Path(args.pdf),
        force=args.force
    )
    
    # Mostrar resultado
    if result["success"]:
        print(f"\n✅ Conversión exitosa!")
        print(f"📄 Tipo: {result.get('pdf_type', 'N/A')}")
        print(f"🔧 Estrategia: {result.get('strategy', 'N/A')}")
        print(f"📝 Markdown: {result.get('markdown_path', 'N/A')}")
        print(f"⏱️  Tiempo: {result.get('elapsed_time', 0):.1f}s")
        
        if result.get('validation'):
            print(f"🤖 Score Ollama: {result['validation'].get('quality_score', 'N/A')}")
    else:
        print(f"\n❌ Error: {result.get('error', 'Desconocido')}")
        sys.exit(1)

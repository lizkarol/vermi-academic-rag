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
import os
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import json
import re
import statistics

# Agregar directorio padre al path para imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from pdf_type_detector import PDFTypeDetector, PDFType
from conversion_db import ConversionTracker
from markdown_normalizer import MarkdownNormalizer, normalize_markdown_file
from conversion_profiles import ProfileManager, ConversionProfile
from profile_detector import ProfileDetector

# Lazy imports (solo cargar lo necesario)
_pdfplumber = None
_marker = None
_docling = None
_torch = None

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - opcional
    load_dotenv = None

if load_dotenv:
    env_file = os.getenv("CONVERSION_ENV_FILE")
    if env_file and Path(env_file).exists():
        load_dotenv(env_file)
    else:
        load_dotenv()

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
            logger.warning("⚠️  PyTorch no encontrado, usando fallback CPU.")
            _torch = False
    return _torch


def _resolve_env_path(var_name: str, fallback: Path, project_root: Path) -> Path:
    """Resuelve rutas tomando en cuenta valores en .env (relativas o absolutas)."""
    value = os.getenv(var_name)
    if not value:
        return fallback
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = project_root / candidate
    return candidate


class HardwareConfig:
    """Configuración de hardware detectado."""
    
    def __init__(self):
        """Detecta hardware disponible."""
        torch = _import_torch()
        
        if not torch:
            self.device = "cpu"
            self.device_name = "CPU (sin PyTorch)"
            self.device_memory = None
            self.workers = 1
            self.batch_size = 1
            logger.info("🖥️  PyTorch ausente, usando configuración CPU básica")
            return
        
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
        >>> converter = AdaptivePDFConverter(sources_dir="sources")
        >>> result = converter.convert_single("paper.pdf")
        >>> print(f"Markdown: {result['markdown_path']}")
    """
    
    def __init__(
        self,
        sources_dir: str = "sources",
        use_ollama: bool = False,
        ollama_url: str = "http://localhost:11434",
        ollama_model: str = "gemma3:12b",
        force_strategy: Optional[str] = None,
        normalize: bool = True,
        profile: Optional[str] = None
    ):
        """
        Inicializa el convertidor.
        
        Args:
            sources_dir: Directorio base para fuentes (default: sources)
            use_ollama: Activar validación con Ollama
            ollama_url: URL del servidor Ollama
            ollama_model: Modelo LLM a usar
            force_strategy: Forzar estrategia ("native", "scanned", "mixed")
            normalize: Activar post-procesamiento de normalización (default: True)
            profile: Nombre del perfil de conversión a usar (ej: "academic_apa", "universidad_de_chile_thesis")
        """
        project_root = Path(__file__).parent.parent.parent
        
        provided_dir = Path(sources_dir)
        if not provided_dir.is_absolute():
            provided_dir = project_root / provided_dir
        
        # Permitir override desde .env únicamente cuando se usa el valor por defecto
        if sources_dir == "sources":
            env_sources = os.getenv("SOURCES_DIR")
            if env_sources:
                provided_dir = _resolve_env_path("SOURCES_DIR", provided_dir, project_root)
        
        self.sources_dir = provided_dir
        
        self.originals_dir = _resolve_env_path(
            "SOURCES_ORIGINALS",
            self.sources_dir / "originals",
            project_root
        )
        self.converted_dir = _resolve_env_path(
            "SOURCES_CONVERTED",
            self.sources_dir / "converted",
            project_root
        )
        self.metadata_dir = _resolve_env_path(
            "SOURCES_METADATA",
            self.sources_dir / "metadata",
            project_root
        )
        self.reports_dir = _resolve_env_path(
            "SOURCES_REPORTS",
            self.sources_dir / "reports",
            project_root
        )
        
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
        
        # Sistema de perfiles
        self.profile = profile  # Guardar nombre del perfil
        self.profile_manager = ProfileManager()
        self.profile_detector = ProfileDetector(self.profile_manager)  # Detector automático
        self.active_profile: Optional[ConversionProfile] = None
        if profile:
            self.active_profile = self.profile_manager.get_profile(profile)
            if self.active_profile:
                logger.info(f"✅ Perfil activo: {profile}")
                # Aplicar configuración del perfil
                if self.active_profile.preferred_strategy:
                    self.force_strategy = self.active_profile.preferred_strategy
            else:
                logger.warning(f"⚠️  Perfil '{profile}' no encontrado, usando configuración por defecto")
        
        # Post-procesamiento
        self.normalize = normalize
        self.normalizer = MarkdownNormalizer() if normalize else None
        
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
        Convierte PDF nativo priorizando preservación de estructura.
        
        Estrategia:
        1. Extraer palabras con metadatos (tamaño de fuente, posición)
        2. Reconstruir líneas y detectar encabezados, listas y párrafos
        3. Adjuntar tablas como bloques Markdown
        
        Performance: ~6-12 segundos para 50 páginas (dependiendo del contenido)
        """
        logger.info("🚀 [NATIVE] Usando pdfplumber (estructura preservada)")
        
        pdfplumber = _import_pdfplumber()
        
        markdown_blocks: list[str] = []
        metadata = {
            "converter": "pdfplumber_structured",
            "strategy": "native",
            "pages": 0,
            "tables_extracted": 0,
            "headings_detected": 0,
            "list_items": 0,
            "paragraphs": 0
        }
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                metadata["pages"] = len(pdf.pages)
                
                for page_number, page in enumerate(pdf.pages, start=1):
                    page_lines = [f"## Página {page_number}"]
                    
                    structured_text, page_stats = self._render_page_with_structure(page)
                    metadata["headings_detected"] += page_stats.get("headings", 0)
                    metadata["list_items"] += page_stats.get("list_items", 0)
                    metadata["paragraphs"] += page_stats.get("paragraphs", 0)
                    
                    if structured_text:
                        page_lines.append("")
                        page_lines.append(structured_text)
                    
                    tables = page.extract_tables()
                    if tables:
                        for table in tables:
                            table_md = self._table_to_markdown(table)
                            if not table_md:
                                continue
                            metadata["tables_extracted"] += 1
                            page_lines.append("")
                            page_lines.append(table_md)
                    
                    page_block = "\n".join(
                        line for line in page_lines if line is not None
                    ).strip()
                    
                    if page_block:
                        markdown_blocks.append(page_block)
                
                markdown = self._join_with_page_separators(markdown_blocks)
                
                logger.info(
                    "✅ [NATIVE] Estructura preservada | "
                    f"Páginas: {metadata['pages']} | "
                    f"Encabezados: {metadata['headings_detected']} | "
                    f"Listas: {metadata['list_items']} | "
                    f"Tablas: {metadata['tables_extracted']}"
                )
                
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
    
    def _render_page_with_structure(self, page) -> Tuple[str, Dict[str, int]]:
        """
        Reconstruye el contenido de una página en Markdown preservando estructura básica.
        
        Retorna:
            Tuple con (markdown_page, stats)
                stats = {"headings": int, "list_items": int, "paragraphs": int}
        """
        stats = {"headings": 0, "list_items": 0, "paragraphs": 0}
        
        try:
            words = page.extract_words(
                extra_attrs=["size", "fontname"],
                use_text_flow=True
            )
        except TypeError:
            # Algunas versiones no soportan use_text_flow
            words = page.extract_words(extra_attrs=["size", "fontname"])
        except Exception:
            words = []
        
        if not words:
            fallback_text = (page.extract_text(layout=True) or "").strip()
            if fallback_text:
                stats["paragraphs"] = max(1, fallback_text.count("\n\n") + 1)
            return fallback_text, stats
        
        size_values = [w.get("size") for w in words if w.get("size")]
        body_size = statistics.median(size_values) if size_values else None
        max_size = max(size_values) if size_values else None
        base_indent = min((w.get("x0") or 0.0) for w in words)
        
        lines = self._group_words_into_lines(words)
        page_output: list[str] = []
        paragraph_buffer: list[str] = []
        last_list_idx: Optional[int] = None
        
        def flush_paragraph():
            nonlocal paragraph_buffer
            nonlocal last_list_idx
            if paragraph_buffer:
                paragraph_text = " ".join(paragraph_buffer)
                paragraph_text = self._normalize_sentence(paragraph_text)
                if paragraph_text:
                    page_output.append(paragraph_text)
                    stats["paragraphs"] += 1
                    page_output.append("")
                paragraph_buffer = []
            last_list_idx = None
        
        def append_to_active_list(text: str, indent_level: float) -> bool:
            nonlocal last_list_idx
            if last_list_idx is None:
                return False
            if indent_level <= 4:  # Requiere ligera sangría para considerar continuación
                return False
            continuation = AdaptivePDFConverter._normalize_sentence(text)
            if not continuation:
                return False
            page_output[last_list_idx] += f" {continuation}"
            return True
        
        for line_index, line_words in enumerate(lines):
            line_text = self._join_words(line_words)
            if not line_text:
                flush_paragraph()
                last_list_idx = None
                continue
            
            line_sizes = [w.get("size") for w in line_words if w.get("size")]
            avg_size = statistics.mean(line_sizes) if line_sizes else body_size
            first_x0 = min((w.get("x0") or base_indent) for w in line_words)
            indent = max(0.0, first_x0 - base_indent)
            
            heading_level = self._detect_heading(
                line_text, avg_size, body_size, max_size, line_index
            )
            if heading_level:
                flush_paragraph()
                last_list_idx = None
                stats["headings"] += 1
                page_output.append(f"{'#' * heading_level} {line_text}")
                page_output.append("")
                continue
            
            bullet_line = self._format_bullet_line(line_text, indent)
            if bullet_line:
                flush_paragraph()
                last_list_idx = len(page_output)
                stats["list_items"] += 1
                page_output.append(bullet_line)
                continue
            
            numbered_line = self._format_numbered_line(line_text, indent)
            if numbered_line:
                flush_paragraph()
                last_list_idx = len(page_output)
                stats["list_items"] += 1
                page_output.append(numbered_line)
                continue
            
            if append_to_active_list(line_text, indent):
                continue
            
            last_list_idx = None
            paragraph_buffer.append(line_text)
        
        flush_paragraph()
        
        # Limpiar dobles saltos al final
        while page_output and page_output[-1] == "":
            page_output.pop()
        
        page_markdown = "\n".join(page_output).strip()
        
        if not page_markdown:
            fallback = (page.extract_text(layout=True) or "").strip()
            if fallback:
                return fallback, stats
        
        return page_markdown, stats
    
    @staticmethod
    def _group_words_into_lines(words: list, tolerance: float = 2.5) -> list[list[dict]]:
        """Agrupa palabras en líneas usando tolerancia vertical."""
        if not words:
            return []
        
        sorted_words = sorted(
            words,
            key=lambda w: (
                round(w.get("top", 0.0), 2),
                w.get("x0", 0.0)
            )
        )
        
        lines: list[list[dict]] = []
        current_line: list[dict] = []
        last_top: Optional[float] = None
        
        for word in sorted_words:
            top = word.get("top", 0.0)
            if last_top is None or abs(top - last_top) <= tolerance:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(current_line)
                current_line = [word]
            last_top = top
        
        if current_line:
            lines.append(current_line)
        
        return [
            sorted(line, key=lambda w: w.get("x0", 0.0))
            for line in lines
        ]
    
    @staticmethod
    def _join_words(words: list[dict]) -> str:
        """Une palabras manejando espacios y puntuación."""
        if not words:
            return ""
        
        tokens = [w.get("text", "").strip() for w in words]
        line = " ".join(token for token in tokens if token)
        
        if not line:
            return ""
        
        # Ajustar espacios con puntuación
        line = re.sub(r"\s+([,.;:!?%])", r"\1", line)
        line = re.sub(r"([(\[])\s+", r"\1", line)
        line = re.sub(r"\s+([)\]])", r"\1", line)
        line = re.sub(r"\s{2,}", " ", line)
        
        return line.strip()
    
    @staticmethod
    def _normalize_sentence(text: str) -> str:
        """Normaliza espacios y puntuación en un párrafo."""
        cleaned = re.sub(r"\s+([,.;:!?%])", r"\1", text)
        cleaned = re.sub(r"([(\[])\s+", r"\1", cleaned)
        cleaned = re.sub(r"\s+([)\]])", r"\1", cleaned)
        cleaned = re.sub(r"\s{2,}", " ", cleaned)
        return cleaned.strip()
    
    @staticmethod
    def _detect_heading(
        text: str,
        avg_size: Optional[float],
        body_size: Optional[float],
        max_size: Optional[float],
        line_index: int
    ) -> Optional[int]:
        """Heurística para identificar encabezados y asignar nivel."""
        stripped = text.strip()
        if not stripped or len(stripped) > 140:
            return None
        
        words = stripped.split()
        heading_level = None
        
        if body_size and avg_size:
            if max_size and avg_size >= max_size - 0.3:
                heading_level = 2
            elif avg_size >= body_size * 1.45:
                heading_level = 2 if line_index <= 2 else 3
            elif avg_size >= body_size * 1.25:
                heading_level = 3
        
        # Heurística adicional por formato
        if heading_level is None:
            if re.match(r"^\d+\.\d+(?:\.\d+)*\s+[A-ZÁÉÍÓÚÑ]", stripped):
                heading_level = 3
        
        # Evitar considerar oraciones con punto final como encabezado
        if heading_level and stripped.endswith("."):
            heading_level = None
        
        return heading_level
    
    @staticmethod
    def _format_bullet_line(text: str, indent: float) -> Optional[str]:
        """Formatea líneas tipo viñeta."""
        stripped = text.strip()
        bullet_match = re.match(r"^([\-\*\u2022•▪◦])\s+(.+)$", stripped)
        if not bullet_match:
            return None
        
        content = bullet_match.group(2).strip()
        if not content:
            return None
        
        indent_level = max(0, int(indent // 18))
        indentation = "  " * indent_level
        content = AdaptivePDFConverter._normalize_sentence(content)
        return f"{indentation}- {content}"
    
    @staticmethod
    def _format_numbered_line(text: str, indent: float) -> Optional[str]:
        """Formatea listas numeradas."""
        stripped = text.strip()
        number_match = re.match(r"^(\d+(?:\.\d+)*)(?:[\.\)])\s+(.+)$", stripped)
        if not number_match:
            return None
        
        numbering = number_match.group(1)
        content = number_match.group(2).strip()
        if not content:
            return None
        
        indent_level = max(0, int(indent // 18))
        indentation = "  " * indent_level
        content = AdaptivePDFConverter._normalize_sentence(content)
        return f"{indentation}{numbering}. {content}"
    
    @staticmethod
    def _table_to_markdown(table: list) -> str:
        """Convierte tablas detectadas en formato Markdown."""
        if not table or not table[0]:
            return ""
        
        def _normalize_row(row):
            return [str(cell or "").strip() for cell in row]
        
        header_row_index = next(
            (idx for idx, row in enumerate(table) if any((cell or "").strip() for cell in row)),
            None
        )
        if header_row_index is None:
            return ""
        
        header = _normalize_row(table[header_row_index])
        data_rows = [row for i, row in enumerate(table) if i != header_row_index]
        
        if not any(header):
            header = [f"Columna {i+1}" for i in range(len(header))]
        
        md_lines = [
            "| " + " | ".join(header) + " |",
            "|" + "|".join(["---"] * len(header)) + "|"
        ]
        
        for row in data_rows:
            cells = _normalize_row(row)
            if not any(cells):
                continue
            if len(cells) < len(header):
                cells += [""] * (len(header) - len(cells))
            md_lines.append("| " + " | ".join(cells) + " |")
        
        return "\n".join(md_lines)
    
    @staticmethod
    def _join_with_page_separators(blocks: list[str]) -> str:
        """Une bloques de página con separadores visibles."""
        cleaned = [block.strip() for block in blocks if block and block.strip()]
        if not cleaned:
            return ""
        return ("\n\n---\n\n".join(cleaned)).strip()
    
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
        
        # 3. Detección automática de perfil (si no se especificó uno)
        profile_detection_info = {}
        if not self.profile and not self.active_profile:
            logger.info("🔍 Detectando perfil automáticamente...")
            detected_profile, profile_detection_info = self.profile_detector.detect_profile(pdf_path, quick=True)
            self.profile = detected_profile
            self.active_profile = self.profile_manager.get_profile(detected_profile)
            logger.info(f"✅ Perfil auto-detectado: {detected_profile} (confianza: {profile_detection_info.get('confidence', 0):.0%})")
        
        # 4. Registrar en DB
        conversion_id = self.tracker.add_conversion(
            pdf_path=pdf_path,
            pdf_name=pdf_path.name,
            status="processing"
        )
        
        try:
            # 5. Detectar tipo de PDF
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
            
            # 6.5 Post-procesar con normalización (nuevo)
            normalization_report = None
            if self.normalize and self.normalizer:
                logger.info("🔄 Aplicando post-procesamiento de normalización...")
                try:
                    norm_result = self.normalizer.normalize(markdown)
                    
                    # Guardar markdown normalizado
                    normalized_md = norm_result['markdown']
                    md_path.write_text(normalized_md, encoding="utf-8")
                    
                    # Guardar reporte de normalización
                    norm_report_path = self.reports_dir / f"{pdf_path.stem}_normalization.json"
                    with open(norm_report_path, 'w', encoding='utf-8') as f:
                        json.dump({
                            "validation": norm_result['validation'],
                            "changes_count": len(norm_result['changes']),
                            "changes": norm_result['changes'][:20]
                        }, f, indent=2, ensure_ascii=False)
                    
                    normalization_report = norm_result['validation']
                    logger.info(f"✅ Normalización completada - Fidelidad: {normalization_report['fidelity_score']:.1f}%")
                    logger.info(f"📊 Reporte: {norm_report_path}")
                except Exception as e:
                    logger.warning(f"⚠️  Error en normalización: {e}")
                    normalization_report = {"error": str(e)}
            
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
                pdf_type=pdf_type.value,
                profile_used=self.profile,
                fidelity_score=normalization_report.get("fidelity_score") if normalization_report else None,
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
                "validation": validation_report,
                "normalization": normalization_report
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
    parser.add_argument("pdf", nargs='?', help="Archivo PDF a convertir")
    parser.add_argument("--force", action="store_true", help="Forzar reconversión")
    parser.add_argument("--ollama", action="store_true", help="Activar validación Ollama")
    parser.add_argument("--no-normalize", action="store_true", help="Desactivar post-procesamiento")
    parser.add_argument("--strategy", choices=["native", "scanned", "mixed"], 
                       help="Forzar estrategia (debug)")
    parser.add_argument("--sources-dir", default="sources", 
                       help="Directorio de fuentes (default: sources)")
    parser.add_argument("--profile", type=str,
                       help="Usar perfil de conversión (ej: academic_apa, universidad_de_chile_thesis)")
    parser.add_argument("--list-profiles", action="store_true",
                       help="Listar perfiles disponibles y salir")
    parser.add_argument("--create-profile", type=str, metavar="UNIVERSITY_NAME",
                       help="Crear perfil personalizado para una universidad")
    
    args = parser.parse_args()
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Comando: Listar perfiles
    if args.list_profiles:
        manager = ProfileManager()
        print("\n" + "="*60)
        print("📋 PERFILES DISPONIBLES")
        print("="*60)
        for name in manager.list_profiles():
            profile = manager.get_profile(name)
            print(f"\n🔹 {name}")
            print(f"   Descripción: {profile.description}")
            if profile.normalization.institution:
                print(f"   Institución: {profile.normalization.institution}")
            print(f"   Estilo: {profile.normalization.citation_style}")
            print(f"   Encabezados: {profile.normalization.heading_style}")
        print("\n" + "="*60)
        sys.exit(0)
    
    # Comando: Crear perfil
    if args.create_profile:
        from conversion_profiles import CitationStyle, HeadingStyle
        manager = ProfileManager()
        
        print(f"\n📝 Creando perfil para: {args.create_profile}")
        profile = manager.create_university_profile(
            university_name=args.create_profile,
            citation_style=CitationStyle.APA,  # Por defecto
            heading_style=HeadingStyle.DECIMAL
        )
        
        if manager.save_profile(profile):
            print(f"✅ Perfil creado: {profile.name}")
            print(f"💾 Guardado en: {manager.profiles_dir / f'{profile.name}.json'}")
            print(f"\n💡 Uso: python adaptive_converter.py documento.pdf --profile {profile.name}")
        else:
            print(f"❌ Error creando perfil")
        
        sys.exit(0)
    
    # Verificar que se proporcionó PDF
    if not args.pdf:
        parser.error("Se requiere especificar un archivo PDF")
    
    # Convertir
    converter = AdaptivePDFConverter(
        sources_dir=args.sources_dir,
        use_ollama=args.ollama,
        force_strategy=args.strategy,
        normalize=not args.no_normalize,
        profile=args.profile
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
        
        if result.get('normalization'):
            print(f"📊 Fidelidad: {result['normalization'].get('fidelity_score', 'N/A')}%")
        
        if result.get('validation'):
            print(f"🤖 Score Ollama: {result['validation'].get('quality_score', 'N/A')}")
    else:
        print(f"\n❌ Error: {result.get('error', 'Desconocido')}")
        sys.exit(1)

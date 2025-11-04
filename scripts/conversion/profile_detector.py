#!/usr/bin/env python3
"""
profile_detector.py
Sistema de detección automática de perfiles de conversión

Detecta automáticamente el perfil adecuado para un PDF basándose en:
- Metadata del PDF (autor, institución, keywords)
- Patrones en primeras páginas (logos, headers, footers)
- Estructura del documento (capítulos, secciones)

Autor: VermiKhipu Academic RAG Team
Fecha: Noviembre 3, 2025
"""

import re
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import logging

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

logger = logging.getLogger(__name__)


class ProfileDetector:
    """Detecta automáticamente el perfil de conversión apropiado para un PDF."""
    
    # Patrones institucionales
    INSTITUTION_PATTERNS = {
        "universidad_de_chile": [
            r"universidad\s+de\s+chile",
            r"uchile",
            r"u\.\s*de\s*chile",
        ],
        "universidad_catolica": [
            r"pontificia\s+universidad\s+cat[oó]lica",
            r"uc\s+chile",
            r"puc",
        ],
        "universidad_santiago": [
            r"universidad\s+de\s+santiago",
            r"usach",
        ],
        "universidad_tacna": [
            r"universidad\s+(?:privada\s+)?de\s+tacna",
            r"upt",
        ],
        "universidad_generica": [
            r"universidad\s+\w+",  # Cualquier universidad
            r"facultad\s+de",
            r"escuela\s+profesional",
        ],
    }
    
    # Patrones de formato de citación
    CITATION_PATTERNS = {
        "apa": [
            r"\(\d{4}\)\.",  # (2024). 
            r"et\s+al\.",
            r"Retrieved\s+from",
        ],
        "vancouver": [
            r"\[\d+\]",  # [1], [2]
            r"Available\s+from:",
        ],
        "ieee": [
            r"\[\d+\]",
            r"vol\.",
            r"no\.",
            r"pp\.",
        ],
    }
    
    # Patrones de estructura
    STRUCTURE_PATTERNS = {
        "thesis": [
            r"tesis\s+para\s+optar",
            r"para\s+optar(?:\s+(?:el|al))?\s+t[ií]tulo",
            r"memoria\s+para\s+optar",
            r"thesis\s+submitted",
            r"cap[ií]tulo\s+[IVX]+",
            r"tesis\b",  # Palabra "tesis" sola
            r"escuela\s+profesional",
            r"facultad\s+de\s+ingenier[ií]a",
        ],
        "paper": [
            r"abstract",
            r"keywords:",
            r"introduction",
            r"methodology",
            r"results",
            r"discussion",
        ],
        "book": [
            r"cap[ií]tulo\s+\d+",
            r"chapter\s+\d+",
            r"parte\s+[IVX]+",
            r"secci[oó]n\s+\d+",
        ],
        "legal": [
            r"art[ií]culo\s+\d+",
            r"inciso\s+\d+",
            r"p[aá]rrafo\s+\d+",
            r"ley\s+n[º°]",
        ],
    }
    
    def __init__(self, profiles_manager):
        """
        Inicializa el detector.
        
        Args:
            profiles_manager: Instancia de ProfileManager con perfiles disponibles
        """
        self.profiles_manager = profiles_manager
        self.available_profiles = profiles_manager.list_profiles()
        
        if not pdfplumber:
            logger.warning("pdfplumber no disponible - detección limitada")
    
    def detect_profile(self, pdf_path: Path, quick: bool = True) -> Tuple[Optional[str], Dict]:
        """
        Detecta automáticamente el perfil apropiado para un PDF.
        
        Args:
            pdf_path: Ruta del PDF a analizar
            quick: Si True, solo analiza primeras 3 páginas
        
        Returns:
            (profile_name, detection_info): Tupla con nombre del perfil y dict con info de detección
        """
        logger.info(f"🔍 Detectando perfil para: {pdf_path.name}")
        
        detection_info = {
            "method": "automatic",
            "confidence": 0.0,
            "matches": {},
            "analyzed_pages": 0
        }
        
        if not pdfplumber:
            logger.warning("⚠️  pdfplumber no disponible, usando perfil genérico")
            return "academic_apa", detection_info
        
        try:
            # 1. Extraer metadata del PDF
            metadata = self._extract_metadata(pdf_path)
            detection_info["metadata"] = metadata
            
            # 2. Extraer texto de primeras páginas
            text_sample = self._extract_text_sample(pdf_path, pages=3 if quick else 10)
            detection_info["analyzed_pages"] = len(text_sample.split('\n\n'))
            
            # 3. Detectar institución
            institution = self._detect_institution(text_sample, metadata)
            if institution:
                detection_info["matches"]["institution"] = institution
                # Buscar perfil específico de institución
                profile_name = f"{institution}_thesis"
                if profile_name in self.available_profiles:
                    detection_info["confidence"] = 0.9
                    logger.info(f"✅ Perfil detectado por institución: {profile_name}")
                    return profile_name, detection_info
            
            # 4. Detectar estilo de citación
            citation_style = self._detect_citation_style(text_sample)
            if citation_style:
                detection_info["matches"]["citation_style"] = citation_style
            
            # 5. Detectar tipo de documento
            doc_type = self._detect_document_type(text_sample, metadata)
            if doc_type:
                detection_info["matches"]["document_type"] = doc_type
            
            # 6. Seleccionar perfil basándose en detecciones
            profile_name = self._select_best_profile(
                citation_style=citation_style,
                doc_type=doc_type,
                institution=institution
            )
            
            detection_info["confidence"] = self._calculate_confidence(detection_info["matches"])
            
            logger.info(f"✅ Perfil detectado: {profile_name} (confianza: {detection_info['confidence']:.0%})")
            return profile_name, detection_info
            
        except Exception as e:
            logger.error(f"❌ Error en detección: {e}")
            detection_info["error"] = str(e)
            return "academic_apa", detection_info
    
    def _extract_metadata(self, pdf_path: Path) -> Dict:
        """Extrae metadata del PDF."""
        metadata = {}
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                if pdf.metadata:
                    metadata = {
                        "title": pdf.metadata.get("Title", ""),
                        "author": pdf.metadata.get("Author", ""),
                        "subject": pdf.metadata.get("Subject", ""),
                        "keywords": pdf.metadata.get("Keywords", ""),
                        "creator": pdf.metadata.get("Creator", ""),
                    }
        except Exception as e:
            logger.warning(f"⚠️  Error extrayendo metadata: {e}")
        
        return metadata
    
    def _extract_text_sample(self, pdf_path: Path, pages: int = 3) -> str:
        """Extrae texto de las primeras N páginas."""
        text_parts = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages[:pages]):
                    try:
                        page_text = page.extract_text() or ""
                        text_parts.append(page_text)
                    except Exception as e:
                        logger.warning(f"⚠️  Error en página {i+1}: {e}")
                        continue
        except Exception as e:
            logger.error(f"❌ Error abriendo PDF: {e}")
        
        return "\n\n".join(text_parts)
    
    def _detect_institution(self, text: str, metadata: Dict) -> Optional[str]:
        """Detecta institución académica."""
        text_lower = text.lower()
        
        # Buscar en texto
        for institution, patterns in self.INSTITUTION_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    logger.debug(f"  📚 Institución detectada: {institution}")
                    return institution
        
        # Buscar en metadata
        author = metadata.get("author", "").lower()
        subject = metadata.get("subject", "").lower()
        
        for institution, patterns in self.INSTITUTION_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, author + " " + subject, re.IGNORECASE):
                    logger.debug(f"  📚 Institución detectada en metadata: {institution}")
                    return institution
        
        return None
    
    def _detect_citation_style(self, text: str) -> Optional[str]:
        """Detecta estilo de citación predominante."""
        scores = {}
        
        for style, patterns in self.CITATION_PATTERNS.items():
            count = 0
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                count += len(matches)
            
            if count > 0:
                scores[style] = count
        
        if scores:
            best_style = max(scores, key=scores.get)
            logger.debug(f"  📝 Estilo de citación: {best_style} ({scores[best_style]} matches)")
            return best_style
        
        return None
    
    def _detect_document_type(self, text: str, metadata: Dict) -> Optional[str]:
        """Detecta tipo de documento."""
        scores = {}
        
        # Buscar patrones en texto
        for doc_type, patterns in self.STRUCTURE_PATTERNS.items():
            count = 0
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                count += len(matches)
            
            if count > 0:
                scores[doc_type] = count
        
        # Boost por metadata
        title = metadata.get("title", "").lower()
        if "thesis" in title or "tesis" in title:
            scores["thesis"] = scores.get("thesis", 0) + 5
        
        if scores:
            best_type = max(scores, key=scores.get)
            logger.debug(f"  📄 Tipo de documento: {best_type} ({scores[best_type]} matches)")
            return best_type
        
        return None
    
    def _select_best_profile(
        self,
        citation_style: Optional[str],
        doc_type: Optional[str],
        institution: Optional[str]
    ) -> str:
        """
        Selecciona el mejor perfil basándose en las detecciones.
        
        Prioridad:
        1. Perfil específico de institución (si existe en config/profiles/)
        2. Perfil genérico por tipo + estilo (fallback inteligente)
        3. Perfil genérico por estilo de citación
        4. Fallback final a academic_apa
        """
        # 1. Intentar perfil institucional específico
        if institution and institution not in ["universidad_generica"]:
            profile_name = f"{institution}_thesis"
            if profile_name in self.available_profiles:
                logger.debug(f"  ✓ Perfil institucional específico: {profile_name}")
                return profile_name
            else:
                logger.debug(f"  ℹ️  Perfil {profile_name} no existe, usando genérico")
        
        # 2. Perfil genérico por tipo de documento + estilo
        if doc_type == "thesis":
            # Mapeo inteligente para tesis
            if citation_style == "apa" and "academic_apa" in self.available_profiles:
                logger.debug(f"  ✓ Tesis APA: academic_apa")
                return "academic_apa"
            elif citation_style == "vancouver" and "medical_vancouver" in self.available_profiles:
                logger.debug(f"  ✓ Tesis Vancouver: medical_vancouver")
                return "medical_vancouver"
            elif citation_style == "ieee" and "engineering_ieee" in self.available_profiles:
                logger.debug(f"  ✓ Tesis IEEE: engineering_ieee")
                return "engineering_ieee"
            else:
                # Tesis sin estilo específico
                if "academic_apa" in self.available_profiles:
                    logger.debug(f"  ✓ Tesis genérica: academic_apa (default)")
                    return "academic_apa"
        
        if doc_type == "book" and "book_chapters" in self.available_profiles:
            logger.debug(f"  ✓ Libro: book_chapters")
            return "book_chapters"
        
        if doc_type == "legal" and "legal_documents" in self.available_profiles:
            logger.debug(f"  ✓ Legal: legal_documents")
            return "legal_documents"
        
        # 3. Perfil genérico por estilo de citación
        if citation_style:
            style_map = {
                "apa": "academic_apa",
                "vancouver": "medical_vancouver",
                "ieee": "engineering_ieee"
            }
            preferred = style_map.get(citation_style)
            if preferred and preferred in self.available_profiles:
                logger.debug(f"  ✓ Por estilo {citation_style}: {preferred}")
                return preferred
        
        # 4. Fallback final - buscar cualquier perfil disponible
        if "academic_apa" in self.available_profiles:
            logger.debug(f"  ✓ Fallback: academic_apa")
            return "academic_apa"
        elif self.available_profiles:
            fallback = self.available_profiles[0]
            logger.debug(f"  ⚠️  Fallback: {fallback} (primer perfil disponible)")
            return fallback
        else:
            logger.error(f"  ❌ No hay perfiles disponibles!")
            return "academic_apa"  # Último recurso
    
    def _calculate_confidence(self, matches: Dict) -> float:
        """Calcula confianza de la detección basándose en matches."""
        confidence = 0.0
        
        # Puntos por cada match
        if "institution" in matches:
            confidence += 0.4
        
        if "citation_style" in matches:
            confidence += 0.3
        
        if "document_type" in matches:
            confidence += 0.3
        
        return min(confidence, 1.0)
    
    def suggest_profile(self, pdf_path: Path) -> str:
        """
        Método de conveniencia que solo retorna el nombre del perfil.
        
        Args:
            pdf_path: Ruta del PDF
        
        Returns:
            Nombre del perfil sugerido
        """
        profile_name, _ = self.detect_profile(pdf_path, quick=True)
        return profile_name

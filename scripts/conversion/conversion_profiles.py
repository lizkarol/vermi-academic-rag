"""
Sistema de Perfiles de Conversión Personalizables

Permite definir perfiles reutilizables para instituciones, formatos o estilos
de documentos recurrentes (ej: tesis de una universidad específica).

Autor: VermiKhipu Academic RAG
Fecha: Noviembre 3, 2025
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class CitationStyle(Enum):
    """Estilos de citación soportados."""
    APA = "apa"
    VANCOUVER = "vancouver"
    IEEE = "ieee"
    CHICAGO = "chicago"
    HARVARD = "harvard"
    MLA = "mla"
    ISO = "iso"
    CUSTOM = "custom"


class HeadingStyle(Enum):
    """Estilos de numeración de encabezados."""
    DECIMAL = "decimal"           # 1.1.1, 1.2, etc.
    ROMAN = "roman"               # I, II, III
    LETTER = "letter"             # A, B, C
    KEYWORD = "keyword"           # Capítulo, Parte, Sección
    MIXED = "mixed"               # Combinación
    NONE = "none"                 # Sin numeración


@dataclass
class NormalizationProfile:
    """
    Perfil de normalización personalizable.
    
    Define reglas específicas para un tipo de documento o institución.
    """
    # Identificación
    name: str
    description: str
    institution: Optional[str] = None
    document_type: Optional[str] = None  # tesis, paper, libro, manual
    
    # Estilo de citación
    citation_style: str = CitationStyle.APA.value
    
    # Estilo de encabezados
    heading_style: str = HeadingStyle.DECIMAL.value
    heading_keywords: Optional[List[str]] = None  # Para KEYWORD style
    
    # Jerarquía de encabezados
    max_heading_level: int = 6
    start_level_offset: int = 1  # ¿Empezar en H1 o H2?
    
    # Patrones específicos
    page_marker_pattern: Optional[str] = None  # Regex para "Página X"
    footer_pattern: Optional[str] = None
    header_pattern: Optional[str] = None
    
    # Reglas de detección
    min_chars_for_heading: int = 3
    max_chars_for_heading: int = 200
    uppercase_is_heading: bool = True
    detect_bold_as_heading: bool = True
    
    # Fusión de líneas
    merge_fragmented_lines: bool = True
    min_line_length_for_merge: int = 60
    
    # Tablas e imágenes
    preserve_tables: bool = True
    preserve_images: bool = True
    extract_image_captions: bool = True
    
    # Metadata
    preserve_metadata: bool = False
    extract_bibliography: bool = True
    
    # Validación
    llm_validation: bool = False
    fidelity_threshold: float = 0.70  # Mínimo aceptable
    
    # Tags para clasificación
    tags: Optional[List[str]] = None
    
    def __post_init__(self):
        """Validación post-inicialización."""
        if self.tags is None:
            self.tags = []
        if self.heading_keywords is None:
            self.heading_keywords = []


@dataclass
class ConversionProfile:
    """
    Perfil completo de conversión (detección + normalización).
    
    Incluye configuración de estrategia de conversión según tipo de PDF.
    """
    # Identificación
    name: str
    description: str
    
    # Estrategia de conversión
    preferred_strategy: Optional[str] = None  # 'pdfplumber', 'marker', 'docling'
    force_ocr: bool = False
    ocr_languages: List[str] = None
    
    # Perfil de normalización asociado
    normalization: NormalizationProfile = None
    
    # Detección de tipo
    quick_detection: bool = True  # Analizar solo primeras páginas
    
    # Performance
    enable_gpu: bool = True
    batch_size: int = 1
    
    # Outputs
    save_intermediate_files: bool = False
    generate_report: bool = True
    
    def __post_init__(self):
        """Inicialización de valores por defecto."""
        if self.ocr_languages is None:
            self.ocr_languages = ['es', 'en']
        if self.normalization is None:
            self.normalization = NormalizationProfile(
                name=f"{self.name}_default",
                description="Perfil de normalización por defecto"
            )


class ProfileManager:
    """
    Gestor de perfiles de conversión.
    
    Permite cargar, guardar y aplicar perfiles personalizados.
    """
    
    def __init__(self, profiles_dir: Optional[Path] = None):
        """
        Inicializa el gestor de perfiles.
        
        Args:
            profiles_dir: Directorio donde guardar/cargar perfiles.
                         Por defecto: ./config/profiles/
        """
        if profiles_dir is None:
            profiles_dir = Path(__file__).parent.parent.parent / "config" / "profiles"
        
        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        
        self.profiles: Dict[str, ConversionProfile] = {}
        self._load_profiles_from_json()
    
    def _load_profiles_from_json(self):
        """Carga todos los perfiles desde archivos JSON."""
        json_files = list(self.profiles_dir.glob("*.json"))
        
        if not json_files:
            logger.warning(f"⚠️  No se encontraron perfiles en {self.profiles_dir}")
            return
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Reconstruir objetos
                norm_data = data.get('normalization', {})
                normalization = NormalizationProfile(**norm_data)
                
                profile_data = {k: v for k, v in data.items() if k != 'normalization'}
                profile = ConversionProfile(**profile_data, normalization=normalization)
                
                self.profiles[profile.name] = profile
                logger.info(f"✅ Perfil cargado: {profile.name}")
                
            except Exception as e:
                logger.error(f"❌ Error cargando perfil {json_file.name}: {e}")
        
        logger.info(f"📂 Total de perfiles cargados: {len(self.profiles)}")
    
    def get_profile(self, name: str) -> Optional[ConversionProfile]:
        """Obtiene un perfil por nombre."""
        return self.profiles.get(name)
    
    def list_profiles(self) -> List[str]:
        """Lista nombres de perfiles disponibles."""
        return list(self.profiles.keys())
    
    def save_profile(self, profile: ConversionProfile, overwrite: bool = False) -> bool:
        """
        Guarda un perfil personalizado.
        
        Args:
            profile: Perfil a guardar
            overwrite: Si True, sobrescribe si existe
        
        Returns:
            True si se guardó exitosamente
        """
        json_file = self.profiles_dir / f"{profile.name}.json"
        
        if json_file.exists() and not overwrite:
            logger.warning(f"⚠️  Perfil {profile.name} ya existe. Use overwrite=True")
            return False
        
        try:
            # Convertir a dict recursivamente
            profile_dict = self._profile_to_dict(profile)
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(profile_dict, f, indent=2, ensure_ascii=False)
            
            self.profiles[profile.name] = profile
            logger.info(f"✅ Perfil guardado: {json_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error guardando perfil: {e}")
            return False
    
    def _profile_to_dict(self, profile: ConversionProfile) -> Dict:
        """Convierte perfil a diccionario serializable."""
        result = asdict(profile)
        
        # Convertir Enums a strings
        if 'normalization' in result:
            norm = result['normalization']
            if 'citation_style' in norm and hasattr(norm['citation_style'], 'value'):
                norm['citation_style'] = norm['citation_style'].value
            if 'heading_style' in norm and hasattr(norm['heading_style'], 'value'):
                norm['heading_style'] = norm['heading_style'].value
        
        return result
    
    def create_university_profile(
        self,
        university_name: str,
        citation_style: CitationStyle = CitationStyle.APA,
        heading_style: HeadingStyle = HeadingStyle.DECIMAL,
        custom_patterns: Optional[Dict[str, str]] = None
    ) -> ConversionProfile:
        """
        Crea un perfil personalizado para una universidad.
        
        Args:
            university_name: Nombre de la universidad
            citation_style: Estilo de citación usado
            heading_style: Estilo de numeración de encabezados
            custom_patterns: Patrones regex personalizados
        
        Returns:
            Perfil configurado para la universidad
        
        Ejemplo:
            >>> manager = ProfileManager()
            >>> profile = manager.create_university_profile(
            ...     "Universidad de Chile",
            ...     citation_style=CitationStyle.APA,
            ...     heading_style=HeadingStyle.DECIMAL
            ... )
            >>> manager.save_profile(profile)
        """
        safe_name = university_name.lower().replace(" ", "_").replace(".", "")
        
        normalization = NormalizationProfile(
            name=f"{safe_name}_norm",
            description=f"Normalización para {university_name}",
            institution=university_name,
            document_type="tesis",
            citation_style=citation_style.value,
            heading_style=heading_style.value,
            tags=[safe_name, "universidad", "tesis"]
        )
        
        # Aplicar patrones personalizados si existen
        if custom_patterns:
            if 'page_marker' in custom_patterns:
                normalization.page_marker_pattern = custom_patterns['page_marker']
            if 'footer' in custom_patterns:
                normalization.footer_pattern = custom_patterns['footer']
            if 'header' in custom_patterns:
                normalization.header_pattern = custom_patterns['header']
        
        profile = ConversionProfile(
            name=f"{safe_name}_thesis",
            description=f"Tesis de {university_name}",
            normalization=normalization
        )
        
        return profile


# ========== CLI para testing ==========
if __name__ == "__main__":
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s - %(message)s'
    )
    
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
        if profile.normalization.tags:
            print(f"   Tags: {', '.join(profile.normalization.tags)}")
    
    print("\n" + "="*60)
    print("💡 EJEMPLO: Crear perfil personalizado")
    print("="*60)
    
    # Crear perfil de ejemplo
    uchile_profile = manager.create_university_profile(
        "Universidad de Chile",
        citation_style=CitationStyle.APA,
        heading_style=HeadingStyle.DECIMAL,
        custom_patterns={
            'page_marker': r'Página\s+\d+',
            'footer': r'Universidad de Chile.*\d{4}'
        }
    )
    
    print(f"\n✅ Perfil creado: {uchile_profile.name}")
    print(f"   Descripción: {uchile_profile.description}")
    print(f"   Normalización: {uchile_profile.normalization.name}")
    
    # Guardar perfil de ejemplo
    if manager.save_profile(uchile_profile):
        print(f"💾 Perfil guardado en: {manager.profiles_dir / f'{uchile_profile.name}.json'}")
    
    print("\n" + "="*60)

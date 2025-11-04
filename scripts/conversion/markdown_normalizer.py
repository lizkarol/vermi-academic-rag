#!/usr/bin/env python3
"""
Post-procesador de Markdown: normalización de jerarquía y fidelidad.
Complemento robusto para Docling.

Resuelve 3 problemas críticos:
1. Jerarquía de encabezados inconsistente
2. Líneas fragmentadas por saltos de página
3. Marcadores "Página X" innecesarios
"""

import re
import logging
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class HeadingInfo:
    """Información de encabezado detectado."""
    original_text: str
    original_level: int  # H1-H6 (1-6)
    semantic_level: Optional[Tuple[int, ...]]  # Nivel semántico (1, 2, 1) para "1.2.1"
    numbering_pattern: Optional[str]  # Ej: "1.2.1"
    is_detected_heading: bool  # ¿Es encabezado detectado por reglas?
    confidence: float  # 0.0-1.0
    line_number: int


class MarkdownNormalizer:
    """Normalizador robusto de Markdown con fidelidad."""
    
    def __init__(self):
        self.heading_map = {}  # Mapeo: (semantic_level) → (markdown_level)
        self.changes_log = []
    
    def normalize(self, markdown: str) -> Dict:
        """Pipeline completo de normalización."""
        
        logger.info("="*60)
        logger.info("🔄 NORMALIZANDO MARKDOWN")
        logger.info("="*60)
        
        # Fase 1: Limpieza de metadata
        cleaned = self._phase1_cleanup_metadata(markdown)
        logger.info(f"✅ Fase 1: {len(cleaned.splitlines())} líneas después limpieza")
        
        # Fase 2: Detección de encabezados
        lines = cleaned.splitlines()
        heading_info = self._phase2_detect_headings(lines)
        logger.info(f"✅ Fase 2: {len(heading_info)} encabezados detectados")
        
        # Fase 3: Análisis de profundidad
        self.heading_map = self._phase3_analyze_hierarchy(heading_info)
        logger.info(f"✅ Fase 3: Mapeo de jerarquía completado")
        
        # Fase 4: Aplicar normalización
        normalized_lines = self._phase4_apply_normalization(lines, heading_info)
        logger.info(f"✅ Fase 4: Normalización aplicada")
        
        # Fase 5: Fusión de líneas fragmentadas
        normalized_lines = self._phase5_merge_fragmented_lines(normalized_lines)
        logger.info(f"✅ Fase 5: Líneas fragmentadas fusionadas")
        
        # Convertir a string
        normalized = '\n'.join(normalized_lines)
        
        # Validación final
        validation = self._validate(normalized)
        
        logger.info("="*60)
        logger.info(f"📊 RESULTADO FINAL")
        logger.info(f"  Fidelidad: {validation['fidelity_score']:.1f}%")
        logger.info(f"  Cambios: {len(self.changes_log)}")
        logger.info("="*60)
        
        return {
            "markdown": normalized,
            "validation": validation,
            "changes": self.changes_log,
            "heading_map": self.heading_map
        }
    
    # ========== FASE 1: LIMPIEZA DE METADATA ==========
    
    def _phase1_cleanup_metadata(self, markdown: str) -> str:
        """Elimina metadata no semántica."""
        
        # Patrón: "Página X", "Page X", etc.
        markdown = re.sub(r'^#+\s*(?:Página|Page)\s*\d+\s*$', '', markdown, flags=re.MULTILINE)
        
        # Patrón: "---" (separadores vacíos solos)
        markdown = re.sub(r'^---\s*$\n', '', markdown, flags=re.MULTILINE)
        
        # Footer/header patterns
        patterns_to_remove = [
            r'^#{1,6}\s*(?:©|®|™|All rights|Derechos reservados).*$',
            r'^#{1,6}\s*(?:Footer|Header|Pie de página).*$',
            r'^#{1,6}\s*(?:\d+|-|—)\s*$',  # Solo números o guiones
            r'^#{1,6}\s*[ivxIVX]+\s*$',  # Solo números romanos
        ]
        
        for pattern in patterns_to_remove:
            markdown = re.sub(pattern, '', markdown, flags=re.MULTILINE)
        
        # Múltiples líneas en blanco → una sola
        markdown = re.sub(r'\n\n+', '\n\n', markdown)
        
        return markdown.strip()
    
    # ========== FASE 2: DETECCIÓN DE ENCABEZADOS ==========
    
    def _phase2_detect_headings(self, lines: List[str]) -> Dict[int, HeadingInfo]:
        """Detecta encabezados por múltiples heurísticas."""
        
        heading_info = {}
        
        for line_num, line in enumerate(lines):
            # Ya es markdown heading?
            md_match = re.match(r'^(#+)\s+(.+)$', line)
            if md_match:
                level = len(md_match.group(1))
                text = md_match.group(2).strip()
                
                # FILTRO: Si es un párrafo que NO debería ser encabezado, omitir
                # Ej: "## A Dios y a la virgencita..." es párrafo, NO encabezado
                is_paragraph_like = (
                    len(text) > 100 or  # Muy largo para ser encabezado
                    (text.startswith('A ') and not text[2:3].isupper()) or  # "A dios...", "A mis..."
                    text.endswith(('.', ','))  # Termina con puntuación (párrafo)
                )
                
                if is_paragraph_like:
                    # No es encabezado, omitir
                    continue
                
                # Detectar patrón semántico
                semantic = self._extract_semantic_level(text)
                
                heading_info[line_num] = HeadingInfo(
                    original_text=text,
                    original_level=level,
                    semantic_level=semantic,
                    numbering_pattern=self._extract_numbering(text),
                    is_detected_heading=True,
                    confidence=0.95,
                    line_number=line_num
                )
            
            # Heurística 1: TEXTO EN MAYÚSCULAS (probablemente encabezado)
            # Pero EVITAR párrafos largos que casualmente comienzan con mayúsculas
            elif (line.strip() and line.isupper() and 10 <= len(line) <= 150 and 
                  not line.startswith('A ') and  # Párrafos "A Dios...", "A mis padres..."
                  not re.match(r'^[A-Z]\s+[a-z]', line)):  # "A mis...", "A nuestros..."
                heading_info[line_num] = HeadingInfo(
                    original_text=line,
                    original_level=2,  # Default H2
                    semantic_level=None,
                    numbering_pattern=None,
                    is_detected_heading=False,
                    confidence=0.70,
                    line_number=line_num
                )
        
        return heading_info
    
    def _extract_semantic_level(self, text: str) -> Optional[Tuple[int, ...]]:
        """
        Extrae nivel semántico de numeración en múltiples formatos.
        
        Soporta:
        - Decimal: 1.2.3 → (1, 2, 3)
        - Letras: A.1, B.2.1 → (10, 1), (11, 2, 1)
        - Romano: I, II.1, III.2.1 → (1,), (2, 1), (3, 2, 1)
        - Palabras: Capítulo 1, Parte II → (1,), (2,)
        - Mixto: 1.A.2 → (1, 10, 2)
        """
        
        # 1. PATRÓN DECIMAL: 1, 1.1, 1.2.3
        decimal_pattern = r'^(\d+(?:\.\d+)*)[.\s:]+'
        match = re.match(decimal_pattern, text)
        if match:
            numbering = match.group(1)
            parts = tuple(int(x) for x in numbering.split('.'))
            return parts
        
        # 2. PATRÓN CON LETRAS: A, A.1, B.2.3
        # Formato común en apéndices, anexos
        letter_pattern = r'^([A-Z])(?:\.(\d+(?:\.\d+)*))?[.\s:]+'
        match = re.match(letter_pattern, text)
        if match:
            letter = match.group(1)
            # Convertir letra a número (A=1, B=2, ..., Z=26)
            # Para distinguir de números normales, usar offset 100
            letter_num = ord(letter) - ord('A') + 100
            
            if match.group(2):  # Hay números después: A.1.2
                sub_nums = tuple(int(x) for x in match.group(2).split('.'))
                return (letter_num,) + sub_nums
            else:  # Solo letra: A
                return (letter_num,)
        
        # 3. PATRÓN ROMANO: I, II, III, IV, etc.
        # Común en capítulos de libros, partes principales
        roman_pattern = r'^([IVXLCDMivxlcdm]+)[.\s:]+'
        match = re.match(roman_pattern, text)
        if match:
            roman = match.group(1).upper()
            try:
                num = self._roman_to_int(roman)
                # Usar offset 200 para distinguir de otros tipos
                return (200 + num,)
            except ValueError:
                pass  # No es romano válido
        
        # 4. PALABRAS CLAVE: "Capítulo 1", "Parte II", "Sección A"
        keyword_patterns = [
            (r'^(?:Capítulo|Chapter|CAPÍTULO|CHAPTER)\s+(\d+)', 1),  # Capítulo 1
            (r'^(?:Capítulo|Chapter|CAPÍTULO|CHAPTER)\s+([IVX]+)', 200),  # Capítulo I
            (r'^(?:Parte|Part|PARTE|PART)\s+(\d+)', 1),  # Parte 1
            (r'^(?:Parte|Part|PARTE|PART)\s+([IVX]+)', 200),  # Parte II
            (r'^(?:Sección|Section|SECCIÓN|SECTION)\s+(\d+)', 1),  # Sección 1
            (r'^(?:Sección|Section|SECCIÓN|SECTION)\s+([A-Z])', 100),  # Sección A
            (r'^(?:Apéndice|Appendix|APÉNDICE|APPENDIX)\s+([A-Z])', 100),  # Apéndice A
            (r'^(?:Anexo|Annex|ANEXO|ANNEX)\s+(\d+)', 1),  # Anexo 1
        ]
        
        for pattern, offset in keyword_patterns:
            match = re.match(pattern, text)
            if match:
                value = match.group(1)
                if value.isdigit():
                    return (int(value) + offset - 1,)  # offset=1 no cambia
                elif value.isalpha() and value.isupper():
                    if offset == 200:  # Romano
                        try:
                            return (offset + self._roman_to_int(value),)
                        except ValueError:
                            pass
                    elif offset == 100:  # Letra
                        return (offset + ord(value) - ord('A'),)
        
        return None
    
    def _extract_numbering(self, text: str) -> Optional[str]:
        """Extrae string de numeración en cualquier formato."""
        
        # Probar múltiples patrones
        patterns = [
            r'^(\d+(?:\.\d+)*)',  # 1.2.3
            r'^([A-Z](?:\.\d+)*)',  # A.1.2
            r'^([IVXLCDMivxlcdm]+)',  # I, II, III
            r'^(?:Capítulo|Chapter|CAPÍTULO|CHAPTER)\s+(\d+|[IVX]+)',
            r'^(?:Parte|Part|PARTE|PART)\s+(\d+|[IVX]+)',
            r'^(?:Sección|Section|SECCIÓN|SECTION)\s+(\d+|[A-Z])',
            r'^(?:Apéndice|Appendix|APÉNDICE|APPENDIX)\s+([A-Z])',
            r'^(?:Anexo|Annex|ANEXO|ANNEX)\s+(\d+)',
        ]
        
        for pattern in patterns:
            match = re.match(pattern, text)
            if match:
                return match.group(1)
        
        return None
    
    def _roman_to_int(self, roman: str) -> int:
        """Convierte números romanos a enteros."""
        roman_values = {
            'I': 1, 'V': 5, 'X': 10, 'L': 50, 
            'C': 100, 'D': 500, 'M': 1000
        }
        
        total = 0
        prev_value = 0
        
        for char in reversed(roman.upper()):
            if char not in roman_values:
                raise ValueError(f"Carácter romano inválido: {char}")
            
            value = roman_values[char]
            if value < prev_value:
                total -= value
            else:
                total += value
            prev_value = value
        
        # Validar rango razonable para encabezados
        if total < 1 or total > 100:
            raise ValueError(f"Número romano fuera de rango: {total}")
        
        return total
    
    # ========== FASE 3: ANÁLISIS DE PROFUNDIDAD ==========
    
    def _phase3_analyze_hierarchy(self, heading_info: Dict[int, HeadingInfo]) -> Dict:
        """
        Mapea niveles semánticos a niveles markdown.
        
        Considera:
        - Profundidad (número de niveles)
        - Rango de valores (detectar si es decimal, letra, romano)
        - Presencia de H1 existente
        """
        
        heading_map = {}
        
        # Extraer todos los niveles semánticos y sus valores
        semantic_depths = {}  # {depth: [valores]}
        has_h1 = False
        
        for info in heading_info.values():
            if info.original_level == 1:
                has_h1 = True
            
            if info.semantic_level:
                depth = len(info.semantic_level)
                first_value = info.semantic_level[0]
                
                if depth not in semantic_depths:
                    semantic_depths[depth] = []
                semantic_depths[depth].append(first_value)
        
        if not semantic_depths:
            return {}
        
        # Determinar estrategia de mapeo
        sorted_depths = sorted(semantic_depths.keys())
        
        # Detectar tipo de numeración predominante
        all_first_values = []
        for values in semantic_depths.values():
            all_first_values.extend(values)
        
        # Offset base según si hay H1 y tipo de numeración
        if has_h1:
            # Ya existe H1, empezar desde H2
            base_offset = 2
        else:
            # Decidir según valores
            if all_first_values:
                max_val = max(all_first_values)
                if max_val >= 200:  # Romano (offset 200)
                    base_offset = 1  # Capítulos romanos como H1
                elif max_val >= 100:  # Letras (offset 100)
                    base_offset = 2  # Apéndices como H2
                else:  # Decimal normal
                    base_offset = 2  # Dejar H1 para título potencial
            else:
                base_offset = 2
        
        # Crear mapeo: profundidad → nivel H
        for i, depth in enumerate(sorted_depths):
            markdown_level = base_offset + i
            heading_map[depth] = min(markdown_level, 6)  # H6 máximo
        
        logger.info(f"  Mapeo de profundidad: {heading_map}")
        logger.info(f"  Offset base: {base_offset} (has_h1={has_h1})")
        
        return heading_map
    
    # ========== FASE 4: APLICAR NORMALIZACIÓN ==========
    
    def _phase4_apply_normalization(self, lines: List[str], 
                                     heading_info: Dict[int, HeadingInfo]) -> List[str]:
        """Aplica normalización de jerarquía."""
        
        normalized_lines = []
        
        for line_num, line in enumerate(lines):
            if line_num in heading_info:
                info = heading_info[line_num]
                
                # Determinar nivel correcto
                if info.semantic_level:
                    depth = len(info.semantic_level)
                    new_level = self.heading_map.get(depth, depth + 1)
                    
                    # Log información de transformación
                    if depth in self.heading_map:
                        self.changes_log.append({
                            "line": line_num,
                            "type": "semantic_mapping",
                            "semantic_level": info.semantic_level,
                            "depth": depth,
                            "mapped_to": f"H{new_level}",
                            "numbering": info.numbering_pattern
                        })
                else:
                    # Sin numeración semántica, mantener original
                    new_level = info.original_level
                
                # Reconstruir línea
                new_hashes = '#' * new_level
                normalized_line = f"{new_hashes} {info.original_text}"
                
                # Log de cambios de nivel
                if new_level != info.original_level:
                    self.changes_log.append({
                        "line": line_num,
                        "type": "heading_level_change",
                        "from": f"H{info.original_level}",
                        "to": f"H{new_level}",
                        "text": info.original_text[:50],
                        "reason": "semantic_depth_mapping" if info.semantic_level else "unknown"
                    })
                
                normalized_lines.append(normalized_line)
            else:
                normalized_lines.append(line)
        
        return normalized_lines
    
    # ========== FASE 5: FUSIÓN DE LÍNEAS FRAGMENTADAS ==========
    
    def _phase5_merge_fragmented_lines(self, lines: List[str]) -> List[str]:
        """Fusiona líneas fragmentadas que pertenecen al mismo párrafo."""
        
        merged = []
        i = 0
        
        while i < len(lines):
            current = lines[i]
            
            # Si es encabezado o línea en blanco, dejar como está
            if current.startswith('#') or not current.strip():
                merged.append(current)
                i += 1
                continue
            
            # Heurística: ¿próxima línea continúa este párrafo?
            # Indicadores:
            # 1. Línea actual NO termina con puntuación fuerte
            # 2. Próxima línea NO es encabezado
            # 3. Próxima línea NO comienza con mayúscula (nueva oración)
            
            while i + 1 < len(lines):
                next_line = lines[i + 1]
                
                # Verificar si próxima línea existe y no está vacía
                if not next_line.strip():
                    i += 1
                    continue
                
                # ¿Debe fusionar?
                should_merge = (
                    current.strip() and  # Línea actual no vacía
                    not next_line.startswith('#') and  # No es encabezado
                    not current.rstrip().endswith(('.', '!', '?', ':', ';')) and  # No termina con puntuación
                    (len(next_line) > 0 and not next_line[0].isupper())  # Próxima NO comienza con mayúscula
                )
                
                if should_merge:
                    current = current.rstrip() + " " + next_line.strip()
                    i += 1
                    
                    self.changes_log.append({
                        "type": "line_merge",
                        "result": current[:60] + "..." if len(current) > 60 else current
                    })
                else:
                    break
            
            merged.append(current)
            i += 1
        
        return merged
    
    # ========== VALIDACIÓN ==========
    
    def _validate(self, markdown: str) -> Dict:
        """Valida fidelidad del markdown."""
        
        checks = {
            "has_h1": bool(re.search(r'^#\s+', markdown, re.MULTILINE)),
            "no_duplicate_hashes": not bool(re.search(r'^###+\s*##', markdown, re.MULTILINE)),
            "valid_hierarchy": self._check_valid_hierarchy(markdown),
            "no_metadata_markers": not bool(re.search(r'^#{1,6}\s*(?:Página|Page)\s*\d', markdown, re.MULTILINE)),
            "proper_spacing": not bool(re.search(r'\n\n\n+', markdown))
        }
        
        score = sum(checks.values()) / len(checks) * 100
        
        return {
            "fidelity_score": score,
            "checks": checks,
            "warnings": [k for k, v in checks.items() if not v]
        }
    
    def _check_valid_hierarchy(self, markdown: str) -> bool:
        """Valida que la jerarquía sea semánticamente correcta."""
        
        current_level = 0
        for match in re.finditer(r'^(#+)\s', markdown, re.MULTILINE):
            level = len(match.group(1))
            
            # Primer encabezado puede ser cualquier nivel
            if current_level == 0:
                current_level = level
                continue
            
            # No puede saltar más de un nivel hacia abajo
            if level > current_level + 1:
                logger.warning(f"⚠️  Salto de jerarquía: H{current_level} → H{level}")
                return False
            
            current_level = level
        
        return True


def normalize_markdown_file(markdown_path: Path, 
                            output_path: Optional[Path] = None) -> Dict:
    """Normaliza un archivo markdown."""
    
    # Leer markdown
    with open(markdown_path, 'r', encoding='utf-8') as f:
        markdown = f.read()
    
    # Normalizar
    normalizer = MarkdownNormalizer()
    result = normalizer.normalize(markdown)
    
    # Guardar
    if output_path is None:
        output_path = markdown_path.parent / f"{markdown_path.stem}_normalized.md"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result['markdown'])
    
    # Guardar reporte
    report_path = output_path.parent / f"{output_path.stem}_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            "validation": result['validation'],
            "changes_count": len(result['changes']),
            "changes": result['changes'][:20]  # Primeros 20 cambios
        }, f, indent=2, ensure_ascii=False)
    
    logger.info(f"✅ Markdown normalizado guardado en: {output_path}")
    logger.info(f"📊 Reporte en: {report_path}")
    
    return result


if __name__ == "__main__":
    # Test con documento de ejemplo
    test_markdown = """## Página 1

## UNIVERSIDAD PRIVADA DE TACNA

FACULTAD DE INGENIERÍA

---

## CAPÍTULO I: EL PROBLEMA DE INVESTIGACIÓN

### 1.1 Descripción del problema

Este es un párrafo que describe el problema. El texto continúa
en la siguiente línea debido a salto de página.

## 1.2.1 Problema general

Este encabezado debería ser H4 (####) no H2.

### 1.3 Justificación e Importancia

## 1.3.1 Desde el punto de vista económico

Este también debería ser H4.

## Página 2

## CAPÍTULO II: MARCO TEÓRICO

### 2.1 Antecedentes

Texto del marco teórico.
"""
    
    normalizer = MarkdownNormalizer()
    result = normalizer.normalize(test_markdown)
    
    print("\n" + "="*60)
    print("MARKDOWN NORMALIZADO:")
    print("="*60)
    print(result['markdown'])
    
    print("\n" + "="*60)
    print("VALIDACIÓN:")
    print("="*60)
    print(json.dumps(result['validation'], indent=2, ensure_ascii=False))
    
    print("\n" + "="*60)
    print("CAMBIOS APLICADOS:")
    print("="*60)
    for i, change in enumerate(result['changes'][:10], 1):
        print(f"{i}. {change}")

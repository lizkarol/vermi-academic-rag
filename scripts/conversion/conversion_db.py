#!/usr/bin/env python3
"""
conversion_db.py
Sistema de base de datos SQLite para tracking de conversiones PDF→Markdown
"""
import sqlite3
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class ConversionTracker:
    """Gestiona el tracking de conversiones PDF en base de datos SQLite."""
    
    def __init__(self, db_dir: str = "sources/metadata"):
        """
        Inicializa tracker.
        
        Args:
            db_dir: Directorio donde se guardará conversion_tracker.db
        """
        db_dir_path = Path(db_dir)
        db_dir_path.mkdir(parents=True, exist_ok=True)
        self.db_path = db_dir_path / "conversion_tracker.db"
        self.conn = None
        self._init_db()
    
    def _init_db(self):
        """Inicializa la base de datos con tablas necesarias."""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        
        # Tabla principal de conversiones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pdf_filename TEXT NOT NULL,
                pdf_path TEXT NOT NULL,
                pdf_hash TEXT NOT NULL UNIQUE,
                pdf_size_bytes INTEGER,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                markdown_path TEXT,
                pages INTEGER,
                has_tables BOOLEAN DEFAULT 0,
                has_equations BOOLEAN DEFAULT 0,
                is_scanned BOOLEAN DEFAULT 0,
                language TEXT DEFAULT 'unknown',
                conversion_time_seconds REAL,
                confidence_score INTEGER DEFAULT 0,
                notes TEXT,
                pdf_type TEXT DEFAULT 'unknown',
                profile_used TEXT,
                fidelity_score REAL
            )
        """)
        
        # Tabla de reportes de validación
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS validation_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversion_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                structure_ok BOOLEAN,
                ocr_quality INTEGER,
                tables_ok BOOLEAN,
                confidence INTEGER,
                validator TEXT DEFAULT 'gemma3:12b',
                report_json TEXT,
                FOREIGN KEY (conversion_id) REFERENCES conversions(id)
            )
        """)
        
        # Tabla de errores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversion_errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversion_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                error_type TEXT NOT NULL,
                error_message TEXT NOT NULL,
                step TEXT,
                FOREIGN KEY (conversion_id) REFERENCES conversions(id)
            )
        """)
        
        # Índices para búsqueda rápida
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_pdf_hash 
            ON conversions(pdf_hash)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_status 
            ON conversions(status)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_created_at 
            ON conversions(created_at)
        """)
        
        self.conn.commit()
        logger.info(f"Base de datos inicializada: {self.db_path}")
    
    def _calculate_hash(self, pdf_path: Path) -> str:
        """Calcula SHA-256 hash del PDF para detección de duplicados."""
        sha256_hash = hashlib.sha256()
        with open(pdf_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def is_duplicate(self, pdf_path: Path) -> Tuple[bool, Optional[int]]:
        """
        Verifica si el PDF ya fue procesado.
        
        Returns:
            (is_duplicate, conversion_id): Tupla con booleano y ID si existe
        """
        pdf_hash = self._calculate_hash(pdf_path)
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, status FROM conversions WHERE pdf_hash = ?",
            (pdf_hash,)
        )
        result = cursor.fetchone()
        
        if result:
            return True, result['id']
        return False, None
    
    def add_conversion(
        self,
        pdf_path: Path,
        status: str = "pending",
        **kwargs
    ) -> int:
        """
        Registra una nueva conversión en la base de datos.
        
        Args:
            pdf_path: Ruta del PDF
            status: Estado inicial (pending, processing, success, failed)
            **kwargs: Campos adicionales (pages, has_tables, etc.)
        
        Returns:
            conversion_id: ID del registro creado
        """
        pdf_hash = self._calculate_hash(pdf_path)
        pdf_size = pdf_path.stat().st_size
        now = datetime.utcnow().isoformat()
        
        cursor = self.conn.cursor()
        
        # Verificar duplicado
        is_dup, existing_id = self.is_duplicate(pdf_path)
        if is_dup:
            logger.warning(f"PDF duplicado detectado: {pdf_path.name} (ID: {existing_id})")
            return existing_id
        
        cursor.execute("""
            INSERT INTO conversions (
                pdf_filename, pdf_path, pdf_hash, pdf_size_bytes,
                status, created_at, updated_at,
                pages, has_tables, has_equations, is_scanned,
                language, notes, pdf_type, profile_used, fidelity_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pdf_path.name,
            str(pdf_path),
            pdf_hash,
            pdf_size,
            status,
            now,
            now,
            kwargs.get('pages', 0),
            kwargs.get('has_tables', False),
            kwargs.get('has_equations', False),
            kwargs.get('is_scanned', False),
            kwargs.get('language', 'unknown'),
            kwargs.get('notes', ''),
            kwargs.get('pdf_type', 'unknown'),
            kwargs.get('profile_used'),
            kwargs.get('fidelity_score')
        ))
        
        self.conn.commit()
        conversion_id = cursor.lastrowid
        logger.info(f"Conversión registrada: {pdf_path.name} (ID: {conversion_id})")
        return conversion_id
    
    def update_conversion(
        self,
        conversion_id: int,
        status: Optional[str] = None,
        **kwargs
    ):
        """
        Actualiza un registro de conversión.
        
        Args:
            conversion_id: ID del registro
            status: Nuevo estado (opcional)
            **kwargs: Campos a actualizar
        """
        now = datetime.utcnow().isoformat()
        cursor = self.conn.cursor()
        
        # Construir query dinámicamente
        updates = ["updated_at = ?"]
        values = [now]
        
        if status:
            updates.append("status = ?")
            values.append(status)
        
        for key, value in kwargs.items():
            updates.append(f"{key} = ?")
            values.append(value)
        
        values.append(conversion_id)
        
        query = f"UPDATE conversions SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, values)
        self.conn.commit()
        logger.info(f"Conversión actualizada: ID {conversion_id}")
    
    def add_validation_report(
        self,
        conversion_id: int,
        structure_ok: bool,
        ocr_quality: int,
        tables_ok: bool,
        confidence: int,
        report_json: Dict,
        validator: str = "gemma3:12b"
    ):
        """Registra un reporte de validación."""
        now = datetime.utcnow().isoformat()
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO validation_reports (
                conversion_id, created_at, structure_ok, ocr_quality,
                tables_ok, confidence, validator, report_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            conversion_id,
            now,
            structure_ok,
            ocr_quality,
            tables_ok,
            confidence,
            validator,
            json.dumps(report_json, ensure_ascii=False)
        ))
        
        self.conn.commit()
        logger.info(f"Reporte de validación registrado para conversión ID {conversion_id}")
    
    def add_error(
        self,
        conversion_id: int,
        error_type: str,
        error_message: str,
        step: Optional[str] = None
    ):
        """Registra un error de conversión."""
        now = datetime.utcnow().isoformat()
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO conversion_errors (
                conversion_id, created_at, error_type, error_message, step
            ) VALUES (?, ?, ?, ?, ?)
        """, (conversion_id, now, error_type, error_message, step or 'unknown'))
        
        self.conn.commit()
        logger.error(f"Error registrado para conversión ID {conversion_id}: {error_type}")
    
    def get_conversion(self, conversion_id: int) -> Optional[Dict]:
        """Obtiene un registro de conversión por ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM conversions WHERE id = ?", (conversion_id,))
        result = cursor.fetchone()
        return dict(result) if result else None
    
    def get_conversions_by_status(self, status: str) -> List[Dict]:
        """Obtiene todas las conversiones con un estado específico."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM conversions WHERE status = ?", (status,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict:
        """Genera estadísticas de conversiones."""
        cursor = self.conn.cursor()
        
        stats = {
            "total_conversions": 0,
            "by_status": {},
            "average_confidence": 0,
            "total_pages": 0,
            "total_size_mb": 0,
            "with_tables": 0,
            "with_equations": 0,
            "scanned_pdfs": 0
        }
        
        # Total conversiones
        cursor.execute("SELECT COUNT(*) as count FROM conversions")
        stats["total_conversions"] = cursor.fetchone()['count']
        
        # Por estado
        cursor.execute("SELECT status, COUNT(*) as count FROM conversions GROUP BY status")
        stats["by_status"] = {row['status']: row['count'] for row in cursor.fetchall()}
        
        # Promedios y totales
        cursor.execute("""
            SELECT 
                AVG(confidence_score) as avg_conf,
                SUM(pages) as total_pages,
                SUM(pdf_size_bytes) as total_bytes,
                SUM(CASE WHEN has_tables = 1 THEN 1 ELSE 0 END) as with_tables,
                SUM(CASE WHEN has_equations = 1 THEN 1 ELSE 0 END) as with_equations,
                SUM(CASE WHEN is_scanned = 1 THEN 1 ELSE 0 END) as scanned
            FROM conversions
        """)
        result = cursor.fetchone()
        
        if result:
            stats["average_confidence"] = round(result['avg_conf'] or 0, 2)
            stats["total_pages"] = result['total_pages'] or 0
            stats["total_size_mb"] = round((result['total_bytes'] or 0) / (1024 * 1024), 2)
            stats["with_tables"] = result['with_tables'] or 0
            stats["with_equations"] = result['with_equations'] or 0
            stats["scanned_pdfs"] = result['scanned'] or 0
        
        return stats
    
    def close(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()
            logger.info("Base de datos cerrada")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Funciones auxiliares para uso rápido
def get_tracker(db_path: str = "sources/metadata/conversion_tracker.db") -> ConversionTracker:
    """Factory function para obtener tracker."""
    return ConversionTracker(db_path)


if __name__ == "__main__":
    # Test básico
    logging.basicConfig(level=logging.INFO)
    
    with ConversionTracker() as tracker:
        print("✅ Base de datos inicializada correctamente")
        print(f"📊 Ubicación: {tracker.db_path}")
        
        stats = tracker.get_statistics()
        print(f"\n📈 Estadísticas:")
        print(f"  Total conversiones: {stats['total_conversions']}")
        print(f"  Por estado: {stats['by_status']}")

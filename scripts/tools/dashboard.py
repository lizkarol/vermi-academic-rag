#!/usr/bin/env python3
"""
Dashboard CLI para visualizar metadatos de conversiones PDF→Markdown

Funcionalidades:
- Listar conversiones recientes
- Detectar PDFs duplicados
- Estadísticas por perfil
- Detalle de conversión específica

Uso:
    python dashboard.py --list
    python dashboard.py --duplicates
    python dashboard.py --stats
    python dashboard.py --detail 5

Autor: VermiKhipu Academic RAG Team
Fecha: Noviembre 3, 2025
"""

import sys
import argparse
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# Agregar path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / "conversion"))

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
    from rich.progress import track
except ImportError:
    print("❌ Error: rich no instalado")
    print("Instalar con: pip install rich")
    sys.exit(1)

try:
    from conversion_db import ConversionTracker
except ImportError:
    print("❌ Error: No se puede importar ConversionTracker")
    print("Verificar que conversion_db.py existe en scripts/conversion/")
    sys.exit(1)


class ConversionDashboard:
    """Dashboard CLI para visualizar conversiones."""
    
    def __init__(self, metadata_dir: str = "sources/metadata"):
        """
        Inicializa el dashboard.
        
        Args:
            metadata_dir: Directorio con conversion_tracker.db
        """
        self.metadata_dir = Path(metadata_dir)
        
        # Verificar que existe el directorio
        if not self.metadata_dir.exists():
            # Intentar alternativas
            alt_paths = [
                Path("sources/metadata"),
                Path("data/metadata"),
                Path(__file__).parent.parent.parent / "sources/metadata"
            ]
            
            for alt_path in alt_paths:
                if alt_path.exists():
                    self.metadata_dir = alt_path
                    break
            else:
                raise FileNotFoundError(
                    f"No se encontró el directorio de metadata.\n"
                    f"Buscado en: {metadata_dir}\n"
                    f"Alternativas: {[str(p) for p in alt_paths]}"
                )
        
        self.tracker = ConversionTracker(str(self.metadata_dir))
        self.console = Console()
    
    def show_conversions(self, limit: int = 50):
        """Muestra tabla unificada con todas las conversiones y duplicados marcados."""
        try:
            conversions = self._get_all_conversions_with_duplicates(limit)
        except Exception as e:
            self.console.print(f"[red]❌ Error obteniendo conversiones: {e}[/red]")
            return
        
        if not conversions:
            self.console.print("[yellow]⚠️  No se encontraron conversiones[/yellow]")
            return
        
        # Construir mapa de duplicados
        duplicates_map = {}
        for conv in conversions:
            hash_val = conv.get('pdf_hash')
            if hash_val:
                if hash_val not in duplicates_map:
                    duplicates_map[hash_val] = []
                duplicates_map[hash_val].append(conv['id'])
        
        # Identificar qué hashes tienen duplicados
        duplicate_hashes = {h: ids for h, ids in duplicates_map.items() if len(ids) > 1}
        
        table = Table(
            title=f"📊 Todas las Conversiones (últimas {len(conversions)}) - Duplicados en [red bold]ROJO[/red bold]",
            box=box.ROUNDED
        )
        table.add_column("ID", style="cyan", width=5)
        table.add_column("Archivo", style="green", width=30)
        table.add_column("Tipo", style="yellow", width=8)
        table.add_column("Perfil", style="magenta", width=18)
        table.add_column("Fidelidad", style="blue", justify="right", width=10)
        table.add_column("Tiempo", style="white", justify="right", width=8)
        table.add_column("Fecha", style="dim", width=10)
        table.add_column("Duplicado", style="red", width=12)
        
        for conv in conversions:
            conv_id = str(conv.get('id', 'N/A'))
            filename = conv.get('filename', 'N/A')[:27] + '...' if len(conv.get('filename', '')) > 30 else conv.get('filename', 'N/A')
            pdf_type = conv.get('pdf_type', 'N/A').upper()
            profile = conv.get('profile_used') or 'sin perfil'
            profile = profile[:15] + '...' if len(profile) > 18 else profile
            
            # Fidelidad
            fidelity = conv.get('fidelity_score')
            fidelity_str = f"{fidelity:.1f}%" if fidelity else "N/A"
            
            # Tiempo
            elapsed = conv.get('elapsed_time')
            time_str = f"{elapsed:.1f}s" if elapsed else "N/A"
            
            # Fecha
            timestamp = conv.get('timestamp', '')
            date_str = timestamp[:10] if timestamp else "N/A"
            
            # Verificar si es duplicado
            pdf_hash = conv.get('pdf_hash')
            is_duplicate = pdf_hash in duplicate_hashes
            duplicate_str = ""
            
            if is_duplicate:
                # Encontrar IDs de duplicados
                dup_ids = [str(id) for id in duplicate_hashes[pdf_hash] if id != conv['id']]
                if dup_ids:
                    duplicate_str = f"IDs: {','.join(dup_ids)}"
                
                # Marcar toda la fila en rojo si es duplicado
                conv_id = f"[red bold]{conv_id}[/red bold]"
                filename = f"[red]{filename}[/red]"
                pdf_type = f"[red]{pdf_type}[/red]"
                profile = f"[red]{profile}[/red]"
                time_str = f"[red]{time_str}[/red]"
                date_str = f"[red]{date_str}[/red]"
                
                # Color de fidelidad
                if fidelity and fidelity >= 90:
                    fidelity_str = f"[red bold]{fidelity_str}[/red bold]"
                elif fidelity and fidelity >= 70:
                    fidelity_str = f"[red]{fidelity_str}[/red]"
                elif fidelity:
                    fidelity_str = f"[red dim]{fidelity_str}[/red dim]"
                else:
                    fidelity_str = f"[red]{fidelity_str}[/red]"
            else:
                # Color según fidelidad (no duplicado)
                if fidelity and fidelity >= 90:
                    fidelity_str = f"[green]{fidelity_str}[/green]"
                elif fidelity and fidelity >= 70:
                    fidelity_str = f"[yellow]{fidelity_str}[/yellow]"
                elif fidelity:
                    fidelity_str = f"[dim]{fidelity_str}[/dim]"
            
            table.add_row(
                conv_id,
                filename,
                pdf_type,
                profile,
                fidelity_str,
                time_str,
                date_str,
                duplicate_str
            )
        
        self.console.print(table)
        
        # Resumen de duplicados
        if duplicate_hashes:
            self.console.print(f"\n[red]⚠️  {len(duplicate_hashes)} grupos de duplicados detectados[/red]")
        else:
            self.console.print(f"\n[green]✅ No se detectaron duplicados[/green]")
        
        self.console.print(f"\n💡 Ver detalle: [cyan]python dashboard.py --detail <ID>[/cyan]")
    
    def show_duplicates(self):
        """Detecta y muestra PDFs duplicados."""
        try:
            duplicates = self._find_duplicates()
        except Exception as e:
            self.console.print(f"[red]❌ Error detectando duplicados: {e}[/red]")
            return
        
        if not duplicates:
            self.console.print("\n[green]✅ No se encontraron PDFs duplicados[/green]")
            return
        
        panel = Panel.fit(
            f"⚠️  Se encontraron [yellow]{len(duplicates)}[/yellow] grupos de PDFs duplicados\n"
            f"(mismo contenido, posiblemente diferentes nombres)",
            style="yellow",
            border_style="yellow"
        )
        self.console.print("\n", panel)
        
        for i, group in enumerate(duplicates, 1):
            table = Table(
                title=f"Grupo {i}: Hash {group['hash'][:16]}...",
                box=box.SIMPLE
            )
            table.add_column("Archivo", style="cyan")
            table.add_column("Conversiones", style="green", justify="center")
            table.add_column("Última conversión", style="white")
            
            for pdf in group['files']:
                table.add_row(
                    pdf['filename'][:50],
                    str(pdf.get('conversion_count', 1)),
                    pdf.get('last_conversion', 'N/A')[:10]
                )
            
            self.console.print(table)
            self.console.print()
    
    def show_profile_stats(self):
        """Estadísticas por perfil."""
        try:
            stats = self._get_profile_stats()
        except Exception as e:
            self.console.print(f"[red]❌ Error obteniendo estadísticas: {e}[/red]")
            return
        
        if not stats:
            self.console.print("[yellow]⚠️  No hay estadísticas disponibles[/yellow]")
            return
        
        table = Table(
            title="📈 Estadísticas por Perfil de Conversión",
            box=box.ROUNDED
        )
        table.add_column("Perfil", style="cyan", width=30)
        table.add_column("Usos", style="green", justify="right")
        table.add_column("Fidelidad Promedio", style="blue", justify="right")
        table.add_column("Tiempo Promedio", style="yellow", justify="right")
        
        # Ordenar por uso
        stats_sorted = sorted(stats, key=lambda x: x['count'], reverse=True)
        
        for stat in stats_sorted:
            profile = stat['profile'] or 'sin perfil'
            count = str(stat['count'])
            
            avg_fidelity = stat.get('avg_fidelity')
            fidelity_str = f"{avg_fidelity:.1f}%" if avg_fidelity else "N/A"
            
            avg_time = stat.get('avg_time')
            time_str = f"{avg_time:.1f}s" if avg_time else "N/A"
            
            table.add_row(profile, count, fidelity_str, time_str)
        
        self.console.print("\n", table)
    
    def show_conversion_detail(self, conversion_id: int):
        """Muestra detalle completo de una conversión."""
        try:
            conv = self._get_conversion_by_id(conversion_id)
        except Exception as e:
            self.console.print(f"[red]❌ Error obteniendo conversión: {e}[/red]")
            return
        
        if not conv:
            self.console.print(f"[red]❌ No se encontró conversión con ID {conversion_id}[/red]")
            return
        
        # Panel principal
        title = f"📄 Conversión #{conversion_id}: {conv.get('filename', 'N/A')}"
        
        details = []
        details.append(f"[cyan]Archivo:[/cyan] {conv.get('filepath', 'N/A')}")
        details.append(f"[cyan]Tipo PDF:[/cyan] {conv.get('pdf_type', 'N/A')}")
        details.append(f"[cyan]Estrategia:[/cyan] {conv.get('strategy', 'N/A')}")
        details.append(f"[cyan]Perfil usado:[/cyan] {conv.get('profile_used') or 'sin perfil'}")
        details.append(f"[cyan]Estado:[/cyan] {conv.get('status', 'N/A')}")
        details.append(f"[cyan]Hash SHA-256:[/cyan] {conv.get('file_hash', 'N/A')[:32]}...")
        details.append("")
        details.append(f"[yellow]Fidelidad:[/yellow] {conv.get('fidelity_score', 0):.1f}%")
        details.append(f"[yellow]Tiempo:[/yellow] {conv.get('elapsed_time', 0):.2f}s")
        details.append(f"[yellow]Fecha:[/yellow] {conv.get('timestamp', 'N/A')}")
        
        # Notas si existen
        notes = conv.get('notes')
        if notes:
            try:
                notes_dict = json.loads(notes) if isinstance(notes, str) else notes
                details.append("")
                details.append("[magenta]Notas:[/magenta]")
                for key, value in notes_dict.items():
                    details.append(f"  • {key}: {value}")
            except:
                details.append(f"\n[magenta]Notas:[/magenta] {notes}")
        
        panel = Panel(
            "\n".join(details),
            title=title,
            border_style="blue"
        )
        
        self.console.print("\n", panel)
        
        # Buscar reporte de normalización
        reports_dir = self.metadata_dir.parent / "reports"
        filename = conv.get('filename', '')
        report_file = reports_dir / f"{Path(filename).stem}_normalization.json"
        
        if report_file.exists():
            self.console.print(f"\n[green]📊 Reporte de normalización encontrado:[/green] {report_file}")
            try:
                with open(report_file) as f:
                    report = json.load(f)
                
                self.console.print(f"  • Cambios aplicados: {report.get('changes_count', 0)}")
                self.console.print(f"  • Encabezados detectados: {len(report.get('heading_map', {}))}")
                self.console.print(f"  • Fidelidad: {report.get('validation', {}).get('fidelity_score', 0):.1f}%")
            except Exception as e:
                self.console.print(f"[red]  ❌ Error leyendo reporte: {e}[/red]")
    
    # ========== Métodos auxiliares ==========
    
    def _get_all_conversions(self, limit: int = 20) -> List[Dict]:
        """Obtiene conversiones (wrapper con manejo de errores)."""
        cursor = self.tracker.conn.execute("""
            SELECT 
                id, pdf_filename as filename, pdf_path as filepath,
                COALESCE(pdf_type, CASE WHEN is_scanned = 1 THEN 'SCANNED' ELSE 'NATIVE' END) as pdf_type,
                'pdfplumber' as strategy,
                profile_used,
                COALESCE(fidelity_score, confidence_score) as fidelity_score,
                conversion_time_seconds as elapsed_time,
                updated_at as timestamp, status, pdf_hash
            FROM conversions
            ORDER BY updated_at DESC
            LIMIT ?
        """, (limit,))
        
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def _get_all_conversions_with_duplicates(self, limit: int = 50) -> List[Dict]:
        """Obtiene todas las conversiones con información de hash para detectar duplicados."""
        cursor = self.tracker.conn.execute("""
            SELECT 
                id, pdf_filename as filename, pdf_path as filepath,
                COALESCE(pdf_type, CASE WHEN is_scanned = 1 THEN 'scanned' ELSE 'native' END) as pdf_type,
                profile_used,
                COALESCE(fidelity_score, confidence_score) as fidelity_score,
                conversion_time_seconds as elapsed_time,
                updated_at as timestamp, status, pdf_hash
            FROM conversions
            ORDER BY updated_at DESC
            LIMIT ?
        """, (limit,))
        
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def _find_duplicates(self) -> List[Dict]:
        """Detecta duplicados por hash."""
        cursor = self.tracker.conn.execute("""
            SELECT 
                pdf_hash as file_hash,
                COUNT(*) as count,
                GROUP_CONCAT(pdf_filename) as files,
                MAX(updated_at) as last_conversion
            FROM conversions
            WHERE pdf_hash IS NOT NULL
            GROUP BY pdf_hash
            HAVING count > 1
            ORDER BY count DESC
        """)
        
        duplicates = []
        for row in cursor.fetchall():
            file_hash, count, files_str, last_conv = row
            files_list = files_str.split(',')
            
            duplicates.append({
                'hash': file_hash,
                'count': count,
                'files': [
                    {
                        'filename': f,
                        'conversion_count': 1,  # Simplificado
                        'last_conversion': last_conv
                    }
                    for f in files_list
                ]
            })
        
        return duplicates
    
    def _get_profile_stats(self) -> List[Dict]:
        """Estadísticas por perfil."""
        cursor = self.tracker.conn.execute("""
            SELECT 
                CASE WHEN is_scanned = 1 THEN 'SCANNED' ELSE 'NATIVE' END as profile,
                COUNT(*) as count,
                AVG(confidence_score) as avg_fidelity,
                AVG(conversion_time_seconds) as avg_time
            FROM conversions
            WHERE status = 'completed'
            GROUP BY is_scanned
            ORDER BY count DESC
        """)
        
        columns = ['profile', 'count', 'avg_fidelity', 'avg_time']
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def _get_conversion_by_id(self, conversion_id: int) -> Optional[Dict]:
        """Obtiene conversión por ID."""
        cursor = self.tracker.conn.execute("""
            SELECT * FROM conversions WHERE id = ?
        """, (conversion_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))


# ========== CLI ==========

def main():
    parser = argparse.ArgumentParser(
        description="Dashboard CLI para visualizar conversiones PDF→Markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python dashboard.py --list              # Listar conversiones recientes
  python dashboard.py --duplicates        # Detectar PDFs duplicados
  python dashboard.py --stats             # Estadísticas por perfil
  python dashboard.py --detail 5          # Ver detalle de conversión ID 5
  python dashboard.py                     # Vista completa (todo)
        """
    )
    
    parser.add_argument("--list", action="store_true", help="Listar conversiones recientes")
    parser.add_argument("--duplicates", action="store_true", help="Detectar PDFs duplicados")
    parser.add_argument("--stats", action="store_true", help="Estadísticas por perfil")
    parser.add_argument("--detail", type=int, metavar="ID", help="Ver detalle de conversión específica")
    parser.add_argument("--limit", type=int, default=20, help="Límite de conversiones a mostrar (default: 20)")
    parser.add_argument("--metadata-dir", default="sources/metadata", help="Directorio de metadata")
    
    args = parser.parse_args()
    
    # Inicializar dashboard
    try:
        dashboard = ConversionDashboard(args.metadata_dir)
    except Exception as e:
        print(f"❌ Error inicializando dashboard: {e}")
        return 1
    
    # Ejecutar comandos
    try:
        if args.detail:
            dashboard.show_conversion_detail(args.detail)
        elif args.list:
            dashboard.show_conversions(limit=args.limit)
        elif args.duplicates:
            dashboard.show_duplicates()
        elif args.stats:
            dashboard.show_profile_stats()
        else:
            # Vista completa por defecto
            dashboard.console.print("\n[bold cyan]═══════════════════════════════════════════════════[/bold cyan]")
            dashboard.console.print("[bold cyan]    📊 DASHBOARD DE CONVERSIONES PDF→MARKDOWN    [/bold cyan]")
            dashboard.console.print("[bold cyan]═══════════════════════════════════════════════════[/bold cyan]")
            
            dashboard.show_conversions(limit=10)
            dashboard.show_duplicates()
            dashboard.show_profile_stats()
            
            dashboard.console.print("\n[dim]💡 Usa --help para ver más opciones[/dim]\n")
    
    except KeyboardInterrupt:
        dashboard.console.print("\n[yellow]⚠️  Interrumpido por el usuario[/yellow]")
        return 130
    except Exception as e:
        dashboard.console.print(f"\n[red]❌ Error: {e}[/red]")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

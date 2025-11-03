import argparse
import os
import torch
from marker.models import load_all_models
from marker.convert import convert_single_pdf

def convert_pdf_to_md(pdf_path, output_dir):
    """
    Convierte un único archivo PDF a Markdown utilizando el modelo Marker.
    El archivo de salida se guardará en el directorio especificado.
    """
    if not os.path.exists(pdf_path):
        print(f"❌ Error: El archivo PDF no se encuentra en la ruta: {pdf_path}")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Directorio de salida creado en: {output_dir}")

    # Cargar los modelos de Marker. Esto puede tardar la primera vez.
    print("🔄 Cargando modelos de Marker... (Puede tardar unos minutos la primera vez)")
    try:
        model_lst = load_all_models()
    except Exception as e:
        print(f"❌ Error al cargar los modelos de Marker. Asegúrate de que las dependencias están instaladas.")
        print(f"   Puedes necesitar ejecutar: pip install 'marker-sdk[cpu]' o 'marker-sdk[gpu]'")
        print(f"   Error original: {e}")
        return

    # Convertir el PDF
    try:
        print(f"🚀 Convirtiendo el archivo: {os.path.basename(pdf_path)}")
        full_text, out_meta = convert_single_pdf(pdf_path, model_lst)
        
        # Guardar el resultado en un archivo .md
        output_filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".md"
        output_path = os.path.join(output_dir, output_filename)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)
            
        print(f"✅ ¡Conversión completada! Archivo guardado en: {output_path}")
        print(f"   Se detectaron {out_meta['pages']} páginas en el documento.")

    except Exception as e:
        print(f"❌ Ocurrió un error durante la conversión del PDF.")
        print(f"   Asegúrate de que el archivo no esté corrupto y que tienes suficiente memoria.")
        print(f"   Error original: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Convierte un archivo PDF a Markdown localmente usando Marker.",
        epilog="""
        Ejemplo de uso:
        python scripts/convert_pdf_local.py "C:\\ruta\\a\\mi\\documento.pdf" --output_dir sources/markdown
        
        Este script está diseñado para ser usado localmente como parte del flujo de trabajo BYOS.
        NUNCA subas los PDFs o los archivos .md generados (si contienen material con copyright) al repositorio público.
        La carpeta 'sources/' ya está en .gitignore para prevenir subidas accidentales.
        """
    )
    parser.add_argument(
        "pdf_path",
        type=str,
        help="Ruta completa al archivo PDF que se va a convertir."
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="sources/markdown_outputs",
        help="Directorio donde se guardará el archivo .md de salida. Por defecto: 'sources/markdown_outputs'."
    )
    
    args = parser.parse_args()
    convert_pdf_to_md(args.pdf_path, args.output_dir)

if __name__ == "__main__":
    # Verificar si torch está disponible
    try:
        import torch
    except ImportError:
        print("❌ Error: PyTorch no está instalado.")
        print("   Por favor, instálalo siguiendo las instrucciones en https://pytorch.org/get-started/locally/")
        print("   O instala las dependencias completas con: pip install -r scripts/requirements.txt")
        exit(1)
        
    main()

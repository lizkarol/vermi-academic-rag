# Workflow de Ingesta de Datos

Este documento describe el flujo de trabajo para la ingesta de nuevos datos en el dataset, siguiendo el modelo BYOS (Bring Your Own Sources).

## Flujo Híbrido: Local + GitHub

### 1. Proceso de Ingesta Manual (Local)

El proceso comienza en el entorno local del contribuidor para evitar subir material con derechos de autor al repositorio público.

```
PASO 1: Obtener Fuente (LOCAL)
└─ Descargar PDF académico/manual con permiso.
   └─ Almacenar en una carpeta local (ej. `sources/pdfs/`), que está ignorada por Git.

PASO 2: Convertir a Markdown (LOCAL)
└─ Instalar las dependencias necesarias:
   └─ pip install -r scripts/requirements.txt
└─ Ejecutar el script de conversión proporcionado:
   └─ python scripts/convert_pdf_local.py "sources/pdfs/mi_documento.pdf" --output_dir "sources/markdown"
└─ Revisar y limpiar manualmente el archivo .md generado en `sources/markdown/` si es necesario.

PASO 3: Generar Chunks JSON (LOCAL + WEB)
└─ Abrir el script `scripts/generate_cards_local.md`.
└─ Copiar el contenido del archivo .md generado en el paso anterior.
└─ Pegar el contenido en una interfaz de LLM (como Gemini, ChatGPT) junto con el prompt proporcionado.
   └─ El LLM generará un array JSON con los chunks parafraseados y estructurados.
└─ Copiar la salida JSON.

PASO 4: Añadir Chunks al Dataset (LOCAL + REPO)
└─ Abrir el archivo `dataset/chunks_enriched/chunks_enriched_vX.Y.jsonl`.
└─ Pegar los nuevos objetos JSON generados en el archivo.
└─ Guardar el archivo.

PASO 5: Contribuir al Repositorio (GIT)
└─ Crear una nueva rama: `git checkout -b feature/add-chunks-paper-name`
└─ Añadir los cambios: `git add dataset/chunks_enriched/`
└─ Hacer commit: `git commit -m "feat: Add chunks from [Source Name]"`
└─ Subir la rama: `git push origin feature/add-chunks-paper-name`
└─ Abrir un Pull Request en GitHub.
```

### 2. Proceso Automatizado (GitHub Actions)

Una vez que se abre un Pull Request, el sistema de CI/CD toma el control.

```
CI/CD (En GitHub)
├─ Trigger: Pull Request o push a `main`.
├─ Workflow `validate-dataset.yml`:
│  ├─ Validar esquema de los nuevos chunks.
│  ├─ Comprobar duplicados.
│  └─ Realizar análisis de cobertura y semántica (sobre una muestra).
├─ Workflow `test-rag.yml`:
│  └─ Ejecutar pruebas de recuperación para asegurar que los nuevos chunks no rompen el sistema RAG.
└─ Feedback:
   ├─ Si falla: El PR se bloquea y se notifica al autor para que corrija los errores.
   └─ Si tiene éxito: El PR está listo para ser revisado y fusionado por un mantenedor.
```

Este flujo garantiza que solo datos de alta calidad, validados y legalmente seguros se incorporen al dataset principal.


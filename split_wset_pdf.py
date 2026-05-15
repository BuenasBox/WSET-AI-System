"""
WSET L3 PDF Splitter → Markdown Files
=======================================
Extrae cada sección/subtema del PDF y genera archivos .md listos para RAG.

REQUISITOS:
    pip install pdfplumber pypdf

USO:
    python split_wset_pdf.py

SALIDA:
    Carpeta `wset_markdown/` con subcarpetas por sección y un .md por subtema.
"""

import os
import re
import json
import pdfplumber
from pypdf import PdfReader

# ── Configuración ──────────────────────────────────────────────────────────────
PDF_PATH = os.path.join(os.path.dirname(__file__), "knowledge", "official-wset", "study-guide", "WSET_L3_Study_Guide_Official_2026.pdf")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "knowledge", "official-wset", "study-guide", "wset_markdown")
# ──────────────────────────────────────────────────────────────────────────────


def slugify(text: str) -> str:
    """Convierte texto a nombre de archivo seguro."""
    text = text.lower().strip()
    text = re.sub(r"[áàäâ]", "a", text)
    text = re.sub(r"[éèëê]", "e", text)
    text = re.sub(r"[íìïî]", "i", text)
    text = re.sub(r"[óòöô]", "o", text)
    text = re.sub(r"[úùüû]", "u", text)
    text = re.sub(r"[ñ]", "n", text)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s]+", "_", text)
    text = re.sub(r"-+", "-", text)
    return text[:60]


def extract_outline(pdf_path: str):
    """
    Extrae la tabla de contenido (bookmarks) del PDF.
    Devuelve lista de dicts: {title, page, level}
    """
    reader = PdfReader(pdf_path)
    outline_items = []

    def parse_outline(items, level=0):
        for item in items:
            if isinstance(item, list):
                parse_outline(item, level + 1)
            else:
                try:
                    page_num = reader.get_destination_page_number(item)
                    outline_items.append({
                        "title": item.title.strip(),
                        "page": page_num,  # 0-indexed
                        "level": level
                    })
                except Exception:
                    pass

    if reader.outline:
        parse_outline(reader.outline)

    return outline_items


def extract_text_range(pdf_path: str, start_page: int, end_page: int) -> str:
    """Extrae texto de un rango de páginas (ambos inclusive, 0-indexed)."""
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        end_page = min(end_page, total_pages - 1)
        for page_num in range(start_page, end_page + 1):
            page = pdf.pages[page_num]
            page_text = page.extract_text(x_tolerance=2, y_tolerance=2)
            if page_text:
                text_parts.append(f"<!-- página {page_num + 1} -->\n{page_text}")
    return "\n\n".join(text_parts)


def clean_text(text: str) -> str:
    """Limpieza básica del texto extraído."""
    # Elimina líneas con solo números de página
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Saltar líneas que son solo número de página
        if re.match(r"^<!--.*-->$", stripped):
            cleaned.append(line)
            continue
        if re.match(r"^\d{1,3}$", stripped):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def build_markdown(title: str, section_num: str, subtopic_num: str,
                   parent_section: str, text: str) -> str:
    """Genera el contenido Markdown con frontmatter YAML para RAG."""
    # Frontmatter YAML — muy útil para LlamaIndex / LangChain metadata filters
    frontmatter = f"""---
title: "{title}"
section: "{section_num}"
subtopic: "{subtopic_num}"
parent_section: "{parent_section}"
source: "WSET Level 3 Study Guide 2026"
tags: [wset, level3, wine, spirits]
---
"""
    body = f"# {title}\n\n{clean_text(text)}"
    return frontmatter + "\n" + body


def group_into_sections(outline: list) -> list:
    """
    Agrupa los items del outline en secciones (nivel 0) con sus subtemas.
    Devuelve:
        [
          {
            "section": {...},
            "subtopics": [{...}, ...]
          },
          ...
        ]
    """
    sections = []
    current_section = None

    for item in outline:
        if item["level"] == 0:
            current_section = {"section": item, "subtopics": []}
            sections.append(current_section)
        else:
            if current_section is not None:
                current_section["subtopics"].append(item)

    return sections


def process_pdf():
    print(f"\n{'='*60}")
    print("  WSET L3 PDF → Markdown Splitter")
    print(f"{'='*60}\n")

    if not os.path.exists(PDF_PATH):
        print(f"❌ PDF no encontrado en: {PDF_PATH}")
        print("   Asegúrate de que el PDF está en la misma carpeta que este script.")
        return

    print(f"📄 Leyendo: {os.path.basename(PDF_PATH)}")

    # ── 1. Extraer tabla de contenido ─────────────────────────────────────────
    print("📑 Extrayendo tabla de contenido...")
    outline = extract_outline(PDF_PATH)

    if not outline:
        print("⚠️  El PDF no tiene bookmarks embebidos. Usando modo alternativo...")
        # Fallback: extraer ToC de las primeras páginas
        outline = extract_toc_from_text(PDF_PATH)

    if not outline:
        print("❌ No se pudo extraer la tabla de contenido.")
        return

    print(f"   → {len(outline)} entradas encontradas en el índice\n")

    # Mostrar estructura
    for item in outline:
        indent = "  " * item["level"]
        print(f"   {indent}{'📁' if item['level'] == 0 else '📄'} [{item['page']+1:3d}] {item['title']}")

    # ── 2. Agrupar en secciones ───────────────────────────────────────────────
    sections = group_into_sections(outline)
    print(f"\n📊 Estructura detectada: {len(sections)} secciones")
    total_subtopics = sum(len(s["subtopics"]) for s in sections)
    print(f"   Total subtemas: {total_subtopics}\n")

    # ── 3. Crear carpetas de salida ───────────────────────────────────────────
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Guardar índice JSON (útil para el sistema RAG)
    index = []

    # ── 4. Procesar cada sección y subtema ────────────────────────────────────
    with pdfplumber.open(PDF_PATH) as pdf:
        total_pages = len(pdf.pages)
        print(f"📖 PDF total: {total_pages} páginas\n")

    all_items_flat = []
    for s_idx, sec in enumerate(sections):
        all_items_flat.append(sec["section"])
        for sub in sec["subtopics"]:
            all_items_flat.append(sub)

    # Calcular rangos de páginas
    for i, item in enumerate(all_items_flat):
        if i + 1 < len(all_items_flat):
            item["end_page"] = all_items_flat[i + 1]["page"] - 1
        else:
            # Último item — leer hasta el final del PDF
            reader = PdfReader(PDF_PATH)
            item["end_page"] = len(reader.pages) - 1

    # Re-agrupar con rangos
    sections = group_into_sections(all_items_flat)

    files_created = 0
    for s_idx, sec_group in enumerate(sections):
        sec = sec_group["section"]
        subtopics = sec_group["subtopics"]

        section_num = str(s_idx + 1)
        section_slug = slugify(sec["title"])
        section_dir = os.path.join(OUTPUT_DIR, f"seccion_{section_num}_{section_slug}")
        os.makedirs(section_dir, exist_ok=True)

        print(f"📁 Sección {section_num}: {sec['title']} (pp. {sec['page']+1}–{sec['end_page']+1})")

        # Si la sección no tiene subtemas, generar un solo archivo
        items_to_process = subtopics if subtopics else [sec]

        for sub_idx, sub in enumerate(items_to_process):
            sub_num = f"{section_num}.{sub_idx + 1}" if subtopics else section_num
            sub_slug = slugify(sub["title"])
            filename = f"{sub_num.replace('.', '-')}_{sub_slug}.md"
            filepath = os.path.join(section_dir, filename)

            start = sub["page"]
            end = sub["end_page"]

            print(f"   📄 {sub_num} {sub['title'][:50]} (pp. {start+1}–{end+1})...", end=" ")

            text = extract_text_range(PDF_PATH, start, end)

            if not text.strip():
                print("⚠️  sin texto")
                text = "_[Contenido no extraíble — posiblemente imagen o diagrama]_"

            md_content = build_markdown(
                title=sub["title"],
                section_num=section_num,
                subtopic_num=sub_num,
                parent_section=sec["title"],
                text=text
            )

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(md_content)

            print(f"✅ ({len(text):,} chars)")
            files_created += 1

            index.append({
                "file": os.path.relpath(filepath, OUTPUT_DIR),
                "title": sub["title"],
                "section": section_num,
                "subtopic": sub_num,
                "parent_section": sec["title"],
                "start_page": start + 1,
                "end_page": end + 1,
                "char_count": len(text)
            })

    # ── 5. Guardar índice JSON ────────────────────────────────────────────────
    index_path = os.path.join(OUTPUT_DIR, "_index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    # ── 6. Generar README del corpus ─────────────────────────────────────────
    readme_content = f"""# WSET Level 3 — Corpus Markdown para RAG

Generado automáticamente desde: `{os.path.basename(PDF_PATH)}`

## Estructura

```
wset_markdown/
"""
    for s_idx, sec_group in enumerate(sections):
        sec = sec_group["section"]
        section_num = str(s_idx + 1)
        section_slug = slugify(sec["title"])
        readme_content += f"├── seccion_{section_num}_{section_slug}/\n"
        for sub_idx, sub in enumerate(sec_group["subtopics"][:3]):
            sub_num = f"{section_num}.{sub_idx + 1}"
            sub_slug = slugify(sub["title"])
            readme_content += f"│   ├── {sub_num.replace('.', '-')}_{sub_slug[:30]}.md\n"
        if len(sec_group["subtopics"]) > 3:
            readme_content += f"│   └── ... ({len(sec_group['subtopics'])} subtemas)\n"

    readme_content += f"""```

## Estadísticas
- **Archivos generados:** {files_created}
- **Índice JSON:** `_index.json`

## Uso con LlamaIndex

```python
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

documents = SimpleDirectoryReader(
    input_dir="./wset_markdown",
    recursive=True,
    required_exts=[".md"]
).load_data()

index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

response = query_engine.query("¿Cuáles son las principales regiones vinícolas de Burdeos?")
print(response)
```

## Uso con LangChain

```python
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

loader = DirectoryLoader(
    "./wset_markdown",
    glob="**/*.md",
    loader_cls=UnstructuredMarkdownLoader
)
documents = loader.load()

vectorstore = Chroma.from_documents(documents, OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={{"k": 4}})
```

## Metadata por archivo

Cada `.md` incluye YAML frontmatter con:
- `title` — nombre del subtema
- `section` — número de sección (1–5)
- `subtopic` — número de subtema (ej. "2.3")
- `parent_section` — nombre de la sección padre
- `source` — fuente del documento
- `tags` — etiquetas para filtrado
"""

    readme_path = os.path.join(OUTPUT_DIR, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    # ── Resumen final ─────────────────────────────────────────────────────────
    total_chars = sum(item["char_count"] for item in index)
    print(f"\n{'='*60}")
    print(f"✅ COMPLETADO")
    print(f"   Archivos .md creados : {files_created}")
    print(f"   Texto total extraído : {total_chars:,} caracteres (~{total_chars//4:,} tokens)")
    print(f"   Carpeta de salida    : {OUTPUT_DIR}")
    print(f"   Índice JSON          : {index_path}")
    print(f"{'='*60}\n")


def extract_toc_from_text(pdf_path: str) -> list:
    """
    Fallback: intenta extraer ToC de las primeras páginas del PDF
    buscando patrones de índice (texto + número de página).
    """
    outline = []
    toc_pattern = re.compile(r"^(.+?)\s{2,}(\d{1,3})\s*$")

    with pdfplumber.open(pdf_path) as pdf:
        # Buscar en las primeras 15 páginas
        for page_num in range(min(15, len(pdf.pages))):
            page = pdf.pages[page_num]
            text = page.extract_text()
            if not text:
                continue

            lines = text.split("\n")
            for line in lines:
                match = toc_pattern.match(line.strip())
                if match:
                    title = match.group(1).strip()
                    page_ref = int(match.group(2)) - 1  # convertir a 0-indexed
                    # Heurística: títulos cortos (< 80 chars) son entradas de ToC
                    if 5 < len(title) < 80 and page_ref > 0:
                        level = 0 if not title[0].isspace() else 1
                        outline.append({
                            "title": title,
                            "page": page_ref,
                            "level": level
                        })

    # Ordenar por página
    outline.sort(key=lambda x: x["page"])
    return outline


if __name__ == "__main__":
    process_pdf()

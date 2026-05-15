# WSET Level 3 — Corpus Markdown para RAG

Generado automáticamente desde: `WSET_L3_Study_Guide_Official_2026.pdf`

## Estructura

```
wset_markdown/
├── seccion_1_contents/
├── seccion_2_foreword/
├── seccion_3_introduction/
├── seccion_4_section_1_wine_and_the_consumer/
│   ├── 4-1_1_the_systematic_approach_to_t.md
│   ├── 4-2_2_wine_with_food.md
│   ├── 4-3_3_storage_and_service_of_wine.md
├── seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/
│   ├── 5-1_4_the_vine.md
│   ├── 5-2_5_the_growing_environment.md
│   ├── 5-3_6_vineyard_management.md
│   └── ... (8 subtemas)
├── seccion_6_section_3_still_wines_of_the_world/
│   ├── 6-1_12_introduction_to_france.md
│   ├── 6-2_13_bordeaux.md
│   ├── 6-3_14_the_dordogne_and_south_west.md
│   └── ... (29 subtemas)
├── seccion_7_section_4_sparkling_wines_of_the_world/
│   ├── 7-1_41_sparkling_wine_production.md
│   ├── 7-2_42_sparkling_wines_of_the_worl.md
├── seccion_8_section_5_fortified_wines_of_the_world/
│   ├── 8-1_43_sherry.md
│   ├── 8-2_44_port.md
│   ├── 8-3_45_fortified_muscats.md
├── seccion_9_acknowledgements/
├── seccion_10_index/
```

## Estadísticas
- **Archivos generados:** 50
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
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
```

## Metadata por archivo

Cada `.md` incluye YAML frontmatter con:
- `title` — nombre del subtema
- `section` — número de sección (1–5)
- `subtopic` — número de subtema (ej. "2.3")
- `parent_section` — nombre de la sección padre
- `source` — fuente del documento
- `tags` — etiquetas para filtrado

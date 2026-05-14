from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import pdfplumber


ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_ROOT = ROOT / "knowledge" / "official-wset"
OUTPUT_DIR = ROOT / "knowledge" / "enrichment" / "wset_master_dictionary"
TRANSCRIPT_DIR = ROOT / "knowledge" / "wine-with-jimmy" / "chunk-ready"

CSV_COLUMNS = [
    "canonical_term",
    "category",
    "official_source",
    "source_document",
    "ra",
    "aliases",
    "confidence",
    "manually_reviewed",
    "notes",
]


@dataclass(frozen=True)
class SourceDoc:
    official_source: str
    path: Path
    priority: int


SOURCES = [
    SourceDoc(
        "specification",
        OFFICIAL_ROOT / "specification" / "WSET_L3_Specification_Official_2026.pdf",
        1,
    ),
    SourceDoc(
        "sat",
        OFFICIAL_ROOT / "sat" / "WSET_L3_SAT_Official_2016.pdf",
        2,
    ),
    SourceDoc(
        "study-guide",
        OFFICIAL_ROOT / "study-guide" / "WSET_L3_Study_Guide_Official_2026.pdf",
        3,
    ),
]


# Terms are intentionally conservative. They are seed candidates only; a row is
# emitted only when the term or an observed official OCR/accent variant is found
# in one of the local official WSET PDFs.
TERMS: dict[str, set[str]] = {
    "grape_variety": {
        "Agiorgitiko",
        "Aglianico",
        "Airén",
        "Albariño",
        "Alfrocheiro",
        "Alicante Bouschet",
        "Aligoté",
        "Alvarinho",
        "Arinto",
        "Assyrtiko",
        "Baga",
        "Barbera",
        "Blaufränkisch",
        "Bonarda",
        "Cabernet Franc",
        "Cabernet Sauvignon",
        "Carignan",
        "Cariñena",
        "Carmenère",
        "Chardonnay",
        "Chenin Blanc",
        "Cinsault",
        "Corvina",
        "Cortese",
        "Dolcetto",
        "Dornfelder",
        "Fiano",
        "Furmint",
        "Gamay",
        "Garganega",
        "Gewurztraminer",
        "Glera",
        "Graciano",
        "Grenache",
        "Grechetto",
        "Greco",
        "Grüner Veltliner",
        "Hárslevelű",
        "Jaen",
        "Loureiro",
        "Macabeo",
        "Malbec",
        "Malvasia",
        "Marsanne",
        "Mazuelo",
        "Melon Blanc",
        "Mencía",
        "Merlot",
        "Meunier",
        "Monastrell",
        "Montepulciano",
        "Mourvèdre",
        "Müller-Thurgau",
        "Muscat",
        "Muscat Blanc à Petits Grains",
        "Muscadelle",
        "Nebbiolo",
        "Negroamaro",
        "Nero d’Avola",
        "Palomino",
        "Parellada",
        "Pedro Ximénez",
        "Petit Manseng",
        "Petit Verdot",
        "Picpoul",
        "Pinot Blanc",
        "Pinot Gris",
        "Pinot Grigio",
        "Pinot Noir",
        "Pinotage",
        "Primitivo",
        "Riesling",
        "Roussanne",
        "Sangiovese",
        "Sauvignon Blanc",
        "Sémillon",
        "Semillon",
        "Sercial",
        "Shiraz",
        "Silvaner",
        "Spätburgunder",
        "Syrah",
        "Tannat",
        "Tempranillo",
        "Tinta Barroca",
        "Tinta Roriz",
        "Tinto Cão",
        "Torrontés",
        "Touriga Franca",
        "Touriga Nacional",
        "Trebbiano",
        "Trincadeira",
        "Ugni Blanc",
        "Verdejo",
        "Verdicchio",
        "Vidal",
        "Viognier",
        "Viura",
        "Welschriesling",
        "Xarel-lo",
        "Xinomavro",
        "Zinfandel",
        "Zweigelt",
    },
    "region": {
        "Aconcagua Region",
        "Alsace",
        "Australia",
        "Austria",
        "Baden",
        "Barossa",
        "Beaujolais",
        "Bordeaux",
        "Burgundy",
        "California",
        "Canada",
        "Central Italy",
        "Champagne",
        "Chile",
        "Dordogne",
        "France",
        "Franken",
        "Greece",
        "Italy",
        "Languedoc-Roussillon",
        "Loire Valley",
        "Mendoza",
        "Mosel",
        "Nahe",
        "New Zealand",
        "Northern Italy",
        "Northern Rhône",
        "Oregon",
        "Pfalz",
        "Portugal",
        "Rheingau",
        "Rheinhessen",
        "Rhône",
        "South Africa",
        "Southern France",
        "Southern Italy",
        "Southern Rhône",
        "Spain",
        "Tokaj",
        "Tuscany",
        "USA",
        "Veneto",
        "Washington",
        "Western Australia",
        "Western Cape",
    },
    "appellation": {
        "Aglianico del Vulture",
        "Alsace Grand Cru",
        "Amarone della Valpolicella",
        "Anjou",
        "Asti",
        "Bandol",
        "Barbaresco",
        "Barbera d’Asti",
        "Barolo",
        "Barsac",
        "Beaujolais Villages",
        "Bergerac",
        "Bolgheri",
        "Bordeaux Supérieur",
        "Bourgueil",
        "Bourgogne",
        "Brouilly",
        "Brunello di Montalcino",
        "Cahors",
        "Cava",
        "Chablis",
        "Châteauneuf-du-Pape",
        "Chianti",
        "Chianti Classico",
        "Chinon",
        "Collio",
        "Conegliano-Valdobbiadene",
        "Condrieu",
        "Cornas",
        "Côte Rôtie",
        "Coteaux du Layon",
        "Côtes de Bordeaux",
        "Côtes de Gascogne",
        "Côtes du Rhône",
        "Côtes du Rhône Villages",
        "Côtes du Roussillon",
        "Côtes du Roussillon Villages",
        "Crémant d’Alsace",
        "Crémant de Bourgogne",
        "Crémant de Loire",
        "Crozes-Hermitage",
        "Dolcetto d’Alba",
        "Entre-Deux-Mers",
        "Fiano di Avellino",
        "Fitou",
        "Fleurie",
        "Gavi",
        "Gigondas",
        "Graves",
        "Hermitage",
        "IGP Pays d’Oc",
        "Jurançon",
        "Madiran",
        "Margaux",
        "Médoc",
        "Menetou-Salon",
        "Minervois",
        "Monbazillac",
        "Morgon",
        "Muscadet",
        "Muscadet Sèvre et Maine",
        "Muscat de Beaumes-de-Venise",
        "Nemea",
        "Pauillac",
        "Pessac-Léognan",
        "Pomerol",
        "Pouilly-Fumé",
        "Prosecco",
        "Ribera del Duero",
        "Rioja",
        "Rutherglen",
        "Sancerre",
        "Saint-Émilion",
        "Saint-Émilion Grand Cru",
        "Saint-Estèphe",
        "Saint-Joseph",
        "Saint-Julien",
        "Sauternes",
        "Savennières",
        "Soave",
        "Soave Classico",
        "Tavel",
        "Taurasi",
        "Touraine",
        "Vacqueyras",
        "Valpolicella",
        "Valpolicella Classico",
        "Vino Nobile di Montepulciano",
        "Vouvray",
    },
    "viticulture": {
        "bench grafting",
        "Botrytis cinerea",
        "budburst",
        "canopy management",
        "clones",
        "coulure",
        "crossings",
        "density of planting",
        "diseases",
        "flowering",
        "frost",
        "fruit set",
        "fungal diseases",
        "grafting",
        "grey rot",
        "hail",
        "hand harvesting",
        "harvest",
        "hybrids",
        "irrigation",
        "millerandage",
        "nematodes",
        "noble rot",
        "one-year-old wood",
        "organic agriculture",
        "permanent wood",
        "pests",
        "phylloxera",
        "pruning",
        "replacement cane pruning",
        "rootstock",
        "shoots",
        "site selection",
        "summer pruning",
        "training",
        "trellising",
        "vineyard management",
        "Vitis vinifera",
        "whole bunch fermentation",
    },
    "vinification": {
        "acidification",
        "alcoholic fermentation",
        "anaerobic winemaking",
        "autolysis",
        "barrel",
        "blending",
        "carbonation",
        "carbonic maceration",
        "chaptalisation",
        "clarification",
        "crushing",
        "deacidification",
        "destemming",
        "dosage",
        "fermentation",
        "filtration",
        "fining",
        "fortification",
        "free run juice",
        "lees ageing",
        "malolactic conversion",
        "malolactic fermentation",
        "maturation",
        "oak",
        "oxidation",
        "pressing",
        "pumping over",
        "punching down",
        "rack and return",
        "racking",
        "red winemaking",
        "reduction",
        "riddling",
        "second alcoholic fermentation",
        "sedimentation",
        "semi-carbonic maceration",
        "skin contact",
        "sorting",
        "stabilisation",
        "traditional method",
        "transfer method",
        "whole bunch fermentation",
        "white winemaking",
    },
    "climate": {
        "altitude",
        "climate",
        "continental climate",
        "continentality",
        "cool climate",
        "diurnal range",
        "fog",
        "hot climate",
        "latitude",
        "maritime climate",
        "Mediterranean climate",
        "oceans",
        "orientation",
        "rainfall",
        "soil",
        "sunlight",
        "temperature",
        "temperate climate",
        "water",
        "weather",
        "warm climate",
    },
    "wine_law": {
        "AOC",
        "AVA",
        "Beerenauslese",
        "Brut",
        "Brut Nature",
        "Classico",
        "Costa",
        "Crianza",
        "DAC",
        "Demi-sec",
        "DOC",
        "DOCa",
        "DOCG",
        "DOQ",
        "Eiswein",
        "Entre Cordilleras",
        "Eszencia",
        "Grand Cru",
        "Gran Reserva",
        "Grosses Gewächs",
        "IGP",
        "IGT",
        "Indication géographique protégée",
        "Joven",
        "Kabinett",
        "Late Bottled Vintage",
        "Non-Vintage",
        "Prädikatswein",
        "Premier cru",
        "Qualitätswein",
        "Reserva",
        "Riserva",
        "Ruby",
        "sélection de grains nobles",
        "Spätlese",
        "sur lie",
        "Tawny",
        "Tokaji Aszú",
        "Trockenbeerenauslese",
        "VDP",
        "vendanges tardives",
        "Vin de France",
        "Vin de Pays",
        "Vino de la Tierra",
        "Vinos de Pago",
        "Vintage",
        "VQA",
        "Wine of Origin",
    },
    "sat_term": {
        "Acidez",
        "acidity",
        "Alcohol",
        "ámbar",
        "arándano azul",
        "balance",
        "baja",
        "burbujas",
        "Calidad",
        "Características del aroma",
        "Características del sabor",
        "claro",
        "Color",
        "complexity",
        "Condición",
        "Cuerpo",
        "Dulzor",
        "Evolución",
        "Final",
        "floral",
        "Fruta cítrica",
        "Fruta de hueso",
        "Fruta negra",
        "Fruta roja",
        "Fruta tropical",
        "Fruta verde",
        "Intensidad",
        "Intensidad del sabor",
        "limpia",
        "media",
        "medio",
        "Mousse",
        "Nivel de calidad",
        "NARIZ",
        "Otras observaciones",
        "primario",
        "pronunciada",
        "roble",
        "secundario",
        "tannin",
        "Tanino",
        "terciario",
    },
}


CANONICAL_OVERRIDES = {
    "Rhone": "Rhône",
    "Northern Rhone": "Northern Rhône",
    "Southern Rhone": "Southern Rhône",
    "Pays d'Oc": "IGP Pays d’Oc",
    "Botrytis Cinerea": "Botrytis cinerea",
    "Malolactic Conversion": "malolactic conversion",
    "Lees Ageing": "lees ageing",
    "Whole Bunch Fermentation": "whole bunch fermentation",
}


OBSERVED_VARIANTS = {
    "Rhône": {"Rhone"},
    "Northern Rhône": {"Northern Rhone"},
    "Southern Rhône": {"Southern Rhone"},
    "Languedoc-Roussillon": {"Languedoc and Roussillon", "Languedoc Roussillon"},
    "IGP Pays d’Oc": {"Pays d'Oc", "Pays d’Oc"},
    "Botrytis cinerea": {"Botrytis Cinerea"},
    "malolactic conversion": {"malolactic fermentation", "MLF"},
    "lees ageing": {"lees aging", "lees contact"},
    "whole bunch fermentation": {"whole bunch"},
    "carbonic maceration": {"carbonicm aceration"},
    "anaerobic winemaking": {"anaerobicw inemaking"},
}


def deaccent(value: str) -> str:
    return "".join(
        char for char in unicodedata.normalize("NFKD", value) if not unicodedata.combining(char)
    )


def norm_key(value: str) -> str:
    value = deaccent(value).lower()
    value = value.replace("’", "'").replace("–", "-")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def term_pattern(term: str) -> re.Pattern[str]:
    pieces = [re.escape(part) for part in re.split(r"\s+", term.strip())]
    return re.compile(r"(?<!\w)" + r"\s+".join(pieces) + r"(?!\w)", re.IGNORECASE)


def loose_pattern(term: str) -> re.Pattern[str]:
    plain = deaccent(term).replace("’", "'")
    pieces = [re.escape(part) for part in re.split(r"\s+", plain.strip())]
    return re.compile(r"(?<!\w)" + r"\s+".join(pieces) + r"(?!\w)", re.IGNORECASE)


def extract_pdf_pages(source: SourceDoc) -> list[dict[str, object]]:
    pages: list[dict[str, object]] = []
    with pdfplumber.open(source.path) as pdf:
        for idx, page in enumerate(pdf.pages, start=1):
            if source.official_source == "study-guide" and idx < 10:
                continue
            text = page.extract_text(x_tolerance=1, y_tolerance=3) or ""
            pages.append(
                {
                    "page": idx,
                    "text": text,
                    "norm": deaccent(text).replace("’", "'"),
                }
            )
    return pages


def infer_ra(source: str, page: int) -> str:
    if source == "sat":
        return "Unit 2 SAT"
    if source == "study-guide":
        if 10 <= page <= 18:
            return "SAT chapter"
        if 206 <= page <= 209:
            return "Index"
        return f"Study Guide p.{page}"
    if source == "specification":
        if 10 <= page <= 11:
            return "RA1"
        if 12 <= page <= 17:
            return "RA2"
        if 18 <= page <= 19:
            return "RA3"
        if 20 <= page <= 21:
            return "RA4/RA5"
        if page == 22:
            return "Unit 2 SAT"
        return f"Specification p.{page}"
    return ""


def find_matches(term: str, pages: list[dict[str, object]]) -> tuple[list[int], set[str], str]:
    aliases: set[str] = set()
    matched_pages: list[int] = []
    exact = term_pattern(term)
    loose = loose_pattern(term)

    for page in pages:
        text = str(page["text"])
        normalized_text = str(page["norm"])
        page_no = int(page["page"])
        if exact.search(text):
            matched_pages.append(page_no)
            continue
        if loose.search(normalized_text):
            matched_pages.append(page_no)
            aliases.add(deaccent(term))
            continue
        for alias in OBSERVED_VARIANTS.get(term, set()):
            if term_pattern(alias).search(text) or loose_pattern(alias).search(normalized_text):
                matched_pages.append(page_no)
                aliases.add(alias)
                break

    confidence = "high" if matched_pages and not aliases else "medium" if matched_pages else "low"
    return sorted(set(matched_pages)), aliases, confidence


def observed_transcript_aliases(term: str) -> set[str]:
    aliases = set()
    if not TRANSCRIPT_DIR.exists():
        return aliases
    expected = norm_key(term)
    for variant in OBSERVED_VARIANTS.get(term, set()):
        variant_key = norm_key(variant)
        if variant_key == expected:
            continue
        for path in TRANSCRIPT_DIR.glob("*.jsonl"):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if variant_key in norm_key(text):
                aliases.add(variant)
                break
    return aliases


def build_rows() -> list[dict[str, str]]:
    source_pages = {source.path.name: extract_pdf_pages(source) for source in SOURCES}
    rows: list[dict[str, str]] = []

    for category, terms in TERMS.items():
        allowed_sources = [
            source
            for source in SOURCES
            if category != "sat_term" or source.official_source in {"sat", "study-guide"}
        ]
        for raw_term in sorted(terms, key=lambda item: (norm_key(item), item)):
            canonical = CANONICAL_OVERRIDES.get(raw_term, raw_term)
            for source in allowed_sources:
                pages_for_match = source_pages[source.path.name]
                if category == "sat_term" and source.official_source == "study-guide":
                    pages_for_match = [
                        page for page in pages_for_match if 10 <= int(page["page"]) <= 15
                    ]
                pages, aliases, confidence = find_matches(canonical, pages_for_match)
                if not pages:
                    continue
                aliases |= observed_transcript_aliases(canonical)
                notes = f"Matched official PDF pages: {', '.join(map(str, pages[:12]))}"
                if len(pages) > 12:
                    notes += f" (+{len(pages) - 12} more)"
                if raw_term != canonical:
                    aliases.add(raw_term)
                if aliases and confidence == "high":
                    confidence = "medium"
                rows.append(
                    {
                        "canonical_term": canonical,
                        "category": category,
                        "official_source": source.official_source,
                        "source_document": source.path.name,
                        "ra": infer_ra(source.official_source, pages[0]),
                        "aliases": "; ".join(sorted(aliases, key=str.casefold)),
                        "confidence": confidence,
                        "manually_reviewed": "false",
                        "notes": notes,
                    }
                )
    return rows


def build_quality_flags(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    term_counts = Counter((norm_key(row["canonical_term"]), row["category"]) for row in rows)
    category_map: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        category_map[norm_key(row["canonical_term"])].add(row["category"])

    flags: list[dict[str, str]] = []
    for row in rows:
        duplicate = term_counts[(norm_key(row["canonical_term"]), row["category"])] > 1
        ambiguous = len(category_map[norm_key(row["canonical_term"])]) > 1
        low_confidence = row["confidence"] == "low"
        possible_ocr = bool(row["aliases"])
        if not any([duplicate, ambiguous, low_confidence, possible_ocr]):
            continue
        details = []
        if duplicate:
            details.append("duplicate_term")
        if ambiguous:
            details.append("ambiguous_category")
        if low_confidence:
            details.append("low_confidence_extraction")
        if possible_ocr:
            details.append(f"possible_ocr_issue: {row['aliases']}")
        flags.append(
            {
                "canonical_term": row["canonical_term"],
                "category": row["category"],
                "official_source": row["official_source"],
                "source_document": row["source_document"],
                "duplicate_term": str(duplicate).lower(),
                "ambiguous_category": str(ambiguous).lower(),
                "low_confidence_extraction": str(low_confidence).lower(),
                "possible_ocr_issue": str(possible_ocr).lower(),
                "details": "; ".join(details),
            }
        )
    return flags


def write_report(rows: list[dict[str, str]], flags: list[dict[str, str]]) -> None:
    counts = Counter(row["category"] for row in rows)
    duplicate_count = sum(1 for flag in flags if flag["duplicate_term"] == "true")
    ambiguous_count = sum(1 for flag in flags if flag["ambiguous_category"] == "true")
    low_count = sum(1 for flag in flags if flag["low_confidence_extraction"] == "true")
    ocr_count = sum(1 for flag in flags if flag["possible_ocr_issue"] == "true")
    sample_terms = rows[:20]

    lines = [
        "# WSET Level 3 Master Dictionary Extraction Report",
        "",
        "Controlled vocabulary extraction only. No embeddings, retrieval indexes, semantic graph linking, transcript mutation, question-bank mutation, or official PDF mutation were performed.",
        "",
        "## Official Sources",
    ]
    for source in SOURCES:
        lines.append(f"- {source.priority}. `{source.official_source}`: `{source.path.relative_to(ROOT)}`")

    lines.extend(["", "## Category Counts", ""])
    for category in sorted(counts):
        lines.append(f"- `{category}`: {counts[category]}")

    lines.extend(
        [
            "",
            "## Quality Flags",
            "",
            f"- `duplicate_term`: {duplicate_count}",
            f"- `ambiguous_category`: {ambiguous_count}",
            f"- `low_confidence_extraction`: {low_count}",
            f"- `possible_ocr_issue`: {ocr_count}",
            "",
            "## Method",
            "",
            "The extractor uses a conservative seeded vocabulary drawn from official WSET specification lists, the official study-guide index, and official SAT vocabulary. A candidate is emitted only when it is found in the local official PDFs. SAT rows are emitted only from the standalone official SAT sheet or the official SAT chapter/table in the study guide.",
            "",
            "Canonical terms preserve official WSET capitalization/spelling from the seeded official term. Aliases are emitted only for observed accent, capitalization, OCR, or ASR variants such as `Rhone` for `Rhône` and `carbonicm aceration` for `carbonic maceration`.",
            "",
            "## First 20 Extracted Terms",
            "",
        ]
    )
    for row in sample_terms:
        lines.append(
            f"- {row['canonical_term']} | {row['category']} | {row['official_source']} | {row['confidence']}"
        )

    (OUTPUT_DIR / "extraction_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = build_rows()
    rows.sort(
        key=lambda row: (
            row["category"],
            norm_key(row["canonical_term"]),
            row["official_source"],
            row["source_document"],
        )
    )
    flags = build_quality_flags(rows)

    with (OUTPUT_DIR / "master_terms.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    with (OUTPUT_DIR / "master_terms.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    with (OUTPUT_DIR / "extraction_quality_flags.csv").open(
        "w", newline="", encoding="utf-8-sig"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "canonical_term",
                "category",
                "official_source",
                "source_document",
                "duplicate_term",
                "ambiguous_category",
                "low_confidence_extraction",
                "possible_ocr_issue",
                "details",
            ],
        )
        writer.writeheader()
        writer.writerows(flags)

    write_report(rows, flags)

    print("Category counts:")
    for category, count in sorted(Counter(row["category"] for row in rows).items()):
        print(f"{category}: {count}")
    print("\nSample extracted terms:")
    for row in rows[:20]:
        print(f"{row['canonical_term']} | {row['category']} | {row['official_source']}")
    print(f"\nRows: {len(rows)}")
    print(f"Quality flags: {len(flags)}")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

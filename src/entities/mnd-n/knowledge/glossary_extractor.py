import hashlib
import json
import re
import unicodedata
from pathlib import Path


LOCATION_PATTERN = re.compile(
    r"Course Overview|Assigned Video \d+\.\d+|Bonus Audio \d+\.\d+|"
    r"Lecture \d+\.\d+|Reading \d+\.\d+"
)


def _slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")
    return slug or hashlib.sha1(value.encode("utf-8")).hexdigest()[:12]


def parse_locations(value: str) -> list[str]:
    return LOCATION_PATTERN.findall(value)


def _row_text(page, row, table_bbox: tuple[float, float, float, float]) -> list[str]:
    cells = [cell for cell in row.cells if cell]
    if not cells:
        return ["", "", ""]

    top = min(cell[1] for cell in cells)
    bottom = max(cell[3] for cell in cells)
    left, _, right, _ = table_bbox
    width = right - left
    columns = [
        (left, left + width * 0.25),
        (left + width * 0.25, left + width * 0.5),
        (left + width * 0.5, right),
    ]
    return [
        " ".join((page.crop((x0, top, x1, bottom)).extract_text() or "").split())
        for x0, x1 in columns
    ]


def extract_glossary(pdf_path: Path) -> list[dict]:
    """Extract term, location, definition, and page provenance from the PDF table."""
    try:
        import pdfplumber
    except ImportError as error:
        raise RuntimeError("Install requirements-lightrag.txt before extraction") from error

    source_hash = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    entries: list[dict] = []
    seen_ids: set[str] = set()

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            for table in page.find_tables():
                for row in table.rows:
                    term, location_text, definition = _row_text(page, row, table.bbox)
                    if (
                        not term
                        or not definition
                        or term == "Term"
                        or term.startswith("—")
                    ):
                        continue

                    entry_id = _slugify(term)
                    if entry_id in seen_ids:
                        entry_id = f"{entry_id}-p{page_number}"
                    seen_ids.add(entry_id)
                    entries.append(
                        {
                            "id": entry_id,
                            "term_en": term,
                            "term_ko": None,
                            "definition_en": definition,
                            "definition_ko": None,
                            "aliases_ko": [],
                            "locations": parse_locations(location_text),
                            "relations": [],
                            "translation_status": "not_started",
                            "relation_status": "not_started",
                            "source": {
                                "document_id": "social-psychology-glossary",
                                "title": "Social Psychology Glossary",
                                "page": page_number,
                                "sha256": source_hash,
                            },
                        }
                    )
    return entries


def write_jsonl(entries: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(output_path.suffix + ".tmp")
    temporary_path.write_text(
        "".join(json.dumps(entry, ensure_ascii=False) + "\n" for entry in entries),
        encoding="utf-8",
    )
    temporary_path.replace(output_path)


def read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

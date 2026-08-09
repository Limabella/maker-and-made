import argparse
import asyncio
from pathlib import Path

from glossary_extractor import extract_glossary, write_jsonl
from lightrag_adapter import index_glossary, query_glossary
from translation_pipeline import translate_jsonl


REPOSITORY_ROOT = next(
    parent for parent in Path(__file__).resolve().parents if (parent / ".git").exists()
)
DEFAULT_RUNTIME_DIR = REPOSITORY_ROOT / "runtime" / "psychology"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MND-N bilingual psychology LightRAG tools")
    commands = parser.add_subparsers(dest="command", required=True)

    extract = commands.add_parser("extract", help="Extract the English glossary from a PDF")
    extract.add_argument("--pdf", type=Path, required=True)
    extract.add_argument("--output", type=Path, default=DEFAULT_RUNTIME_DIR / "glossary.en.jsonl")

    translate = commands.add_parser("translate", help="Create machine-draft Korean translations")
    translate.add_argument("--input", type=Path, default=DEFAULT_RUNTIME_DIR / "glossary.en.jsonl")
    translate.add_argument("--output", type=Path, default=DEFAULT_RUNTIME_DIR / "glossary.ko.jsonl")
    translate.add_argument("--batch-size", type=int, default=6)
    translate.add_argument(
        "--max-batches",
        type=int,
        help="Stop after this many new batches; rerun to resume safely",
    )
    translate.add_argument("--model")

    index = commands.add_parser("index", help="Index bilingual entries with LightRAG")
    index.add_argument("--input", type=Path, default=DEFAULT_RUNTIME_DIR / "glossary.ko.jsonl")
    index.add_argument("--storage", type=Path, default=DEFAULT_RUNTIME_DIR / "lightrag")
    index.add_argument("--limit", type=int, help="Index only the first N records")
    index.add_argument(
        "--extract-relations",
        action="store_true",
        help="Let the index LLM draft entities and relations instead of using reviewed records",
    )

    query = commands.add_parser("query", help="Query the MND-N psychology knowledge base")
    query.add_argument("question")
    query.add_argument("--storage", type=Path, default=DEFAULT_RUNTIME_DIR / "lightrag")
    query.add_argument("--mode", choices=["local", "global", "hybrid", "mix"], default="mix")
    return parser


def main() -> None:
    args = _parser().parse_args()
    if args.command == "extract":
        entries = extract_glossary(args.pdf)
        write_jsonl(entries, args.output)
        print(f"Extracted {len(entries)} terms to {args.output}")
    elif args.command == "translate":
        entries = translate_jsonl(
            args.input,
            args.output,
            args.batch_size,
            args.model,
            args.max_batches,
        )
        print(f"Prepared {len(entries)} bilingual terms so far in {args.output}")
    elif args.command == "index":
        count = asyncio.run(
            index_glossary(
                args.input,
                args.storage,
                args.limit,
                args.extract_relations,
            )
        )
        print(f"Indexed {count} terms in {args.storage}")
    elif args.command == "query":
        print(asyncio.run(query_glossary(args.question, args.storage, args.mode)))


if __name__ == "__main__":
    main()

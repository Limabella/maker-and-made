import json
import os
from pathlib import Path

try:
    from .glossary_extractor import read_jsonl, write_jsonl
    from .nvidia_client import chat_completion, load_repository_env
except ImportError:
    from glossary_extractor import read_jsonl, write_jsonl
    from nvidia_client import chat_completion, load_repository_env


SYSTEM_PROMPT = """You translate a social psychology glossary into Korean.
Use established Korean academic terminology when it is well known.
Keep the definition faithful, concise, and educational.
Do not diagnose a reader or add claims absent from the source.
Return strict JSON only: {"items":[{"id":"...","term_ko":"...",
"definition_ko":"...","aliases_ko":[],"translation_notes":""}]}.
Every input id must appear exactly once."""


def _strip_json_fence(value: str) -> str:
    value = value.strip()
    if value.startswith("```") and value.endswith("```"):
        lines = value.splitlines()
        return "\n".join(lines[1:-1]).strip()
    return value


def translate_batch(entries: list[dict], model: str | None = None) -> list[dict]:
    payload = [
        {
            "id": entry["id"],
            "term_en": entry["term_en"],
            "definition_en": entry["definition_en"],
        }
        for entry in entries
    ]
    content = chat_completion(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        model=model,
    )
    parsed = json.loads(_strip_json_fence(content))
    translated_by_id = {item["id"]: item for item in parsed["items"]}
    expected_ids = {entry["id"] for entry in entries}
    if set(translated_by_id) != expected_ids:
        raise RuntimeError("Translation response ids do not match the input batch")

    model_name = (
        model
        or os.getenv("PSYCH_RAG_INDEX_MODEL")
        or os.getenv("NVIDIA_MODEL")
        or os.getenv("NIM_MODEL")
    )
    output: list[dict] = []
    for entry in entries:
        translated = translated_by_id[entry["id"]]
        merged = dict(entry)
        merged.update(
            {
                "term_ko": str(translated["term_ko"]).strip(),
                "definition_ko": str(translated["definition_ko"]).strip(),
                "aliases_ko": [str(value).strip() for value in translated.get("aliases_ko", [])],
                "translation_notes": str(translated.get("translation_notes", "")).strip(),
                "translation_status": "machine_draft",
                "translation_model": model_name,
            }
        )
        output.append(merged)
    return output


def translate_jsonl(
    input_path: Path,
    output_path: Path,
    batch_size: int = 6,
    model: str | None = None,
    max_batches: int | None = None,
) -> list[dict]:
    load_repository_env()
    entries = read_jsonl(input_path)
    completed = {
        entry["id"]: entry
        for entry in (read_jsonl(output_path) if output_path.exists() else [])
    }
    pending = [entry for entry in entries if entry["id"] not in completed]

    batches = range(0, len(pending), batch_size)
    if max_batches is not None:
        batches = list(batches)[:max_batches]

    for start in batches:
        for translated in translate_batch(pending[start : start + batch_size], model):
            completed[translated["id"]] = translated
        ordered = [completed[entry["id"]] for entry in entries if entry["id"] in completed]
        write_jsonl(ordered, output_path)
        print(f"Translated {len(ordered)}/{len(entries)} terms", flush=True)

    return [completed[entry["id"]] for entry in entries if entry["id"] in completed]

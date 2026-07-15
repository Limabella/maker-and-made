import asyncio
import os
from pathlib import Path

try:
    from .glossary_extractor import read_jsonl
    from .mnd_n_education_policy import educational_answer_instruction
    from .nvidia_client import chat_completion, load_repository_env, ollama_embeddings
except ImportError:
    from glossary_extractor import read_jsonl
    from mnd_n_education_policy import educational_answer_instruction
    from nvidia_client import chat_completion, load_repository_env, ollama_embeddings


def format_entry_for_index(entry: dict) -> str:
    source = entry["source"]
    relations = entry.get("relations", [])
    relation_text = "; ".join(
        f"{item.get('type')} -> {item.get('target')}" for item in relations
    ) or "machine extraction pending"
    return "\n".join(
        [
            f"Concept ID: {entry['id']}",
            f"English term: {entry['term_en']}",
            f"Korean term: {entry.get('term_ko') or 'translation pending'}",
            f"English definition: {entry['definition_en']}",
            f"Korean definition: {entry.get('definition_ko') or 'translation pending'}",
            f"Korean aliases: {', '.join(entry.get('aliases_ko', [])) or 'none'}",
            f"Relations: {relation_text}",
            f"Source: {source['title']}, page {source['page']}",
            f"Translation status: {entry.get('translation_status', 'not_started')}",
            f"Relation status: {entry.get('relation_status', 'machine_draft')}",
        ]
    )


def build_custom_kg(entries: list[dict]) -> dict:
    """Build a provenance-preserving KG without asking the chat model to parse it."""
    chunks: list[dict] = []
    entities: list[dict] = []
    relationships: list[dict] = []

    for entry in entries:
        source = entry["source"]
        source_id = entry["id"]
        file_path = f"{source['title']}#page={source['page']}"
        chunks.append(
            {
                "content": format_entry_for_index(entry),
                "source_id": source_id,
                "file_path": file_path,
            }
        )
        entities.append(
            {
                "entity_name": entry["term_en"],
                "entity_type": "SOCIAL_PSYCHOLOGY_CONCEPT",
                "description": format_entry_for_index(entry),
                "source_id": source_id,
                "file_path": file_path,
            }
        )

        if entry.get("relation_status") != "reviewed":
            continue
        for relation in entry.get("relations", []):
            relationships.append(
                {
                    "src_id": entry["term_en"],
                    "tgt_id": relation["target"],
                    "description": relation.get("evidence") or relation["type"],
                    "keywords": relation["type"],
                    "source_id": source_id,
                    "file_path": file_path,
                }
            )

    return {
        "chunks": chunks,
        "entities": entities,
        "relationships": relationships,
    }


async def create_lightrag(working_dir: Path):
    try:
        import numpy as np
        from lightrag import LightRAG
        from lightrag.utils import wrap_embedding_func_with_attrs
    except ImportError as error:
        raise RuntimeError("Install requirements-lightrag.txt before indexing") from error

    load_repository_env()
    embedding_dimension = int(os.getenv("PSYCH_RAG_EMBED_DIM", "1024"))

    @wrap_embedding_func_with_attrs(
        embedding_dim=embedding_dimension,
        max_token_size=8192,
        model_name=os.getenv("PSYCH_RAG_EMBED_MODEL", "bge-m3"),
    )
    async def embedding_func(texts: list[str]):
        values = await asyncio.to_thread(ollama_embeddings, texts)
        return np.asarray(values, dtype=np.float32)

    async def llm_model_func(
        prompt: str,
        system_prompt: str | None = None,
        history_messages: list[dict] | None = None,
        **kwargs,
    ) -> str:
        messages: list[dict] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.extend(history_messages or [])
        messages.append({"role": "user", "content": prompt})
        model = (
            os.getenv("PSYCH_RAG_QUERY_MODEL")
            if kwargs.get("keyword_extraction") is False
            else os.getenv("PSYCH_RAG_INDEX_MODEL")
        )
        return await asyncio.to_thread(chat_completion, messages, model)

    rag = LightRAG(
        working_dir=str(working_dir),
        workspace="mnd_n_psychology",
        llm_model_func=llm_model_func,
        llm_model_name=os.getenv("PSYCH_RAG_INDEX_MODEL", "nvidia/nvidia-nemotron-nano-9b-v2"),
        embedding_func=embedding_func,
    )
    await rag.initialize_storages()
    return rag


async def index_glossary(
    input_path: Path,
    working_dir: Path,
    limit: int | None = None,
    extract_relations: bool = False,
) -> int:
    entries = read_jsonl(input_path)
    if limit is not None:
        entries = entries[:limit]
    rag = await create_lightrag(working_dir)
    try:
        if extract_relations:
            for entry in entries:
                await rag.ainsert(format_entry_for_index(entry))
        else:
            await rag.ainsert_custom_kg(build_custom_kg(entries))
    finally:
        await rag.finalize_storages()
    return len(entries)


async def query_glossary(question: str, working_dir: Path, mode: str = "mix") -> str:
    from lightrag import QueryParam

    rag = await create_lightrag(working_dir)
    try:
        return await rag.aquery(
            question,
            param=QueryParam(
                mode=mode,
                response_type="A concise Korean educational explanation",
                user_prompt=educational_answer_instruction(),
                enable_rerank=False,
                include_references=True,
            ),
        )
    finally:
        await rag.finalize_storages()

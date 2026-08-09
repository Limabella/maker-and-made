import asyncio
import os
from pathlib import Path

try:
    from .lightrag_adapter import query_glossary
    from .mnd_n_education_policy import should_retrieve_psychology_knowledge
except ImportError:
    from lightrag_adapter import query_glossary
    from mnd_n_education_policy import should_retrieve_psychology_knowledge


REPOSITORY_ROOT = next(
    parent for parent in Path(__file__).resolve().parents if (parent / ".git").exists()
)
DEFAULT_STORAGE = REPOSITORY_ROOT / "runtime" / "psychology" / "lightrag"


def maybe_answer_psychology_question(user_sentence: str) -> str | None:
    """Return a grounded educational answer only when the optional RAG is ready."""
    enabled = os.getenv("PSYCH_RAG_ENABLED", "false").lower() in {"1", "true", "yes"}
    if not enabled or not should_retrieve_psychology_knowledge(user_sentence):
        return None

    storage = Path(os.getenv("PSYCH_RAG_STORAGE", str(DEFAULT_STORAGE)))
    graph_path = storage / "mnd_n_psychology" / "graph_chunk_entity_relation.graphml"
    if not graph_path.exists():
        return None
    return asyncio.run(query_glossary(user_sentence, storage))

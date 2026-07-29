# MND-N Bilingual Psychology LightRAG

This module turns externally supplied psychology references into a reusable,
source-grounded knowledge layer. It does not fine-tune the dialogue model.

## Why LightRAG

- LightRAG combines text chunks, semantic retrieval, entities, and relations.
- The graph-ready source schema keeps a later migration to a larger GraphRAG
  architecture straightforward.
- The same external knowledge base can be connected to another generation model
  without retraining that base model.
- The raw knowledge, reviewed translations, graph index, training data, and
  evaluation data remain separate assets.

The generation model and embedding model have different jobs. Nemotron creates
machine-draft translations, entity-relation candidates, and answers. A
multilingual embedding model retrieves English and Korean passages. The default
prototype expects `bge-m3` through Ollama; provider settings remain replaceable.

LightRAG recommends a capable long-context model for entity-relation extraction.
The current Nemotron Nano 9B model is acceptable for a small prototype, but every
automatically translated term or extracted relation must remain marked as
`machine_draft` until reviewed. A stronger model can later be assigned with
`PSYCH_RAG_INDEX_MODEL` without changing the source records.

## Local Data Policy

The source PDF, extracted definitions, Korean translations, and LightRAG index
are written below `runtime/psychology/`, which is excluded from Git. Do not
redistribute source text or use it for model training until its license permits
that use. Store only scripts, schemas, review rules, and synthetic test fixtures
in the public repository.

## Commands

Install optional dependencies and the embedding model:

```powershell
.venv\Scripts\python -m pip install -r requirements-lightrag.txt
ollama pull bge-m3
```

Extract the glossary with page-level provenance:

```powershell
.venv\Scripts\python src/entities/mnd-n/knowledge/psychology_rag_cli.py extract `
  --pdf "C:\path\to\SocialPsychGlossary.pdf"
```

Create resumable machine-draft Korean translations:

```powershell
.venv\Scripts\python src/entities/mnd-n/knowledge/psychology_rag_cli.py translate `
  --max-batches 1
```

Review the first six machine-draft translations, then rerun the command without
`--max-batches` to resume and finish the remaining terms. Completed records are
not requested again.

Index and query:

```powershell
.venv\Scripts\python src/entities/mnd-n/knowledge/psychology_rag_cli.py index --limit 1
.venv\Scripts\python src/entities/mnd-n/knowledge/psychology_rag_cli.py query "인지 부조화란 무엇인가요?"
```

Use `--limit 1` for the first end-to-end check. Remove it only after inspecting
the generated graph. By default, reviewed source records are inserted as a custom
knowledge graph, so a small chat model cannot silently corrupt the graph format.
Only relationships with `relation_status: reviewed` are inserted.

`--extract-relations` asks the configured index model to draft entities and
relations. Treat its output as experimental: Nemotron Nano 9B can fail LightRAG's
strict extraction format, and LightRAG recommends a larger long-context model for
this job.

MND-N must use this knowledge for education only. It may explain a general
concept, but it must not diagnose, label, or infer a user's personality from a
conversation.

After reviewing and indexing the records, enable retrieval in `.env`:

```dotenv
PSYCH_RAG_ENABLED=true
PSYCH_RAG_STORAGE=runtime/psychology/lightrag
```

The conversation service gives retrieved knowledge to MND-N when the player
explicitly asks for a psychology term, research basis, resilience concept, or
educational intervention option. The deterministic counselor-guidance layer
still owns the practice boundary and safety caution. Retrieval can supplement
that card but cannot turn a glossary result into a diagnosis or overwrite the
safety path. Safety mode always skips educational retrieval.

## Proposed Commit Message

```text
[FEAT] add bilingual psychology LightRAG knowledge pipeline

- Use LightRAG to preserve concept relationships and keep future GraphRAG migration straightforward.
- Reuse the same external RAG knowledge base across generation models without retraining each base model.
- Extract English glossary terms with page-level provenance and prepare reviewable Korean translations.
- Keep educational retrieval separate from diagnosis, personality inference, and clinical judgment.
```

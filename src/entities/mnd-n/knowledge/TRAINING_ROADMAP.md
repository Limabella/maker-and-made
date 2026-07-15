# Future Training Assets

The LightRAG knowledge base is the reusable source layer. It can later produce
reviewed datasets for multiple training strategies, but RAG records must not be
treated as training-ready automatically.

## Supported Future Paths

- **Supervised fine-tuning (SFT):** teach accurate term explanations and the
  bounded MND-N educational voice with reviewed instruction-answer pairs.
- **LoRA:** adapt a selected model at lower cost while preserving the reusable
  source knowledge outside the model weights.
- **Preference tuning:** learn the difference between grounded, respectful
  explanations and answers that are inaccurate, diagnostic, or overly certain.
- **Relation extraction model:** improve identification of evidence-backed
  relations such as `related_to`, `contrasts_with`, and `type_of`.
- **Korean psychology translation model:** learn consistent Korean terminology
  from expert-reviewed English-Korean term and definition pairs.

## Required Dataset Separation

```text
source knowledge        original text, provenance, and license status
reviewed translations   approved Korean terms and definitions
graph relations         evidence, source page, confidence, review status
interaction candidates  consented and anonymized examples only
training                reviewed instruction and preference records
evaluation              held out permanently from training
```

Before training, confirm source licensing, remove personal information, record
reviewer decisions, and keep an immutable evaluation split. A new generation
model can use the RAG immediately; fine-tuning is optional and should happen only
after enough high-quality reviewed examples exist.

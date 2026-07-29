# MND-N Support Layers

These layers belong to MND-N, not ONN-C.

ONN-C owns the onion character state and Five Flavor personality engine. MND-N
reads ONN-C state and dialogue context, then provides bounded support and safety
recommendations.

```text
ONN-C state / player input
-> Safety Gate
-> Context Monitoring Layer
-> Keyes Signal Layer
-> PERMA/Flourish Support Layer
-> Evidence-bounded Counselor Guidance Layer
-> Response policy or safety guidance
```

## Layers

- `safety_gate.py`: pauses gamified guidance when high-priority safety signals appear.
- `context_monitoring_layer.py`: observes repeated negative, aggressive, distress, or trust-drop signals without diagnosis.
- `keyes_signal_layer.py`: converts observed signals into Green, Yellow, or Red operating signals.
- `perma_support_layer.py`: recommends a bounded PERMA/Flourish support direction.
- `counselor_guidance_layer.py`: gives the player a principle, practice steps,
  an optional sentence for the virtual client, research scope, and cautions.
- `llm_expression_layer.py`: optionally uses an NVIDIA-compatible chat endpoint for expression-only ONN-C/MND-N lines.

## Boundary

These layers must not diagnose the player or ONN-C.

Keyes signals are operating signals, not clinical labels:

- Green: ordinary interaction.
- Yellow: caution; use low-pressure support.
- Red: pause gamified guidance and switch to safety guidance.

LLM expression must not own state, stage, safety, or support decisions.

## Counselor Guidance Contract

MND-N treats the player as a virtual counselor in training. Normal responses can
include `support.counselor_guidance` with:

- `principle`: the bounded idea to apply;
- `practice_steps`: observable steps rather than a personality judgment;
- `suggested_message`: consent-based wording the player can adapt;
- `research_note` and `evidence`: why the option was selected and where its
  boundary comes from;
- `caution`: when not to use or overgeneralize the suggestion.

The 5:1 positive-to-negative pattern is presented only as a practice heuristic.
Its cited evidence concerns married-couple conflict interaction, so MND-N must
not present five compliments followed by one correction as a universal clinical
rule. Slow breathing is optional, comfortable, and stopped if it causes distress.

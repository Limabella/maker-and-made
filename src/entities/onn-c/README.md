# ONN-C Five Flavor Onion Prototype

This is a small Python MVP for ONN-C, the onion character personality and state engine.

ONN-C uses the Five Flavor Onion model as its character personality tool. MND-N
is a separate bounded helper that can read ONN-C state and offer
PERMA/Flourish-based support guidance. MND-N is not a therapist, counselor, or
diagnostic system.

```text
Input
-> Big Five Layer
-> Emotion Layer
-> Memory Layer
-> Decision Layer
-> NPC Action
```

Integrated demo mode also calls MND-N support layers:

```text
ONN-C state output
-> MND-N Safety Gate
-> MND-N Context Monitoring
-> MND-N Keyes Signal
-> MND-N PERMA/Flourish Support
-> ONN-C action boundary / safety guidance
```

The prototype does not use any external AI API. It uses simple English and Korean keyword rules so the behavior is easy to inspect and change.
The first CLI MVP also includes a small multilingual keyword set for common
Japanese, Chinese, Spanish, and French emotion signals. This is still a
prototype-level heuristic, not full multilingual understanding.

## Structure

```text
src/entities/onn-c/
  main.py
  play_cli.py
  layers/
    big_five_layer.py
    emotion_layer.py
    state_layer.py
    memory_layer.py
    decision_layer.py
    action_layer.py
  data/
    npc_memory.json
  README.md
```

## Layers

- `big_five_layer.py`: estimates OCEAN scores from English and Korean user sentence keywords.
- `emotion_layer.py`: estimates joy, anger, trust, and sadness from English and Korean keywords.
- `state_layer.py`: estimates the playable ONN-C state snapshot: stage, trust, darkness, stability, energy, and attachment.
- `memory_layer.py`: stores previous interactions in `data/npc_memory.json` and summarizes trust/familiarity.
- `decision_layer.py`: chooses one NPC behavior from personality, emotion, and memory summary.
- `action_layer.py`: turns the chosen behavior into the final NPC action payload.

MND-N support layers live outside ONN-C:

```text
src/entities/mnd-n/support_layers/
  safety_gate.py
  context_monitoring_layer.py
  keyes_signal_layer.py
  perma_support_layer.py
```

## Actions

The NPC always returns one of:

- `greet`
- `help`
- `refuse`
- `joke`
- `avoid`
- `respond`
- `ask_question`
- `safety_guidance`

`safety_guidance` pauses gamified advice and switches to safety guidance. It has
priority over the normal character action loop.

## How to Run

From the repository root:

```bash
python src/entities/onn-c/main.py
```

For direct player testing, run the CLI MVP:

```bash
python src/entities/onn-c/play_cli.py
```

For the second CLI MVP expression layer, set `NVIDIA_API_KEY` and run:

```bash
python src/entities/onn-c/play_cli.py --nvidia
```

For local configuration, copy `.env.example` to `.env` in the repository root
and put the real API key in `.env`. The CLI loads it automatically. Shell
environment variables take precedence over values from the file, and `.env` is
excluded from Git.

Optional NVIDIA settings:

```text
NVIDIA_API_KEY       required for NVIDIA expression mode
NVIDIA_MODEL         optional, defaults to nvidia/nvidia-nemotron-nano-9b-v2
NIM_MODEL            accepted as an alias for NVIDIA_MODEL
NVIDIA_API_BASE_URL  optional, defaults to an NVIDIA-compatible chat completions URL
NVIDIA_TIMEOUT_SECONDS optional, defaults to 30 seconds
```

If the key is missing or the endpoint fails, the CLI falls back to deterministic
template dialogue. State and safety decisions are never delegated to the model.

To test a different sentence, pass it as a command line argument:

```bash
python src/entities/onn-c/main.py "안녕 친구야, 새로운 장소를 탐험하게 도와줄래?"
python src/entities/onn-c/main.py "I hate you and I will attack."
```

You can still edit `user_sentence` in `main.py` if you prefer a fixed scenario.

CLI commands:

- `/help`: show commands.
- `/state`: show memory summary.
- `/reset`: clear CLI play memory.
- `/quit`: exit.

## Notes

The Big Five model is represented as five simple scores:

- Openness: creativity and interest in new experiences.
- Conscientiousness: planning, responsibility, and goal focus.
- Extraversion: social energy and positive interaction.
- Agreeableness: cooperation, empathy, and trust.
- Neuroticism: emotional instability, worry, and stress.

## Memory Behavior

Each run appends one interaction to `data/npc_memory.json`.

The memory layer summarizes prior interactions into:

- `trust_level`: rises after helpful, friendly, joyful, or trusting interactions; falls after angry, sad, avoidant, or refusing interactions.
- `familiarity`: rises as the NPC sees more interactions.
- `recent_negative_streak`: counts recent negative interactions in a row.

The decision layer uses those values to shift NPC attitude. High trust makes help and friendly behavior more likely. Low trust or repeated negative interactions makes refuse or avoid more likely.

The expression layer also sends up to four recent dialogue turns to NIM. General
questions and neutral statements default to `respond`; `ask_question` is reserved
for cases where a follow-up is actually needed. The prompt explicitly prevents
echoing the player's sentence back as a question.

The project name follows the "five flavors" metaphor for the five personality factors.

## Playable State

The first CLI MVP uses a transparent rule-based state model:

- `stage`: `bright`, `mixed`, `guarded`, `dark`, `recovering`, or `safety`.
- `trust`: relationship trust derived from memory.
- `darkness`: defensive/darkening pressure, not a pathology label.
- `stability`: resistance to emotional pressure.
- `energy`: current expressive energy.
- `attachment`: relationship closeness tendency.

This comes before machine learning. The next CLI MVP can add an NVIDIA-backed
local/free model as an expression engine for ONN-C and MND-N dialogue, while the
state and safety decisions remain rule-based and inspectable.

## Language Handling

The current CLI is keyword-based. It can react to common Korean, English,
Japanese, Chinese, Spanish, and French emotion words, but it does not yet
understand arbitrary multilingual phrasing.

The second CLI MVP can use an NVIDIA-backed local/free model as an expression
helper. The model does not own state, safety, or stage decisions.

## MND-N Support Behavior in Demo Mode

ONN-C does not own MND-N support policy. In demo mode, it calls MND-N's support
layers so the prototype can show the full interaction loop.

MND-N uses PERMA as a small support map:

- Positive Emotion: notice a small safe or pleasant signal.
- Engagement: choose a small activity that fits the onion's current energy.
- Relationships: repair the interaction with a respectful, low-pressure step.
- Meaning: connect the next action to a small reason that matters.
- Accomplishment: make the next step small enough to finish now.

If the safety gate is triggered, MND-N pauses PERMA guidance and switches to
safety guidance.

For the integrated architecture, roadmap, governance, and trait model, see `experiments_ko/oniontest/README_KO.md`.

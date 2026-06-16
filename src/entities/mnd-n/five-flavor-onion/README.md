# Five Flavor Onion NPC Prototype

This is a small Python MVP for a game NPC personality pipeline.

```text
Input
-> Big Five Layer
-> Emotion Layer
-> Memory Layer
-> Decision Layer
-> NPC Action
```

The prototype does not use any external AI API. It uses simple English and Korean keyword rules so the behavior is easy to inspect and change.

## Structure

```text
src/entities/mnd-n/five-flavor-onion/
  main.py
  layers/
    big_five_layer.py
    emotion_layer.py
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
- `memory_layer.py`: stores previous interactions in `data/npc_memory.json` and summarizes trust/familiarity.
- `decision_layer.py`: chooses one NPC behavior from personality, emotion, and memory summary.
- `action_layer.py`: turns the chosen behavior into the final NPC action payload.

## Actions

The NPC always returns one of:

- `greet`
- `help`
- `refuse`
- `joke`
- `avoid`
- `ask_question`

## How to Run

From the repository root:

```bash
python src/entities/mnd-n/five-flavor-onion/main.py
```

To test a different sentence, pass it as a command line argument:

```bash
python src/entities/mnd-n/five-flavor-onion/main.py "안녕 친구야, 새로운 장소를 탐험하게 도와줄래?"
python src/entities/mnd-n/five-flavor-onion/main.py "I hate you and I will attack."
```

You can still edit `user_sentence` in `main.py` if you prefer a fixed scenario.

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

The project name follows the "five flavors" metaphor for the five personality factors.

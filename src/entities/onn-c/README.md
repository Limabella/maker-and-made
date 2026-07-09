# ONN-C Runtime

ONN-C is the Onion Bot runtime shell.

This folder keeps ONN-C separate from the MND-N engine:

```text
ONN-C
-> character identity, visible state, player-facing shell

MND-N Five Flavor Onion
-> internal psychology pipeline, memory scoring, decision support
```

The first runtime uses the existing MVP engine at:

```text
src/entities/mnd-n/five-flavor-onion/
```

## Run

From the repository root:

```bash
python src/entities/onn-c/play_cli.py
```

Single message:

```bash
python src/entities/onn-c/play_cli.py "안녕 양파야"
```

Optional parser flag placeholder:

```bash
python src/entities/onn-c/play_cli.py --nvidia "안녕 양파야"
```

`--nvidia` does not call an external service yet. It marks the intended parser slot so the runtime shape stays stable before any model vendor is selected.

## Commands

- `/state`: print current ONN-C visible state.
- `/quit`: exit the interactive shell.

## Visible State

ONN-C maps engine output into three visible onion states:

- `orange`: normal, friendly, responsive.
- `white`: careful, softened, supportive.
- `black`: guarded after threat, refusal, or repeated negative pressure.

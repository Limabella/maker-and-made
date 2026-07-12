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

Generate the final reply with NVIDIA NIM:

```bash
python src/entities/onn-c/play_cli.py --nvidia "안녕 양파야"
```

Hosted NVIDIA API example (PowerShell):

```powershell
$env:NVIDIA_API_KEY = "your-key"
$env:NIM_MODEL = "meta/llama-3.3-70b-instruct"
python src/entities/onn-c/play_cli.py --nvidia
```

For NVIDIA Nemotron Nano 9B v2:

```powershell
$env:NIM_MODEL = "nvidia/nvidia-nemotron-nano-9b-v2"
python src/entities/onn-c/play_cli.py --nvidia
```

ONN-C automatically uses Nemotron's `/no_think` mode because short character dialogue does not need a visible reasoning trace.

For a local NIM server, keep the same CLI and change only the endpoint:

```powershell
$env:NIM_BASE_URL = "http://localhost:8000/v1"
$env:NIM_MODEL = "your-local-model-id"
python src/entities/onn-c/play_cli.py --nvidia
```

Configuration variables:

- `NVIDIA_API_KEY` or `NIM_API_KEY`: bearer token; optional for an unauthenticated local server.
- `NIM_BASE_URL`: defaults to `https://integrate.api.nvidia.com/v1`.
- `NIM_MODEL`: defaults to `meta/llama-3.3-70b-instruct`.
- `NIM_TIMEOUT_SECONDS`: defaults to `30`.

If NIM is unavailable or returns an invalid response, ONN-C reports the failure and falls back to the existing rule-based line.

## Commands

- `/state`: print current ONN-C visible state.
- `/quit`: exit the interactive shell.

## Visible State

ONN-C maps engine output into three visible onion states:

- `orange`: normal, friendly, responsive.
- `white`: careful, softened, supportive.
- `black`: guarded after threat, refusal, or repeated negative pressure.

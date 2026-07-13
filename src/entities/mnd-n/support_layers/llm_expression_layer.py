import json
import os
import urllib.error
import urllib.request


DEFAULT_NVIDIA_API_BASE_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
DEFAULT_NVIDIA_MODEL = "nvidia/nvidia-nemotron-nano-9b-v2"


def build_fallback_expression(result: dict) -> dict:
    """Build deterministic dialogue when no LLM is configured or available."""
    onion_state = result["onion_state"]
    action = result["npc_action"]["action"]
    support = result["mnd_n_support"]
    signal = result["keyes_signal"]["signal"]

    stage_lines = {
        "bright": "양파는 아직 밝고 열려 있는 상태예요.",
        "mixed": "양파는 반응이 조금 흔들리고 있어요.",
        "guarded": "양파는 조심스럽고 방어적으로 반응하고 있어요.",
        "dark": "양파는 어두운 방어 상태에 가까워졌어요.",
        "recovering": "양파는 다시 안정되는 중이에요.",
        "safety": "지금은 게임화된 반응을 멈추고 안전 안내가 우선이에요.",
    }

    action_lines = {
        "greet": "안녕. 지금은 천천히 이야기해도 괜찮아.",
        "help": "내가 할 수 있는 작은 도움부터 해볼게.",
        "refuse": "지금 방식으로는 계속하기 어려워.",
        "joke": "조금 가볍게 숨을 돌려볼까?",
        "avoid": "지금은 조금 물러나 있을게.",
        "respond": "응, 네 말에 바로 답해볼게.",
        "ask_question": "지금 나에게 어떤 걸 해보고 싶어?",
        "safety_guidance": "지금은 안전이 먼저야. 게임 조언은 잠시 멈출게.",
    }

    return {
        "provider": "fallback",
        "onn_c_line": action_lines.get(action, action_lines["ask_question"]),
        "mnd_n_line": (
            f"{stage_lines.get(onion_state['stage'], stage_lines['mixed'])} "
            f"주의 신호는 {signal.upper()}이고, 권장 방향은 {support['label']}입니다."
        ),
    }


def generate_nvidia_expression(
    player_input: str,
    result: dict,
    recent_interactions: list[dict] | None = None,
    api_key: str | None = None,
    model: str | None = None,
    base_url: str | None = None,
    timeout_seconds: int | None = None,
) -> dict:
    """Generate ONN-C and MND-N lines using an NVIDIA-compatible chat endpoint.

    The LLM is expression-only. It must not change ONN-C state, MND-N signal, or
    safety decisions.
    """
    api_key = api_key or os.getenv("NVIDIA_API_KEY")
    model = (
        model
        or os.getenv("NVIDIA_MODEL")
        or os.getenv("NIM_MODEL")
        or DEFAULT_NVIDIA_MODEL
    )
    base_url = base_url or os.getenv("NVIDIA_API_BASE_URL") or DEFAULT_NVIDIA_API_BASE_URL
    timeout_seconds = timeout_seconds or int(os.getenv("NVIDIA_TIMEOUT_SECONDS", "30"))

    if not api_key:
        expression = build_fallback_expression(result)
        expression["provider"] = "fallback:no_nvidia_api_key"
        return expression

    history_messages = _build_history_messages(recent_interactions or [])
    reasoning_control = "/no_think\n" if "nemotron-nano-9b-v2" in model.lower() else ""
    payload = {
        "model": model,
        "temperature": 0.4,
        "max_tokens": 220,
        "messages": [
            {
                "role": "system",
                "content": reasoning_control + (
                    "You are an expression layer for a prototype game. "
                    "You do not diagnose, treat, or change system state. "
                    "Write concise Korean dialogue only. "
                    "Return strict JSON with keys onn_c_line and mnd_n_line. "
                    "ONN-C is an onion character. MND-N is a bounded support helper. "
                    "Answer the player's current message directly before asking anything. "
                    "Do not echo, paraphrase, or turn the player's words back into a question. "
                    "Ask a follow-up only when it is genuinely needed. "
                    "If asked about something you cannot see or know, say that plainly. "
                    "For playful commands, respond with a brief in-character action. "
                    "If safety is triggered, do not provide gamified advice."
                ),
            },
            *history_messages,
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "player_input": player_input,
                        "onn_c_state": result["onion_state"],
                        "onn_c_action": result["npc_action"]["action"],
                        "safety": result["safety"],
                        "keyes_signal": result["keyes_signal"],
                        "mnd_n_support": result["mnd_n_support"],
                        "instruction": (
                            "Create one short ONN-C line and one short MND-N line. "
                            "Do not alter any state. Avoid clinical labels. "
                            "Respond to the current message instead of repeating it."
                        ),
                    },
                    ensure_ascii=False,
                ),
            },
        ],
    }

    request = urllib.request.Request(
        base_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        expression = build_fallback_expression(result)
        expression["provider"] = "fallback:nvidia_error"
        expression["error"] = str(error)
        return expression

    try:
        content = data["choices"][0]["message"]["content"]
        content = _strip_json_fence(content)
        parsed = json.loads(content)
        return {
            "provider": "nvidia",
            "model": model,
            "onn_c_line": str(parsed["onn_c_line"]).strip(),
            "mnd_n_line": str(parsed["mnd_n_line"]).strip(),
        }
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as error:
        expression = build_fallback_expression(result)
        expression["provider"] = "fallback:nvidia_parse_error"
        expression["error"] = str(error)
        return expression


def _build_history_messages(interactions: list[dict], limit: int = 4) -> list[dict]:
    """Convert recent stored dialogue into chat-completions messages."""
    messages: list[dict] = []
    for interaction in interactions[-limit:]:
        user_sentence = interaction.get("user_sentence")
        if user_sentence:
            messages.append({"role": "user", "content": str(user_sentence)})

        onn_c_line = interaction.get("onn_c_line")
        mnd_n_line = interaction.get("mnd_n_line")
        if onn_c_line or mnd_n_line:
            messages.append(
                {
                    "role": "assistant",
                    "content": json.dumps(
                        {
                            "onn_c_line": str(onn_c_line or ""),
                            "mnd_n_line": str(mnd_n_line or ""),
                        },
                        ensure_ascii=False,
                    ),
                }
            )
    return messages


def _strip_json_fence(content: str) -> str:
    content = content.strip()
    if content.startswith("```") and content.endswith("```"):
        lines = content.splitlines()
        if len(lines) >= 3:
            return "\n".join(lines[1:-1]).strip()
    return content

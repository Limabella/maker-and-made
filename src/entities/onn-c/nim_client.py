from __future__ import annotations

import os
from dataclasses import dataclass
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = "https://integrate.api.nvidia.com/v1"
DEFAULT_MODEL = "meta/llama-3.3-70b-instruct"


class NimError(RuntimeError):
    """Raised when a NIM response cannot be used."""


@dataclass(frozen=True)
class NimConfig:
    base_url: str
    model: str
    api_key: str | None
    timeout_seconds: float = 30.0

    @classmethod
    def from_environment(cls) -> "NimConfig":
        return cls(
            base_url=os.getenv("NIM_BASE_URL", DEFAULT_BASE_URL).rstrip("/"),
            model=os.getenv("NIM_MODEL", DEFAULT_MODEL),
            api_key=os.getenv("NVIDIA_API_KEY") or os.getenv("NIM_API_KEY"),
            timeout_seconds=float(os.getenv("NIM_TIMEOUT_SECONDS", "30")),
        )


class NimClient:
    """Small OpenAI-compatible client for hosted or local NVIDIA NIM."""

    def __init__(self, config: NimConfig | None = None):
        self.config = config or NimConfig.from_environment()

    def generate_reply(
        self,
        user_message: str,
        result: dict,
        recent_interactions: list[dict] | None = None,
    ) -> str:
        if self.config.base_url == DEFAULT_BASE_URL and not self.config.api_key:
            raise NimError(
                "NVIDIA_API_KEY is required for the hosted NIM API. "
                "Set NIM_BASE_URL for a local NIM server."
            )
        state = _visible_state(result)
        action = result["npc_action"]["action"]
        memory = result["memory_summary_before"]
        history = _history_messages(recent_interactions or [])

        reasoning_control = (
            "/no_think\n"
            if "nemotron-nano-9b-v2" in self.config.model.lower()
            else ""
        )
        system_prompt = reasoning_control + (
            "너는 게임 속 양파 캐릭터 ONN-C다. 한국어로 자연스럽고 따뜻하게 대화한다. "
            "설명문이나 분석 결과를 말하지 말고 캐릭터의 실제 대사만 출력한다. "
            "답변은 보통 1~3문장으로 간결하게 한다. 사용자의 감정을 단정하지 않는다. "
            f"현재 외형 상태는 {state}, 선택된 행동은 {action}, "
            f"신뢰도는 {memory['trust_level']:.2f}다. 선택된 행동의 의도를 존중한다."
        )
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"

        request = Request(
            f"{self.config.base_url}/chat/completions",
            headers=headers,
            data=json.dumps(
                {
                    "model": self.config.model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 180,
                    "stream": False,
                }
            ).encode("utf-8"),
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.config.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
            content = payload["choices"][0]["message"]["content"].strip()
        except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError,
                KeyError, IndexError, TypeError, ValueError) as exc:
            raise NimError(f"NIM request failed: {exc}") from exc

        if not content:
            raise NimError("NIM returned an empty response.")
        return content


def _visible_state(result: dict) -> str:
    emotion = result.get("emotion", {})
    action = result.get("npc_action", {}).get("action", "ask_question")
    memory = result.get("memory_summary_before", {})
    if action in {"refuse", "avoid"} or memory.get("recent_negative_streak", 0) >= 2:
        return "black"
    if emotion.get("sadness", 0.0) > 0 or action == "help":
        return "white"
    return "orange"


def _history_messages(interactions: list[dict], limit: int = 4) -> list[dict]:
    messages: list[dict] = []
    for interaction in interactions[-limit:]:
        user_sentence = interaction.get("user_sentence")
        if user_sentence:
            messages.append({"role": "user", "content": str(user_sentence)})
        npc_line = interaction.get("npc_line")
        if npc_line:
            messages.append({"role": "assistant", "content": str(npc_line)})
    return messages

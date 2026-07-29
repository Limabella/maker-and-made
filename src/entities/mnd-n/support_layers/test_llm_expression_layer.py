import json
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch


MND_N_PATH = Path(__file__).resolve().parents[1]
if str(MND_N_PATH) not in sys.path:
    sys.path.insert(0, str(MND_N_PATH))

from support_layers.llm_expression_layer import generate_nvidia_expression


RESULT = {
    "onion_state": {"stage": "bright"},
    "npc_action": {"action": "respond"},
    "safety": {"triggered": False},
    "keyes_signal": {"signal": "green"},
    "mnd_n_support": {"label": "Accomplishment", "prompt": "Take one step."},
    "counselor_guidance": {
        "active": True,
        "principle": "작은 행동을 제안합니다.",
        "suggested_message": "한 걸음만 함께 해볼까요?",
        "research_note": "일반적인 연습 안내입니다.",
    },
}


class ExpressionLayerTests(unittest.TestCase):
    @patch("support_layers.llm_expression_layer.urllib.request.urlopen")
    def test_uses_history_and_nemotron_no_think(self, urlopen: Mock) -> None:
        response = Mock()
        response.read.return_value = json.dumps(
            {
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(
                                {"onn_c_line": "두 개로 찍어볼게!", "mnd_n_line": "정답을 알려줘."},
                                ensure_ascii=False,
                            )
                        }
                    }
                ]
            }
        ).encode("utf-8")
        urlopen.return_value.__enter__.return_value = response

        expression = generate_nvidia_expression(
            "손가락 몇 개 들고 있을까?",
            RESULT,
            recent_interactions=[
                {"user_sentence": "안녕", "onn_c_line": "반가워!", "mnd_n_line": "천천히 말해줘."}
            ],
            api_key="secret",
            model="nvidia/nvidia-nemotron-nano-9b-v2",
        )

        self.assertEqual(expression["onn_c_line"], "두 개로 찍어볼게!")
        request = urlopen.call_args.args[0]
        payload = json.loads(request.data.decode("utf-8"))
        self.assertTrue(payload["messages"][0]["content"].startswith("/no_think\n"))
        self.assertEqual(payload["messages"][1]["content"], "안녕")
        self.assertEqual(payload["messages"][2]["role"], "assistant")
        current_turn = json.loads(payload["messages"][-1]["content"])
        self.assertIn("counselor_guidance", current_turn)

    @patch.dict("os.environ", {"NIM_MODEL": "nvidia/test-model"}, clear=True)
    def test_accepts_nim_model_alias_without_calling_endpoint(self) -> None:
        expression = generate_nvidia_expression("안녕", RESULT)
        self.assertEqual(expression["provider"], "fallback:no_nvidia_api_key")


if __name__ == "__main__":
    unittest.main()

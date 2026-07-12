import json
import unittest
from unittest.mock import Mock, patch

from nim_client import NimClient, NimConfig, NimError


RESULT = {
    "emotion": {"sadness": 0.25},
    "npc_action": {"action": "help", "line": "fallback"},
    "memory_summary_before": {"trust_level": 0.6, "recent_negative_streak": 0},
}


class NimClientTests(unittest.TestCase):
    def test_hosted_api_requires_key(self) -> None:
        with self.assertRaisesRegex(NimError, "NVIDIA_API_KEY"):
            NimClient(NimConfig("https://integrate.api.nvidia.com/v1", "model", None)).generate_reply(
                "안녕", RESULT
            )

    @patch("nim_client.urlopen")
    def test_generates_reply_from_openai_compatible_response(self, urlopen: Mock) -> None:
        response = Mock()
        response.read.return_value = json.dumps({
            "choices": [{"message": {"content": "오늘 많이 힘들었구나. 옆에 있을게."}}]
        }).encode("utf-8")
        urlopen.return_value.__enter__.return_value = response
        client = NimClient(NimConfig("http://localhost:8000/v1", "test-model", None))

        reply = client.generate_reply("오늘 힘들어", RESULT)

        self.assertEqual(reply, "오늘 많이 힘들었구나. 옆에 있을게.")
        request = urlopen.call_args.args[0]
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(payload["model"], "test-model")
        self.assertNotIn("Authorization", dict(request.header_items()))

    @patch("nim_client.urlopen")
    def test_uses_bearer_token(self, urlopen: Mock) -> None:
        response = Mock()
        response.read.return_value = json.dumps(
            {"choices": [{"message": {"content": "안녕!"}}]}
        ).encode("utf-8")
        urlopen.return_value.__enter__.return_value = response
        client = NimClient(NimConfig("https://example.test/v1", "model", "secret"))

        client.generate_reply("안녕", RESULT)

        request = urlopen.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "Bearer secret")

    @patch("nim_client.urlopen")
    def test_nemotron_nano_disables_reasoning_for_character_chat(self, urlopen: Mock) -> None:
        response = Mock()
        response.read.return_value = json.dumps(
            {"choices": [{"message": {"content": "반가워!"}}]}
        ).encode("utf-8")
        urlopen.return_value.__enter__.return_value = response
        client = NimClient(
            NimConfig(
                "https://integrate.api.nvidia.com/v1",
                "nvidia/nvidia-nemotron-nano-9b-v2",
                "secret",
            )
        )

        client.generate_reply("안녕", RESULT)

        request = urlopen.call_args.args[0]
        payload = json.loads(request.data.decode("utf-8"))
        self.assertTrue(payload["messages"][0]["content"].startswith("/no_think\n"))

    @patch("nim_client.urlopen")
    def test_rejects_empty_response(self, urlopen: Mock) -> None:
        response = Mock()
        response.read.return_value = json.dumps(
            {"choices": [{"message": {"content": " "}}]}
        ).encode("utf-8")
        urlopen.return_value.__enter__.return_value = response

        with self.assertRaises(NimError):
            NimClient(NimConfig("http://localhost/v1", "model", None)).generate_reply(
                "안녕", RESULT
            )


if __name__ == "__main__":
    unittest.main()

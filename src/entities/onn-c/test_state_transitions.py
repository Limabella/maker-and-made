import json
from pathlib import Path
from tempfile import TemporaryDirectory
import threading
import unittest
import urllib.request

import api_server
from conversation_service import ConversationService
from layers.memory_layer import MemoryLayer
from layers.state_layer import estimate_onion_state
from ue_response import build_ue_response


class StateTransitionScenarioTests(unittest.TestCase):
    def test_state_transition_scenarios(self) -> None:
        case_path = Path(__file__).with_name("state_transition_cases.json")
        cases = json.loads(case_path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(cases), 30)

        for case in cases:
            with self.subTest(case=case["name"]):
                state = estimate_onion_state(
                    emotion=case["emotion"],
                    memory_summary=case["memory"],
                    action_name=case["action"],
                    keyes_signal={"signal": case["signal"]},
                )
                self.assertEqual(state["stage"], case["expected"])
                for field in ("trust", "darkness", "stability", "energy", "attachment"):
                    self.assertGreaterEqual(state[field], 0.0)
                    self.assertLessEqual(state[field], 1.0)

    def test_conversation_is_persisted_once_with_dialogue(self) -> None:
        with TemporaryDirectory() as directory:
            memory = MemoryLayer(Path(directory) / "memory.json")
            turn = ConversationService(memory, use_nvidia=False).respond("안녕")

            interactions = memory.load_interactions()
            self.assertEqual(len(interactions), 1)
            self.assertEqual(interactions[0]["user_sentence"], "안녕")
            self.assertTrue(interactions[0]["onn_c_line"])
            self.assertTrue(interactions[0]["mnd_n_line"])

            response = build_ue_response(turn.result, turn.expression)
            self.assertEqual(response["schema_version"], "onn-c.v1")
            self.assertEqual(response["dialogue"]["onn_c"], interactions[0]["onn_c_line"])
            self.assertIn(response["character"]["animation"], {
                "greet_warmly", "listen_gently", "set_boundary", "lighten_mood",
                "step_back", "talk_neutral", "listen_curiously", "safety_focus",
            })

    def test_memory_is_bounded(self) -> None:
        with TemporaryDirectory() as directory:
            memory = MemoryLayer(Path(directory) / "memory.json", max_interactions=2)
            memory.add_interaction({"user_sentence": "first"})
            memory.add_interaction({"user_sentence": "second"})
            memory.add_interaction({"user_sentence": "third"})

            self.assertEqual(
                [item["user_sentence"] for item in memory.load_interactions()],
                ["second", "third"],
            )

    def test_http_api_returns_safety_state_for_ue(self) -> None:
        with TemporaryDirectory() as directory:
            original_data_dir = api_server.DATA_DIR
            api_server.DATA_DIR = Path(directory)
            server = api_server.ThreadingHTTPServer(
                ("127.0.0.1", 0),
                api_server.OnionRequestHandler,
            )
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                body = json.dumps(
                    {
                        "session_id": "test-session",
                        "message": "죽고 싶어",
                        "use_nvidia": False,
                    },
                    ensure_ascii=False,
                ).encode("utf-8")
                request = urllib.request.Request(
                    f"http://127.0.0.1:{server.server_port}/v1/conversations/respond",
                    data=body,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(request, timeout=5) as response:
                    payload = json.loads(response.read().decode("utf-8"))

                self.assertEqual(payload["schema_version"], "onn-c.v1")
                self.assertTrue(payload["safety"]["triggered"])
                self.assertEqual(payload["character"]["stage"], "safety")
                self.assertEqual(payload["character"]["animation"], "safety_focus")
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)
                api_server.DATA_DIR = original_data_dir


if __name__ == "__main__":
    unittest.main()

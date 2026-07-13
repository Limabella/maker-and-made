import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from layers.decision_layer import decide_action
from play_cli import _load_local_env


NEUTRAL_BIG_FIVE = {
    "openness": 0.5,
    "conscientiousness": 0.5,
    "extraversion": 0.5,
    "agreeableness": 0.5,
    "neuroticism": 0.5,
}
NEUTRAL_EMOTION = {"joy": 0.0, "anger": 0.0, "trust": 0.0, "sadness": 0.0}


class DecisionLayerTests(unittest.TestCase):
    def test_question_defaults_to_direct_response(self) -> None:
        action = decide_action(
            "내가 손가락 몇 개를 들고 있을까?",
            NEUTRAL_BIG_FIVE,
            NEUTRAL_EMOTION,
            [],
        )
        self.assertEqual(action, "respond")

    def test_loads_dotenv_without_overriding_shell(self) -> None:
        with TemporaryDirectory() as directory:
            env_path = Path(directory) / ".env"
            env_path.write_text(
                '$env:NVIDIA_API_KEY = "file-key"\n'
                "NVIDIA_MODEL=file-model\n"
                "client = OpenAI()\n",
                encoding="utf-8",
            )
            with patch.dict(os.environ, {"NVIDIA_MODEL": "shell-model"}, clear=True):
                _load_local_env(env_path)
                self.assertEqual(os.environ["NVIDIA_API_KEY"], "file-key")
                self.assertEqual(os.environ["NVIDIA_MODEL"], "shell-model")
                self.assertNotIn("client", os.environ)

    def test_neutral_statement_does_not_force_follow_up_question(self) -> None:
        action = decide_action(
            "춤춰",
            NEUTRAL_BIG_FIVE,
            NEUTRAL_EMOTION,
            [{"npc_action": "respond"}],
        )
        self.assertEqual(action, "respond")


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
import sys
import unittest


MND_N_PATH = Path(__file__).resolve().parents[1]
if str(MND_N_PATH) not in sys.path:
    sys.path.insert(0, str(MND_N_PATH))

from support_layers.safety_gate import check_safety_gate


class SafetyGateTests(unittest.TestCase):
    def test_explicit_self_harm_signal_triggers_review(self) -> None:
        result = check_safety_gate("요즘 자해 생각이 반복돼요.")

        self.assertTrue(result["triggered"])
        self.assertEqual(result["reason"], "self_harm_signal")
        self.assertTrue(result["requires_context_review"])
        self.assertEqual(result["policy_version"], "1.0.0")

    def test_latin_keyword_does_not_match_inside_another_word(self) -> None:
        result = check_safety_gate("My diet changed this week.")

        self.assertFalse(result["triggered"])

    def test_ordinary_completion_phrase_is_not_blocked(self) -> None:
        result = check_safety_gate("오늘 일을 끝내고 집에서 쉬고 싶어요.")

        self.assertFalse(result["triggered"])

    def test_match_exposes_rule_id_for_audit(self) -> None:
        result = check_safety_gate("I want to die.")

        self.assertEqual(result["matched_signals"][0]["rule_id"], "self-harm-explicit-v1")


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
import sys
import unittest


MND_N_PATH = Path(__file__).resolve().parents[1]
if str(MND_N_PATH) not in sys.path:
    sys.path.insert(0, str(MND_N_PATH))

from support_layers.counselor_guidance_layer import (
    format_counselor_guidance,
    recommend_counselor_guidance,
)


SAFE = {"triggered": False, "message": None}
SUPPORT = {"perma_axis": "accomplishment"}


class CounselorGuidanceLayerTests(unittest.TestCase):
    def test_five_to_one_is_labeled_as_a_bounded_heuristic(self) -> None:
        guidance = recommend_counselor_guidance(
            "칭찬 5번과 피드백 1번을 어떻게 말할까요?",
            SUPPORT,
            SAFE,
        )

        self.assertEqual(guidance["card"], "five_to_one_feedback")
        self.assertEqual(guidance["kind"], "practice_heuristic")
        self.assertIn("보편적인 5:1 처방", guidance["research_note"])
        self.assertEqual(guidance["evidence"][0]["id"], "interaction_balance")

    def test_breathing_guidance_requires_consent_and_stop_condition(self) -> None:
        guidance = recommend_counselor_guidance(
            "4-7-8 호흡법을 권해볼까요?",
            SUPPORT,
            SAFE,
        )

        self.assertEqual(guidance["card"], "slow_breathing")
        self.assertIn("괜찮다면", guidance["suggested_message"])
        self.assertIn("어지러", guidance["caution"])
        self.assertEqual(
            [item["id"] for item in guidance["evidence"]],
            ["slow_breathing_meta_analysis", "adaptive_wearable_biofeedback"],
        )

    def test_resilience_guidance_preserves_group_level_boundary(self) -> None:
        guidance = recommend_counselor_guidance(
            "회복탄력성 연구 사례를 알려줘",
            SUPPORT,
            SAFE,
        )

        self.assertEqual(guidance["card"], "resilience")
        self.assertIn("약 1시간 뒤", guidance["research_note"])
        self.assertIn("개별 내담자", guidance["caution"])

    def test_perma_axis_supplies_proactive_default(self) -> None:
        guidance = recommend_counselor_guidance(
            "오늘 있었던 일을 말해줘",
            {"perma_axis": "meaning"},
            SAFE,
        )

        self.assertEqual(guidance["card"], "resilience")
        self.assertTrue(guidance["active"])

    def test_safety_stops_normal_counselor_coaching(self) -> None:
        guidance = recommend_counselor_guidance(
            "호흡법을 알려줘",
            SUPPORT,
            {"triggered": True, "message": "Use the safety path."},
        )

        self.assertFalse(guidance["active"])
        self.assertEqual(guidance["mode"], "safety")
        self.assertEqual(guidance["evidence"], [])
        self.assertNotIn("예시:", format_counselor_guidance(guidance))

    def test_formatter_includes_option_and_research_boundary(self) -> None:
        guidance = recommend_counselor_guidance(
            "긍정심리학을 적용해볼까요?",
            SUPPORT,
            SAFE,
        )
        rendered = format_counselor_guidance(guidance)

        self.assertIn("상담자 안내:", rendered)
        self.assertIn("예시:", rendered)
        self.assertIn("연구 메모:", rendered)


if __name__ == "__main__":
    unittest.main()

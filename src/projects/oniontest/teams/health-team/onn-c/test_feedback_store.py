from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from feedback_store import create_feedback_report, save_feedback_report


class FeedbackStoreTests(unittest.TestCase):
    def test_report_omits_conversation_content_by_default(self) -> None:
        report = create_feedback_report(
            {
                "session_id": "local-session",
                "category": "unsafe_response",
                "note": "The response minimized the risk.",
            }
        )

        self.assertFalse(report["content_included"])
        self.assertIsNone(report["content"])
        self.assertNotEqual(report["session_ref"], "local-session")

    def test_report_requires_consent_to_include_content(self) -> None:
        report = create_feedback_report(
            {
                "session_id": "local-session",
                "category": "missed_risk",
                "include_content": True,
                "ai_response": "A response selected by the user for review.",
            }
        )

        self.assertTrue(report["content_included"])
        self.assertEqual(report["content"]["ai_response"], "A response selected by the user for review.")

    def test_saved_report_enters_pending_review_queue(self) -> None:
        with TemporaryDirectory() as directory:
            report = save_feedback_report(
                {"session_id": "s1", "category": "false_alarm"},
                Path(directory),
            )
            lines = (Path(directory) / "pending_reports.jsonl").read_text(encoding="utf-8").splitlines()

        self.assertEqual(len(lines), 1)
        self.assertEqual(json.loads(lines[0])["report_id"], report["report_id"])
        self.assertEqual(report["status"], "pending_review")

    def test_unknown_category_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            create_feedback_report({"session_id": "s1", "category": "delete_policy"})


if __name__ == "__main__":
    unittest.main()

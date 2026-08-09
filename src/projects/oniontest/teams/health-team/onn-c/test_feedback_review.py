from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from feedback_review import (
    load_reports,
    public_report_view,
    summarize_reports,
    update_report,
)
from feedback_store import save_feedback_report


class FeedbackReviewTests(unittest.TestCase):
    def _create_report(self, directory: str) -> tuple[Path, dict]:
        report = save_feedback_report(
            {
                "session_id": "review-session",
                "category": "missed_risk",
                "note": "Reviewer-only note",
                "include_content": True,
                "ai_response": "Selected response content",
            },
            Path(directory),
        )
        return Path(directory) / "pending_reports.jsonl", report

    def test_list_view_hides_note_and_content_by_default(self) -> None:
        with TemporaryDirectory() as directory:
            path, _ = self._create_report(directory)
            report = load_reports(path)[0]

        view = public_report_view(report)
        self.assertNotIn("note", view)
        self.assertNotIn("content", view)
        self.assertTrue(view["content_included"])

    def test_summary_counts_status_and_category(self) -> None:
        with TemporaryDirectory() as directory:
            path, _ = self._create_report(directory)
            summary = summarize_reports(load_reports(path))

        self.assertEqual(summary["total"], 1)
        self.assertEqual(summary["by_status"], {"pending_review": 1})
        self.assertEqual(summary["by_category"], {"missed_risk": 1})

    def test_review_update_records_case_id(self) -> None:
        with TemporaryDirectory() as directory:
            path, report = self._create_report(directory)
            updated = update_report(
                path,
                report["report_id"],
                "converted_to_test",
                "local-reviewer",
                "Converted after reproducing the missed signal.",
                case_id="SAFE-C11",
            )
            stored = json.loads(path.read_text(encoding="utf-8").splitlines()[0])

        self.assertEqual(updated["status"], "converted_to_test")
        self.assertEqual(stored["review"]["case_id"], "SAFE-C11")

    def test_test_conversion_requires_case_id(self) -> None:
        with TemporaryDirectory() as directory:
            path, report = self._create_report(directory)
            with self.assertRaises(ValueError):
                update_report(
                    path,
                    report["report_id"],
                    "converted_to_test",
                    "local-reviewer",
                    "Missing test reference.",
                )


if __name__ == "__main__":
    unittest.main()

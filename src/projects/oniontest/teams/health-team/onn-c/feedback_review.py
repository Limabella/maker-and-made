import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPORT_STATUSES = {
    "pending_review",
    "confirmed_issue",
    "needs_context",
    "converted_to_test",
    "policy_updated",
    "dismissed",
}
DEFAULT_REPORT_FILE = Path(__file__).parent / "data" / "reports" / "pending_reports.jsonl"


def load_reports(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def summarize_reports(reports: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "total": len(reports),
        "by_status": dict(sorted(Counter(report["status"] for report in reports).items())),
        "by_category": dict(sorted(Counter(report["category"] for report in reports).items())),
        "with_content": sum(bool(report.get("content_included")) for report in reports),
    }


def public_report_view(report: dict[str, Any], include_content: bool = False) -> dict[str, Any]:
    view = {
        "report_id": report["report_id"],
        "created_at": report["created_at"],
        "status": report["status"],
        "category": report["category"],
        "turn_id": report.get("turn_id"),
        "content_included": report.get("content_included", False),
        "review": report.get("review"),
    }
    if include_content:
        view["note"] = report.get("note")
        view["content"] = report.get("content")
    return view


def update_report(
    path: Path,
    report_id: str,
    status: str,
    reviewer: str,
    review_note: str,
    case_id: str | None = None,
    policy_version: str | None = None,
) -> dict[str, Any]:
    if status not in REPORT_STATUSES - {"pending_review"}:
        raise ValueError("status is not a valid review outcome")
    if not reviewer.strip() or not review_note.strip():
        raise ValueError("reviewer and review_note are required")
    if status == "converted_to_test" and not case_id:
        raise ValueError("converted_to_test requires case_id")
    if status == "policy_updated" and not policy_version:
        raise ValueError("policy_updated requires policy_version")

    reports = load_reports(path)
    matched = None
    for report in reports:
        if report.get("report_id") == report_id:
            report["status"] = status
            report["review"] = {
                "reviewed_at": datetime.now(timezone.utc).isoformat(),
                "reviewer": reviewer.strip(),
                "note": review_note.strip(),
                "case_id": case_id,
                "policy_version": policy_version,
            }
            matched = report
            break

    if matched is None:
        raise ValueError("report_id was not found")

    temporary_path = path.with_suffix(path.suffix + ".tmp")
    temporary_path.write_text(
        "".join(json.dumps(report, ensure_ascii=False) + "\n" for report in reports),
        encoding="utf-8",
    )
    temporary_path.replace(path)
    return matched


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Review local Onion AI feedback reports.")
    parser.add_argument("--report-file", type=Path, default=DEFAULT_REPORT_FILE)
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List reports without raw content.")
    list_parser.add_argument("--status", choices=sorted(REPORT_STATUSES))
    list_parser.add_argument("--include-content", action="store_true")

    update_parser = subparsers.add_parser("update", help="Record a human review outcome.")
    update_parser.add_argument("--report-id", required=True)
    update_parser.add_argument(
        "--status",
        required=True,
        choices=sorted(REPORT_STATUSES - {"pending_review"}),
    )
    update_parser.add_argument("--reviewer", required=True)
    update_parser.add_argument("--review-note", required=True)
    update_parser.add_argument("--case-id")
    update_parser.add_argument("--policy-version")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    if args.command == "list":
        reports = load_reports(args.report_file)
        if args.status:
            reports = [report for report in reports if report["status"] == args.status]
        payload = {
            "summary": summarize_reports(reports),
            "reports": [
                public_report_view(report, include_content=args.include_content)
                for report in reports
            ],
        }
    else:
        report = update_report(
            args.report_file,
            args.report_id,
            args.status,
            args.reviewer,
            args.review_note,
            args.case_id,
            args.policy_version,
        )
        payload = public_report_view(report)

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

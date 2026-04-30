from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = ROOT / "qa_tests" / "data" / "manual_frontend_checklist.csv"
REPORTS = ROOT / "qa_tests" / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

rows = list(csv.DictReader(CHECKLIST.open(encoding="utf-8")))
passed = [r for r in rows if r.get("status", "").strip().lower() == "pass"]
failed = [r for r in rows if r.get("status", "").strip().lower() == "fail"]
pending = [r for r in rows if r not in passed and r not in failed]

report = [
    "# MathPath Frontend Manual QA Report",
    "",
    f"Generated: {datetime.now().isoformat(timespec='seconds')}",
    "",
    f"Total checks: {len(rows)}",
    f"Passed: {len(passed)}",
    f"Failed: {len(failed)}",
    f"Pending/blank: {len(pending)}",
    "",
    "## Failed Checks",
]

if failed:
    for row in failed:
        report.append(f"- {row['check_id']} — {row['test_item']} | Notes: {row.get('notes', '')}")
else:
    report.append("None")

report.append("\n## Pending Checks")
if pending:
    for row in pending:
        report.append(f"- {row['check_id']} — {row['test_item']}")
else:
    report.append("None")

out = REPORTS / "manual_frontend_qa_report.md"
out.write_text("\n".join(report), encoding="utf-8")
print(f"Report written to {out}")

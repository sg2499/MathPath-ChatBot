from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "qa_tests" / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

console = Console()


def run() -> int:
    api_base = os.getenv("MATHPATH_API_BASE_URL", "http://localhost:8000")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS / f"pytest_report_{timestamp}.txt"

    console.print(Panel.fit(f"Running MathPath QA tests\nBackend: {api_base}"))

    command = [
        sys.executable,
        "-m",
        "pytest",
        str(ROOT / "qa_tests"),
        "-v",
        "--tb=short",
    ]

    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    output = completed.stdout + "\n" + completed.stderr
    report_path.write_text(output, encoding="utf-8")

    if completed.returncode == 0:
        console.print(f"[bold green]All automated QA tests passed.[/bold green]")
    else:
        console.print(f"[bold red]Some QA tests failed.[/bold red]")

    console.print(f"Report saved to: {report_path}")
    console.print(output)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(run())

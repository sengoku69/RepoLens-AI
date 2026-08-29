from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent
CASES_DIR = ROOT / "cases"
RESULTS_FILE = ROOT / "baseline_results.json"


def run_case(case_path: Path) -> dict:
    command = [
        sys.executable,
        "-m",
        "tools.baseline_analyzer",
        str(case_path),
    ]

    completed = subprocess.run(
        command,
        cwd=Path(__file__).parent.parent,
        capture_output=True,
        text=True,
    )

    if completed.returncode != 0:
        return {
            "case": case_path.name,
            "status": "error",
            "error": completed.stderr[-2000:],
        }

    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {
            "case": case_path.name,
            "status": "error",
            "error": "Baseline output was not valid JSON.",
            "output": completed.stdout[-2000:],
        }

    baseline = result["baseline"]

    return {
        "case": case_path.name,
        "status": "success",
        "score": baseline["score"],
        "maximum_score": baseline["maximum_score"],
        "percentage": baseline["percentage"],
        "findings": baseline["findings"],
    }


def main() -> None:
    if not CASES_DIR.exists():
        print("Evaluation cases directory does not exist.")
        sys.exit(1)

    cases = sorted(
        path
        for path in CASES_DIR.iterdir()
        if path.is_dir()
    )

    if not cases:
        print("No evaluation cases found.")
        sys.exit(1)

    results = [
        run_case(case_path)
        for case_path in cases
    ]

    successful = [
        result
        for result in results
        if result["status"] == "success"
    ]

    average_score = 0

    if successful:
        average_score = round(
            sum(
                result["percentage"]
                for result in successful
            )
            / len(successful),
            2,
        )

    report = {
        "evaluation": "deterministic_baseline",
        "case_count": len(cases),
        "successful_cases": len(successful),
        "average_score": average_score,
        "results": results,
    }

    RESULTS_FILE.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            report,
            indent=2,
        )
    )

    print()
    print(
        f"Saved baseline results to: "
        f"{RESULTS_FILE}"
    )


if __name__ == "__main__":
    main()
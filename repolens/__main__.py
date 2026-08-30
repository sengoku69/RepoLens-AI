from __future__ import annotations

import sys
from typing import Any

from agents.graph import run_repolens


def _print_header() -> None:
    print("=" * 58)
    print("                         RepoLens-AI")
    print("                  Repository Risk Analyzer")
    print("=" * 58)
    print()


def _print_final_report(
    result: dict[str, Any],
) -> None:
    report = result.get(
        "final_report",
        {},
    )

    if not isinstance(report, dict):
        print("Final report is unavailable.")
        return

    risk_score = report.get(
        "risk_score",
        "N/A",
    )

    risk_level = str(
        report.get(
            "risk_level",
            "unknown",
        )
    ).upper()

    finding_count = report.get(
        "finding_count",
        0,
    )

    severity_counts = report.get(
        "severity_counts",
        {},
    )

    findings = report.get(
        "findings",
        [],
    )

    print("-" * 58)
    print("                    FINAL RISK REPORT")
    print("-" * 58)
    print()
    print(f"Risk Level : {risk_level}")
    print(f"Risk Score : {risk_score}")
    print(f"Findings   : {finding_count}")
    print()

    if isinstance(severity_counts, dict):
        print("Severity Summary:")
        print(
            f"  Critical : "
            f"{severity_counts.get('critical', 0)}"
        )
        print(
            f"  High     : "
            f"{severity_counts.get('high', 0)}"
        )
        print(
            f"  Medium   : "
            f"{severity_counts.get('medium', 0)}"
        )
        print(
            f"  Low      : "
            f"{severity_counts.get('low', 0)}"
        )

    if isinstance(findings, list) and findings:
        print()
        print("Findings:")
        print()

        for index, finding in enumerate(
            findings,
            start=1,
        ):
            if not isinstance(finding, dict):
                continue

            severity = str(
                finding.get(
                    "severity",
                    "unknown",
                )
            ).upper()

            category = str(
                finding.get(
                    "category",
                    "unknown",
                )
            )

            description = str(
                finding.get(
                    "finding",
                    "",
                )
            )

            recommendation = str(
                finding.get(
                    "recommendation",
                    "",
                )
            )

            print(
                f"{index}. [{severity}] "
                f"{category}"
            )
            print(
                f"   {description}"
            )

            if recommendation:
                print(
                    f"   Recommendation: "
                    f"{recommendation}"
                )

            print()

    print("-" * 58)
    print("Analysis completed successfully.")
    print("-" * 58)


def main() -> None:
    repository_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "."
    )

    try:
        _print_header()

        print(
            f"Repository: {repository_path}"
        )
        print()
        print(
            "Running repository analysis..."
        )
        print()

        result = run_repolens(
            repository_path
        )

        _print_final_report(result)

    except Exception as error:
        print()
        print("-" * 58)
        print(
            "RepoLens-AI failed to complete analysis."
        )
        print("-" * 58)
        print()
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
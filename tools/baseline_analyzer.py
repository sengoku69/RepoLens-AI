"""
Deterministic baseline analyzer for RepoLens-AI.

This module analyzes repository evidence and produces a deterministic
baseline score. It does not require an LLM or external API.
"""

import json
import sys
from pathlib import Path

from tools.evidence_collector import collect_repository_evidence


def calculate_baseline_score(evidence: dict) -> dict:
    """
    Calculate a deterministic repository-quality baseline score.

    Maximum score: 100
    """

    repository = evidence["repository"]
    dependencies = evidence["dependencies"]
    tests = evidence["tests"]

    score = 0
    maximum_score = 100
    findings = []

    # ---------------------------------------------------------
    # Repository structure: 25 points
    # ---------------------------------------------------------

    # README: 10 points
    if repository["readme_present"]:
        score += 10
    else:
        findings.append(
            {
                "category": "documentation",
                "severity": "medium",
                "finding": "Repository does not contain a README.",
            }
        )

    # Source directories: 15 points
    if repository["source_directories"]:
        score += 15
    else:
        findings.append(
            {
                "category": "structure",
                "severity": "medium",
                "finding": "No source directories were detected.",
            }
        )

    # ---------------------------------------------------------
    # Dependencies: 20 points
    # ---------------------------------------------------------

    # Dependency file: 10 points
    if dependencies["dependency_files"]:
        score += 10
    else:
        findings.append(
            {
                "category": "dependencies",
                "severity": "medium",
                "finding": "No dependency file was detected.",
            }
        )

    # Detected dependencies: 10 points
    if dependencies["dependency_count"] > 0:
        score += 10
    else:
        findings.append(
            {
                "category": "dependencies",
                "severity": "low",
                "finding": "No dependencies were detected.",
            }
        )

    # ---------------------------------------------------------
    # Testing: 40 points
    # ---------------------------------------------------------

    # Dedicated test directory: 10 points
    if tests.get("test_target"):
        score += 10
    else:
        findings.append(
            {
                "category": "testing",
                "severity": "medium",
                "finding": "No dedicated test directory was detected.",
            }
        )

    # Passing test suite: 20 points
    if tests.get("status") == "passed":
        score += 20
    else:
        findings.append(
            {
                "category": "testing",
                "severity": "high",
                "finding": "Repository test suite is not passing.",
            }
        )

    # Executable tests: 10 points
    if tests.get("tests_collected", 0) > 0:
        score += 10
    else:
        findings.append(
            {
                "category": "testing",
                "severity": "medium",
                "finding": "No executable tests were detected.",
            }
        )

    # ---------------------------------------------------------
    # Language detection: 15 points
    # ---------------------------------------------------------

    if repository["languages"]:
        score += 15
    else:
        findings.append(
            {
                "category": "structure",
                "severity": "medium",
                "finding": "No programming languages were detected.",
            }
        )

    return {
        "score": score,
        "maximum_score": maximum_score,
        "percentage": round(
            (score / maximum_score) * 100,
            2,
        ),
        "findings": findings,
    }


def analyze_repository(repository_path: str) -> dict:
    """
    Run deterministic repository analysis.
    """

    root = Path(repository_path).resolve()

    if not root.exists():
        raise FileNotFoundError(
            f"Repository does not exist: {root}"
        )

    if not root.is_dir():
        raise NotADirectoryError(
            f"Path is not a directory: {root}"
        )

    evidence = collect_repository_evidence(
        str(root)
    )

    baseline = calculate_baseline_score(
        evidence
    )

    return {
        "repository_path": str(root),
        "analyzer": "deterministic_baseline",
        "evidence": evidence,
        "baseline": baseline,
    }


def main() -> None:
    """
    Command-line entry point.
    """

    if len(sys.argv) != 2:
        print(
            "Usage: python -m tools.baseline_analyzer "
            "<repository_path>"
        )
        sys.exit(1)

    repository_path = sys.argv[1]

    try:
        result = analyze_repository(
            repository_path
        )

        print(
            json.dumps(
                result,
                indent=2,
            )
        )

    except (
        FileNotFoundError,
        NotADirectoryError,
    ) as error:
        print(f"Error: {error}")
        sys.exit(1)


# IMPORTANT:
if __name__ == "__main__":
    main()
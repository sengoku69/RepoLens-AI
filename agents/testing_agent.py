from __future__ import annotations

from typing import Any

from agents.state import RepoLensState


def analyze_testing(state: RepoLensState) -> dict[str, Any]:
    evidence = state.get("evidence", {})
    tests = evidence.get("tests", {})

    findings = []

    test_target = tests.get("test_target")
    status = tests.get("status")
    collected = tests.get("tests_collected", 0)
    passed = tests.get("tests_passed", 0)
    failed = tests.get("tests_failed", 0)
    errors = tests.get("tests_errors", 0)
    skipped = tests.get("tests_skipped", 0)

    if not test_target:
        findings.append(
            {
                "category": "testing",
                "severity": "medium",
                "finding": "No dedicated test target was detected.",
                "evidence": tests.get("message", "No test target"),
            }
        )

    if status != "passed":
        findings.append(
            {
                "category": "testing",
                "severity": "high",
                "finding": "Repository test suite is not passing.",
                "evidence": {
                    "status": status,
                    "failed": failed,
                    "errors": errors,
                },
            }
        )

    if collected == 0:
        findings.append(
            {
                "category": "testing",
                "severity": "medium",
                "finding": "No executable tests were detected.",
                "evidence": "tests_collected=0",
            }
        )

    if collected > 0 and passed == collected:
        test_health = "healthy"
    elif failed > 0 or errors > 0:
        test_health = "failing"
    else:
        test_health = "incomplete"

    return {
        "testing_analysis": {
            "agent": "testing_agent",
            "findings": findings,
            "summary": {
                "framework": tests.get("test_framework"),
                "status": status,
                "tests_collected": collected,
                "tests_passed": passed,
                "tests_failed": failed,
                "tests_errors": errors,
                "tests_skipped": skipped,
                "test_health": test_health,
            },
        }
    }
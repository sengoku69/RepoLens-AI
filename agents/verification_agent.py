from __future__ import annotations

from typing import Any

from agents.state import RepoLensState


VALID_SEVERITIES = {
    "low",
    "medium",
    "high",
    "critical",
}


def _text(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip().lower()


def _finding_category(finding: dict[str, Any]) -> str:
    return _text(
        finding.get("category", "unknown")
    )


def _evidence_contains(
    evidence: dict[str, Any],
    terms: list[str],
) -> bool:
    evidence_text = _text(evidence)

    if not evidence_text:
        return False

    meaningful_terms = [
        term
        for term in terms
        if len(term.strip()) >= 4
    ]

    if not meaningful_terms:
        return False

    return all(
        term.strip().lower() in evidence_text
        for term in meaningful_terms
    )


def _repository_finding_supported(
    finding: dict[str, Any],
    evidence: dict[str, Any],
) -> bool:
    repository_evidence = evidence.get(
        "repository",
        {},
    )

    finding_evidence = _text(
        finding.get("evidence", "")
    )

    finding_text = _text(
        finding.get("finding", "")
    )

    repository_text = _text(
        repository_evidence
    )

    if not finding_evidence:
        return False

    if not repository_text:
        return False

    evidence_terms = [
        word
        for word in finding_evidence.split()
        if len(word) >= 4
    ]

    matching_terms = [
        word
        for word in evidence_terms
        if word in repository_text
    ]

    if len(matching_terms) < 2:
        return False

    if "readme" in finding_text:
        return bool(
            repository_evidence.get(
                "readme_present",
                False,
            )
        )

    if "test director" in finding_text:
        return bool(
            repository_evidence.get(
                "test_directories"
            ) is not None
        )

    if "source director" in finding_text:
        return bool(
            repository_evidence.get(
                "source_directories"
            ) is not None
        )

    return len(matching_terms) >= 3


def _dependency_finding_supported(
    finding: dict[str, Any],
    evidence: dict[str, Any],
) -> bool:
    dependency_evidence = evidence.get(
        "dependencies",
        {},
    )

    dependencies = dependency_evidence.get(
        "items",
        dependency_evidence.get(
            "dependencies",
            [],
        ),
    )

    if not isinstance(dependencies, list):
        return False

    if not dependencies:
        return False

    finding_evidence = _text(
        finding.get("evidence", "")
    )

    finding_text = _text(
        finding.get("finding", "")
    )

    dependency_text = _text(
        dependency_evidence
    )

    if not finding_evidence:
        return False

    if not dependency_text:
        return False

    if (
        "unpinned" in finding_text
        or "unpin" in finding_text
        or "version" in finding_text
    ):
        unpinned_dependencies = [
            item
            for item in dependencies
            if isinstance(item, dict)
            and not item.get("version")
        ]

        if unpinned_dependencies:
            return True

    package_names = [
        _text(item.get("name"))
        for item in dependencies
        if isinstance(item, dict)
        and item.get("name")
    ]

    mentioned_packages = [
        package
        for package in package_names
        if package and package in finding_evidence
    ]

    if mentioned_packages:
        return True

    evidence_terms = [
        word
        for word in finding_evidence.split()
        if len(word) >= 4
    ]

    matching_terms = [
        word
        for word in evidence_terms
        if word in dependency_text
    ]

    return len(matching_terms) >= 3


def _testing_finding_supported(
    finding: dict[str, Any],
    evidence: dict[str, Any],
) -> bool:
    testing_evidence = evidence.get(
        "tests",
        {},
    )

    if not isinstance(testing_evidence, dict):
        return False

    finding_text = _text(
        finding.get("finding", "")
    )

    finding_evidence = _text(
        finding.get("evidence", "")
    )

    if not finding_evidence:
        return False

    status = _text(
        testing_evidence.get("status")
    )

    collected = testing_evidence.get(
        "tests_collected"
    )

    passed = testing_evidence.get(
        "tests_passed"
    )

    failed = testing_evidence.get(
        "tests_failed"
    )

    errors = testing_evidence.get(
        "tests_errors"
    )

    if (
        "not passing" in finding_text
        or "failing test" in finding_text
        or "test failure" in finding_text
    ):
        return (
            status not in {
                "",
                "passed",
            }
            or bool(failed)
            or bool(errors)
        )

    if (
        "no executable test" in finding_text
        or "no tests" in finding_text
    ):
        if collected is None:
            return False

        return collected == 0

    if (
        "test coverage" in finding_text
        or "lack test coverage" in finding_text
        or "lack dedicated test" in finding_text
    ):
        return (
            "test" in finding_evidence
            and collected is not None
        )

    return (
        "test" in finding_evidence
        and (
            collected is not None
            or passed is not None
            or failed is not None
            or errors is not None
        )
    )


def _is_supported_finding(
    finding: dict[str, Any],
    evidence: dict[str, Any],
) -> bool:
    category = _finding_category(
        finding
    )

    if category == "dependencies":
        return _dependency_finding_supported(
            finding,
            evidence,
        )

    if category == "testing":
        return _testing_finding_supported(
            finding,
            evidence,
        )

    if category in {
        "repository",
        "documentation",
        "architecture",
        "maintainability",
    }:
        return _repository_finding_supported(
            finding,
            evidence,
        )

    finding_evidence = _text(
        finding.get("evidence", "")
    )

    if not finding_evidence:
        return False

    combined_evidence = _text(
        evidence
    )

    evidence_terms = [
        word
        for word in finding_evidence.split()
        if len(word) >= 4
    ]

    matches = [
        word
        for word in evidence_terms
        if word in combined_evidence
    ]

    return len(matches) >= 3


def _normalize_finding(
    finding: dict[str, Any],
    agent: str,
) -> dict[str, Any]:
    severity = _text(
        finding.get(
            "severity",
            "medium",
        )
    )

    if severity not in VALID_SEVERITIES:
        severity = "medium"

    category = _text(
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
    ).strip()

    evidence = finding.get(
        "evidence",
        "",
    )

    recommendation = str(
        finding.get(
            "recommendation",
            "",
        )
    ).strip()

    return {
        "agent": agent,
        "category": category or "unknown",
        "severity": severity,
        "finding": description,
        "evidence": evidence,
        "recommendation": recommendation,
    }


def _verify_deterministic_findings(
    state: RepoLensState,
) -> list[dict[str, Any]]:
    verified_findings: list[dict[str, Any]] = []

    deterministic_agents = [
        (
            "repository_agent",
            state.get(
                "repository_analysis",
                {},
            ),
        ),
        (
            "dependency_agent",
            state.get(
                "dependency_analysis",
                {},
            ),
        ),
        (
            "testing_agent",
            state.get(
                "testing_analysis",
                {},
            ),
        ),
    ]

    for agent_name, analysis in deterministic_agents:
        if not isinstance(analysis, dict):
            continue

        findings = analysis.get(
            "findings",
            [],
        )

        if not isinstance(findings, list):
            continue

        for finding in findings:
            if not isinstance(finding, dict):
                continue

            normalized = _normalize_finding(
                finding,
                agent_name,
            )

            if not normalized["finding"]:
                continue

            verified_findings.append(
                normalized
            )

    return verified_findings


def _verify_reasoning_findings(
    state: RepoLensState,
    evidence: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    verified_findings: list[dict[str, Any]] = []
    rejected_findings: list[dict[str, Any]] = []

    reasoning = state.get(
        "reasoning_analysis",
        {},
    )

    if not isinstance(reasoning, dict):
        return (
            verified_findings,
            rejected_findings,
        )

    reasoning_findings = reasoning.get(
        "findings",
        [],
    )

    if not isinstance(reasoning_findings, list):
        return (
            verified_findings,
            rejected_findings,
        )

    for finding in reasoning_findings:
        if not isinstance(finding, dict):
            continue

        normalized = _normalize_finding(
            finding,
            "llm_reasoning_agent",
        )

        if not normalized["finding"]:
            rejected_findings.append(
                {
                    **normalized,
                    "reason": (
                        "Finding contains no description."
                    ),
                }
            )
            continue

        if _is_supported_finding(
            finding,
            evidence,
        ):
            verified_findings.append(
                normalized
            )
        else:
            rejected_findings.append(
                {
                    **normalized,
                    "reason": (
                        "Finding could not be "
                        "supported by repository evidence."
                    ),
                }
            )

    return (
        verified_findings,
        rejected_findings,
    )


def _deduplicate_findings(
    findings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    unique_findings: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()

    for finding in findings:
        key = (
            _text(finding.get("category")),
            _text(finding.get("severity")),
            _text(finding.get("finding")),
        )

        if key in seen:
            continue

        seen.add(key)
        unique_findings.append(finding)

    return unique_findings


def verify_findings(
    state: RepoLensState,
) -> dict[str, Any]:
    evidence = state.get(
        "evidence",
        {},
    )

    if not isinstance(evidence, dict):
        evidence = {}

    deterministic_findings = (
        _verify_deterministic_findings(
            state
        )
    )

    (
        reasoning_verified,
        rejected_findings,
    ) = _verify_reasoning_findings(
        state,
        evidence,
    )

    verified_findings = _deduplicate_findings(
        deterministic_findings
        + reasoning_verified
    )

    severity_counts = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for finding in verified_findings:
        severity = finding.get(
            "severity"
        )

        if severity in severity_counts:
            severity_counts[severity] += 1

    return {
        "verification": {
            "status": "completed",
            "verified_findings": verified_findings,
            "rejected_findings": rejected_findings,
            "finding_count": len(
                verified_findings
            ),
            "rejected_count": len(
                rejected_findings
            ),
            "severity_counts": severity_counts,
        }
    }
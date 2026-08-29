from __future__ import annotations

from typing import Any

from agents.state import RepoLensState


VALID_SEVERITIES = {
    "low",
    "medium",
    "high",
    "critical",
}


def _is_supported_finding(
    finding: dict[str, Any],
    evidence: dict[str, Any],
) -> bool:
    evidence_text = str(
        finding.get("evidence", "")
    ).lower()

    if not evidence_text:
        return False

    repository_text = str(
        evidence.get("repository", {})
    ).lower()

    dependency_text = str(
        evidence.get("dependencies", {})
    ).lower()

    testing_text = str(
        evidence.get("tests", {})
    ).lower()

    combined_evidence = (
        repository_text
        + " "
        + dependency_text
        + " "
        + testing_text
    )

    evidence_words = [
        word
        for word in evidence_text.split()
        if len(word) > 3
    ]

    matches = sum(
        1
        for word in evidence_words
        if word in combined_evidence
    )

    return matches >= 2


def _normalize_finding(
    finding: dict[str, Any],
    agent: str,
) -> dict[str, Any]:
    severity = str(
        finding.get(
            "severity",
            "medium",
        )
    ).lower()

    if severity not in VALID_SEVERITIES:
        severity = "medium"

    return {
        "agent": agent,
        "category": finding.get(
            "category",
            "unknown",
        ),
        "severity": severity,
        "finding": finding.get(
            "finding",
            "",
        ),
        "evidence": finding.get(
            "evidence",
            "",
        ),
        "recommendation": finding.get(
            "recommendation",
            "",
        ),
    }


def verify_findings(
    state: RepoLensState,
) -> dict[str, Any]:
    evidence = state.get(
        "evidence",
        {},
    )

    verified_findings: list[dict[str, Any]] = []
    rejected_findings: list[dict[str, Any]] = []

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

            verified_findings.append(
                normalized
            )

    reasoning = state.get(
        "reasoning_analysis",
        {},
    )

    reasoning_findings = reasoning.get(
        "findings",
        [],
    )

    if isinstance(reasoning_findings, list):
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

    severity_counts = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for finding in verified_findings:
        severity = finding["severity"]

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
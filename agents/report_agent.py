from __future__ import annotations

from typing import Any

from agents.state import RepoLensState


SEVERITY_WEIGHT = {
    "critical": 10,
    "high": 7,
    "medium": 4,
    "low": 1,
}


def _severity_rank(severity: str) -> int:
    return {
        "critical": 4,
        "high": 3,
        "medium": 2,
        "low": 1,
    }.get(severity, 0)


def _finding_key(finding: dict[str, Any]) -> str:
    category = str(
        finding.get("category", "")
    ).strip().lower()

    text = str(
        finding.get("finding", "")
    ).strip().lower()

    return f"{category}:{text}"


def _are_related(
    first: dict[str, Any],
    second: dict[str, Any],
) -> bool:
    first_category = str(
        first.get("category", "")
    ).lower()

    second_category = str(
        second.get("category", "")
    ).lower()

    if first_category != second_category:
        return False

    first_text = str(
        first.get("finding", "")
    ).lower()

    second_text = str(
        second.get("finding", "")
    ).lower()

    dependency_terms = [
        "unpinned",
        "version",
        "dependency",
        "dependencies",
    ]

    if first_category == "dependencies":
        return any(
            term in first_text
            for term in dependency_terms
        ) and any(
            term in second_text
            for term in dependency_terms
        )

    return False


def _deduplicate_findings(
    findings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    unique: list[dict[str, Any]] = []
    seen_keys: set[str] = set()

    for finding in findings:
        key = _finding_key(finding)

        if key in seen_keys:
            continue

        related_index = None

        for index, existing in enumerate(unique):
            if _are_related(
                existing,
                finding,
            ):
                related_index = index
                break

        if related_index is not None:
            existing = unique[related_index]

            if _severity_rank(
                finding.get("severity", "low")
            ) > _severity_rank(
                existing.get("severity", "low")
            ):
                unique[related_index] = finding

            continue

        seen_keys.add(key)
        unique.append(finding)

    return unique


def _calculate_risk_score(
    findings: list[dict[str, Any]],
) -> int:
    risk = sum(
        SEVERITY_WEIGHT.get(
            finding.get("severity", "low"),
            1,
        )
        for finding in findings
    )

    return min(
        100,
        risk,
    )


def _risk_level(score: int) -> str:
    if score >= 25:
        return "critical"

    if score >= 15:
        return "high"

    if score >= 7:
        return "medium"

    if score > 0:
        return "low"

    return "healthy"


def build_final_report(
    state: RepoLensState,
) -> dict[str, Any]:
    verification = state.get(
        "verification",
        {},
    )

    findings = verification.get(
        "verified_findings",
        [],
    )

    if not isinstance(findings, list):
        findings = []

    deduplicated = _deduplicate_findings(
        findings
    )

    deduplicated.sort(
        key=lambda finding: _severity_rank(
            finding.get("severity", "low")
        ),
        reverse=True,
    )

    risk_score = _calculate_risk_score(
        deduplicated
    )

    severity_counts = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for finding in deduplicated:
        severity = finding.get(
            "severity",
            "low",
        )

        if severity in severity_counts:
            severity_counts[severity] += 1

    report = {
        "repository_path": state.get(
            "repository_path",
            "",
        ),
        "risk_score": risk_score,
        "risk_level": _risk_level(
            risk_score
        ),
        "finding_count": len(
            deduplicated
        ),
        "severity_counts": severity_counts,
        "findings": deduplicated,
    }

    return {
        "final_report": report
    }
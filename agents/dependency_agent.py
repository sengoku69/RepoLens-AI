from __future__ import annotations

from typing import Any

from agents.state import RepoLensState


def analyze_dependencies(state: RepoLensState) -> dict[str, Any]:
    evidence = state.get("evidence", {})
    dependencies = evidence.get("dependencies", {})

    items = dependencies.get("items", [])
    dependency_files = dependencies.get("dependency_files", [])

    findings = []

    if not dependency_files:
        findings.append(
            {
                "category": "dependencies",
                "severity": "medium",
                "finding": "No dependency file was detected.",
                "evidence": "dependency_files=[]",
            }
        )

    if not items:
        findings.append(
            {
                "category": "dependencies",
                "severity": "low",
                "finding": "No dependencies were detected.",
                "evidence": "dependency_count=0",
            }
        )

    unpinned = [
        item
        for item in items
        if item.get("version") is None
    ]

    if unpinned:
        findings.append(
            {
                "category": "dependencies",
                "severity": "medium",
                "finding": (
                    f"{len(unpinned)} of {len(items)} "
                    "dependencies do not specify a version."
                ),
                "evidence": [
                    item.get("name")
                    for item in unpinned
                ],
            }
        )

    if len(items) >= 10:
        findings.append(
            {
                "category": "dependencies",
                "severity": "medium",
                "finding": (
                    f"Repository declares {len(items)} dependencies, "
                    "which may increase maintenance complexity."
                ),
                "evidence": [
                    item.get("name")
                    for item in items
                ],
            }
        )

    return {
        "dependency_analysis": {
            "agent": "dependency_agent",
            "findings": findings,
            "summary": {
                "dependency_files": dependency_files,
                "dependency_count": len(items),
                "unpinned_count": len(unpinned),
                "dependencies": [
                    item.get("name")
                    for item in items
                ],
            },
        }
    }
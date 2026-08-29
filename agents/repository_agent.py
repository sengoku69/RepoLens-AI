from __future__ import annotations

from typing import Any

from agents.state import RepoLensState


def analyze_repository(state: RepoLensState) -> dict[str, Any]:
    evidence = state.get("evidence", {})
    repository = evidence.get("repository", {})

    findings = []

    if not repository.get("readme_present", False):
        findings.append(
            {
                "category": "documentation",
                "severity": "medium",
                "finding": "Repository does not contain a README.",
                "evidence": "readme_present=false",
            }
        )

    if not repository.get("source_directories"):
        findings.append(
            {
                "category": "structure",
                "severity": "high",
                "finding": "No source directories were detected.",
                "evidence": "source_directories=[]",
            }
        )

    if not repository.get("languages"):
        findings.append(
            {
                "category": "structure",
                "severity": "medium",
                "finding": "No programming languages were detected.",
                "evidence": "languages={}",
            }
        )

    if repository.get("file_count", 0) == 0:
        findings.append(
            {
                "category": "structure",
                "severity": "high",
                "finding": "Repository contains no files.",
                "evidence": "file_count=0",
            }
        )

    return {
        "repository_analysis": {
            "agent": "repository_agent",
            "findings": findings,
            "summary": {
                "file_count": repository.get("file_count", 0),
                "languages": repository.get("languages", {}),
                "source_directories": repository.get(
                    "source_directories", []
                ),
                "test_directories": repository.get(
                    "test_directories", []
                ),
                "readme_present": repository.get(
                    "readme_present", False
                ),
            },
        }
    }
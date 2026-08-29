from __future__ import annotations

from typing import Any, TypedDict


class RepoLensState(TypedDict, total=False):
    repository_path: str
    evidence: dict[str, Any]
    repository_analysis: dict[str, Any]
    dependency_analysis: dict[str, Any]
    testing_analysis: dict[str, Any]
    reasoning_analysis: dict[str, Any]
    verification: dict[str, Any]
    final_report: dict[str, Any]
from __future__ import annotations

from typing import Any

from langgraph.graph import END, START, StateGraph

from agents.dependency_agent import analyze_dependencies
from agents.reasoning_agent import analyze_with_llm
from agents.report_agent import build_final_report
from agents.repository_agent import analyze_repository
from agents.state import RepoLensState
from agents.testing_agent import analyze_testing
from agents.verification_agent import verify_findings


def build_graph():
    graph = StateGraph(RepoLensState)

    graph.add_node(
        "repository_analysis",
        analyze_repository,
    )

    graph.add_node(
        "dependency_analysis",
        analyze_dependencies,
    )

    graph.add_node(
        "testing_analysis",
        analyze_testing,
    )

    graph.add_node(
        "reasoning_analysis",
        analyze_with_llm,
    )

    graph.add_node(
        "verification",
        verify_findings,
    )

    graph.add_node(
        "final_report",
        build_final_report,
    )

    graph.add_edge(
        START,
        "repository_analysis",
    )

    graph.add_edge(
        "repository_analysis",
        "dependency_analysis",
    )

    graph.add_edge(
        "dependency_analysis",
        "testing_analysis",
    )

    graph.add_edge(
        "testing_analysis",
        "reasoning_analysis",
    )

    graph.add_edge(
        "reasoning_analysis",
        "verification",
    )

    graph.add_edge(
        "verification",
        "final_report",
    )

    graph.add_edge(
        "final_report",
        END,
    )

    return graph.compile()


def run_repolens(
    repository_path: str,
) -> dict[str, Any]:
    from tools.evidence_collector import (
        collect_repository_evidence,
    )

    evidence = collect_repository_evidence(
        repository_path
    )

    initial_state: RepoLensState = {
        "repository_path": repository_path,
        "evidence": evidence,
    }

    app = build_graph()

    return app.invoke(initial_state)
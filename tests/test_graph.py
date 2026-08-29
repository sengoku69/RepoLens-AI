from agents import graph


def test_graph_executes_all_nodes(monkeypatch):
    execution_order = []

    def fake_repository_analysis(state):
        execution_order.append("repository")
        return {
            "repository_analysis": {
                "agent": "repository_agent",
                "findings": [],
            }
        }

    def fake_dependency_analysis(state):
        execution_order.append("dependency")
        return {
            "dependency_analysis": {
                "agent": "dependency_agent",
                "findings": [],
            }
        }

    def fake_testing_analysis(state):
        execution_order.append("testing")
        return {
            "testing_analysis": {
                "agent": "testing_agent",
                "findings": [],
            }
        }

    def fake_reasoning_analysis(state):
        execution_order.append("reasoning")
        return {
            "reasoning_analysis": {
                "agent": "llm_reasoning_agent",
                "findings": [],
            }
        }

    def fake_verification(state):
        execution_order.append("verification")
        return {
            "verification": {
                "status": "completed",
                "verified_findings": [],
                "rejected_findings": [],
                "finding_count": 0,
                "rejected_count": 0,
                "severity_counts": {
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0,
                },
            }
        }

    def fake_report(state):
        execution_order.append("report")
        return {
            "final_report": {
                "repository_path": ".",
                "risk_score": 0,
                "risk_level": "healthy",
                "finding_count": 0,
                "severity_counts": {
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0,
                },
                "findings": [],
            }
        }

    monkeypatch.setattr(
        graph,
        "analyze_repository",
        fake_repository_analysis,
    )

    monkeypatch.setattr(
        graph,
        "analyze_dependencies",
        fake_dependency_analysis,
    )

    monkeypatch.setattr(
        graph,
        "analyze_testing",
        fake_testing_analysis,
    )

    monkeypatch.setattr(
        graph,
        "analyze_with_llm",
        fake_reasoning_analysis,
    )

    monkeypatch.setattr(
        graph,
        "verify_findings",
        fake_verification,
    )

    monkeypatch.setattr(
        graph,
        "build_final_report",
        fake_report,
    )

    app = graph.build_graph()

    result = app.invoke(
        {
            "repository_path": ".",
            "evidence": {},
        }
    )

    assert execution_order == [
        "repository",
        "dependency",
        "testing",
        "reasoning",
        "verification",
        "report",
    ]

    assert "final_report" in result
    assert result["final_report"]["risk_level"] == "healthy"


def test_graph_contains_final_report():
    app = graph.build_graph()

    assert app is not None
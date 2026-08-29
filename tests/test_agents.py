from agents.graph import build_graph
from agents.report_agent import build_final_report
from agents.state import RepoLensState


def test_state_accepts_all_pipeline_fields():
    state: RepoLensState = {
        "repository_path": ".",
        "evidence": {},
        "repository_analysis": {},
        "dependency_analysis": {},
        "testing_analysis": {},
        "reasoning_analysis": {},
        "verification": {},
        "final_report": {},
    }

    assert state["repository_path"] == "."
    assert "final_report" in state


def test_graph_builds_successfully():
    graph = build_graph()

    assert graph is not None


def test_final_report_deduplicates_dependency_findings():
    state: RepoLensState = {
        "repository_path": ".",
        "verification": {
            "verified_findings": [
                {
                    "agent": "dependency_agent",
                    "category": "dependencies",
                    "severity": "medium",
                    "finding": "6 of 6 dependencies do not specify a version.",
                    "evidence": [
                        "langgraph",
                        "langchain",
                    ],
                    "recommendation": "",
                },
                {
                    "agent": "llm_reasoning_agent",
                    "category": "dependencies",
                    "severity": "high",
                    "finding": "Unpinned production dependencies risk breaking changes.",
                    "evidence": "All dependencies are unpinned.",
                    "recommendation": "Pin dependency versions.",
                },
            ]
        },
    }

    result = build_final_report(state)
    report = result["final_report"]

    assert report["finding_count"] == 1
    assert report["severity_counts"]["high"] == 1
    assert report["severity_counts"]["medium"] == 0


def test_final_report_calculates_risk_level():
    state: RepoLensState = {
        "repository_path": ".",
        "verification": {
            "verified_findings": [
                {
                    "agent": "test_agent",
                    "category": "testing",
                    "severity": "high",
                    "finding": "Missing agent tests.",
                    "evidence": "No agent tests found.",
                    "recommendation": "Add tests.",
                }
            ]
        },
    }

    result = build_final_report(state)
    report = result["final_report"]

    assert report["risk_score"] == 7
    assert report["risk_level"] == "medium"
    assert report["finding_count"] == 1


def test_final_report_handles_no_findings():
    state: RepoLensState = {
        "repository_path": ".",
        "verification": {
            "verified_findings": []
        },
    }

    result = build_final_report(state)
    report = result["final_report"]

    assert report["risk_score"] == 0
    assert report["risk_level"] == "healthy"
    assert report["finding_count"] == 0


def test_final_report_orders_findings_by_severity():
    state: RepoLensState = {
        "repository_path": ".",
        "verification": {
            "verified_findings": [
                {
                    "agent": "test",
                    "category": "documentation",
                    "severity": "low",
                    "finding": "Minor documentation issue.",
                },
                {
                    "agent": "test",
                    "category": "testing",
                    "severity": "high",
                    "finding": "Important testing issue.",
                },
                {
                    "agent": "test",
                    "category": "dependencies",
                    "severity": "medium",
                    "finding": "Dependency issue.",
                },
            ]
        },
    }

    result = build_final_report(state)
    findings = result["final_report"]["findings"]

    assert findings[0]["severity"] == "high"
    assert findings[1]["severity"] == "medium"
    assert findings[2]["severity"] == "low"
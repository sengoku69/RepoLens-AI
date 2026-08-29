RepoLens-AI

RepoLens-AI is a multi-agent repository evaluation system that analyzes a software repository, collects deterministic evidence, reasons over the evidence with an LLM, verifies the resulting findings, and produces a final risk report.

The system is designed to combine deterministic repository analysis with LLM-based reasoning while keeping the final findings grounded in collected evidence.

**Features**

- Repository structure analysis
- Programming language detection
- README and source-directory detection
- Dependency discovery and version analysis
- Automated test execution and test-health reporting
- LLM-based repository reasoning
- Finding verification
- Finding deduplication
- Risk scoring and severity classification
- Deterministic evaluation benchmark
- JSON-based machine-readable output
- Local CLI entry point
- Mock-based tests for agent components

**Architecture**

The main workflow follows this sequence:

Repository
↓
Evidence Collection
↓
Repository Agent
↓
Dependency Agent
↓
Testing Agent
↓
LLM Reasoning Agent
↓
Verification Agent
↓
Final Report

The deterministic tools collect observable repository evidence before the reasoning agent analyzes the repository.

The verification stage checks LLM-generated findings against the available evidence and rejects unsupported findings.

**Project Structure**

```text
RepoLens-AI/
├── agents/
│   ├── dependency_agent.py
│   ├── graph.py
│   ├── llm_provider.py
│   ├── reasoning_agent.py
│   ├── report_agent.py
│   ├── repository_agent.py
│   ├── state.py
│   ├── testing_agent.py
│   └── verification_agent.py
│
├── repolens/
│   ├── __init__.py
│   └── __main__.py
│
├── tools/
│   ├── baseline_analyzer.py
│   ├── dependency_collector.py
│   ├── evidence_collector.py
│   ├── repository_scanner.py
│   └── test_runner.py
│
├── tests/
│   ├── test_agents.py
│   ├── test_dependency_collector.py
│   ├── test_evidence_collector.py
│   ├── test_graph.py
│   ├── test_llm_provider.py
│   ├── test_repository_scanner.py
│   └── test_test_runner.py
│
├── evaluation/
│   ├── cases/
│   ├── baseline.md
│   ├── baseline_results.json
│   └── run_baseline.py
│
├── README.md
├── requirements.txt
└── .gitignore
RepoLens-AI
===========

An evidence-first multi-agent AI system for repository quality and risk analysis.

RepoLens-AI analyzes a software repository and produces a structured risk report. It combines deterministic repository inspection with LLM-based reasoning and an evidence verification stage.

The main goal is simple:

> Let deterministic tools collect the facts first, then let AI reason about those facts, and finally verify the AI's findings before producing the final report.

This approach helps reduce unsupported or purely speculative findings from an LLM.


Project Overview
----------------

Software repositories contain many different signals about their quality.

For example:

- Does the repository contain a README?
- What programming languages are being used?
- Are dependencies defined?
- Are dependency versions pinned?
- Does the project have tests?
- Do the tests pass?
- How is the project organized?
- Are important parts of the application covered by tests?
- Are there architectural or maintainability concerns?

A traditional rule-based scanner can answer many of these questions, but it can have difficulty understanding higher-level architectural or maintainability issues.

An LLM can reason about these higher-level issues, but an LLM should not be trusted to invent repository facts.

RepoLens-AI combines both approaches.

The system first collects observable evidence from the repository. That evidence is then provided to an LLM reasoning agent. The resulting findings are passed through a verification stage before they are included in the final report.


Core Idea
---------

The system follows an evidence-first design:

```text
Repository
     |
     v
Deterministic Evidence Collection
     |
     +-------------------+
     |                   |
     v                   v
Repository Analysis   Dependency Analysis
     |                   |
     +---------+---------+
               |
               v
        Testing Analysis
               |
               v
       LLM Reasoning Agent
               |
               v
       Verification Agent
               |
               v
          Final Report
```

The important distinction is:

```text
Deterministic tools
        |
        | collect facts
        v
Structured evidence
        |
        | provide context
        v
LLM reasoning
        |
        | propose findings
        v
Evidence verification
        |
        | accept or reject findings
        v
Final risk report
```

This creates a clear separation between facts and reasoning.


Why RepoLens-AI?
---------------

A repository analysis system should not depend entirely on an LLM.

For example, an LLM should not need to guess whether a project contains tests. A deterministic test runner can check that directly.

Similarly, the system can directly inspect:

- Files
- Directories
- README files
- Dependency files
- Dependency versions
- Programming languages
- Test execution results

The LLM is then used for the parts where reasoning is more useful.

For example, based on the collected evidence, the LLM may identify:

- Architectural concerns
- Maintainability issues
- Missing test coverage
- Dependency-management risks
- Organization problems

The verification stage then checks whether those findings are actually supported by the repository evidence.


Main Features
-------------

Repository Analysis

RepoLens-AI scans a repository and collects structural information.

It can detect:

- Total file count
- Programming languages
- Source directories
- Test directories
- README files
- Dependency files
- Configuration files
- Representative repository files

This information becomes the foundation for the rest of the analysis.


Programming Language Detection

The repository scanner recognizes multiple common programming languages based on source-file extensions.

The current scanner includes support for languages such as:

- Python
- JavaScript
- TypeScript
- Java
- Go
- Rust
- C
- C++
- C#
- PHP
- Ruby
- Swift
- Kotlin

The scanner records the number of detected files for each language.


Dependency Analysis

The dependency agent analyzes supported dependency files and extracts dependency information.

For Python requirements files, the system can identify:

- Package name
- Version
- Version operator
- Source file
- Line number

For example:

```text
langgraph==1.2.11
langchain==1.3.18
pydantic==2.13.5
```

The system can distinguish between pinned and unpinned dependencies.

This allows the analysis pipeline to identify dependency-management risks without asking the LLM to manually inspect the dependency file.


Automated Test Analysis

The testing agent detects supported test frameworks and executes the repository's tests.

The test evidence can include:

- Test framework
- Test command
- Test target
- Test status
- Exit code
- Number of collected tests
- Number of passing tests
- Number of failing tests
- Number of test errors
- Number of skipped tests

For example, the current RepoLens-AI test suite produces:

```text
39 passed
```

This information is collected deterministically and passed into the analysis pipeline.


LLM-Based Repository Reasoning

After deterministic evidence has been collected, the reasoning agent uses an LLM to analyze the repository.

The LLM does not need to independently discover basic repository facts.

Instead, it receives structured evidence and is asked to reason about possible risks.

A finding can include:

- Category
- Severity
- Finding description
- Evidence
- Recommendation

Example categories include:

- Dependencies
- Testing
- Architecture
- Maintainability
- Documentation


Finding Verification

The verification agent is an important part of the system.

LLMs can produce reasonable-sounding findings that are not actually supported by the repository.

RepoLens-AI therefore introduces a verification stage after LLM reasoning.

The verification agent checks generated findings against the collected evidence.

Findings that are supported can continue to the final report.

Findings that cannot be supported can be rejected.

The result contains:

```text
Verified findings
Rejected findings
Finding count
Rejected count
Severity counts
```

This gives the pipeline an additional layer of protection against unsupported AI conclusions.


Risk Scoring
------------

The final report includes a risk score and risk level.

The report can contain severity counts such as:

```text
Critical
High
Medium
Low
```

For example:

```json
{
  "risk_score": 4,
  "risk_level": "low",
  "finding_count": 1,
  "severity_counts": {
    "critical": 0,
    "high": 0,
    "medium": 1,
    "low": 0
  }
}
```

The score provides a compact way to understand the overall result while the individual findings provide the detailed explanation.


Multi-Agent Architecture
------------------------

RepoLens-AI uses separate agents for different responsibilities.

This makes the system easier to understand, test, and extend.


Repository Agent

The repository agent focuses on repository structure.

Its responsibilities include:

- Understanding repository layout
- Reviewing file and directory evidence
- Identifying structural characteristics
- Producing repository-level findings


Dependency Agent

The dependency agent focuses on dependency information.

Its responsibilities include:

- Discovering dependency files
- Extracting dependencies
- Checking version specifications
- Identifying dependency-management concerns


Testing Agent

The testing agent focuses on test health.

Its responsibilities include:

- Detecting supported test frameworks
- Running tests
- Collecting test results
- Reporting failures and errors
- Determining overall test health


LLM Reasoning Agent

The reasoning agent receives the evidence collected by the deterministic agents and reasons over it.

Its responsibilities include:

- Reviewing repository evidence
- Identifying possible risks
- Assigning severity
- Explaining why a finding matters
- Providing recommendations


Verification Agent

The verification agent reviews findings produced by the reasoning stage.

Its responsibilities include:

- Checking evidence support
- Rejecting unsupported findings
- Preserving supported findings
- Producing verified findings


Report Agent

The report agent produces the final structured result.

The final report combines the verified findings into a machine-readable format containing information such as:

- Repository path
- Risk score
- Risk level
- Finding count
- Severity counts
- Individual findings


LLM Provider

The LLM provider provides a common interface for communicating with an OpenAI-compatible API.

The current development setup has been tested with Gemini through its OpenAI-compatible endpoint.

The provider abstraction keeps LLM configuration separate from the reasoning logic.

The provider can expose:

```text
Provider
Base URL
Model
```

This makes it easier to change the underlying model configuration without changing the rest of the analysis pipeline.


End-to-End Workflow
-------------------

A complete RepoLens-AI analysis follows this general sequence:

```text
Step 1
Repository is provided
        |
        v
Step 2
Repository scanner inspects files and directories
        |
        v
Step 3
Dependency collector analyzes dependency files
        |
        v
Step 4
Test runner executes the repository test suite
        |
        v
Step 5
Evidence collector combines the collected information
        |
        v
Step 6
Repository, dependency, and testing agents analyze the evidence
        |
        v
Step 7
LLM reasoning agent identifies higher-level risks
        |
        v
Step 8
Verification agent checks the generated findings
        |
        v
Step 9
Report agent produces the final report
```

The architecture therefore separates the workflow into three major phases:

```text
Evidence Collection
        |
        v
Reasoning
        |
        v
Verification and Reporting
```


Evidence Collection
-------------------

The deterministic evidence layer is implemented through tools under the `tools/` directory.

The main tools are:

```text
tools/
|
├── repository_scanner.py
├── dependency_collector.py
├── test_runner.py
├── evidence_collector.py
└── baseline_analyzer.py
```

`repository_scanner.py`

Scans the repository and collects structural evidence.

`dependency_collector.py`

Discovers dependency files and extracts dependency information.

`test_runner.py`

Detects supported test frameworks and executes tests.

`evidence_collector.py`

Combines repository, dependency, and testing evidence into a single structured representation.

`baseline_analyzer.py`

Provides deterministic scoring for the evaluation benchmark.


AI Analysis Layer
-----------------

The AI analysis components are located under `agents/`.

```text
agents/
|
├── dependency_agent.py
├── graph.py
├── llm_provider.py
├── reasoning_agent.py
├── report_agent.py
├── repository_agent.py
├── state.py
├── testing_agent.py
└── verification_agent.py
```

The `graph.py` module connects the different stages of the workflow.

The `state.py` module provides the shared state used while information moves through the agent pipeline.

This allows the different agents to work as parts of one analysis workflow rather than as unrelated scripts.


Evaluation System
-----------------

RepoLens-AI includes a deterministic evaluation benchmark.

The benchmark contains 10 repository cases designed to represent different repository conditions.

The current cases include:

```text
case_01_good_project
case_02_no_readme
case_03_no_tests
case_04_no_dependencies
case_05_failing_tests
case_06_many_dependencies
case_07_empty_source
case_08_multiple_modules
case_09_documented_project
case_10_mixed_quality
```

These cases allow the deterministic analyzer to be tested against known repository conditions.

The evaluation system checks whether the analyzer:

- Handles valid repositories
- Detects missing README files
- Detects missing tests
- Detects missing dependencies
- Detects failing tests
- Handles repositories with many dependencies
- Handles empty source situations
- Handles multiple modules
- Handles documented projects
- Handles mixed-quality repositories


Current Evaluation Result
-------------------------

The latest deterministic benchmark completed successfully:

```text
Evaluation: deterministic_baseline

Cases:              10
Successful cases:   10
Average score:      90.0
```

The individual benchmark scores are:

```text
case_01_good_project        100
case_02_no_readme            90
case_03_no_tests             60
case_04_no_dependencies     80
case_05_failing_tests       80
case_06_many_dependencies   100
case_07_empty_source        100
case_08_multiple_modules    100
case_09_documented_project  100
case_10_mixed_quality        90
```

The benchmark is designed as a repeatable baseline rather than as a claim that every repository should receive a particular score.


Testing and Validation
----------------------

The project currently has automated tests covering the deterministic tools and important agent components.

The latest test run produced:

```text
39 passed
```

The test suite currently covers areas including:

- Agent behavior
- Graph execution
- LLM provider handling
- Dependency collection
- Evidence collection
- Repository scanning
- Test execution

Run the test suite with:

```powershell
python -m pytest tests/
```

A successful run should report all tests passing.


Example Analysis
----------------

A final RepoLens-AI report can look like this:

```json
{
  "repository_path": ".",
  "risk_score": 4,
  "risk_level": "low",
  "finding_count": 1,
  "severity_counts": {
    "critical": 0,
    "high": 0,
    "medium": 1,
    "low": 0
  },
  "findings": [
    {
      "agent": "llm_reasoning_agent",
      "category": "architecture",
      "severity": "medium",
      "finding": "Core application modules are located at the repository root rather than encapsulated inside the primary package module.",
      "evidence": "Source directories show agents and tools at the top level alongside repolens.",
      "recommendation": "Refactor the module layout to place agents and tools inside the primary package structure."
    }
  ]
}
```

The exact findings depend on the repository being analyzed.


Project Structure
-----------------

```text
RepoLens-AI/
|
├── agents/
|   ├── __init__.py
|   ├── dependency_agent.py
|   ├── graph.py
|   ├── llm_provider.py
|   ├── reasoning_agent.py
|   ├── report_agent.py
|   ├── repository_agent.py
|   ├── state.py
|   ├── testing_agent.py
|   └── verification_agent.py
|
├── repolens/
|   ├── __init__.py
|   └── __main__.py
|
├── tools/
|   ├── __init__.py
|   ├── baseline_analyzer.py
|   ├── dependency_collector.py
|   ├── evidence_collector.py
|   ├── repository_scanner.py
|   └── test_runner.py
|
├── tests/
|   ├── test_agents.py
|   ├── test_dependency_collector.py
|   ├── test_evidence_collector.py
|   ├── test_graph.py
|   ├── test_llm_provider.py
|   ├── test_repository_scanner.py
|   └── test_test_runner.py
|
├── evaluation/
|   ├── cases/
|   ├── baseline.md
|   ├── baseline_results.json
|   ├── generate_cases.py
|   └── run_baseline.py
|
├── README.md
├── requirements.txt
└── .gitignore
```


Technology Stack
----------------

The project currently uses:

- Python
- LangGraph
- LangChain
- LangChain OpenAI integration
- OpenAI-compatible APIs
- Gemini
- Pydantic
- pytest
- python-dotenv


Configuration
-------------

RepoLens-AI uses environment variables for LLM configuration.

Example:

```text
LLM_PROVIDER=gemini
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_MODEL=gemini-3.6-flash
```

API keys and other secrets should never be committed to Git.

The project `.gitignore` is configured to ignore `.env` files and virtual-environment files.


Installation
------------

Create a Python virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install project dependencies:

```powershell
pip install -r requirements.txt
```


Running the Tests
-----------------

Run:

```powershell
python -m pytest tests/
```

The current project validation result is:

```text
39 passed
```


Running the Deterministic Evaluation
------------------------------------

Run:

```powershell
python evaluation/run_baseline.py
```

The evaluation runner executes all 10 benchmark repositories and produces a JSON result.

The results are saved to:

```text
evaluation/baseline_results.json
```


Running RepoLens-AI
------------------

The project includes a Python module entry point.

Run:

```powershell
python -m repolens
```

The exact behavior of the CLI depends on the current implementation and configured LLM provider.


Design Principles
-----------------

Evidence Before Reasoning

The system collects repository facts before asking the LLM to reason about the repository.

This reduces the amount of information the LLM needs to discover by itself.

Separation of Responsibilities

Different components handle different responsibilities.

Repository scanning, dependency analysis, testing, reasoning, verification, and reporting are separated into different modules and agents.

Verification Before Reporting

LLM-generated findings are not automatically treated as final findings.

They pass through a verification stage before reaching the final report.

Machine-Readable Output

The analysis pipeline produces structured JSON that can be used by other applications or automation systems.

Repeatable Evaluation

The deterministic benchmark provides a stable set of repository cases for measuring changes to the analysis system.


Current Project Status
----------------------

RepoLens-AI currently provides:

- Deterministic repository scanning
- Programming language detection
- Dependency discovery
- Dependency version analysis
- Automated test execution
- Test-health reporting
- Multi-agent repository analysis
- LLM-based reasoning
- Evidence-based finding verification
- Risk scoring
- Structured JSON reports
- Deterministic evaluation benchmarks
- Automated test coverage for core components

Current validation:

```text
Automated tests:       39 passed
Evaluation cases:      10/10 successful
Deterministic average: 90.0
```


Known Improvement Area
----------------------

The current project still has an architectural improvement opportunity.

The main application logic is currently split between root-level `agents/` and `tools/` directories and the `repolens/` package.

A future packaging improvement could consolidate these modules under a single primary package namespace.

For example:

```text
repolens/
|
├── agents/
├── tools/
└── ...
```

This would make the package structure more consistent for distribution and long-term maintenance.

This is intentionally documented as an improvement area rather than hidden from the project description.


Future Improvements
-------------------

Possible future improvements include:

- More comprehensive agent integration tests
- Additional repository analysis rules
- More programming language support
- Dependency vulnerability analysis
- More advanced risk scoring
- Additional evaluation cases
- Continuous integration
- Automated benchmark execution in CI
- More LLM provider options
- Improved packaging and distribution
- Better CLI configuration
- More detailed repository reports
- Historical comparison between repository scans


Project Goal
------------

RepoLens-AI is being developed as an example of how deterministic software analysis and LLM reasoning can work together.

The project does not try to replace deterministic tooling with an LLM.

Instead, it gives each approach the responsibility it handles best:

```text
Deterministic tools
    -> collect facts

LLM reasoning
    -> understand and interpret the facts

Verification
    -> check whether conclusions are supported

Final report
    -> present actionable results
```

This evidence-first architecture is the central design idea behind RepoLens-AI.
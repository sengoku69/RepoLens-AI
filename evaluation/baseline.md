# RepoLens AI — Baseline

## Baseline Version

Baseline v0 — Single-Prompt Repository Review

## Purpose

The baseline represents a simple and reasonable approach to evaluating
an unfamiliar software repository using a general-purpose AI model.

## Workflow

1. Collect the repository files and relevant project information.
2. Provide the repository context to a single general-purpose AI prompt.
3. Ask the model to assess the repository.
4. Generate a structured codebase quality report.

## Baseline Does Not Use

- Multiple specialized agents
- Agent-to-agent orchestration
- Verification agents
- Persistent agent memory
- Specialized analysis tools
- Evidence verification workflows

## Evaluation Dimensions

The baseline evaluates:

1. Code Quality
2. Architecture
3. Testing
4. Dependencies
5. Reliability

## Primary Metric

### Finding Accuracy

The percentage of important findings produced by the system that are
judged correct by the evaluation rubric.

## Secondary Metrics

- Evidence Coverage
- False Positive Rate
- Human Time per Repository
- Cost per Repository

## Evaluation Dataset

The final evaluation will use the same fixed repository cases for both
the baseline and the final RepoLens system.

The target is 10 or more repositories when practical, including at least
one challenging case.

## Fair Comparison

The baseline and final system will receive the same evaluation cases
and will be assessed using the same evaluation rubric.

No final-system-specific information will be added to the baseline
evaluation cases.

## Status

Baseline specification only.

No evaluation results have been collected yet.
# RepoLens AI — Evaluation Rubric

## Purpose

This rubric defines how repository-analysis findings will be evaluated.

The same rubric must be applied to the baseline and the final RepoLens
system.

---

## Finding Evaluation

Each reported finding receives a score from 0 to 2.

### Score 2 — Correct and Supported

The issue exists in the repository and the system provides sufficient
evidence to verify the finding.

Examples:

- A failing test is supported by actual test output.
- A dependency issue is supported by the repository's dependency data.
- A code-quality issue is supported by a specific file and relevant
  code section.

### Score 1 — Partially Correct

The finding identifies a real or plausible concern but has incomplete,
weak, or partially inaccurate evidence.

### Score 0 — Incorrect or Unsupported

The finding is not supported by the repository evidence, is factually
incorrect, or is based only on speculation.

---

## Severity

Each finding may also be classified as:

- Critical
- High
- Medium
- Low

Severity describes the potential impact of the issue. It does not
determine whether the finding itself is correct.

---

## Evidence Requirements

A strong finding should provide one or more forms of evidence:

- File path
- Relevant code section
- Line reference when available
- Test output
- Build output
- Dependency information
- Configuration evidence

Claims that cannot be traced back to repository evidence should not
receive the highest accuracy score.

---

# Primary Metric

## Finding Accuracy

Finding Accuracy measures the proportion of evaluated findings that are
correct.

Formula:

Correct Findings / Total Evaluated Findings

A finding is considered correct when it accurately identifies a real
repository issue and provides sufficient supporting evidence.

---

# Secondary Metrics

## False Positive Rate

Incorrect Findings / Total Findings

A lower false-positive rate is better.

## Evidence Coverage

Findings with Verifiable Evidence / Total Findings

A higher evidence coverage is better.

## Human Time Per Repository

The amount of human time required to complete the repository assessment.

## Cost Per Repository

The approximate computational/API cost required to produce one
repository assessment.

---

# Evaluation Dimensions

The systems will evaluate five dimensions:

1. Code Quality
2. Architecture
3. Testing
4. Dependencies
5. Reliability

---

## Code Quality

Evaluate:

- Readability
- Maintainability
- Complexity
- Duplication
- Error-prone implementation patterns

---

## Architecture

Evaluate:

- Project organization
- Separation of responsibilities
- Component structure
- Major architectural risks

---

## Testing

Evaluate:

- Presence of tests
- Test quality
- Test failures
- Important areas lacking tests

---

## Dependencies

Evaluate:

- Dependency organization
- Version information
- Obvious dependency risks
- Unnecessary or problematic dependencies when supported by evidence

---

## Reliability

Evaluate:

- Error handling
- Failure handling
- Runtime risks
- Configuration-related reliability concerns
- Other evidence-backed reliability issues

---

# Evaluation Procedure

1. Select a fixed set of repositories.
2. Run the baseline on every repository.
3. Run the final RepoLens system on the same repositories.
4. Apply this rubric to both outputs.
5. Record every finding, including incorrect findings.
6. Calculate the primary and secondary metrics.
7. Compare the baseline and final results.

The evaluation cases and scoring process should remain consistent between
the baseline and final system.

---

# Challenging Case

At least one evaluation repository should contain a difficult or
non-obvious issue.

The purpose is to determine whether the system can identify meaningful
problems rather than only obvious issues.

The result of the challenging case should be discussed separately in
the final report.

---

## Evaluation Status

Rubric defined before evaluation.

No performance results have been recorded yet.
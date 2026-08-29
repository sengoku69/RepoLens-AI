from __future__ import annotations

import json
from typing import Any

from agents.llm_provider import get_llm
from agents.state import RepoLensState


def _extract_json(text: str) -> dict[str, Any]:
    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

        if text.startswith("json"):
            text = text[4:].strip()

    try:
        result = json.loads(text)

        if isinstance(result, dict):
            return result

    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:
        try:
            result = json.loads(
                text[start : end + 1]
            )

            if isinstance(result, dict):
                return result

        except json.JSONDecodeError:
            pass

    raise ValueError(
        "LLM response did not contain valid JSON."
    )


def _build_prompt(evidence: dict[str, Any]) -> str:
    repository = evidence.get(
        "repository",
        {},
    )

    dependencies = evidence.get(
        "dependencies",
        {},
    )

    tests = evidence.get(
        "tests",
        {},
    )

    evidence_payload = {
        "repository": repository,
        "dependencies": dependencies,
        "tests": tests,
    }

    return f"""
Analyze the following repository evidence for RepoLens-AI.

Your goal is to identify meaningful software-engineering risks
that a simple deterministic repository scanner could miss.

Focus on:
- code quality
- architecture
- dependency risks
- testing weaknesses
- documentation weaknesses
- maintainability
- suspicious or incomplete project structure

Do not invent facts that are not supported by the evidence.

Every finding must include concrete evidence from the supplied
repository information.

Return ONLY valid JSON with this exact structure:

{{
  "summary": "short overall assessment",
  "findings": [
    {{
      "category": "code|architecture|dependencies|testing|documentation|maintainability",
      "severity": "low|medium|high|critical",
      "finding": "specific problem",
      "evidence": "specific evidence supporting the finding",
      "recommendation": "specific improvement"
    }}
  ]
}}

Repository evidence:

{json.dumps(evidence_payload, indent=2)}
""".strip()


def analyze_with_llm(
    state: RepoLensState,
) -> dict[str, Any]:
    evidence = state.get(
        "evidence",
        {},
    )

    llm = get_llm()

    prompt = _build_prompt(evidence)

    response = llm.generate(
        [
            {
                "role": "system",
                "content": (
                    "You are a senior software engineer "
                    "performing evidence-based repository analysis."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.1,
    )

    result = _extract_json(response)

    findings = result.get(
        "findings",
        [],
    )

    if not isinstance(findings, list):
        findings = []

    return {
        "reasoning_analysis": {
            "agent": "llm_reasoning_agent",
            "provider": llm.info(),
            "summary": result.get(
                "summary",
                "",
            ),
            "findings": findings,
        }
    }
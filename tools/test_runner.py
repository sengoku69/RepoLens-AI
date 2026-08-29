from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


def detect_test_framework(repository_path: Path) -> str | None:
    """
    Detect a supported Python test framework.
    """

    if (repository_path / "pytest.ini").exists():
        return "pytest"

    pyproject_path = repository_path / "pyproject.toml"

    if pyproject_path.exists():
        pyproject = pyproject_path.read_text(
            encoding="utf-8"
        )

        if "pytest" in pyproject.lower():
            return "pytest"

    requirements_path = repository_path / "requirements.txt"

    if requirements_path.exists():
        requirements = requirements_path.read_text(
            encoding="utf-8"
        )

        if re.search(
            r"^\s*pytest(?:[<>=!~].*)?$",
            requirements,
            re.MULTILINE,
        ):
            return "pytest"

    if (repository_path / "tests").is_dir():
        return "pytest"

    return None


def determine_test_target(repository_path: Path) -> str:
    """
    Determine the safest conventional test target.

    Prefer the repository's dedicated tests/ directory.
    """

    tests_directory = repository_path / "tests"

    if tests_directory.is_dir():
        return "tests"

    return "."


def parse_pytest_output(output: str) -> dict:
    """
    Extract basic test statistics from pytest output.
    """

    result = {
        "tests_collected": None,
        "tests_passed": 0,
        "tests_failed": 0,
        "tests_skipped": 0,
        "tests_errors": 0,
    }

    collected_match = re.search(
        r"collected\s+(\d+)\s+items?",
        output,
        re.IGNORECASE,
    )

    if collected_match:
        result["tests_collected"] = int(
            collected_match.group(1)
        )

    passed_match = re.search(
        r"(\d+)\s+passed",
        output,
        re.IGNORECASE,
    )

    if passed_match:
        result["tests_passed"] = int(
            passed_match.group(1)
        )

    failed_match = re.search(
        r"(\d+)\s+failed",
        output,
        re.IGNORECASE,
    )

    if failed_match:
        result["tests_failed"] = int(
            failed_match.group(1)
        )

    skipped_match = re.search(
        r"(\d+)\s+skipped",
        output,
        re.IGNORECASE,
    )

    if skipped_match:
        result["tests_skipped"] = int(
            skipped_match.group(1)
        )

    error_match = re.search(
        r"(\d+)\s+errors?",
        output,
        re.IGNORECASE,
    )

    if error_match:
        result["tests_errors"] = int(
            error_match.group(1)
        )

    return result


def run_pytest(
    repository_path: Path,
    test_target: str,
) -> dict:
    """
    Run pytest against the selected test target.

    Uses the current Python interpreter so that the active
    virtual environment is respected.
    """

    command = [
        sys.executable,
        "-m",
        "pytest",
        test_target,
    ]

    try:
        completed = subprocess.run(
            command,
            cwd=repository_path,
            capture_output=True,
            text=True,
            timeout=120,
        )

        output = (
            completed.stdout
            + "\n"
            + completed.stderr
        ).strip()

        statistics = parse_pytest_output(output)

        if completed.returncode == 0:
            status = "passed"
        elif statistics["tests_errors"] > 0:
            status = "error"
        else:
            status = "failed"

        return {
            "test_framework": "pytest",
            "command": (
                f"python -m pytest {test_target}"
            ),
            "test_target": test_target,
            "status": status,
            "exit_code": completed.returncode,
            **statistics,
            "output": output[-5000:],
        }

    except subprocess.TimeoutExpired:
        return {
            "test_framework": "pytest",
            "command": (
                f"python -m pytest {test_target}"
            ),
            "test_target": test_target,
            "status": "timeout",
            "exit_code": None,
            "tests_collected": None,
            "tests_passed": 0,
            "tests_failed": 0,
            "tests_skipped": 0,
            "tests_errors": 0,
            "output": (
                "Test execution exceeded "
                "120 seconds."
            ),
        }


def collect_test_evidence(repository_path: str) -> dict:
    root = Path(repository_path).resolve()

    if not root.exists():
        raise FileNotFoundError(
            f"Repository does not exist: {root}"
        )

    if not root.is_dir():
        raise NotADirectoryError(
            f"Path is not a directory: {root}"
        )

    framework = detect_test_framework(root)

    if framework is None:
        return {
            "repository_path": str(root),
            "test_framework": None,
            "status": "not_detected",
            "message": (
                "No supported test framework detected."
            ),
        }

    if framework == "pytest":
        test_target = determine_test_target(root)

        result = run_pytest(
            root,
            test_target,
        )

        result["repository_path"] = str(root)

        return result

    return {
        "repository_path": str(root),
        "test_framework": framework,
        "status": "unsupported",
    }


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Usage: python tools/test_runner.py "
            "<repository_path>"
        )
        sys.exit(1)

    repository_path = sys.argv[1]

    try:
        result = collect_test_evidence(
            repository_path
        )

        print(
            json.dumps(
                result,
                indent=2,
            )
        )

    except (
        FileNotFoundError,
        NotADirectoryError,
    ) as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
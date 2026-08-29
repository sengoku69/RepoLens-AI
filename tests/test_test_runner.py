from pathlib import Path

from tools.test_runner import (
    detect_test_framework,
    determine_test_target,
    parse_pytest_output,
)


def test_detect_pytest_from_requirements(tmp_path: Path):
    requirements = tmp_path / "requirements.txt"

    requirements.write_text(
        "pytest\nrequests\n",
        encoding="utf-8",
    )

    assert detect_test_framework(tmp_path) == "pytest"


def test_detect_pytest_from_tests_directory(tmp_path: Path):
    tests_directory = tmp_path / "tests"
    tests_directory.mkdir()

    assert detect_test_framework(tmp_path) == "pytest"


def test_detect_no_framework(tmp_path: Path):
    assert detect_test_framework(tmp_path) is None


def test_determine_tests_directory(tmp_path: Path):
    tests_directory = tmp_path / "tests"
    tests_directory.mkdir()

    assert determine_test_target(tmp_path) == "tests"


def test_determine_repository_when_no_tests_directory(
    tmp_path: Path,
):
    assert determine_test_target(tmp_path) == "."


def test_parse_successful_pytest_output():
    output = """
    ============================= test session starts =============================
    collected 12 items

    tests/test_example.py ............

    ============================= 12 passed in 0.07s ==============================
    """

    result = parse_pytest_output(output)

    assert result["tests_collected"] == 12
    assert result["tests_passed"] == 12
    assert result["tests_failed"] == 0
    assert result["tests_skipped"] == 0
    assert result["tests_errors"] == 0


def test_parse_failed_pytest_output():
    output = """
    ============================= test session starts =============================
    collected 10 items

    tests/test_example.py ....F..F..

    ==================== 2 failed, 8 passed in 0.10s =============================
    """

    result = parse_pytest_output(output)

    assert result["tests_collected"] == 10
    assert result["tests_passed"] == 8
    assert result["tests_failed"] == 2


def test_parse_skipped_pytest_output():
    output = """
    collected 5 items

    ==================== 4 passed, 1 skipped in 0.05s =============================
    """

    result = parse_pytest_output(output)

    assert result["tests_passed"] == 4
    assert result["tests_skipped"] == 1
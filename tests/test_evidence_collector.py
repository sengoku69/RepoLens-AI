from pathlib import Path

from tools.evidence_collector import collect_repository_evidence


def create_sample_repository(tmp_path: Path) -> Path:
    repository = tmp_path / "sample_repo"

    (repository / "src").mkdir(parents=True)
    (repository / "tests").mkdir()

    (repository / "src" / "main.py").write_text(
        "print('hello')",
        encoding="utf-8",
    )

    (repository / "tests" / "test_main.py").write_text(
        "def test_example():\n    assert True\n",
        encoding="utf-8",
    )

    (repository / "README.md").write_text(
        "# Sample Repository",
        encoding="utf-8",
    )

    (repository / "requirements.txt").write_text(
        "requests==2.31.0\n",
        encoding="utf-8",
    )

    return repository


def test_collect_repository_evidence_structure(
    tmp_path: Path,
):
    repository = create_sample_repository(tmp_path)

    result = collect_repository_evidence(
        str(repository)
    )

    assert "repository" in result
    assert "dependencies" in result
    assert "tests" in result


def test_collect_repository_evidence_dependencies(
    tmp_path: Path,
):
    repository = create_sample_repository(tmp_path)

    result = collect_repository_evidence(
        str(repository)
    )

    assert result["dependencies"]["dependency_count"] == 1

    assert (
        result["dependencies"]["items"][0]["name"]
        == "requests"
    )


def test_collect_repository_evidence_repository_details(
    tmp_path: Path,
):
    repository = create_sample_repository(tmp_path)

    result = collect_repository_evidence(
        str(repository)
    )

    repository_data = result["repository"]

    assert repository_data["file_count"] == 4

    assert repository_data["languages"] == {
        "Python": 2
    }

    assert repository_data["readme_present"] is True

    assert "tests" in repository_data[
        "test_directories"
    ]


def test_collect_repository_evidence_runs_tests(
    tmp_path: Path,
):
    repository = create_sample_repository(tmp_path)

    result = collect_repository_evidence(
        str(repository)
    )

    test_data = result["tests"]

    assert test_data["test_framework"] == "pytest"
    assert test_data["status"] == "passed"
    assert test_data["exit_code"] == 0
    assert test_data["tests_passed"] == 1
    assert test_data["tests_failed"] == 0


def test_collect_repository_evidence_rejects_missing_repository(
    tmp_path: Path,
):
    missing_repository = tmp_path / "does_not_exist"

    try:
        collect_repository_evidence(
            str(missing_repository)
        )
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass
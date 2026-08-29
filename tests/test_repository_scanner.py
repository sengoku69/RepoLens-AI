from pathlib import Path

from tools.repository_scanner import scan_repository


def create_test_repository(tmp_path: Path) -> Path:
    repository = tmp_path / "sample_repo"

    (repository / "src").mkdir(parents=True)
    (repository / "tests").mkdir()
    (repository / ".venv").mkdir()
    (repository / ".git").mkdir()

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
        "requests==2.0.0\n",
        encoding="utf-8",
    )

    (repository / ".env").write_text(
        "SECRET_KEY=do-not-expose",
        encoding="utf-8",
    )

    (repository / ".venv" / "hidden.py").write_text(
        "print('should be ignored')",
        encoding="utf-8",
    )

    (repository / ".git" / "config").write_text(
        "git data",
        encoding="utf-8",
    )

    return repository


def test_scanner_detects_python_files(tmp_path):
    repository = create_test_repository(tmp_path)

    result = scan_repository(str(repository))

    assert result["languages"]["Python"] == 2


def test_scanner_detects_test_directory(tmp_path):
    repository = create_test_repository(tmp_path)

    result = scan_repository(str(repository))

    assert "tests" in result["test_directories"]


def test_scanner_detects_dependency_files(tmp_path):
    repository = create_test_repository(tmp_path)

    result = scan_repository(str(repository))

    assert "requirements.txt" in result["dependency_files"]


def test_scanner_detects_readme(tmp_path):
    repository = create_test_repository(tmp_path)

    result = scan_repository(str(repository))

    assert result["readme_present"] is True
    assert "README.md" in result["readme_files"]


def test_scanner_excludes_env_file(tmp_path):
    repository = create_test_repository(tmp_path)

    result = scan_repository(str(repository))

    assert ".env" not in result["files_sample"]


def test_scanner_excludes_virtual_environment(tmp_path):
    repository = create_test_repository(tmp_path)

    result = scan_repository(str(repository))

    assert ".venv/hidden.py" not in result["files_sample"]


def test_scanner_excludes_git_directory(tmp_path):
    repository = create_test_repository(tmp_path)

    result = scan_repository(str(repository))

    assert ".git/config" not in result["files_sample"]
from pathlib import Path

from tools.dependency_collector import (
    collect_dependencies,
    parse_package_json,
    parse_requirements_file,
)


def test_parse_requirements_file(tmp_path: Path):
    requirements = tmp_path / "requirements.txt"

    requirements.write_text(
        """
# Comment
requests==2.31.0
flask>=2.0
pydantic
""".strip(),
        encoding="utf-8",
    )

    result = parse_requirements_file(requirements)

    assert len(result) == 3

    assert result[0]["name"] == "requests"
    assert result[0]["operator"] == "=="
    assert result[0]["version"] == "2.31.0"

    assert result[1]["name"] == "flask"
    assert result[1]["operator"] == ">="
    assert result[1]["version"] == "2.0"

    assert result[2]["name"] == "pydantic"
    assert result[2]["version"] is None


def test_parse_requirements_ignores_comments_and_blank_lines(
    tmp_path: Path,
):
    requirements = tmp_path / "requirements.txt"

    requirements.write_text(
        """
# This is a comment

requests==2.31.0

# Another comment
""".strip(),
        encoding="utf-8",
    )

    result = parse_requirements_file(requirements)

    assert len(result) == 1
    assert result[0]["name"] == "requests"


def test_parse_package_json(tmp_path: Path):
    package_json = tmp_path / "package.json"

    package_json.write_text(
        """
{
    "dependencies": {
        "react": "^18.2.0",
        "axios": "^1.6.0"
    },
    "devDependencies": {
        "vitest": "^1.0.0"
    }
}
""".strip(),
        encoding="utf-8",
    )

    result = parse_package_json(package_json)

    assert len(result) == 3

    names = {dependency["name"] for dependency in result}

    assert names == {"react", "axios", "vitest"}


def test_collect_dependencies(tmp_path: Path):
    repository = tmp_path / "sample_repo"
    repository.mkdir()

    (repository / "requirements.txt").write_text(
        """
requests==2.31.0
flask>=2.0
""".strip(),
        encoding="utf-8",
    )

    result = collect_dependencies(str(repository))

    assert result["dependency_files"] == ["requirements.txt"]
    assert result["dependency_count"] == 2

    names = {
        dependency["name"]
        for dependency in result["dependencies"]
    }

    assert names == {"requests", "flask"}


def test_collect_dependencies_with_no_dependency_files(
    tmp_path: Path,
):
    repository = tmp_path / "empty_repo"
    repository.mkdir()

    result = collect_dependencies(str(repository))

    assert result["dependency_files"] == []
    assert result["dependency_count"] == 0
    assert result["dependencies"] == []
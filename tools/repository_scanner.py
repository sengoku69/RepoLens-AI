from __future__ import annotations

import json
import sys
from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "node_modules",
    ".idea",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
}

IGNORED_FILES = {
    ".env",
    ".env.local",
    ".env.development",
    ".env.production",
    ".env.test",
}

SOURCE_EXTENSIONS = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
    ".cpp": "C++",
    ".cc": "C++",
    ".c": "C",
    ".cs": "C#",
    ".php": "PHP",
    ".rb": "Ruby",
    ".swift": "Swift",
    ".kt": "Kotlin",
}

DEPENDENCY_FILES = {
    "requirements.txt",
    "pyproject.toml",
    "poetry.lock",
    "Pipfile",
    "Pipfile.lock",
    "package.json",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "pom.xml",
    "build.gradle",
    "go.mod",
    "Cargo.toml",
    "Gemfile",
}

TEST_DIRECTORY_NAMES = {
    "test",
    "tests",
    "__tests__",
}

CONFIG_FILES = {
    ".env.example",
    "config.yaml",
    "config.yml",
    "config.json",
    "settings.py",
    "docker-compose.yml",
    "docker-compose.yaml",
    "Dockerfile",
    "Makefile",
}


def scan_repository(
    repository_path: str,
    exclude_evaluation: bool = False,
) -> dict:
    root = Path(repository_path).resolve()

    if not root.exists():
        raise FileNotFoundError(
            f"Repository does not exist: {root}"
        )

    if not root.is_dir():
        raise NotADirectoryError(
            f"Path is not a directory: {root}"
        )

    files = []
    languages = {}
    source_directories = set()
    test_directories = set()
    dependency_files = []
    config_files = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        relative_path = path.relative_to(root)
        relative_parts = relative_path.parts

        if any(
            part in IGNORED_DIRECTORIES
            for part in relative_parts
        ):
            continue

        if (
            exclude_evaluation
            and relative_parts
            and relative_parts[0].lower()
            == "evaluation"
        ):
            continue

        if (
            path.name in IGNORED_FILES
            or path.name.startswith(".env.")
        ):
            continue

        relative_string = relative_path.as_posix()

        files.append(relative_string)

        extension = path.suffix.lower()

        if extension in SOURCE_EXTENSIONS:
            language = SOURCE_EXTENSIONS[extension]

            languages[language] = (
                languages.get(language, 0) + 1
            )

            if len(relative_parts) > 1:
                source_directories.add(
                    relative_parts[0]
                )

        if any(
            directory.lower()
            in TEST_DIRECTORY_NAMES
            for directory in relative_parts[:-1]
        ):
            if len(relative_parts) > 1:
                test_directories.add(
                    relative_parts[0]
                )

        if path.name in DEPENDENCY_FILES:
            dependency_files.append(
                relative_string
            )

        if path.name in CONFIG_FILES:
            config_files.append(
                relative_string
            )

    readme_files = [
        file
        for file in files
        if Path(file).name.lower()
        in {
            "readme",
            "readme.md",
            "readme.txt",
        }
    ]

    return {
        "repository_path": str(root),
        "file_count": len(files),
        "languages": dict(
            sorted(languages.items())
        ),
        "source_directories": sorted(
            source_directories
        ),
        "test_directories": sorted(
            test_directories
        ),
        "dependency_files": sorted(
            dependency_files
        ),
        "configuration_files": sorted(
            config_files
        ),
        "readme_present": bool(
            readme_files
        ),
        "readme_files": sorted(
            readme_files
        ),
        "files_sample": sorted(files)[:50],
    }


def main() -> None:
    if len(sys.argv) not in {2, 3}:
        print(
            "Usage: python tools/repository_scanner.py "
            "<repository_path> [exclude_evaluation]"
        )
        sys.exit(1)

    repository_path = sys.argv[1]

    exclude_evaluation = False

    if len(sys.argv) == 3:
        exclude_evaluation = (
            sys.argv[2].lower()
            in {
                "true",
                "1",
                "yes",
            }
        )

    try:
        result = scan_repository(
            repository_path,
            exclude_evaluation=exclude_evaluation,
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
        print(
            f"Error: {error}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
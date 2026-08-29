from __future__ import annotations

import json
import sys
from pathlib import Path

from tools.dependency_collector import collect_dependencies
from tools.repository_scanner import scan_repository
from tools.test_runner import collect_test_evidence


def collect_repository_evidence(repository_path: str) -> dict:
    """
    Collect all currently supported evidence for a repository.

    Evidence sources:
    - Repository structure
    - Dependencies
    - Test execution
    """

    root = Path(repository_path).resolve()

    if not root.exists():
        raise FileNotFoundError(
            f"Repository does not exist: {root}"
        )

    if not root.is_dir():
        raise NotADirectoryError(
            f"Path is not a directory: {root}"
        )

    repository_evidence = scan_repository(str(root))
    dependency_evidence = collect_dependencies(str(root))
    test_evidence = collect_test_evidence(str(root))

    return {
        "repository": {
            "path": str(root),
            "file_count": repository_evidence["file_count"],
            "languages": repository_evidence["languages"],
            "source_directories": repository_evidence[
                "source_directories"
            ],
            "test_directories": repository_evidence[
                "test_directories"
            ],
            "readme_present": repository_evidence[
                "readme_present"
            ],
            "readme_files": repository_evidence[
                "readme_files"
            ],
            "files_sample": repository_evidence[
                "files_sample"
            ],
        },
        "dependencies": {
            "dependency_files": dependency_evidence[
                "dependency_files"
            ],
            "dependency_count": dependency_evidence[
                "dependency_count"
            ],
            "items": dependency_evidence[
                "dependencies"
            ],
        },
        "tests": test_evidence,
    }


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Usage: python tools/evidence_collector.py "
            "<repository_path>"
        )
        sys.exit(1)

    repository_path = sys.argv[1]

    try:
        evidence = collect_repository_evidence(
            repository_path
        )

        print(
            json.dumps(
                evidence,
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
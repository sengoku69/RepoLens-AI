from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIREMENTS_PATTERN = re.compile(
    r"^\s*([A-Za-z0-9_.-]+)\s*"
    r"(?:([<>=!~]{1,2})\s*([A-Za-z0-9_.+!*,-]+))?"
)


def parse_requirements_file(path: Path) -> list[dict]:
    dependencies = []

    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        line = raw_line.strip()

        # Ignore blank lines and comments.
        if not line or line.startswith("#"):
            continue

        # Ignore editable/local/path installs for now.
        if line.startswith(("-e", "--editable", ".", "/")):
            continue

        match = REQUIREMENTS_PATTERN.match(line)

        if not match:
            continue

        name, operator, version = match.groups()

        dependency = {
            "name": name,
            "version": version,
            "operator": operator,
            "source": path.name,
            "line": line_number,
        }

        dependencies.append(dependency)

    return dependencies


def parse_package_json(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))

    dependencies = []

    for section in ("dependencies", "devDependencies", "peerDependencies"):
        section_data = data.get(section, {})

        for name, version in section_data.items():
            dependencies.append(
                {
                    "name": name,
                    "version": version,
                    "operator": None,
                    "source": path.name,
                    "section": section,
                }
            )

    return dependencies


def parse_pyproject_toml(path: Path) -> list[dict]:
    """
    Lightweight parser for common PEP 621 dependency declarations.

    We intentionally avoid adding a TOML dependency here because Python
    3.10 does not include tomllib in the standard library.
    """

    text = path.read_text(encoding="utf-8")

    dependencies = []

    in_project_dependencies = False

    for line in text.splitlines():
        stripped = line.strip()

        if stripped.startswith("["):
            in_project_dependencies = stripped == "[project]"
            continue

        if not in_project_dependencies:
            continue

        if stripped.startswith("dependencies") and "=" in stripped:
            _, value = stripped.split("=", 1)

            quoted_dependencies = re.findall(
                r"""["']([^"']+)["']""",
                value,
            )

            for dependency in quoted_dependencies:
                match = REQUIREMENTS_PATTERN.match(dependency)

                if not match:
                    continue

                name, operator, version = match.groups()

                dependencies.append(
                    {
                        "name": name,
                        "version": version,
                        "operator": operator,
                        "source": path.name,
                    }
                )

    return dependencies


def collect_dependencies(repository_path: str) -> dict:
    root = Path(repository_path).resolve()

    if not root.exists():
        raise FileNotFoundError(f"Repository does not exist: {root}")

    if not root.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {root}")

    dependency_files = []
    dependencies = []

    requirements_path = root / "requirements.txt"

    if requirements_path.exists():
        dependency_files.append("requirements.txt")
        dependencies.extend(
            parse_requirements_file(requirements_path)
        )

    package_json_path = root / "package.json"

    if package_json_path.exists():
        dependency_files.append("package.json")
        dependencies.extend(
            parse_package_json(package_json_path)
        )

    pyproject_path = root / "pyproject.toml"

    if pyproject_path.exists():
        dependency_files.append("pyproject.toml")
        dependencies.extend(
            parse_pyproject_toml(pyproject_path)
        )

    return {
        "repository_path": str(root),
        "dependency_files": sorted(dependency_files),
        "dependency_count": len(dependencies),
        "dependencies": dependencies,
    }


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Usage: python tools/dependency_collector.py "
            "<repository_path>"
        )
        sys.exit(1)

    repository_path = sys.argv[1]

    try:
        result = collect_dependencies(repository_path)
        print(json.dumps(result, indent=2))
    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
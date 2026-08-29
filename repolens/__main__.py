from __future__ import annotations

import json
import sys

from agents.graph import run_repolens


def main() -> None:
    repository_path = sys.argv[1] if len(sys.argv) > 1 else "."

    try:
        result = run_repolens(repository_path)

        print(
            json.dumps(
                result,
                indent=2,
                default=str,
            )
        )

    except Exception as error:
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": str(error),
                },
                indent=2,
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
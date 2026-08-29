from pathlib import Path


ROOT = Path(__file__).parent / "cases"


CASES = {
    "case_01_good_project": {
        "requirements": "pytest\nrequests==2.32.0\n",
        "readme": "# Good Project\n\nA small well-tested Python project.\n",
        "source": "def add(a, b):\n    return a + b\n",
        "test": "from src.main import add\n\n\ndef test_add():\n    assert add(2, 3) == 5\n",
    },
    "case_02_no_readme": {
        "requirements": "pytest\n",
        "readme": None,
        "source": "def hello():\n    return 'hello'\n",
        "test": "from src.main import hello\n\n\ndef test_hello():\n    assert hello() == 'hello'\n",
    },
    "case_03_no_tests": {
        "requirements": "requests==2.32.0\n",
        "readme": "# Untested Project\n",
        "source": "def process(data):\n    return data.strip()\n",
        "test": None,
    },
    "case_04_no_dependencies": {
        "requirements": None,
        "readme": "# Minimal Project\n",
        "source": "def calculate(x):\n    return x * 2\n",
        "test": "from src.main import calculate\n\n\ndef test_calculate():\n    assert calculate(4) == 8\n",
    },
    "case_05_failing_tests": {
        "requirements": "pytest\n",
        "readme": "# Broken Tests\n",
        "source": "def multiply(a, b):\n    return a * b\n",
        "test": "from src.main import multiply\n\n\ndef test_multiply():\n    assert multiply(2, 3) == 7\n",
    },
    "case_06_many_dependencies": {
        "requirements": (
            "pytest\n"
            "requests\n"
            "flask\n"
            "django\n"
            "numpy\n"
            "pandas\n"
            "torch\n"
            "transformers\n"
            "langchain\n"
            "fastapi\n"
        ),
        "readme": "# Dependency Heavy Project\n",
        "source": "def run():\n    return True\n",
        "test": "def test_run():\n    assert True\n",
    },
    "case_07_empty_source": {
        "requirements": "pytest\n",
        "readme": "# Empty Source\n",
        "source": "",
        "test": "def test_basic():\n    assert True\n",
    },
    "case_08_multiple_modules": {
        "requirements": "pytest\nrequests\n",
        "readme": "# Multi Module Project\n",
        "source": (
            "def fetch():\n"
            "    return True\n\n"
            "def transform(value):\n"
            "    return value * 2\n"
        ),
        "test": (
            "def test_fetch():\n"
            "    assert True\n\n"
            "def test_transform():\n"
            "    assert 2 * 2 == 4\n"
        ),
    },
    "case_09_documented_project": {
        "requirements": "pytest\n",
        "readme": (
            "# Documented Project\n\n"
            "## Installation\n"
            "pip install -r requirements.txt\n\n"
            "## Testing\n"
            "python -m pytest tests\n"
        ),
        "source": "def greet(name):\n    return f'Hello {name}'\n",
        "test": (
            "def test_greet():\n"
            "    assert 'Hello' in 'Hello World'\n"
        ),
    },
    "case_10_mixed_quality": {
        "requirements": "pytest\nrequests\nflask\n",
        "readme": None,
        "source": (
            "def process(value):\n"
            "    return value\n"
        ),
        "test": (
            "def test_process():\n"
            "    assert True\n"
        ),
    },
}


def create_case(name: str, config: dict) -> None:
    case_root = ROOT / name

    src = case_root / "src"
    tests = case_root / "tests"

    src.mkdir(parents=True, exist_ok=True)

    (src / "main.py").write_text(
        config["source"],
        encoding="utf-8",
    )

    if config["test"] is not None:
        tests.mkdir(parents=True, exist_ok=True)

        (tests / "test_main.py").write_text(
            config["test"],
            encoding="utf-8",
        )

    if config["readme"] is not None:
        (case_root / "README.md").write_text(
            config["readme"],
            encoding="utf-8",
        )

    if config["requirements"] is not None:
        (case_root / "requirements.txt").write_text(
            config["requirements"],
            encoding="utf-8",
        )


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)

    for name, config in CASES.items():
        create_case(name, config)

    print(f"Created {len(CASES)} evaluation cases.")
    print(f"Location: {ROOT.resolve()}")


if __name__ == "__main__":
    main()
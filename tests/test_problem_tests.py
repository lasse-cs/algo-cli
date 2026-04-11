from pathlib import Path

import pytest

from algo_cli.pytest_runner import run_pytest

PROBLEMS_ROOT = Path("src/algo_cli/problems")


def all_problem_dirs() -> list[Path]:
    return sorted(path for path in PROBLEMS_ROOT.iterdir() if path.is_dir())


@pytest.mark.parametrize("problem_dir", all_problem_dirs(), ids=lambda path: path.name)
def test_problem_tests_run_successfully(problem_dir: Path):
    result = run_pytest(cwd=problem_dir, test_target="tests.py")
    assert result.success

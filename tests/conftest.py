from pathlib import Path
import time_machine

import pytest

from typer.testing import CliRunner

from algo_cli.attempt_repository import AttemptRepository
from algo_cli.models import Problem, ProblemDirectory
from algo_cli.problem_repository import ProblemRepository

time_machine.naive_mode = time_machine.NaiveMode.LOCAL


@pytest.fixture
def base_dir(tmp_path: Path):
    yield tmp_path


@pytest.fixture()
def base_attempt_dir(base_dir: Path):
    attempts_dir = base_dir / "attempts"
    attempts_dir.mkdir()
    yield attempts_dir


@pytest.fixture()
def base_problem_dir(base_dir: Path):
    problems_dir = base_dir / "problems"
    problems_dir.mkdir()
    yield problems_dir


@pytest.fixture()
def attempt_repository(base_attempt_dir: Path):
    yield AttemptRepository(base_attempt_dir)


@pytest.fixture()
def problem_repository(base_problem_dir: Path):
    yield ProblemRepository(base_problem_dir)


@pytest.fixture
def runner(base_problem_dir: Path, base_attempt_dir: Path):
    yield CliRunner(
        env={
            "ALGO_CLI_PROBLEM_DIR": str(base_problem_dir),
            "ALGO_CLI_ATTEMPT_DIR": str(base_attempt_dir),
        }
    )


@pytest.fixture()
def problem_directory_factory(base_problem_dir: Path):
    def create_problem_directory(
        problem: Problem,
        prompt: str = "Some prompt",
        starter: str = "def main():\n    pass",
        tests: str = "from attempt import main\n\ndef test_something():\n    assert True",
    ) -> ProblemDirectory:
        problem_base_path = base_problem_dir / problem.id
        problem_base_path.mkdir()
        problem_dir = ProblemDirectory(problem_base_path)
        problem_dir.problem_path.write_text(problem.model_dump_json())
        problem_dir.prompt_path.write_text(prompt)
        problem_dir.starter_path.write_text(starter)
        problem_dir.tests_path.write_text(tests)
        return problem_dir

    yield create_problem_directory

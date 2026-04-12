from pathlib import Path
import time_machine

import pytest

from typer.testing import CliRunner

from algo_cli.attempt_repository import AttemptRepository
from algo_cli.current_state_repository import CurrentStateRepository
from algo_cli.models import Problem, ProblemDirectory
from algo_cli.problem_repository import ProblemRepository
from algo_cli.stats_repository import StatsRepository

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
def base_state_dir(base_dir: Path):
    state_dir = base_dir / "state"
    state_dir.mkdir()
    yield state_dir


@pytest.fixture()
def base_stats_dir(base_dir: Path):
    stats_dir = base_dir / "stats"
    stats_dir.mkdir()
    yield stats_dir


@pytest.fixture()
def attempt_repository(base_attempt_dir: Path):
    yield AttemptRepository(base_attempt_dir)


@pytest.fixture()
def problem_repository(base_problem_dir: Path):
    yield ProblemRepository(base_problem_dir)


@pytest.fixture()
def current_state_repository(base_state_dir: Path):
    yield CurrentStateRepository(base_state_dir)


@pytest.fixture()
def stats_repository(base_stats_dir: Path):
    yield StatsRepository(base_stats_dir)


@pytest.fixture(autouse=True)
def test_env(
    monkeypatch,
    base_problem_dir: Path,
    base_attempt_dir: Path,
    base_state_dir: Path,
    base_stats_dir: Path,
):
    monkeypatch.setenv("ALGO_CLI_PROBLEM_DIR", str(base_problem_dir))
    monkeypatch.setenv("ALGO_CLI_ATTEMPT_DIR", str(base_attempt_dir))
    monkeypatch.setenv("ALGO_CLI_STATE_DIR", str(base_state_dir))
    monkeypatch.setenv("ALGO_CLI_STATS_DIR", str(base_stats_dir))


@pytest.fixture()
def runner():
    yield CliRunner()


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

from pathlib import Path

import pytest

from typer.testing import CliRunner

from algo_cli.models import Problem, ProblemDirectory


@pytest.fixture
def base_dir(tmp_path: Path):
    yield tmp_path


@pytest.fixture
def runner(base_dir: Path):
    yield CliRunner(env={"ALGO_CLI_PROBLEM_DIR": str(base_dir)})


@pytest.fixture()
def problem_directory_factory(base_dir: Path):
    def create_problem_directory(problem: Problem):
        problem_dir = base_dir / problem.id
        problem_dir.mkdir()
        problem_file = problem_dir / "problem.json"
        problem_file.write_text(problem.model_dump_json())
        return ProblemDirectory(problem_dir)
    yield create_problem_directory
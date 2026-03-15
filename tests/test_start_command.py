import datetime as dt
import pytest

from algo_cli.main import app
from algo_cli.models import Problem


def test_start_attempt_nonexistent_id(runner):
    result = runner.invoke(app, ["start", "abc"])
    assert result.exit_code == 1
    assert "abc" in result.output


@pytest.mark.time_machine(dt.datetime(2020, 10, 20, 12, 11, 9))
def test_start_attempt(attempt_repository, problem_directory_factory, runner):
    problem = Problem(id="p1", title="problem1")
    problem_directory_factory(problem)
    result = runner.invoke(app, ["start", "p1"])
    assert result.exit_code == 0
    attempt_dir = attempt_repository.get_attempt("p1", "2020-10-20T12-11-09")
    assert attempt_dir.solution_path.exists()
    assert attempt_dir.attempt.attempt_id in result.output


@pytest.mark.time_machine(dt.datetime(2020, 10, 20, 12, 11, 9))
def test_start_multiple_attempts(
    attempt_repository, problem_directory_factory, runner, time_machine
):
    problem = Problem(id="p1", title="problem1")
    problem_directory_factory(problem)

    result = runner.invoke(app, ["start", "p1"])
    assert result.exit_code == 0

    time_machine.shift(10)

    result = runner.invoke(app, ["start", "p1"])
    assert result.exit_code == 0

    assert len(attempt_repository.list_attempts("p1")) == 2

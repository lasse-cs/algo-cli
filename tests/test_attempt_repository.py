import datetime as dt
import pytest

from algo_cli.exceptions import AttemptDoesNotExist, InvalidBaseDirectory
from algo_cli.models import Problem
from algo_cli.attempt_repository import AttemptRepository


@pytest.mark.time_machine(dt.datetime(2020, 10, 20, 12, 11, 9))
def test_create_attempt(attempt_repository, problem_directory_factory):
    problem = Problem(id="p1", title="problem1")
    problem_directory = problem_directory_factory(problem)
    attempt_directory = attempt_repository.create_attempt(problem_directory)

    assert attempt_directory.attempt.problem_id == problem.id
    assert attempt_directory.attempt.attempt_id == "2020-10-20T12-11-09"
    assert attempt_directory.attempt_path.exists()
    assert attempt_directory.solution_path.exists()
    assert (
        problem_directory.starter_path.read_text()
        == attempt_directory.solution_path.read_text()
    )


@pytest.mark.time_machine(dt.datetime(2020, 10, 20, 12, 11, 9))
def test_get_attempt(attempt_repository, problem_directory_factory):
    problem = Problem(id="p1", title="problem1")
    problem_directory = problem_directory_factory(problem)
    attempt_directory = attempt_repository.create_attempt(problem_directory)
    assert attempt_directory == attempt_repository.get_attempt(
        "p1", "2020-10-20T12-11-09"
    )


def test_get_attempt_for_nonexistent_problem(attempt_repository):
    with pytest.raises(AttemptDoesNotExist):
        attempt_repository.get_attempt("abc", "def")


def test_get_attempt_for_existent_problem_no_attempts(
    attempt_repository, problem_directory_factory
):
    problem = Problem(id="p1", title="problem1")
    problem_directory_factory(problem)
    with pytest.raises(AttemptDoesNotExist):
        attempt_repository.get_attempt(problem_id="p1", attempt_id="def")


@pytest.mark.time_machine(dt.datetime(2020, 10, 20, 12, 11, 9))
def test_list_attempts_in_order(
    attempt_repository, problem_directory_factory, time_machine
):
    problem = Problem(id="p1", title="problem1")
    problem_dir = problem_directory_factory(problem)
    earlier_attempt = attempt_repository.create_attempt(problem_dir)
    # move to later
    time_machine.shift(10)
    later_attempt = attempt_repository.create_attempt(problem_dir)

    assert attempt_repository.list_attempts("p1") == [later_attempt, earlier_attempt]


def test_list_attempts_nonexistent_problem(attempt_repository):
    assert attempt_repository.list_attempts("p1") == []


def test_list_attempts_existent_problem_nonexistent_attempt(
    attempt_repository, problem_directory_factory
):
    problem = Problem(id="p1", title="problem1")
    problem_directory_factory(problem)
    assert attempt_repository.list_attempts("p1") == []


def test_raises_for_invalid_base_dir(tmp_path):
    non_exist_path = tmp_path / "some_path"
    with pytest.raises(InvalidBaseDirectory):
        AttemptRepository(non_exist_path)

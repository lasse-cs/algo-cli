import datetime as dt
from types import SimpleNamespace

import pytest

from algo_cli.commands.common import complete_problem_id, complete_attempt_id
from algo_cli.models import Problem


def test_complete_problem_id(problem_directory_factory, test_env):
    problems = [
        Problem(id="alpha", title="alpha"),
        Problem(id="aleph", title="aleph"),
        Problem(id="beta", title="beta"),
    ]
    for problem in problems:
        problem_directory_factory(problem)

    completed_problem_ids = complete_problem_id("al")
    assert set(completed_problem_ids) == {"alpha", "aleph"}


def test_complete_problem_id_no_matches(problem_directory_factory, test_env):
    problems = [
        Problem(id="alpha", title="alpha"),
        Problem(id="aleph", title="aleph"),
        Problem(id="beta", title="beta"),
    ]
    for problem in problems:
        problem_directory_factory(problem)

    completed_problem_ids = complete_problem_id("gamma")
    assert set(completed_problem_ids) == set()


@pytest.mark.time_machine(dt.datetime(2020, 10, 20, 12, 11, 9))
def test_complete_attempt_id(problem_directory_factory, attempt_repository, test_env):
    problems = [
        Problem(id="alpha", title="alpha"),
        Problem(id="aleph", title="aleph"),
        Problem(id="beta", title="beta"),
    ]
    problem_directories = [problem_directory_factory(p) for p in problems]
    attempt_directory = attempt_repository.create_attempt(problem_directories[0])

    context = SimpleNamespace(params={"problem_id": "alpha"})
    attempt_ids = complete_attempt_id(context, "2020")
    assert set(attempt_ids) == {attempt_directory.attempt.attempt_id}


@pytest.mark.time_machine(dt.datetime(2020, 10, 20, 12, 11, 9))
def test_complete_attempt_id_no_matches(
    problem_directory_factory, attempt_repository, test_env
):
    problems = [
        Problem(id="alpha", title="alpha"),
        Problem(id="aleph", title="aleph"),
        Problem(id="beta", title="beta"),
    ]
    problem_directories = [problem_directory_factory(p) for p in problems]
    attempt_repository.create_attempt(problem_directories[0])

    context = SimpleNamespace(params={"problem_id": "alpha"})
    attempt_ids = complete_attempt_id(context, "2021")
    assert set(attempt_ids) == set()


@pytest.mark.time_machine(dt.datetime(2020, 10, 20, 12, 11, 9))
def test_complete_attempt_id_no_(
    problem_directory_factory, attempt_repository, test_env
):
    problems = [
        Problem(id="alpha", title="alpha"),
        Problem(id="aleph", title="aleph"),
        Problem(id="beta", title="beta"),
    ]
    problem_directories = [problem_directory_factory(p) for p in problems]
    attempt_repository.create_attempt(problem_directories[0])

    context = SimpleNamespace(params={"problem_id": "gamma"})
    attempt_ids = complete_attempt_id(context, "2020")
    assert set(attempt_ids) == set()

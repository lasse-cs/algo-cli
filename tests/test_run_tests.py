from algo_cli.models import Problem
from algo_cli.run_tests import run_tests


def test_run_successful_tests(attempt_repository, problem_directory_factory):
    problem = Problem(id="p1", title="problem1")
    problem_dir = problem_directory_factory(
        problem,
        starter="def main():\n    return 1",
        tests="from solution import main\n\ndef test_main():\n    assert main() == 1",
    )
    attempt_dir = attempt_repository.create_attempt(problem_dir)

    result = run_tests(attempt_dir)
    assert result.success


def test_run_failing_tests(attempt_repository, problem_directory_factory):
    problem = Problem(id="p1", title="problem1")
    problem_dir = problem_directory_factory(
        problem,
        starter="def main():\n    return 1",
        tests="from solution import main\n\ndef test_main():\n    assert main() == 1",
    )
    attempt_dir = attempt_repository.create_attempt(problem_dir)

    result = run_tests(attempt_dir)
    assert result.success

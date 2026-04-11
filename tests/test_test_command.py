from algo_cli.main import app
from algo_cli.models import Problem


def test_passing_attempt(runner, attempt_repository, problem_directory_factory):
    problem_dir = problem_directory_factory(
        Problem(id="id", title="title"),
        prompt="This is great!",
        starter="def main():\n    return 1",
        tests="from solution import main\n\ndef test_main():\n    assert main() == 1",
    )
    attempt_dir = attempt_repository.create_attempt(problem_dir)
    result = runner.invoke(
        app, ["test", attempt_dir.attempt.problem_id, attempt_dir.attempt.attempt_id]
    )
    assert result.exit_code == 0
    assert "Success" in result.output


def test_failing_attempt(runner, attempt_repository, problem_directory_factory):
    problem_dir = problem_directory_factory(
        Problem(id="id", title="title"),
        prompt="This is great!",
        starter="def main():\n    return 1",
        tests="from solution import main\n\ndef test_main():\n    assert main() == 2",
    )
    attempt_dir = attempt_repository.create_attempt(problem_dir)
    result = runner.invoke(
        app, ["test", attempt_dir.attempt.problem_id, attempt_dir.attempt.attempt_id]
    )
    assert result.exit_code == 1
    assert "Success" not in result.output


def test_missing_attempt(runner):
    result = runner.invoke(app, ["test", "not-real", "also-not-real"])
    assert result.exit_code == 1


def test_run_tests_uses_current_state_when_no_args(runner, problem_directory_factory):
    problem_directory_factory(
        Problem(id="id", title="title"),
        starter="def main():\n    return 1",
        tests="from solution import main\n\ndef test_main():\n    assert main() == 1",
    )
    runner.invoke(app, ["start", "id"])
    result = runner.invoke(app, ["test"])
    assert result.exit_code == 0
    assert "Success" in result.output


def test_run_tests_exits_when_no_args_and_no_state(runner):
    result = runner.invoke(app, ["test"])
    assert result.exit_code == 1
    assert "No current problem/attempt set" in result.output

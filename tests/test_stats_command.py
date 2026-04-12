from algo_cli.main import app
from algo_cli.models import Problem


def test_stats_no_data_shows_empty_message(runner):
    result = runner.invoke(app, ["stats"])
    assert result.exit_code == 0
    assert "No stats recorded yet" in result.output


def test_stats_all_problems_shows_table(runner, stats_repository):
    stats_repository.record("bubble-sort", True)
    stats_repository.record("bubble-sort", False)
    stats_repository.record("merge-sort", True)
    result = runner.invoke(app, ["stats"])
    assert result.exit_code == 0
    assert "bubble-sort" in result.output
    assert "merge-sort" in result.output


def test_stats_specific_problem_shows_detail(runner, stats_repository):
    stats_repository.record("bubble-sort", True)
    stats_repository.record("bubble-sort", False)
    result = runner.invoke(app, ["stats", "bubble-sort"])
    assert result.exit_code == 0
    assert "bubble-sort" in result.output
    assert "2" in result.output  # total_runs


def test_stats_specific_problem_with_no_runs(runner):
    result = runner.invoke(app, ["stats", "bubble-sort"])
    assert result.exit_code == 0
    assert "bubble-sort" in result.output
    assert "0" in result.output


def test_test_command_records_success(
    runner, attempt_repository, problem_directory_factory
):
    problem_dir = problem_directory_factory(
        Problem(id="id", title="title"),
        starter="def main():\n    return 1",
        tests="from solution import main\n\ndef test_main():\n    assert main() == 1",
    )
    attempt_dir = attempt_repository.create_attempt(problem_dir)
    runner.invoke(app, ["test", "id", attempt_dir.attempt.attempt_id])
    result = runner.invoke(app, ["stats", "id"])
    assert result.exit_code == 0
    assert "1" in result.output


def test_test_command_records_failure(
    runner, attempt_repository, problem_directory_factory
):
    problem_dir = problem_directory_factory(
        Problem(id="id", title="title"),
        starter="def main():\n    return 1",
        tests="from solution import main\n\ndef test_main():\n    assert main() == 99",
    )
    attempt_dir = attempt_repository.create_attempt(problem_dir)
    runner.invoke(app, ["test", "id", attempt_dir.attempt.attempt_id])
    result = runner.invoke(app, ["stats", "id"])
    assert result.exit_code == 0
    assert "1" in result.output

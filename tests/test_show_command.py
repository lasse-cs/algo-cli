from algo_cli.main import app
from algo_cli.models import Problem


def test_show_problem(runner, problem_directory_factory):
    problem_dir = problem_directory_factory(
        Problem(id="id", title="title"), prompt="This is great!"
    )
    result = runner.invoke(app, ["show", "id"])
    assert result.exit_code == 0
    assert problem_dir.problem.title in result.output
    assert problem_dir.prompt in result.output


def test_show_missing_problem(runner, problem_directory_factory):
    problem_dir = problem_directory_factory(
        Problem(id="id", title="title"), prompt="This is great!"
    )
    result = runner.invoke(app, ["show", "not-that-id"])
    assert result.exit_code == 1
    assert problem_dir.problem.title not in result.output

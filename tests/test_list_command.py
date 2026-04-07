from algo_cli.main import app
from algo_cli.models import Problem


def test_list_problems(runner, problem_directory_factory):
    problems = [Problem(id="id1", title="title1"), Problem(id="id2", title="title2")]
    [problem_directory_factory(p) for p in problems]

    result = runner.invoke(app, "list problems")
    assert result.exit_code == 0
    assert "ID" in result.output
    assert "Title" in result.output
    assert "id1" in result.output
    assert "id2" in result.output
    assert "title1" in result.output
    assert "title2" in result.output


def test_list_no_problems(runner):
    result = runner.invoke(app, "list problems")
    assert result.exit_code == 0

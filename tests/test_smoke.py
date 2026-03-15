from algo_cli.main import app


def test_help(runner):
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0

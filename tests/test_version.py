from algo_cli.main import app
from algo_cli.version import __version__


def test_version(runner):
    result = runner.invoke(app, "version")
    assert result.exit_code == 0
    assert __version__ in result.output

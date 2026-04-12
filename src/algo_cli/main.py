import typer

from algo_cli.commands.edit import app as edit_app
from algo_cli.commands.list import app as list_app
from algo_cli.commands.show import app as show_app
from algo_cli.commands.start import app as start_app
from algo_cli.commands.run_tests import app as test_app
from algo_cli.commands.stats import app as stats_app
from algo_cli.commands.version import app as version_app


app = typer.Typer()
app.add_typer(version_app)
app.add_typer(list_app)
app.add_typer(show_app)
app.add_typer(start_app)
app.add_typer(test_app)
app.add_typer(edit_app)
app.add_typer(stats_app)

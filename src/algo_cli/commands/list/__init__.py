import typer

from algo_cli.commands.list.attempts import app as attempts_app
from algo_cli.commands.list.problems import app as problems_app


app = typer.Typer(name="list")
app.add_typer(problems_app)
app.add_typer(attempts_app)


@app.callback()
def callback():
    """
    List problems
    """

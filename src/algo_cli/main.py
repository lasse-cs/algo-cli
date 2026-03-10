from pathlib import Path
from typing import Annotated

import typer

from .commands.list import app as list_app
from .problem_repository import ProblemRepository
from .version import app as version_app


app = typer.Typer()
app.add_typer(version_app)
app.add_typer(list_app)


class Config:
    def __init__(self, problem_repository: ProblemRepository):
        self.problem_repository = problem_repository


@app.callback()
def callback(
    ctx: typer.Context,
    problem_dir: Annotated[
        Path | None,
        typer.Option(
            envvar="ALGO_CLI_PROBLEM_DIR",
            hidden=True,
        ),
    ] = None,
):
    if problem_dir is None:
        problem_dir = Path(__file__).parent / "problems"
    ctx.obj = Config(problem_repository=ProblemRepository(problem_dir.resolve()))

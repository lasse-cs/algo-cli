from pathlib import Path
from typing import Annotated

import typer

from .attempt_repository import AttemptRepository
from .commands.list import app as list_app
from .commands.show import app as show_app
from .problem_repository import ProblemRepository
from .version import app as version_app


APP_NAME = "algo-cli"


app = typer.Typer()
app.add_typer(version_app)
app.add_typer(list_app)
app.add_typer(show_app)


class Config:
    def __init__(
        self,
        problem_repository: ProblemRepository,
        attempt_repository: AttemptRepository,
    ):
        self.problem_repository = problem_repository
        self.attempt_repository = attempt_repository


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
    attempt_dir: Annotated[
        Path | None,
        typer.Option(
            envvar="ALGO_CLI_ATTEMPT_DIR",
            hidden=True,
        ),
    ] = None,
):
    if problem_dir is None:
        problem_dir = Path(__file__).parent / "problems"
    if attempt_dir is None:
        app_dir: Path = Path(typer.get_app_dir(APP_NAME))
        app_dir.mkdir(exist_ok=True)
        attempt_dir = Path(app_dir) / "attempts"
        attempt_dir.mkdir(exist_ok=True)
    ctx.obj = Config(
        problem_repository=ProblemRepository(problem_dir.resolve()),
        attempt_repository=AttemptRepository(attempt_dir.resolve()),
    )

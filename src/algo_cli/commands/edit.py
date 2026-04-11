from typing import Annotated

import typer
from rich.console import Console

from algo_cli.commands.common import complete_attempt_id, complete_problem_id
from algo_cli.config import Config
from algo_cli.exceptions import AttemptDoesNotExist


err_console = Console(stderr=True)
console = Console()

app = typer.Typer()


@app.command(name="edit")
def edit(
    problem_id: Annotated[
        str | None, typer.Argument(autocompletion=complete_problem_id)
    ] = None,
    attempt_id: Annotated[
        str | None, typer.Argument(autocompletion=complete_attempt_id)
    ] = None,
):
    """
    Open an editor to edit the attempt for a problem
    """
    config = Config.get()
    if problem_id is None and attempt_id is None:
        state = config.current_state_repository.get_current_state()
        problem_id = state.problem_id
        attempt_id = state.attempt_id
    if problem_id is None or attempt_id is None:
        err_console.print(
            "No current problem/attempt set. Provide problem_id and attempt_id or start an attempt first."
        )
        raise typer.Exit(1)
    try:
        attempt_dir = config.attempt_repository.get_attempt(problem_id, attempt_id)
    except AttemptDoesNotExist:
        err_console.print(
            f"No attempt with id {attempt_id} for problem with id {problem_id}"
        )
        raise typer.Exit(1)
    filename = str(attempt_dir.solution_path.resolve())
    typer.edit(filename=filename)

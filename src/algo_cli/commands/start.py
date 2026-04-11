from typing import Annotated

import typer
from rich.console import Console

from algo_cli.commands.common import complete_problem_id
from algo_cli.config import Config
from algo_cli.exceptions import ProblemDoesNotExist
from algo_cli.models import CurrentState


err_console = Console(stderr=True)
console = Console()

app = typer.Typer()


@app.command(name="start")
def start_attempt(
    id: Annotated[str, typer.Argument(autocompletion=complete_problem_id)],
):
    """
    Start an attempt for a problem by id
    """
    config = Config.get()
    try:
        problem_dir = Config.get().problem_repository.get_problem(id)
    except ProblemDoesNotExist:
        err_console.print(f"No problem with id {id}")
        raise typer.Exit(1)
    attempt_dir = config.attempt_repository.create_attempt(problem_dir)
    config.current_state_repository.set_current_state(
        CurrentState(
            problem_id=attempt_dir.attempt.problem_id,
            attempt_id=attempt_dir.attempt.attempt_id,
        )
    )
    console.print(
        f"Created {attempt_dir.attempt.attempt_id} for {attempt_dir.attempt.problem_id}."
    )
    console.print(f"Edit the file at {attempt_dir.solution_path}")

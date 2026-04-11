from typing import Annotated

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from algo_cli.config import Config
from algo_cli.exceptions import ProblemDoesNotExist
from algo_cli.commands.common import complete_problem_id

console = Console()
err_console = Console(stderr=True)


app = typer.Typer()


@app.command(name="show")
def show_problem(
    id: Annotated[
        str | None, typer.Argument(autocompletion=complete_problem_id)
    ] = None,
):
    """
    Show a problem by id
    """
    config = Config.get()
    if id is None:
        state = config.current_state_repository.get_current_state()
        id = state.problem_id
    if id is None:
        err_console.print(
            "No current problem set. Provide a problem id or start an attempt first."
        )
        raise typer.Exit(1)
    try:
        problem_dir = config.problem_repository.get_problem(id)
    except ProblemDoesNotExist:
        err_console.print(f"No problem with id {id}")
        raise typer.Exit(1)
    console.print(
        Panel(
            Markdown(problem_dir.prompt),
            title=f"{problem_dir.problem.id}: {problem_dir.problem.title}",
        )
    )

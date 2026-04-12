from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from algo_cli.commands.common import complete_problem_id
from algo_cli.config import Config
from algo_cli.exceptions import ProblemDoesNotExist
from algo_cli.models import Attempt, Problem

err_console = Console(stderr=True)
console = Console()


app = typer.Typer()


@app.command(name="attempts")
def list_attempts(
    problem_id: Annotated[str, typer.Argument(autocompletion=complete_problem_id)],
):
    """
    List the available attempts for a problem
    """
    config = Config.get()
    try:
        problem_dir = config.problem_repository.get_problem(problem_id)
    except ProblemDoesNotExist:
        err_console.print(f"No problem with id {problem_id}")
        raise typer.Exit(1)

    attempt_dirs = config.attempt_repository.list_attempts(problem_id)
    attempts = [attempt_dir.attempt for attempt_dir in attempt_dirs]
    table = attempts_to_table(attempts, problem_dir.problem)
    console.print(table)


def attempts_to_table(attempts: list[Attempt], problem: Problem) -> Table:
    table = Table("Problem ID", "Attempt ID", title=f"Attempts for {problem.title}")
    for attempt in attempts:
        table.add_row(attempt.problem_id, attempt.attempt_id)
    return table

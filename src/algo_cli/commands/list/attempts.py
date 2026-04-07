import typer
from rich.console import Console
from rich.table import Table

from algo_cli.models import Attempt
from algo_cli.exceptions import ProblemDoesNotExist

err_console = Console(stderr=True)
console = Console()


app = typer.Typer()


@app.command(name="attempts")
def list_attempts(ctx: typer.Context, problem_id: str):
    """
    List the available attempts for a problem
    """
    try:
        ctx.obj.problem_repository.get_problem(problem_id)
    except ProblemDoesNotExist:
        err_console.print(f"No problem with id {problem_id}")
        raise typer.Exit(1)

    attempt_dirs = ctx.obj.attempt_repository.list_attempts(problem_id)
    attempts = [attempt_dir.attempt for attempt_dir in attempt_dirs]
    table = attempts_to_table(attempts)
    console.print(table)


def attempts_to_table(attempts: list[Attempt]) -> Table:
    table = Table("Problem ID", "Attempt ID")
    for attempt in attempts:
        table.add_row(attempt.problem_id, attempt.attempt_id)
    return table

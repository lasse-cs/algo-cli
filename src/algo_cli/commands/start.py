import typer
from rich.console import Console

from algo_cli.exceptions import ProblemDoesNotExist
from algo_cli.models import AttemptDirectory, ProblemDirectory


err_console = Console(stderr=True)
console = Console()

app = typer.Typer()


@app.command(name="start")
def start_attempt(ctx: typer.Context, id: str):
    """
    Start an attempt for a problem by id
    """
    try:
        problem_dir: ProblemDirectory = ctx.obj.problem_repository.get_problem(id)
    except ProblemDoesNotExist:
        err_console.print(f"No problem with id {id}")
        raise typer.Exit(1)
    attempt_dir: AttemptDirectory = ctx.obj.attempt_repository.create_attempt(
        problem_dir
    )
    console.print(
        f"Created {attempt_dir.attempt.attempt_id} for {attempt_dir.attempt.problem_id}."
    )
    console.print(f"Edit the file at {attempt_dir.solution_path}")

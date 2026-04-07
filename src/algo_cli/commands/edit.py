import typer
from rich.console import Console

from algo_cli.exceptions import AttemptDoesNotExist
from algo_cli.models import AttemptDirectory


err_console = Console(stderr=True)
console = Console()

app = typer.Typer()


@app.command(name="edit")
def edit(ctx: typer.Context, problem_id: str, attempt_id: str):
    """
    Open an editor to edit the attempt for a problem
    """
    try:
        attempt_dir: AttemptDirectory = ctx.obj.attempt_repository.get_attempt(
            problem_id, attempt_id
        )
    except AttemptDoesNotExist:
        err_console.print(
            f"No attempt with id {attempt_id} for problem with id {problem_id}"
        )
        raise typer.Exit(1)
    filename = str(attempt_dir.solution_path.resolve())
    typer.edit(filename=filename)

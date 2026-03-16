import typer
from rich.console import Console

from algo_cli.exceptions import AttemptDoesNotExist
from algo_cli.models import AttemptDirectory
from algo_cli.run_tests import run_tests as test_runner


err_console = Console(stderr=True)
console = Console()

app = typer.Typer()


@app.command(name="test")
def run_tests(ctx: typer.Context, problem_id: str, attempt_id: str):
    """
    Run the tests for an attempt to a problem
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
    result = test_runner(attempt_dir)
    if result.success:
        console.print("[bold green]Success![/bold green]")
    else:
        err_console.print("[bold red]Failure[/bold red]")
        err_console.print(result.output)
        err_console.print(result.error)
        raise typer.Exit(1)

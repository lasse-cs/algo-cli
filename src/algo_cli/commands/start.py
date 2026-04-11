import typer
from rich.console import Console

from algo_cli.config import Config
from algo_cli.exceptions import ProblemDoesNotExist


err_console = Console(stderr=True)
console = Console()

app = typer.Typer()


@app.command(name="start")
def start_attempt(id: str):
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
    console.print(
        f"Created {attempt_dir.attempt.attempt_id} for {attempt_dir.attempt.problem_id}."
    )
    console.print(f"Edit the file at {attempt_dir.solution_path}")

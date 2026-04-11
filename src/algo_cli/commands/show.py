import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from algo_cli.config import Config
from algo_cli.exceptions import ProblemDoesNotExist


console = Console()
err_console = Console(stderr=True)


app = typer.Typer()


@app.command(name="show")
def show_problem(id: str):
    """
    Show a problem by id
    """
    try:
        problem_dir = Config.get().problem_repository.get_problem(id)
    except ProblemDoesNotExist:
        err_console.print(f"No problem with id {id}")
        raise typer.Exit(1)
    console.print(
        Panel(
            Markdown(problem_dir.prompt),
            title=f"{problem_dir.problem.id}: {problem_dir.problem.title}",
        )
    )

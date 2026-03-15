import typer
from rich.console import Console
from rich.table import Table

from algo_cli.models import Problem


console = Console()


app = typer.Typer()


@app.command(name="list")
def list_problems(ctx: typer.Context):
    """
    List the available problems
    """
    problem_dirs = ctx.obj.problem_repository.list_problems()
    problems = [problem_dir.problem for problem_dir in problem_dirs]
    table = problems_to_table(problems)
    console.print(table)


def problems_to_table(problems: list[Problem]) -> Table:
    table = Table("ID", "Title")
    for problem in problems:
        table.add_row(problem.id, problem.title)
    return table

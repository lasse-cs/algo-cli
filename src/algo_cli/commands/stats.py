from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from algo_cli.commands.common import complete_problem_id
from algo_cli.config import Config


console = Console()

app = typer.Typer()


@app.command(name="stats")
def stats(
    problem_id: Annotated[
        str | None, typer.Argument(autocompletion=complete_problem_id)
    ] = None,
):
    """
    Show solve statistics — total runs, successes, and failures per problem.
    """
    config = Config.get()

    if problem_id is not None:
        problem_stats = config.stats_repository.get(problem_id)
        table = Table(title=f"Stats: {problem_id}")
        table.add_column("Metric", style="bold")
        table.add_column("Count", justify="right")
        table.add_row("Total runs", str(problem_stats.total_runs))
        table.add_row("Successful", str(problem_stats.successful_runs))
        table.add_row("Failed", str(problem_stats.failed_runs))
        console.print(table)
    else:
        all_stats = config.stats_repository.get_all()
        table = Table(title="Problem Stats")
        table.add_column("Problem", style="bold")
        table.add_column("Total Runs", justify="right")
        table.add_column("Successful", justify="right", style="green")
        table.add_column("Failed", justify="right", style="red")
        for s in sorted(all_stats, key=lambda x: x.problem_id):
            table.add_row(
                s.problem_id,
                str(s.total_runs),
                str(s.successful_runs),
                str(s.failed_runs),
            )
        console.print(table)

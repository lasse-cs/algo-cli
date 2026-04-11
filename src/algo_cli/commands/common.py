import typer

from algo_cli.config import Config


def complete_problem_id(incomplete_problem_id: str):
    problems = Config.get().problem_repository.list_problems()
    for problem in problems:
        if problem.problem.id.startswith(incomplete_problem_id):
            yield problem.problem.id


def complete_attempt_id(ctx: typer.Context, incomplete_attempt_id: str):
    problem_id = ctx.params.get("problem_id")
    attempts = (
        Config.get().attempt_repository.list_attempts(problem_id) if problem_id else []
    )

    for attempt in attempts:
        if attempt.attempt.attempt_id.startswith(incomplete_attempt_id):
            yield attempt.attempt.attempt_id

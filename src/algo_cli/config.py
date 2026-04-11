import os

import typer

from pathlib import Path

from algo_cli.attempt_repository import AttemptRepository
from algo_cli.current_state_repository import CurrentStateRepository
from algo_cli.problem_repository import ProblemRepository


APP_NAME = "algo-cli"


class Config:
    def __init__(
        self,
        problem_repository: ProblemRepository,
        attempt_repository: AttemptRepository,
        current_state_repository: CurrentStateRepository,
    ):
        self.problem_repository = problem_repository
        self.attempt_repository = attempt_repository
        self.current_state_repository = current_state_repository

    @classmethod
    def get(cls) -> "Config":
        if "ALGO_CLI_PROBLEM_DIR" in os.environ:
            problem_dir = Path(os.environ["ALGO_CLI_PROBLEM_DIR"])
        else:
            problem_dir = Path(__file__).parent / "problems"

        if "ALGO_CLI_ATTEMPT_DIR" in os.environ:
            attempt_dir = Path(os.environ["ALGO_CLI_ATTEMPT_DIR"])
        else:
            app_dir: Path = Path(typer.get_app_dir(APP_NAME))
            app_dir.mkdir(exist_ok=True)
            attempt_dir = Path(app_dir) / "attempts"
        attempt_dir.mkdir(exist_ok=True)

        if "ALGO_CLI_STATE_DIR" in os.environ:
            state_dir = Path(os.environ["ALGO_CLI_STATE_DIR"])
        else:
            app_dir = Path(typer.get_app_dir(APP_NAME))
            app_dir.mkdir(exist_ok=True)
            state_dir = Path(app_dir) / "state"
        state_dir.mkdir(exist_ok=True)

        return cls(
            ProblemRepository(problem_dir),
            AttemptRepository(attempt_dir),
            CurrentStateRepository(state_dir),
        )

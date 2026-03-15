from pathlib import Path

from algo_cli.models import ProblemDirectory

from algo_cli.exceptions import (
    InvalidBaseDirectory,
)


class ProblemRepository:
    def __init__(self, base_problem_dir: Path):
        if not base_problem_dir.is_dir():
            raise InvalidBaseDirectory(f"{base_problem_dir} is not a directory")
        self._base_problem_dir = base_problem_dir

    def get_problem(self, problem_id: str) -> ProblemDirectory:
        return ProblemDirectory(self._base_problem_dir / problem_id)

    def list_problems(self) -> list[ProblemDirectory]:
        return sorted(
            (
                ProblemDirectory(child)
                for child in self._base_problem_dir.iterdir()
                if child.is_dir()
            ),
            key=lambda pd: pd.problem.id,
        )

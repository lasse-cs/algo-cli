from pathlib import Path

from .models import ProblemDirectory

from .exceptions import InvalidBaseDirectory

class ProblemRepository:
    def __init__(self, base_problem_dir: Path):
        if not base_problem_dir.is_dir():
            raise InvalidBaseDirectory(f"{base_problem_dir} is not a directory")
        self._base_problem_dir = base_problem_dir


    def get_problem(self, problem_id: str) -> ProblemDirectory | None:
        problem_path = self._base_problem_dir / problem_id
        if not problem_path.is_dir():
            return None
        return ProblemDirectory(self._base_problem_dir / problem_id)


    def list_problems(self) -> list[ProblemDirectory]:
        result = []
        for child in self._base_problem_dir.iterdir():
            if not child.is_dir():
                continue
            result.append(ProblemDirectory(child))
        return sorted(result, key=lambda pd: pd.problem.id)
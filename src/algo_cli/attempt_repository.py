import datetime
from pathlib import Path

from algo_cli.exceptions import InvalidBaseDirectory

from algo_cli.models import Attempt, AttemptDirectory, ProblemDirectory


ATTEMPT_ID_FORMAT = "%Y-%m-%dT%H-%M-%S"


class AttemptRepository:
    def __init__(self, base_attempt_dir: Path):
        if not base_attempt_dir.is_dir():
            raise InvalidBaseDirectory(f"{base_attempt_dir} is not a directory")
        self._base_attempt_dir = base_attempt_dir

    def create_attempt(self, problem_dir: ProblemDirectory) -> AttemptDirectory:
        attempt_id = datetime.datetime.now().strftime(ATTEMPT_ID_FORMAT)
        problem_id = problem_dir.problem.id
        attempt_parent = self._base_attempt_dir / problem_id
        attempt_parent.mkdir(exist_ok=True)
        attempt_base = attempt_parent / attempt_id
        attempt_base.mkdir()
        attempt = Attempt(attempt_id=attempt_id, problem_id=problem_id)
        attempt_dir = AttemptDirectory(path=attempt_base)
        attempt_dir.attempt_path.write_text(attempt.model_dump_json())
        problem_dir.starter_path.copy(attempt_dir.solution_path)
        return attempt_dir

    def get_attempt(self, problem_id: str, attempt_id: str) -> AttemptDirectory:
        return AttemptDirectory(path=self._base_attempt_dir / problem_id / attempt_id)

    def list_attempts(self, problem_id: str) -> list[AttemptDirectory]:
        base_problem_attempts = self._base_attempt_dir / problem_id
        if not base_problem_attempts.is_dir():
            return []
        return sorted(
            (
                AttemptDirectory(child)
                for child in base_problem_attempts.iterdir()
                if child.is_dir()
            ),
            key=lambda ad: datetime.datetime.strptime(
                ad.attempt.attempt_id, ATTEMPT_ID_FORMAT
            ),
        )

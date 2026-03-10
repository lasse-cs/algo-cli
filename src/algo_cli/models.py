from dataclasses import dataclass

from pathlib import Path

from pydantic import BaseModel

from .exceptions import MalformedProblemDirectory


class Problem(BaseModel):
    id: str
    title: str


@dataclass
class ProblemDirectory:
    def __init__(self, path: Path):
        self.path = path
        if not self.path.is_dir():
            raise MalformedProblemDirectory(f"{path} is not a directory")
        try:
            self.problem = Problem.model_validate_json(self.problem_path().read_text())
        except (ValueError, OSError) as e:
            raise MalformedProblemDirectory(f"Could not read problem file at {self.problem_path()}") from e

    def problem_path(self) -> Path:
        return self.path / "problem.json"
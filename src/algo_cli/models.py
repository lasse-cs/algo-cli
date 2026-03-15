from dataclasses import dataclass

from pathlib import Path

from pydantic import BaseModel

from .exceptions import (
    AttemptDoesNotExist,
    MalformedAttemptDirectory,
    MalformedProblemDirectory,
    ProblemDoesNotExist,
)


class Problem(BaseModel):
    id: str
    title: str


@dataclass
class ProblemDirectory:
    def __init__(self, path: Path):
        if not path.is_dir():
            raise ProblemDoesNotExist(f"Problem at {path} does not exist")
        self.path = path

    @property
    def problem_path(self) -> Path:
        return self.path / "problem.json"

    @property
    def prompt_path(self) -> Path:
        return self.path / "prompt.md"

    @property
    def starter_path(self) -> Path:
        return self.path / "starter.py"

    @property
    def problem(self) -> Problem:
        if not hasattr(self, "_problem"):
            try:
                self._problem = Problem.model_validate_json(
                    self.problem_path.read_text()
                )
            except (ValueError, OSError) as e:
                raise MalformedProblemDirectory(
                    f"Could not read problem file at {self.problem_path}"
                ) from e
        return self._problem

    @property
    def prompt(self) -> str:
        if not hasattr(self, "_prompt"):
            try:
                self._prompt = self.prompt_path.read_text()
            except (ValueError, OSError) as e:
                raise MalformedProblemDirectory(
                    f"Could not read problem file at {self.prompt_path}"
                ) from e
        return self._prompt


class Attempt(BaseModel):
    attempt_id: str
    problem_id: str


@dataclass
class AttemptDirectory:
    def __init__(self, path: Path):
        if not path.is_dir():
            raise AttemptDoesNotExist(f"Attempt at {path} does not exist.")
        self.path = path

    @property
    def attempt_path(self):
        return self.path / "attempt.json"

    @property
    def solution_path(self):
        return self.path / "solution.py"

    @property
    def attempt(self):
        if not hasattr(self, "_attempt"):
            try:
                self._attempt = Attempt.model_validate_json(
                    self.attempt_path.read_text()
                )
            except (ValueError, OSError) as e:
                raise MalformedAttemptDirectory(
                    f"Could not read attempt file at {self.attempt_path}"
                ) from e
        return self._attempt

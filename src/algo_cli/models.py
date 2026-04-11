from dataclasses import dataclass
from functools import cached_property

from pathlib import Path

from pydantic import BaseModel

from algo_cli.exceptions import (
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
    def tests_path(self) -> Path:
        return self.path / "tests.py"

    @cached_property
    def problem(self) -> Problem:
        try:
            return Problem.model_validate_json(self.problem_path.read_text())
        except (ValueError, OSError) as e:
            raise MalformedProblemDirectory(
                f"Could not read problem file at {self.problem_path}"
            ) from e

    @cached_property
    def prompt(self) -> str:
        try:
            return self.prompt_path.read_text()
        except (ValueError, OSError) as e:
            raise MalformedProblemDirectory(
                f"Could not read problem file at {self.prompt_path}"
            ) from e


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
    def tests_path(self):
        return self.path / "tests.py"

    @cached_property
    def attempt(self):
        try:
            return Attempt.model_validate_json(self.attempt_path.read_text())
        except (ValueError, OSError) as e:
            raise MalformedAttemptDirectory(
                f"Could not read attempt file at {self.attempt_path}"
            ) from e


@dataclass
class RunTestResult:
    success: bool
    output: str
    error: str

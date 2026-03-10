import pytest

from algo_cli.exceptions import InvalidBaseDirectory
from algo_cli.models import Problem
from algo_cli.problem_repository import ProblemRepository



def test_list_empty_problems(base_dir):
    problem_repository = ProblemRepository(base_dir)
    assert problem_repository.list_problems() == []


def test_list_problems(base_dir, problem_directory_factory):
    problems = [Problem(id="id1", title="title1"), Problem(id="id2", title="title2")]
    problem_directories = [problem_directory_factory(p) for p in problems]
    
    problem_repository = ProblemRepository(base_dir)
    assert problem_repository.list_problems() == problem_directories


def test_raises_for_invalid_base_dir(tmp_path):
    non_exist_path = tmp_path / "some_path"
    with pytest.raises(InvalidBaseDirectory):
        ProblemRepository(non_exist_path)
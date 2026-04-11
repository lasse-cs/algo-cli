import pytest

from algo_cli.current_state_repository import CurrentStateRepository
from algo_cli.exceptions import InvalidBaseDirectory, MalformedCurrentState
from algo_cli.models import CurrentState


def test_get_current_state_returns_empty_state_when_no_file(current_state_repository):
    state = current_state_repository.get_current_state()
    assert state == CurrentState()
    assert state.problem_id is None
    assert state.attempt_id is None


def test_set_and_get_current_state(current_state_repository):
    state = CurrentState(problem_id="bubble-sort", attempt_id="2024-01-01T00-00-00")
    current_state_repository.set_current_state(state)
    result = current_state_repository.get_current_state()
    assert result.problem_id == "bubble-sort"
    assert result.attempt_id == "2024-01-01T00-00-00"


def test_set_current_state_overwrites_previous(current_state_repository):
    current_state_repository.set_current_state(
        CurrentState(problem_id="bubble-sort", attempt_id="old")
    )
    current_state_repository.set_current_state(
        CurrentState(problem_id="merge-sort", attempt_id="new")
    )
    result = current_state_repository.get_current_state()
    assert result.problem_id == "merge-sort"
    assert result.attempt_id == "new"


def test_get_current_state_raises_for_malformed_file(base_state_dir):
    repo = CurrentStateRepository(base_state_dir)
    (base_state_dir / "state.json").write_text("not valid json")
    with pytest.raises(MalformedCurrentState):
        repo.get_current_state()


def test_raises_for_invalid_base_dir(tmp_path):
    non_exist_path = tmp_path / "some_path"
    with pytest.raises(InvalidBaseDirectory):
        CurrentStateRepository(non_exist_path)

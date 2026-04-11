from pathlib import Path

from algo_cli.models import CurrentState

from algo_cli.exceptions import (
    InvalidBaseDirectory,
    MalformedCurrentState,
)


class CurrentStateRepository:
    def __init__(self, base_config_dir: Path):
        if not base_config_dir.is_dir():
            raise InvalidBaseDirectory(f"{base_config_dir} is not a directory")
        self._state_file = base_config_dir / "state.json"

    def get_current_state(self) -> CurrentState:
        try:
            if not self._state_file.exists():
                return CurrentState()
            return CurrentState.model_validate_json(self._state_file.read_text())
        except (ValueError, OSError) as e:
            raise MalformedCurrentState(
                f"Could not read state file at {self._state_file}"
            ) from e

    def set_current_state(self, state: CurrentState):
        try:
            self._state_file.write_text(state.model_dump_json())
        except OSError as e:
            raise MalformedCurrentState(
                f"Could not write to state file at {self._state_file}"
            ) from e

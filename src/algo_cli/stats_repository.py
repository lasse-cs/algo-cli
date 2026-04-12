import json
from pathlib import Path

from algo_cli.exceptions import InvalidBaseDirectory, MalformedStats
from algo_cli.models import ProblemStats


class StatsRepository:
    def __init__(self, base_stats_dir: Path):
        if not base_stats_dir.is_dir():
            raise InvalidBaseDirectory(f"{base_stats_dir} is not a directory")
        self._stats_file = base_stats_dir / "stats.json"

    def get(self, problem_id: str) -> ProblemStats:
        try:
            if not self._stats_file.exists():
                return ProblemStats(problem_id=problem_id)
            data: dict[str, dict] = json.loads(self._stats_file.read_text())
            if problem_id not in data:
                return ProblemStats(problem_id=problem_id)
            return ProblemStats.model_validate(data[problem_id])
        except (ValueError, OSError) as e:
            raise MalformedStats(
                f"Could not read stats file at {self._stats_file}"
            ) from e

    def get_all(self) -> list[ProblemStats]:
        try:
            if not self._stats_file.exists():
                return []
            data: dict[str, dict] = json.loads(self._stats_file.read_text())
            return [ProblemStats.model_validate(v) for v in data.values()]
        except (ValueError, OSError) as e:
            raise MalformedStats(
                f"Could not read stats file at {self._stats_file}"
            ) from e

    def record(self, problem_id: str, success: bool) -> None:
        try:
            if self._stats_file.exists():
                data: dict[str, dict] = json.loads(self._stats_file.read_text())
            else:
                data = {}

            if problem_id in data:
                stats = ProblemStats.model_validate(data[problem_id])
            else:
                stats = ProblemStats(problem_id=problem_id)

            stats.total_runs += 1
            if success:
                stats.successful_runs += 1
            else:
                stats.failed_runs += 1

            data[problem_id] = stats.model_dump()
            self._stats_file.write_text(json.dumps(data))
        except (ValueError, OSError) as e:
            raise MalformedStats(
                f"Could not write to stats file at {self._stats_file}"
            ) from e

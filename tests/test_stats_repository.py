import pytest

from algo_cli.exceptions import InvalidBaseDirectory, MalformedStats
from algo_cli.models import ProblemStats
from algo_cli.stats_repository import StatsRepository


def test_get_returns_zeroed_stats_when_no_file(stats_repository):
    result = stats_repository.get("bubble-sort")
    assert result == ProblemStats(problem_id="bubble-sort")
    assert result.total_runs == 0
    assert result.successful_runs == 0
    assert result.failed_runs == 0


def test_get_returns_zeroed_stats_for_unknown_problem(stats_repository):
    stats_repository.record("other-problem", True)
    result = stats_repository.get("bubble-sort")
    assert result.total_runs == 0


def test_record_success_increments_correctly(stats_repository):
    stats_repository.record("bubble-sort", True)
    result = stats_repository.get("bubble-sort")
    assert result.total_runs == 1
    assert result.successful_runs == 1
    assert result.failed_runs == 0


def test_record_failure_increments_correctly(stats_repository):
    stats_repository.record("bubble-sort", False)
    result = stats_repository.get("bubble-sort")
    assert result.total_runs == 1
    assert result.successful_runs == 0
    assert result.failed_runs == 1


def test_record_multiple_runs_accumulate(stats_repository):
    stats_repository.record("bubble-sort", False)
    stats_repository.record("bubble-sort", False)
    stats_repository.record("bubble-sort", True)
    result = stats_repository.get("bubble-sort")
    assert result.total_runs == 3
    assert result.successful_runs == 1
    assert result.failed_runs == 2


def test_record_tracks_multiple_problems_independently(stats_repository):
    stats_repository.record("bubble-sort", True)
    stats_repository.record("merge-sort", False)
    bubble = stats_repository.get("bubble-sort")
    merge = stats_repository.get("merge-sort")
    assert bubble.total_runs == 1
    assert bubble.successful_runs == 1
    assert merge.total_runs == 1
    assert merge.failed_runs == 1


def test_get_all_returns_empty_list_when_no_file(stats_repository):
    assert stats_repository.get_all() == []


def test_get_all_returns_all_recorded_problems(stats_repository):
    stats_repository.record("bubble-sort", True)
    stats_repository.record("merge-sort", False)
    all_stats = stats_repository.get_all()
    ids = {s.problem_id for s in all_stats}
    assert ids == {"bubble-sort", "merge-sort"}


def test_get_raises_for_malformed_file(base_stats_dir):
    repo = StatsRepository(base_stats_dir)
    (base_stats_dir / "stats.json").write_text("not valid json")
    with pytest.raises(MalformedStats):
        repo.get("bubble-sort")


def test_get_all_raises_for_malformed_file(base_stats_dir):
    repo = StatsRepository(base_stats_dir)
    (base_stats_dir / "stats.json").write_text("not valid json")
    with pytest.raises(MalformedStats):
        repo.get_all()


def test_raises_for_invalid_base_dir(tmp_path):
    non_exist_path = tmp_path / "some_path"
    with pytest.raises(InvalidBaseDirectory):
        StatsRepository(non_exist_path)

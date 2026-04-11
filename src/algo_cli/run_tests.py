from algo_cli.models import AttemptDirectory
from algo_cli.pytest_runner import run_pytest


def run_tests(attempt_dir: AttemptDirectory):
    return run_pytest(
        cwd=attempt_dir.path,
        test_target=attempt_dir.tests_path.name,
    )

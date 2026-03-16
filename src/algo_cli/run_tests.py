import subprocess

from algo_cli.models import AttemptDirectory, RunTestResult


def run_tests(attempt_dir: AttemptDirectory):
    result = subprocess.run(
        ["pytest", str(attempt_dir.tests_path)],
        capture_output=True,
        text=True,
        cwd=attempt_dir.path,
    )
    return RunTestResult(
        success=result.returncode == 0, output=result.stdout, error=result.stderr
    )

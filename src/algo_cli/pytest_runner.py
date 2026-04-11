import contextlib
import importlib
import io
import os
import sys
from pathlib import Path

import pytest

from algo_cli.models import RunTestResult


def run_pytest(
    *,
    cwd: Path,
    test_target: str | Path,
    args: list[str] | None = None,
    reset_modules: tuple[str, ...] = ("solution", "tests"),
) -> RunTestResult:
    output_stream = io.StringIO()
    error_stream = io.StringIO()
    original_cwd = Path.cwd()

    try:
        os.chdir(cwd)
        # Repeated pytest.main calls share interpreter state, so drop common
        # module names to avoid import-file-mismatch across different folders.
        for module_name in reset_modules:
            sys.modules.pop(module_name, None)
        importlib.invalidate_caches()

        pytest_args = [*(args or []), str(test_target)]
        with (
            contextlib.redirect_stdout(output_stream),
            contextlib.redirect_stderr(error_stream),
        ):
            exit_code = pytest.main(pytest_args)
    finally:
        os.chdir(original_cwd)

    return RunTestResult(
        success=exit_code == pytest.ExitCode.OK,
        output=output_stream.getvalue(),
        error=error_stream.getvalue(),
    )

from algo_cli.main import app


def test_edit_attempt_opens_editor_with_solution_path(
    runner, base_attempt_dir, monkeypatch
):
    attempt_dir = base_attempt_dir / "p1" / "a1"
    attempt_dir.mkdir(parents=True)
    (attempt_dir / "solution.py").write_text("print('hello')")

    called = {}

    def fake_edit(*, filename):
        called["filename"] = filename

    monkeypatch.setattr("algo_cli.commands.edit.typer.edit", fake_edit)

    result = runner.invoke(app, ["edit", "p1", "a1"])

    assert result.exit_code == 0
    assert called["filename"] == str((attempt_dir / "solution.py").resolve())


def test_edit_attempt_missing_attempt_exits_1(runner):
    result = runner.invoke(app, ["edit", "p1", "missing"])
    assert result.exit_code == 1
    assert "No attempt with id missing for problem with id p1" in result.output


def test_edit_uses_current_state_when_no_args(
    runner, problem_directory_factory, monkeypatch
):
    from algo_cli.models import Problem

    problem_directory_factory(Problem(id="p1", title="problem1"))
    runner.invoke(app, ["start", "p1"])

    called = {}

    def fake_edit(*, filename):
        called["filename"] = filename

    monkeypatch.setattr("algo_cli.commands.edit.typer.edit", fake_edit)

    result = runner.invoke(app, ["edit"])

    assert result.exit_code == 0
    assert called["filename"].endswith("solution.py")


def test_edit_exits_when_no_args_and_no_state(runner):
    result = runner.invoke(app, ["edit"])
    assert result.exit_code == 1
    assert "No current problem/attempt set" in result.output

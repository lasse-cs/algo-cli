from importlib.metadata import version as app_version

import typer


__version__ = app_version("algo-cli")


app = typer.Typer()


@app.command(name="version")
def version():
    """
    Show the algo-cli version
    """
    print(__version__)

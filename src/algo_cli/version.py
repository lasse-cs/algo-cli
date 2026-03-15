import typer

__version__ = "0.1.0"


app = typer.Typer()


@app.command()
def version():
    """
    Show the algo-cli version
    """
    print(__version__)

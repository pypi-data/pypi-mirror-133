import pathlib

import typer
from plumbum import FG, local

app = typer.Typer()


@app.command()
def setup(ip):
    local["ansible-galaxy"]["install", "geerlingguy.docker"] & FG
    (
        local["ansible-playbook"][
            "-i",
            f"{ip},",
            str(pathlib.Path(__file__).parent.resolve()) + "/../ansible/setup.yaml",
        ]
        & FG
    )

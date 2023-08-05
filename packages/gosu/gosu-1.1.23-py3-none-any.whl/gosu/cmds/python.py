import glob
import json
import os
import subprocess

import toml
import typer
from dotenv import dotenv_values
from plumbum import FG, ProcessExecutionError, local

app = typer.Typer()


def env_from_sourcing(source_path, include_unexported_variables=True):
    source = "{}source {}".format(
        "set -a && " if include_unexported_variables else "", source_path
    )
    dump = 'python3 -c "import os, json; print(json.dumps(dict(os.environ)))"'
    with subprocess.Popen(
        ["/bin/bash", "-c", f"{source} && {dump}"], stdout=subprocess.PIPE
    ) as pipe:
        return json.loads(pipe.stdout.read())


def _manage_env_vars():
    env_vars = dotenv_values(".env")
    for name, value in env_vars.items():
        local.env[name] = value

    if "TUHLS_SETTINGS_MODULE" in local.env:
        t = local.env["TUHLS_SETTINGS_MODULE"].split(".")
        local.env["DJANGO_CONFIGURATION"] = t[-1].capitalize()
        local.env["DJANGO_SETTINGS_MODULE"] = ".".join(t[:-1])

    return env_vars


def get_project_src():
    t = _get_pyproject_toml()
    return t["project"]["name"]


def _run(*cmds, src=False):
    _manage_env_vars()
    print(cmds)  # noqa
    if src:
        local.cwd.chdir(get_project_src())
    if not os.path.isdir(".venv"):
        local[cmds[0]][cmds[1:]] & FG
        return

    try:
        local.get(f".venv/bin/{cmds[0]}")[cmds[1:]] & FG
    except ProcessExecutionError:
        exit(1)


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def run(ctx: typer.Context):
    _run(*ctx.args)


@app.command()
def sh():
    _manage_env_vars()
    for k, v in env_from_sourcing(".venv/bin/activate").items():
        local.env[k] = v
    local.get(local.env["SHELL"].split("/")[-1]) & FG


def _get_pyproject_toml():
    parts = os.getcwd().split(os.sep)
    for x in range(len(parts), 0, -1):
        try:
            return toml.load(os.sep.join(parts[0:x] + ["pyproject.toml"]))
        except FileNotFoundError:
            pass
    raise FileNotFoundError


def _get_editable_installs():
    t = _get_pyproject_toml()
    if "gosu" not in t:
        return {}
    if "editable" not in t["gosu"]:
        return {}
    return {key: path for key, path in t["gosu"]["editable"].items()}


@app.command()
def create_venv():
    _manage_env_vars()
    local["python3"]["-m", "venv", ".venv"] & FG


@app.command()
def install_dependencies(env: str = typer.Argument("dev")):
    _manage_env_vars()
    _run("pip", "install", "-U", "pip", "wheel", "gosu")
    if env == "dev" or env == "editable":
        _run("pip", "install", "-e", ".[dev]")
    if env == "editable":
        for key, path in _get_editable_installs().items():
            _run("pip", "install", "-e", path)
    if env == "prod":
        _run("pip", "install", *list(glob.glob("*.tar.gz")))


def _get_pkg_pyfiles():
    files = list(
        filter(
            lambda e: all(
                [not (x in e) for x in ["node_modules", "migrations", "build"]]
            ),
            glob.glob("**/*.py", recursive=True),
        )
    )
    print(files)  # noqa
    return files


@app.command()
def fix():
    _run("pyupgrade", "--py38-plus", "--exit-zero-even-if-changed", *_get_pkg_pyfiles())
    _run("isort", "--profile", "black", *_get_pkg_pyfiles())
    _run("black", *_get_pkg_pyfiles())
    _run("flake8", "--config", f"{os.path.dirname(__file__)}/../.flake8")


@app.command()
def lint():
    _run("pyupgrade", "--py38-plus", *_get_pkg_pyfiles())
    _run("isort", "--profile", "black", "-c", *_get_pkg_pyfiles())
    _run("black", "--check", *_get_pkg_pyfiles())
    _run("flake8", "--config", f"{os.path.dirname(__file__)}/../.flake8")


@app.command()
def test():
    rcfile = f"--rcfile={os.path.dirname(__file__)}/../.coveragerc_python"
    _run(
        "coverage",
        "run",
        rcfile,
        "-m",
        "pytest",
        "-o",
        "console_output_style=progress",
    )
    _run("coverage", "report", "-i", rcfile)


@app.command()
def build():
    _run("flit", "build")


@app.command()
def precommit():
    fix()
    test()
    build()

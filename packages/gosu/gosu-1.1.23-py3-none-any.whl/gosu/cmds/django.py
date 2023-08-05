import os

import typer
from plumbum import local

from gosu.cmds.python import _manage_env_vars, _run, build, fix

app = typer.Typer()


def _pm(*cmds):
    _manage_env_vars()
    _run("python", "-m", f"{get_project()}.manage", *cmds)


def get_project():
    if "TUHLS_SETTINGS_MODULE" not in local.env:
        return "example"
    else:
        return local.env["TUHLS_SETTINGS_MODULE"].split(".")[0]


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def pm(ctx: typer.Context):
    _pm(*ctx.args)


@app.command()
def migrate():
    _pm("makemigrations")
    _pm("migrate")


@app.command()
def gunicorn():
    _pm("collectstatic", "--no-input")
    _pm("migrate")
    local.env["DJANGO_CONFIGURATION"] = local.env["TUHLS_SETTINGS_MODULE"].split(".")[
        -1
    ]
    local.env["DJANGO_SETTINGS_MODULE"] = ".".join(
        local.env["TUHLS_SETTINGS_MODULE"].split(".")[:-1]
    )
    _run(
        "gunicorn",
        "--bind",
        "0.0.0.0:8000",
        "--workers=2",
        "--worker-tmp-dir",
        "/dev/shm",
        f"{get_project()}.base.wsgi:application",
    )


@app.command()
def test():
    _manage_env_vars()

    local.env["DEFAULT_CACHE"] = "locmemcache://"
    local.env["QUEUE_CACHE"] = "locmemcache://"
    rcfile = f"--rcfile={os.path.dirname(__file__)}/../.coveragerc_django"
    _run(
        "coverage",
        "run",
        "--concurrency=multiprocessing",
        "--parallel-mode",
        rcfile,
        f"{get_project()}/manage.py",
        "test",
        "--parallel=3",
        ".",
        get_project(),
    )
    _run("coverage", "combine", rcfile)
    _run("coverage", "report", "-i", rcfile)


@app.command()
def precommit():
    fix()
    test()
    build()


@app.command()
def notebook():
    local.env["DJANGO_ALLOW_ASYNC_UNSAFE"] = True
    _pm("shell_plus", "--notebook")

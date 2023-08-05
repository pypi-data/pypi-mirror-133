import os

import plumbum.commands.processes
import pytest

from gosu.cmds.ci import get_version, git_num_changes
from gosu.cmds.python import (
    _get_editable_installs,
    _get_pkg_pyfiles,
    _manage_env_vars,
    _run,
)


@pytest.fixture
def chdir():
    saved_dir = os.getcwd()
    os.chdir("tests")
    yield
    os.chdir(saved_dir)


def test_run_env(chdir):
    _run("python", "-v")


def test_run_env_missing_command(chdir):
    with pytest.raises(plumbum.commands.processes.CommandNotFound):
        _run("missing")


def test_get_env_vars(chdir):
    e = _manage_env_vars()
    assert e["test"] == "1"


def test_get_pkg_pyfiles(chdir):
    e = _get_pkg_pyfiles()
    assert len(e) > 0


def test_get_version(chdir):
    assert get_version() != ""


def test_git_num_changes(chdir):
    assert git_num_changes() != ""


def test_get_editable_installs(chdir):
    assert _get_editable_installs()["something"] == "../something"

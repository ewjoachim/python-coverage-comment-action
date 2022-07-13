import os
import subprocess

import pytest

# In this directory, `gh` is not the global `gh` fixture, but is instead
# a fixture letting you use the `gh` CLI tool.


@pytest.fixture
def gh():
    def _(*args, token, json=True):
        call = subprocess.run(
            ["gh"] + args,
            text=True,
            check=True,
            capture_output=True,
            env={"GH_TOKEN": token, "NO_COLOR": "1"},
        )
        stdout = call.stdout
        if stdout and json:
            return json.loads(stdout)
        else:
            return stdout

    return _


@pytest.mark.skipif(
    "GITHUB_TOKEN_USER_1" not in os.environ,
    reason="requires GITHUB_TOKEN_USER_1 in environment variables",
)
@pytest.fixture
def token_user_1():
    return os.environ["GITHUB_TOKEN_USER_1"]


@pytest.mark.skipif(
    "GITHUB_TOKEN_USER_2" not in os.environ,
    reason="requires GITHUB_TOKEN_USER_2 in environment variables",
)
@pytest.fixture
def token_user_2():
    return os.environ["GITHUB_TOKEN_USER_2"]


@pytest.fixture
def gh_me(gh, token_user_1):
    def _(*args):
        gh(*args, token=token_user_1)

    return _


@pytest.fixture
def gh_other(gh, token_user_2):
    def _(*args):
        gh(*args, token=token_user_2)

    return _


@pytest.fixture
def git():
    # TODO same as gh, maybe make a common fixture "call"
    pass


@pytest.fixture
def cd(tmp_path):
    curdir = os.getcwd()

    def _(path):
        os.chdir(tmp_path / path)

    yield tmp_path
    os.chdir(curdir)


@pytest.fixture
def git_repo(cd, git):
    cd("repo")
    git("init")
    # TODO shutil.copytree to copy a static dir in the tests
    git("add", ".")
    git("commit", "-m", "...")  # Will need a name and email


@pytest.fixture
def gh_repo(gh_me, git_repo):
    gh_me("repo", "create", "--push")

    yield

    gh_me("repo", "delete", ...)


@pytest.fixture
def gh_fork(cd, gh_other, git_repo):
    cd("fork")
    gh_other("repo", "fork")

    yield

    gh_other("repo", "delete", ...)

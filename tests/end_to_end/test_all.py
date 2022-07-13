def test_push_main_branch(gh_repo, git, gh_me):
    sha1 = git("rev-parse", "HEAD")  # Could be a fixture
    while True:
        run = gh_me(
            "gh", "run", "list", "-b", "v2", "-L", "1", "--json", "databaseId,headSha"
        )
        if run and run[0]["headSha"] == sha1:
            break

    id = run[0]["databaseId"]

    gh_me("gh", "run", "watch", f"{id}")

    # Check the coverage badge. Maybe even extract its exact URL from the watch
    # command above.


def test_self_pr(gh_repo, git, gh_me):
    # TODO
    pass


def test_external_pr(gh_repo, git, gh_me, gh_other):
    # TODO
    pass

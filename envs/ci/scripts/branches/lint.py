"""This script checks that current branch satisfies our custom gitflow rules."""

import os
import subprocess
import sys


GITHUB_CURRENT_BRANCH = os.environ["GITHUB_CURRENT_BRANCH"]
GITHUB_DEFAULT_BRANCH = os.environ["GITHUB_DEFAULT_BRANCH"]


def main():
    errors = get_errors()
    if errors:
        print("Following errors were found:")
        for error in errors:
            print(f"  * {error}")
        sys.exit(1)
    print("No errors were found.")
    sys.exit(0)


def get_errors():
    """Run checkers and get error messages."""
    errors = []
    if not branch_rebased():
        errors.append("Branch is not rebased.")
    if not commits_squashed():
        errors.append("Commits are not squashed.")
    return errors


def branch_rebased():
    """Check that current branch is rebased to the last default branch."""
    cmd = subprocess.run(["git", "merge-base", "--fork-point", f"origin/{GITHUB_DEFAULT_BRANCH}"], capture_output=True)
    current_branch_fork_point = cmd.stdout.decode("utf-8").strip("\n")

    cmd = subprocess.run(["git", "rev-parse", f"origin/{GITHUB_DEFAULT_BRANCH}"], capture_output=True)
    default_branch_last_commit = cmd.stdout.decode("utf-8").strip("\n")

    return current_branch_fork_point == default_branch_last_commit


def commits_squashed():
    """Check that current branch has only one commit."""
    cmd = subprocess.run(["git", "cherry", f"origin/{GITHUB_DEFAULT_BRANCH}"], capture_output=True, encoding="utf-8")
    commits = cmd.stdout.strip("\n").split("\n")

    return len(commits) == 1


if __name__ == "__main__":
    main()

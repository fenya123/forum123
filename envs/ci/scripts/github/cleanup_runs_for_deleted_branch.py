"""This script cleans up GitHub old workflow runs for deleted branches.

There is no sense to keep these runs, because they are related to nonexistent commits from nonexistent branches.
Since runs of this workflow will remain after each deleted branch we want to clean them up as well, that's why
this script removes runs not only for deleted branches but also the old runs of this workflow. This means that we will
always have only one run of this workflow - the run for the most recent deleted branch.

This script is supposed to be run in GitHub workflow, which will provide environment variables we need.
"""

import os

from github import Github


GITHUB_EVENT_REF = os.environ["GITHUB_EVENT_REF"]  # full git ref of deleted branch, for example: 'refs/heads/main'
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]  # the owner and repository name, for example: 'octocat/Hello-World'
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]  # unique secret to authenticate in a workflow run, generated by GitHub

DELETED_BRANCH_NAME = GITHUB_EVENT_REF.split("/")[-1]


def main():
    repository = Github(GITHUB_TOKEN).get_repo(GITHUB_REPOSITORY)
    for run in repository.get_workflow_runs(branch=DELETED_BRANCH_NAME):
        run.delete()

    # clean up the old runs of this workflow as well
    for run in repository.get_workflow_runs(event="delete"):
        run.delete()


if __name__ == "__main__":
    main()

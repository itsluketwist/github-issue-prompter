import logging
import os

from openai import OpenAI

from github_issue_prompter.constants import PROMPTER_GITHUB_TOKEN, PROMPTER_OPENAI_TOKEN
from github_issue_prompter.github_gql import get_issue_list, get_repository_list
from github_issue_prompter.github_rest import comment_on_github_issue
from github_issue_prompter.status import check_issue_status
from github_issue_prompter.types import IssueCheckMode, PostCommentsOptions, Status


logger = logging.getLogger(__name__)


def prompt_issues(
    organisation: str,
    repository: str | None = None,
    github_token: str | None = None,
    mode: IssueCheckMode | str = IssueCheckMode.AI,
    prompt_count: int = 5,
    post_comments: PostCommentsOptions = PostCommentsOptions.NONE,
    only_assigned: bool = False,
    openai_token: str | None = None,
    **kwargs,
) -> None:
    """
    Query and check issue's for any that need prompting or are available to be worked on.

    Parameters
    ----------
    organisation : str
    repository : str | None = None
    github_token : str | None = None
    mode : IssueCheckMode = IssueCheckMode.AI
    prompt_count : int = 5
    post_comments : PostCommentsOptions = PostCommentsOptions.NONE
    only_assigned : bool = False
    openai_token : str | None = None
    **kwargs
    """
    logger.info(
        "Prompting issues for %s%s (mode: %s, prompt_count: %s, "
        "post_comments: %s, only_assigned: %s).",
        organisation,
        ("/" + repository) if repository else "",
        mode,
        prompt_count,
        post_comments,
        only_assigned,
    )

    mode = IssueCheckMode(mode)

    _github_token = github_token or os.getenv(PROMPTER_GITHUB_TOKEN)
    if _github_token is None:
        raise ValueError(
            "A GitHub API key must be passed in or assigned to "
            f"environment variable {PROMPTER_GITHUB_TOKEN}."
        )

    _openai_token = openai_token or os.getenv(PROMPTER_OPENAI_TOKEN)
    if _openai_token is None and mode == IssueCheckMode.AI:
        raise ValueError(
            "An OpenAI API key must be passed in or assigned to environment variable "
            f"{PROMPTER_OPENAI_TOKEN} when {IssueCheckMode.AI} mode is selected."
        )
    elif _openai_token:
        _status_client = OpenAI(api_key=_openai_token)
    else:
        _status_client = None

    if prompt_count <= 0:
        raise ValueError(
            f"Number of prompts must be a positive integer, given: {prompt_count}"
        )

    if not repository:
        # query repositories in the given org
        repos = get_repository_list(organisation=organisation, token=_github_token)
        logger.info(
            "Queried %s repositories from %s: %s",
            len(repos),
            organisation,
            repos,
        )
    else:
        repos = [repository]

    # per repository, query the issue's (and relevant data)
    issues = []
    for repo in repos:
        issues.extend(
            get_issue_list(
                organisation=organisation,
                repository=repo,
                token=_github_token,
            )
        )

    issues.sort(key=lambda i: i.created)  # prompt most recent issues first
    if only_assigned:
        # filter out unassigned issues if selected
        issues = [i for i in issues if i.assignees]

    logger.info("Queried %s potential issues to check for staleness.", len(issues))

    # process each issue one-by-one, making/printing a comment if it's stale
    issues_processed = 0
    for issue in issues:
        _status = check_issue_status(
            mode=mode,
            issue=issue,
            client=_status_client,
            **kwargs,
        )

        # process issue depending on it's status
        match _status.status:
            case Status.STALE | Status.FREE:
                posted = False

                if _status.comment is not None and (
                    post_comments == PostCommentsOptions.ALL
                    or (
                        post_comments == PostCommentsOptions.FREE
                        and _status.status == Status.FREE
                    )
                    or (
                        post_comments == PostCommentsOptions.STALE
                        and _status.status == Status.STALE
                    )
                ):
                    posted = comment_on_github_issue(
                        issue=issue,
                        comment=_status.comment,
                        token=_github_token,
                    )

                issues_processed += 1
                logger.info(
                    "Issue %s found to be %s:\n\treason   - %s\n\tcomment  - %s\n\tposted   - %s\n",
                    issue,
                    _status.status,
                    _status.reason,
                    _status.comment,
                    posted,
                )

            case Status.ACTIVE:
                logger.info("Issue %s is active.", issue)

            case Status.ERROR:
                logger.info(
                    "There was an error determining the status of issue %s.", issue
                )

            case _:
                raise NotImplementedError(
                    f"Unsupported issue Status found: {_status.status}"
                )

        if issues_processed == prompt_count:
            break

    logger.info(
        "Success! %s issues that can be worked on have been found%s.",
        issues_processed,
        " and commented on" if post_comments else "",
    )

import json
import logging

import requests

from github_issue_prompter.types import Issue


logger = logging.getLogger(__name__)


class GitHubCommentsAPIError(Exception):
    pass


def comment_on_github_issue(
    issue: Issue,
    comment: str,
    token: str,
    raise_errors: bool = False,
    timeout: int = 3,
) -> bool:
    """
    Use the GitHub Rest API to post a comment to an issue.

    Parameters
    ----------
    issue : Issue
    comment : str
    token : str
    raise_errors : bool = False
    timeout : int = 3

    Returns
    -------
    bool
        True if the comment was posted to the issue successfully, False otherwise.
    """
    logger.debug("Posting comment on GitHub Issue %s: %s", issue, comment)

    response = requests.post(
        url=f"https://api.github.com/repos/{issue}/comments",
        headers={"Authorization": f"Bearer {token}"},
        data=json.dumps({"body": comment}),
        timeout=timeout,
    )

    if response.status_code not in [200, 201]:
        error_message = (
            f"Failed to comment on GitHub issue via the Rest API, "
            f"returning code: {response.status_code}. "
            f"Issue: {issue}, comment: {comment}"
        )
        if raise_errors:
            raise GitHubCommentsAPIError(error_message)
        else:
            logger.error(error_message)
            return False

    data = response.json()

    if "errors" in data and len(data["errors"]) > 0:
        error_message = (
            f"GitHub Rest API returned errors: {data['errors']}. "
            f"Issue: {issue}, comment: {comment}"
        )
        if raise_errors:
            raise GitHubCommentsAPIError(error_message)
        else:
            logger.error(error_message)
            return False

    logger.debug("GitHub comment post successful, received: %s", data)
    return True

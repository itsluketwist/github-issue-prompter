from datetime import datetime, timedelta

from github_issue_prompter.types import Issue, IssueCheckMode, IssueStatus, Status


def check_issue_status(
    mode: IssueCheckMode,
    issue: Issue,
    **kwargs,
) -> IssueStatus:
    """
    Check whether an issue's status, and whether it needs prompting.

    Use different StatusModes to configure the exact logic used for checking.

    Parameters
    ----------
    mode : IssueCheckMode
    issue : Issue
    **kwargs
        Method specific arguments for usage depending on the chosen mode.

    Returns
    -------
    IssueStatus
        An object detailing the current status of the issue, along with a reason
        and a comment that can be used to prompt the issue.
    """
    match mode:
        case IssueCheckMode.SIMPLE:
            return _check_simple(issue=issue, **kwargs)
        case IssueCheckMode.AI:
            return _check_ai(issue=issue, **kwargs)
        case _:
            raise NotImplementedError(
                f"Unsupported IssueCheckMode was provided: {mode}"
            )


def _check_simple(issue: Issue, **_) -> IssueStatus:
    """
    Determine whether an Issue is stale or active, using simple criteria depending on whether the
    issue is assigned, and whether it has any comments, and when it was last updated.

    Parameters
    ----------
    issue
        Object detailing all necessary issue information to check its status.
    **_
        Unused kwargs.

    Returns
    -------
    IssueStatus
        An object detailing the current status of the issue, along with a reason
        and a comment that can be used to prompt the issue.
    """
    if issue.assignees and issue.comments:
        # prompt assigned issue's if there hasn't been a comment in 2 weeks
        two_weeks_ago = datetime.now() - timedelta(days=14)
        if issue.comments and issue.comments[0].updated < two_weeks_ago:
            return IssueStatus(
                status=Status.STALE,
                reason="The issue is assigned, but hasn't had a comment in 2 weeks.",
                comment=f"Hey {issue.assignees_str}, I noticed this issue didn't seem to "
                f"have any comments recently, and wondered if it was still "
                f"actively being worked on or if I could take a look?",
            )

    elif issue.comments:
        # prompt unassigned issue with comments if there hasn't been a comment in 1 week
        one_week_ago = datetime.now() - timedelta(days=7)
        if issue.comments[0].updated < one_week_ago:
            return IssueStatus(
                status=Status.STALE,
                reason="The issue is assigned, but hasn't had a comment in 2 weeks.",
                comment=f"Hey @{issue.author}, I noticed this issue didn't seem to have "
                f"any progress, and wondered if it was available for me to "
                f"look into?",
            )

    elif issue.assignees:
        # prompt assigned issue without comments if there hasn't been an update in 3 weeks
        three_weeks_ago = datetime.now() - timedelta(days=21)
        if issue.updated < three_weeks_ago:
            return IssueStatus(
                status=Status.STALE,
                reason="The issue is assigned and has no comments, but hasn't "
                "been updated in 3 weeks.",
                comment=f"Hey {issue.assignees_str}, I noticed this issue didn't seem "
                f"to have been updated recently, and wondered if it was still "
                f"actively being worked on or if I could take a look?",
            )

    else:
        # unassigned and no comments == not stale, free to pick up and work on
        return IssueStatus(
            status=Status.FREE,
            reason="The issue is unassigned and has no comments.",
            comment=f"Hey @{issue.author}, mind if I take on this issue?",
        )

    # otherwise issue is deemed to be actively worked on
    return IssueStatus(status=Status.ACTIVE)


def _check_ai(issue: Issue, openai_token: str, **_) -> IssueStatus:
    raise NotImplementedError("Not done yet...")

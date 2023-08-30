import logging
from typing import Any, Dict, List, Optional, Set

import requests

from github_issue_prompter.types import Issue, IssueComment


logger = logging.getLogger(__name__)


class GitHubError(Exception):
    pass


def query_graphql(
    query: str,
    token: str,
    timeout: int = 5,
) -> Dict[str, Any]:
    """
    Perform a GitHub GraphQL query, handling any errors and returning the result.

    Parameters
    ----------
    query : str
    token : str
    timeout : str = 5

    Returns
    -------
    Dict[str, Any]
        The queried data.
    """
    logger.debug("Querying GitHub GraphQL: %s", query)
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query},
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        timeout=timeout,
    )

    if response.status_code != 200:
        raise GitHubError(
            f"GitHub GraphQL query failed to run, returning code: {response.status_code}. "
            f"Query: {query}"
        )

    data = response.json()

    if "errors" in data and len(data["errors"]) > 0:
        raise GitHubError(
            f"GitHub GraphQL query returned errors: {data['errors']}. Query: {query}"
        )

    logger.debug("GitHub GraphQL query successful, received: %s", data)
    return data["data"]


def get_repository_list(
    owner: str,
    token: str,
) -> List[str]:
    """
    Query a list of repositories for a given GitHub user/organisation (the owner).

    Parameters
    ----------
    owner : str
    token : str

    Returns
    -------
    List[str]
        The list of owned repositories.
    """
    logger.debug("Querying GitHub GraphQL API for %s's repositories.", owner)
    has_next_page = True
    cursor: Optional[str] = None
    data: Set[str] = set()

    while has_next_page:
        # build the query
        cursor_arg = f'after: "{cursor}"' if cursor else ""
        query = f"""
            {{
                owner: repositoryOwner(login: "{owner}") {{
                    repositories(
                        first: 100
                        ownerAffiliations: OWNER
                        privacy: PUBLIC
                        isFork: false
                        isLocked: false
                        {cursor_arg}
                    ) {{
                        nodes {{
                            name
                        }}

                        pageInfo {{
                            hasNextPage
                            endCursor
                        }}
                    }}
                }}
            }}
        """

        next_result = query_graphql(query=query, token=token)

        data.update([r["name"] for r in next_result["owner"]["repositories"]["nodes"]])
        has_next_page = next_result["owner"]["repositories"]["pageInfo"]["hasNextPage"]
        cursor = next_result["owner"]["repositories"]["pageInfo"]["endCursor"]

    return list(data)


def get_issue_list(
    owner: str,
    repository: str,
    token: str,
) -> List[Issue]:
    """
    Query a list of issues for a given GitHub repository.

    Parameters
    ----------
    owner : str
    repository : str
    token : str

    Returns
    -------
    List[Issue]
        The list of issues for the repository.
    """
    logger.debug(
        "Querying GitHub GraphQL API for issues in repository %s/%s.", owner, repository
    )
    has_next_page = True
    cursor: Optional[str] = None
    data: List[Issue] = []

    while has_next_page:
        # build the query
        cursor_arg = f'after: "{cursor}"' if cursor else ""
        query = f"""
            {{
                repository(name:"{repository}", owner: "{owner}") {{
                    issues(
                        first: 50
                        states: OPEN
                        {cursor_arg}
                    ) {{
                        nodes {{
                            number
                            title
                            bodyText
                            createdAt
                            lastEditedAt

                            assignees(
                                first: 10
                            ) {{
                                nodes {{
                                    login
                                }}
                            }}

                            comments(
                                first: 5
                                orderBy: {{field: UPDATED_AT, direction: DESC}}
                            ) {{
                                nodes {{
                                    author {{
                                        login
                                    }}
                                    body
                                    updatedAt
                                }}
                            }}
                        }}

                        pageInfo {{
                            hasNextPage
                            endCursor
                        }}
                    }}
                }}
            }}
        """

        next_result = query_graphql(query=query, token=token)

        for issue in next_result["repository"]["issues"]["nodes"]:
            data.append(
                Issue(
                    owner=owner,
                    repository=repository,
                    number=issue["number"],
                    title=issue["title"],
                    body=issue["bodyText"],
                    created=issue["createdAt"],
                    edited=issue["lastEditedAt"],
                    assignees=[_a["login"] for _a in issue["assignees"]["nodes"]],
                    comments=[
                        IssueComment(
                            author=_c["author"]["login"],
                            body=_c["body"],
                            updated=_c["updatedAt"],
                        )
                        for _c in issue["comments"]["nodes"]
                    ],
                )
            )

        has_next_page = next_result["repository"]["issues"]["pageInfo"]["hasNextPage"]
        cursor = next_result["repository"]["issues"]["pageInfo"]["endCursor"]

    return data

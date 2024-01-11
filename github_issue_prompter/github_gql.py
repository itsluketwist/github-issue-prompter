import logging
from datetime import datetime
from typing import Any

import requests

from github_issue_prompter.types import Issue, IssueComment


logger = logging.getLogger(__name__)


class GitHubGraphQLError(Exception):
    pass


def _parse_datetime(_datetime: str) -> datetime:
    """
    Parse a GraphQL datetime string (in ISO-8601 format).

    Parameters
    ----------
    _datetime : str

    Returns
    -------
    datetime
    """
    return datetime.strptime(_datetime, "%Y-%m-%dT%H:%M:%SZ")


def query_graphql(
    query: str,
    token: str,
    timeout: int = 5,
) -> dict[str, Any]:
    """
    Perform a GitHub GraphQL query, handling any errors and returning the result.

    Parameters
    ----------
    query : str
    token : str
    timeout : str = 5

    Returns
    -------
    dict[str, Any]
        The queried data.
    """
    logger.debug("Querying GitHub GraphQL: %s", query)
    response = requests.post(
        url="https://api.github.com/graphql",
        json={"query": query},
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        timeout=timeout,
    )

    if response.status_code not in [200, 201]:
        raise GitHubGraphQLError(
            f"GitHub GraphQL query failed to run, returning code: {response.status_code}. "
            f"Query: {query}"
        )

    data = response.json()

    if "errors" in data and len(data["errors"]) > 0:
        raise GitHubGraphQLError(
            f"GitHub GraphQL query returned errors: {data['errors']}. Query: {query}"
        )

    logger.debug("GitHub GraphQL query successful, received: %s", data)
    return data["data"]


def get_repository_list(
    organisation: str,
    token: str,
) -> list[str]:
    """
    Query a list of repositories for a given GitHub user/organisation (the owner).

    Parameters
    ----------
    organisation : str
    token : str

    Returns
    -------
    list[str]
        The list of owned repositories.
    """
    logger.debug(
        "Querying GitHub GraphQL API for %s's repositories.",
        organisation,
    )
    has_next_page = True
    cursor: str | None = None
    data: set[str] = set()

    while has_next_page:
        # build the query
        cursor_arg = f'after: "{cursor}"' if cursor else ""
        query = f"""
            {{
                org: repositoryOwner(login: "{organisation}") {{
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

        # extract data from the result
        data.update([r["name"] for r in next_result["org"]["repositories"]["nodes"]])
        has_next_page = next_result["org"]["repositories"]["pageInfo"]["hasNextPage"]
        cursor = next_result["org"]["repositories"]["pageInfo"]["endCursor"]

    return list(data)


def get_issue_list(
    organisation: str,
    repository: str,
    token: str,
) -> list[Issue]:
    """
    Query a list of issues for a given GitHub repository.

    Parameters
    ----------
    organisation : str
    repository : str
    token : str

    Returns
    -------
    list[Issue]
        The list of issues for the repository.
    """
    logger.debug(
        "Querying GitHub GraphQL API for issues in repository %s/%s.",
        organisation,
        repository,
    )

    has_next_page = True
    cursor: str | None = None
    data: list[Issue] = []

    while has_next_page:
        # build the query
        cursor_arg = f'after: "{cursor}"' if cursor else ""
        query = f"""
            {{
                repository(name:"{repository}", owner: "{organisation}") {{
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
                            updatedAt

                            author {{
                                login
                            }}

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

        # extract data from the result
        for issue in next_result["repository"]["issues"]["nodes"]:
            data.append(
                Issue(
                    organisation=organisation,
                    repository=repository,
                    number=issue["number"],
                    title=issue["title"],
                    author=issue["author"]["login"],
                    body=issue["bodyText"],
                    created=_parse_datetime(issue["createdAt"]),
                    updated=_parse_datetime(issue["updatedAt"]),
                    assignees=[_a["login"] for _a in issue["assignees"]["nodes"]],
                    comments=[
                        IssueComment(
                            author=_c["author"]["login"],
                            body=_c["body"],
                            updated=_parse_datetime(_c["updatedAt"]),
                        )
                        for _c in issue["comments"]["nodes"]
                    ],
                )
            )

        has_next_page = next_result["repository"]["issues"]["pageInfo"]["hasNextPage"]
        cursor = next_result["repository"]["issues"]["pageInfo"]["endCursor"]

    return data

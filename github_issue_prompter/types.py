from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class IssueComment:
    author: str
    body: str
    updated: datetime


@dataclass
class Issue:
    owner: str
    repository: str
    number: int
    title: str
    body: str
    created: datetime
    edited: datetime
    assignees: List[str]
    comments: List[IssueComment]

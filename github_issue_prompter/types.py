from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class _StrEnum(Enum):
    """Extension of an Enum with conveniences for usage with string values."""

    def __str__(self):
        return self.value

    @classmethod
    def from_str(cls, string: str):
        return cls(string.lower())


class IssueCheckMode(_StrEnum):
    SIMPLE = "simple"
    AI = "ai"


class PostCommentsOptions(_StrEnum):
    NONE = "none"
    STALE = "stale"
    FREE = "free"
    ALL = "all"


class Status(_StrEnum):
    ACTIVE = "active"
    STALE = "stale"
    FREE = "free"
    ERROR = "error"


@dataclass
class IssueStatus:
    """Class to store information about the current status of an issue."""

    status: Status
    reason: str | None = None
    comment: str | None = None


@dataclass
class IssueComment:
    """Class to store information about a GitHub issue comment."""

    author: str
    body: str
    updated: datetime


@dataclass
class Issue:
    """Class to store information about a GitHub issue."""

    organisation: str
    repository: str
    number: int
    title: str
    author: str
    body: str
    created: datetime
    updated: datetime
    assignees: list[str]
    comments: list[IssueComment]

    def __repr__(self) -> str:
        # matches the url part of an issue
        return f"{self.organisation}/{self.repository}/issues/{self.number}"

    @property
    def assignees_str(self):
        return ", ".join([f"@{_a}" for _a in self.assignees])

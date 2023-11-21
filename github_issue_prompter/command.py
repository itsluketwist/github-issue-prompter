import logging
import os
from argparse import ArgumentParser

from github_issue_prompter.constants import (
    PROMPTER_GITHUB_TOKEN,
    PROMPTER_LOG_LEVEL,
    PROMPTER_OPENAI_TOKEN,
)
from github_issue_prompter.prompter import prompt_issues
from github_issue_prompter.status import IssueCheckMode


# some basic config for logging to the terminal
logging.basicConfig(
    format="%(levelname)-8s : %(name)s - %(message)s",
    level=os.getenv(PROMPTER_LOG_LEVEL, logging.INFO),
)


# build main parser
parser = ArgumentParser(
    prog="prompt",
    description="Prompt stale issue's in a repository or organisation.",
)


# add the arguments of `prompt_issues`
parser.add_argument(
    "organisation",
    help="The GitHub user or organisation.",
)
parser.add_argument(
    "-r",
    "--repository",
    type=str,
    default=None,
    help="The repository to prompt, if None will prompt all repositories under the given owner.",
)
parser.add_argument(
    "-t",
    "--token",
    type=str,
    default=None,
    help="The GitHub API token to use when querying or making comments. "
    f"If None will default to {PROMPTER_GITHUB_TOKEN}.",
)
parser.add_argument(
    "-o",
    "--openai-token",
    type=str,
    default=None,
    help="The OpenAI API token to use (if mode is set to ai). "
    f"If None will default to {PROMPTER_OPENAI_TOKEN}.",
)
parser.add_argument(
    "-m",
    "--mode",
    type=IssueCheckMode,
    choices=list(IssueCheckMode),
    default=IssueCheckMode.SIMPLE,
    help="How to determine if an issue is stale.",
)
parser.add_argument(
    "-c",
    "--prompt-count",
    type=int,
    default=5,
    help="How many issue's should be prompted.",
)
parser.add_argument(
    "-p",
    "--post-comments",
    action="store_true",
    help="Whether to actually post the comments to the GitHub "
    "issues, or to simply print them to the terminal.",
)
parser.add_argument(
    "-a",
    "--only-assigned",
    action="store_true",
    help="Whether to only prompt issue's that are assigned.",
)


def main():
    """Check and prompt some issues!"""
    args = parser.parse_args()
    kwargs = vars(args)
    prompt_issues(**kwargs)

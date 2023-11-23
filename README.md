# *github-issue-prompter*

It can be hard to sift through GitHub issues, especially when they seem to look busy or appear in limbo. 

This python utility analyses GitHub issues, finding those that are free to work on (even if they look busy at a first 
glance), and suggesting comments to prompt the issue if it seems stale, or offer your hand at solving it.
Taking the stress out of sifting through issues yourself!

![check code workflow](https://github.com/itsluketwist/github-issue-prompter/actions/workflows/check.yaml/badge.svg)

<div>
    <!-- badges from : https://shields.io/ -->
    <!-- logos available : https://simpleicons.org/ -->
    <a href="https://opensource.org/licenses/MIT">
        <img alt="MIT License" src="https://img.shields.io/badge/Licence-MIT-C10606?style=for-the-badge&logo=docs&logoColor=white" />
    </a>
    <a href="https://www.python.org/">
        <img alt="Python 3" src="https://img.shields.io/badge/Python_3-37709F?style=for-the-badge&logo=python&logoColor=white" />
    </a>
    <a href="https://openai.com/blog/openai-api">
        <img alt="OpenAI API" src="https://img.shields.io/badge/OpenAI_API-412991?style=for-the-badge&logo=openai&logoColor=white" />
    </a>
    <a href="https://docs.github.com/en/graphql">
        <img alt="GitHub GraphQL API" src="https://img.shields.io/badge/GitHub_GraphQL_API-181717?style=for-the-badge&logo=github&logoColor=white" />
    </a>
</div>

## *installation*

Install directly from GitHub, using pip:

```shell
pip install git+https://github.com/itsluketwist/github-issue-prompter
```

## *usage*

You can search for issue's across an organisation, or in a single repository. Results will be displayed along with 
suggested comments to get started, or you can use the `post_comments` argument to have comments posted automatically!

Once installed, you can either use the command line and the `prompt` command, with your desired arguments:

```shell
prompt -h

prompt pytorch -r pytorch
```

Or you can import and call the script via python:

```python
from github_issue_prompter import prompt_issues

prompt_issues(
    organisation="pytorch",
    repository="pytorch",
)
```

You need a GitHub personal access token from your GitHub account in order to use this library, 
you can find out how to get one 
[here](https://docs.github.com/en/enterprise-server@3.6/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

You can then either assign the token to the environment variable `PROMPTER_GITHUB_TOKEN` for automatic usage, 
or pass the token in directly.

## *development*

Clone the repository code:

```shell
git clone https://github.com/itsluketwist/github-issue-prompter.git
```

Once cloned, install the package locally in a virtual environment:

```shell
python -m venv venv

. venv/bin/activate

pip install -e ".[dev]"
```

Install and use pre-commit to ensure code is in a good state:

```shell
pre-commit install

pre-commit run --all-files
```


## *testing*

(todo...) Run the test suite using:

```shell
pytest .
```


## *release*

(todo...) We release to pypi...


## *inspiration*

When starting to get into open source, I found that quite a lot of issues where in uncertain states. 
Either assigned but seemingly inactive, or maybe unassigned but with comments implying someone might be working on it. 
This sometimes made it hard to find suitable issue's to get started on, and I figured it would be convenient to have 
an automatic tool to scan for these issue's and prompt the assignees/maintainers to clear up the status.

## *todo*

- add/upload to pypi
- implement some tests
- more detailed docs/use-cases

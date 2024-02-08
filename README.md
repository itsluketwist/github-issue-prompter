# *github-issue-prompter*

Use AI to find GitHub issue's that you can work on (even if the issue's appear active)!

![check code workflow](https://github.com/itsluketwist/github-issue-prompter/actions/workflows/check.yaml/badge.svg)
![release workflow](https://github.com/itsluketwist/github-issue-prompter/actions/workflows/release.yaml/badge.svg)

<div>
    <!-- badges from : https://shields.io/ -->
    <!-- logos available : https://simpleicons.org/ -->
    <a href="https://opensource.org/licenses/MIT">
        <img alt="MIT License" src="https://img.shields.io/badge/Licence-MIT-C10606?style=for-the-badge&logo=docs&logoColor=white" />
    </a>
    <a href="https://www.python.org/">
        <img alt="Python 3.10+" src="https://img.shields.io/badge/Python_3.10+-37709F?style=for-the-badge&logo=python&logoColor=white" />
    </a>
    <a href="https://openai.com/blog/openai-api">
        <img alt="OpenAI API" src="https://img.shields.io/badge/OpenAI_API-412991?style=for-the-badge&logo=openai&logoColor=white" />
    </a>
    <a href="https://docs.github.com/en/graphql">
        <img alt="GitHub GraphQL API" src="https://img.shields.io/badge/GitHub_GraphQL_API-181717?style=for-the-badge&logo=github&logoColor=white" />
    </a>
</div>

## *about*

It can be hard to sift through open GitHub issues, especially when they seem to look busy or appear in limbo. 
This python utility uses AI to analyse GitHub issues, finding those that are free to work on (even if they 
look busy/taken at a first glance), and suggests comments to prompt the issue if it seems stale, or to offer 
your hand at solving it. Taking the stress out of sifting through issues yourself!

## *installation*

Install directly from PyPI using pip:

```shell
pip install github-issue-prompter
```

## *tokens*

You need a GitHub personal access token and an OpenAI API token (to use the AI functionality).
You can store them in `PROMPTER_GITHUB_TOKEN` and `PROMPTER_OPENAI_TOKEN` environment variables,
or pass them in as arguments.

Instructions for how to get a GitHub personal access token from your GitHub account available 
[here](https://docs.github.com/en/enterprise-server@3.6/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

Instructions for how to get an OpenAI API token available 
[here](https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key).


## *usage*

You can search for issue's across an organisation, or in a single repository. 
Results will be displayed along with suggested comments to get started, or you can use the `post_comments` 
argument to have comments posted automatically!

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

If you don't have access to the OpenAI API, or just want more basic functionality, you can use the `-s`/`--simple`
command line argument, or the `mode="simple"` keyword argument.

## *development*

Fork and clone the repository code:

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

pre-commit autoupdate

pre-commit run --all-files
```


## *testing*

(todo...) Run the test suite using:

```shell
pytest .
```


## *inspiration*

When getting into open source, I found that plenty of issues where in uncertain states. Either assigned but seemingly 
inactive, or unassigned but with comments implying someone might be working on it. This made it hard to find suitable 
issue's to get started on, and I figured it would be convenient to have an automatic tool to scan for these issue's 
and prompt the assignees/maintainers to clear up the status.

## *todo*

- implement some tests
- expand use-cases and instructions above
- all api prompt config/options

# *github-issue-prompter*

A python utility to find and prompt stale GitHub issues that may be available to work on.

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
</div>

## *todo*

- add/upload to pypi
- add to docs (mainly usage)
- prompt options, only stale, or available too..?

## *installation*

Install directly from GitHub, using pip:

```shell
pip install git+https://github.com/itsluketwist/github-issue-prompter
```

## *usage*

There are ...

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

Run the test suite using:

```shell
pytest .
```


## *release*

We release to pypi, by running...


## *inspiration*

When starting to get into open source, I found that quite a lot of issues where in uncertain states. 
Either assigned but seemingly inactive, or maybe unassigned but with comments implying someone might be working on it. 
This sometimes made it hard to find suitable issue's to get started on, and I figured it would be convenient to have 
an automatic tool to scan for these issue's and prompt the assignees/maintainers to clear up the status.

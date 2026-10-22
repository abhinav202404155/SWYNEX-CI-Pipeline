# SWYNEX-CI-Pipeline

![CI](https://github.com/abhinav202404155/SWYNEX-CI-Pipeline/actions/workflows/ci.yml/badge.svg)

A small command line expense tracker written in Python. I built it as Task 2 of my
SWYNEX Technologies internship, and the main goal was to set up a proper
continuous integration pipeline with GitHub Actions around it.

## What the pipeline does

The workflow lives in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) and runs on
every push and pull request to `main`. It has three jobs that run one after another:

1. **lint** - runs `ruff check` to catch unused imports, style issues and plain mistakes.
2. **test** - runs the pytest suite on Python 3.9, 3.11 and 3.12 and prints coverage.
3. **build** - builds the wheel and source distribution and uploads them as an artifact.

If lint fails, tests do not run. If tests fail, nothing gets built. That way a broken
commit is caught at the earliest step.

## The app

```
expense-tracker add 250 travel --note "bus pass"
expense-tracker add 80 food
expense-tracker summary
```

Expenses are stored in a local `expenses.json` file (use `--file` to change it).

## Running things locally

```
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pip install -e .

ruff check .
pytest
python -m build
```

## Project layout

```
src/expense_tracker/   application code
tests/                 pytest tests
.github/workflows/     CI workflow
pyproject.toml         package, pytest and ruff config
```

## Things I learned

- Splitting the workflow into separate jobs with `needs` makes the Actions page much
  easier to read when something breaks.
- A test matrix is cheap and showed me which Python versions the code really works on.
- Caching pip downloads (`cache: pip`) noticeably cut the run time.

## Author

Abhinav Kashyap - [@abhinav202404155](https://github.com/abhinav202404155)

# Development workflow

The repository uses short-lived feature branches and a single long-lived branch: `main`.
Historical work is preserved by merged or closed pull requests and by files under `archive/`; old feature branches are not part of the archival strategy.

## Branch lifecycle

1. Start from an up-to-date `main`.
2. Create one narrowly scoped branch for one scientific, documentation, or infrastructure change.
3. Open a pull request early enough that CI and the scientific assumptions are visible.
4. Merge only after the required checks pass.
5. Delete the remote feature branch after merge or after the work is explicitly superseded.
6. Prune local remote-tracking refs.

Recommended branch prefixes are `feature/`, `fix/`, `paper/`, `data/`, and `chore/`. Prefer names such as `data/barchart-cl-curve` or `paper/jfm-results` over long-lived catch-all branches.

Do not reuse an old merged branch for new work. A follow-up change starts from current `main` in a new branch.

## Canonical local workflow

```bash
git switch main
git pull --ff-only origin main
git switch -c feature/short-description
```

Run the repository checks before opening or updating a pull request:

```bash
python -m scripts.check_repo_structure
python paper/build.py --check
python -m pytest -q
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

After the pull request is merged:

```bash
git switch main
git pull --ff-only origin main
git fetch --prune
```

Delete the merged remote branch if GitHub did not delete it automatically:

```bash
git push origin --delete <branch-name>
```

On PowerShell the same command is used. Delete a local branch only after confirming that its pull request was merged or intentionally superseded:

```powershell
git branch -d <branch-name>
git fetch --prune
```

Use `git branch -D` only for a branch that was intentionally abandoned/superseded and whose useful work is already preserved elsewhere.

## What belongs where

- reusable scientific implementation: `bayesian_asian_options/src/bayesian_asian_options/`;
- experiment orchestration: `experiments/`;
- workstation/repository utilities: `scripts/`;
- tests: `tests/`;
- empirical source data and provenance: `data/`;
- generated experiment outputs: `results/`;
- active JFM manuscript: `paper/manuscript/`;
- methodological design notes: `research/`;
- superseded notebooks, manuscripts, presentations, and outputs: `archive/`.

Do not create new top-level folders when an existing domain directory already fits the artifact.

## Current empirical source contract

The current WTI APO pilot intentionally separates data roles:

- Barchart APO histories under `data/csv/` are the external option-price benchmark;
- Barchart individual CL histories under `data/csv/CL/` provide the valuation-date futures curve and contractual first-nearby fixing levels;
- `data/csv/CL/contract_expiries.csv` provides explicit CL last-trade dates;
- Yahoo `CL=F` is used only as a labelled continuous/front-month proxy for physical-measure volatility inference;
- U.S. Treasury daily par-yield data provide date-specific discounting under the documented pilot approximation.

Do not silently replace one of these objects with another source merely because the ticker or price series looks similar.

## Pull-request scope

A pull request should normally contain one coherent change. Public library functionality requires implementation, scientific docstrings/type hints, tests, and Sphinx API documentation in the same PR. Empirical numerical claims require a traceable experiment configuration, source provenance, seed where relevant, and code commit.

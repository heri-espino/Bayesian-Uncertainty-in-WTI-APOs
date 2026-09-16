# Contributing

This is a research repository with scientific and reproducibility constraints. Read `AGENTS.md` before changing code, data workflows, or the manuscript.

The canonical contributor workflow is documented in `docs/development.md`.

In short:

1. branch from current `main`;
2. keep the branch narrowly scoped;
3. preserve the P/Q separation and WTI APO contract mechanics;
4. add tests and Sphinx documentation with public library APIs;
5. run the required repository, manuscript, pytest, and Sphinx checks;
6. merge through a pull request;
7. delete the feature branch after merge or explicit supersession.

Do not use old merged branches as persistent development lines. Pull requests and `archive/` preserve history; `main` is the only long-lived branch.

For market data, preserve source provenance and verify redistribution rights before making raw third-party files public.

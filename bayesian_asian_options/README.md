# Python library boundary

All reusable scientific logic belongs in `src/bayesian_asian_options/`.

Install the repository from its root with:

```bash
python -m pip install -e .
```

Experiment drivers, manuscript code, one-off data conversions, and generated results do
not belong in this package. See the root `AGENTS.md` and `docs/architecture.md` before
adding modules.

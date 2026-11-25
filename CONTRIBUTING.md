# Contributing

Pull requests are welcome when they improve testable, reproducible research behavior.

1. Set up `python -m pip install -e '.[dev]'`.
2. Add an offline test reproducing the issue or covering the new behavior.
3. Run `ruff check src tests examples` and `pytest -q`.
4. Document any change to economic assumptions, data sources, public APIs, or CLI output in `docs/methodology.md` and `CHANGELOG.md`.
5. Do not replace or rewrite the frozen historical CANSIM data. A cleaned derivative should have a new name and documented transformation.
6. Tests must not depend on external network, private credentials or live table availability.

Model correctness and statistical validity are separate responsibilities; a numerically reproducible result does not make an underlying selection of historical vectors economically defensible. Any proposed canonical series selection needs source metadata and documented scope, price basis, units, reference period, and revisions.

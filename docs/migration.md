# Migration from the experimental EconCan repository

The original project combined two partially formed namespaces (`econcan` and `econcore`), legacy workflows, exploratory scripts, table definitions and stubs. Its `pyproject.toml` identified the distribution as `statcan` and required Python 3.14, while `README.md` contained only a heading. Legacy calculations frequently relied on positional columns, ambiguous dictionary/set representations, hard-coded CANSIM IDs and unchecked imports.

## Preserved material

Everything under the original `src/` is kept under `archive/econcan-original/src/` for further archaeology: prior attempts at fetching tables, domain-specific vector lists, historical workflow code, and exploratory graphics. The original package metadata, lockfile, README and gitignore are in `archive/econcan-original/`.

All three originally supplied CANSIM CSV files are unchanged in `data/legacy/`:

- `dataset_can_cansim5245628780870031920.csv`: a historical monthly manufacturing GDP export with a `Monthly,v...` heading. The new `legacy-series` CLI can read the two vectors listed in its header.
- `dataset_can_cansim7931814471809016759.csv`: a historical, legend-heavy matrix of fixed-capital-formation values with an unusual delimiter/row layout. Retained intact, **not** treated as a modern full-table download.
- `dataset_can_cansim8448814858763853126.csv`: a historical, legend-heavy inventory investment matrix. Retained intact, **not** parsed by the modern client.

The previous directory layout and empty files were not retained as live modules, deliberately: importing the package must not trigger I/O or plotting, and experimental code must not masquerade as a supported API.

## New entry points

| Original idea | New supported interface |
| --- | --- |
| `econcan.providers.statcan.provider.StatCanProvider` | `canprod.statcan.StatCanClient` (current named-header ZIP format) |
| `econcan.connectors.statcan.DatasetDefinition` | `canprod.statcan.SeriesSpec` with explicit aggregation |
| Multiple ad-hoc `BLUEPRINT_*` sets | `canprod.workflow.ProductionSpec.from_file` |
| `econcan.funcs.combine_can(...)` | `canprod.workflow.build_production_frame(...)` |
| `econcan.models.cobb_douglas.transform_cobb_douglas` | `canprod.model.fit_cobb_douglas` |
| Global `plt.show()` scripts | `canprod.plot.save_fit_plot` / `canprod fit --plot` |
| `some_read_stockpile.py` monthly reader | `canprod.legacy.legacy_annual_series` |

There is no guarantee of API compatibility. Prior code is preserved in the archive but **not** put on the new import path.

## Specific legacy issues corrected

- `cobb_douglas_can.py` called an undefined `get_fig_map` and invoked the plotter with incompatible arguments.
- The original `get_blueprint()` returned a set of definitions, while `combine_can()` treated its input as a dictionary keyed by table IDs. An economic blueprint therefore could not be replayed reliably.
- `capital.py` and `labour.py` contained module-level data acquisition/plotting; importing them performed work and could fail.
- `funcs.py` redefined `pull_can_capital`, included interpolated SQL and relied on positional data and unknown local database state.
- The StatCan provider used positional CSV field indexes and wrote Parquet without an explicit compatible dependency or data-layout guarantee.
- Source CSV exports had heterogeneous, legacy layouts that cannot be safely parsed by an ordinary `read_csv` without schema-specific handling.

The new code is a deliberately smaller supported core; researchers can extract useful vector lists from the archive and promote them to **verified** specs with source metadata. Do not automatically carry over legacy study conclusions.

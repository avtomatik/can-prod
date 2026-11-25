# CanProd

**Canadian Production & Productivity Research** · Python 3.11+ · MIT

CanProd is a research-oriented toolkit for building transparent Canadian capital–labour–output datasets from Statistics Canada public tables and estimating Cobb–Douglas production functions. It replaces a collection of experimental EconCan scripts with a tested package, a small command-line interface, explicit economic assumptions, and provenance-oriented exports.

> **Research status:** The software pipeline and offline demonstration are tested. The bundled historical exports are real archived data; the demonstration production dataset is **synthetic**. The project does **not** ship a validated, harmonized modern Canadian capital/labour/output series selection. Users must check definitions, base years, sector coverage, price concepts, frequencies, and source revisions before drawing economic conclusions. No claim of causal identification is made.

## Quick start: offline model demonstration

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e '.[plot]'

canprod fit \
  --input examples/synthetic_production.csv \
  --base-year 2012 \
  --returns-to-scale constant \
  --outdir outputs/demo \
  --plot
```

On Windows, run the command on one line instead of using backslash line continuations. The package also supports `python -m canprod` wherever `canprod` appears.

This creates:

- `outputs/demo/fitted_observations.csv`: original (or base-year-normalized) capital, labour, output, prediction, and residuals by year;
- `outputs/demo/fit_metrics.json`: machine-readable elasticities, scale, R² (levels and logs), MAE, RMSE, observation count, and modelling mode;
- `outputs/demo/cobb_douglas_fit.png`: non-interactive model fit chart (requires `[plot]`).

To allow free returns to scale, use `--returns-to-scale free`. No base-year normalization happens unless `--base-year` is specified.

## Use your own annual production data

Provide a CSV with the exact column names below, where values are **positive**, **numeric**, and **economically compatible**. Year must be a unique calendar year.

```csv
year,capital,labour,output
2012,100,85,125
2013,104,87,130
2014,109,88,136
2015,111,89,139
2016,116,91,145
```

```bash
canprod fit --input path/to/production.csv --outdir outputs/your-study \
  --returns-to-scale free
```

No missing values are silently filled. `--drop-missing` drops only rows with null input values and is always explicit; zeros, negatives, invalid years, and nonfinite observations remain errors.

## Load public Statistics Canada data

CanProd fetches official **English, non-Census, full-table CSV ZIP** downloads from `https://www150.statcan.gc.ca/n1/tbl/csv/<PID>-eng.zip`. It uses **named** fields (`REF_DATE`, `VECTOR`, `VALUE`) rather than historical field positions. The ZIPs are cached, streamed, read without extraction and available offline after the first successful download.

```bash
canprod fetch-series --table 36100096 --vector v90968617 \
  --name candidate_capital --aggregation last \
  --out outputs/candidate_capital.csv
```

**Important:** This command demonstrates historical catalog identifiers found in the old EconCan source. It does not establish that the vector is still available, that its unit is suited to the intended model, or that its last observation is the economically correct annual measure. For a new study, verify each vector against current Statistics Canada metadata.

Cache defaults to `~/.cache/canprod/statcan` (override with `--cache-dir` or `CANPROD_CACHE_DIR`). An archive is not refreshed automatically: use `--refresh` for updated data, or `--offline` to use existing archives only. Live downloads depend on external availability and are not part of the offline test suite.

### Assemble a three-factor dataset from verified vectors

1. Copy `configs/production.template.json` to a study-specific JSON file.
2. Replace **all** placeholder PIDs and vectors with three **independently verified** sources. Choose annual aggregation for each: `last` (a year-end stock, where appropriate), `mean` (a within-year mean), or `sum` (within-year flows, where appropriate).
3. Ensure the three series measure compatible sectors, geographies, concepts and years before fitting.
4. Run:

```bash
canprod build --spec configs/my_verified_production.json \
  --outdir outputs/canada --fit --base-year 2012 --plot
```

Exports include the aligned `production_data.csv` and `provenance.json`. Joining uses **only common calendar years** and never interpolates between series. The provenance manifest includes table IDs, vector IDs, aggregation and source ZIP hashes. There is no automatic index rebasing except the optional `--base-year` for modelling.

> **Annualization warning:** A partial year may contain fewer monthly/quarterly observations than a complete year. By default, the modern StatCan client rejects years with fewer observations than the highest-count year; after inspecting the source, override with `--allow-partial-years` (`fetch-series`) or `"allow_partial_years": true` in a build specification. This count-based guard is a warning mechanism, **not** proof that a year with the maximum number of observations is complete. Inspect input coverage and exclude incomplete years before relying on annual aggregates. StatCan `VALUE` is accompanied by units and scalar factors; verify these in metadata rather than assuming differently scaled or defined vectors are interchangeable.

## Historical data: preserved, not erased

The previous project's code is preserved under `archive/econcan-original/src/`; its manifest, previous lockfile and scratch scripts are also archived. The three raw CANSIM-era exports are preserved **byte-for-byte** under `data/legacy/`.

A dedicated reader supports the supplied **monthly** CANSIM export:

```bash
canprod legacy-series \
  --input data/legacy/dataset_can_cansim5245628780870031920.csv \
  --vector v65201809 --aggregation mean \
  --out outputs/historical-manufacturing-monthly-average.csv
```

This yields an annual **mean of monthly reported observations**, **not** an annual GDP total. The last year (2017) is incomplete in that frozen export. The other two archived CANSIM CSVs have unusual historical matrix/legend layouts and remain available for forensic recovery rather than being misparsed as modern CSV tables. See [migration](docs/migration.md) and [data provenance](docs/data-provenance.md).

## Design

```text
canprod/
├── src/canprod/
│   ├── cli.py        # User-facing, reproducible operations
│   ├── statcan.py    # Offline-capable StatCan ZIP client / vector selection
│   ├── workflow.py   # Strict series specification and annual assembly
│   ├── model.py      # Validated Cobb–Douglas OLS / diagnostics
│   ├── legacy.py     # Narrow reader for a frozen historical CANSIM export
│   ├── plot.py       # Optional, headless visualization
│   └── errors.py     # Explicit domain errors
├── configs/          # Unfilled study specification template
├── examples/         # Explicitly synthetic K/L/Y example data
├── tests/            # Network-free regression and data pipeline tests
├── data/legacy/      # Historical source exports, unchanged
├── archive/          # Original EconCan implementation, unchanged
└── docs/             # Architecture, methodology and migration notes
```

The package is intentionally small: no empty frameworks, dual data abstractions, implicit network calls on import, giant dependency stack, or untested research claims.

## Developer workflow

```bash
python -m pip install -e '.[dev]'
ruff check src tests examples
pytest -q
```

The GitHub Actions workflow runs linting, the offline test suite, and a full synthetic-model CLI smoke test on Python 3.11–3.13.

## Limitations

This is **reproducible research infrastructure**, not validated economic evidence or a policy/forecasting product. The model uses ordinary log-linear least squares, imposes constant returns to scale by default, supplies **in-sample** diagnostics, and makes **no** causal or statistical-inference claims. No automatic checks can establish that investment is capital stock, that employment counts are labour hours, or that outputs and inputs belong to the same industry. See [methodology](docs/methodology.md).

Official source documentation: [Statistics Canada Full Table Download CSV User Guide](https://www.statcan.gc.ca/en/developers/csv/user-guide) and [Web Data Service User Guide](https://www.statcan.gc.ca/en/developers/wds/user-guide).

## License

MIT. Original copyright and historical attribution are preserved in `LICENSE.md` and the archived source. Statistics Canada data are subject to their own terms and attribution requirements; the package license does not relicense official datasets.

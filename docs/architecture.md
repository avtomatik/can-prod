# Architecture and invariants

## One pathway for each responsibility

**Source acquisition** (`statcan.py`): Validated eight-digit PIDs, fixed official English full-table URL, retry/backoff, explicit refresh and offline mode, compressed-size limit, temporary download followed by atomic replace. No ZIP extraction. `read_vector` filters rows from the table by exact vector ID, preserves source `UOM`, `SCALAR_FACTOR`, and `STATUS`, and checks duplicate dates and unit inconsistencies.

**Research specification** (`workflow.py`): Three named factors (capital, labour, output) are chosen by an explicit JSON manifest. Annual aggregation is a required property of each series, never inferred from names or historical guesses. Year alignment uses a strict inner join. Source selection is the caller's scientific responsibility; placeholder specs cannot be run.

**Numerical science** (`model.py`): Positive, complete, annual K/L/Y input is validated, normalized only on request, and then modelled independently of I/O. Constant-returns and unrestricted models have explicit equations and metrics. No global state; no mutation of caller's DataFrame.

**User interface** (`cli.py`): Converts inputs to validated types, orchestrates work, writes outputs and returns a nonzero exit status for user errors. It never downloads just by being imported. Files land only in user-chosen output directories or an explicit/default cache.

**Historical evidence** (`legacy.py`, `data/legacy/`, `archive/`): A narrow reader handles the known exported monthly file. Other matrix-shaped legacy datasets are retained but not automatically interpreted; experimental scripts do not participate in the installable Python package.

## Boundaries and planned extension points

- `StatCanClient`: Replacing a fetch strategy with a metadata-rich, authenticated, or bulk-vector adapter should not alter the model API.
- `ProductionSpec`: A studied series catalog can evolve independently; it must carry explicit unit, scope, base price, revision, and aggregation metadata before it is called a validated canonical dataset.
- `fit_cobb_douglas`: Keep estimation pure and versionable. Do not add I/O side effects or use a fitted model as evidence for productivity growth without economic validation.
- `plot.py`: Optional publication layer. No display/GUI requirements for CI or servers.

## Reproducibility contract

For a model run, record: package version, source ZIP checksums, manifest, annualization choices, overlapping years, mode of returns to scale, base year, and code revision/commit. `build` exports source IDs and hashes; the user should also keep the source archives and model outputs together for independent replication. A hash detects changes to a local source ZIP, but does not make past remote revisions recoverable unless the ZIP itself is retained.

## Explicit non-goals

No scraping, private account access, implicit catalog curation, automated domain-expert validation, live fetching in the test suite, black-box ML claims, or graphing as an import side effect.

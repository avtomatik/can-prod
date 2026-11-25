# Data sources, provenance and limits

## Bundled historical evidence

The `data/legacy/` files were provided in the original EconCan archive. Their contents were copied without changing byte order, delimiters, metadata or values. They should be considered frozen CANSIM-era exports, not a current statistical database. The original files are additionally described by scripts in `archive/econcan-original/`.

The three archives have different layouts. `legacy-series` supports **only** the identifiable `Monthly` layout of `dataset_can_cansim5245628780870031920.csv`. Do not use the generic modern StatCan reader for the two legend/matrix files or interpret their raw matrix rows as an economic panel.

## Official modern source

Statistics Canada's *Full Table Download CSV User Guide* defines the English ZIP naming convention (`PID-eng.zip`) and current non-Census data fields such as `REF_DATE`, `VECTOR`, `VALUE`, `UOM`, `SCALAR_FACTOR`, and `STATUS`. The service returns an entire table including a metadata CSV. References:

- https://www.statcan.gc.ca/en/developers/csv/user-guide
- https://www.statcan.gc.ca/en/developers/wds/user-guide

CanProd downloads public English table ZIPs from one official HTTPS hostname. It stores each archive by PID and does not extract untrusted ZIP paths. The `read_vector()` API preserves units, scalar-factor labels and status where present. Missing/suppressed observations are rejected for annualization rather than treated as zero.

### Provenance exported by `build`

`provenance.json` includes source URLs, PIDs, vectors, and annual aggregation. `archive_sha256` records the exact cached ZIP bytes used, if present. The complete source ZIP files themselves should be retained with an archival publication; downloading again can yield a revised version.

### Not inferred by the software

- Whether a vector is published, active, revised, discontinued, or suitable for a particular research question.
- Whether values are in millions, dollars, index points, year-end stocks, quarterly rates or flows. The source metadata must be consulted.
- Whether `sum`, `mean`, or `last` correctly converts each source frequency to a year.
- Whether a year is **complete** when the source ends mid-year. Unequal annual observation counts are rejected by default, but equal counts alone do not prove completeness.
- Whether a table's internal coverage or statistical classification changed historically.
- Whether archived CANSIM tables can be mapped directly onto modern PIDs or definitions.

## Example dataset

`examples/synthetic_production.csv` is generated from a deterministic pseudorandom seed for testing and demonstrations only. It is **not** Statistics Canada data and does not represent estimates of Canadian capital, labour or output.

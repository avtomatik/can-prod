# Engineering upgrade report — EconCan → CanProd

**Scope:** A clean, installable successor to the uploaded 2021–2023 Python experiments, preserving their research materials without pretending their scripts and source selections were validated production systems.

## Initial assessment

The original repository mixed unimplemented `econcore` infrastructure, two competing StatCan integration concepts, experimental `econcan` scripts, legacy CANSIM table identifiers, ad hoc source aggregation, global plotting, and unvalidated model transformations. It contained a nearly empty README, mismatched package metadata (`statcan` vs `econcan`), and no tests. A direct rename would not make the empirical analysis reproducible.

Specific examples of broken interfaces and hidden assumptions are recorded in [migration.md](migration.md). All supplied original source bytes remain available in the archived folders.

## Delivered architecture

1. **Stable `canprod` package and CLI:** `fit`, `build`, `fetch-series`, and `legacy-series`, plus a documented Python API.
2. **Modern source boundary:** eight-digit StatCan PID ZIP downloads, named-column extraction, single-vector selection, unit/scalar preservation, offline mode, retries, size limits, and atomic caching.
3. **Explicit aggregation:** a required `mean` / `sum` / `last` decision, strict annual date parsing, suppression/duplicate/partial-coverage guards, and no hidden interpolation.
4. **Reproducible model:** two well-defined Cobb–Douglas OLS specifications (constant/free returns to scale), input validation, optional base-year normalization, predictions, residuals and in-sample diagnostics.
5. **Provenance:** source PID/vector/URL, ZIP SHA-256 digests, aggregation, date-coverage metadata and study manifest for `build` outputs.
6. **Historical preservation:** original source tree, metadata and lockfile, plus byte-for-byte copies of all three old CANSIM exports. Only the known monthly CSV is handled by a supported legacy parser.
7. **Automated tests and documentation:** offline data ingestion/HTTP/cache fixtures, known-coefficient synthetic regression cases, full workflow integration test, CI, methodology and migration guidance.

## Tested here

- Installed the editable package without fetching new dependencies.
- Executed the test suite against pandas 2.2.3 and NumPy 2.3.5.
- Ran the CLI on synthetic production input through data validation, model estimation, JSON and CSV export, and headless PNG plotting.
- Verified the full ZIP ingestion → three-factor join → estimator → provenance pipeline against offline test archives.
- Did **not** call live Statistics Canada to verify the availability of old vectors or an official three-factor dataset selection.
- Could not run Ruff locally because package downloads were unavailable; the CI workflow includes Ruff to validate linting in an environment with dependencies.

## The next scientific milestone

Select and **document a defensible modern capital, labour, and output panel** for a single Canadian production boundary. This requires economic research in addition to software engineering. The repository intentionally ships a template, not a made-up or silently repurposed canonical dataset. Once the empirical definitions are vetted, commit the study-specific config and data dictionary, validate the time series, and reproduce the model in CI from a retained source snapshot.

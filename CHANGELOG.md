# Changelog

## 1.0.0 — Architecture rebuild (2026-11)

- Recast the repository as CanProd, with a single importable Python package and CLI.
- Added modern StatCan ZIP ingestion by named columns, safe local cache, explicit aggregation and offline execution.
- Added validated, reproducible Cobb–Douglas OLS for constant and unrestricted returns to scale.
- Added a fully synthetic, clearly labeled offline demonstration, output exports, and optional plotting.
- Added tests, CI, data/source documentation, and a historical-code archive.
- Preserved original historical CANSIM exports unchanged, and separated them from modern StatCan datasets.

This release is a new, explicit API and is **not** backward compatible with experimental EconCan scripts.

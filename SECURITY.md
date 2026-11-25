# Security and data integrity

- No authentication, credentials, or private accounts are needed for public StatCan CSV downloads.
- Downloads use a fixed Statistics Canada HTTPS host, a connect/read timeout, retry/backoff, a compressed size limit and atomic cache writes.
- Files are read as exact ZIP entries; archive members are **never extracted** to the filesystem.
- Source ZIP files can still be large. A limit on uncompressed member bytes is applied, but pandas analysis may require substantial RAM. Use smaller vectors/tables when possible.
- Cached archives are not digitally signed. Validate research provenance and source revisions independently for high-stakes use.
- `--offline` disables network downloads. User-controlled inputs are validated; never load arbitrary pickles.
- Reporting a vulnerability: open a private channel with the repository maintainer rather than publishing exploit details.

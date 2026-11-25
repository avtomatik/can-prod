"""Statistics Canada full-table CSV client.
The CSV format is detected by column *names*, not by historical positional offsets.
Only English non-Census table ZIPs are supported. No ZIP member is extracted.
"""

import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from zipfile import BadZipFile, ZipFile

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from canprod.errors import DataUnavailableError, DataValidationError

BASE_URL = "https://www150.statcan.gc.ca/n1/tbl/csv"
Aggregation = Literal["mean", "sum", "last"]
_VECTOR = re.compile(r"v[0-9]{1,10}\Z")


@dataclass(frozen=True, slots=True)
class SeriesSpec:
    """An exact vector in a StatCan PID, and an explicit annualization choice."""

    table_id: int
    vector: str
    name: str
    aggregation: Aggregation
    allow_partial_years: bool = False

    def __post_init__(self) -> None:
        if isinstance(self.table_id, bool) or not isinstance(
            self.table_id, int
        ):
            raise DataValidationError(
                "table_id must be an eight-digit integer PID"
            )
        if not (10_000_000 <= self.table_id <= 99_999_999):
            raise DataValidationError(
                "table_id must be an eight-digit StatCan PID"
            )
        if not isinstance(self.vector, str) or not _VECTOR.fullmatch(
            self.vector.lower()
        ):
            raise DataValidationError("vector must look like v1234567")
        if not isinstance(self.name, str) or not self.name.strip():
            raise DataValidationError("name must be a nonempty string")
        if self.aggregation not in ("mean", "sum", "last"):
            raise DataValidationError("aggregation must be mean, sum, or last")
        if not isinstance(self.allow_partial_years, bool):
            raise DataValidationError(
                "allow_partial_years must be true or false"
            )
        object.__setattr__(self, "vector", self.vector.lower())


def default_cache_dir() -> Path:
    override = os.getenv("CANPROD_CACHE_DIR")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".cache" / "canprod" / "statcan"


class StatCanClient:
    """Cache-backed, streamed downloader with an explicit offline mode."""

    def __init__(
        self,
        cache_dir: Path | str | None = None,
        *,
        offline: bool = False,
        timeout: float = 45.0,
        max_archive_bytes: int = 512 * 1024 * 1024,
        session: requests.Session | None = None,
    ) -> None:
        self.cache_dir = (
            Path(cache_dir) if cache_dir is not None else default_cache_dir()
        )
        self.offline = offline
        if timeout <= 0 or max_archive_bytes <= 0:
            raise ValueError("timeout and max_archive_bytes must be positive")
        self.timeout = timeout
        self.max_archive_bytes = max_archive_bytes
        self._session = session

    @property
    def session(self) -> requests.Session:
        if self._session is None:
            session = requests.Session()
            retry = Retry(
                total=3,
                backoff_factor=0.6,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET"],
                respect_retry_after_header=True,
            )
            session.mount("https://", HTTPAdapter(max_retries=retry))
            self._session = session
        return self._session

    def archive_path(self, table_id: int) -> Path:
        if (
            isinstance(table_id, bool)
            or not isinstance(table_id, int)
            or not (10_000_000 <= table_id <= 99_999_999)
        ):
            raise DataValidationError(
                "table_id must be an eight-digit StatCan PID"
            )
        return self.cache_dir / f"{table_id:08d}-eng.zip"

    def ensure_archive(self, table_id: int, *, refresh: bool = False) -> Path:
        destination = self.archive_path(table_id)
        if destination.is_file() and not refresh:
            return destination
        if self.offline:
            raise DataUnavailableError(
                f"No usable cached archive for {table_id}: {destination}. "
                "Provide the ZIP in --cache-dir or retry without --offline."
            )
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        url = f"{BASE_URL}/{table_id:08d}-eng.zip"
        # Write to a temporary file in the same directory: never replace a good cache
        # with an incomplete HTTP response.
        fd, candidate = tempfile.mkstemp(
            prefix=f".{table_id:08d}-", suffix=".download", dir=self.cache_dir
        )
        os.close(fd)
        try:
            with self.session.get(
                url, stream=True, timeout=self.timeout, allow_redirects=False
            ) as r:
                r.raise_for_status()
                if 300 <= r.status_code < 400:
                    raise DataUnavailableError(
                        "Unexpected redirect in Statistics Canada download"
                    )
                size = 0
                with open(candidate, "wb") as out:
                    for block in r.iter_content(chunk_size=1024 * 1024):
                        if not block:
                            continue
                        size += len(block)
                        if size > self.max_archive_bytes:
                            raise DataUnavailableError(
                                f"Archive exceeds limit of {self.max_archive_bytes} bytes"
                            )
                        out.write(block)
            # Validate the expected member before committing the cache.
            with ZipFile(candidate) as archive:
                if f"{table_id:08d}.csv" not in archive.namelist():
                    raise DataValidationError(
                        f"ZIP has no {table_id:08d}.csv member"
                    )
                if archive.getinfo(f"{table_id:08d}.csv").file_size > (
                    self.max_archive_bytes * 4
                ):
                    raise DataValidationError(
                        "Uncompressed table exceeds safety limit"
                    )
            os.replace(candidate, destination)
        except (requests.RequestException, BadZipFile, OSError) as exc:
            raise DataUnavailableError(
                f"Could not download Statistics Canada table {table_id}: {exc}"
            ) from exc
        finally:
            Path(candidate).unlink(missing_ok=True)
        return destination

    def read_vector(
        self, table_id: int, vector: str, *, refresh: bool = False
    ) -> pd.DataFrame:
        """Return source observations, preserving units/status and raw reference dates.
        Output columns: REF_DATE, VALUE, and any of UOM, SCALAR_FACTOR, STATUS
        found in the source. Missing VALUE is retained as NaN (never imputed).
        """
        if not isinstance(vector, str) or not _VECTOR.fullmatch(
            vector.lower()
        ):
            raise DataValidationError("vector must look like v1234567")
        archive_path = self.ensure_archive(table_id, refresh=refresh)
        member = f"{table_id:08d}.csv"
        try:
            with ZipFile(archive_path) as archive:
                info = archive.getinfo(member)
                if info.file_size > self.max_archive_bytes * 4:
                    raise DataValidationError(
                        "Uncompressed table exceeds safety limit"
                    )
                with archive.open(member) as file:
                    header = pd.read_csv(file, nrows=0, encoding="utf-8-sig")
                required = {"REF_DATE", "VECTOR", "VALUE"}
                missing = required.difference(header.columns)
                if missing:
                    raise DataValidationError(
                        f"Table {table_id} missing {sorted(missing)}; "
                        "expected a modern English StatCan full-table CSV"
                    )
                selected = [
                    col
                    for col in (
                        "REF_DATE",
                        "VECTOR",
                        "VALUE",
                        "UOM",
                        "SCALAR_FACTOR",
                        "STATUS",
                    )
                    if col in header.columns
                ]
                chunks: list[pd.DataFrame] = []
                with archive.open(member) as file:
                    for chunk in pd.read_csv(
                        file,
                        usecols=selected,
                        dtype={"REF_DATE": str, "VECTOR": str},
                        chunksize=50_000,
                        low_memory=False,
                        encoding="utf-8-sig",
                    ):
                        match = chunk["VECTOR"].str.lower().eq(vector.lower())
                        if match.any():
                            chunks.append(
                                chunk.loc[match].drop(columns="VECTOR").copy()
                            )
        except (BadZipFile, KeyError, OSError) as exc:
            raise DataValidationError(
                f"Invalid cache/archive for table {table_id}: {exc}"
            ) from exc
        if not chunks:
            raise DataValidationError(
                f"Vector {vector} not found in table {table_id}"
            )
        result = pd.concat(chunks, ignore_index=True)
        result["VALUE"] = pd.to_numeric(result["VALUE"], errors="coerce")
        if result["REF_DATE"].isna().any():
            raise DataValidationError(
                f"Vector {vector} contains missing dates"
            )
        if result["REF_DATE"].duplicated().any():
            raise DataValidationError(
                f"Vector {vector} has duplicate reference dates"
            )
        for col in ("UOM", "SCALAR_FACTOR"):
            if col in result and result[col].nunique(dropna=True) > 1:
                raise DataValidationError(
                    f"Vector {vector} mixes {col} values"
                )
        return result.sort_values("REF_DATE", kind="stable").reset_index(
            drop=True
        )

    def annual_series(
        self, spec: SeriesSpec, *, refresh: bool = False
    ) -> pd.Series:
        raw = self.read_vector(spec.table_id, spec.vector, refresh=refresh)
        # Reject year-spanning periods rather than silently misclassifying them.
        period = raw["REF_DATE"].astype(str)
        valid_format = period.str.fullmatch(
            r"\d{4}(?:-(?:0[1-9]|1[0-2])(?:-(?:0[1-9]|[12][0-9]|3[01]))?|-Q[1-4])?"
        )
        # Reject impossible calendar dates, including Feb 31, not just bad syntax.
        full_dates = period.str.fullmatch(r"\d{4}-\d{2}-\d{2}")
        if full_dates.any():
            parsed = pd.to_datetime(
                period.loc[full_dates], format="%Y-%m-%d", errors="coerce"
            )
            valid_format.loc[full_dates] &= parsed.notna().to_numpy()
        years = period.str.slice(0, 4).where(valid_format)
        if years.isna().any():
            examples = raw.loc[years.isna(), "REF_DATE"].head(3).tolist()
            raise DataValidationError(
                f"Unsupported REF_DATE format for {spec.vector}: {examples}. "
                "Use annual/quarterly/monthly periods, not spanned fiscal years."
            )
        # Mixing annual, monthly, quarterly or daily periods within one vector
        # would make annualization ill-defined even when all dates look valid.
        frequency = (
            "quarterly"
            if period.str.contains(r"-Q[1-4]$").all()
            else (
                "daily"
                if period.str.fullmatch(r"\d{4}-\d{2}-\d{2}").all()
                else (
                    "monthly"
                    if period.str.fullmatch(r"\d{4}-\d{2}").all()
                    else (
                        "annual"
                        if period.str.fullmatch(r"\d{4}").all()
                        else None
                    )
                )
            )
        )
        if frequency is None:
            raise DataValidationError(
                f"Vector {spec.vector} mixes reference-period frequencies; cannot annualize"
            )
        values = raw.assign(year=years.astype(int)).set_index("year")["VALUE"]
        if values.isna().any():
            raise DataValidationError(
                f"Vector {spec.vector} has missing or suppressed observations. "
                "Review STATUS and select a complete range explicitly before annualizing."
            )
        # No forward fills; sums require at least one observation, and missing
        # source values are NOT silently treated as zero.
        by_year = values.groupby(level=0, sort=True)
        counts = by_year.size()
        partial_years = [
            int(year) for year, count in counts.items() if count < counts.max()
        ]
        if partial_years and not spec.allow_partial_years:
            raise DataValidationError(
                f"Vector {spec.vector} has fewer observations in years {partial_years} "
                "than the maximum year. This may indicate partial annual coverage; "
                "inspect source dates and explicitly allow partial years if justified."
            )
        if spec.aggregation == "mean":
            output = by_year.mean()
        elif spec.aggregation == "sum":
            output = by_year.sum(min_count=1)
        else:
            output = by_year.last()
        if output.isna().any():
            raise DataValidationError(
                f"Annual series {spec.name} has missing aggregated years"
            )
        output.name = spec.name
        output.index.name = "year"
        output.attrs["source_metadata"] = {
            "frequency_inferred_from_dates": frequency,
            "unit": (
                str(raw["UOM"].dropna().iloc[0])
                if "UOM" in raw and raw["UOM"].notna().any()
                else None
            ),
            "scalar_factor": (
                str(raw["SCALAR_FACTOR"].dropna().iloc[0])
                if "SCALAR_FACTOR" in raw
                and raw["SCALAR_FACTOR"].notna().any()
                else None
            ),
            "observations": len(raw),
            "annual_observation_counts": {
                str(int(year)): int(count) for year, count in counts.items()
            },
            "potential_partial_years": partial_years,
        }
        return output

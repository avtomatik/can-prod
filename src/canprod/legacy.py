"""Read selected frozen historical CANSIM exports, without pretending they are current tables."""

import csv
from pathlib import Path

import pandas as pd

from canprod.errors import DataValidationError


def read_legacy_monthly(path: str | Path, vector: str) -> pd.Series:
    """Read the supplied CANSIM monthly export with a `Monthly,v...` header.
    A historically exported, static CSV; not interchangeable with the modern
    Statistics Canada CSV schema or a live StatCan download.
    """
    source = Path(path)
    vector = vector.lower()
    try:
        with source.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.reader(stream)
            for row in reader:
                if row and row[0].strip().lower() == "monthly":
                    vectors = [entry.lower().strip() for entry in row[1:]]
                    if vector not in vectors:
                        raise DataValidationError(
                            f"Vector {vector} not listed in monthly CSV header: {vectors}"
                        )
                    position = vectors.index(vector) + 1
                    period_to_value: list[tuple[str, float]] = []
                    for observation in reader:
                        if not observation or not observation[0].strip():
                            continue
                        if len(observation) <= position:
                            raise DataValidationError(
                                "Truncated monthly record"
                            )
                        period_to_value.append(
                            (observation[0], float(observation[position]))
                        )
                    break
            else:
                raise DataValidationError(
                    "No 'Monthly' header; unsupported legacy CSV layout"
                )
    except (OSError, ValueError, csv.Error) as exc:
        raise DataValidationError(f"Unable to read legacy CSV: {exc}") from exc
    if not period_to_value:
        raise DataValidationError(
            "Legacy monthly CSV contains no observations"
        )
    periods = pd.to_datetime(
        [p for p, _ in period_to_value], format="%b-%Y", errors="coerce"
    )
    if periods.isna().any() or periods.duplicated().any():
        raise DataValidationError(
            "Legacy CSV contains invalid or duplicate monthly dates"
        )
    return pd.Series(
        [value for _, value in period_to_value],
        index=pd.DatetimeIndex(periods, name="period"),
        name=vector,
        dtype=float,
    ).sort_index()


def legacy_annual_series(
    path: str | Path, vector: str, *, aggregation: str
) -> pd.Series:
    """Aggregate observations explicitly; never imply a mean is an annual GDP total."""
    if aggregation not in ("mean", "sum", "last"):
        raise DataValidationError("Aggregation must be mean, sum, or last")
    series = read_legacy_monthly(path, vector)
    groups = series.groupby(series.index.year)
    result = {"mean": groups.mean, "sum": groups.sum, "last": groups.last}[
        aggregation
    ]()
    result.index.name = "year"
    return result

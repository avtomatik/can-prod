"""Orchestrate a reproducible three-series input from explicit source specifications."""

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from canprod.errors import DataValidationError
from canprod.model import prepare_production_data
from canprod.statcan import SeriesSpec, StatCanClient


@dataclass(frozen=True)
class ProductionSpec:
    title: str
    capital: SeriesSpec
    labour: SeriesSpec
    output: SeriesSpec

    @classmethod
    def from_file(cls, path: str | Path) -> "ProductionSpec":
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise DataValidationError(f"Cannot read config: {exc}") from exc
        if not isinstance(data, dict) or not isinstance(
            data.get("series"), dict
        ):
            raise DataValidationError(
                "Config must be an object with a 'series' object"
            )
        series = data["series"]
        definitions = {}
        for name in ("capital", "labour", "output"):
            if not isinstance(series.get(name), dict):
                raise DataValidationError(
                    f"Config missing series.{name} object"
                )
            kwargs = series[name]
            try:
                definitions[name] = SeriesSpec(name=name, **kwargs)
            except (TypeError, DataValidationError) as exc:
                raise DataValidationError(
                    f"Invalid series.{name}: {exc}"
                ) from exc
        return cls(
            title=str(data.get("title", "Canadian production")), **definitions
        )

    def provenance(self) -> dict[str, object]:
        return {
            "title": self.title,
            "source": "Statistics Canada English full-table CSV (non-Census)",
            "series": {
                item.name: {
                    "table_id": item.table_id,
                    "vector": item.vector,
                    "aggregation": item.aggregation,
                    "allow_partial_years": item.allow_partial_years,
                    "source_url": (
                        f"https://www150.statcan.gc.ca/n1/tbl/csv/{item.table_id:08d}-eng.zip"
                    ),
                }
                for item in (self.capital, self.labour, self.output)
            },
        }


def build_production_frame(
    spec: ProductionSpec, client: StatCanClient, *, refresh: bool = False
) -> pd.DataFrame:
    """Inner-join calendar years; reject hidden gaps in any retained year."""
    columns = [
        client.annual_series(series, refresh=refresh)
        for series in (spec.capital, spec.labour, spec.output)
    ]
    frame = pd.concat(columns, axis=1, join="inner")
    if frame.empty:
        raise DataValidationError(
            "The three input series have no overlapping calendar years"
        )
    result = prepare_production_data(frame)
    result.attrs["source_metadata"] = {
        series.name: column.attrs.get("source_metadata", {})
        for series, column in zip(
            (spec.capital, spec.labour, spec.output), columns, strict=True
        )
    }
    return result

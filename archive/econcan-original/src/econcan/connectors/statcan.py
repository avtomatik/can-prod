from dataclasses import dataclass
from functools import cache
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class DatasetDefinition:
    series_id: str | int
    table_id: int
    description: str = ""


class StatCanConnector:
    def __init__(self, provider):
        self._provider = provider

    @cache
    def read_table(self, table_id: int) -> pd.DataFrame:
        return self._provider.load_table(table_id)

    def load_series(
        self, series_map: dict[str | int, int] | Iterable[DatasetDefinition]
    ) -> pd.DataFrame:
        if isinstance(series_map, dict):
            items = series_map.items()
        else:
            items = ((ds.series_id, ds.table_id) for ds in series_map)
        frames = []
        for series_id, table_id in items:
            df_table = self.read_table(table_id)
            if series_id not in df_table.columns:
                raise KeyError(
                    f"Series ID {series_id} not found in table {table_id}"
                )
            frames.append(df_table[[series_id]])
        combined = pd.concat(frames, axis=1, sort=True)
        combined.index = pd.to_datetime(combined.index)
        return combined

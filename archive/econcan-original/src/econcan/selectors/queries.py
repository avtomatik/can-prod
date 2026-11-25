import pandas as pd
from econcan.connectors.statcan import StatCanConnector
from econcan.funcs import transform_sum
from econcan.providers.statcan.provider import StatCanProvider
from econcore.transforms.time import transform_year_mean

provider = StatCanProvider()
connector = StatCanConnector(provider)


def combine_can_price_a(series_ids: tuple[dict[str, int]]) -> pd.DataFrame:
    return pd.concat(
        map(
            lambda _: connector.load_series(_).pipe(transform_deflator),
            series_ids,
        ),
        axis=1,
        sort=True,
    )


def combine_can_price_b(series_ids: tuple[dict[str, int]]) -> pd.DataFrame:
    return pd.concat(
        map(
            lambda _: connector.load_series(_).pipe(transform_pct_change),
            series_ids,
        ),
        axis=1,
    )


def combine_can_plain_or_sum(series_ids: dict[str, int]) -> pd.DataFrame:
    if len(series_ids) == 1:
        return connector.load_series(series_ids)
    return connector.load_series(series_ids).pipe(
        transform_sum, name="_".join((*series_ids, "sum"))
    )


def combine_can_special(
    series_ids_plain: dict[str, int], series_ids_mean: dict[str, int]
) -> pd.DataFrame:
    if series_ids_plain:
        return combine_can_plain_or_sum(series_ids_plain)
    if series_ids_mean:
        return combine_can_plain_or_sum(series_ids_mean).pipe(
            transform_year_mean
        )

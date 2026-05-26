# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 21:10:29 2021

@author: Alexander Mikhailov
"""


import pandas as pd

from core.constants import BLUEPRINT_CAPITAL
from core.funcs import combine_can_special, stockpile_can, transform_sum
from econdata.providers.statcan.schemas import TO_PARSE_DATES


# =============================================================================
# TODO: Clear It Up
# =============================================================================
def combine_can_plain_or_sum(series_ids: dict[str, int]) -> pd.DataFrame:
    if len(series_ids) > 1:
        return stockpile_can(series_ids).pipe(
            transform_sum, name="_".join((*series_ids, "sum"))
        )
    return stockpile_can(series_ids)


def dichotomize_series_ids(
    series_ids: dict[str, int], source_ids: tuple[int]
) -> tuple[dict[str, int]]:
    """
    Parameters
    ----------
    series_ids : dict[str, int]
        DESCRIPTION.
    source_ids : tuple[int]
        DESCRIPTION.
    Returns
    -------
    tuple[dict[str, int]]
        DESCRIPTION.
    """
    return (
        {
            key: value
            for key, value in series_ids.items()
            if value not in source_ids
        },
        {
            key: value
            for key, value in series_ids.items()
            if value in source_ids
        },
    )


# =============================================================================
# Product
# =============================================================================

SERIES_IDS = (
    {"v37482": 10100094},  # Not Useful: Capacity Utilization
    {"v4331088": 16100109},  # Not Useful: Capacity Utilization
    {"v142817": 16100111},  # Not Useful: Capacity Utilization
)

df = pd.concat(
    map(
        lambda _: combine_can_special(
            *dichotomize_series_ids(_, TO_PARSE_DATES)
        ),
        SERIES_IDS,
    ),
    axis=1,
    sort=True,
)

df.plot(grid=True)

SERIES_IDS = (
    {"v21573668": 36100207},  # Not Useful: Real Gross Domestic Product
)

df = pd.concat(
    map(
        lambda _: combine_can_special(
            *dichotomize_series_ids(_, TO_PARSE_DATES)
        ),
        SERIES_IDS,
    ),
    axis=1,
    sort=True,
)

df.plot(grid=True)

SERIES_IDS = (
    {"v41713056": 36100208},  # Not Useful: Capital Input
    {"v41713073": 36100208},  # Not Useful: Capital Stock
    {"v41707775": 36100309},  # Not Useful: Capital Input
    {"v42189387": 36100310},  # Not Useful: Capital Input
)

df = pd.concat(
    map(
        lambda _: combine_can_special(
            *dichotomize_series_ids(_, TO_PARSE_DATES)
        ),
        SERIES_IDS,
    ),
    axis=1,
    sort=True,
)

df.plot(grid=True)

# =============================================================================
# Capital cost
# =============================================================================
SERIES_IDS = {
    "v41713243": 36100208,
    "v41708375": 36100309,
    "v42189907": 36100310,
}

df = stockpile_can(SERIES_IDS)
df["mean"] = df.mean(axis=1)
df.plot(grid=True)
df = df.iloc[:, [-1]]

# =============================================================================
# FILE_NAME = 'data_composed.csv'
# kwargs = {
#     'path_or_buf': BASE_DIR / FILE_NAME
# }
# df.to_csv(**kwargs)
# =============================================================================

df = pd.concat([stockpile_can(BLUEPRINT_CAPITAL), df], axis=1)


SERIES_IDS = {
    # =========================================================================
    # Manufacturing Indexes
    # =========================================================================
    "v86718697": 36100217,
    "v41707475": 36100309,
    "v42189127": 36100310,
    "v11567": 36100386,
}

df = stockpile_can(SERIES_IDS)

SERIES_IDS = {
    # =========================================================================
    # Gross Output
    # =========================================================================
    "v86719219": 36100217,
    "v41708195": 36100309,
    "v42189751": 36100310,
    "v64602050": 36100488,
}

df = stockpile_can(SERIES_IDS)

# =============================================================================
# FILE_NAME = 'data_composed.csv'
# kwargs = {
#     'path_or_buf': BASE_DIR / FILE_NAME
# }
# df.to_csv(**kwargs)
# =============================================================================


SERIES_IDS = {
    "v46445661": 36100210,
    "v46445722": 36100210,
    "v46445783": 36100210,
    "v46445844": 36100210,
    "v46445905": 36100210,
}
df = stockpile_can(SERIES_IDS)
df["mean"] = df.sum(axis=1)
df = df.iloc[:, [-1]]


SERIES_IDS = {
    "v46444624": 36100210,
    "v46444685": 36100210,
    "v46444746": 36100210,
    "v46444990": 36100210,
    "v46445051": 36100210,
    "v46445112": 36100210,
    "v46445356": 36100210,
    "v46445417": 36100210,
    "v46445478": 36100210,
    "v46445722": 36100210,
    "v46445783": 36100210,
    "v46445844": 36100210,
}

for series_id in tuple(SERIES_IDS)[::3]:
    stockpile_can({series_id: SERIES_IDS[series_id]}).plot(grid=True)

for series_id in tuple(SERIES_IDS)[1::3]:
    stockpile_can({series_id: SERIES_IDS[series_id]}).plot(grid=True)

for series_id in tuple(SERIES_IDS)[2::3]:
    stockpile_can({series_id: SERIES_IDS[series_id]}).plot(grid=True)

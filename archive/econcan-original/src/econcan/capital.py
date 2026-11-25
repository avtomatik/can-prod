# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 21:10:29 2021
@author: Alexander Mikhailov
"""
from typing import Sequence

import pandas as pd
from econcan.connectors.statcan import DatasetDefinition, StatCanConnector
from econcan.domain.capital.definition import BLUEPRINT_CAPITAL
from econcan.providers.statcan.provider import StatCanProvider
from econcan.selectors.queries import combine_can_special
from econcan.statcan.schema.tables import TO_PARSE_DATES


def split_series_by_reference_ids(
    series_to_id: dict[str, int],
    reference_ids: Sequence[int],
) -> tuple[dict[str, int], dict[str, int]]:
    reference_set = set(reference_ids)
    in_reference: dict[str, int] = {}
    not_in_reference: dict[str, int] = {}
    for name, id_ in series_to_id.items():
        if id_ in reference_set:
            in_reference[name] = id_
        else:
            not_in_reference[name] = id_
    return not_in_reference, in_reference


###############################################################################
# Product
###############################################################################
SERIES_IDS = [
    DatasetDefinition(
        series_id="v37482",
        table_id=10100094,
        description="Not Useful: Capacity Utilization",
    ),
    DatasetDefinition(
        series_id="v4331088",
        table_id=16100109,
        description="Not Useful: Capacity Utilization",
    ),
    DatasetDefinition(
        series_id="v142817",
        table_id=16100111,
        description="Not Useful: Capacity Utilization",
    ),
]
df = pd.concat(
    map(
        lambda _: combine_can_special(
            *split_series_by_reference_ids(_, TO_PARSE_DATES)
        ),
        SERIES_IDS,
    ),
    axis=1,
    sort=True,
)
df.plot(grid=True)
SERIES_IDS = [
    DatasetDefinition(
        series_id="v21573668",
        table_id=36100207,
        description="Not Useful: Real Gross Domestic Product",
    )
]
df = pd.concat(
    map(
        lambda _: combine_can_special(
            *split_series_by_reference_ids(_, TO_PARSE_DATES)
        ),
        SERIES_IDS,
    ),
    axis=1,
    sort=True,
)
df.plot(grid=True)
SERIES_IDS = [
    DatasetDefinition(
        series_id="v41713056",
        table_id=36100208,
        description="Not Useful: Capital Input",
    ),
    DatasetDefinition(
        series_id="v41713073",
        table_id=36100208,
        description="Not Useful: Capital Stock",
    ),
    DatasetDefinition(
        series_id="v41707775",
        table_id=36100309,
        description="Not Useful: Capital Input",
    ),
    DatasetDefinition(
        series_id="v42189387",
        table_id=36100310,
        description="Not Useful: Capital Input",
    ),
]
df = pd.concat(
    map(
        lambda _: combine_can_special(
            *split_series_by_reference_ids(_, TO_PARSE_DATES)
        ),
        SERIES_IDS,
    ),
    axis=1,
    sort=True,
)
df.plot(grid=True)
provider = StatCanProvider()
connector = StatCanConnector(provider)
###############################################################################
# Capital cost
###############################################################################
SERIES_IDS = {
    DatasetDefinition(series_id="v41713243", table_id=36100208),
    DatasetDefinition(series_id="v41708375", table_id=36100309),
    DatasetDefinition(series_id="v42189907", table_id=36100310),
}
df = connector.load_series(SERIES_IDS)
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
df = pd.concat([connector.load_series(BLUEPRINT_CAPITAL), df], axis=1)
SERIES_IDS = {
    # =========================================================================
    # Manufacturing Indexes
    # =========================================================================
    DatasetDefinition(
        series_id="v86718697",
        table_id=36100217,
        description="Manufacturing Indexes",
    ),
    DatasetDefinition(
        series_id="v41707475",
        table_id=36100309,
        description="Manufacturing Indexes",
    ),
    DatasetDefinition(
        series_id="v42189127",
        table_id=36100310,
        description="Manufacturing Indexes",
    ),
    DatasetDefinition(
        series_id="v11567",
        table_id=36100386,
        description="Manufacturing Indexes",
    ),
}
df = connector.load_series(SERIES_IDS)
SERIES_IDS = {
    # =========================================================================
    # Gross Output
    # =========================================================================
    DatasetDefinition(
        series_id="v86719219", table_id=36100217, description="Gross Output"
    ),
    DatasetDefinition(
        series_id="v41708195", table_id=36100309, description="Gross Output"
    ),
    DatasetDefinition(
        series_id="v42189751", table_id=36100310, description="Gross Output"
    ),
    DatasetDefinition(
        series_id="v64602050", table_id=36100488, description="Gross Output"
    ),
}
df = connector.load_series(SERIES_IDS)
# =============================================================================
# FILE_NAME = 'data_composed.csv'
# kwargs = {
#     'path_or_buf': BASE_DIR / FILE_NAME
# }
# df.to_csv(**kwargs)
# =============================================================================
SERIES_IDS = {
    DatasetDefinition(series_id="v46445661", table_id=36100210),
    DatasetDefinition(series_id="v46445722", table_id=36100210),
    DatasetDefinition(series_id="v46445783", table_id=36100210),
    DatasetDefinition(series_id="v46445844", table_id=36100210),
    DatasetDefinition(series_id="v46445905", table_id=36100210),
}
df = connector.load_series(SERIES_IDS)
df["mean"] = df.sum(axis=1)
df = df.iloc[:, [-1]]
SERIES_IDS = {
    DatasetDefinition(series_id="v46444624", table_id=36100210),
    DatasetDefinition(series_id="v46444685", table_id=36100210),
    DatasetDefinition(series_id="v46444746", table_id=36100210),
    DatasetDefinition(series_id="v46444990", table_id=36100210),
    DatasetDefinition(series_id="v46445051", table_id=36100210),
    DatasetDefinition(series_id="v46445112", table_id=36100210),
    DatasetDefinition(series_id="v46445356", table_id=36100210),
    DatasetDefinition(series_id="v46445417", table_id=36100210),
    DatasetDefinition(series_id="v46445478", table_id=36100210),
    DatasetDefinition(series_id="v46445722", table_id=36100210),
    DatasetDefinition(series_id="v46445783", table_id=36100210),
    DatasetDefinition(series_id="v46445844", table_id=36100210),
}
for series_id in tuple(SERIES_IDS)[::3]:
    connector.load_series({series_id: SERIES_IDS[series_id]}).plot(grid=True)
for series_id in tuple(SERIES_IDS)[1::3]:
    connector.load_series({series_id: SERIES_IDS[series_id]}).plot(grid=True)
for series_id in tuple(SERIES_IDS)[2::3]:
    connector.load_series({series_id: SERIES_IDS[series_id]}).plot(grid=True)

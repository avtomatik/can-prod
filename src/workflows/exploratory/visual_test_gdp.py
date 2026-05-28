import matplotlib.pyplot as plt
import pandas as pd

from econcan.domain.gdp.definition import SERIES_IDS
from econcan.providers.statcan.provider import StatCanProvider
from econcan.providers.statcan.selectors import pull_by_series_id
from econcore.transforms.time import transform_year_sum


def plot_can_test(df: pd.DataFrame) -> None:
    plt.figure()
    df.plot(logy=True)
    plt.title("Discrepancy")
    plt.xlabel("Period")
    plt.ylabel("Index")
    plt.grid()
    plt.show()


def test_data_can():
    """Project I: Canada Gross Domestic Product Data Comparison"""
    _provider = StatCanProvider()

    df = pd.concat(
        [
            pd.concat(
                [
                    _provider.load_table(_args[0]).pipe(
                        transform_year_sum, _args[1]
                    )
                    for _args in SERIES_IDS[:3]
                ],
                axis=1,
                sort=True,
            ),
            pd.concat(
                [
                    _provider.load_table(_args[0]).pipe(
                        pull_by_series_id, _args[1]
                    )
                    for _args in SERIES_IDS[3:]
                ],
                axis=1,
                sort=True,
            ).apply(pd.to_numeric, errors="coerce"),
        ],
        axis=1,
        sort=True,
    ).dropna(axis=0)
    df["series_0x0"] = df.iloc[:, 0].div(df.iloc[0, 0])
    df["series_0x1"] = df.iloc[:, 4].div(df.iloc[0, 4])
    df["series_0x2"] = df.iloc[:, 5].div(df.iloc[0, 5])
    df["series_0x3"] = (
        df.iloc[:, 7].div(df.iloc[:, 6]).div(df.iloc[:, 5]).mul(100)
    )
    df["series_0x4"] = df.iloc[:, 8].div(df.iloc[0, 8])
    # =========================================================================
    # Option 1
    # =========================================================================
    df.iloc[:, (-5, -3)].pipe(plot_can_test)
    # =========================================================================
    # Option 2
    # =========================================================================
    df.iloc[:, (-2, -1)].pipe(plot_can_test)
    # =========================================================================
    # Option 3
    # =========================================================================
    df.iloc[:, (-4, -1)].pipe(plot_can_test)

    # =========================================================================
    # Option 4: What?
    # =========================================================================
    # plot_can_test(df.iloc[:, -1].div(df.iloc[:, -1]), df.iloc[:, -3])

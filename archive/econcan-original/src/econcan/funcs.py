#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 20:44:49 2023
@author: green-machine
"""
import re
import sqlite3

import pandas as pd
from econcan.connectors.statcan import DatasetDefinition
from econcan.providers.statcan.provider import StatCanProvider
from econcan.providers.statcan.selectors import pull_by_series_id
from econcore.storage.paths import DATA_DIR
from econcore.transforms.time import transform_year_sum


def pull_can_capital(df: pd.DataFrame) -> list[str]:
    """
    Retrieves Series IDs from Statistics Canada -- Fixed Assets Tables
    """
    {
        "table": "031-0004",
        "title": "Flows and stocks of fixed non-residential capital, total all industries, by asset, provinces and territories, annual (dollars x 1,000,000)",
        "file_name": "dataset_can_00310004-eng.zip",
    }
    _filter = (
        (df.iloc[:, 2].str.contains("2007 constant prices"))
        & (df.iloc[:, 4] == "Geometric (infinite) end-year net stock")
        & (df.iloc[:, 5].str.contains("Industrial", flags=re.IGNORECASE))
    )
    {
        "table": "36-10-0238-01 (formerly CANSIM 031-0004)",
        "title": "Flows and stocks of fixed non-residential capital, total all industries, by asset, provinces and territories, annual (dollars x 1,000,000)",
    }
    _filter = (
        (df.iloc[:, 3].str.contains("2007 constant prices"))
        & (df.iloc[:, 5] == "Straight-line end-year net stock")
        & (df.iloc[:, 6].str.contains("Industrial", flags=re.IGNORECASE))
    )
    return sorted(set(df[_filter].loc[:, "VECTOR"]))


def pull_can_capital(
    df: pd.DataFrame, params: tuple[int, str]
) -> pd.DataFrame:
    """
    WARNING: VERY EXPENSIVE OPERATION !
    Retrieves Series IDs from Statistics Canada -- Fixed Assets Tables
    Parameters
    ----------
    df : pd.DataFrame
    params : tuple[int, str]
        param : YEAR_BASE : Basic Price Year.
        param : CATEGORY : Estimate Basis.
        param : COMPONENT : Search Key Word
    Returns
    -------
    pd.DataFrame
    """
    DBNAME = "capital"
    stmt = f"""
    SELECT * FROM {DBNAME}
    WHERE
        geo = 'Canada'
        AND prices LIKE '%{params[0]} constant prices%'
        AND industry = '{params[1]}'
        AND category = '{params[2]}'
        AND component IN {params[-1]}
    ;
    """
    db_path = DATA_DIR / f"{DBNAME}.db"
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        df.to_sql(DBNAME, conn, if_exists="replace", index=True)
        cursor = conn.execute(stmt)
        return pd.DataFrame(
            cursor.fetchall(),
            columns=(
                "period",
                "geo",
                "prices",
                "industry",
                "category",
                "component",
                "series_id",
                "value",
            ),
        )


def pull_can_capital_former(
    df: pd.DataFrame, params: tuple[int, str]
) -> pd.DataFrame:
    """
    Retrieves Series IDs from Statistics Canada -- Fixed Assets Tables
    Parameters
    ----------
    df : pd.DataFrame
    params : tuple[int, str]
        param : YEAR_BASE : Basic Price Year.
        param : CATEGORY : Estimate Basis.
        param : COMPONENT : Search Key Word
    Returns
    -------
    pd.DataFrame
    """
    DBNAME = "capital"
    stmt = f"""
    SELECT * FROM {DBNAME}
    WHERE
        prices LIKE '%{params[0]} constant prices%'
        AND category = '{params[1]}'
        AND lower(component) LIKE '%{params[-1]}%'
    ;
    """
    db_path = DATA_DIR / f"{DBNAME}.db"
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        df.to_sql(DBNAME, conn, if_exists="replace", index=True)
        cursor = conn.execute(stmt)
        return pd.DataFrame(
            cursor.fetchall(),
            columns=(
                "period",
                "prices",
                "category",
                "component",
                "series_id",
                "value",
            ),
        )


def transform_stockpile(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================
    name : str
        New Column Name.
    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Sum of <series_ids>
        ================== =================================
    """
    return pd.concat(
        map(
            lambda _: df.pipe(pull_by_series_id, _), sorted(set(df.iloc[:, 0]))
        ),
        axis=1,
    ).apply(pd.to_numeric, errors="coerce")


def transform_sum(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """
    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, ...]    Series
        ================== =================================
    name : str
        New Column Name.
    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Sum of <series_ids>
        ================== =================================
    """
    df[name] = df.sum(axis=1)
    return df.iloc[:, [-1]]


def combine_can(blueprint: dict) -> pd.DataFrame:
    """
    Parameters
    ----------
    blueprint : dict
        DESCRIPTION.
    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Capital
        df.iloc[:, 1]      Labor
        df.iloc[:, 2]      Product
        ================== =================================
    """
    _provider = StatCanProvider()
    FILE_NAME = f"{tuple(blueprint)[0]}_preloaded.csv"
    kwargs = {
        "filepath_or_buffer": DATA_DIR / FILE_NAME,
    }
    if (DATA_DIR / f"{tuple(blueprint)[0]}_preloaded.csv").is_file():
        kwargs["index_col"] = 0
        _df = pd.read_csv(**kwargs)
    else:
        function = (
            # =================================================================
            # WARNING : pull_can_capital() : VERY EXPENSIVE OPERATION !
            # =================================================================
            pull_can_capital,
            pull_can_capital_former,
        )[max(blueprint) < 10**7]
        _df = _provider.load_table(tuple(blueprint)[0]).pipe(
            function, blueprint.get(tuple(blueprint)[0])
        )
        # =====================================================================
        # Kludge
        # =====================================================================
        _df = _df.set_index(_df.iloc[:, 0])
    df = pd.concat(
        [
            # =================================================================
            # Capital
            # =================================================================
            _df.loc[:, ("series_id", "value")]
            .pipe(transform_stockpile)
            .pipe(transform_sum, name="capital"),
            # =================================================================
            # Labor
            # =================================================================
            _provider.load_table(tuple(blueprint)[1])
            .pipe(pull_by_series_id, blueprint.get(tuple(blueprint)[1]))
            .apply(pd.to_numeric, errors="coerce"),
            # =================================================================
            # Manufacturing
            # =================================================================
            _provider.load_table(tuple(blueprint)[-1]).pipe(
                transform_year_sum, blueprint.get(tuple(blueprint)[-1])
            ),
        ],
        axis=1,
    ).dropna(axis=0)
    df.columns = ("capital", "labor", "product")
    return df.div(df.iloc[0, :])


def get_blueprint(year_base: int = 2012) -> dict:
    return {
        # =====================================================================
        # Capital
        # =====================================================================
        # 36100096: (
        #     year_base,
        #     "Manufacturing",
        #     "Linear end-year net stock",
        #     (
        #         "Non-residential buildings",
        #         "Engineering construction",
        #         "Machinery and equipment",
        #     ),
        # ),
        # =====================================================================
        # Labor : DatasetDefinition(series_id="v2523012", table_id=14100027), Preferred Over DatasetDefinition(series_id="v3437501", table_id=2820011) Which Is Quarterly
        # =====================================================================
        DatasetDefinition(series_id="v2523012", table_id=14100027),
        DatasetDefinition(
            series_id="v65201809",
            table_id=36100434,
            description="Manufacturing",
        ),
    }


def get_blueprint_former(year_base: int = 2007) -> dict:
    return {
        # =====================================================================
        # Capital
        # =====================================================================
        # 310004: (
        #     year_base,
        #     "Geometric (infinite) end-year net stock",
        #     "industrial",
        # ),
        # =====================================================================
        # Labor : DatasetDefinition(series_id="v2523012", table_id=2820012), Preferred Over DatasetDefinition(series_id="v3437501", table_id=2820011) Which Is Quarterly
        # =====================================================================
        DatasetDefinition(series_id="v2523012", table_id=2820012),
        DatasetDefinition(
            series_id="v65201809",
            table_id=3790031,
            description="Manufacturing",
        ),
    }


def filter_df(df: pd.DataFrame) -> pd.DataFrame:
    FILTER = (df.loc[:, "naics"] == "All industries (x 1,000,000)") & (
        df.loc[:, "series_id"] != "v65201756"
    )
    FILTER = (df.loc[:, "naics"] == "Manufacturing (x 1,000,000)") & (
        df.loc[:, "series_id"] != "v65201809"
    )
    return df[FILTER].iloc[:, -2:]

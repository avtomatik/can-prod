import pandas as pd


def pull_by_series_id(df: pd.DataFrame, series_id: str) -> pd.DataFrame:
    """
    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================
    series_id : str
    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series
        ================== =================================
    """
    assert df.shape[1] == 2
    return (
        df[df.iloc[:, 0] == series_id]
        .iloc[:, [1]]
        .rename(columns={"value": series_id})
    )

import matplotlib.pyplot as plt
import pandas as pd


def plot_cobb_douglas_3d(df: pd.DataFrame) -> None:
    """
    Cobb--Douglas 3D-Plotting

    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Capital
        df.iloc[:, 1]      Labor
        df.iloc[:, 2]      Product
        ================== =================================
    Returns
    -------
    None
    """
    assert df.shape[1] == 3

    fig = plt.figure()
    ax = fig.gca(projection="3d")
    ax.plot(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2])
    ax.set_xlabel("Capital")
    ax.set_ylabel("Labor")
    ax.set_zlabel("Production")
    ax.view_init(30, 45)
    plt.show()

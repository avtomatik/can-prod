import pandas as pd
from econcan.connectors.statcan import StatCanConnector
from econcan.domain.capital.definition import BLUEPRINT_CAPITAL
from econcan.domain.labour.definition import BLUEPRINT_LABOUR
from econcan.domain.product.definition import BLUEPRINT_PRODUCT
from econcan.providers.statcan.provider import StatCanProvider
from econcore.storage.paths import BASE_DIR


def main(series_ids: dict[str, int], file_name: str = "stat_can_desc.csv"):
    provider = StatCanProvider()
    connector = StatCanConnector(provider)
    FILE_NAMES = ("stat_can_cap.csv", "stat_can_lab.csv", "stat_can_prd.csv")
    # =========================================================================
    # Construct CSV File from Specification
    # =========================================================================
    connector.load_series(series_ids)
    # =========================================================================
    # Retrieve Series Description
    # =========================================================================
    df = pd.concat(
        map(lambda _: pd.read_csv(_, index_col=0), FILE_NAMES), axis=1
    )
    pd.merge(
        pd.read_csv(file_name, index_col=0),
        df.transpose(),
        left_index=True,
        right_index=True,
    ).transpose().to_csv(BASE_DIR / file_name)


if __name__ == "__main__":
    main(BLUEPRINT_CAPITAL | BLUEPRINT_LABOUR | BLUEPRINT_PRODUCT)

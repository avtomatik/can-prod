import pandas as pd

FILE_NAME = "stat_can_cap_matching.csv"
df = pd.read_csv(FILE_NAME, index_col=0)
CRITERIA = [
    "Information and communication technologies machinery and equipment",
    "Land",
]
df = df[~df.loc[:, "desc_1"].isin(CRITERIA)]
CRITERIA = ["Intellectual property products"]
df = df[~df.loc[:, "desc_2"].isin(CRITERIA)]
# =============================================================================
# df.dropna(axis=0, how='all').to_csv(
#     DATA_DIR / FILE_NAME, index=True
# )
# =============================================================================

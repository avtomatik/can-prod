from econcan.connectors.statcan import DatasetDefinition

# =========================================================================
# Expenditure-Based Gross Domestic Product Series Used
# Income-Based Gross Domestic Product Series Not Used
# =========================================================================
SERIES_IDS = {
    # =====================================================================
    # Series A: Equals Series D, However, Series D Is Preferred Over Series A As It Is Yearly:
    # v62307282 - 380-0066 Price indexes, gross domestic product; Canada; Implicit price indexes; Gross domestic product at market prices (quarterly, 1961-03-01 to 2017-09-01)
    # =====================================================================
    DatasetDefinition(series_id="v62307282", table_id=3800066),
    # =====================================================================
    # Series B: Equals Both Series C & Series E, However, Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62306896 - 380-0084 Gross domestic product at 2007 constant prices, expenditure-based; Canada; Seasonally adjusted at annual rates; Gross domestic product at market prices (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)
    # =====================================================================
    DatasetDefinition(series_id="v62306896", table_id=3800084),
    # =====================================================================
    # Series C: Equals Both Series B & Series E, However, Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62306938 - 380-0084 Gross domestic product at 2007 constant prices, expenditure-based; Canada; Unadjusted; Gross domestic product at market prices (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)
    # =====================================================================
    DatasetDefinition(series_id="v62306938", table_id=3800084),
    # =====================================================================
    # Series D: Equals Series A, However, Series D Is Preferred Over Series A As It Is Yearly: v62471023 - 380-0102 Gross domestic product indexes; Canada; Implicit price indexes; Gross domestic product at market prices (annual, 1961 to 2016)
    # =====================================================================
    DatasetDefinition(series_id="v62471023", table_id=3800102),
    # =====================================================================
    # Series E: Equals Both Series B & Series C, However, Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62471340 - 380-0106 Gross domestic product at 2007 constant prices, expenditure-based; Canada; Gross domestic product at market prices (x 1,000,000) (annual, 1961 to 2016)
    # =====================================================================
    DatasetDefinition(series_id="v62471340", table_id=3800106),
    DatasetDefinition(series_id="v96411770", table_id=3800518),
    DatasetDefinition(series_id="v96391932", table_id=3800566),
    DatasetDefinition(series_id="v96730304", table_id=3800567),
    DatasetDefinition(series_id="v96730338", table_id=3800567),
}

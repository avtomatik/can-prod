from econcan.connectors.statcan import DatasetDefinition

SERIES_IDS_CD = {
    # =========================================================================
    # Annual Increase in Terms of Cost Price (1)
    # =========================================================================
    "CDT2S1": "dataset_usa_cobb-douglas.zip",
    # =========================================================================
    # Annual Increase in Terms of 1880 dollars (3)
    # =========================================================================
    "CDT2S3": "dataset_usa_cobb-douglas.zip",
}
SERIES_IDS_PRCH = {"P0107": "dataset_uscb.zip", "P0110": "dataset_uscb.zip"}
SERIES_IDS_PRICE_A = (
    {
        DatasetDefinition(series_id="v90968617", table_id=36100096),
        DatasetDefinition(series_id="v90971177", table_id=36100096),
    },
    {
        DatasetDefinition(series_id="v90968618", table_id=36100096),
        DatasetDefinition(series_id="v90971178", table_id=36100096),
    },
    {
        DatasetDefinition(series_id="v90968619", table_id=36100096),
        DatasetDefinition(series_id="v90971179", table_id=36100096),
    },
    {
        DatasetDefinition(series_id="v90968620", table_id=36100096),
        DatasetDefinition(series_id="v90971180", table_id=36100096),
    },
    {
        DatasetDefinition(series_id="v90968621", table_id=36100096),
        DatasetDefinition(series_id="v90971181", table_id=36100096),
    },
    {
        DatasetDefinition(series_id="v1071434", table_id=36100236),
        DatasetDefinition(series_id="v1119722", table_id=36100236),
    },
    {
        DatasetDefinition(series_id="v1071435", table_id=36100236),
        DatasetDefinition(series_id="v1119723", table_id=36100236),
    },
    {
        DatasetDefinition(series_id="v1071436", table_id=36100236),
        DatasetDefinition(series_id="v1119724", table_id=36100236),
    },
    {
        DatasetDefinition(series_id="v1071437", table_id=36100236),
        DatasetDefinition(series_id="v1119725", table_id=36100236),
    },
)
SERIES_IDS_PRICE_A = (
    {
        DatasetDefinition(series_id="v90968617", table_id=36100096),
        DatasetDefinition(series_id="v90973737", table_id=36100096),
    },
    {
        DatasetDefinition(series_id="v90968618", table_id=36100096),
        DatasetDefinition(series_id="v90973738", table_id=36100096),
    },
    {
        DatasetDefinition(series_id="v90968619", table_id=36100096),
        DatasetDefinition(series_id="v90973739", table_id=36100096),
    },
    {
        DatasetDefinition(series_id="v90968620", table_id=36100096),
        DatasetDefinition(series_id="v90973740", table_id=36100096),
    },
    {
        DatasetDefinition(series_id="v90968621", table_id=36100096),
        DatasetDefinition(series_id="v90973741", table_id=36100096),
    },
    {
        DatasetDefinition(series_id="v1071434", table_id=36100236),
        DatasetDefinition(series_id="v4421025", table_id=36100236),
    },
    {
        DatasetDefinition(series_id="v1071435", table_id=36100236),
        DatasetDefinition(series_id="v4421026", table_id=36100236),
    },
    {
        DatasetDefinition(series_id="v1071436", table_id=36100236),
        DatasetDefinition(series_id="v4421027", table_id=36100236),
    },
    {
        DatasetDefinition(series_id="v1071437", table_id=36100236),
        DatasetDefinition(series_id="v4421028", table_id=36100236),
    },
    {
        DatasetDefinition(series_id="v64498363", table_id=36100236),
        DatasetDefinition(series_id="v64498379", table_id=36100236),
    },
)
SERIES_IDS_PRICE_B = (
    {
        DatasetDefinition(series_id="v46444990", table_id=36100210),
    },
    {
        DatasetDefinition(series_id="v46445051", table_id=36100210),
    },
    {
        DatasetDefinition(series_id="v46445112", table_id=36100210),
    },
)

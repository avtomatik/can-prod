from econcan.connectors.statcan import DatasetDefinition

# =============================================================================
# 16100077-eng.zip: NO;
# 16100088-eng.zip: NO;
# 16100118-eng.zip: NO;
# 34100278-eng.zip: NO;
# 34100279-eng.zip: NO;
# 36100096-eng.zip: YES;
# 36100097-eng.zip: NO;
# 36100109-eng.zip: NO;
# 36100174-eng.zip: NO;
# 36100210-eng.zip: NO;
# 36100236-eng.zip: YES ALTERNATIVE;
# 36100237-eng.zip: YES ALTERNATIVE;
# 36100238-eng.zip: NO;
# =============================================================================
BLUEPRINT_CAPITAL = {
    DatasetDefinition(series_id="v90968617", table_id=36100096),
    DatasetDefinition(series_id="v90968618", table_id=36100096),
    DatasetDefinition(series_id="v90968619", table_id=36100096),
    DatasetDefinition(series_id="v90968620", table_id=36100096),
    DatasetDefinition(series_id="v90968621", table_id=36100096),
    DatasetDefinition(series_id="v90971177", table_id=36100096),
    DatasetDefinition(series_id="v90971178", table_id=36100096),
    DatasetDefinition(series_id="v90971179", table_id=36100096),
    DatasetDefinition(series_id="v90971180", table_id=36100096),
    DatasetDefinition(series_id="v90971181", table_id=36100096),
    DatasetDefinition(series_id="v90973737", table_id=36100096),
    DatasetDefinition(series_id="v90973738", table_id=36100096),
    DatasetDefinition(series_id="v90973739", table_id=36100096),
    DatasetDefinition(series_id="v90973740", table_id=36100096),
    DatasetDefinition(series_id="v90973741", table_id=36100096),
    DatasetDefinition(series_id="v46444563", table_id=36100210),
    DatasetDefinition(series_id="v46444624", table_id=36100210),
    DatasetDefinition(series_id="v46444685", table_id=36100210),
    DatasetDefinition(series_id="v46444746", table_id=36100210),
    DatasetDefinition(series_id="v46444807", table_id=36100210),
    DatasetDefinition(series_id="v46444929", table_id=36100210),
    DatasetDefinition(series_id="v46444990", table_id=36100210),
    DatasetDefinition(series_id="v46445051", table_id=36100210),
    DatasetDefinition(series_id="v46445112", table_id=36100210),
    DatasetDefinition(series_id="v46445173", table_id=36100210),
    DatasetDefinition(series_id="v46445295", table_id=36100210),
    DatasetDefinition(series_id="v46445356", table_id=36100210),
    DatasetDefinition(series_id="v46445417", table_id=36100210),
    DatasetDefinition(series_id="v46445478", table_id=36100210),
    DatasetDefinition(series_id="v46445539", table_id=36100210),
    DatasetDefinition(series_id="v46445661", table_id=36100210),
    DatasetDefinition(series_id="v46445722", table_id=36100210),
    DatasetDefinition(series_id="v46445783", table_id=36100210),
    DatasetDefinition(series_id="v46445844", table_id=36100210),
    DatasetDefinition(series_id="v46445905", table_id=36100210),
    DatasetDefinition(series_id="v1071434", table_id=36100236),
    DatasetDefinition(series_id="v1071435", table_id=36100236),
    DatasetDefinition(series_id="v1071436", table_id=36100236),
    DatasetDefinition(series_id="v1071437", table_id=36100236),
    DatasetDefinition(series_id="v64498363", table_id=36100236),
    DatasetDefinition(series_id="v1119722", table_id=36100236),
    DatasetDefinition(series_id="v1119723", table_id=36100236),
    DatasetDefinition(series_id="v1119724", table_id=36100236),
    DatasetDefinition(series_id="v1119725", table_id=36100236),
    DatasetDefinition(series_id="v64498371", table_id=36100236),
    DatasetDefinition(series_id="v4421025", table_id=36100236),
    DatasetDefinition(series_id="v4421026", table_id=36100236),
    DatasetDefinition(series_id="v4421027", table_id=36100236),
    DatasetDefinition(series_id="v4421028", table_id=36100236),
    DatasetDefinition(series_id="v64498379", table_id=36100236),
}
###############################################################################
# Gross fixed capital formation Data Block
###############################################################################
CAN_GROSS_FIXED_CAPITAL_FORMATION = (
    {
        "table": 3800068,
        "title": "Gross fixed capital formation",
        "geo": "Canada",
        "prices": "Chained (2007) dollars",
        "seas": "Seasonally adjusted at annual rates",
        "estimates": "Industrial machinery and equipment (x 1,000,000)",
        "frequency_start_end": "(quarterly, 1961-03-01 to 2017-09-01)",
        "series_id": "v62143969",
    },
    {
        "table": 3800068,
        "title": "Gross fixed capital formation",
        "geo": "Canada",
        "prices": "Chained (2007) dollars",
        "seas": "Seasonally adjusted at annual rates",
        "estimates": "Industrial machinery and equipment (x 1,000,000)",
        "frequency_start_end": "(quarterly, 1961-03-01 to 2017-09-01)",
        "series_id": "v62143990",
    },
)

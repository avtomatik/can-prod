from econcan.connectors.statcan import DatasetDefinition

# =============================================================================
# 14100027-eng.zip: YES;
# 14100036-eng.zip: NO;
# 14100221-eng.zip: NO;
# 14100235-eng.zip: YES;
# 14100238-eng.zip: NO;
# 14100242-eng.zip: NO;
# 14100243-eng.zip: NO;
# 14100259-eng.zip: MAYBE;
# 14100265-eng.zip: YES;
# 14100355-eng.zip: MAYBE;
# 14100392-eng.zip: NO;
# 36100489-eng.zip: NO;
# =============================================================================


BLUEPRINT_LABOUR = {
    DatasetDefinition(series_id="v2523013", table_id=14100027),
    DatasetDefinition(series_id="v54027148", table_id=14100221),
    DatasetDefinition(series_id="v54027152", table_id=14100221),
    DatasetDefinition(series_id="v74989", table_id=14100235),
    DatasetDefinition(series_id="v1596771", table_id=14100238),
    # =========================================================================
    # '?v78923847': 14100242,
    # =========================================================================
    # =========================================================================
    # '?v78923849': 14100242,
    # =========================================================================
    # =========================================================================
    # '?v78923848': 14100242,
    # =========================================================================
    DatasetDefinition(series_id="v78931172", table_id=14100243),
    DatasetDefinition(series_id="v78931174", table_id=14100243),
    DatasetDefinition(series_id="v78931173", table_id=14100243),
    # =========================================================================
    # '?v248856': 14100259,
    # =========================================================================
    # =========================================================================
    # '?v729388': 14100259,
    # =========================================================================
    # =========================================================================
    # '?v249422': 14100259,
    # =========================================================================
    # =========================================================================
    # '?v249984': 14100259,
    # =========================================================================
    DatasetDefinition(series_id="v249139", table_id=14100265),
    DatasetDefinition(series_id="v249703", table_id=14100265),
    DatasetDefinition(series_id="v250265", table_id=14100265),
    DatasetDefinition(series_id="v2057609", table_id=14100355),
    DatasetDefinition(series_id="v123355112", table_id=14100355),
    DatasetDefinition(series_id="v2057818", table_id=14100355),
    # =========================================================================
    # '?v101893670': 14100355,
    # =========================================================================
    # =========================================================================
    # '?v101893671': 14100355,
    # =========================================================================
    # =========================================================================
    # '?v101893672': 14100355,
    # =========================================================================
    DatasetDefinition(series_id="v1235071986", table_id=14100392),
    DatasetDefinition(series_id="v65521825", table_id=36100489),
    # =========================================================================
    # '!v65522120': 36100489,
    # =========================================================================
    # =========================================================================
    # '!v65522415': 36100489
    # =========================================================================
}

SERIES_IDS_INDEXES = [
    {
        DatasetDefinition(series_id="v74989", table_id=14100235),
    },
    DatasetDefinition(
        series_id="v21573686",
        table_id=36100207,
        description="Total number of jobs",
    ),
    DatasetDefinition(
        series_id="v719421",
        table_id=36100305,
        description="Total number of jobs",
    ),
]

SERIES_IDS_THOUSANDS = (
    {
        DatasetDefinition(series_id="v2523013", table_id=14100027),
    },
    {
        DatasetDefinition(series_id="v123355112", table_id=14100355),
    },
    {
        DatasetDefinition(series_id="v2057609", table_id=14100355),
    },
    {
        DatasetDefinition(series_id="v2057818", table_id=14100355),
    },
    {
        DatasetDefinition(series_id="v1235071986", table_id=14100392),
    },
)
SERIES_IDS_PERSONS = (
    {
        DatasetDefinition(series_id="v54027148", table_id=14100221),
        DatasetDefinition(series_id="v54027152", table_id=14100221),
    },
    {
        DatasetDefinition(series_id="v1596771", table_id=14100238),
    },
    {
        DatasetDefinition(series_id="v78931172", table_id=14100243),
    },
    {
        DatasetDefinition(series_id="v78931173", table_id=14100243),
        DatasetDefinition(series_id="v78931174", table_id=14100243),
    },
    {
        DatasetDefinition(series_id="v249139", table_id=14100265),
    },
    {
        DatasetDefinition(series_id="v249703", table_id=14100265),
        DatasetDefinition(series_id="v250265", table_id=14100265),
    },
    {
        DatasetDefinition(
            series_id="v535579",
            table_id=16100053,
            description="Production workers male",
        ),
        DatasetDefinition(
            series_id="v535593",
            table_id=16100053,
            description="Production workers female",
        ),
        DatasetDefinition(
            series_id="v535663",
            table_id=16100053,
            description="Administrative staff male",
        ),
        DatasetDefinition(
            series_id="v535677",
            table_id=16100053,
            description="Administrative staff female",
        ),
    },
    {
        DatasetDefinition(series_id="v761808", table_id=16100054),
        DatasetDefinition(series_id="v761927", table_id=16100054),
    },
    DatasetDefinition(
        series_id="v716397",
        table_id=36100303,
        description="Total number of jobs",
    ),
    {
        DatasetDefinition(series_id="v718173", table_id=36100303),
    },
    DatasetDefinition(
        series_id="v111382232",
        table_id=36100480,
        description="Total number of jobs",
    ),
    {
        DatasetDefinition(series_id="v65521825", table_id=36100489),
    },
)

from econcan.connectors.statcan import DatasetDefinition

# =============================================================================
# 16100013-eng.zip: NO;
# 16100038-eng.zip: NO;
# 16100047-eng.zip: NO;
# 16100052-eng.zip: NO;
# 16100053-eng.zip: NO;
# 16100054-eng.zip: NO;
# 16100056-eng.zip: NO;
# 16100079-eng.zip: NO;
# 16100117-eng.zip: NO;
# 16100119-eng.zip: NO;
# 36100207-eng.zip: NO;
# 36100217-eng.zip: NO;
# 36100303-eng.zip: NO;
# 36100305-eng.zip: NO;
# 36100309-eng.zip: NO;
# 36100310-eng.zip: NO;
# 36100383-eng.zip: NO;
# 36100384-eng.zip: NO;
# 36100385-eng.zip: YES;
# 36100386-eng.zip: YES;
# =============================================================================
BLUEPRINT_PRODUCT = {
    # =========================================================================
    # Not Useful: Capacity Utilization :: 10100094 :: Capacity utilization rates (Bank of Canada calculated series), seasonally adjusted
    # =========================================================================
    DatasetDefinition(
        series_id="v37482",
        table_id=10100094,
        description="Not Useful: Capacity Utilization",
    ),
    DatasetDefinition(series_id="v535579", table_id=16100053),
    DatasetDefinition(series_id="v535593", table_id=16100053),
    DatasetDefinition(series_id="v535663", table_id=16100053),
    DatasetDefinition(series_id="v535677", table_id=16100053),
    DatasetDefinition(series_id="v761808", table_id=16100054),
    DatasetDefinition(series_id="v761927", table_id=16100054),
    # =========================================================================
    # Not Useful: Capacity Utilization :: 16100109 :: Industrial capacity utilization rates, by industry
    # =========================================================================
    DatasetDefinition(
        series_id="v4331088",
        table_id=16100109,
        description="Not Useful: Capacity Utilization",
    ),
    # =========================================================================
    # Not Useful: Capacity Utilization :: 16100111 :: Industrial capacity utilization rates, by Standard Industrial Classification, 1980 (SIC)
    # =========================================================================
    DatasetDefinition(
        series_id="v142817",
        table_id=16100111,
        description="Not Useful: Capacity Utilization",
    ),
    DatasetDefinition(
        series_id="v21573668",
        table_id=36100207,
        description="Not Useful: Real Gross Domestic Product",
    ),
    DatasetDefinition(series_id="v21573686", table_id=36100207),
    # =========================================================================
    # '!v41712954': 36100208,
    # =========================================================================
    DatasetDefinition(
        series_id="v41713056",
        table_id=36100208,
        description="Not Useful: Capital Input",
    ),
    DatasetDefinition(
        series_id="v41713073",
        table_id=36100208,
        description="Not Useful: Capital Stock",
    ),
    DatasetDefinition(series_id="v41713243", table_id=36100208),
    DatasetDefinition(
        series_id="v86718697",
        table_id=36100217,
        description="Manufacturing Indexes",
    ),
    DatasetDefinition(
        series_id="v86719219", table_id=36100217, description="Gross Output"
    ),
    DatasetDefinition(series_id="v716397", table_id=36100303),
    DatasetDefinition(series_id="v718173", table_id=36100303),
    DatasetDefinition(series_id="v719421", table_id=36100305),
    DatasetDefinition(
        series_id="v41707475",
        table_id=36100309,
        description="Manufacturing Indexes",
    ),
    # =========================================================================
    # '!v41707595': 36100309,
    # =========================================================================
    DatasetDefinition(
        series_id="v41707775",
        table_id=36100309,
        description="Not Useful: Capital Input",
    ),
    DatasetDefinition(
        series_id="v41708195", table_id=36100309, description="Gross Output"
    ),
    DatasetDefinition(series_id="v41708375", table_id=36100309),
    DatasetDefinition(
        series_id="v42189127",
        table_id=36100310,
        description="Manufacturing Indexes",
    ),
    # =========================================================================
    # '!v42189231': 36100310,
    # =========================================================================
    DatasetDefinition(
        series_id="v42189387",
        table_id=36100310,
        description="Not Useful: Capital Input",
    ),
    DatasetDefinition(
        series_id="v42189751", table_id=36100310, description="Gross Output"
    ),
    DatasetDefinition(series_id="v42189907", table_id=36100310),
    DatasetDefinition(series_id="v248", table_id=36100383),
    DatasetDefinition(series_id="v328", table_id=36100383),
    DatasetDefinition(series_id="v394", table_id=36100385),
    DatasetDefinition(series_id="v473", table_id=36100385),
    DatasetDefinition(
        series_id="v11567",
        table_id=36100386,
        description="Manufacturing Indexes",
    ),
    DatasetDefinition(
        series_id="v111382232",
        table_id=36100480,
        description="Total number of jobs",
    ),
    # =========================================================================
    # Gross Output :: Output, by sector and industry, provincial and territorial;
    # =========================================================================
    DatasetDefinition(
        series_id="v64602050", table_id=36100488, description="Gross Output"
    ),
}

DATA_CONSTRUCT_CAN_FORMER = {
    # =========================================================================
    # Fixed Assets
    # =========================================================================
    "Capital": {
        "details": {
            "prices": "2007 constant prices",
            "category": "Geometric (infinite) end-year net stock",
        },
        "Industrial buildings (x 1,000,000)": {
            "series_ids": (
                "v43975603",
                "v43977683",
                "v43978099",
                "v43978515",
                "v43978931",
                "v43979347",
                "v43979763",
                "v43980179",
                "v43980595",
                "v43976019",
                "v43976435",
                "v43976851",
                "v43977267",
            )
        },
        "Industrial machinery (x 1,000,000)": {
            "series_ids": (
                "v43975594",
                "v43977674",
                "v43978090",
                "v43978506",
                "v43978922",
                "v43979338",
                "v43979754",
                "v43980170",
                "v43980586",
                "v43976010",
                "v43976426",
                "v43976842",
                "v43977258",
            )
        },
    },
    # =========================================================================
    # Labor
    # =========================================================================
    "Labor": {
        "table": 2820012,
        "title": "Labour Force Survey Estimates (LFS), employment by class of worker, North American Industry Classification System (NAICS) and sex",
        "geo": "Canada",
        "classofworker": "Total employed, all class of workers",
        "industry": "Manufacturing",
        "sex": "Both sexes (x 1,000)",
        "frequency_start_end": "(annual, 1987 to 2017)",
        "series_id": "v2523012",
    },
    # =========================================================================
    # Manufacturing
    # =========================================================================
    "Manufacturing": {
        "table": 3790031,
        "title": "Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS)",
        "geo": "Canada",
        "seas": "Trading-day adjusted",
        "prices": "2007 constant prices",
        "naics": "Manufacturing (x 1,000,000)",
        "frequency_start_end": "(monthly, 1997-01-01 to 2017-10-01)",
        "series_id": "v65201809",
    },
}
DATA_CONSTRUCT_CAN_FORMER_NOT_USED = {
    # =========================================================================
    # Fixed Assets
    # =========================================================================
    "Capital": [
        {
            "details": {
                "prices": "Chained (2007) dollars",
                "category": "Geometric (infinite) end-year net stock",
            },
            "Industrial buildings (x 1,000,000)": {
                "series_ids": (
                    "v43980803",
                    "v43981843",
                    "v43982051",
                    "v43982259",
                    "v43982467",
                    "v43982675",
                    "v43982883",
                    "v43983091",
                    "v43983299",
                    "v43981011",
                    "v43981219",
                    "v43981427",
                    "v43981635",
                )
            },
            "Industrial machinery (x 1,000,000)": {
                "series_ids": (
                    "v43980794",
                    "v43981834",
                    "v43982042",
                    "v43982250",
                    "v43982458",
                    "v43982666",
                    "v43982874",
                    "v43983082",
                    "v43983290",
                    "v43981002",
                    "v43981210",
                    "v43981418",
                    "v43981626",
                )
            },
        },
        {
            "details": {
                "prices": "Current prices",
                "category": "Geometric (infinite) end-year net stock",
            },
            "Industrial buildings (x 1,000,000)": {
                "series_ids": (
                    "v43975395",
                    "v43977475",
                    "v43977891",
                    "v43978307",
                    "v43978723",
                    "v43979139",
                    "v43979555",
                    "v43979971",
                    "v43980387",
                    "v43975811",
                    "v43976227",
                    "v43976643",
                    "v43977059",
                )
            },
            "Industrial machinery (x 1,000,000)": {
                "series_ids": (
                    "v43975386",
                    "v43977466",
                    "v43977882",
                    "v43978298",
                    "v43978714",
                    "v43979130",
                    "v43979546",
                    "v43979962",
                    "v43980378",
                    "v43975802",
                    "v43976218",
                    "v43976634",
                    "v43977050",
                )
            },
        },
    ],
    # =========================================================================
    # Labor
    # =========================================================================
    "Labor": {
        "table": 2820011,
        "title": "Labour Force Survey estimates (LFS), employment by class of worker, North American Industry Classification System (NAICS) and sex, unadjusted for seasonality",
        "geo": "Canada",
        "classofworker": "Total employed, all classes of workers",
        "industry": "Manufacturing",
        "sex": "Both sexes (x 1,000)",
        "frequency_start_end": "(monthly, 1987-01-01 to 2017-12-01)",
        "series_id": "v3437501",
    },
    # =========================================================================
    # Manufacturing
    # =========================================================================
    "Manufacturing": {
        "table": 3790031,
        "title": "Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS)",
        "geo": "Canada",
        "seas": "Seasonnaly adjusted at annual rates",
        "prices": "2007 constant prices",
        "naics": "Manufacturing (x 1,000,000)",
        "frequency_start_end": "(monthly, 1997-01-01 to 2017-10-01)",
        "series_id": "v65201536",
    },
}
DATA_STATCAN_ARCHIVE = (
    {
        "table": 2820012,
        "title": "Labour Force Survey Estimates (LFS), employment by class of worker, North American Industry Classification System (NAICS) and sex",
        "measure": "none",
    },
    {
        "table": 3790031,
        "title": "Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS)",
        "measure": "monthly (dollars x 1,000,000)",
    },
    {
        "table": 3800068,
        "title": "Gross fixed capital formation",
        "measure": "quarterly (dollars x 1,000,000)",
    },
    {
        "table": 310004,
        "title": "Flows and stocks of fixed non-residential capital, total all industries, by asset, provinces and territories",
        "measure": "annual (dollars x 1,000,000)",
    },
    {
        "table": 3790028,
        "title": "Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS), provinces and territories",
        "measure": "annual (percentage share)",
    },
    {
        "table": 3800001,
        "title": "Gross domestic product (GDP), income-based, *Terminated*",
        "measure": "quarterly (dollars x 1,000,000)",
    },
    {
        "table": 3800002,
        "title": "Gross domestic product (GDP), expenditure-based, *Terminated*",
        "measure": "quarterly (dollars x 1,000,000)",
    },
    {
        "table": 3800063,
        "title": "Gross domestic product, income-based",
        "measure": "quarterly (dollars x 1,000,000)",
    },
    {
        "table": 3800064,
        "title": "Gross domestic product, expenditure-based",
        "measure": "quarterly (dollars x 1,000,000)",
    },
    {
        "table": 3800069,
        "title": "Investment in inventories",
        "measure": "quarterly (dollars unless otherwise noted)",
    },
    {
        "table": 36100238,
        "title": "Flows and stocks of fixed non-residential capital, total all industries, by asset, provinces and territories Archived",
    },
    {
        "table": 36100096,
        "title": "Flows and stocks of fixed non-residential capital, by industry and type of asset, Canada, provinces and territories",
    },
)

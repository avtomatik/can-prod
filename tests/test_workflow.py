import json

import pandas as pd
import pytest

from canprod.errors import DataValidationError
from canprod.statcan import SeriesSpec
from canprod.workflow import ProductionSpec, build_production_frame


def test_json_config_and_build(tmp_path):
    config = {
        "title": "Fixture",
        "series": {
            "capital": {
                "table_id": 36100096,
                "vector": "v101",
                "aggregation": "last",
            },
            "labour": {
                "table_id": 14100027,
                "vector": "v102",
                "aggregation": "mean",
            },
            "output": {
                "table_id": 36100434,
                "vector": "v103",
                "aggregation": "sum",
            },
        },
    }
    source = tmp_path / "config.json"
    source.write_text(json.dumps(config))
    spec = ProductionSpec.from_file(source)
    assert spec.capital == SeriesSpec(36100096, "v101", "capital", "last")
    assert (
        "36100096-eng.zip"
        in spec.provenance()["series"]["capital"]["source_url"]
    )

    class Client:
        def annual_series(self, series, refresh=False):
            assert not refresh
            return pd.Series(
                {2020: 1.0, 2021: 2.0, 2022: 3.0, 2023: 4.0}, name=series.name
            )

    output = build_production_frame(spec, Client())
    assert output.columns.tolist() == ["capital", "labour", "output"]
    assert output.index.tolist() == [2020, 2021, 2022, 2023]


def test_invalid_template_fails_informatively(tmp_path):
    source = tmp_path / "config.json"
    source.write_text(
        '{"series":{"capital":{"table_id":null,"vector":"vREPLACE","aggregation":"last"}}}'
    )
    with pytest.raises(DataValidationError, match="capital"):
        ProductionSpec.from_file(source)

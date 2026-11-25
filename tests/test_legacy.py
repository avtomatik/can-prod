from pathlib import Path

import pytest

from canprod.errors import DataValidationError
from canprod.legacy import legacy_annual_series, read_legacy_monthly

FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "data/legacy/dataset_can_cansim5245628780870031920.csv"
)


def test_real_archived_monthly_dataset():
    series = read_legacy_monthly(FIXTURE, "v65201809")
    assert len(series) == 250
    assert series.iloc[0] == 11663
    assert series.iloc[-1] == 15444
    result = legacy_annual_series(FIXTURE, "v65201809", aggregation="mean")
    assert result.index.min() == 1997
    assert result.index.max() == 2017
    assert result.loc[1997] == pytest.approx(series.loc["1997"].mean())
    assert result.loc[2017] == pytest.approx(series.loc["2017"].mean())


def test_wrong_vector_rejected():
    with pytest.raises(DataValidationError, match="not listed"):
        read_legacy_monthly(FIXTURE, "v00001")


def test_other_layout_rejected(tmp_path):
    path = tmp_path / "unknown.csv"
    path.write_text("Legend:\nabc,def\n")
    with pytest.raises(DataValidationError, match="unsupported"):
        read_legacy_monthly(path, "v1")

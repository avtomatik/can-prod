import numpy as np
import pandas as pd
import pytest

from canprod.errors import DataValidationError, ModelEstimationError
from canprod.model import fit_cobb_douglas, prepare_production_data


def sample(alpha=0.4, beta=0.6, a=1.25):
    years = np.arange(2000, 2020)
    n = np.arange(len(years))
    k = 100 + 5 * n + 2 * np.sin(n)
    l = 50 + 2 * n + 3 * np.cos(n * 1.3)  # noqa: E741
    return pd.DataFrame(
        {
            "year": years,
            "capital": k,
            "labour": l,
            "output": a * k**alpha * l**beta,
        }
    )


def test_constant_returns_recovers_ground_truth():
    result = fit_cobb_douglas(sample(), returns_to_scale="constant")
    assert result.metrics.alpha_capital == pytest.approx(0.4, abs=1e-10)
    assert result.metrics.beta_labour == pytest.approx(0.6, abs=1e-10)
    assert result.metrics.scale_factor == pytest.approx(1.25, abs=1e-10)
    assert result.metrics.r_squared_level == pytest.approx(1.0)
    assert result.observations["residual_output"].abs().max() < 1e-10


def test_free_returns_recovers_ground_truth():
    result = fit_cobb_douglas(
        sample(alpha=0.37, beta=0.82), returns_to_scale="free"
    )
    assert result.metrics.alpha_capital == pytest.approx(0.37, abs=1e-10)
    assert result.metrics.beta_labour == pytest.approx(0.82, abs=1e-10)
    assert result.metrics.returns_to_scale_sum == pytest.approx(1.19)


def test_base_year_indexed_to_one():
    result = fit_cobb_douglas(sample(), base_year=2012)
    assert result.observations.loc[
        2012, ["capital", "labour", "output"]
    ].tolist() == [1.0, 1.0, 1.0]
    assert result.metrics.base_year == 2012
    assert result.metrics.r_squared_level == pytest.approx(1.0)


def test_missing_rejected_or_explicitly_dropped():
    df = sample()
    df.loc[0, "output"] = np.nan
    with pytest.raises(DataValidationError, match="missing"):
        fit_cobb_douglas(df)
    assert fit_cobb_douglas(df, missing="drop").metrics.observations == 19


@pytest.mark.parametrize("column", ["capital", "labour", "output"])
@pytest.mark.parametrize("value", [0, -1, np.inf])
def test_nonpositive_or_nonfinite_rejected(column, value):
    df = sample()
    df.loc[0, column] = value
    with pytest.raises(DataValidationError, match="finite and > 0"):
        prepare_production_data(df)


def test_duplicate_year_rejected():
    df = sample()
    df.loc[1, "year"] = 2000
    with pytest.raises(DataValidationError, match="Duplicate years"):
        fit_cobb_douglas(df)


def test_collinear_regressors_rejected():
    years = list(range(2000, 2020))
    df = pd.DataFrame(
        {
            "year": years,
            "capital": [100] * 20,
            "labour": [50] * 20,
            "output": range(10, 30),
        }
    )
    with pytest.raises(ModelEstimationError, match="collinear"):
        fit_cobb_douglas(df)


def test_missing_base_year_rejected():
    with pytest.raises(DataValidationError, match="absent"):
        fit_cobb_douglas(sample(), base_year=1988)


def test_model_does_not_mutate_input():
    df = sample()
    before = df.copy(deep=True)
    fit_cobb_douglas(df)
    pd.testing.assert_frame_equal(df, before)


def test_underdetermined_model_rejected():
    with pytest.raises(ModelEstimationError, match="at least 5"):
        fit_cobb_douglas(sample().head(4), returns_to_scale="free")

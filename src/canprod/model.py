"""Transparent Cobb–Douglas estimators using ordinary least squares.
This is descriptive estimation, not causal identification. OLS errors and
standard fit metrics are in-sample; see docs/methodology.md.
"""

from dataclasses import asdict, dataclass
from typing import Literal

import numpy as np
import pandas as pd

from canprod.errors import DataValidationError, ModelEstimationError

ReturnsToScale = Literal["constant", "free"]
_REQUIRED = ("capital", "labour", "output")


@dataclass(frozen=True, slots=True)
class FitMetrics:
    observations: int
    returns_to_scale: str
    base_year: int | None
    alpha_capital: float
    beta_labour: float
    scale_factor: float
    returns_to_scale_sum: float
    r_squared_level: float
    r_squared_log: float
    rmse_level: float
    mae_level: float

    def to_dict(self) -> dict[str, float | int | str | None]:
        return asdict(self)


@dataclass(frozen=True)
class FitResult:
    metrics: FitMetrics
    observations: pd.DataFrame


def prepare_production_data(
    frame: pd.DataFrame, *, missing: Literal["error", "drop"] = "error"
) -> pd.DataFrame:
    """Enforce unique annual observations and strictly positive numeric K, L, Y.
    Accept `year` as a column or the index. No reordering of model variables.
    Any invalid value is an error unless missing='drop', which drops only rows
    with null values, not zero/negative or nonnumeric values.
    """
    if missing not in ("error", "drop"):
        raise ValueError("missing must be 'error' or 'drop'")
    if not isinstance(frame, pd.DataFrame):
        raise DataValidationError("Expected a pandas DataFrame")
    df = frame.copy()
    if "year" in df.columns:
        df = df.set_index("year", drop=True)
    absent = set(_REQUIRED).difference(df.columns)
    if absent:
        raise DataValidationError(
            f"Input missing required columns: {sorted(absent)}"
        )
    try:
        years = pd.to_numeric(pd.Index(df.index), errors="raise")
    except (TypeError, ValueError) as exc:
        raise DataValidationError(
            "Years must be integer calendar years"
        ) from exc
    year_values = np.asarray(years, dtype=float)
    if (not np.isfinite(year_values).all()) or not np.equal(
        year_values, np.floor(year_values)
    ).all():
        raise DataValidationError("Years must be finite integers")
    if ((year_values < 1000) | (year_values > 9999)).any():
        raise DataValidationError("Years must be four-digit calendar years")
    df.index = pd.Index(year_values.astype(int), name="year")
    if df.index.has_duplicates:
        raise DataValidationError(
            "Duplicate years: one observation per calendar year is required"
        )
    df = df.loc[:, list(_REQUIRED)]
    for column in _REQUIRED:
        try:
            df[column] = pd.to_numeric(df[column], errors="raise")
        except (TypeError, ValueError) as exc:
            raise DataValidationError(
                f"Column {column} must contain numeric values"
            ) from exc
    if missing == "drop":
        df = df.dropna(how="any")
    if df.isna().any().any():
        raise DataValidationError(
            "Input contains missing K/L/Y; explicitly request missing='drop'"
        )
    numbers = df.to_numpy(dtype=float)
    if not np.isfinite(numbers).all() or (numbers <= 0).any():
        raise DataValidationError(
            "All capital, labour and output values must be finite and > 0"
        )
    return df.sort_index().astype(float)


def fit_cobb_douglas(
    frame: pd.DataFrame,
    *,
    base_year: int | None = None,
    returns_to_scale: ReturnsToScale = "constant",
    missing: Literal["error", "drop"] = "error",
) -> FitResult:
    """OLS estimation of Y = A K^alpha L^beta.
    'constant': estimate log(Y/L) = log(A) + alpha*log(K/L), beta=1-alpha.
    'free': estimate log(Y) = log(A) + alpha*log(K) + beta*log(L).
    If base_year is set, normalize K, L, Y to 1 in that year first.
    """
    if returns_to_scale not in ("constant", "free"):
        raise ValueError("returns_to_scale must be 'constant' or 'free'")
    df = prepare_production_data(frame, missing=missing)
    minimum = 4 if returns_to_scale == "constant" else 5
    if len(df) < minimum:
        raise ModelEstimationError(
            f"Need at least {minimum} complete years; got {len(df)}"
        )
    if base_year is not None:
        if isinstance(base_year, bool) or not isinstance(base_year, int):
            raise DataValidationError("base_year must be a calendar year")
        if base_year not in df.index:
            raise DataValidationError(
                f"Base year {base_year} is absent from input"
            )
        df = df.div(df.loc[base_year])
    y = np.log(df["output"].to_numpy())
    k = np.log(df["capital"].to_numpy())
    labour = np.log(df["labour"].to_numpy())
    if returns_to_scale == "constant":
        response = y - labour
        design = np.column_stack((np.ones(len(df)), k - labour))
    else:
        response = y
        design = np.column_stack((np.ones(len(df)), k, labour))
    if np.linalg.matrix_rank(design) != design.shape[1]:
        raise ModelEstimationError(
            "Regressors are collinear or constant; elasticities not identifiable"
        )
    coefficients, *_ = np.linalg.lstsq(design, response, rcond=None)
    log_a = float(coefficients[0])
    alpha = float(coefficients[1])
    beta = (
        (1 - alpha)
        if returns_to_scale == "constant"
        else float(coefficients[2])
    )
    log_prediction = log_a + alpha * k + beta * labour
    prediction = np.exp(log_prediction)
    if not np.isfinite(prediction).all():
        raise ModelEstimationError(
            "Predicted output overflowed; rescale the inputs"
        )
    actual = df["output"].to_numpy()
    level_residual = actual - prediction
    log_residual = y - log_prediction

    def r2(observed: np.ndarray, residual: np.ndarray) -> float:
        denominator = float(np.square(observed - observed.mean()).sum())
        if denominator <= 1e-24:
            raise ModelEstimationError(
                "Output has no usable variation; R-squared undefined"
            )
        return float(1 - np.square(residual).sum() / denominator)

    metrics = FitMetrics(
        observations=len(df),
        returns_to_scale=returns_to_scale,
        base_year=base_year,
        alpha_capital=alpha,
        beta_labour=beta,
        scale_factor=float(np.exp(log_a)),
        returns_to_scale_sum=alpha + beta,
        r_squared_level=r2(actual, level_residual),
        r_squared_log=r2(y, log_residual),
        rmse_level=float(np.sqrt(np.mean(np.square(level_residual)))),
        mae_level=float(np.mean(np.abs(level_residual))),
    )
    observations = df.assign(
        predicted_output=prediction,
        residual_output=level_residual,
        residual_log_output=log_residual,
    )
    return FitResult(metrics=metrics, observations=observations)

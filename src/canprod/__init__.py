"""CanProd: transparent, reproducible Canadian productivity research."""

from canprod.model import FitResult, fit_cobb_douglas, prepare_production_data
from canprod.statcan import SeriesSpec, StatCanClient

__version__ = "1.0.0"
__all__ = [
    "FitResult",
    "SeriesSpec",
    "StatCanClient",
    "fit_cobb_douglas",
    "prepare_production_data",
]

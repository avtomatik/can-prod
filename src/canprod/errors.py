"""Typed errors for predictable CLI and programmatic handling."""


class CanProdError(Exception):
    """Base error for data, schema, and modelling problems."""


class DataValidationError(CanProdError):
    """A source or model input violates an explicit contract."""


class DataUnavailableError(CanProdError):
    """The requested data are not cached and cannot be loaded."""


class ModelEstimationError(CanProdError):
    """Data cannot identify the requested regression."""

import pytest

from canprod.errors import DataUnavailableError, DataValidationError
from canprod.statcan import SeriesSpec, StatCanClient


def test_vector_filter_and_annual_aggregation(table_zip, tmp_path):
    table_zip()
    client = StatCanClient(cache_dir=tmp_path, offline=True)
    raw = client.read_vector(36100096, "V42")
    assert raw.shape[0] == 4
    assert raw["VALUE"].tolist() == [10, 20, 30, 40]
    assert raw["SCALAR_FACTOR"].unique().tolist() == ["millions"]
    mean = client.annual_series(SeriesSpec(36100096, "v42", "capital", "mean"))
    assert mean.to_dict() == {2020: 15.0, 2021: 35.0}
    total = client.annual_series(SeriesSpec(36100096, "v42", "capital", "sum"))
    assert total.to_dict() == {2020: 30.0, 2021: 70.0}
    last = client.annual_series(SeriesSpec(36100096, "v42", "capital", "last"))
    assert last.to_dict() == {2020: 20.0, 2021: 40.0}


def test_offline_miss(tmp_path):
    client = StatCanClient(cache_dir=tmp_path, offline=True)
    with pytest.raises(DataUnavailableError, match="No usable cached"):
        client.ensure_archive(36100096)


def test_old_cansim_id_rejected(tmp_path):
    with pytest.raises(DataValidationError, match="eight-digit"):
        SeriesSpec(3790031, "v42", "value", "mean")
    with pytest.raises(DataValidationError, match="eight-digit"):
        StatCanClient(tmp_path).archive_path(3790031)


def test_unknown_vector_rejected(table_zip, tmp_path):
    table_zip()
    with pytest.raises(DataValidationError, match="not found"):
        StatCanClient(tmp_path, offline=True).read_vector(36100096, "v777")


def test_missing_required_header(table_zip, tmp_path):
    table_zip(
        columns=[
            "REF_DATE",
            "GEO",
            "VECTOR",
            "MEASURE",
            "UOM",
            "SCALAR_FACTOR",
            "STATUS",
        ]
    )
    with pytest.raises(DataValidationError, match="missing"):
        StatCanClient(tmp_path, offline=True).read_vector(36100096, "v42")


def test_duplicate_dates_rejected(table_zip, tmp_path):
    table_zip(
        rows=[
            ["2020-01", "Canada", "v42", "10", "Dollars", "millions", ""],
            ["2020-01", "Canada", "v42", "20", "Dollars", "millions", ""],
        ]
    )
    with pytest.raises(DataValidationError, match="duplicate"):
        StatCanClient(tmp_path, offline=True).read_vector(36100096, "v42")


def test_unit_mixture_rejected(table_zip, tmp_path):
    table_zip(
        rows=[
            ["2020-01", "Canada", "v42", "10", "Dollars", "millions", ""],
            ["2020-02", "Canada", "v42", "20", "Dollars", "thousands", ""],
        ]
    )
    with pytest.raises(DataValidationError, match="mixes"):
        StatCanClient(tmp_path, offline=True).read_vector(36100096, "v42")


def test_cache_no_download_when_present(table_zip, tmp_path):
    expected = table_zip()
    client = StatCanClient(tmp_path, offline=True)
    assert client.ensure_archive(36100096) == expected


def test_refresh_offline_rejected(table_zip, tmp_path):
    table_zip()
    with pytest.raises(DataUnavailableError):
        StatCanClient(tmp_path, offline=True).ensure_archive(
            36100096, refresh=True
        )


def test_invalid_date_rejected(table_zip, tmp_path):
    table_zip(
        rows=[["FY2020/21", "Canada", "v42", "10", "Dollars", "millions", ""]]
    )
    with pytest.raises(DataValidationError, match="Unsupported REF_DATE"):
        StatCanClient(tmp_path, offline=True).annual_series(
            SeriesSpec(36100096, "v42", "capital", "mean")
        )


def test_download_is_streamed_and_committed(tmp_path, table_zip):
    original = table_zip()
    payload = original.read_bytes()
    original.unlink()

    class Response:
        status_code = 200

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            pass

        def raise_for_status(self):
            pass

        def iter_content(self, chunk_size):
            assert chunk_size > 0
            yield payload[:10]
            yield payload[10:]

    class Session:
        def get(self, url, **options):
            assert url.endswith("/36100096-eng.zip")
            assert options["stream"] is True
            assert options["allow_redirects"] is False
            return Response()

    client = StatCanClient(tmp_path, session=Session())
    assert client.ensure_archive(36100096).read_bytes() == payload


def test_size_limit_preserves_good_cache(tmp_path, table_zip):
    original = table_zip()
    data = original.read_bytes()

    class Response:
        status_code = 200

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            pass

        def raise_for_status(self):
            pass

        def iter_content(self, chunk_size):
            yield b"x" * 100

    class Session:
        def get(self, *_args, **_kwargs):
            return Response()

    with pytest.raises(DataUnavailableError, match="exceeds limit"):
        StatCanClient(
            tmp_path, max_archive_bytes=50, session=Session()
        ).ensure_archive(36100096, refresh=True)
    assert original.read_bytes() == data


def test_partial_years_require_explicit_opt_in(table_zip, tmp_path):
    table_zip(
        rows=[
            ["2020-01", "Canada", "v42", "1", "Index", "units", ""],
            ["2020-02", "Canada", "v42", "2", "Index", "units", ""],
            ["2021-01", "Canada", "v42", "3", "Index", "units", ""],
        ]
    )
    client = StatCanClient(tmp_path, offline=True)
    with pytest.raises(DataValidationError, match="fewer observations"):
        client.annual_series(SeriesSpec(36100096, "v42", "x", "sum"))
    series = client.annual_series(
        SeriesSpec(36100096, "v42", "x", "sum", allow_partial_years=True)
    )
    assert series.to_dict() == {2020: 3.0, 2021: 3.0}
    assert series.attrs["source_metadata"]["potential_partial_years"] == [2021]


def test_mixed_frequency_rejected(table_zip, tmp_path):
    table_zip(
        rows=[
            ["2020-01", "Canada", "v42", "1", "Index", "units", ""],
            ["2020-Q2", "Canada", "v42", "2", "Index", "units", ""],
        ]
    )
    with pytest.raises(
        DataValidationError, match="mixes reference-period frequencies"
    ):
        StatCanClient(tmp_path, offline=True).annual_series(
            SeriesSpec(36100096, "v42", "x", "mean", allow_partial_years=True)
        )

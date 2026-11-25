import csv
import io
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import pytest


@pytest.fixture
def table_zip(tmp_path: Path):
    """Create a tiny modern StatCan English ZIP for offline integration tests."""

    def create(table: int = 36100096, *, rows=None, columns=None) -> Path:
        if columns is None:
            columns = [
                "REF_DATE",
                "GEO",
                "VECTOR",
                "VALUE",
                "UOM",
                "SCALAR_FACTOR",
                "STATUS",
            ]
        if rows is None:
            rows = [
                ["2020-01", "Canada", "v42", "10", "Dollars", "millions", ""],
                ["2020-02", "Canada", "v42", "20", "Dollars", "millions", ""],
                ["2021-01", "Canada", "v42", "30", "Dollars", "millions", ""],
                ["2021-02", "Canada", "v42", "40", "Dollars", "millions", ""],
                ["2020-01", "Canada", "v99", "5", "Dollars", "millions", ""],
            ]
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(columns)
        writer.writerows(rows)
        zip_path = tmp_path / f"{table:08d}-eng.zip"
        with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as archive:
            archive.writestr(f"{table:08d}.csv", buf.getvalue())
            archive.writestr(f"{table:08d}_Metadata.csv", "metadata")
        return zip_path

    return create

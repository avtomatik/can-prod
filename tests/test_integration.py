"""End-to-end offline StatCan-like ZIPs -> aligned frame -> fitted output."""

import csv
import io
import json
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd

from canprod.cli import main


def test_build_fit_and_provenance_from_offline_archives(tmp_path):
    cache = tmp_path / "cache"
    cache.mkdir()
    components = [
        (36100096, "v201", "capital", "last"),
        (14100027, "v202", "labour", "mean"),
        (36100434, "v203", "output", "sum"),
    ]
    for table, vector, factor, _method in components:
        csvfile = io.StringIO()
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "REF_DATE",
                "GEO",
                "VECTOR",
                "VALUE",
                "UOM",
                "SCALAR_FACTOR",
                "STATUS",
            ]
        )
        for year in range(2010, 2020):
            t = year - 2010
            k = 100 + 4 * t + 1.2 * (t % 3)
            l = 60 + t + 0.3 * (t % 4)  # noqa: E741
            y = 1.4 * k**0.35 * l**0.65
            values = {"capital": k, "labour": l, "output": y / 2}
            # Two quarterly-like rows per year. Last/mean/sum all perform as configured.
            for month in ("01", "07"):
                writer.writerow(
                    [
                        f"{year}-{month}",
                        "Canada",
                        vector,
                        values[factor],
                        "Index",
                        "units",
                        "",
                    ]
                )
        with ZipFile(
            cache / f"{table:08d}-eng.zip", "w", compression=ZIP_DEFLATED
        ) as archive:
            archive.writestr(f"{table:08d}.csv", csvfile.getvalue())
    spec = {
        "title": "Synthetic integration fixture, NOT official StatCan data",
        "series": {
            factor: {
                "table_id": table,
                "vector": vector,
                "aggregation": method,
            }
            for table, vector, factor, method in components
        },
    }
    config = tmp_path / "verified-synthetic.json"
    config.write_text(json.dumps(spec))
    dest = tmp_path / "out"
    assert (
        main(
            [
                "build",
                "--spec",
                str(config),
                "--outdir",
                str(dest),
                "--cache-dir",
                str(cache),
                "--offline",
                "--fit",
                "--base-year",
                "2012",
            ]
        )
        == 0
    )
    data = pd.read_csv(dest / "production_data.csv")
    assert list(data.columns) == ["year", "capital", "labour", "output"]
    assert len(data) == 10
    metrics = json.loads((dest / "fit_metrics.json").read_text())
    assert abs(metrics["alpha_capital"] - 0.35) < 1e-10
    assert metrics["r_squared_level"] > 0.999999
    provenance = json.loads((dest / "provenance.json").read_text())
    assert provenance["year_coverage"] == {
        "first_year": 2010,
        "last_year": 2019,
        "aligned_years": 10,
    }
    assert len(provenance["series"]["capital"]["archive_sha256"]) == 64
    assert provenance["series"]["capital"]["metadata"]["observations"] == 20

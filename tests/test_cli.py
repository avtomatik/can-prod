import json
from pathlib import Path

import pandas as pd

from canprod.cli import main

ROOT = Path(__file__).resolve().parents[1]


def test_cli_synthetic_fit(tmp_path):
    output = tmp_path / "fit"
    result = main(
        [
            "fit",
            "--input",
            str(ROOT / "examples/synthetic_production.csv"),
            "--base-year",
            "2012",
            "--outdir",
            str(output),
        ]
    )
    assert result == 0
    metrics = json.loads((output / "fit_metrics.json").read_text())
    assert metrics["observations"] == 26
    assert metrics["base_year"] == 2012
    assert 0 < metrics["alpha_capital"] < 1
    assert (output / "fitted_observations.csv").exists()


def test_cli_legacy_series(tmp_path):
    output = tmp_path / "series.csv"
    result = main(
        [
            "legacy-series",
            "--input",
            str(
                ROOT / "data/legacy/dataset_can_cansim5245628780870031920.csv"
            ),
            "--vector",
            "v65201809",
            "--aggregation",
            "mean",
            "--out",
            str(output),
        ]
    )
    assert result == 0
    assert list(pd.read_csv(output).columns) == ["year", "v65201809"]


def test_cli_returns_nonzero_for_invalid_fit(tmp_path, capsys):
    path = tmp_path / "bad.csv"
    path.write_text("year,capital,labour,output\n2020,0,2,3\n")
    assert (
        main(["fit", "--input", str(path), "--outdir", str(tmp_path / "o")])
        == 2
    )
    assert "canprod:" in capsys.readouterr().err

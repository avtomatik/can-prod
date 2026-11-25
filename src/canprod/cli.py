"""Stable command-line interface: python -m canprod / canprod."""

import argparse
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

from canprod.errors import CanProdError
from canprod.legacy import legacy_annual_series
from canprod.model import fit_cobb_douglas
from canprod.statcan import SeriesSpec, StatCanClient
from canprod.workflow import ProductionSpec, build_production_frame


def _client(args: argparse.Namespace) -> StatCanClient:
    return StatCanClient(cache_dir=args.cache_dir, offline=args.offline)


def _save_series(series: pd.Series, path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    series.to_frame().to_csv(target, index=True)
    print(f"Wrote {target} ({len(series)} annual values)")


def _write_fit(
    data: pd.DataFrame, args: argparse.Namespace, outdir: Path
) -> None:
    result = fit_cobb_douglas(
        data,
        base_year=args.base_year,
        returns_to_scale=args.returns_to_scale,
        missing="drop" if args.drop_missing else "error",
    )
    outdir.mkdir(parents=True, exist_ok=True)
    result.observations.to_csv(outdir / "fitted_observations.csv", index=True)
    (outdir / "fit_metrics.json").write_text(
        json.dumps(result.metrics.to_dict(), indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    if args.plot:
        from canprod.plot import save_fit_plot

        save_fit_plot(result, outdir / "cobb_douglas_fit.png")
    print(json.dumps(result.metrics.to_dict(), indent=2, allow_nan=False))
    print(f"Wrote analysis to {outdir}")


def _source_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--cache-dir", type=Path, default=None, help="Cache for StatCan ZIPs"
    )
    parser.add_argument(
        "--offline", action="store_true", help="Never access the network"
    )
    parser.add_argument(
        "--refresh", action="store_true", help="Re-fetch ZIP even if cached"
    )


def _fit_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--base-year",
        type=int,
        default=None,
        help="Normalize all inputs to this year",
    )
    parser.add_argument(
        "--returns-to-scale", choices=["constant", "free"], default="constant"
    )
    parser.add_argument(
        "--drop-missing",
        action="store_true",
        help="Drop rows with null K/L/Y (never nonpositive)",
    )
    parser.add_argument(
        "--plot", action="store_true", help="Write optional PNG figure"
    )


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="canprod",
        description="Reproducible Canada production-function research",
    )
    parser.add_argument("--version", action="version", version="canprod 1.0.0")
    commands = parser.add_subparsers(dest="command", required=True)
    fit = commands.add_parser(
        "fit", help="Fit a Cobb–Douglas model to a three-series CSV"
    )
    fit.add_argument("--input", type=Path, required=True)
    fit.add_argument("--outdir", type=Path, required=True)
    _fit_args(fit)
    build = commands.add_parser(
        "build",
        help="Download/align three explicitly specified StatCan vectors",
    )
    build.add_argument(
        "--spec",
        type=Path,
        required=True,
        help="JSON production series definitions",
    )
    build.add_argument("--outdir", type=Path, required=True)
    build.add_argument(
        "--fit", action="store_true", help="Fit the aligned data as well"
    )
    _source_args(build)
    _fit_args(build)
    fetch = commands.add_parser(
        "fetch-series", help="Download and annualize one StatCan vector"
    )
    fetch.add_argument(
        "--table", type=int, required=True, help="Eight-digit StatCan PID"
    )
    fetch.add_argument("--vector", required=True, help="Vector e.g. v123456")
    fetch.add_argument("--name", default="value")
    fetch.add_argument(
        "--aggregation", required=True, choices=["mean", "sum", "last"]
    )
    fetch.add_argument(
        "--allow-partial-years",
        action="store_true",
        help="Permit incomplete annual periods after inspecting source coverage",
    )
    fetch.add_argument("--out", type=Path, required=True)
    _source_args(fetch)
    legacy = commands.add_parser(
        "legacy-series", help="Read bundled historical Monthly CANSIM CSV"
    )
    legacy.add_argument("--input", type=Path, required=True)
    legacy.add_argument("--vector", required=True)
    legacy.add_argument(
        "--aggregation", required=True, choices=["mean", "sum", "last"]
    )
    legacy.add_argument("--out", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = make_parser().parse_args(argv)
    try:
        if args.command == "fit":
            frame = pd.read_csv(args.input)
            _write_fit(frame, args, args.outdir)
        elif args.command == "build":
            spec = ProductionSpec.from_file(args.spec)
            client = _client(args)
            frame = build_production_frame(spec, client, refresh=args.refresh)
            args.outdir.mkdir(parents=True, exist_ok=True)
            frame.to_csv(args.outdir / "production_data.csv", index=True)
            provenance = spec.provenance()
            provenance["year_coverage"] = {
                "first_year": int(frame.index.min()),
                "last_year": int(frame.index.max()),
                "aligned_years": len(frame),
            }
            for name, source in provenance["series"].items():
                archive = client.archive_path(source["table_id"])
                if archive.exists():
                    sha = hashlib.sha256()
                    with archive.open("rb") as stream:
                        for chunk in iter(
                            lambda: stream.read(1024 * 1024), b""
                        ):
                            sha.update(chunk)
                    source["archive_sha256"] = sha.hexdigest()
                source["metadata"] = frame.attrs.get(
                    "source_metadata", {}
                ).get(name, {})
            (args.outdir / "provenance.json").write_text(
                json.dumps(provenance, indent=2, allow_nan=False) + "\n",
                encoding="utf-8",
            )
            print(
                f"Wrote {len(frame)} aligned years to {args.outdir / 'production_data.csv'}"
            )
            if args.fit:
                _write_fit(frame, args, args.outdir)
        elif args.command == "fetch-series":
            spec = SeriesSpec(
                args.table,
                args.vector,
                args.name,
                args.aggregation,
                args.allow_partial_years,
            )
            _save_series(
                _client(args).annual_series(spec, refresh=args.refresh),
                args.out,
            )
        elif args.command == "legacy-series":
            _save_series(
                legacy_annual_series(
                    args.input, args.vector, aggregation=args.aggregation
                ),
                args.out,
            )
        else:
            raise AssertionError(f"Unknown subcommand: {args.command}")
    except (
        CanProdError,
        OSError,
        ValueError,
        pd.errors.ParserError,
        RuntimeError,
    ) as exc:
        print(f"canprod: {exc}", file=sys.stderr)
        return 2
    return 0

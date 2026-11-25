"""Optional, non-interactive publication-ready figure for an estimation result."""

from pathlib import Path

from canprod.model import FitResult


def save_fit_plot(result: FitResult, target: str | Path) -> None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        from matplotlib import pyplot as plt
    except ImportError as exc:
        raise RuntimeError(
            "Plotting requires 'pip install canprod[plot]'"
        ) from exc
    df = result.observations
    fig, ax = plt.subplots(figsize=(10, 5.5), constrained_layout=True)
    ax.plot(
        df.index,
        df["output"],
        marker="o",
        linewidth=1.6,
        label="Observed output",
    )
    ax.plot(
        df.index, df["predicted_output"], linewidth=2, label="Estimated output"
    )
    ax.set(xlabel="Year", ylabel="Output (input units or base-year index)")
    ax.set_title("Cobb–Douglas fit · descriptive OLS")
    ax.grid(alpha=0.25)
    ax.legend()
    dest = Path(target)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=180)
    plt.close(fig)

#!/usr/bin/env python3
"""Build an interactive Plotly dashboard from CSV metrics."""

from __future__ import annotations

import argparse
from pathlib import Path


def build_dashboard(csv_path: Path, output_html: Path) -> None:
    import pandas as pd
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    df = pd.read_csv(csv_path, parse_dates=["date"])

    trend = px.line(df, x="date", y="revenue", color="region", title="Revenue Trend")
    mix = px.bar(df, x="region", y="orders", color="channel", barmode="group", title="Orders by Region/Channel")
    scatter = px.scatter(
        df,
        x="orders",
        y="revenue",
        color="region",
        size="ad_spend",
        title="Orders vs Revenue",
        hover_data=["channel"],
    )

    fig = make_subplots(rows=3, cols=1, subplot_titles=["Trend", "Mix", "Correlation"])

    for trace in trend.data:
        fig.add_trace(trace, row=1, col=1)
    for trace in mix.data:
        fig.add_trace(trace, row=2, col=1)
    for trace in scatter.data:
        fig.add_trace(trace, row=3, col=1)

    fig.update_layout(height=1200, title_text="Business Dashboard", template="plotly_white")
    fig.write_html(output_html)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path, help="Input CSV path")
    parser.add_argument("--out", type=Path, default=Path("dashboard.html"), help="Output HTML path")
    args = parser.parse_args()

    build_dashboard(args.csv, args.out)
    print(f"Dashboard saved to {args.out}")


if __name__ == "__main__":
    main()

"""Chart Module Q7: Transit Hub Ratio per Thousand Housing Units by Borough.

Answers: Which boroughs feature the greatest density of transit facilities per residential unit?
Type: Ranked Horizontal Bar Chart.
"""

import pandas as pd
import plotly.graph_objects as go
from src.charts.theme import apply_citylink_theme, BOROUGH_COLORS


def build_chart(df: pd.DataFrame) -> go.Figure:
    """Build the Q7 Transit Hub Ratio horizontal bar chart."""
    if df.empty:
        fig = go.Figure()
        return apply_citylink_theme(fig, "Q7: Transit Density Ratio", note="No data available.")

    # Calculate ratio: (average station density * 1000) / total units per borough
    grouped = df.groupby("borough").agg({
        "residential_units": "sum",
        "subway_station_density": "mean",
        "transit_accessibility_score": "mean"
    }).reset_index()

    # Ratio: Station index normalized per 1,000 residential units
    grouped["ratio"] = (grouped["subway_station_density"] / (grouped["residential_units"] / 1000.0)).round(2)
    grouped = grouped.sort_values("ratio", ascending=True)

    colors = [BOROUGH_COLORS.get(b, "#00F2FE") for b in grouped["borough"]]

    fig = go.Figure(
        data=go.Bar(
            x=grouped["ratio"],
            y=grouped["borough"],
            orientation="h",
            marker=dict(color=colors, line=dict(color="rgba(255,255,255,0.2)", width=1)),
            text=grouped["ratio"].apply(lambda v: f"{v:.2f} idx"),
            textposition="auto",
            hovertemplate="<b>%{y}</b><br>Transit Density Ratio: %{x:.2f} hubs / 1k units<extra></extra>"
        )
    )

    return apply_citylink_theme(
        fig=fig,
        title="Q7: Transit Facility Density per 1,000 Residential Units",
        x_title="Transit Hub Density Ratio (Index)",
        y_title="NYC Borough",
        note="Normalizes public transit infrastructure against newly built housing volume."
    )

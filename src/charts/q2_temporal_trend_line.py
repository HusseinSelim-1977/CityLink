"""Chart Module Q2: Temporal Trends in Housing Units & Transit Ridership (2018-2024).

Answers: How have residential completions trended alongside transit ridership over time?
Type: Multi-trace Line Chart with markers.
"""

import pandas as pd
import plotly.graph_objects as go
from src.charts.theme import apply_citylink_theme, COLOR_TRANSIT, COLOR_HOUSING


def build_chart(df: pd.DataFrame) -> go.Figure:
    """Build the Q2 Housing vs Transit Ridership temporal line chart."""
    if df.empty:
        fig = go.Figure()
        return apply_citylink_theme(fig, "Q2: Temporal Trends (2018-2024)", note="No data matching active filters.")

    # Aggregate by year
    yearly = df.groupby("year").agg({
        "residential_units": "sum",
        "transit_ridership_m": "sum"
    }).reset_index().sort_values("year")

    fig = go.Figure()

    # Trace 1: Residential Units (Left Axis)
    fig.add_trace(
        go.Scatter(
            x=yearly["year"],
            y=yearly["residential_units"],
            name="Residential Units",
            mode="lines+markers",
            line=dict(color=COLOR_HOUSING, width=3),
            marker=dict(size=8, color=COLOR_HOUSING, symbol="circle"),
            hovertemplate="Year: %{x}<br>Residential Units: %{y:,.0f}<extra></extra>",
            yaxis="y1"
        )
    )

    # Trace 2: Transit Ridership (Right Axis)
    fig.add_trace(
        go.Scatter(
            x=yearly["year"],
            y=yearly["transit_ridership_m"],
            name="Transit Ridership (M)",
            mode="lines+markers",
            line=dict(color=COLOR_TRANSIT, width=3, dash="dot"),
            marker=dict(size=8, color=COLOR_TRANSIT, symbol="diamond"),
            hovertemplate="Year: %{x}<br>Ridership: %{y:.1f}M Trips<extra></extra>",
            yaxis="y2"
        )
    )

    # Dual axis layout
    fig.update_layout(
        yaxis=dict(
            title=dict(text="Total Residential Units", font=dict(color=COLOR_HOUSING)),
            tickfont=dict(color=COLOR_HOUSING),
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.05)"
        ),
        yaxis2=dict(
            title=dict(text="Annual Transit Ridership (Millions)", font=dict(color=COLOR_TRANSIT)),
            tickfont=dict(color=COLOR_TRANSIT),
            overlaying="y",
            side="right",
            showgrid=False
        )
    )

    return apply_citylink_theme(
        fig=fig,
        title="Q2: Housing Completions vs Transit Ridership (2018–2024)",
        x_title="Calendar Year",
        note="Tracks multi-year development momentum against public transit demand."
    )

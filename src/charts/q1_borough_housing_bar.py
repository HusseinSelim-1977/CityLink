"""Chart Module Q1: New Residential Housing Units by NYC Borough.

Answers: How do residential housing completions and authorizations compare across the 5 boroughs?
Type: Grouped & Styled Bar Chart.
"""

import pandas as pd
import plotly.graph_objects as go
from src.charts.theme import apply_citylink_theme, BOROUGH_COLORS


def build_chart(df: pd.DataFrame) -> go.Figure:
    """Build the Q1 Borough Housing Units bar chart."""
    if df.empty:
        fig = go.Figure()
        return apply_citylink_theme(fig, "Q1: Residential Units by Borough", note="No data matching active filters.")

    # Aggregate total units by borough and housing category
    grouped = df.groupby(["borough", "housing_category"])["residential_units"].sum().reset_index()

    fig = go.Figure()

    # Create stacked or grouped bars per housing category
    categories = grouped["housing_category"].unique()
    colors = ["#00F2FE", "#FF6B6B", "#A855F7", "#F59E0B"]

    for idx, cat in enumerate(categories):
        sub = grouped[grouped["housing_category"] == cat]
        fig.add_trace(
            go.Bar(
                x=sub["borough"],
                y=sub["residential_units"],
                name=cat,
                marker=dict(
                    color=colors[idx % len(colors)],
                    line=dict(width=1, color="rgba(255,255,255,0.15)")
                ),
                hovertemplate="<b>%{x}</b><br>Category: " + cat + "<br>Units: %{y:,.0f}<extra></extra>"
            )
        )

    fig.update_layout(barmode="stack")

    return apply_citylink_theme(
        fig=fig,
        title="Q1: Residential Housing Units by Borough",
        x_title="NYC Borough",
        y_title="Total Residential Units (Count)",
        note="Aggregated from NYC housing development filings. Stacked by development category."
    )

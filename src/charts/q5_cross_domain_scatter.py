"""Chart Module Q5: Cross-Domain Relationship: Housing Density vs Average Commute Times.

Answers: What is the observed correlation between residential volume and local transit commute times?
Type: Cross-domain Scatter Plot with Ordinary Least Squares (OLS) Trendline and Pearson r.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from src.charts.theme import apply_citylink_theme, BOROUGH_COLORS, COLOR_NEXUS


def build_chart(df: pd.DataFrame) -> go.Figure:
    """Build the Q5 Cross-domain scatter plot with correlation and trendline."""
    if df.empty or len(df) < 3:
        fig = go.Figure()
        return apply_citylink_theme(
            fig,
            "Q5: Housing Density vs Commute Times",
            note="Insufficient data points to compute correlation."
        )

    # Aggregate by neighborhood and year for granular scatter
    scatter_df = df.groupby(["neighborhood", "borough", "year"]).agg({
        "residential_units": "sum",
        "avg_commute_time_min": "mean",
        "transit_accessibility_score": "mean"
    }).reset_index()

    x_vals = scatter_df["residential_units"].values
    y_vals = scatter_df["avg_commute_time_min"].values

    # Compute Pearson correlation coefficient r and linear fit
    corr_coef = 0.0
    slope, intercept = 0.0, 0.0
    r_squared = 0.0
    if len(x_vals) > 1 and np.std(x_vals) > 0 and np.std(y_vals) > 0:
        corr_matrix = np.corrcoef(x_vals, y_vals)
        corr_coef = corr_matrix[0, 1]
        poly = np.polyfit(x_vals, y_vals, deg=1)
        slope, intercept = poly[0], poly[1]
        r_squared = corr_coef ** 2

    fig = go.Figure()

    # Traces per borough
    for borough in scatter_df["borough"].unique():
        sub = scatter_df[scatter_df["borough"] == borough]
        color = BOROUGH_COLORS.get(borough, "#00F2FE")

        fig.add_trace(
            go.Scatter(
                x=sub["residential_units"],
                y=sub["avg_commute_time_min"],
                mode="markers",
                name=borough,
                marker=dict(size=9, color=color, opacity=0.75, line=dict(width=1, color="rgba(255,255,255,0.2)")),
                text=sub["neighborhood"],
                customdata=sub["year"],
                hovertemplate=(
                    "<b>%{text}</b> (%{data.name})<br>"
                    "Year: %{customdata}<br>"
                    "Units: %{x:,.0f}<br>"
                    "Avg Commute: %{y:.1f} min<extra></extra>"
                )
            )
        )

    # Add OLS Trendline if correlation calculated
    if len(x_vals) > 1 and np.std(x_vals) > 0:
        x_trend = np.linspace(x_vals.min(), x_vals.max(), 50)
        y_trend = slope * x_trend + intercept

        fig.add_trace(
            go.Scatter(
                x=x_trend,
                y=y_trend,
                mode="lines",
                name=f"OLS Trendline (r = {corr_coef:.2f})",
                line=dict(color=COLOR_NEXUS, width=2.5, dash="dash"),
                hoverinfo="skip"
            )
        )

    # Annotated correlation banner
    fig.add_annotation(
        text=f"<b>Pearson r:</b> {corr_coef:+.2f} &nbsp;|&nbsp; <b>R²:</b> {r_squared:.2f}",
        xref="paper",
        yref="paper",
        x=0.98,
        y=0.04,
        showarrow=False,
        font=dict(size=11, color="#FFFFFF"),
        bgcolor="rgba(15, 17, 26, 0.85)",
        bordercolor="rgba(168, 85, 247, 0.4)",
        borderwidth=1,
        borderpad=6
    )

    return apply_citylink_theme(
        fig=fig,
        title="Q5: Cross-Domain Correlation: Housing Volume vs Commute Time",
        x_title="Residential Housing Units (Volume)",
        y_title="Average Commute Time (Minutes)",
        note="Non-causal relationship. Statistical correlation reflects spatial clustering, not direct causation."
    )

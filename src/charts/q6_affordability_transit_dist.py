"""Chart Module Q6: Transit Accessibility Distribution across Housing Categories.

Answers: How does transit connectivity distribute across affordable vs market-rate projects?
Type: Styled Box Plot showing medians, interquartile ranges, and variance.
"""

import pandas as pd
import plotly.graph_objects as go
from src.charts.theme import apply_citylink_theme


def build_chart(df: pd.DataFrame) -> go.Figure:
    """Build the Q6 Box plot distribution."""
    if df.empty:
        fig = go.Figure()
        return apply_citylink_theme(fig, "Q6: Transit Accessibility Distribution", note="No data available.")

    fig = go.Figure()

    palette = ["#00F2FE", "#FF6B6B", "#A855F7", "#F59E0B"]
    categories = df["housing_category"].unique()

    for idx, cat in enumerate(categories):
        sub = df[df["housing_category"] == cat]
        color = palette[idx % len(palette)]

        fig.add_trace(
            go.Box(
                y=sub["transit_accessibility_score"],
                name=cat,
                boxmean=True,
                marker=dict(color=color),
                line=dict(color=color, width=1.5),
                hovertemplate="<b>" + cat + "</b><br>Accessibility Score: %{y:.1f}/100<extra></extra>"
            )
        )

    return apply_citylink_theme(
        fig=fig,
        title="Q6: Transit Accessibility Score Distribution by Project Type",
        x_title="Housing Project Classification",
        y_title="Transit Accessibility Index (0–100)",
        note="Dashed lines inside boxes indicate group means; solid lines show medians (IQR)."
    )

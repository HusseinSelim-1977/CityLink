"""Chart Module Q3: Transit Accessibility Score Heatmap across Housing Categories & Boroughs.

Answers: How does transit connectivity index vary by housing development type across boroughs?
Type: 2D Density Heatmap.
"""

import pandas as pd
import plotly.graph_objects as go
from src.charts.theme import apply_citylink_theme


def build_chart(df: pd.DataFrame) -> go.Figure:
    """Build the Q3 Heatmap matrix."""
    if df.empty:
        fig = go.Figure()
        return apply_citylink_theme(fig, "Q3: Transit Accessibility Heatmap", note="No data matching active filters.")

    # Pivot table: Housing category x Borough -> Mean accessibility score
    pivot = df.pivot_table(
        index="housing_category",
        columns="borough",
        values="transit_accessibility_score",
        aggfunc="mean"
    ).round(1)

    # Matrix values
    z_data = pivot.values
    x_labels = list(pivot.columns)
    y_labels = list(pivot.index)

    fig = go.Figure(
        data=go.Heatmap(
            z=z_data,
            x=x_labels,
            y=y_labels,
            colorscale=[
                [0.0, "#08090E"],
                [0.3, "#1E1B4B"],
                [0.6, "#7928CA"],
                [0.85, "#00F2FE"],
                [1.0, "#FFFFFF"]
            ],
            colorbar=dict(
                title=dict(text="Score (0-100)", font=dict(color="#94A3B8", size=10)),
                tickfont=dict(color="#94A3B8", size=9),
                len=0.8
            ),
            text=z_data,
            texttemplate="%{text}",
            textfont=dict(size=12, color="#FFFFFF"),
            hovertemplate="<b>Borough:</b> %{x}<br><b>Category:</b> %{y}<br><b>Accessibility Score:</b> %{z}/100<extra></extra>"
        )
    )

    return apply_citylink_theme(
        fig=fig,
        title="Q3: Transit Accessibility Score Matrix (0–100)",
        x_title="NYC Borough",
        y_title="Housing Development Category",
        note="Higher scores indicate superior transit frequency, subway density, and shorter walk radii."
    )

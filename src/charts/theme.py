"""Unified Plotly Chart Styling Theme for CityLink.

Applies the 'Midnight Metropolitan' aesthetic across all data visualizations,
ensuring consistent typography, transparent backgrounds, accessible contrast,
and descriptive hover labels.
"""

from typing import Optional
import plotly.graph_objects as go

# Canonical Palette
COLOR_HOUSING = "#FF6B6B"       # Warm Coral
COLOR_TRANSIT = "#00F2FE"       # Electric Cyan
COLOR_NEXUS = "#A855F7"         # Nexus Violet
COLOR_ACCENT = "#F59E0B"        # Amber
COLOR_SUCCESS = "#10B981"       # Emerald
COLOR_MUTED = "#64748B"         # Slate 500
COLOR_GRID = "rgba(255, 255, 255, 0.07)"
COLOR_ZERO = "rgba(255, 255, 255, 0.15)"
COLOR_TEXT = "#F1F5F9"          # Slate 100
COLOR_SUBTEXT = "#94A3B8"       # Slate 400

BOROUGH_COLORS = {
    "Manhattan": "#A855F7",
    "Brooklyn": "#00F2FE",
    "Queens": "#FF6B6B",
    "Bronx": "#F59E0B",
    "Staten Island": "#10B981"
}


def apply_citylink_theme(
    fig: go.Figure,
    title: str,
    x_title: Optional[str] = None,
    y_title: Optional[str] = None,
    note: Optional[str] = None,
    height: int = 400
) -> go.Figure:
    """Apply the high-craft CityLink visual theme to any Plotly figure."""
    annotations = list(fig.layout.annotations) if fig.layout.annotations else []

    if note:
        annotations.append(
            dict(
                text=f"<i>Note: {note}</i>",
                xref="paper",
                yref="paper",
                x=0.0,
                y=-0.22,
                showarrow=False,
                font=dict(size=10, color=COLOR_MUTED),
                align="left"
            )
        )

    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=15, color=COLOR_TEXT, family="system-ui, -apple-system, sans-serif"),
            x=0.02,
            y=0.96
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=50, r=30, t=55, b=65 if note else 45),
        font=dict(family="system-ui, -apple-system, sans-serif", color=COLOR_TEXT, size=11),
        hoverlabel=dict(
            bgcolor="#0F111A",
            bordercolor="rgba(0, 242, 254, 0.4)",
            font=dict(family="system-ui, -apple-system, sans-serif", size=12, color="#FFFFFF")
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
            font=dict(size=11, color=COLOR_SUBTEXT),
            bgcolor="rgba(0,0,0,0)"
        ),
        annotations=annotations
    )

    if x_title:
        fig.update_xaxes(
            title=dict(text=x_title, font=dict(size=11, color=COLOR_SUBTEXT)),
            showgrid=True,
            gridcolor=COLOR_GRID,
            zeroline=True,
            zerolinecolor=COLOR_ZERO,
            tickfont=dict(size=10, color=COLOR_SUBTEXT)
        )

    if y_title:
        fig.update_yaxes(
            title=dict(text=y_title, font=dict(size=11, color=COLOR_SUBTEXT)),
            showgrid=True,
            gridcolor=COLOR_GRID,
            zeroline=True,
            zerolinecolor=COLOR_ZERO,
            tickfont=dict(size=10, color=COLOR_SUBTEXT)
        )

    return fig

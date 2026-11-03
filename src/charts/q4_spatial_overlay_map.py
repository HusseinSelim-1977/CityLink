"""Chart Module Q4: Spatial Geo-Overlay of Housing Developments & Transit Density.

Answers: Where are new residential projects located relative to transit nodes in NYC?
Type: Scatter Map with carto-darkmatter basemap (Zero API token required).
Supports Plotly 6/7+ Scattermap and legacy Scattermapbox.
"""

import pandas as pd
import plotly.graph_objects as go
from src.charts.theme import apply_citylink_theme, BOROUGH_COLORS

# Compatibility for Plotly 7+ (Scattermap) and legacy (Scattermapbox)
ScatterMapClass = getattr(go, "Scattermap", getattr(go, "Scattermapbox", None))


def build_chart(df: pd.DataFrame) -> go.Figure:
    """Build the Q4 Spatial Map visualization."""
    if df.empty or "latitude" not in df.columns or ScatterMapClass is None:
        fig = go.Figure()
        return apply_citylink_theme(fig, "Q4: Spatial Housing & Transit Map", note="No geographic data available.")

    # Aggregate by neighborhood to prevent overplotting
    geo_df = df.groupby(["neighborhood", "borough"]).agg({
        "latitude": "mean",
        "longitude": "mean",
        "residential_units": "sum",
        "transit_accessibility_score": "mean",
        "subway_station_density": "mean"
    }).reset_index()

    fig = go.Figure()

    # Add bubbles per borough
    for borough in geo_df["borough"].unique():
        sub = geo_df[geo_df["borough"] == borough]
        color = BOROUGH_COLORS.get(borough, "#00F2FE")
        
        # Scale marker size proportionally
        marker_sizes = (sub["residential_units"] / sub["residential_units"].max() * 26 + 8).tolist()

        fig.add_trace(
            ScatterMapClass(
                lat=sub["latitude"],
                lon=sub["longitude"],
                mode="markers+text",
                name=borough,
                marker=dict(
                    size=marker_sizes,
                    color=color,
                    opacity=0.85
                ),
                text=sub["neighborhood"],
                textposition="top right",
                textfont=dict(size=9, color="#E2E8F0"),
                customdata=list(zip(sub["residential_units"], sub["transit_accessibility_score"], sub["subway_station_density"])),
                hovertemplate=(
                    "<b>%{text}</b> (%{data.name})<br>"
                    "Total Housing Units: %{customdata[0]:,.0f}<br>"
                    "Transit Accessibility: %{customdata[1]:.1f}/100<br>"
                    "Station Density: %{customdata[2]:.2f} / sq mi<extra></extra>"
                )
            )
        )

    # Configure Carto Dark Matter style (no token required)
    map_config = dict(
        style="carto-darkmatter",
        center=dict(lat=40.725, lon=-73.94),
        zoom=9.8
    )

    if hasattr(go, "Scattermap"):
        fig.update_layout(map=map_config)
    else:
        fig.update_layout(mapbox=map_config)

    return apply_citylink_theme(
        fig=fig,
        title="Q4: Spatial Overlay: Housing Projects vs Transit Density",
        note="Bubble size indicates cumulative residential units. Powered by Carto Darkmatter basemap tiles."
    )

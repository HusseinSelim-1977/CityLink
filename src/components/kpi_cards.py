"""KPI Telemetry Cards Component for CityLink.

Renders four glassmorphic metric cards with animated numbers and
subtext indicators, plus an automatic verification fixture notice.
"""

from typing import Dict, Any
from dash import html


def render_kpi_cards(kpi_data: Dict[str, Any]) -> html.Div:
    """Generate the 4-card KPI telemetry row from computed data."""
    total_units = kpi_data.get("total_units", 0)
    avg_commute = kpi_data.get("avg_commute_time", 0.0)
    avg_access = kpi_data.get("avg_accessibility", 0.0)
    ridership = kpi_data.get("total_ridership_m", 0.0)
    is_fixture = kpi_data.get("is_fixture", False)

    fixture_badge = None
    if is_fixture:
        fixture_badge = html.Div(
            style={
                "background": "rgba(245, 158, 11, 0.12)",
                "border": "1px solid rgba(245, 158, 11, 0.3)",
                "borderRadius": "9999px",
                "padding": "0.35rem 1rem",
                "color": "#FBBF24",
                "fontSize": "0.75rem",
                "display": "inline-flex",
                "alignItems": "center",
                "gap": "0.5rem",
                "marginBottom": "1rem"
            },
            children=[
                html.Span("ℹ", style={"fontWeight": "bold"}),
                html.Span("Verification Fixture Loaded (Awaiting live src.data pipeline integration)")
            ]
        )

    cards = [
        # Card 1: Housing Units
        html.Div(
            className="kpi-card housing",
            children=[
                html.Div("Total Residential Units", className="kpi-label"),
                html.Div(
                    f"{total_units:,}",
                    className="kpi-value kpi-number-animate",
                    **{"data-target-val": str(total_units), "data-is-decimal": "false"}
                ),
                html.Div("Permitted & completed housing units", className="kpi-subtext")
            ]
        ),
        # Card 2: Commute Time
        html.Div(
            className="kpi-card transit",
            children=[
                html.Div("Mean Commute Duration", className="kpi-label"),
                html.Div(
                    f"{avg_commute:.1f} min",
                    className="kpi-value kpi-number-animate",
                    **{"data-target-val": str(avg_commute), "data-is-decimal": "true"}
                ),
                html.Div("Average one-way transit commute time", className="kpi-subtext")
            ]
        ),
        # Card 3: Transit Accessibility
        html.Div(
            className="kpi-card nexus",
            children=[
                html.Div("Transit Access Index", className="kpi-label"),
                html.Div(
                    f"{avg_access:.1f} / 100",
                    className="kpi-value kpi-number-animate",
                    **{"data-target-val": str(avg_access), "data-is-decimal": "true"}
                ),
                html.Div("Composite walkability & subway density", className="kpi-subtext")
            ]
        ),
        # Card 4: Transit Ridership
        html.Div(
            className="kpi-card amber",
            children=[
                html.Div("Annual Transit Trips", className="kpi-label"),
                html.Div(
                    f"{ridership:.1f} M",
                    className="kpi-value kpi-number-animate",
                    **{"data-target-val": str(ridership), "data-is-decimal": "true"}
                ),
                html.Div("Estimated annual public transit trips", className="kpi-subtext")
            ]
        ),
    ]

    return html.Div([
        fixture_badge,
        html.Div(className="kpi-container", children=cards)
    ])

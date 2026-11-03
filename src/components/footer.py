"""Shared Footer Component for CityLink.

Provides contextual provenance, course information, and attribution.
"""

from dash import html


def render_footer() -> html.Footer:
    """Generate the standardized application footer."""
    return html.Footer(
        className="citylink-footer",
        children=[
            html.Div(
                style={"maxWidth": "1200px", "margin": "0 auto", "display": "flex", "flexDirection": "column", "gap": "1rem"},
                children=[
                    html.Div([
                        html.Span("CityLink", style={"fontWeight": "800", "color": "#F8FAFC"}),
                        html.Span(" — An interactive data-storytelling portal exploring the nexus of NYC Housing and Transit networks."),
                    ]),
                    html.Div(
                        style={"color": "#64748B", "fontSize": "0.8rem"},
                        children=[
                            html.Span("Built for the GIU course "),
                            html.Strong("Data Engineering and Visualization", style={"color": "#94A3B8"}),
                            html.Span(" (Winter 2026, due 9 Nov 2026). "),
                            html.Span("Source data powered by "),
                            html.Strong("NYC Open Data", style={"color": "#94A3B8"}),
                            html.Span(" (DOB, HPD, MTA)."),
                        ]
                    ),
                    html.Div(
                        style={"display": "flex", "justifyContent": "center", "gap": "1.5rem", "fontSize": "0.75rem", "color": "#475569"},
                        children=[
                            html.Span("Zero Runtime CDN Dependencies"),
                            html.Span("•"),
                            html.Span("Plotly & Three.js Accelerated"),
                            html.Span("•"),
                            html.Span("Non-Causal Statistical Disclaimers Honored"),
                        ]
                    )
                ]
            )
        ]
    )

"""Team & Contributions Page for CityLink.

Course: GIU Data Engineering and Visualization (Winter 2026).
Provides structured profile cards and contribution portfolios for the
4-member development team, with clean placeholders for names and student IDs.
"""

import dash
from dash import html

dash.register_page(__name__, path="/team", title="CityLink — Development Team")

TEAM_MEMBERS = [
    {
        "name": "[Team Member 1 - Insert Full Name]",
        "student_id": "ID: [Insert Student ID]",
        "role": "Lead Data Engineer & Pipeline Architect",
        "badge_color": "#FF6B6B",
        "contributions": [
            "Architected NYC DOB and HPD data ingestion pipelines.",
            "Standardized historical building permits and occupancy certificates.",
            "Formulated research inquiries for Q1 (Borough Volumes) and Q2 (Multi-Year Trends)."
        ]
    },
    {
        "name": "[Team Member 2 - Insert Full Name]",
        "student_id": "ID: [Insert Student ID]",
        "role": "Spatial Analyst & GIS Specialist",
        "badge_color": "#00F2FE",
        "contributions": [
            "Conducted geospatial spatial joins between NTA boundaries and subway hubs.",
            "Engineered the Carto Darkmatter Mapbox overlay (Q4) and accessibility heatmap (Q3).",
            "Harmonized EPSG:4326 coordinate projections and spatial bounds."
        ]
    },
    {
        "name": "[Team Member 3 - Insert Full Name]",
        "student_id": "ID: [Insert Student ID]",
        "role": "Senior Frontend & Interactive Systems Engineer",
        "badge_color": "#A855F7",
        "contributions": [
            "Constructed the multi-page Dash application architecture and client bridge.",
            "Designed the 'Midnight Metropolitan' aesthetic, CSS design system, and bento grids.",
            "Engineered the procedural Three.js 3D city canvas and Anime.js micro-interactions."
        ]
    },
    {
        "name": "[Team Member 4 - Insert Full Name]",
        "student_id": "ID: [Insert Student ID]",
        "role": "Quantitative Analyst & Statistical Modeler",
        "badge_color": "#F59E0B",
        "contributions": [
            "Implemented cross-domain OLS correlation models (Q5) and non-causal validation.",
            "Designed distribution analysis for affordable housing connectivity (Q6).",
            "Synthesized multi-category treemap decomposition and ratio metrics (Q7, Q8)."
        ]
    }
]


def layout():
    """Render the Development Team page layout."""
    cards = []
    for member in TEAM_MEMBERS:
        cards.append(
            html.Div(
                className="bento-card",
                children=[
                    html.Div(
                        style={"display": "flex", "justifyContent": "space-between", "alignItems": "flex-start", "marginBottom": "1rem"},
                        children=[
                            html.Div([
                                html.H3(member["name"], style={"fontSize": "1.25rem", "fontWeight": "800", "color": "#FFFFFF", "margin": "0 0 0.25rem 0"}),
                                html.Div(member["student_id"], style={"fontSize": "0.85rem", "color": "#94A3B8", "fontFamily": "var(--font-mono)"})
                            ]),
                            html.Span(
                                member["role"].split()[0],
                                style={
                                    "background": f"{member['badge_color']}20",
                                    "color": member["badge_color"],
                                    "border": f"1px solid {member['badge_color']}40",
                                    "borderRadius": "9999px",
                                    "padding": "0.25rem 0.75rem",
                                    "fontSize": "0.75rem",
                                    "fontWeight": "700"
                                }
                            )
                        ]
                    ),
                    html.Div(member["role"], style={"fontSize": "0.95rem", "fontWeight": "600", "color": "#E2E8F0", "marginBottom": "1rem"}),
                    html.Div(
                        style={"borderTop": "1px solid rgba(255, 255, 255, 0.08)", "paddingTop": "1rem"},
                        children=[
                            html.Div("Key Responsibilities & Deliverables:", style={"fontSize": "0.75rem", "fontWeight": "700", "letterSpacing": "0.05em", "color": "#64748B", "textTransform": "uppercase", "marginBottom": "0.5rem"}),
                            html.Ul(
                                style={"color": "#94A3B8", "fontSize": "0.85rem", "lineHeight": "1.6", "paddingLeft": "1.2rem", "margin": 0},
                                children=[html.Li(c) for c in member["contributions"]]
                            )
                        ]
                    )
                ]
            )
        )

    return html.Div(
        style={"maxWidth": "1200px", "margin": "0 auto", "padding": "3rem 1.5rem 6rem 1.5rem"},
        children=[
            # Header
            html.Div(
                style={"marginBottom": "3rem", "textAlign": "center"},
                children=[
                    html.Div(
                        style={"display": "inline-flex", "alignItems": "center", "gap": "0.5rem", "marginBottom": "0.75rem"},
                        children=[
                            html.Span("COURSE COLLABORATION ROSTER", style={"fontSize": "0.75rem", "fontWeight": "800", "letterSpacing": "0.1em", "color": "#00F2FE"}),
                        ]
                    ),
                    html.H1(
                        "Project Team & Individual Contributions",
                        style={"fontSize": "clamp(2.25rem, 5vw, 3.5rem)", "fontWeight": "900", "letterSpacing": "-0.04em", "color": "#FFFFFF", "margin": "0 0 1rem 0"}
                    ),
                    html.P(
                        "GIU Course: Data Engineering and Visualization (Winter 2026, due 9 Nov 2026). Each member contributed directly to the data pipeline, research questions, and interactive visualizations.",
                        style={"fontSize": "1.1rem", "color": "#94A3B8", "maxWidth": "750px", "margin": "0 auto"}
                    )
                ]
            ),

            # Team Grid (2x2 layout)
            html.Div(
                style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(340px, 1fr))", "gap": "1.5rem"},
                children=cards
            )
        ]
    )

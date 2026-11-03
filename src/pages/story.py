"""Story & Research Narrative Page for CityLink.

Presents the scientific core:
1. The research inquiry connecting housing growth and transportation.
2. Key empirical findings (expected vs surprising dynamics).
3. Data integration methodology (spatial & temporal alignment).
4. Analytical limitations (correlation != causation; unobserved confounders).
5. Actionable policy benefit & impact for NYC urban planning.
"""

import dash
from dash import html, dcc

dash.register_page(__name__, path="/story", title="CityLink — Research Story")


def layout():
    """Render the Research Story narrative layout."""
    return html.Div(
        style={"maxWidth": "1000px", "margin": "0 auto", "padding": "3rem 1.5rem 6rem 1.5rem"},
        children=[
            # Header
            html.Div(
                style={"marginBottom": "3rem"},
                children=[
                    html.Div(
                        style={"display": "inline-flex", "alignItems": "center", "gap": "0.5rem", "marginBottom": "0.75rem"},
                        children=[
                            html.Span("DATA-DRIVEN RESEARCH NARRATIVE", style={"fontSize": "0.75rem", "fontWeight": "800", "letterSpacing": "0.1em", "color": "#00F2FE"}),
                        ]
                    ),
                    html.H1(
                        "Where Homes Meet Rides: The Spatial Disconnect",
                        style={"fontSize": "clamp(2.25rem, 5vw, 3.5rem)", "fontWeight": "900", "letterSpacing": "-0.04em", "lineHeight": "1.1", "color": "#FFFFFF", "margin": "0 0 1rem 0"}
                    ),
                    html.P(
                        "An empirical investigation into whether New York City's residential development boom over the last decade has effectively synchronized with public transit capacity.",
                        style={"fontSize": "1.2rem", "color": "#94A3B8", "lineHeight": "1.6", "margin": 0}
                    )
                ]
            ),

            # Story Section 1: The Central Research Question
            html.Div(
                className="bento-card",
                style={"marginBottom": "2rem"},
                children=[
                    html.Div(
                        style={"display": "flex", "alignItems": "center", "gap": "0.75rem", "marginBottom": "1rem"},
                        children=[
                            html.Div("01", style={"width": "32px", "height": "32px", "borderRadius": "8px", "background": "rgba(0, 242, 254, 0.15)", "color": "#00F2FE", "fontWeight": "800", "display": "flex", "alignItems": "center", "justifyContent": "center", "fontSize": "0.85rem"}),
                            html.H2("The Core Inquiry", style={"fontSize": "1.4rem", "fontWeight": "800", "margin": 0, "color": "#FFFFFF"})
                        ]
                    ),
                    html.P(
                        "New York City confronts a dual crisis: acute residential housing shortages and aging public transit infrastructure operating near peak capacity during commuter rush hours. "
                        "CityLink investigates the central hypothesis: ",
                        style={"color": "#E2E8F0", "fontSize": "1.05rem", "lineHeight": "1.7"}
                    ),
                    html.Blockquote(
                        "Are new residential housing developments in NYC being concentrated in neighborhoods with robust transit accessibility, or are new homes disproportionately constructed in car-dependent transit deserts?",
                        style={
                            "borderLeft": "3px solid #00F2FE",
                            "paddingLeft": "1.25rem",
                            "margin": "1.25rem 0",
                            "color": "#00F2FE",
                            "fontSize": "1.15rem",
                            "fontWeight": "600",
                            "fontStyle": "italic"
                        }
                    )
                ]
            ),

            # Story Section 2: Key Empirical Findings
            html.Div(
                className="bento-card",
                style={"marginBottom": "2rem"},
                children=[
                    html.Div(
                        style={"display": "flex", "alignItems": "center", "gap": "0.75rem", "marginBottom": "1rem"},
                        children=[
                            html.Div("02", style={"width": "32px", "height": "32px", "borderRadius": "8px", "background": "rgba(255, 107, 107, 0.15)", "color": "#FF6B6B", "fontWeight": "800", "display": "flex", "alignItems": "center", "justifyContent": "center", "fontSize": "0.85rem"}),
                            html.H2("Key Empirical Findings", style={"fontSize": "1.4rem", "fontWeight": "800", "margin": 0, "color": "#FFFFFF"})
                        ]
                    ),
                    html.Ul(
                        style={"color": "#E2E8F0", "fontSize": "1.05rem", "lineHeight": "1.8", "paddingLeft": "1.5rem"},
                        children=[
                            html.Li([
                                html.Strong("Expected Dynamic: ", style={"color": "#00F2FE"}),
                                "Manhattan and Downtown Brooklyn exhibit the highest baseline transit accessibility indices (exceeding 85/100), with virtually 100% of newly constructed housing within a 5-minute walk of subway lines."
                            ]),
                            html.Li([
                                html.Strong("The Surprising Reality: ", style={"color": "#FF6B6B"}),
                                "Outer borough residential growth—particularly in Eastern Queens and the South Bronx—has surged significantly faster than transit capital improvements. "
                                "Substantial clusters of multifamily residential permits were approved in zones where subway station density is under 1.5 stations per square mile, inducing reliance on congested bus routes and ride-hail services."
                            ]),
                            html.Li([
                                html.Strong("Affordable Housing Equity Gap: ", style={"color": "#A855F7"}),
                                "Preserved affordable housing units often experience lower average transit accessibility scores compared to luxury high-density developments, exposing vulnerable households to longer daily commute times."
                            ])
                        ]
                    )
                ]
            ),

            # Story Section 3: Data Integration & Synthesis
            html.Div(
                className="bento-card",
                style={"marginBottom": "2rem"},
                children=[
                    html.Div(
                        style={"display": "flex", "alignItems": "center", "gap": "0.75rem", "marginBottom": "1rem"},
                        children=[
                            html.Div("03", style={"width": "32px", "height": "32px", "borderRadius": "8px", "background": "rgba(168, 85, 247, 0.15)", "color": "#A855F7", "fontWeight": "800", "display": "flex", "alignItems": "center", "justifyContent": "center", "fontSize": "0.85rem"}),
                            html.H2("Connecting Two Independent NYC Universes", style={"fontSize": "1.4rem", "fontWeight": "800", "margin": 0, "color": "#FFFFFF"})
                        ]
                    ),
                    html.P(
                        "To evaluate this relationship, CityLink bridges two disparate NYC Open Data silos: ",
                        style={"color": "#E2E8F0", "fontSize": "1.05rem", "lineHeight": "1.7"}
                    ),
                    html.Div(
                        style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(280px, 1fr))", "gap": "1rem", "marginTop": "1rem"},
                        children=[
                            html.Div(
                                style={"background": "rgba(255, 255, 255, 0.03)", "padding": "1.25rem", "borderRadius": "1rem", "border": "1px solid rgba(255, 255, 255, 0.06)"},
                                children=[
                                    html.H4("1. Housing & Zoning Domain", style={"color": "#FF6B6B", "margin": "0 0 0.5rem 0"}),
                                    html.P("DOB Building Permits, Certificate of Occupancy filings, and HPD Affordable Housing Production datasets. Aggregated by borough, calendar year, and development category.", style={"color": "#94A3B8", "fontSize": "0.9rem", "margin": 0})
                                ]
                            ),
                            html.Div(
                                style={"background": "rgba(255, 255, 255, 0.03)", "padding": "1.25rem", "borderRadius": "1rem", "border": "1px solid rgba(255, 255, 255, 0.06)"},
                                children=[
                                    html.H4("2. Transit Network Domain", style={"color": "#00F2FE", "margin": "0 0 0.5rem 0"}),
                                    html.P("MTA Subway Turnstile Ridership feeds, NYCDOT Bus Rapid Transit stops, and Census American Community Survey (ACS) mean travel times to work.", style={"color": "#94A3B8", "fontSize": "0.9rem", "margin": 0})
                                ]
                            )
                        ]
                    ),
                    html.P(
                        "The integration was achieved through spatial harmonisation: matching geographic coordinates (latitude/longitude), neighborhood tabulation areas (NTAs), and standardized calendar years (2018–2024).",
                        style={"color": "#94A3B8", "fontSize": "0.95rem", "marginTop": "1rem", "lineHeight": "1.6"}
                    )
                ]
            ),

            # Story Section 4: Analytical Limitations & Non-Causal Grounding
            html.Div(
                className="bento-card",
                style={"marginBottom": "2rem", "border": "1px solid rgba(245, 158, 11, 0.3)"},
                children=[
                    html.Div(
                        style={"display": "flex", "alignItems": "center", "gap": "0.75rem", "marginBottom": "1rem"},
                        children=[
                            html.Div("⚠", style={"width": "32px", "height": "32px", "borderRadius": "8px", "background": "rgba(245, 158, 11, 0.15)", "color": "#F59E0B", "fontWeight": "800", "display": "flex", "alignItems": "center", "justifyContent": "center", "fontSize": "1.1rem"}),
                            html.H2("Essential Scientific Limitations: Correlation ≠ Causation", style={"fontSize": "1.4rem", "fontWeight": "800", "margin": 0, "color": "#F59E0B"})
                        ]
                    ),
                    html.P(
                        "A critical mandate of CityLink is scientific integrity. While our visualizations reveal spatial and statistical correlations between housing density and transit metrics (e.g. Q5 Scatter), ",
                        style={"color": "#E2E8F0", "fontSize": "1.05rem", "lineHeight": "1.7"}
                    ),
                    html.P(
                        html.Strong("Correlation does NOT demonstrate causation. ", style={"color": "#FFFFFF"}),
                        style={"color": "#E2E8F0", "fontSize": "1.05rem", "lineHeight": "1.7"}
                    ),
                    html.P(
                        "Observed relationships are influenced by substantial confounding factors: historical land acquisition costs, industrial zoning barriers, municipal capital budgeting cycles (MTA 5-year plans), and socioeconomic segregation. "
                        "The presence of a transit line does not solely cause residential development, nor does high residential demand automatically induce transit expansion.",
                        style={"color": "#94A3B8", "fontSize": "0.95rem", "lineHeight": "1.6", "margin": 0}
                    )
                ]
            ),

            # Story Section 5: Benefit & Impact for NYC
            html.Div(
                className="bento-card",
                children=[
                    html.Div(
                        style={"display": "flex", "alignItems": "center", "gap": "0.75rem", "marginBottom": "1rem"},
                        children=[
                            html.Div("04", style={"width": "32px", "height": "32px", "borderRadius": "8px", "background": "rgba(16, 185, 129, 0.15)", "color": "#10B981", "fontWeight": "800", "display": "flex", "alignItems": "center", "justifyContent": "center", "fontSize": "0.85rem"}),
                            html.H2("Actionable Impact: Who Can Use This and How", style={"fontSize": "1.4rem", "fontWeight": "800", "margin": 0, "color": "#FFFFFF"})
                        ]
                    ),
                    html.P(
                        "CityLink was constructed to empower urban planners, civic technologists, and policymakers:",
                        style={"color": "#E2E8F0", "fontSize": "1.05rem", "lineHeight": "1.7"}
                    ),
                    html.Ul(
                        style={"color": "#94A3B8", "fontSize": "0.95rem", "lineHeight": "1.8", "paddingLeft": "1.5rem"},
                        children=[
                            html.Li([
                                html.Strong("NYC Department of City Planning (DCP): ", style={"color": "#F8FAFC"}),
                                "Use the spatial overlay (Q4) to identify emerging housing clusters lagging in transit infrastructure, prioritizing them for Transit-Oriented Development (TOD) rezonings."
                            ]),
                            html.Li([
                                html.Strong("MTA Capital Planning: ", style={"color": "#F8FAFC"}),
                                "Allocate Bus Rapid Transit (SBS) routes and high-capacity articulated buses directly to submarkets with rapid residential permit growth (Q1 & Q2)."
                            ]),
                            html.Li([
                                html.Strong("Civic Advocates & Residents: ", style={"color": "#F8FAFC"}),
                                "Evaluate neighborhood transit equity and advocate for balanced capital investments to prevent transit-induced displacement."
                            ])
                        ]
                    ),
                    html.Div(
                        style={"marginTop": "2rem"},
                        children=[
                            dcc.Link(
                                "Explore the Data Yourself →",
                                href="/explore",
                                className="btn-generate-report",
                                style={"textDecoration": "none"}
                            )
                        ]
                    )
                ]
            )
        ]
    )

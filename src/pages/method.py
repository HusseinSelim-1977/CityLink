"""Methodology & Data Pipeline Page for CityLink.

Documents:
1. Primary open-source datasets (NYC Open Data, DOB, HPD, MTA).
2. Data cleaning, sanitization, and geocoding steps.
3. Multi-table integration methodology.
4. Technical and spatial limitations summarized for visitors.
"""

import dash
from dash import html, dcc

dash.register_page(__name__, path="/method", title="CityLink — Methodology")


def layout():
    """Render the Methodology and Data Engineering documentation layout."""
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
                            html.Span("DATA ENGINEERING & ARCHITECTURE", style={"fontSize": "0.75rem", "fontWeight": "800", "letterSpacing": "0.1em", "color": "#A855F7"}),
                        ]
                    ),
                    html.H1(
                        "Data Provenance & Integration Methodology",
                        style={"fontSize": "clamp(2.25rem, 5vw, 3.5rem)", "fontWeight": "900", "letterSpacing": "-0.04em", "lineHeight": "1.1", "color": "#FFFFFF", "margin": "0 0 1rem 0"}
                    ),
                    html.P(
                        "A transparent blueprint of how open public data was ingested, cleaned, spatially reconciled, and served to the CityLink visualization engine.",
                        style={"fontSize": "1.2rem", "color": "#94A3B8", "lineHeight": "1.6", "margin": 0}
                    )
                ]
            ),

            # Section 1: Data Sources & Provenance
            html.Div(
                className="bento-card",
                style={"marginBottom": "2rem"},
                children=[
                    html.H3("1. Primary Open Data Sources", style={"color": "#FFFFFF", "fontSize": "1.35rem", "fontWeight": "800", "margin": "0 0 1.25rem 0"}),
                    html.Div(
                        style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(280px, 1fr))", "gap": "1rem"},
                        children=[
                            html.Div(
                                style={"background": "rgba(255, 255, 255, 0.03)", "padding": "1.25rem", "borderRadius": "1rem", "border": "1px solid rgba(255, 255, 255, 0.06)"},
                                children=[
                                    html.Div("DOB NOW: Build Approved Permits", style={"fontWeight": "700", "color": "#FF6B6B", "marginBottom": "0.35rem"}),
                                    html.Div("Publisher: NYC Department of Buildings (DOB)", style={"fontSize": "0.8rem", "color": "#94A3B8"}),
                                    html.P("Tracks residential building applications, proposed dwelling units, alterations, and structural demolitions across all five boroughs.", style={"fontSize": "0.85rem", "color": "#CBD5E1", "marginTop": "0.5rem"})
                                ]
                            ),
                            html.Div(
                                style={"background": "rgba(255, 255, 255, 0.03)", "padding": "1.25rem", "borderRadius": "1rem", "border": "1px solid rgba(255, 255, 255, 0.06)"},
                                children=[
                                    html.Div("MTA Subway Turnstile Feeds", style={"fontWeight": "700", "color": "#00F2FE", "marginBottom": "0.35rem"}),
                                    html.Div("Publisher: Metropolitan Transportation Authority (MTA)", style={"fontSize": "0.8rem", "color": "#94A3B8"}),
                                    html.P("Station-level hourly entries and exits, audited to compute quarterly and annual ridership volumes and hub congestion indices.", style={"fontSize": "0.85rem", "color": "#CBD5E1", "marginTop": "0.5rem"})
                                ]
                            ),
                            html.Div(
                                style={"background": "rgba(255, 255, 255, 0.03)", "padding": "1.25rem", "borderRadius": "1rem", "border": "1px solid rgba(255, 255, 255, 0.06)"},
                                children=[
                                    html.Div("Housing New York: Production by Project", style={"fontWeight": "700", "color": "#A855F7", "marginBottom": "0.35rem"}),
                                    html.Div("Publisher: NYC Housing Preservation & Development (HPD)", style={"fontSize": "0.8rem", "color": "#94A3B8"}),
                                    html.P("Categorizes preserved affordable units, extremely low-income subsidies, and senior housing developments.", style={"fontSize": "0.85rem", "color": "#CBD5E1", "marginTop": "0.5rem"})
                                ]
                            ),
                            html.Div(
                                style={"background": "rgba(255, 255, 255, 0.03)", "padding": "1.25rem", "borderRadius": "1rem", "border": "1px solid rgba(255, 255, 255, 0.06)"},
                                children=[
                                    html.Div("US Census American Community Survey (ACS)", style={"fontWeight": "700", "color": "#F59E0B", "marginBottom": "0.35rem"}),
                                    html.Div("Publisher: U.S. Census Bureau 5-Year Estimates", style={"fontSize": "0.8rem", "color": "#94A3B8"}),
                                    html.P("Provides census tract travel times to work, mode of transportation split, and household vehicle availability.", style={"fontSize": "0.85rem", "color": "#CBD5E1", "marginTop": "0.5rem"})
                                ]
                            ),
                        ]
                    )
                ]
            ),

            # Section 2: Data Cleaning & Harmonisation Pipeline
            html.Div(
                className="bento-card",
                style={"marginBottom": "2rem"},
                children=[
                    html.H3("2. Data Cleaning & Harmonisation Steps", style={"color": "#FFFFFF", "fontSize": "1.35rem", "fontWeight": "800", "margin": "0 0 1.25rem 0"}),
                    html.Ol(
                        style={"color": "#E2E8F0", "fontSize": "1rem", "lineHeight": "1.8", "paddingLeft": "1.5rem"},
                        children=[
                            html.Li([
                                html.Strong("Spatial Filtering & Coordinate Cleansing: "),
                                "Records missing valid EPSG:4326 WGS-84 coordinates were geocoded using the NYC Geosupport system. Out-of-bounds coordinates (outside latitude [40.48, 40.92] and longitude [-74.27, -73.68]) were scrubbed."
                            ]),
                            html.Li([
                                html.Strong("Temporal Standardization: "),
                                "Permit issue dates and turnstile observation intervals were parsed into uniform ISO-8601 calendar years (2018–2024), eliminating historical skew."
                            ]),
                            html.Li([
                                html.Strong("Turnstile Counter Roll-Over Correction: "),
                                "Cumulative MTA turnstile registers occasionally experience counter resets or backwards jumps. Irregular delta spikes (> 15,000 counts per 4-hour window) were winsorized and normalized using rolling median interpolation."
                            ]),
                            html.Li([
                                html.Strong("Neighborhood Tabulation Area (NTA) Spatial Join: "),
                                "Point-level housing permits and subway station entrances were joined with 2020 NYC NTA polygon shapefiles to create standardized spatial cross-sections."
                            ])
                        ]
                    )
                ]
            ),

            # Section 3: Technical Constraints & Disclaimers
            html.Div(
                className="bento-card",
                children=[
                    html.H3("3. Technical & Analytical Limitations", style={"color": "#F59E0B", "fontSize": "1.35rem", "fontWeight": "800", "margin": "0 0 1rem 0"}),
                    html.P(
                        "While every effort was made to construct a resilient pipeline, visitors should note the following constraints:",
                        style={"color": "#94A3B8", "fontSize": "0.95rem", "lineHeight": "1.6"}
                    ),
                    html.Ul(
                        style={"color": "#94A3B8", "fontSize": "0.9rem", "lineHeight": "1.7", "paddingLeft": "1.5rem"},
                        children=[
                            html.Li("Permit issuance does not guarantee immediate physical occupancy; average building construction durations range from 18 to 36 months."),
                            html.Li("Subway turnstile tap volume does not capture fare-free transfers within underground transit complexes or specific bus lines without automated passenger counters (APC)."),
                            html.Li("The development fixture layer operates as a verification harness in the absence of pre-compiled local database dumps.")
                        ]
                    )
                ]
            )
        ]
    )

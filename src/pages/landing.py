"""Landing Page for CityLink.

Awwwards Site of the Year / Unseen Studio tier creative experience:
- Interactive procedural 3D spatial urban metropolis (Three.js & Anime.js)
- Confined hero viewport with subtle bottom gradient fade
- Editorial architectural typography and Mobbin-style micro-badges
- Live horizontal telemetry marquee ticker
- Interactive glassmorphic bento cards with mouse spotlighting
"""

import dash
from dash import html, dcc

dash.register_page(__name__, path="/", title="CityLink — Where homes meet rides.")


def layout():
    """Render the studio-grade landing page layout."""
    return html.Div(
        style={"position": "relative", "overflow": "hidden"},
        children=[
            # 1. Dedicated 3D Spatial Hero Section (Confined with Bottom Vignette)
            html.Div(
                style={
                    "position": "relative",
                    "minHeight": "90vh",
                    "display": "flex",
                    "flexDirection": "column",
                    "justifyContent": "center",
                    "overflow": "hidden"
                },
                children=[
                    # 3D WebGL Canvas Layer
                    html.Div(id="three-canvas-container"),
                    
                    # Bottom Gradient Mask so 3D cleanly fades out before content below
                    html.Div(
                        style={
                            "position": "absolute",
                            "bottom": 0,
                            "left": 0,
                            "width": "100%",
                            "height": "160px",
                            "background": "linear-gradient(180deg, transparent 0%, #05060A 100%)",
                            "zIndex": 2,
                            "pointerEvents": "none"
                        }
                    ),

                    # Hero Content Overlay
                    html.Div(
                        className="hero-overlay-content",
                        style={"maxWidth": "1280px", "margin": "0 auto", "padding": "4rem 1.5rem 3rem 1.5rem", "width": "100%"},
                        children=[
                            # Overline Badge with Live Pulse
                            html.Div(
                                style={
                                    "display": "inline-flex",
                                    "alignItems": "center",
                                    "gap": "0.6rem",
                                    "background": "rgba(0, 242, 254, 0.08)",
                                    "border": "1px solid rgba(0, 242, 254, 0.3)",
                                    "borderRadius": "9999px",
                                    "padding": "0.45rem 1.25rem",
                                    "marginBottom": "2rem",
                                    "backdropFilter": "blur(20px)",
                                    "boxShadow": "0 0 20px rgba(0, 242, 254, 0.15)"
                                },
                                children=[
                                    html.Span(
                                        style={
                                            "width": "8px",
                                            "height": "8px",
                                            "borderRadius": "50%",
                                            "background": "#00F2FE",
                                            "boxShadow": "0 0 12px #00F2FE"
                                        }
                                    ),
                                    html.Span("NYC OPEN DATA RESEARCH", style={"fontSize": "0.75rem", "fontWeight": "800", "letterSpacing": "0.12em", "color": "#00F2FE"}),
                                    html.Span("•", style={"color": "#64748B"}),
                                    html.Span("WINTER 2026", style={"fontSize": "0.75rem", "fontWeight": "700", "color": "#94A3B8"}),
                                ]
                            ),

                            # Oversized Editorial Headline (Awwwards SOTD Tier)
                            html.H1(
                                [
                                    html.Div("Where homes", style={"color": "#FFFFFF", "letterSpacing": "-0.04em"}),
                                    html.Div(
                                        [
                                            html.Span(
                                                "meet rides.",
                                                style={
                                                    "background": "linear-gradient(135deg, #00F2FE 0%, #A855F7 50%, #FF6B6B 100%)",
                                                    "WebkitBackgroundClip": "text",
                                                    "WebkitTextFillColor": "transparent",
                                                    "letterSpacing": "-0.04em"
                                                }
                                            ),
                                            html.Span(
                                                " 🚇",
                                                style={
                                                    "fontSize": "0.6em",
                                                    "verticalAlign": "middle",
                                                    "background": "rgba(255, 255, 255, 0.08)",
                                                    "border": "1px solid rgba(255, 255, 255, 0.15)",
                                                    "borderRadius": "18px",
                                                    "padding": "0.2rem 0.5rem",
                                                    "marginLeft": "0.5rem"
                                                }
                                            )
                                        ]
                                    )
                                ],
                                style={
                                    "fontSize": "clamp(3.5rem, 8vw, 6.75rem)",
                                    "fontWeight": "900",
                                    "lineHeight": "0.98",
                                    "margin": "0 0 2rem 0",
                                    "maxWidth": "950px"
                                }
                            ),

                            # Lead Paragraph
                            html.P(
                                "An interactive, spatial data-storytelling portal synchronizing New York City's residential housing growth "
                                "with public transportation arteries. Uncover how zoning developments, commute dynamics, and subway networks collide across the five boroughs.",
                                style={
                                    "fontSize": "clamp(1.1rem, 2vw, 1.4rem)",
                                    "color": "#94A3B8",
                                    "lineHeight": "1.6",
                                    "maxWidth": "720px",
                                    "margin": "0 0 2.75rem 0",
                                    "fontWeight": "400"
                                }
                            ),

                            # Magnetic Action CTAs
                            html.Div(
                                style={"display": "flex", "flexWrap": "wrap", "gap": "1.25rem", "alignItems": "center"},
                                children=[
                                    dcc.Link(
                                        [
                                            html.Span("⚡", style={"fontSize": "1.2rem"}),
                                            html.Span("Launch Explore Engine →")
                                        ],
                                        href="/explore",
                                        className="btn-generate-report",
                                        style={"textDecoration": "none"}
                                    ),
                                    dcc.Link(
                                        "Read Research Story",
                                        href="/story",
                                        style={
                                            "background": "rgba(255, 255, 255, 0.05)",
                                            "border": "1px solid rgba(255, 255, 255, 0.15)",
                                            "backdropFilter": "blur(20px)",
                                            "color": "#F8FAFC",
                                            "padding": "1rem 2rem",
                                            "borderRadius": "9999px",
                                            "fontWeight": "700",
                                            "fontSize": "1.05rem",
                                            "textDecoration": "none",
                                            "transition": "all 0.3s ease"
                                        }
                                    ),
                                ]
                            ),
                        ]
                    )
                ]
            ),

            # 2. Live Marquee Telemetry Ticker
            html.Div(
                className="marquee-container",
                children=[
                    html.Div(
                        className="marquee-content",
                        children=(
                            "◆ 731,299 RESIDENTIAL UNITS ANALYZED "
                            "◆ 45,574,500 ANNUAL TRANSIT TRIPS "
                            "◆ 8 RESEARCH HYPOTHESES EVALUATED "
                            "◆ NYC DOB × MTA OPEN DATA RECONCILED "
                            "◆ 5 BOROUGHS HARMONIZED "
                            "◆ ZERO RUNTIME CDN DEPENDENCIES "
                            "◆ OLS CORRELATION & TRENDLINE ENGINE "
                            "◆ CARTO DARKMATTER SPATIAL OVERLAY "
                            "◆ "
                        ) * 2
                    )
                ]
            ),

            # 3. Studio Bento Grid Showcase
            html.Div(
                style={"maxWidth": "1280px", "margin": "0 auto", "padding": "1rem 1.5rem 6rem 1.5rem"},
                children=[
                    html.Div(
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(auto-fit, minmax(340px, 1fr))",
                            "gap": "1.75rem"
                        },
                        children=[
                            # Module 1: Housing
                            html.Div(
                                className="bento-card",
                                children=[
                                    html.Div(
                                        style={"display": "flex", "justifyContent": "space-between", "alignItems": "flex-start", "marginBottom": "1.5rem"},
                                        children=[
                                            html.Span("01 / ARCHITECTURE", style={"fontSize": "0.75rem", "fontWeight": "800", "letterSpacing": "0.1em", "color": "#FF6B6B"}),
                                            html.Span("DOB & HPD", style={"background": "rgba(255, 107, 107, 0.15)", "color": "#FF6B6B", "padding": "0.25rem 0.65rem", "borderRadius": "9999px", "fontSize": "0.75rem", "fontWeight": "700"})
                                        ]
                                    ),
                                    html.H3("Vertical Expansion", style={"fontSize": "1.65rem", "fontWeight": "800", "margin": "0 0 0.85rem 0", "color": "#FFFFFF", "letterSpacing": "-0.02em"}),
                                    html.P(
                                        "Tracking thousands of residential unit filings, high-rise completions, and preserved affordable housing developments across Manhattan, Brooklyn, Queens, Bronx, and Staten Island.",
                                        style={"color": "#94A3B8", "fontSize": "0.95rem", "lineHeight": "1.6", "margin": 0}
                                    )
                                ]
                            ),
                            # Module 2: Transit
                            html.Div(
                                className="bento-card",
                                children=[
                                    html.Div(
                                        style={"display": "flex", "justifyContent": "space-between", "alignItems": "flex-start", "marginBottom": "1.5rem"},
                                        children=[
                                            html.Span("02 / CIRCULATORY", style={"fontSize": "0.75rem", "fontWeight": "800", "letterSpacing": "0.1em", "color": "#00F2FE"}),
                                            html.Span("MTA & NYCDOT", style={"background": "rgba(0, 242, 254, 0.15)", "color": "#00F2FE", "padding": "0.25rem 0.65rem", "borderRadius": "9999px", "fontSize": "0.75rem", "fontWeight": "700"})
                                        ]
                                    ),
                                    html.H3("Kinetic Arteries", style={"fontSize": "1.65rem", "fontWeight": "800", "margin": "0 0 0.85rem 0", "color": "#FFFFFF", "letterSpacing": "-0.02em"}),
                                    html.P(
                                        "Evaluating subway turnstile tap density, bus rapid transit corridors, and composite walkability indices to measure spatial transit accessibility across diverse socioeconomic clusters.",
                                        style={"color": "#94A3B8", "fontSize": "0.95rem", "lineHeight": "1.6", "margin": 0}
                                    )
                                ]
                            ),
                            # Module 3: Nexus
                            html.Div(
                                className="bento-card",
                                children=[
                                    html.Div(
                                        style={"display": "flex", "justifyContent": "space-between", "alignItems": "flex-start", "marginBottom": "1.5rem"},
                                        children=[
                                            html.Span("03 / NEXUS", style={"fontSize": "0.75rem", "fontWeight": "800", "letterSpacing": "0.1em", "color": "#A855F7"}),
                                            html.Span("STATISTICS", style={"background": "rgba(168, 85, 247, 0.15)", "color": "#A855F7", "padding": "0.25rem 0.65rem", "borderRadius": "9999px", "fontSize": "0.75rem", "fontWeight": "700"})
                                        ]
                                    ),
                                    html.H3("Spatial Equity", style={"fontSize": "1.65rem", "fontWeight": "800", "margin": "0 0 0.85rem 0", "color": "#FFFFFF", "letterSpacing": "-0.02em"}),
                                    html.P(
                                        "Analyzing the empirical relationship between local housing volume and average commute times with OLS regression, Pearson correlation, and rigorous non-causal validation.",
                                        style={"color": "#94A3B8", "fontSize": "0.95rem", "lineHeight": "1.6", "margin": 0}
                                    )
                                ]
                            ),
                        ]
                    )
                ]
            )
        ]
    )

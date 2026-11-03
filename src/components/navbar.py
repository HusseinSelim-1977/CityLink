"""Shared Navigation Bar Component for CityLink.

Renders an Apple/Linear-inspired floating pill header with branding,
internal routing links, and an 'Explore Engine' CTA button.
"""

from dash import html, dcc


def render_navbar(active_path: str = "/") -> html.Div:
    """Generate the primary navigation bar."""
    nav_items = [
        {"label": "Overview", "href": "/"},
        {"label": "Explore Engine", "href": "/explore"},
        {"label": "Story & Findings", "href": "/story"},
        {"label": "Methodology", "href": "/method"},
        {"label": "Team", "href": "/team"},
    ]

    links = []
    for item in nav_items:
        is_active = active_path == item["href"]
        links.append(
            dcc.Link(
                item["label"],
                href=item["href"],
                className=f"nav-link-item {'active' if is_active else ''}"
            )
        )

    # Add quick launch CTA
    links.append(
        dcc.Link(
            "Launch Explore →",
            href="/explore",
            className="nav-link-item nav-cta-btn"
        )
    )

    return html.Div(
        className="citylink-navbar",
        children=[
            # Brand identity
            dcc.Link(
                href="/",
                className="brand-container",
                children=[
                    html.Div("CL", className="brand-logo-badge"),
                    html.Div([
                        html.Div("CityLink", className="brand-text-title"),
                        html.Div("Where homes meet rides.", className="brand-tagline"),
                    ])
                ]
            ),
            # Route links
            html.Nav(
                className="nav-links-group",
                children=links
            )
        ]
    )

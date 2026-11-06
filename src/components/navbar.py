"""Shared Navigation Bar Component for CityLink.

Renders a modern, floating "dock" navigation header with a blurred glassmorphism effect,
branded identity, and interactive links.
"""

from dash import html, dcc


def render_navbar(active_path: str = "/") -> html.Div:
    """Generate the high-end floating navigation dock."""
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
                className=f"nav-dock-link {'nav-dock-active' if is_active else ''}"
            )
        )

    # Add high-impact CTA
    links.append(
        dcc.Link(
            "Launch Engine →",
            href="/explore",
            className="nav-dock-cta"
        )
    )

    return html.Div(
        className="nav-dock-container",
        children=[
            # Branding: Compact & Premium
            dcc.Link(
                href="/",
                className="nav-dock-brand",
                children=[
                    html.Div("CL", className="nav-dock-logo"),
                    html.Div("CityLink", className="nav-dock-title"),
                ]
            ),
            # Navigation Group
            html.Nav(
                className="nav-dock-nav",
                children=links
            ),
            # Action Button
            html.Div(
                className="nav-dock-actions",
                children=[
                    dcc.Link(
                        "SIGN IN",
                        href="/login",
                        className="nav-dock-btn-ghost"
                    ),
                ]
            )
        ]
    )

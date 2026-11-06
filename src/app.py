"""Main Dash Application Entrypoint for CityLink.

Exposes `app` and `server = app.server` for WSGI/Gunicorn execution.
Configured as a multi-page Dash application using absolute package imports.
Launch via:
    python -m src.app
or:
    gunicorn src.app:server
"""
import sys
sys.path.append('src')
import os
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

from src.components.navbar import render_navbar
from src.components.footer import render_footer

# Compute absolute path to pages and assets folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(BASE_DIR, "pages")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Initialize multi-page Dash app
app = dash.Dash(
    __name__,
    use_pages=True,
    pages_folder=PAGES_DIR,
    assets_folder=ASSETS_DIR,
    suppress_callback_exceptions=True,
    title="CityLink — Where homes meet rides.",
    update_title=None,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=5"},
        {"name": "description", "content": "CityLink: An interactive spatial data-storytelling portal connecting NYC housing with transportation data."},
        {"name": "theme-color", "content": "#08090E"}
    ]
)

# Expose server for gunicorn
server = app.server

# Custom HTML Index String (Typography, Favicon, Zero CDN Dependencies)
app.index_string = """<!DOCTYPE html>
<html lang="en">
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        <!-- High-craft Display Fonts -->
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
        {%css%}
        <style>
            /* Force dark luxury theme on Dash 4.5+ button.dash-dropdown controls */
            button.dash-dropdown,
            .dash-dropdown,
            div.dash-dropdown {
                background-color: #0E1222 !important;
                background: #0E1222 !important;
                border: 1px solid rgba(255, 255, 255, 0.18) !important;
                border-radius: 12px !important;
                color: #FFFFFF !important;
                height: 44px !important;
            }
            .dash-dropdown-value,
            .dash-dropdown-value-item,
            .dash-dropdown-value-item span,
            .dash-dropdown-trigger {
                color: #FFFFFF !important;
                font-weight: 600 !important;
            }
            .dash-dropdown-menu,
            div[data-dash-dropdown-menu] {
                background-color: #0A0D18 !important;
                background: #0A0D18 !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 12px !important;
                box-shadow: 0 16px 40px rgba(0, 0, 0, 0.8) !important;
            }
            .dash-dropdown-option {
                color: #94A3B8 !important;
            }
            .dash-dropdown-option:hover,
            .dash-dropdown-option[data-highlighted] {
                background-color: rgba(0, 242, 254, 0.15) !important;
                color: #00F2FE !important;
            }
            div.Select-control, .Select-control {
                background-color: #0E1222 !important;
                background: #0E1222 !important;
                border: 1px solid rgba(255, 255, 255, 0.18) !important;
                border-radius: 12px !important;
                color: #FFFFFF !important;
            }
            .Select-value-label, .Select-placeholder, .Select-value {
                color: #FFFFFF !important;
            }
            .Select-input > input {
                color: #FFFFFF !important;
            }
            .Select-menu-outer, .Select-menu {
                background-color: #0A0D18 !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 12px !important;
            }
            .Select-option {
                background-color: transparent !important;
                color: #94A3B8 !important;
            }
            .Select-option:hover, .Select-option.is-focused {
                background-color: rgba(0, 242, 254, 0.15) !important;
                color: #00F2FE !important;
            }
            .Select-arrow {
                border-top-color: #00F2FE !important;
            }
        </style>
    </head>
    <body style="background-color: #08090E; margin: 0; padding: 0;">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

# Dynamic Root Layout
app.layout = html.Div(
    id="citylink-root",
    style={"minHeight": "100vh", "display": "flex", "flexDirection": "column"},
    children=[
        dcc.Location(id="url", refresh=False),
        # Global Staging Store for cross-component state
        dcc.Store(id="global-search-store", storage_type="memory", data={}),
        # Top Navigation
        html.Div(id="navbar-container", children=[render_navbar("/")]),
        # Dynamic Page View
        html.Main(
            style={"flex": "1 0 auto"},
            children=[dash.page_container]
        ),
        # Footer
        render_footer()
    ]
)


@callback(
    Output("navbar-container", "children"),
    Input("url", "pathname")
)
def sync_navbar_active_state(pathname: str):
    """Synchronize the active navigation tab with the current URL path."""
    current_path = pathname if pathname else "/"
    return render_navbar(current_path)


if __name__ == "__main__":
    # Local development server
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=True, host="0.0.0.0", port=port)

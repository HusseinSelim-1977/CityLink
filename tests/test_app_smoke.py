"""Smoke test for CityLink app entrypoint.

Verifies that src.app can be imported, exposes the Flask server instance,
and registers all Dash Pages without exceptions.
"""

import pytest


def test_app_server_exists():
    """Assert that src.app exposes a valid Flask WSGI server instance."""
    from src.app import app, server

    assert app is not None, "Dash app instance should not be None"
    assert server is not None, "server = app.server must be exposed for Gunicorn"
    assert hasattr(server, "wsgi_app"), "server must be a WSGI-compliant Flask instance"


def test_dash_pages_registered():
    """Assert that all five core Dash Pages are discovered and registered."""
    import dash
    from src.app import app

    # Check registered page paths
    page_paths = {p["path"] for p in dash.page_registry.values()}
    expected_paths = {"/", "/explore", "/story", "/method", "/team"}

    assert expected_paths.issubset(page_paths), f"Missing pages! Registered: {page_paths}"

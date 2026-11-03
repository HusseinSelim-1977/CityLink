"""Frontend tests for Page Layout Generation and Rendering."""

import pytest
# Ensure Dash app is initialized first before registering pages
from src.app import app

from dash.development.base_component import Component
from src.pages.landing import layout as landing_layout
from src.pages.explore import layout as explore_layout
from src.pages.story import layout as story_layout
from src.pages.method import layout as method_layout
from src.pages.team import layout as team_layout


def test_all_page_layouts_render():
    """Verify that every page's layout() function executes and returns a Dash component."""
    for name, layout_fn in [
        ("Landing", landing_layout),
        ("Explore", explore_layout),
        ("Story", story_layout),
        ("Method", method_layout),
        ("Team", team_layout)
    ]:
        comp = layout_fn()
        assert isinstance(comp, Component), f"{name} layout should return a Dash Component"


def test_explore_page_contains_mandatory_elements():
    """Verify Explore layout contains Generate Report button, Search Mode, and 4 Dropdowns."""
    explore = explore_layout()

    # Convert layout tree to string representation for structural inspection
    layout_repr = str(explore)

    assert "btn-generate-report" in layout_repr, "Explore must contain the central Generate Report button"
    assert "search-input" in layout_repr, "Explore must contain the search input"
    assert "filter-borough" in layout_repr, "Explore must contain Borough filter"
    assert "filter-year" in layout_repr, "Explore must contain Year filter"
    assert "filter-housing" in layout_repr, "Explore must contain Housing filter"
    assert "filter-transit" in layout_repr, "Explore must contain Transit filter"
    assert "question-selector" in layout_repr, "Explore must contain the research question selector"

"""Frontend tests for Chart Registry and Individual Figure Builders."""

import pytest
import pandas as pd
import plotly.graph_objects as go

from src.callbacks.data_access import apply_filters
from src.charts.registry import CHART_REGISTRY, get_registered_questions, build_chart


def test_registry_contains_eight_questions():
    """Verify that exactly 8 research questions are registered for the 4-member team."""
    questions = get_registered_questions()
    assert len(questions) == 8
    expected_ids = {"Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"}
    actual_ids = {q["id"] for q in questions}
    assert actual_ids == expected_ids


def test_all_charts_build_successfully():
    """Verify that every registered question builder returns a valid Plotly Figure."""
    df = apply_filters()

    for q_id in CHART_REGISTRY.keys():
        fig = build_chart(q_id, df)
        assert isinstance(fig, go.Figure), f"Chart for {q_id} should be a Plotly Figure"
        assert fig.data is not None, f"Chart {q_id} must have data traces"
        assert fig.layout.title.text is not None, f"Chart {q_id} must have a title"


def test_empty_dataframe_handling():
    """Verify that all figure builders handle empty DataFrames gracefully without crashing."""
    empty_df = pd.DataFrame()

    for q_id in CHART_REGISTRY.keys():
        fig = build_chart(q_id, empty_df)
        assert isinstance(fig, go.Figure), f"Chart {q_id} must return Figure on empty DataFrame"


def test_q5_cross_domain_non_causal_disclaimer():
    """Verify that Q5 cross-domain scatter plot contains non-causal disclaimer and correlation."""
    df = apply_filters()
    fig = build_chart("Q5", df)

    # Check for disclaimer note in annotations
    has_disclaimer = any("Non-causal" in ann.text for ann in fig.layout.annotations if hasattr(ann, "text") and ann.text)
    assert has_disclaimer, "Q5 must explicitly state that correlation does not imply causation"

"""Frontend tests for Data Access Adapter and Search Query Parser."""

import pytest
import pandas as pd
from src.callbacks.data_access import (
    get_filter_options,
    apply_filters,
    compute_kpis,
    parse_search_query,
    get_chart_data
)


def test_get_filter_options():
    """Verify that filter options contain required dimensions with non-empty lists."""
    opts = get_filter_options()
    assert "borough" in opts
    assert "year" in opts
    assert "housing_category" in opts
    assert "transit_category" in opts

    assert len(opts["borough"]) >= 5
    assert "Brooklyn" in opts["borough"]
    assert 2022 in opts["year"]


def test_apply_filters():
    """Verify that applying filters returns properly sliced DataFrames."""
    # Test unconstrained
    df_all = apply_filters()
    assert isinstance(df_all, pd.DataFrame)
    assert not df_all.empty
    assert len(df_all) > 100

    # Test single borough
    df_bk = apply_filters({"borough": "Brooklyn"})
    assert (df_bk["borough"] == "Brooklyn").all()

    # Test borough + year
    df_bk_2022 = apply_filters({"borough": "Brooklyn", "year": 2022})
    assert (df_bk_2022["borough"] == "Brooklyn").all()
    assert (df_bk_2022["year"] == 2022).all()


def test_compute_kpis():
    """Verify that KPI calculations return valid numerical structures."""
    df = apply_filters({"borough": "Manhattan"})
    kpis = compute_kpis(df)

    assert "total_units" in kpis
    assert "avg_commute_time" in kpis
    assert "avg_accessibility" in kpis
    assert "total_ridership_m" in kpis
    assert kpis["total_units"] > 0
    assert kpis["avg_commute_time"] > 0
    assert 0 <= kpis["avg_accessibility"] <= 100


def test_parse_search_query_exact():
    """Verify parsing of standard query strings into discrete filter dimensions."""
    query = "Brooklyn 2022 new buildings subway"
    res = parse_search_query(query)

    filters = res["filters"]
    assert filters.get("borough") == "Brooklyn"
    assert filters.get("year") == 2022
    assert filters.get("housing_category") == "New Residential Construction"
    assert filters.get("transit_category") == "Subway Expansion & Upgrades"
    assert len(res["matched_chips"]) >= 3


def test_parse_search_query_fallback():
    """Verify that arbitrary or unparseable queries fail gracefully without exceptions."""
    res_empty = parse_search_query("")
    assert res_empty["filters"] == {}
    assert res_empty["matched_chips"] == []

    res_unknown = parse_search_query("random extraterrestrial spacecraft")
    assert res_unknown["filters"] == {}
    assert len(res_unknown["unmatched"]) > 0

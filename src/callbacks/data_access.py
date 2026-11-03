"""Data Access Adapter Module for CityLink.

This module acts as the single boundary between the frontend UI and the
data layer. UI components and callbacks NEVER read raw data files directly;
they call this adapter exclusively.

If the backend data pipeline (`src.data`) is available, the adapter delegates
to it. If `src.data` is absent, it seamlessly falls back to the verification
fixture in `src.callbacks.dev_fixture`.
"""

import importlib
import re
from typing import Dict, Any, List, Optional
import pandas as pd

from src.callbacks.dev_fixture import (
    BOROUGHS,
    YEARS,
    HOUSING_CATEGORIES,
    TRANSIT_CATEGORIES,
    get_cached_dev_dataframe
)


def _get_backend_data_module():
    """Attempt dynamic import of src.data to check if real backend is ready."""
    try:
        data_mod = importlib.import_module("src.data")
        # Ensure it has necessary data functions
        if hasattr(data_mod, "apply_filters") and hasattr(data_mod, "get_filter_options"):
            return data_mod
    except (ImportError, ModuleNotFoundError, AttributeError):
        pass
    return None


def get_filter_options() -> Dict[str, List[Any]]:
    """Return selectable dropdown options for all filter dimensions."""
    backend = _get_backend_data_module()
    if backend and hasattr(backend, "get_filter_options"):
        return backend.get_filter_options()

    return {
        "borough": BOROUGHS,
        "year": YEARS,
        "housing_category": HOUSING_CATEGORIES,
        "transit_category": TRANSIT_CATEGORIES,
    }


def parse_search_query(text: str) -> Dict[str, Any]:
    """Parse a natural-language search query into discrete filter values.

    Example:
        'Brooklyn 2022 new buildings' ->
        {
            'filters': {'borough': 'Brooklyn', 'year': 2022, 'housing_category': 'New Residential Construction'},
            'matched_chips': ['Borough: Brooklyn', 'Year: 2022', 'Housing: New Residential Construction'],
            'unmatched': []
        }
    """
    if not text or not text.strip():
        return {"filters": {}, "matched_chips": [], "unmatched": []}

    backend = _get_backend_data_module()
    if backend and hasattr(backend, "parse_search_query"):
        return backend.parse_search_query(text)

    # Local keyword and vocabulary matching
    raw_query = text.lower().strip()
    words = re.findall(r"\w+", raw_query)
    
    parsed_filters: Dict[str, Any] = {}
    matched_chips: List[str] = []
    consumed_words = set()

    # 1. Borough matching
    for b in BOROUGHS:
        b_lower = b.lower()
        # Direct word match or multi-word match (e.g. Staten Island)
        if b_lower in raw_query:
            parsed_filters["borough"] = b
            matched_chips.append(f"Borough: {b}")
            for w in b_lower.split():
                consumed_words.add(w)
            break

    # 2. Year matching
    for y in YEARS:
        str_y = str(y)
        if str_y in words:
            parsed_filters["year"] = y
            matched_chips.append(f"Year: {y}")
            consumed_words.add(str_y)
            break

    # 3. Housing Category keyword heuristics
    housing_synonyms = {
        "New Residential Construction": ["new", "construction", "buildings", "development", "residential", "housing"],
        "Affordable Housing Preserved": ["affordable", "preserved", "subsidized", "low-income"],
        "Zoning Alterations": ["zoning", "variance", "rezoning", "alterations", "permits"],
        "Demolitions & Replacements": ["demolition", "demolitions", "replace", "tear", "redevelopment"]
    }
    for cat, keywords in housing_synonyms.items():
        if any(kw in words for kw in keywords):
            parsed_filters["housing_category"] = cat
            matched_chips.append(f"Housing: {cat}")
            for kw in keywords:
                if kw in words:
                    consumed_words.add(kw)
            break

    # 4. Transit Category keyword heuristics
    transit_synonyms = {
        "Subway Expansion & Upgrades": ["subway", "train", "station", "mta", "metro", "line", "rails"],
        "Bus Rapid Transit (SBS)": ["bus", "sbs", "rapid", "shuttle", "route"],
        "Bike Lane & Micro-Mobility": ["bike", "cycling", "scooter", "micromobility", "citi", "lane"],
        "Ferry Landing & Water Transit": ["ferry", "water", "dock", "landing", "boat"]
    }
    for cat, keywords in transit_synonyms.items():
        if any(kw in words for kw in keywords):
            parsed_filters["transit_category"] = cat
            matched_chips.append(f"Transit: {cat}")
            for kw in keywords:
                if kw in words:
                    consumed_words.add(kw)
            break

    unmatched = [w for w in words if w not in consumed_words and len(w) > 2]

    return {
        "filters": parsed_filters,
        "matched_chips": matched_chips,
        "unmatched": unmatched
    }


def apply_filters(filters: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Filter the dataset according to the provided filter parameters."""
    backend = _get_backend_data_module()
    if backend and hasattr(backend, "apply_filters"):
        return backend.apply_filters(filters)

    df = get_cached_dev_dataframe()
    if not filters:
        return df

    # Apply borough filter
    borough = filters.get("borough")
    if borough and borough != "ALL":
        if isinstance(borough, list):
            df = df[df["borough"].isin(borough)]
        else:
            df = df[df["borough"] == borough]

    # Apply year filter
    year = filters.get("year")
    if year and year != "ALL":
        if isinstance(year, list):
            df = df[df["year"].isin(year)]
        else:
            df = df[df["year"] == int(year)]

    # Apply housing category filter
    h_cat = filters.get("housing_category")
    if h_cat and h_cat != "ALL":
        if isinstance(h_cat, list):
            df = df[df["housing_category"].isin(h_cat)]
        else:
            df = df[df["housing_category"] == h_cat]

    # Apply transit category filter
    t_cat = filters.get("transit_category")
    if t_cat and t_cat != "ALL":
        if isinstance(t_cat, list):
            df = df[df["transit_category"].isin(t_cat)]
        else:
            df = df[df["transit_category"] == t_cat]

    return df


def compute_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute high-level summary KPIs for the active dataset slice."""
    backend = _get_backend_data_module()
    if backend and hasattr(backend, "compute_kpis"):
        return backend.compute_kpis(df)

    if df.empty:
        return {
            "total_units": 0,
            "avg_commute_time": 0.0,
            "avg_accessibility": 0.0,
            "total_ridership_m": 0.0,
            "active_boroughs": 0,
            "total_records": 0,
            "is_fixture": True
        }

    total_units = int(df["residential_units"].sum())
    avg_commute = round(float(df["avg_commute_time_min"].mean()), 1)
    avg_access = round(float(df["transit_accessibility_score"].mean()), 1)
    total_ridership = round(float(df["transit_ridership_m"].sum()), 1)
    active_boroughs = int(df["borough"].nunique())
    is_fixture = bool(df["is_fixture"].iloc[0]) if "is_fixture" in df.columns else False

    return {
        "total_units": total_units,
        "avg_commute_time": avg_commute,
        "avg_accessibility": avg_access,
        "total_ridership_m": total_ridership,
        "active_boroughs": active_boroughs,
        "total_records": len(df),
        "is_fixture": is_fixture
    }


def get_chart_data(question_id: str, filters: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Retrieve and format data slice specifically for a given research question."""
    backend = _get_backend_data_module()
    if backend and hasattr(backend, "get_chart_data"):
        return backend.get_chart_data(question_id, filters)

    # By default, apply active filters to the dataset
    return apply_filters(filters)

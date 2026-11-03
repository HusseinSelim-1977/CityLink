"""Central Chart Registry for CityLink.

Maps each research question (Q1 through Q8 for a 4-member team) to its
corresponding visualization module and metadata.
Adding a new chart is as simple as creating a module in src/charts/ and
adding an entry to this registry.
"""

from typing import Dict, Any, List, Callable
import pandas as pd
import plotly.graph_objects as go

from src.charts.q1_borough_housing_bar import build_chart as build_q1
from src.charts.q2_temporal_trend_line import build_chart as build_q2
from src.charts.q3_transit_housing_heatmap import build_chart as build_q3
from src.charts.q4_spatial_overlay_map import build_chart as build_q4
from src.charts.q5_cross_domain_scatter import build_chart as build_q5
from src.charts.q6_affordability_transit_dist import build_chart as build_q6
from src.charts.q7_borough_transit_ratio import build_chart as build_q7
from src.charts.q8_zoning_transit_breakdown import build_chart as build_q8


CHART_REGISTRY: Dict[str, Dict[str, Any]] = {
    "Q1": {
        "id": "Q1",
        "title": "Borough Housing Unit Volumes",
        "question": "How do residential housing completions and permits compare across the five NYC boroughs?",
        "chart_type": "Stacked Bar",
        "category": "Housing Development",
        "builder": build_q1,
        "description": "Examines borough-level residential unit completions stratified by development category."
    },
    "Q2": {
        "id": "Q2",
        "title": "Housing vs Transit Multi-Year Trends",
        "question": "How have residential housing completions trended alongside annual transit ridership from 2018 to 2024?",
        "chart_type": "Dual-Axis Line",
        "category": "Cross-Domain Temporal",
        "builder": build_q2,
        "description": "Investigates whether annual changes in residential housing units coincide with public transit usage."
    },
    "Q3": {
        "id": "Q3",
        "title": "Transit Accessibility Matrix",
        "question": "What is the distribution of transit accessibility index scores across housing development types and boroughs?",
        "chart_type": "2D Heatmap",
        "category": "Transit Infrastructure",
        "builder": build_q3,
        "description": "Quantifies average walkability and subway proximity index across housing classifications."
    },
    "Q4": {
        "id": "Q4",
        "title": "Spatial Housing & Transit Map Overlay",
        "question": "Where are residential development clusters located relative to subway station density across NYC neighborhoods?",
        "chart_type": "Carto Mapbox Scatter",
        "category": "Spatial Analysis",
        "builder": build_q4,
        "description": "Geospatial scatter plot using Carto Darkmatter tiles displaying neighborhood residential volume and transit hubs."
    },
    "Q5": {
        "id": "Q5",
        "title": "Housing Density vs Commute Time Correlation",
        "question": "Is there a statistically significant relationship between local residential volume and average commute times?",
        "chart_type": "Cross-Domain Scatter (OLS)",
        "category": "Cross-Domain Relationship",
        "builder": build_q5,
        "description": "Evaluates Pearson correlation coefficient and ordinary least squares trendline between units and commute duration."
    },
    "Q6": {
        "id": "Q6",
        "title": "Affordable Housing Transit Accessibility",
        "question": "How does transit connectivity score vary between preserved affordable housing and market-rate projects?",
        "chart_type": "Box Distribution",
        "category": "Equity & Accessibility",
        "builder": build_q6,
        "description": "Box plot comparing interquartile ranges and median transit accessibility scores across housing categories."
    },
    "Q7": {
        "id": "Q7",
        "title": "Transit Facility Density Ratio",
        "question": "Which NYC boroughs feature the highest ratio of transit facilities per thousand residential units?",
        "chart_type": "Horizontal Ratio Bar",
        "category": "Infrastructure Ratio",
        "builder": build_q7,
        "description": "Ranks boroughs by transit hub density normalized per 1,000 newly developed residential units."
    },
    "Q8": {
        "id": "Q8",
        "title": "Zoning & Transit Hierarchical Breakdown",
        "question": "What is the categorical breakdown of transit initiatives across residential zoning alteration zones?",
        "chart_type": "Hierarchical Treemap",
        "category": "Zoning & Planning",
        "builder": build_q8,
        "description": "Multi-level tree decomposition showing borough-level allocation of housing units by zoning classification."
    }
}


def get_registered_questions() -> List[Dict[str, Any]]:
    """Return list of question metadata dictionaries for UI selector menus."""
    return [
        {
            "id": q_id,
            "title": meta["title"],
            "question": meta["question"],
            "chart_type": meta["chart_type"],
            "category": meta["category"],
            "description": meta["description"]
        }
        for q_id, meta in CHART_REGISTRY.items()
    ]


def build_chart(question_id: str, df: pd.DataFrame) -> go.Figure:
    """Build the Plotly figure for the requested question ID using active filtered data."""
    if question_id not in CHART_REGISTRY:
        # Fallback to Q1 if unrecognized
        question_id = "Q1"

    builder: Callable[[pd.DataFrame], go.Figure] = CHART_REGISTRY[question_id]["builder"]
    return builder(df)

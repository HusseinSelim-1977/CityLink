"""Chart Module Q8: Multi-Category Breakdown: Housing Types & Transit Modes.

Answers: How do transit project investments intersect with residential zoning alterations?
Type: Hierarchical Treemap.
"""

import pandas as pd
import plotly.graph_objects as go
from src.charts.theme import apply_citylink_theme


def build_chart(df: pd.DataFrame) -> go.Figure:
    """Build the Q8 Hierarchical Treemap."""
    if df.empty:
        fig = go.Figure()
        return apply_citylink_theme(fig, "Q8: Cross-Category Treemap Breakdown", note="No data available.")

    # Group by Borough -> Housing Category -> Transit Category
    tree_df = df.groupby(["borough", "housing_category", "transit_category"]).agg({
        "residential_units": "sum"
    }).reset_index()

    # Build Treemap data
    # Root level: NYC Total
    # First level: Boroughs
    # Second level: Housing Category
    # Third level: Transit Category

    ids = ["NYC"]
    labels = ["NYC Metro"]
    parents = [""]
    values = [tree_df["residential_units"].sum()]

    # Boroughs
    for borough in tree_df["borough"].unique():
        b_sum = tree_df[tree_df["borough"] == borough]["residential_units"].sum()
        ids.append(f"NYC_{borough}")
        labels.append(borough)
        parents.append("NYC")
        values.append(b_sum)

        # Housing Category under Borough
        b_df = tree_df[tree_df["borough"] == borough]
        for h_cat in b_df["housing_category"].unique():
            h_sum = b_df[b_df["housing_category"] == h_cat]["residential_units"].sum()
            h_id = f"NYC_{borough}_{h_cat}"
            ids.append(h_id)
            labels.append(h_cat)
            parents.append(f"NYC_{borough}")
            values.append(h_sum)

    fig = go.Figure(
        go.Treemap(
            ids=ids,
            labels=labels,
            parents=parents,
            values=values,
            branchvalues="total",
            marker=dict(
                colorscale="Viridis",
                line=dict(width=1.5, color="#08090E")
            ),
            textinfo="label+value+percent parent",
            hovertemplate="<b>%{label}</b><br>Units: %{value:,.0f}<br>Parent Share: %{percentParent:.1%}<extra></extra>"
        )
    )

    return apply_citylink_theme(
        fig=fig,
        title="Q8: Hierarchical Breakdown: Boroughs & Housing Classifications",
        note="Area size correlates with aggregate residential unit volume."
    )

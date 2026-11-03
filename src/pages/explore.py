"""Explore Data Engine Page for CityLink.

Studio-Grade Analytical Cockpit (Inspired by Linear, Arc, and Mobbin):
1. 4 Staged Dropdown Filters (Borough, Year, Housing Classification, Transit Network Mode).
2. Command-Palette SEARCH MODE with natural-language tokenizer & visual chips.
3. Central Magnetic '⚡ Generate Report' button staging state and driving execution.
4. Glassmorphic KPI Telemetry cards with animated number rollups.
5. Direct 8-Question Navigator (Q1 through Q8) across Bar, Line, Heatmap, Mapbox, Scatter OLS, Box, Ratio, Treemap.
6. Cross-domain relationship analysis with Pearson correlation & non-causal disclaimer.
"""

from typing import Dict, Any, List, Optional
import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go

from src.callbacks.data_access import (
    get_filter_options,
    apply_filters,
    compute_kpis,
    parse_search_query,
    get_chart_data
)
from src.charts.registry import get_registered_questions, build_chart, CHART_REGISTRY
from src.components.kpi_cards import render_kpi_cards

dash.register_page(__name__, path="/explore", title="CityLink — Explore Engine")

FILTER_OPTS = get_filter_options()
QUESTIONS = get_registered_questions()


def layout():
    """Render the studio-grade Explore Engine layout."""
    initial_df = apply_filters()
    initial_kpis = compute_kpis(initial_df)
    initial_fig = build_chart("Q1", initial_df)

    # Build question tab pills
    question_pills = []
    for q in QUESTIONS:
        question_pills.append(
            {"label": f"{q['id']}: {q['title']}", "value": q["id"]}
        )

    return html.Div(
        style={"maxWidth": "1280px", "margin": "0 auto", "padding": "2.5rem 1.5rem 6rem 1.5rem"},
        children=[
            # Page Title & Header
            html.Div(
                style={"marginBottom": "2.5rem"},
                children=[
                    html.Div(
                        style={"display": "inline-flex", "alignItems": "center", "gap": "0.6rem", "marginBottom": "0.75rem"},
                        children=[
                            html.Span(
                                style={"width": "8px", "height": "8px", "borderRadius": "50%", "background": "#00F2FE", "boxShadow": "0 0 10px #00F2FE"}
                            ),
                            html.Span("ANALYTICAL ENGINE", style={"fontSize": "0.75rem", "fontWeight": "800", "letterSpacing": "0.12em", "color": "#00F2FE"}),
                            html.Span("•", style={"color": "#64748B"}),
                            html.Span("2,464 SAMPLES READY", style={"fontSize": "0.75rem", "color": "#94A3B8", "fontFamily": "var(--font-mono)"}),
                        ]
                    ),
                    html.H1(
                        "Urban Telemetry & Spatial Evidence",
                        style={
                            "fontSize": "clamp(2.5rem, 5vw, 4rem)",
                            "fontWeight": "900",
                            "letterSpacing": "-0.04em",
                            "margin": "0 0 0.75rem 0",
                            "color": "#FFFFFF",
                            "lineHeight": "1.05"
                        }
                    ),
                    html.P(
                        "Query in natural language or stage multidimensional filters. Visualizations and KPI telemetry calculate upon clicking 'Generate Report'.",
                        style={"color": "#94A3B8", "fontSize": "1.1rem", "margin": 0, "maxWidth": "850px"}
                    )
                ]
            ),

            # Section 1: Command-Palette Search Mode
            html.Div(
                className="bento-card",
                style={"marginBottom": "2rem"},
                children=[
                    html.Div(
                        style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "1.25rem", "flexWrap": "wrap", "gap": "0.5rem"},
                        children=[
                            html.Div([
                                html.Span("SEARCH MODE", style={"fontSize": "0.75rem", "fontWeight": "800", "letterSpacing": "0.1em", "color": "#00F2FE"}),
                                html.Span(" (Natural-Language Tokenizer)", style={"fontSize": "0.75rem", "color": "#64748B"}),
                            ]),
                            html.Span("Try: 'Brooklyn 2022 new construction subway'", style={"fontSize": "0.8rem", "color": "#94A3B8", "fontStyle": "italic"})
                        ]
                    ),
                    html.Div(
                        className="search-mode-box",
                        children=[
                            html.Span("🔍", style={"fontSize": "1.2rem", "opacity": 0.7}),
                            dcc.Input(
                                id="search-input",
                                type="text",
                                placeholder="Type a natural query (e.g. 'Manhattan 2023 affordable housing bus rapid')...",
                                className="search-mode-input",
                                debounce=True
                            ),
                            html.Span("ENTER ↵", className="search-shortcut-badge"),
                            html.Button(
                                "Parse Query",
                                id="btn-parse-search",
                                n_clicks=0,
                                style={
                                    "background": "linear-gradient(135deg, rgba(0, 242, 254, 0.2), rgba(168, 85, 247, 0.2))",
                                    "border": "1px solid rgba(0, 242, 254, 0.4)",
                                    "color": "#00F2FE",
                                    "borderRadius": "9999px",
                                    "padding": "0.55rem 1.4rem",
                                    "fontWeight": "700",
                                    "cursor": "pointer",
                                    "fontSize": "0.85rem",
                                    "transition": "all 0.2s ease"
                                }
                            )
                        ]
                    ),
                    # Chip Output Container
                    html.Div(
                        id="search-chips-container",
                        style={"display": "flex", "flexWrap": "wrap", "gap": "0.5rem", "marginTop": "1rem"},
                        children=[]
                    )
                ]
            ),

            # Section 2: Staged Filter Cockpit (4 Mandatory Dropdowns + Generate Report Button)
            html.Div(
                className="bento-card",
                style={"marginBottom": "3rem"},
                children=[
                    html.Div(
                        style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "1.25rem"},
                        children=[
                            html.Span("STAGE MULTIDIMENSIONAL FILTERS", style={"fontSize": "0.75rem", "fontWeight": "800", "letterSpacing": "0.1em", "color": "#94A3B8"}),
                            html.Span("Changes stage state until button execution", style={"fontSize": "0.75rem", "color": "#64748B"})
                        ]
                    ),
                    html.Div(
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(auto-fit, minmax(230px, 1fr))",
                            "gap": "1.25rem",
                            "marginBottom": "2rem"
                        },
                        children=[
                            # Filter 1: Borough
                            html.Div([
                                html.Label("NYC Borough", style={"fontSize": "0.8rem", "fontWeight": "700", "color": "#E2E8F0", "marginBottom": "0.4rem", "display": "block"}),
                                dcc.Dropdown(
                                    id="filter-borough",
                                    options=[{"label": "All Boroughs", "value": "ALL"}] + [{"label": b, "value": b} for b in FILTER_OPTS["borough"]],
                                    value="ALL",
                                    clearable=False,
                                    className="dash-dropdown"
                                )
                            ]),
                            # Filter 2: Year
                            html.Div([
                                html.Label("Reporting Year", style={"fontSize": "0.8rem", "fontWeight": "700", "color": "#E2E8F0", "marginBottom": "0.4rem", "display": "block"}),
                                dcc.Dropdown(
                                    id="filter-year",
                                    options=[{"label": "All Years (2018–2024)", "value": "ALL"}] + [{"label": str(y), "value": y} for y in FILTER_OPTS["year"]],
                                    value="ALL",
                                    clearable=False,
                                    className="dash-dropdown"
                                )
                            ]),
                            # Filter 3: Housing Category
                            html.Div([
                                html.Label("Housing Classification", style={"fontSize": "0.8rem", "fontWeight": "700", "color": "#E2E8F0", "marginBottom": "0.4rem", "display": "block"}),
                                dcc.Dropdown(
                                    id="filter-housing",
                                    options=[{"label": "All Housing Categories", "value": "ALL"}] + [{"label": h, "value": h} for h in FILTER_OPTS["housing_category"]],
                                    value="ALL",
                                    clearable=False,
                                    className="dash-dropdown"
                                )
                            ]),
                            # Filter 4: Transit Category
                            html.Div([
                                html.Label("Transit Network Mode", style={"fontSize": "0.8rem", "fontWeight": "700", "color": "#E2E8F0", "marginBottom": "0.4rem", "display": "block"}),
                                dcc.Dropdown(
                                    id="filter-transit",
                                    options=[{"label": "All Transit Modes", "value": "ALL"}] + [{"label": t, "value": t} for t in FILTER_OPTS["transit_category"]],
                                    value="ALL",
                                    clearable=False,
                                    className="dash-dropdown"
                                )
                            ]),
                        ]
                    ),
                    # Central Action: Generate Report Button
                    html.Div(
                        style={"display": "flex", "alignItems": "center", "justifyContent": "space-between", "flexWrap": "wrap", "gap": "1.25rem", "borderTop": "1px solid var(--border-subtle)", "paddingTop": "1.5rem"},
                        children=[
                            html.Button(
                                [
                                    html.Span("⚡", style={"fontSize": "1.3rem"}),
                                    html.Span("Generate Report", style={"fontSize": "1.1rem", "fontWeight": "900"}),
                                ],
                                id="btn-generate-report",
                                n_clicks=0,
                                className="btn-generate-report"
                            ),
                            html.Div(
                                id="filter-status-message",
                                style={"fontSize": "0.9rem", "color": "#94A3B8", "fontFamily": "var(--font-mono)"},
                                children="Ready to generate report with active filters."
                            )
                        ]
                    )
                ]
            ),

            # Section 3: Animated KPI Telemetry Display
            dcc.Loading(
                id="loading-kpis",
                type="dot",
                color="#00F2FE",
                children=[
                    html.Div(id="kpi-display-container", children=[render_kpi_cards(initial_kpis)])
                ]
            ),

            # Section 4: Visual Evidence Canvas (Q1–Q8)
            html.Div(
                className="bento-card",
                children=[
                    # Header
                    html.Div(
                        style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "1.5rem", "flexWrap": "wrap", "gap": "1rem"},
                        children=[
                            html.Div([
                                html.Span("VISUAL EVIDENCE GALLERY", style={"fontSize": "0.75rem", "fontWeight": "800", "letterSpacing": "0.1em", "color": "#A855F7"}),
                                html.H2("Research Question Visualizations", style={"fontSize": "1.75rem", "fontWeight": "900", "margin": "0.25rem 0 0 0", "color": "#FFFFFF", "letterSpacing": "-0.03em"})
                            ]),
                            html.Div(
                                style={"width": "100%", "maxWidth": "440px"},
                                children=[
                                    html.Label("Switch Research Question (Q1–Q8):", style={"fontSize": "0.75rem", "fontWeight": "700", "color": "#94A3B8", "marginBottom": "0.35rem", "display": "block"}),
                                    dcc.Dropdown(
                                        id="question-selector",
                                        options=question_pills,
                                        value="Q1",
                                        clearable=False,
                                        className="dash-dropdown"
                                    )
                                ]
                            )
                        ]
                    ),

                    # Question Context Details Banner
                    html.Div(
                        id="question-context-banner",
                        style={
                            "background": "rgba(168, 85, 247, 0.08)",
                            "border": "1px solid rgba(168, 85, 247, 0.25)",
                            "borderRadius": "1.25rem",
                            "padding": "1.25rem 1.5rem",
                            "marginBottom": "2rem"
                        },
                        children=[
                            html.Div(
                                style={"display": "flex", "gap": "0.75rem", "alignItems": "center", "marginBottom": "0.4rem"},
                                children=[
                                    html.Span("ACTIVE QUESTION Q1", id="banner-q-id", style={"fontSize": "0.75rem", "fontWeight": "900", "color": "#A855F7", "letterSpacing": "0.08em"}),
                                    html.Span("•", style={"color": "#64748B"}),
                                    html.Span("Stacked Bar Chart", id="banner-q-type", style={"fontSize": "0.75rem", "color": "#00F2FE", "fontWeight": "700"}),
                                ]
                            ),
                            html.Div(
                                "How do residential housing completions and permits compare across the five NYC boroughs?",
                                id="banner-q-text",
                                style={"fontSize": "1.1rem", "fontWeight": "700", "color": "#FFFFFF", "marginBottom": "0.35rem", "letterSpacing": "-0.01em"}
                            ),
                            html.Div(
                                "Examines borough-level residential unit completions stratified by development category.",
                                id="banner-q-desc",
                                style={"fontSize": "0.9rem", "color": "#94A3B8", "lineHeight": "1.5"}
                            )
                        ]
                    ),

                    # Chart Render Container with Loading State
                    dcc.Loading(
                        id="loading-chart",
                        type="circle",
                        color="#00F2FE",
                        children=[
                            html.Div(
                                id="chart-display-container",
                                children=[
                                    dcc.Graph(
                                        id="main-explore-graph",
                                        figure=initial_fig,
                                        config={"displayModeBar": True, "responsive": True},
                                        style={"height": "560px"}
                                    )
                                ]
                            )
                        ]
                    ),

                    # Empty State Container
                    html.Div(
                        id="empty-state-message",
                        style={"display": "none"},
                        className="empty-state-box",
                        children=[
                            html.Div("🔍", style={"fontSize": "3rem", "marginBottom": "0.75rem"}),
                            html.H3("No Records Found Matching Criteria", style={"color": "#FFFFFF", "marginBottom": "0.5rem"}),
                            html.P("Try broadening your borough, year, or category selections and click 'Generate Report' again.", style={"color": "#94A3B8", "margin": 0})
                        ]
                    )
                ]
            )
        ]
    )


# ==============================================================================
# CALLBACKS FOR EXPLORE PAGE
# ==============================================================================

@callback(
    Output("filter-borough", "value"),
    Output("filter-year", "value"),
    Output("filter-housing", "value"),
    Output("filter-transit", "value"),
    Output("search-chips-container", "children"),
    Input("btn-parse-search", "n_clicks"),
    Input("search-input", "n_submit"),
    State("search-input", "value"),
    prevent_initial_call=True
)
def handle_search_mode(n_clicks: int, n_submit: Optional[int], search_text: Optional[str]):
    """Parse natural language query and update staged filter dropdowns."""
    if not search_text or not search_text.strip():
        return "ALL", "ALL", "ALL", "ALL", []

    res = parse_search_query(search_text)
    filters = res.get("filters", {})
    matched_chips = res.get("matched_chips", [])
    unmatched = res.get("unmatched", [])

    b_val = filters.get("borough", "ALL")
    y_val = filters.get("year", "ALL")
    h_val = filters.get("housing_category", "ALL")
    t_val = filters.get("transit_category", "ALL")

    chips = []
    for chip_text in matched_chips:
        chips.append(
            html.Span([
                html.Span("✓", style={"fontWeight": "900"}),
                html.Span(chip_text)
            ], className="filter-chip")
        )

    if unmatched:
        chips.append(
            html.Span(
                f"Ignored: {', '.join(unmatched[:3])}",
                style={
                    "background": "rgba(255, 255, 255, 0.05)",
                    "color": "#94A3B8",
                    "padding": "0.35rem 0.9rem",
                    "borderRadius": "9999px",
                    "fontSize": "0.75rem",
                    "border": "1px solid rgba(255, 255, 255, 0.1)"
                }
            )
        )

    return b_val, y_val, h_val, t_val, chips


@callback(
    Output("banner-q-id", "children"),
    Output("banner-q-type", "children"),
    Output("banner-q-text", "children"),
    Output("banner-q-desc", "children"),
    Input("question-selector", "value")
)
def update_question_banner(question_id: str):
    """Update contextual question description banner when selector changes."""
    meta = CHART_REGISTRY.get(question_id, CHART_REGISTRY["Q1"])
    return (
        f"ACTIVE QUESTION {meta['id']}",
        f"{meta['chart_type']} ({meta['category']})",
        meta["question"],
        meta["description"]
    )


@callback(
    Output("kpi-display-container", "children"),
    Output("chart-display-container", "children"),
    Output("empty-state-message", "style"),
    Output("filter-status-message", "children"),
    Input("btn-generate-report", "n_clicks"),
    Input("question-selector", "value"),
    State("filter-borough", "value"),
    State("filter-year", "value"),
    State("filter-housing", "value"),
    State("filter-transit", "value"),
    prevent_initial_call=False
)
def execute_generate_report(
    n_clicks: int,
    question_id: str,
    borough: str,
    year: Any,
    housing_cat: str,
    transit_cat: str
):
    """Central callback: Executes data slice and updates KPIs and visualizations.

    Mandatory logic: The central 'Generate Report' button stages state. Visualizations
    and KPIs update when the button is clicked, or when switching the active question view.
    """
    filters: Dict[str, Any] = {}
    if borough and borough != "ALL":
        filters["borough"] = borough
    if year and year != "ALL":
        filters["year"] = int(year)
    if housing_cat and housing_cat != "ALL":
        filters["housing_category"] = housing_cat
    if transit_cat and transit_cat != "ALL":
        filters["transit_category"] = transit_cat

    # Fetch filtered slice
    df = apply_filters(filters)
    kpis = compute_kpis(df)

    if df.empty:
        empty_style = {"display": "block"}
        empty_fig = go.Figure()
        empty_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        graph_children = [dcc.Graph(figure=empty_fig, style={"height": "300px"})]
        status_msg = "Report generated: 0 matching records."
    else:
        empty_style = {"display": "none"}
        fig = build_chart(question_id, df)
        graph_children = [
            dcc.Graph(
                id="main-explore-graph",
                figure=fig,
                config={"displayModeBar": True, "responsive": True},
                style={"height": "560px"}
            )
        ]
        status_msg = f"Report generated: {kpis['total_records']:,} records analyzed across {kpis['active_boroughs']} borough(s)."

    kpi_children = [render_kpi_cards(kpis)]

    return kpi_children, graph_children, empty_style, status_msg

# Frontend Engineering Notes & Architectural Log

> **Project:** CityLink ("Where homes meet rides.")  
> **Course:** GIU Data Engineering and Visualization (Winter 2026, due 9 Nov 2026)  
> **Author:** Autonomous Senior Frontend Engineer  

---

## 1. What Was Built

A full-fledged, multi-page interactive data-storytelling frontend was built from scratch in Python with Dash and Plotly, adhering to the "Midnight Metropolitan" design concept in [`docs/DESIGN.md`](./DESIGN.md) (inspired by Awwwards, Mobbin, and Unseen Studio):

1. **Application Architecture (`src/app.py`):**
   * Multi-page Dash application using `dash.register_page` and absolute package imports.
   * Exposes `server = app.server` for production WSGI deployment via Gunicorn.
   * Runs identically with `python -m src.app` and `gunicorn src.app:server`.
   * Custom HTML index string injecting high-craft display typography (*Plus Jakarta Sans* and *JetBrains Mono*).

2. **Five Integrated Pages (`src/pages/`):**
   * **Landing (`/`):** Immersive hero featuring an interactive, procedural 3D urban voxel grid and kinetic transit spline particles (Three.js and Anime.js), with mission statement and direct routing.
   * **Explore (`/explore`):** Graded analytical engine containing:
     - 4 Multidimensional dropdown filters (Borough, Year, Housing Classification, Transit Network Mode).
     - Natural-language **SEARCH MODE** tokenizing free text (e.g. *"Brooklyn 2022 new construction subway"*) into structured filter states and rendered chips with fallback handling.
     - Central **"Generate Report"** button: filters and search only stage state; KPIs and visualizations update exclusively when clicked.
     - Real-time loading states (`dcc.Loading`) and empty-state messaging.
     - 4 Glassmorphic KPI telemetry cards.
     - Research question navigator toggling between 8 distinct visualizations.
   * **Story (`/story`):** Empirical narrative describing the central research question, key expected vs surprising findings, data harmonisation, non-causal statistical caveats, and actionable policy impacts for NYC agencies (DCP and MTA).
   * **Methodology (`/method`):** Documentation of primary open-source feeds (DOB, HPD, MTA, Census ACS), geocoding/cleaning pipelines, spatial joins, and analytical limitations.
   * **Team (`/team`):** Roster for the 4-member development team with portfolio cards, contribution breakdowns, and clear placeholders for student names and IDs.

3. **Chart Visualizations & Registry (`src/charts/`):**
   * Shared dark theme [`src/charts/theme.py`](../src/charts/theme.py) applying transparent backgrounds, high-contrast labels, and custom glass hovercards.
   * 8 registered research questions (Q1–Q8) mapped in [`src/charts/registry.py`](../src/charts/registry.py):
     - **Q1 (Stacked Bar):** Borough Residential Housing Units by Development Category.
     - **Q2 (Multi-Trace Line):** Multi-Year Housing Completions vs Transit Ridership (2018–2024).
     - **Q3 (2D Heatmap):** Transit Accessibility Index across Housing Classifications and Boroughs.
     - **Q4 (Carto Dark Mapbox Scatter):** Spatial overlay of residential projects and subway hub density (zero API token required).
     - **Q5 (Cross-Domain Scatter OLS):** Housing Density vs Commute Time correlation with OLS trendline, Pearson $r$, $R^2$, and explicit non-causal disclaimer.
     - **Q6 (Box Distribution):** Transit accessibility score variance across project types.
     - **Q7 (Horizontal Ratio Bar):** Transit facility density normalized per 1,000 residential units.
     - **Q8 (Hierarchical Treemap):** Multi-level breakdown across boroughs and housing classifications.

4. **Self-Contained Vendored Assets (`src/assets/`):**
   * Three.js (r128) and Anime.js (v3.2.2) vendored locally in `src/assets/vendor/` with zero runtime CDN dependencies.
   * Kinetic 3D spatial urban canvas and counter animations in `src/assets/js/z_citylink_interactive.js`.
   * High-contrast, glassmorphic CSS design system in `src/assets/css/citylink_theme.css` with WCAG AA compliance and `prefers-reduced-motion` support.

5. **Test Harness (`tests/`):**
   * 13 unit and smoke tests passing across `test_app_smoke.py`, `test_frontend_data_access.py`, `test_frontend_charts.py`, and `test_frontend_pages.py`.

---

## 2. Assumptions Log

1. **Research Question Scope:** Since `docs/` contained no preexisting question list, 8 rigorous questions connecting NYC housing and transit were derived to support a 4-member team, covering all mandatory chart typologies.
2. **Vendored Libraries:** Three.js and Anime.js were version-pinned and vendored in `src/assets/vendor/` to satisfy offline runtime constraints.
3. **Map Tiles:** Open-source `carto-darkmatter` style is utilized for spatial maps via Plotly Scatter Map/Mapbox to guarantee zero requirement for proprietary Mapbox access tokens.
4. **Fixture Disclaimers:** All dev fixture data is explicitly tagged with `is_fixture: True`, and KPI banners inform visitors that verification fixture data is loaded until backend ETL tables are mounted.

---

## 3. Data Access Adapter Interface (`src/callbacks/data_access.py`)

To ensure the frontend is completely decoupled from ongoing data engineering and backend work, all UI components interact strictly with `data_access.py`.

### Implemented Adapter Interface:
```python
def get_filter_options() -> Dict[str, List[Any]]:
    """Returns available options for borough, year, housing_category, and transit_category."""

def apply_filters(filters: Optional[Dict[str, Any]]) -> pd.DataFrame:
    """Accepts selected criteria and returns the filtered DataFrame slice."""

def compute_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Computes total_units, avg_commute_time, avg_accessibility, total_ridership_m, etc."""

def parse_search_query(text: str) -> Dict[str, Any]:
    """Translates natural-language search into discrete filter keys and display chips."""

def get_chart_data(question_id: str, filters: Optional[Dict[str, Any]]) -> pd.DataFrame:
    """Returns tailored data subsets for each registered research question (Q1 through Q8)."""
```

---

## 4. Backend Handoff Contract (What the Backend Must Provide)

When the backend team implements `src/data`, they simply need to export the same five functions from `src/data/__init__.py` or `src/data/api.py`:
- `get_filter_options()`
- `apply_filters(filters)`
- `compute_kpis(df)`
- `parse_search_query(text)`
- `get_chart_data(question_id, filters)`

`data_access.py` automatically detects when `src.data` provides these capabilities and switches seamlessly from `dev_fixture.py` to the real data pipeline with zero frontend modifications needed.

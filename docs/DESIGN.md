# CityLink Design Concept & Creative Direction

> **Tagline:** *"Where homes meet rides."*  
> **Mission:** An interactive, spatial data-storytelling platform exploring the nexus between New York City housing development and urban transportation networks. Built for the GIU course *Data Engineering and Visualization* (Winter 2026).

---

## 1. Identity & Visual Metaphor

CityLink visualizes New York City as an interconnected living organism: **the fixed vertical skeleton of housing and zoning** intertwined with **the dynamic circulatory system of subways, buses, and micro-mobility**.

### The Aesthetic Tone: "Midnight Metropolitan"
* **Atmosphere:** Deep nocturnal urban backdrop, reminiscent of flying over Manhattan at 2:00 AM. It feels analytical, cinematic, and deeply intentional—prioritizing clarity while evoking the quiet energy of the city.
* **Palette:**
  * **Deep Canvas:** `#08090E` (Obsidian Blue-Black) and `#0F111A` (Dark Slate Surface).
  * **Residential / Housing Hue:** `#FF6B6B` to `#FFA07A` (Warm Brick Coral & Architectural Amber).
  * **Transportation / Motion Hue:** `#00F2FE` to `#4FACFE` (Electric Subway Cyan & Kinetic Blue).
  * **Convergence / Nexus Hue:** `#A855F7` to `#7928CA` (Iridescent Violet, representing the intersection where homes meet rides).
  * **Text & Data:** `#F8FAFC` (Primary 98% White), `#94A3B8` (Secondary Slate 400), `#64748B` (Muted Label 500).
* **Typography:**
  * **Display & Headlines:** *Space Grotesk* or *Plus Jakarta Sans*—architectural, geometric, high-contrast.
  * **Data & Body:** *Inter* / System Sans—ultra-legible, calibrated for numerical scanning and tabular data.
  * **Monospace / Indicators:** *JetBrains Mono*—for filter tags, coordinates, and statistics.

---

## 2. Spatial & Surface Architecture

1. **Bento Grid Hierarchy:**
   * Structured, asymmetrical bento card layout inspired by modern high-density dashboards (Linear, Arc, Apple).
   * Cards use subtle glassmorphism (`background: rgba(15, 17, 26, 0.75)`, `backdrop-filter: blur(24px)`, and `border: 1px solid rgba(255, 255, 255, 0.08)`).
   * Squircle border-radii (`border-radius: 1.5rem`) with gentle inner specular rim highlights.

2. **Visual Depth & Contrast:**
   * Clear spatial separation between the ambient background, the 3D interactive layer, and the data-card plane.
   * Visual elements never compete with charts. Chart canvases feature zero-opacity paper backgrounds so Plotly traces float natively inside the glass cards.

---

## 3. 3D & Kinetic Interaction (Three.js & Anime.js)

### A. Three.js Spatial Urban Canvas (Landing Page Hero)
* **Visual Representation:** An interactive, procedural 3D wireframe and volumetric voxel grid representing NYC boroughs.
* **Dual Particle Systems:**
  * *Static Voxel Columns:* Floating isometric pillars whose heights signify housing density across Manhattan, Brooklyn, Queens, Bronx, and Staten Island.
  * *Kinetic Transit Splines:* Illuminated glowing particle pulses traveling along curvilinear bezier transit corridors.
* **Cursor Proximity & Inertia:**
  * The camera glides with subtle, dampened parallax following the user's pointer (`lerp` smoothing).
  * Hovering near borough clusters triggers localized ambient pulses without blocking text readability.
* **Performance & Fallback Budget:**
  * Target: Solid 60 FPS on mid-range laptops.
  * Reused geometry instances (`InstancedMesh`) and zero memory allocations in the render loop.
  * Honors `prefers-reduced-motion`: animation freezes into an elegant static architectural snapshot.

### B. Anime.js Micro-Interactions & State Transitions
* **Number Rollups:** Metric KPI cards smoothly count up from zero (`anime({ targets: '.kpi-value', round: 1, easing: 'easeOutExpo' })`) on initial load and report generation.
* **Generate Report Staging:**
  * The central "Generate Report" button features an energetic glowing pulse and subtle magnetic hover pull.
  * When clicked, filter chips display a brief confirmation ripple, a high-tech glowing scanline sweeps across the canvas, and cards crossfade with a staggered entrance.
* **Filter Chips:** Pill tags dynamically pop in and out with elastic scale transforms (`scale: [0.8, 1], opacity: [0, 1]`).

---

## 4. Data-First Visualization Principles

The visual flair strictly supports—and never obscures—the scientific story:
1. **Zero Misleading Visuals:** No 3D pie charts, no truncated zero baselines on bar charts, and no ungrounded dual axes.
2. **Chart Typology Grounding:**
   * **Bar Charts:** Categorical comparisons (e.g. residential unit completions by borough) with value annotations.
   * **Line Charts:** Temporal evolution across years with clean confidence bands.
   * **Heatmaps:** Two-dimensional density matrices (e.g. Transit proximity vs Median rent index).
   * **Spatial Maps:** Choropleth & scatter point overlays on OpenStreetMap / Carto Dark basemaps without requiring external proprietary API tokens.
   * **Cross-Domain Scatter:** Directly interrogates correlation with an ordinary least squares (OLS) trendline, annotated Pearson correlation coefficient $r$, and explicit disclaimer that *correlation is not causation*.
3. **Information Density & Accessibility:**
   * High contrast compliance (WCAG AA compliant contrast ratios $\ge 4.5:1$).
   * Full keyboard navigation and visible focus rings (`focus-visible: 2px solid #00F2FE`).
   * Informative, multi-line custom hover tooltips showing context, exact numbers, and borough details.

---

## 5. Responsive & Scalable Layout

* **Desktop ($\ge 1200\text{px}$):** Multi-column bento grid, side-by-side filter staging and KPI telemetry, full interactive 3D hero.
* **Tablet ($768\text{px} - 1199\text{px}$):** Stacked 2-column bento modules, sticky filter bar, scaled-down 3D canvas.
* **Mobile ($< 768\text{px}$):** Single-column layout, bottom-sheet filter drawer, touch-optimized button targets ($\ge 44\text{px}$), and simplified low-overhead canvas.

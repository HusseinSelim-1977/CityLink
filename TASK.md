# TASK: Redesign CityLink frontend (Dash/Plotly)

Only edit: src/app.py, src/pages, src/components, src/charts, src/callbacks, src/assets. Never touch the data pipeline.
Data: H4 (DOB Job Application Filings) + T5 (Bus Breakdown and Delays) only.
Style: light theme, beige/off-white + black, award-level modern UI, smooth animation (inspired by awwwards.com, mobbin.com, unseen.co; screenshots only, never scrape).

Must have:
1. Dropdowns: Borough, Year, H4 category, T5 category
2. Search box that parses "Brooklyn 2022 new buildings" into filters
3. One "Generate Report" button that updates ALL charts
4. Bar, line, heatmap, map, scatter charts + one H4-vs-T5 relationship chart
5. Story section: question, findings, limitations, benefit to NYC
6. Loading and empty states

## Progress (update after each step)
- [ ] 1 design tokens + Plotly template (assets/style.css, charts/theme.py)
- [ ] 2 app shell/layout (app.py, components/)
- [ ] 3 filters + search + Generate Report (callbacks/)
- [ ] 4 charts (charts/)
- [ ] 5 story section (pages/)
- [ ] 6 run app, fix errors

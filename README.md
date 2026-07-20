# Interactive Data Dashboards

A small collection of self-built, interactive web dashboards, kept here as a
public portfolio piece. Each dashboard is a single, self-contained HTML file
(vanilla JavaScript + [Chart.js](https://www.chartjs.org/)) and is published
via GitHub Pages — no build step, no framework.

**Live site:** https://volmar86.github.io/dashboards/

---

## Dashboards

### ⛽ Gas Storage Predictor (live data)
`dashboards_live/lng-predictor/`

Tracks and projects European natural-gas storage levels — the EU average
alongside Italy and Germany specifically. It combines real historical
inventory data with adjustable linear and seasonal fill/withdrawal rates,
letting the user simulate different trajectories toward the winter target
levels.

- **Data source:** [GIE AGSI](https://agsi.gie.eu/) platform
- **Auto-updating:** a scheduled GitHub Action refreshes `data.json` every week
- **Resilience:** if the live feed is unavailable, the page falls back to a
  bundled `data_fallback.json` snapshot, so it never renders empty

🔗 https://volmar86.github.io/dashboards/dashboards_live/lng-predictor/

### 🌊 Hormuz Critical-Level Monitor (static data)
`dashboards_static/`

Estimates when gas storage would reach critical thresholds under stress
scenarios. Data is embedded directly in the page (no external feed).

🔗 https://volmar86.github.io/dashboards/dashboards_static/

### 🎨 Montessori Teaching Dashboards
`montessori_dashboards/`

Interactive tools intended for use in my Montessori teaching activity.

🔗 https://volmar86.github.io/dashboards/montessori_dashboards/

---

## Repository structure

# Interactive Data Dashboards

A small collection of self-built, interactive web dashboards, kept here as a
public portfolio piece. Each dashboard is a single, self-contained HTML file
(vanilla JavaScript + [Chart.js](https://www.chartjs.org/)) and is published
via GitHub Pages — no build step, no framework.

**Live site:** [volmar86.github.io/dashboards](https://volmar86.github.io/dashboards/)

## Tech stack

- **HTML5 / CSS3** — layout and styling (Tailwind via CDN)
- **Vanilla JavaScript** — interactivity, state, simulation logic (no framework)
- **Chart.js** — data visualisation
- **Python** — data-fetching and processing script that builds `data.json`
  (pulls from the AGSI API, computes rolling and seasonal rates)
- **GitHub Actions** — scheduled workflow that runs the Python script weekly
- **GitHub Pages** — hosting

---

## Dashboards

### ⛽ Gas Storage Predictor (live data) — [view live](https://volmar86.github.io/dashboards/dashboards_live/lng-predictor/)
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

### 🌊 Hormuz Critical-Level Monitor (static data) — [view live](https://volmar86.github.io/dashboards/dashboards_static/)
`dashboards_static/`

Estimates when gas storage would reach critical thresholds under stress
scenarios. Data is embedded directly in the page (no external feed).

### 🎨 Montessori Teaching Dashboards — [view live](https://volmar86.github.io/dashboards/montessori_dashboards/)
`montessori_dashboards/`

Interactive tools intended for use in my Montessori teaching activity.

---

## Repository structure

```text
dashboards/
├── .github/workflows/          # Scheduled GitHub Action (weekly data update)
├── dashboards_live/            # Dashboards fed by external, auto-updated data
│   └── lng-predictor/
│       ├── index.html          # The dashboard
│       ├── data.json           # Live data (refreshed by the Action)
│       └── data_fallback.json  # Frozen backup snapshot
├── dashboards_static/          # Dashboards with data embedded in the HTML
├── montessori_dashboards/      # Teaching tools
└── README.md
```

## How the live update works

A GitHub Action runs on a weekly schedule, runs a Python script that pulls the
latest figures from the GIE AGSI API, recomputes the rolling and seasonal
rates, and commits the refreshed `data.json` back to the repository. The
dashboard reads that file on load.

---

*Built and maintained by [@volmar86](https://github.com/volmar86).*

# Spotify Analytics Dashboard

Interactive analytics over a large Spotify tracks dataset: genres, audio features, correlations, scatter explorations, tempo distributions, and an animated genre “race” across tempo bins.

**Live site:** [https://plotly-spotify-dashboard.vercel.app/](https://plotly-spotify-dashboard.vercel.app/)

---

## Features

- **Genre insights** — Top genres by average popularity, track share (donut), popularity distributions (box plots), and a popularity funnel (tiers &gt;50 / &gt;75 / &gt;90).
- **Audio features** — Line chart of average danceability, energy, valence, and acousticness across top genres (toggle series); violin plot for danceability; Pearson correlation heatmap.
- **Track explorer** — Sampled scatter plots (energy vs danceability, energy vs valence) with genre color and rich hover (track name, artists, popularity).
- **Trends** — Tempo histogram and an **animated** bar chart of genre popularity across tempo bins.

The UI is a single-page dark theme with tabbed sections and responsive Plotly charts (zoom, pan, hover).

---

## How it works

| Layer | Role |
|--------|------|
| **`index.html`** | Frontend: layout, styles, and JavaScript. Loads [Plotly.js](https://plotly.com/javascript/) from a CDN and renders figures from JSON. |
| **`charts.json`** | Pre-built chart definitions and summary stats (`_stats`), produced by the Python script. The deployed site only needs this file plus `index.html`. |
| **`generate_charts.py`** | Offline pipeline: reads `dataset.csv`, builds figures with Plotly Express, serializes them into `charts.json`. Not executed on Vercel for the current setup. |
| **Hosting** | [Vercel](https://vercel.com/) serves the repo as **static files** (no app server or database on each request). |

---

## Tech stack

- **Python:** pandas, NumPy, Plotly (Python) — chart generation  
- **Browser:** HTML, CSS, vanilla JavaScript, Plotly.js (CDN)  
- **Deploy:** Vercel (static)

---

## Requirements

- Python **3.10+** (3.12 recommended)
- `dataset.csv` in the project root (Spotify-style tracks + audio features; see [Data](#data))

---

## Local setup

```bash
git clone https://github.com/shivammarkanday/plotly-spotify-dashboard.git
cd plotly-spotify-dashboard

python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Place **`dataset.csv`** next to `generate_charts.py`, then regenerate the dashboard data:

```bash
python generate_charts.py
```

You should see `charts.json` created or updated and a short summary in the terminal.

### Preview the site locally

Browsers block `fetch('charts.json')` on `file://`, so serve the folder over HTTP:

```bash
python3 -m http.server 8000
```

Open **[http://127.0.0.1:8000/index.html](http://127.0.0.1:8000/index.html)** (or `/` if the server lists `index.html` as the default).

---

## Deploying to Vercel

1. Push this repository to GitHub.
2. **Import** the repo in Vercel.
3. Set **Framework Preset** to **Other** (static site; no Node build required).
4. Leave **Root Directory** as `./` and use default build/output unless you add a build step.
5. Deploy. Ensure **`charts.json`** is committed so the live site can load chart data.

---

## Project structure

```
.
├── README.md
├── requirements.txt
├── dataset.csv          # Source data (not required on Vercel for current UI)
├── generate_charts.py   # Builds charts.json from dataset.csv
├── charts.json          # Serialized figures + stats for the browser
├── index.html           # Dashboard UI
└── .gitignore
```

---

## Data

The pipeline expects a CSV with Spotify track metadata and audio features (e.g. columns such as `track_name`, `artists`, `track_genre`, `popularity`, `danceability`, `energy`, `valence`, `tempo`, etc.), consistent with public **Spotify tracks** datasets on [Kaggle](https://www.kaggle.com/). Use whichever Kaggle release you are licensed to use, and keep attribution/licensing per that dataset’s terms.

---

## Author

Course / portfolio project (**Lab 7** reference in the site footer).  
Repository: **plotly-spotify-dashboard** · Demo: [plotly-spotify-dashboard.vercel.app](https://plotly-spotify-dashboard.vercel.app/).

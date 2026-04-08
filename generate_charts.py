import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px

# ── Load your dataset ──────────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
_DATA_CSV = _SCRIPT_DIR / "dataset.csv"
if not _DATA_CSV.is_file():
    raise SystemExit(
        f"Missing {_DATA_CSV.name}. Download or copy your Spotify tracks CSV into:\n  {_SCRIPT_DIR}"
    )
df = pd.read_csv(_DATA_CSV)
df = df.drop(columns=['Unnamed: 0'], errors='ignore')

charts = {}

# ── GENRE INSIGHTS ─────────────────────────────────

# 1. Bar: Top 15 Genres by Avg Popularity
genre_pop = df.groupby('track_genre')['popularity'].mean().nlargest(15).reset_index()
fig = px.bar(genre_pop, x='track_genre', y='popularity', color='popularity',
             color_continuous_scale='viridis',
             labels={'track_genre': 'Genre', 'popularity': 'Avg Popularity'})
fig.update_layout(xaxis_tickangle=-45, template='plotly_dark',
                  paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                  showlegend=False, coloraxis_showscale=False,
                  margin=dict(t=10, b=60, l=40, r=10))
charts['bar_genre_pop'] = json.loads(fig.to_json())

# 2. Donut: Track Distribution Top 10 Genres
top10 = df['track_genre'].value_counts().nlargest(10).reset_index()
top10.columns = ['genre', 'count']
fig = px.pie(top10, names='genre', values='count', hole=0.45)
fig.update_traces(textinfo='percent+label', textfont_size=11)
fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
                  showlegend=False, margin=dict(t=10, b=10, l=10, r=10))
charts['donut_track_dist'] = json.loads(fig.to_json())

# 3. Box: Popularity Distribution across Top 10 Genres
top10_genres = df.groupby('track_genre')['popularity'].mean().nlargest(10).index
df_box = df[df['track_genre'].isin(top10_genres)]
fig = px.box(df_box, x='track_genre', y='popularity', color='track_genre',
             labels={'track_genre': 'Genre', 'popularity': 'Popularity'})
fig.update_layout(xaxis_tickangle=-45, template='plotly_dark',
                  paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                  showlegend=False, margin=dict(t=10, b=80, l=40, r=10))
charts['box_popularity'] = json.loads(fig.to_json())

# 4. Funnel: Popularity Tiers
total      = len(df)
popular    = len(df[df['popularity'] > 50])
very_pop   = len(df[df['popularity'] > 75])
hits       = len(df[df['popularity'] > 90])
funnel_df  = pd.DataFrame({
    'Stage': ['All Tracks', 'Popular (>50)', 'Very Popular (>75)', 'Hits (>90)'],
    'Count': [total, popular, very_pop, hits]
})
fig = px.funnel(funnel_df, x='Count', y='Stage', color='Stage')
fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)', showlegend=False,
                  margin=dict(t=10, b=10, l=20, r=10))
charts['funnel_popularity'] = json.loads(fig.to_json())

# ── AUDIO FEATURES ─────────────────────────────────

# 5. Line: Avg Audio Features across Top 10 Genres
top_genres = df.groupby('track_genre')['popularity'].mean().nlargest(10).index
df_top     = df[df['track_genre'].isin(top_genres)]
features   = ['danceability', 'energy', 'valence', 'acousticness']
genre_avg  = df_top.groupby('track_genre')[features].mean().reset_index()
genre_melt = genre_avg.melt(id_vars='track_genre', var_name='Feature', value_name='Average')
fig = px.line(genre_melt, x='track_genre', y='Average', color='Feature', markers=True,
              labels={'track_genre': 'Genre', 'Average': 'Average Value'})
fig.update_layout(xaxis_tickangle=-45, template='plotly_dark',
                  paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                  legend=dict(orientation='h', y=1.1),
                  margin=dict(t=20, b=80, l=40, r=10))
charts['line_features'] = json.loads(fig.to_json())

# 6. Heatmap: Feature Correlation
numeric_cols = ['popularity', 'danceability', 'energy', 'loudness', 'speechiness',
                'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
corr = df[numeric_cols].corr().round(2)
fig  = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r', aspect='auto')
fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  margin=dict(t=10, b=10, l=10, r=10))
charts['heatmap_corr'] = json.loads(fig.to_json())

# 7. Violin: Danceability across Top 8 Genres
top8    = df.groupby('track_genre')['popularity'].mean().nlargest(8).index
df_vio  = df[df['track_genre'].isin(top8)]
fig     = px.violin(df_vio, x='track_genre', y='danceability', color='track_genre',
                    box=True, points=False,
                    labels={'track_genre': 'Genre', 'danceability': 'Danceability'})
fig.update_layout(xaxis_tickangle=-45, template='plotly_dark',
                  paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                  showlegend=False, margin=dict(t=10, b=80, l=40, r=10))
charts['violin_dance'] = json.loads(fig.to_json())

# ── TRACK EXPLORER ─────────────────────────────────

# 8. Scatter: Energy vs Danceability
df_s1 = df.sample(2000, random_state=42)
fig   = px.scatter(df_s1, x='energy', y='danceability', color='track_genre',
                   size='popularity', hover_data=['track_name', 'artists'],
                   labels={'energy': 'Energy', 'danceability': 'Danceability'})
fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)', showlegend=False,
                  margin=dict(t=10, b=40, l=40, r=10))
charts['scatter_energy_dance'] = json.loads(fig.to_json())

# 9. Scatter: Energy vs Valence (rich hover)
df_s2 = df.sample(1000, random_state=42)
fig   = px.scatter(df_s2, x='energy', y='valence', color='track_genre',
                   hover_name='track_name',
                   hover_data={'artists': True, 'popularity': True,
                               'danceability': ':.2f', 'track_genre': False},
                   labels={'energy': 'Energy', 'valence': 'Valence'})
fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)', showlegend=False,
                  margin=dict(t=10, b=40, l=40, r=10))
fig.update_traces(marker=dict(size=8, opacity=0.7))
charts['scatter_energy_valence'] = json.loads(fig.to_json())

# ── TRENDS & DISTRIBUTION ──────────────────────────

# 10. Histogram: Tempo Distribution
fig = px.histogram(df, x='tempo', nbins=50,
                   color_discrete_sequence=['#1DB954'],
                   labels={'tempo': 'Tempo (BPM)', 'count': 'Number of Tracks'})
fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  margin=dict(t=10, b=40, l=40, r=10))
charts['hist_tempo'] = json.loads(fig.to_json())

# 11. Animated Bar: Genre Popularity Race across Tempo Bins
df_anim             = df.copy()
df_anim['tempo_bin'] = pd.cut(df_anim['tempo'], bins=8,
                               labels=[f'Bin {i+1}' for i in range(8)])
top8g   = df_anim.groupby('track_genre')['popularity'].mean().nlargest(8).index
df_anim = df_anim[df_anim['track_genre'].isin(top8g)]
anim_df = df_anim.groupby(['tempo_bin', 'track_genre'])['popularity'].mean().reset_index()
anim_df['tempo_bin'] = anim_df['tempo_bin'].astype(str)
fig = px.bar(anim_df, x='track_genre', y='popularity', color='track_genre',
             animation_frame='tempo_bin',
             labels={'track_genre': 'Genre', 'popularity': 'Avg Popularity'},
             range_y=[0, anim_df['popularity'].max() + 10])
fig.update_layout(xaxis_tickangle=-45, template='plotly_dark',
                  paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                  showlegend=False, margin=dict(t=10, b=80, l=40, r=30))
charts['anim_tempo_race'] = json.loads(fig.to_json())

# ── World map (genre → country proxy; CSV has no lat/lon) ──
# Map clearly regional genre names to ISO-3166 alpha-3 for choropleth.
_GENRE_TO_ISO3 = {
    "afrobeat": "NGA",
    "anime": "JPN",
    "brazil": "BRA",
    "british": "GBR",
    "cantopop": "HKG",
    "chicago-house": "USA",
    "country": "USA",
    "dancehall": "JAM",
    "detroit-techno": "USA",
    "forro": "BRA",
    "french": "FRA",
    "german": "DEU",
    "honky-tonk": "USA",
    "indian": "IND",
    "iranian": "IRN",
    "j-dance": "JPN",
    "j-idol": "JPN",
    "j-pop": "JPN",
    "j-rock": "JPN",
    "k-pop": "KOR",
    "latin": "MEX",
    "latino": "COL",
    "malay": "MYS",
    "mandopop": "CHN",
    "mpb": "BRA",
    "pagode": "BRA",
    "reggae": "JAM",
    "reggaeton": "COL",
    "samba": "BRA",
    "salsa": "COL",
    "sertanejo": "BRA",
    "spanish": "ESP",
    "swedish": "SWE",
    "tango": "ARG",
    "turkish": "TUR",
}
_df_geo = df[df["track_genre"].isin(_GENRE_TO_ISO3.keys())].copy()
_df_geo["iso3"] = _df_geo["track_genre"].map(_GENRE_TO_ISO3)
_geo = (
    _df_geo.groupby("iso3", as_index=False)
    .agg(avg_popularity=("popularity", "mean"), tracks=("track_id", "count"))
    .sort_values("tracks", ascending=False)
)
fig = px.choropleth(
    _geo,
    locations="iso3",
    color="avg_popularity",
    locationmode="ISO-3",
    hover_data={"tracks": True, "iso3": True},
    color_continuous_scale="Viridis",
    labels={
        "avg_popularity": "Avg popularity",
        "iso3": "Country (ISO-3)",
        "tracks": "Tracks (mapped genres)",
    },
    title="",
)
fig.update_traces(hovertemplate=(
    "<b>%{location}</b><br>"
    "Avg popularity: %{z:.1f}<br>"
    "Tracks: %{customdata[0]}<extra></extra>"
))
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=10, b=10, l=10, r=10),
    coloraxis_colorbar=dict(
        title=dict(text="Avg popularity", font=dict(size=11)),
        tickfont=dict(size=10),
    ),
)
fig.update_geos(
    projection_type="natural earth",
    showland=True,
    landcolor="#15151c",
    showocean=True,
    oceancolor="#0a0a0f",
    showcountries=True,
    countrycolor="rgba(29,185,84,0.25)",
    coastlinecolor="rgba(120,120,140,0.35)",
    bgcolor="rgba(0,0,0,0)",
    lonaxis_range=[-180, 180],
    lataxis_range=[-60, 85],
)
charts["world_map"] = json.loads(fig.to_json())

# ── Stats for header cards ─────────────────────────
top_genre   = df.groupby('track_genre')['popularity'].mean().idxmax()
hit_pct     = round(len(df[df['popularity'] > 90]) / len(df) * 100, 1)
total_tracks = len(df)
total_genres = df['track_genre'].nunique()

charts['_stats'] = {
    'total_tracks': f"{total_tracks:,}",
    'total_genres': str(total_genres),
    'top_genre':    top_genre,
    'hit_pct':      f"{hit_pct}%"
}

# ── Write output ───────────────────────────────────
_OUT_JSON = _SCRIPT_DIR / "charts.json"
with open(_OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(charts, f)

print("✅ charts.json generated successfully!")
print(f"   Tracks: {total_tracks:,} | Genres: {total_genres} | Top Genre: {top_genre} | Hits: {hit_pct}%")
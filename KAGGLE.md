# Kaggle upload runbook

Steps to publish this dataset on Kaggle once you have an account. Takes about 10 minutes. Kaggle datasets rank well in Google and get organic traffic from data scientists searching for "sports odds dataset" and similar terms.

## One-time setup

1. Create an account at https://www.kaggle.com (Google SSO is fine). Pick a public-facing username, e.g. `parlayapi`.
2. Verify your phone number in Account settings (required to publish datasets).

## Publish via the website (easiest)

1. Go to https://www.kaggle.com/datasets and click "New Dataset".
2. Upload the three CSVs from `data/` (drag and drop).
3. Title: use the paste-ready title below. Kaggle generates the URL slug from it.
4. Click "Create". The dataset starts private.
5. Open the dataset page, click the pencil / "Edit" to fill in metadata:
   - Subtitle: paste from below.
   - Description: paste from below.
   - License: select "CC BY 4.0 (Attribution 4.0 International)".
   - Tags: `football`, `baseball`, `gambling`, `sports`, `data analytics`.
   - Provenance: sources "Exported from the ParlayAPI production archive (parlay-api.com)".
6. In Settings, flip visibility to Public.
7. Optional but high leverage: create one short public notebook on the dataset ("Line shopping across sportsbooks in 5 minutes with pandas"), since notebooks drive most Kaggle dataset discovery. `load_example.py` in this repo converts almost line-for-line.

## Or publish via the CLI

```bash
pip install kaggle
# Get an API token: kaggle.com -> Settings -> API -> Create New Token
# Save it to ~/.kaggle/kaggle.json, chmod 600

cd /path/to/sports-odds-datasets
mkdir -p kaggle-upload && cp data/*.csv kaggle-upload/
cat > kaggle-upload/dataset-metadata.json <<'JSON'
{
  "title": "Sportsbook Closing Lines: NFL, MLB + 50k Player Props",
  "id": "YOUR_KAGGLE_USERNAME/sportsbook-closing-lines",
  "licenses": [{"name": "CC-BY-4.0"}]
}
JSON
kaggle datasets create -p kaggle-upload/
```

Then add the subtitle, description, and tags on the website (the CLI cannot set all of them).

## Paste-ready metadata

**Title**

```
Sportsbook Closing Lines: NFL, MLB + 50k Player Props
```

**Subtitle**

```
Per-book closing odds: Super Bowl LX, a full 15-game MLB slate, and 50,000 player prop closes across 43 sources.
```

**Description**

```
Real per-sportsbook closing lines exported from the ParlayAPI production archive (https://parlay-api.com).

Three files:

1. superbowl_lx_closing_lines.csv: Super Bowl LX (2026-02-08, Seahawks at Patriots). Closing moneyline, spread, and total from 13 sources, including consensus opening and closing lines.

2. mlb_2026-08-23_closing_lines.csv: one complete MLB day (15 games, all 30 teams) with 1,151 per-book rows across 56 sources, including opening-line snapshots for line-movement analysis.

3. prop_closing_lines_sample_50k.csv: a random 50,000-row sample of player prop closing lines across 43 sources, 23,000+ players, and 1,400+ market keys (MLB, NBA, WNBA, NHL, soccer, tennis, table tennis, esports, and more), sampled from an archive of 30M+ prop closes collected since 2022.

Columns cover American and decimal odds, spreads, totals, implied probabilities, final scores, and capture timestamps. Full schema documentation: https://github.com/JacobiusMakes/sports-odds-datasets

Good for: closing line value (CLV) studies, vig/hold comparison across books, line shopping analysis, calibration of prediction models, teaching material.

Collection method: exported from the ParlayAPI production archive, which aggregates 30+ sportsbooks plus additional data sources across 90+ sport keys (1.7M+ game closing lines back to 2005, 30M+ prop closes since 2022). For live or complete data there is a free API tier (1,000 credits/month, no card): https://parlay-api.com

License: CC BY 4.0. Attribution: ParlayAPI (parlay-api.com).
```

## After publishing

- Add the Kaggle URL to this repo's README.
- Link the Kaggle dataset back to https://github.com/JacobiusMakes/sports-odds-datasets and https://parlay-api.com in the description (already in the paste above).

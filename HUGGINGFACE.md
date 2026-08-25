# Hugging Face upload runbook

Steps to mirror this dataset on the Hugging Face Hub once you have an account. Takes about 10 minutes. HF datasets are indexed by search engines, load directly in pandas and the `datasets` library, and are increasingly what LLM-era developers reach for first.

## One-time setup

1. Create an account at https://huggingface.co/join. Username suggestion: `parlayapi`.
2. Create an access token: Settings -> Access Tokens -> "New token", type "Write".

## Publish via the website

1. Go to https://huggingface.co/new-dataset
2. Owner: your account. Dataset name: `sportsbook-closing-lines`. License: `cc-by-4.0`. Public.
3. On the new repo page, "Files" tab -> "Add file" -> "Upload files": upload the three CSVs into a `data/` folder (type `data/` in the filename box before the file name, or just upload flat).
4. Edit the auto-created `README.md` and replace it with the paste-ready dataset card below (keep the YAML block at the very top).

## Or publish via the CLI

```bash
pip install huggingface_hub
hf auth login   # paste your write token

cd /path/to/sports-odds-datasets
hf repo create sportsbook-closing-lines --repo-type dataset
hf upload YOUR_HF_USERNAME/sportsbook-closing-lines data/ data/ --repo-type dataset
# then upload the card below as README.md:
hf upload YOUR_HF_USERNAME/sportsbook-closing-lines README_hf.md README.md --repo-type dataset
```

## Paste-ready dataset card (README.md on the Hub)

````markdown
---
license: cc-by-4.0
pretty_name: Sportsbook Closing Lines (Game Lines + Player Props)
tags:
- sports
- sports-betting
- odds
- closing-lines
- sports-analytics
- tabular
size_categories:
- 10K<n<100K
language:
- en
---

# Sportsbook Closing Lines: NFL, MLB + 50k Player Props

Real per-sportsbook closing odds exported from the [ParlayAPI](https://parlay-api.com) production archive.

## Files

- `data/superbowl_lx_closing_lines.csv` (13 rows): Super Bowl LX (2026-02-08, Seahawks at Patriots). Closing moneyline, spread, and total from 13 sources, including consensus opening and closing lines.
- `data/mlb_2026-08-23_closing_lines.csv` (1,151 rows): one complete MLB day, 34 games, 56 sources, including opening-line snapshots for line-movement analysis.
- `data/prop_closing_lines_sample_50k.csv` (50,000 rows): random sample of player prop closing lines across 43 sources, 23,000+ players, 1,400+ market keys (MLB, NBA, WNBA, NHL, soccer, tennis, table tennis, esports, and more), sampled from a 30M+ row archive collected since 2022.

Columns cover American and decimal odds, spreads, totals, implied probabilities, final scores, and capture timestamps. Full schema tables: https://github.com/JacobiusMakes/sports-odds-datasets

## Load it

```python
import pandas as pd

props = pd.read_csv(
    "hf://datasets/YOUR_HF_USERNAME/sportsbook-closing-lines/data/prop_closing_lines_sample_50k.csv"
)
```

## Use cases

Closing line value (CLV) studies, vig/hold comparison across books, line shopping analysis, model calibration against the close, teaching material.

## Collection method

Exported from the ParlayAPI production archive, which aggregates 45+ sportsbooks and sources across 90+ sports (1.7M+ game closing lines back to 2005, 30M+ prop closes since 2022). Static slices; for live or complete data there is a free API tier (1,000 credits/month, no card): https://parlay-api.com

## License and attribution

CC BY 4.0. Credit "ParlayAPI (parlay-api.com)" with a link.
````

Replace `YOUR_HF_USERNAME` in the load snippet before saving.

## After publishing

- Add the Hub URL to this repo's README.
- The Hub auto-generates a dataset viewer for the CSVs; check that it renders, it is the main discovery surface.

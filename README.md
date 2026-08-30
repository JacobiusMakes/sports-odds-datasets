# Sports Odds Datasets: Sportsbook Closing Lines (Game Lines + Player Props)

Free, permissively licensed sample datasets of real sportsbook odds, exported from the [ParlayAPI](https://parlay-api.com) production archive. Built by the ParlayAPI team.

These files are meant for data scientists, bettors building models, students, and anyone who wants real per-book closing line data without scraping. If you need fresh or complete data, the live API has a free tier (1,000 credits/month, no card required): https://parlay-api.com

## Files

| File | Rows | Size | What it is |
|---|---|---|---|
| `data/superbowl_lx_closing_lines.csv` | 13 | 2 KB | Super Bowl LX (2026-02-08, Seattle Seahawks at New England Patriots). Per-book closing lines for the main markets: moneyline, spread, total. Includes consensus `closing_line` and `opening_line` rows. |
| `data/mlb_2026-08-23_closing_lines.csv` | 1,151 | 158 KB | One full MLB day (2026-08-23, 15 games). Per-book closing lines across 56 sources, including opening-line snapshots (`_open` sources). |
| `data/prop_closing_lines_sample_50k.csv` | 50,000 | 9.4 MB | Random 50,000-row sample of player prop closing lines across 43 sources, 23,000+ players, 1,400+ market keys, spanning 2026-02-08 to 2026-08-25. Sampled from an archive of 30M+ prop closing lines collected since 2022. |

Total: about 9.6 MB. Everything loads with plain `pandas.read_csv`.

## Schema: game closing lines

Applies to `superbowl_lx_closing_lines.csv` and `mlb_2026-08-23_closing_lines.csv`. One row = one (game, source) pair. Empty cells mean that source did not offer, or we did not capture, that market for that game.

| Column | Type | Description |
|---|---|---|
| `game_date` | text (YYYY-MM-DD) | Local calendar date of the game |
| `sport_key` | text | Sport identifier, e.g. `americanfootball_nfl`, `baseball_mlb` |
| `home_team` | text | Home team name |
| `away_team` | text | Away team name |
| `source` | text | Sportsbook or feed slug (see "About the source column" below) |
| `commence_time` | timestamp (UTC) | Scheduled start time |
| `home_ml`, `away_ml`, `draw_ml` | integer | Moneyline in American odds (draw only for sports that have one) |
| `home_price_decimal`, `away_price_decimal`, `draw_price_decimal` | real | Same moneyline prices in decimal odds |
| `home_spread`, `away_spread` | real | Point spread (handicap) for each side |
| `home_spread_ml`, `away_spread_ml` | integer | Spread prices in American odds |
| `home_spread_price_decimal`, `away_spread_price_decimal` | real | Spread prices in decimal odds |
| `total_line` | real | Game total (over/under line) |
| `over_ml`, `under_ml` | integer | Total prices in American odds |
| `over_price_decimal`, `under_price_decimal` | real | Total prices in decimal odds |
| `home_score`, `away_score` | integer | Final score, when the game has settled |
| `result` | text | Settled result, when available |
| `season` | text | Season label, e.g. `2026` |

## Schema: player prop closing lines

Applies to `prop_closing_lines_sample_50k.csv`. One row = one (game, source, player, market) closing snapshot.

| Column | Type | Description |
|---|---|---|
| `game_date` | text (YYYY-MM-DD) | Local calendar date of the game |
| `sport_key` | text | Sport identifier, e.g. `baseball_mlb`, `basketball_nba`, `table_tennis` |
| `home_team`, `away_team` | text | Team or competitor names |
| `commence_time` | text (ISO 8601) | Scheduled start time |
| `source` | text | Sportsbook or feed slug |
| `player_name` | text | Player (or selection label for some derivative markets) |
| `market_key` | text | Machine-readable market, e.g. `player_hits_alt`, `player_points` |
| `market_label` | text | Book-facing market label as displayed by the source |
| `line` | real | The prop line (may be empty for yes/no style markets) |
| `over_price`, `under_price` | integer | Over/under prices in American odds (one side may be empty) |
| `over_implied_prob`, `under_implied_prob` | real | Implied probabilities computed from the prices |
| `snapshot_time` | timestamp (UTC) | When the closing snapshot was captured |

Notes on the prop sample:

- Player names are real, public sports facts and are kept as-is.
- The sample was drawn with block sampling plus per-row randomization, so it skews toward recent months of the archive (2026-02-08 through 2026-08-25). The full archive goes back to 2022.
- A minority of rows are derivative markets carried on the props feed (for example correct score or winning margin), where `player_name` holds the selection label rather than an athlete.

## Known quirks (real-world data)

- Team names are as each source publishes them, so the same team can appear under variants across sources (for example `Los Angeles Dodgers` vs `LA Dodgers`, or `Athletics` vs `The Athletics`). Normalize on team name before cross-book joins, or join on (game_date, commence_time) plus fuzzy team matching.
- Some international books quote extreme longshot prices (five-figure American odds). Filter outliers if you are averaging across books.
- Not every source offers every market for every game; expect empty cells.

## About the `source` column

- Plain slugs (`fanduel`, `draftkings`, `pinnacle`, `bet365`, ...) are individual sportsbooks.
- A `_open` suffix (for example `fanduel_open`) is that book's opening-line snapshot rather than its close.
- An `_an` suffix is an alternate data feed for the same book.
- `closing_line` and `opening_line` are consensus pseudo-sources, useful as a single reference line per game.

## Odds format cheat sheet

- American odds: negative means favorite (-110 = risk 110 to win 100), positive means underdog (+150 = risk 100 to win 150).
- Decimal odds: total payout per unit staked (1.9091 decimal = -110 American).
- Implied probability from American odds: for negative odds, |odds| / (|odds| + 100); for positive odds, 100 / (odds + 100). The over/under implied prob columns in the props file are computed this way and are not de-vigged.

## Collection method

Exported from the ParlayAPI production archive. ParlayAPI aggregates real-time odds from 30+ sportsbooks plus additional data sources across 90+ sport keys, and archives closing lines continuously: 1.7M+ historical game closing lines going back to 2005 and 30M+ prop closing lines since 2022. These CSVs are small, static slices of that archive.

## Getting fresh or complete data

These files will not update in real time. For live odds, full history, or bigger exports:

- Live API: https://parlay-api.com (free tier: 1,000 credits/month, no card)
- Docs: https://parlay-api.com/docs
- OpenAPI spec: https://parlay-api.com/openapi.json (agent-optimized: https://parlay-api.com/openapi-agent.json)
- Keyless sandbox endpoints for trying it out: `https://parlay-api.com/v1/sandbox/*`
- Python SDK: `pip install parlay-api`
- MCP server for AI agents: `pip install parlayapi-mcp`

## Quick start

```bash
python load_example.py
```

See `load_example.py` for a small pandas walkthrough: loading each file, finding the best available price per game across books, and comparing a book's close to the consensus closing line.

## Update cadence

Occasional. Watch or star the repo if you want to catch new slices when they land.

## License and attribution

Data and documentation are released under [CC BY 4.0](LICENSE). You can use this commercially, remix it, and redistribute it. Attribution requirement: credit "ParlayAPI (parlay-api.com)" with a link.

Suggested citation:

```
ParlayAPI Sports Odds Datasets, exported from the ParlayAPI production archive.
https://github.com/JacobiusMakes/sports-odds-datasets (CC BY 4.0, parlay-api.com)
```

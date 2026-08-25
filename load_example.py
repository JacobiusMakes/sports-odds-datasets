"""Small walkthrough of the sports-odds-datasets CSVs.

Run from the repo root:

    python load_example.py

Requires pandas (pip install pandas). Data license: CC BY 4.0,
attribution to ParlayAPI (parlay-api.com). For live or complete data,
the API has a free tier: https://parlay-api.com
"""

import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    sys.exit("This example needs pandas: pip install pandas")

DATA = Path(__file__).parent / "data"


def american_to_prob(odds):
    """Implied probability from American odds (not de-vigged)."""
    if pd.isna(odds):
        return float("nan")
    odds = float(odds)
    if odds < 0:
        return -odds / (-odds + 100.0)
    return 100.0 / (odds + 100.0)


def main():
    # 1) Super Bowl LX: every book's closing line for the big game
    sb = pd.read_csv(DATA / "superbowl_lx_closing_lines.csv")
    print("=== Super Bowl LX (2026-02-08) closing lines ===")
    cols = ["source", "home_ml", "away_ml", "home_spread", "total_line"]
    print(sb[cols].to_string(index=False))

    consensus = sb[sb["source"] == "closing_line"]
    if not consensus.empty:
        row = consensus.iloc[0]
        print(
            f"\nConsensus close: {row['home_team']} {row['home_ml']} / "
            f"{row['away_team']} {row['away_ml']}, "
            f"spread {row['home_spread']}, total {row['total_line']}"
        )

    # 2) MLB day: best available moneyline per game across books
    mlb = pd.read_csv(DATA / "mlb_2026-08-23_closing_lines.csv")
    books = mlb[~mlb["source"].str.endswith("_open")]
    print("\n=== MLB 2026-08-23: best home moneyline per game (line shopping) ===")
    best = (
        books.dropna(subset=["home_ml"])
        .sort_values("home_ml", ascending=False)
        .groupby(["home_team", "away_team"], as_index=False)
        .first()[["away_team", "home_team", "source", "home_ml"]]
    )
    print(best.head(10).to_string(index=False))
    print(f"({len(best)} games, {books['source'].nunique()} books)")

    # 3) Player props sample: what is in it, plus implied hold per market
    props = pd.read_csv(DATA / "prop_closing_lines_sample_50k.csv")
    print("\n=== Prop closing lines sample ===")
    print(
        f"{len(props):,} rows, {props['source'].nunique()} sources, "
        f"{props['player_name'].nunique():,} players, "
        f"{props['market_key'].nunique():,} market keys"
    )
    print("\nTop sports:")
    print(props["sport_key"].value_counts().head(8).to_string())

    two_sided = props.dropna(subset=["over_price", "under_price"]).copy()
    two_sided["hold"] = (
        two_sided["over_price"].map(american_to_prob)
        + two_sided["under_price"].map(american_to_prob)
        - 1.0
    )
    print("\nMedian implied hold (vig) on two-sided props, by book (top 10 by volume):")
    top_books = two_sided["source"].value_counts().head(10).index
    hold = (
        two_sided[two_sided["source"].isin(top_books)]
        .groupby("source")["hold"]
        .median()
        .sort_values()
    )
    print((hold * 100).round(2).astype(str).add("%").to_string())


if __name__ == "__main__":
    main()

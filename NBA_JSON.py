import pandas as pd
import time
from datetime import datetime
import requests

FILE_PATH      = "Capper Tracking.xlsx"
SHEET_NAME     = "DanGambleAiEdge"

SCOREBOARD_URL = "https://stats.nba.com/stats/scoreboardv2"
BOXSCORE_URL   = "https://stats.nba.com/stats/boxscoretraditionalv2"

HEADERS = {
    "Host":               "stats.nba.com",
    "Connection":         "keep-alive",
    "Accept":             "application/json, text/plain, */*",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token":  "true",
    "User-Agent":         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Referer":            "https://www.nba.com/",
    "Accept-Language":    "en-US,en;q=0.9",
}

STAT_FIELD = {
    "points":   "PTS",
    "assists":  "AST",
    "rebounds": "REB",
}

df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)
schedule_cache = {}
boxscore_cache = {}

def get_games_on(date_obj):
    """Return all NBA game IDs for a given date."""
    key = date_obj.strftime("%Y-%m-%d")
    if key in schedule_cache:
        return schedule_cache[key]

    params = {
        "GameDate": date_obj.strftime("%m/%d/%Y"),
        "LeagueID": "00",
        "DayOffset": 0
    }
    res = requests.get(SCOREBOARD_URL, headers=HEADERS, params=params, timeout=10)
    res.raise_for_status()
    data = res.json()["resultSets"][0]
    hdrs = data["headers"]
    rows = data["rowSet"]
    gid_i = hdrs.index("GAME_ID")
    game_ids = [row[gid_i] for row in rows]
    schedule_cache[key] = game_ids
    return game_ids

def get_boxscore(game_id):
    """Return a dict of player_name_lower → {PTS,AST,REB} for that game."""
    if game_id in boxscore_cache:
        return boxscore_cache[game_id]

    params = {"GameID": game_id, "LeagueID": "00"}
    res = requests.get(BOXSCORE_URL, headers=HEADERS, params=params, timeout=10)
    res.raise_for_status()
    data = res.json()["resultSets"][0]
    hdrs = data["headers"]
    rows = data["rowSet"]

    name_i = hdrs.index("PLAYER_NAME")
    stat_indices = {stat: hdrs.index(field) for stat, field in STAT_FIELD.items()}

    by_player = {}
    for row in rows:
        nm = row[name_i].strip().lower()
        by_player[nm] = { stat: row[idx] for stat, idx in stat_indices.items() }
    boxscore_cache[game_id] = by_player
    return by_player

for idx, row in df.iterrows():
    date_obj   = pd.to_datetime(row["date"])
    player_key = row["player_name"].strip().lower()
    stat_type  = row["stat_type"].strip().lower()

    field = STAT_FIELD.get(stat_type)
    if not field:
        print(f"Skipping {row['player_name']}: unsupported stat '{row['stat_type']}'")
        continue

    actual = None
    for gid in get_games_on(date_obj):
        players = get_boxscore(gid)
        if player_key in players:
            actual = players[player_key].get(stat_type)
            break

    if actual is not None:
        df.at[idx, "actual_statistic"] = actual
        print(f"{row['player_name']} on {date_obj.date()} → actual_statistic = {actual}")
    else:
        print(f"No stat found for {row['player_name']} on {date_obj.date()}")

    time.sleep(1)

df.to_excel(FILE_PATH, sheet_name=SHEET_NAME, index=False)
print("Done")

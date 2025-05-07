import requests

def fetch_goalserve_team_stats(API_KEY, DATE, TEAM_NAME):
    """
    Fetch and print hitter and pitcher stats from Goalserve MLB data for a given team and date.
    
    Parameters:
    - API_KEY (str): Your Goalserve API key
    - DATE (str): Date in format "dd.MM.yyyy"
    - TEAM_NAME (str): Substring of the team name (case-insensitive), e.g., "angels"
    """

    url = f"http://www.goalserve.com/getfeed/{API_KEY}/baseball/usa?date={DATE}&json=1"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Request failed with status code {response.status_code}")
        return

    data = response.json()
    matches = data.get("scores", {}).get("category", {}).get("match", [])
    found = False

    def to_float(val):
        try:
            return float(val)
        except:
            return None

    for match in matches:
        home = match.get("hometeam", {}).get("name", "").lower()
        away = match.get("awayteam", {}).get("name", "").lower()

        if TEAM_NAME.lower() in home or TEAM_NAME.lower() in away:
            print(f"\n✅ Found {TEAM_NAME.title()} game: {match['awayteam']['name']} at {match['hometeam']['name']}")

            team_side = "hometeam" if TEAM_NAME.lower() in home else "awayteam"
            opponent_side = "awayteam" if team_side == "hometeam" else "hometeam"
            team_name = match[team_side]["name"]
            opponent_name = match[opponent_side]["name"]

            hitters = match.get("stats", {}).get("hitters", {}).get(team_side, {}).get("player", [])
            pitchers = match.get("stats", {}).get("pitchers", {}).get(team_side, {}).get("player", [])

            if hitters:
                print(f"\n📋 Batting Stats for {team_name}:")
                for p in hitters:
                    player_stats = {
                        "player_name": p.get("name"),
                        "game_date": DATE,
                        "isHitter": 1,
                        "isPitcher": 0,
                        "team": team_name,
                        "opponent": opponent_name,
                        "hits": to_float(p.get("hits")),
                        "singles": None,  # Not provided
                        "doubles": to_float(p.get("doubles")),
                        "triples": to_float(p.get("triples")),
                        "runs": to_float(p.get("runs")),
                        "rbi": to_float(p.get("runs_batted_in")),
                        "home_runs": to_float(p.get("home_runs")),
                        "walks_hitter": to_float(p.get("walks")),
                        "hit_by_pitch_hitter": to_float(p.get("hit_by_pitch")),
                        "at_bats_hitter": to_float(p.get("at_bats")),
                        "strikeouts_hitter": to_float(p.get("strikeouts")),
                        "total_bases": to_float(p.get("total_bases")),
                        "stolen_bases": to_float(p.get("stolen_bases")),
                        "fantasy_points_hitter": None
                    }
                    print(player_stats)
            else:
                print("⚠️ No hitter stats found for this team.")

            if pitchers:
                print(f"\n⚾ Pitching Stats for {team_name}:")
                for p in pitchers:
                    ip = p.get("innings_pitched", "0")
                    outs = 0
                    if "." in ip:
                        whole, frac = ip.split(".")
                        outs = int(whole) * 3 + int(frac)
                    else:
                        outs = int(ip) * 3

                    pc_st = p.get("pc-st", "0-0").split("-")[0]
                    player_stats = {
                        "player_name": p.get("name"),
                        "game_date": DATE,
                        "isHitter": 0,
                        "isPitcher": 1,
                        "team": team_name,
                        "opponent": opponent_name,
                        "earned_runs": to_float(p.get("earned_runs")),
                        "total_pitches": int(pc_st),
                        "strikeouts_pitcher": to_float(p.get("strikeouts")),
                        "outs_pitched": outs,
                        "hits_allowed": to_float(p.get("hits")),
                        "hit_by_pitch_pitcher": to_float(p.get("hbp")),
                        "win_credited": 1.0 if p.get("win") else 0.0,
                        "quality_start": 1.0 if outs >= 18 and to_float(p.get("earned_runs")) <= 3 else 0.0
                    }
                    print(player_stats)
            else:
                print("⚠️ No pitcher stats found for this team.")

            found = True
            break

    if not found:
        print(f"❌ No game found for {TEAM_NAME.title()} on {DATE}.")


import requests
import xml.etree.ElementTree as ET

def fetch_nba_box_score_xml(api_key, date_str, team_name):
    url = f"http://www.goalserve.com/getfeed/{api_key}/bsktbl/nba-scores?date={date_str}"
    response = requests.get(url)

    print(f"📡 Status: {response.status_code}")
    if response.status_code != 200:
        print("❌ Failed to fetch data.")
        return

    # Parse XML
    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as e:
        print(f"❌ XML parse error: {e}")
        return

    matches = root.findall(".//match")
    print(f"📆 Found {len(matches)} games on {date_str}")

    for match in matches:
        home = match.find("hometeam").attrib.get("name", "")
        away = match.find("awayteam").attrib.get("name", "")
        print(f"📝 Game: {away} at {home}")

        if team_name.lower() in home.lower():
            side = "hometeam"
        elif team_name.lower() in away.lower():
            side = "awayteam"
        else:
            continue  # not the team we’re looking for

        print(f"🎯 Found game involving {team_name}: {away} at {home}")
        players_path = f".//player_stats/{side}"
        players = match.find(players_path)

        if players is None:
            print("⚠️ No player stats found.")
            return

        print("\n📊 Player Stats:")
        for group in ["starters", "bench"]:
            for player in players.find(group):
                print({
                    "name": player.attrib.get("name"),
                    "minutes": player.attrib.get("minutes"),
                    "points": player.attrib.get("points"),
                    "rebounds": player.attrib.get("total_rebounds"),
                    "assists": player.attrib.get("assists"),
                    "steals": player.attrib.get("steals"),
                    "blocks": player.attrib.get("blocks"),
                    "turnovers": player.attrib.get("turnovers"),
                })
        return  # done after first matching game

    print("❌ No matching team found.")

# Example usage
fetch_nba_box_score_xml("b6cccb2cee43489fcb7908dd8718f057", "30.04.2025", "Lakers")



# fetch_goalserve_team_stats("b6cccb2cee43489fcb7908dd8718f057", "30.04.2025", "angels")

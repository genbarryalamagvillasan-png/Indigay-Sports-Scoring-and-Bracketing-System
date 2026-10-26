import os

sports_data = {
    "Basketball": {
        "teams": [],
        "games": [],
        "scores": {},
        "bracket": {},
        "rankings": []
    },
    "Volleyball - Men's": {
        "teams": [],
        "games": [],
        "scores": {},
        "bracket": {},
        "rankings": []
    },
    "Volleyball - Women's": {
        "teams": [],
        "games": [],
        "scores": {},
        "bracket": {},
        "rankings": []
    },
    "Badminton - Men's": {
        "teams": [],
        "games": [],
        "scores": {},
        "bracket": {},
        "rankings": []
    },
    "Badminton - Women's": {
        "teams": [],
        "games": [],
        "scores": {},
        "bracket": {},
        "rankings": []
    },

    "Table Tennis - Men's": {
        "teams": [],
        "games": [],
        "scores": {},
        "bracket": {},
        "rankings": []
    },
    "Table Tennis - Women's": {
        "teams": [],
        "games": [],
        "scores": {},
        "bracket": {},
        "rankings": []
    },

    "Pickleball - Men's": {
        "teams": [],
        "games": [],
        "scores": {},
        "bracket": {},
        "rankings": []
    },
    "Pickleball - Women's": {
        "teams": [],
        "games": [],
        "scores": {},
        "bracket": {},
        "rankings": []
    },
    "Pickleball - Mixed": {
        "teams": [],
        "games": [],
        "scores": {},
        "bracket": {},
        "rankings": []
    },

    "Soccer": {
        "teams": [],
        "games": [],
        "scores": {},
        "bracket": {},
        "rankings": []
    },
    "Frisbee": {
        "teams": [],
        "games": [],
        "scores": {},
        "bracket": {},
        "rankings": []
    }
}

SET_SPORTS = [
    "Volleyball - Men's",
    "Volleyball - Women's",
    "Badminton - Men's",
    "Badminton - Women's",
    "Table Tennis - Men's",
    "Table Tennis - Women's",
    "Pickleball - Men's",
    "Pickleball - Women's",
    "Pickleball - Mixed"
]

for data in sports_data.values():
    data["captains"] = {}
    data["players"] = {}
    data["ready"] = []


currentfolder = os.path.dirname(os.path.abspath(__file__))
projectfolder = os.path.dirname(currentfolder)

database = os.path.join(projectfolder, "data")
filename = os.path.join(database, "tournament.txt")


def convert(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def savesource(source):
    if not source:
        return ""

    return f"{source[0]}:{source[1]}"


def loadsource(value):
    if not value or ":" not in value:
        return None

    result, number = value.split(":", 1)

    return (result, convert(number))


def getgameteam(data, game, slot, seen=None):

    if not game:
        return "Waiting"

    team = game.get(slot)

    if team and str(team).strip() not in (
        "TBD", "Waiting", "None", ""
    ):
        return str(team).strip()

    source = game.get(slot + "_source")

    if not source:
        return "Waiting"

    if seen is None:
        seen = set()

    marker = (game.get("game"), slot)

    if marker in seen:
        return "Waiting"

    seen.add(marker)

    result, game_number = source

    previous = next(
        (
            item for item in data.get("games", [])
            if item.get("game") == game_number
        ),
        None
    )

    prefix = "W" if result == "winner" else "L"
    source_label = f"{prefix}{game_number}"

    if not previous:
        return source_label

    if previous.get("status") != "Completed":
        return source_label

    qualified_team = previous.get(result)

    if qualified_team and str(qualified_team).strip() not in (
        "TBD", "Waiting", "None", ""
    ):
        return str(qualified_team).strip()

    return "Waiting"


def get_current_game(sport):
    data = sports_data[sport]

    for game in data["games"]:
        if game.get("status") == "Completed":
            continue

        team1 = getgameteam(data, game, "team1")
        team2 = getgameteam(data, game, "team2")

        if team1 in data["teams"] and team2 in data["teams"]:
            return game

    return None


def is_all_done(sport):
    games = sports_data[sport]["games"]

    if len(games) == 0:
        return False

    game12done = False
    for game in games:
        if game.get("game") == 12 and game.get("status") == "Completed":
            game12done = True

    for game in games:
        if game.get("status") == "Completed":
            continue

        if game.get("game") == 13 and game12done and game.get("status") == "Waiting":
            continue

        return False

    return True


def is_all_ready(sport):
    data = sports_data[sport]

    if len(data["teams"]) != 7:
        return False

    for team in data["teams"]:
        if team not in data["ready"]:
            return False

    return True


def makegames(sport):
    data = sports_data[sport]
    teams = data["teams"]

    games = [
        {"game": 1, "team1": teams[0], "team2": teams[1]},
        {"game": 2, "team1": teams[2], "team2": teams[3]},
        {"game": 3, "team1": teams[4], "team2": teams[5]},
        {"game": 4, "team1": None, "team2": None},
        {"game": 5, "team1": None, "team2": teams[6]},
        {"game": 6, "team1": None, "team2": None},
        {"game": 7, "team1": None, "team2": None},
        {"game": 8, "team1": None, "team2": None},
        {"game": 9, "team1": None, "team2": None},
        {"game": 10, "team1": None, "team2": None},
        {"game": 11, "team1": None, "team2": None},
        {"game": 12, "team1": None, "team2": None},
        {"game": 13, "team1": None, "team2": None}
    ]

    for game in games:
        game["score1"] = 0
        game["score2"] = 0
        game["winner"] = None
        game["loser"] = None
        game["status"] = "Waiting"
        game["team1_source"] = None
        game["team2_source"] = None

    source = {
        4: {"team1_source": ("winner", 1), "team2_source": ("winner", 2)},
        5: {"team1_source": ("winner", 3)},
        6: {"team1_source": ("loser", 1), "team2_source": ("loser", 2)},
        7: {"team1_source": ("loser", 3), "team2_source": ("loser", 4)},
        8: {"team1_source": ("winner", 6), "team2_source": ("loser", 5)},
        9: {"team1_source": ("winner", 4), "team2_source": ("winner", 5)},
        10: {"team1_source": ("winner", 7), "team2_source": ("winner", 8)},
        11: {"team1_source": ("winner", 10), "team2_source": ("loser", 9)},
        12: {"team1_source": ("winner", 11), "team2_source": ("winner", 9)}
    }

    for game in games:
        game.update(source.get(game["game"], {}))

    data["games"] = games
    data["scores"] = {}
    data["bracket"] = {"bye": teams[6], "winners": {}, "losers": {}}
    data["rankings"] = []

    savetournament()


def get_match_text(sport):
    if is_all_done(sport):
        return "All matches are done"

    current_game = get_current_game(sport)

    if current_game is None:
        return "No current match"

    data = sports_data[sport]
    team1 = getgameteam(data, current_game, "team1")
    team2 = getgameteam(data, current_game, "team2")

    return "Current Match\nGame " + str(current_game["game"]) + ": " + team1 + " VS " + team2


def savetournament():
    os.makedirs(database, exist_ok=True)

    with open(filename, "w", encoding="utf-8") as file:
        for sport, data in sports_data.items():
            file.write(f"SPORT|{sport}\n")

            for team in data["teams"]:
                file.write(f"TEAM|{team}\n")

            for team, captain in data["captains"].items():
                file.write(f"CAPTAIN|{team}|{captain}\n")

            for team, players in data["players"].items():
                for player in players:
                    file.write(f"PLAYER|{team}|{player}\n")

            for team in data["ready"]:
                file.write(f"READY|{team}\n")

            for score, value in data["scores"].items():
                file.write(f"SCORE|{score}|{value}\n")

            for bracket, value in data["bracket"].items():
                file.write(f"BRACKET|{bracket}|{value}\n")

            for ranking in data["rankings"]:
                file.write(f"RANKING|{ranking}\n")

            for game in data["games"]:
                file.write(
                    f"GAME|"
                    f"{game.get('game', '')}|"
                    f"{game.get('team1') or ''}|"
                    f"{game.get('team2') or ''}|"
                    f"{game.get('score1', 0)}|"
                    f"{game.get('score2', 0)}|"
                    f"{game.get('winner') or ''}|"
                    f"{game.get('loser') or ''}|"
                    f"{game.get('status', 'Waiting')}|"
                    f"{savesource(game.get('team1_source'))}|"
                    f"{savesource(game.get('team2_source'))}|"
                    f"{game.get('sets_won1', 0)}|"
                    f"{game.get('sets_won2', 0)}\n"
                )

                for i, item in enumerate(
                    game.get("sets", []), start=1
                ):
                    file.write(
                        f"SET|{game.get('game', '')}|"
                        f"{i}|"
                        f"{item.get('score1', 0)}|"
                        f"{item.get('score2', 0)}|"
                        f"{item.get('winner') or ''}\n"
                    )

            file.write("End\n")


def loadtournament():
    if not os.path.exists(filename):
        savetournament()
        return

    for data in sports_data.values():
        data["teams"] = []
        data["games"] = []
        data["scores"] = {}
        data["bracket"] = {}
        data["rankings"] = []
        data["captains"] = {}
        data["players"] = {}
        data["ready"] = []

    currentsport = None

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.rstrip("\n")

            if not line:
                continue

            parts = line.split("|")
            recordtype = parts[0]

            if recordtype == "SPORT" and len(parts) >= 2:
                currentsport = parts[1]

                if currentsport not in sports_data:
                    currentsport = None

                continue

            if currentsport is None:
                continue

            if recordtype == "TEAM" and len(parts) >= 2:
                sports_data[currentsport]["teams"].append(parts[1])

            elif recordtype == "CAPTAIN" and len(parts) >= 3:
                team = parts[1]
                sports_data[currentsport]["captains"][team] = parts[2]

            elif recordtype == "PLAYER" and len(parts) >= 3:
                team = parts[1]
                players = sports_data[currentsport]["players"]

                if team not in players:
                    players[team] = []

                players[team].append(parts[2])

            elif recordtype == "READY" and len(parts) >= 2:
                sports_data[currentsport]["ready"].append(parts[1])

            elif recordtype == "SCORE" and len(parts) >= 3:
                key = parts[1]
                value = convert(parts[2])

                sports_data[currentsport]["scores"][key] = value

            elif recordtype == "BRACKET" and len(parts) >= 3:
                key = parts[1]
                value = "|".join(parts[2:])

                sports_data[currentsport]["bracket"][key] = value

            elif recordtype == "RANKING" and len(parts) >= 2:
                value = "|".join(parts[1:])

                sports_data[currentsport]["rankings"].append(value)

            elif recordtype == "GAME" and len(parts) >= 9:
                game = {
                    "game": convert(parts[1]),
                    "team1": parts[2] or None,
                    "team2": parts[3] or None,
                    "score1": convert(parts[4]),
                    "score2": convert(parts[5]),
                    "winner": parts[6] or None,
                    "loser": parts[7] or None,
                    "status": parts[8],

                    "team1_source": (
                        loadsource(parts[9])
                        if len(parts) > 9 else None
                    ),

                    "team2_source": (
                        loadsource(parts[10])
                        if len(parts) > 10 else None
                    ),

                    "sets_won1": (
                        convert(parts[11])
                        if len(parts) > 11 else 0
                    ),

                    "sets_won2": (
                        convert(parts[12])
                        if len(parts) > 12 else 0
                    ),

                    "sets": []
                }

                sports_data[currentsport]["games"].append(game)

            elif recordtype == "SET" and len(parts) >= 6:
                game_number = convert(parts[1])
                set_number = convert(parts[2])

                for game in sports_data[currentsport]["games"]:
                    if game["game"] == game_number:
                        sets = game["sets"]

                        while len(sets) < set_number:
                            sets.append({
                                "score1": 0,
                                "score2": 0,
                                "winner": None
                            })

                        sets[set_number - 1] = {
                            "score1": convert(parts[3]),
                            "score2": convert(parts[4]),
                            "winner": parts[5] or None
                        }

                        break

    if os.path.getsize(filename) == 0:
        savetournament()

loadtournament()

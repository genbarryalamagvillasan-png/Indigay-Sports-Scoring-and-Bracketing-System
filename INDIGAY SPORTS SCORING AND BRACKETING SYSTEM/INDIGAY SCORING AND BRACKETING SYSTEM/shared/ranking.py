def updaterankings(data, completedgame):
    rankings = data.setdefault("rankings", [])
    games = data.get("games", [])

    def rankedteam(team):
        for entry in rankings:
            part = entry.split("|", 1)
            if len(part) == 2 and part[1] == team:
                return True

        return False

    losses = {}
    for item in games:
        if item.get("status") != "Completed" or not item.get("loser"):
            continue
        loser = item["loser"]
        losses[loser] = losses.get(loser, 0) + 1

    elimination = ["6th", "5th", "4th", "3rd", "2nd"]
    alreadyeliminated = sum(1 for entry in rankings if entry.split("|", 1)[0] in elimination)

    loser = completedgame.get("loser")
    gamenumber = completedgame.get("game")

    final = (
        gamenumber == 13 or (gamenumber == 12 and completedgame.get("winner") == champ(data, 9))
    )

    if(loser and losses.get(loser, 0) >= 2 and not rankedteam(loser) and not (final and gamenumber in (12, 13))):
        if alreadyeliminated < len(elimination):
            rankings.append(f"{elimination[alreadyeliminated]}|{loser}")

    if final and completedgame.get("winner"):
        champion = completedgame.get("winner")
        first = completedgame.get("loser")
        rankings[:] = [entry for entry in rankings
                       if entry.split("|", 1)[0] not in ("CHAMPION", "1st")
                       ]
        if first:
            rankings.append(f"1st|{first}")
        if champion:
            rankings.append(f"CHAMPION|{champion}")

def champ(data, gamenumber):
    for i in data.get("games", []):
        if i.get("game") == gamenumber:
            return i.get("winner")

    return None

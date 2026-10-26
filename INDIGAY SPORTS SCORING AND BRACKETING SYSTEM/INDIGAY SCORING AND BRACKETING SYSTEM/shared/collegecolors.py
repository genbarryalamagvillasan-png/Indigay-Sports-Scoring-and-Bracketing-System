import customtkinter as ctk

COLLEGE_COLORS = {
    "CCS": "#008080",
    "CON": "#f8bbd0",
    "COE": "#4f1414",
    "CHTM": "#f700ff",
    "CED": "#1980c2",
    "COC": "#3d0056",
    "CAS": "#345b2f",
    "CBAA": "#ffff00",
    "SHS": "#ffa600",
    "JHS": "#00008b",
}


def getcollegecolor(college):
    if college in COLLEGE_COLORS:
        return COLLEGE_COLORS[college]

    return "#f5f5f7"


def getteamparts(team):
    parts = []
    colleges = team.split(" x ")

    for i, college in enumerate(colleges):
        if i > 0:
            parts.append((" x ", "#f5f5f7"))
        parts.append((college, getcollegecolor(college)))

    return parts


def teamlabel(parent, team, font):
    frame = ctk.CTkFrame(parent, fg_color="transparent")

    for text, color in getteamparts(team):
        ctk.CTkLabel(frame, text=text, font=font, text_color=color).pack(side="left")

    return frame


def drawteam(canvas, x, y, team, font, anchor="center"):
    if team == "":
        return

    if anchor == "s":
        partanchor = "sw"
    else:
        partanchor = "w"

    ids = []
    nextx = x
    for text, color in getteamparts(team):
        textid = canvas.create_text(nextx, y, text=text, fill=color, font=font, anchor=partanchor)
        ids.append(textid)
        nextx = canvas.bbox(textid)[2]

    if anchor == "center" or anchor == "s":
        halfwidth = (nextx - x) / 2
        for textid in ids:
            canvas.move(textid, -halfwidth, 0)

import os
import customtkinter as ctk
from PIL import Image
from shared.tournamentdata import sports_data, loadtournament, getgameteam
from shared.collegecolors import teamlabel
from admindash.teams import Teams
from admindash.games import Games
from admindash.scoring import Scoring
from admindash.bracket import Bracket
from admindash.rankings import Rankings

class AdminDashboard(ctk.CTkFrame):
  def __init__(self, master, sport, backtosport):
    super().__init__(master, fg_color="#191a20")

    self.sport = sport
    self.backtosport = backtosport

    self.side = ctk.CTkFrame(self, width=200, fg_color="#202127", corner_radius=0)
    self.side.pack(side="left", fill="y")
    self.side.pack_propagate(False)

    self.con = ctk.CTkFrame(self, fg_color="#191a20", corner_radius=0)
    self.con.pack(side="left", fill="both", expand=True)

    self.createside()
    self.showdashboard()

  def createside(self):
    projectfolder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logopath = os.path.join(projectfolder, "images", "logo.png")

    if os.path.exists(logopath):
      logo = Image.open(logopath)
      self.logo = ctk.CTkImage(light_image=logo, dark_image=logo, size=(170, int(170 * logo.height / logo.width)))
      ctk.CTkLabel(self.side, image=self.logo, text="").pack(pady=(25,15))
    ctk.CTkLabel(self.side, text="Scoring and Bracketing System", font=("arial", 12, "bold"), text_color="#858791").pack(pady=(0, 35))

    self.dashbutton =  self.sidebutton("Dashboard", self.showdashboard)
    self.teambutton = self.sidebutton("Manage Teams", self.showteams)
    self.gamebutton = self.sidebutton("Manage Games", self.showgames)
    self.scorebutton = self.sidebutton("Scoring", self.showscore)
    self.bracketbutton = self.sidebutton("Bracket", self.showbracket)
    self.rankingbutton = self.sidebutton("Ranking", self.showrankings)

    ctk.CTkButton(self.side, text="Back to Sports", font=("arial", 13, "bold"), height=40, fg_color="#303139", hover_color="#41434d", text_color="white", command=self.returntosport).pack(side="bottom", fill="x", padx=12, pady=20)

  def sidebutton(self, text, command):
    button = ctk.CTkButton(self.side, text=text, height=42, anchor="w", font=("arial", 13), fg_color="transparent", hover_color="#343640", text_color="#c7c8d0", command=command)
    button.pack(fill="x", padx=10, pady=4)

    return button

  def activebutton(self, button):
    buttons=[self.dashbutton, self.teambutton, self.gamebutton, self.scorebutton, self.bracketbutton, self.rankingbutton]

    for b in buttons:
      b.configure(fg_color="transparent")

    button.configure(fg_color="#6b6b6a", text_color="white")
    self.actbut = button

  def showpage(self, title):
    for widget in self.con.winfo_children():
      widget.destroy()

    loadtournament()

    ctk.CTkLabel(self.con, text=title, font=("arial", 27, "bold"), text_color="#f5f5f7").pack(anchor="w", padx=28, pady=(25,0))

  def showdashboard(self):
    self.activebutton(self.dashbutton)
    self.showpage("ADMIN DASHBOARD")

    data = sports_data[self.sport]

    c = ctk.CTkFrame(self.con, fg_color="transparent")
    c.pack(fill="x", padx=15, pady=5)
    c.grid_columnconfigure((0,1), weight=1)

    self.cardss(c, "Registered Teams", str(len(data["teams"])), 0, 0)
    self.cardss(c, "Total Games", str(len(data["games"])), 0, 1)
    self.cardss(c, "Tournament Format", "Double Elimination", 1, 0)
    self.cardss(c, "Selected Sport", self.sport, 1, 1)

    p = ctk.CTkFrame(self.con, fg_color="transparent")
    p.pack(fill="both", expand=True, padx=22, pady=15)
    p.grid_columnconfigure((0,1), weight=1)
    p.grid_rowconfigure(0, weight=1)

    g = ctk.CTkFrame(p, fg_color="#23242b", corner_radius=10, border_color="#303139", border_width=1)
    g.grid(row=0, column=0, sticky="nsew", padx=(0,8), pady=5)

    e = ctk.CTkFrame(p, fg_color="#23242b", corner_radius=10, border_color="#303139", border_width=1)
    e.grid(row=0, column=1, sticky="nsew", padx=(8,0), pady=5)

    ctk.CTkLabel(g, text="All Games", font=("arial", 18, "bold"), text_color="#f5f5f7").pack(anchor="w", padx=15, pady=15)

    if len(data["games"]) == 0:
      ctk.CTkLabel(g, text="No games have been added yet!", text_color="#a0a1aa").pack(anchor="w", padx=15, pady=5)
    else:
      gamelist = ctk.CTkScrollableFrame(g, fg_color="transparent")
      gamelist.pack(fill="both", expand=True, padx=5, pady=(0,10))

      for game in data["games"]:
        self.gamerow(gamelist, data, game)

    ctk.CTkLabel(e, text="Tournament Overview", font=("arial", 18, "bold"), text_color="#f5f5f7").pack(anchor="w", padx=15, pady=15)
    self.ol(e, "Sport", self.sport)
    self.ol(e, "Tournament", "Double Elimination")
    self.ol(e, "Registered Teams", str(len(data["teams"])))
    self.ol(e, "Total Games", str(len(data["games"])))
    ctk.CTkLabel(e, text="Manage your teams, games, scores, and brackets using the sidebar.", wraplength=250, justify="left", text_color="#a0a1aa").pack(anchor="w", padx=15, pady=5)

  def gamerow(self, parent, data, game):
    team1 = getgameteam(data, game, "team1")
    team2 = getgameteam(data, game, "team2")

    if game.get("status") == "Completed" and game.get("winner"):
      status = "Completed"
      statuscolor = "#62d98b"
    elif game.get("status") == "In Progress":
      status = "In Progress"
      statuscolor = "#ffa600"
    else:
      status = "Waiting"
      statuscolor = "#a0a1aa"

    row = ctk.CTkFrame(parent, fg_color="#292a31", corner_radius=8)
    row.pack(fill="x", padx=5, pady=4)

    ctk.CTkLabel(row, text="Game " + str(game["game"]), width=70, anchor="w", font=("arial", 12, "bold"), text_color="#a0a1aa").pack(side="left", padx=(12,5), pady=8)
    teamlabel(row, team1, ("arial", 12, "bold")).pack(side="left")
    ctk.CTkLabel(row, text="  VS.  ", font=("arial", 12, "bold"), text_color="#a0a1aa").pack(side="left")
    teamlabel(row, team2, ("arial", 12, "bold")).pack(side="left")
    ctk.CTkLabel(row, text=status, font=("arial", 11, "bold"), text_color=statuscolor).pack(side="right", padx=12)

  def cardss(self, parent, title, value, row, column):
    card = ctk.CTkFrame(parent, fg_color="#23242b", corner_radius=8, height=110, border_color="#303139", border_width=1)
    card.grid(row=row, column=column, sticky="ew", padx=7, pady=7)
    card.grid_propagate(False)

    ctk.CTkLabel(card, text=title, font=("arial", 11, "bold"), text_color="#a0a1aa").pack(anchor="w", padx=17, pady=(17,5))
    ctk.CTkLabel(card, text=value, font=("arial", 21, "bold"), text_color="#f5f5f7", wraplength=300).pack(anchor="w", padx=17, pady=(0,12))

  def ol(self, parent, title, value):
    r = ctk.CTkFrame(parent, fg_color="transparent")
    r.pack(fill="x", padx=18, pady=6)

    ctk.CTkLabel(r, text=title, font=("arial", 12), text_color="#a0a1aa").pack(side="left")
    ctk.CTkLabel(r, text=value, font=("arial", 12, "bold"), text_color="#f5f5f7", wraplength=180).pack(side="right")


  def showteams(self):
    self.activebutton(self.teambutton)
    self.showpage("Manage Teams")

    teams = Teams(self.con, self.sport, self.showdashboard, self.master.show_notif)
    teams.pack(fill="both", expand=True)

  def showgames(self):
    self.activebutton(self.gamebutton)
    self.showpage("Manage Games")

    games = Games(self.con, self.sport)
    games.pack(fill="both", expand=True, padx=28, pady=(0,10))


  def showscore(self):
    self.activebutton(self.scorebutton)
    self.showpage("Scoring")

    scoring = Scoring(self.con, self.sport, self.master.show_notif)
    scoring.pack(fill="both", expand=True, padx=28, pady=(0,10))

  def showbracket(self):
    self.activebutton(self.bracketbutton)
    self.showpage("Bracket")

    bracket = Bracket(self.con, self.sport)
    bracket.pack(fill="both", expand=True)

  def showrankings(self):
    self.activebutton(self.rankingbutton)
    self.showpage("Rankings")

    ranking = Rankings(self.con, self.sport)
    ranking.pack(fill="both", expand=True)

  def returntosport(self):
    self.backtosport()

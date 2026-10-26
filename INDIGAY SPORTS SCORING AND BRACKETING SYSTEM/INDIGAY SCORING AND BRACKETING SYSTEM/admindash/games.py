import customtkinter as ctk
from shared.tournamentdata import sports_data, getgameteam, SET_SPORTS
from shared.collegecolors import teamlabel

class Games(ctk.CTkFrame):
  def __init__(self, master, sport):
    super().__init__(master, fg_color="#191a20")

    self.sport=sport
    self.data=sports_data[self.sport]

    self.showgames()

  def getteam(self, game, slot):
    team = getgameteam(self.data, game, slot)
    return "TBD" if team == "Waiting" else team

  def showgames(self):
    for widget in self.winfo_children():
      widget.destroy()

    ctk.CTkLabel(self, text="Games List", font=("arial", 28, "bold"), text_color="#f5f5f7").pack(anchor="w", padx=25, pady=(10,0))
    ctk.CTkLabel(self, text="INDIGAY / " + self.sport + " / Games", font=("arial", 14), text_color="#a0a1aa").pack(anchor="w", padx=25, pady=(0,20))

    if not self.data["games"]:
      ctk.CTkLabel(self, text="No games yet. Waiting for all 7 captain balls to finish adding players.", font=("arial", 14), text_color="#a0a1aa").pack(pady=30)
      return

    scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
    scroll.pack(fill="both", expand=True, padx=25, pady=(0,20))

    for game in self.data["games"]:
      team1 = self.getteam(game, "team1")
      team2 = self.getteam(game, "team2")

      if game.get("status") == "Completed" and game.get("winner"):
        status = "Completed"
      elif team1 == "TBD" or team2 == "TBD":
        status = "Waiting"
      else:
        status = game.get("status", "Scheduled")

      card = ctk.CTkFrame(scroll, fg_color="#23242b", corner_radius=12, border_width=1, border_color="#303139")
      card.pack(fill="x", pady=7)

      top = ctk.CTkFrame(card, fg_color="transparent")
      top.pack(fill="x", padx=15, pady=(12,5))

      ctk.CTkLabel(top, text="Game " + str(game["game"]), font=("arial", 17, "bold"), text_color="#f4f4f7").pack(side="left")

      statuscolor = (
        "#245b3b" if status == "Completed"
        else "#303f68" if status == "Scheduled"
        else "#594923" if status == "In Progress"
        else "#414149"
      )

      ctk.CTkLabel(top, text=status, font=("arial", 12, "bold"), text_color="white", fg_color=statuscolor, corner_radius=10).pack(side="right", padx=5)

      if self.sport in SET_SPORTS:
        score1 = game.get("sets_won1", 0)
        score2 = game.get("sets_won2", 0)
      else:
        score1 = game.get("score1", 0) or 0
        score2 = game.get("score2", 0) or 0

      teamframe = ctk.CTkFrame(card, fg_color="transparent")
      teamframe.pack(fill="x", padx=16, pady=8)
      teamframe.grid_columnconfigure(0, weight=1)
      teamframe.grid_columnconfigure(1, weight=0)
      teamframe.grid_columnconfigure(2, weight=1)

      teamlabel(teamframe, team1, ("arial", 16, "bold")).grid(row=0, column=0, sticky="w")
      ctk.CTkLabel(teamframe, text=f"{score1} - {score2}", font=("arial", 22, "bold"), text_color="#f5f5f7").grid(row=0, column=1, padx=20)
      teamlabel(teamframe, team2, ("arial", 16, "bold")).grid(row=0, column=2, sticky="e")
    
      if game.get("winner") and game.get("loser"):
        ctk.CTkFrame(card, height=1, fg_color="#393a43").pack(fill="x", padx=16, pady=(8,10))
        ctk.CTkLabel(card, text="Winner: " + str(game["winner"]), font=("arial", 13, "bold"), text_color="#a0cfa7").pack(anchor="w", padx=16, pady=(0, 5))
        ctk.CTkLabel(card, text="Loser: " + str(game["loser"]), font=("arial", 13, "bold"), text_color="#e6a0a0").pack(anchor="w", padx=16, pady=(0,12)) 
        



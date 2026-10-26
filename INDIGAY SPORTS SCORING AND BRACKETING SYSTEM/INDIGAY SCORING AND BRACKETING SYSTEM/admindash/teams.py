import customtkinter as ctk
from shared.tournamentdata import sports_data, savetournament, loadtournament, is_all_done
from authActivity.backend.UserAccount import UserAccount, COLLEGES
from shared.collegecolors import teamlabel

class Teams(ctk.CTkFrame):
  def __init__(self, master, sport, backtodashboard, show_notif):
    super().__init__(master, fg_color="#191a20")

    self.sport=sport
    self.backtodashboard=backtodashboard
    self.show_notif=show_notif
    self.data=sports_data[self.sport]

    self.page()
    self.showteams()

  def page(self):
    g = ctk.CTkFrame(self, fg_color="transparent")
    g.pack(fill="x", padx=25, pady=(5,15))

    ctk.CTkLabel(g, text="Team Management", font=("arial", 23, "bold"), text_color="#f5f5f7").pack(anchor="w")
    ctk.CTkLabel(g, text="Register teams for " + self.sport, font=("arial", 12), text_color="#a0a1aa").pack(anchor="w", pady=(5,0))

    self.f = ctk.CTkFrame(self, fg_color="#23242b", corner_radius=10, border_width=1, border_color="#303139")
    self.f.pack(fill="x", padx=25, pady=5)

    ctk.CTkLabel(self.f, text="COLLEGES:", font=("arial", 11, "bold"), text_color="#a0a1aa").pack(anchor="w", padx=18, pady=(15,5))

    checkframe = ctk.CTkFrame(self.f, fg_color="transparent")
    checkframe.pack(fill="x", padx=18, pady=(0,12))

    self.checkboxes = {}
    for i, college in enumerate(COLLEGES):
      box = ctk.CTkCheckBox(checkframe, text=college, width=100, text_color="#f5f5f7")
      box.grid(row=i // 5, column=i % 5, sticky="w", pady=4)
      self.checkboxes[college] = box

    ctk.CTkLabel(self.f, text="CAPTAIN BALL USERNAME", font=("arial", 11, "bold"), text_color="#a0a1aa").pack(anchor="w", padx=18, pady=(0,5))

    self.captainentry = ctk.CTkEntry(self.f, height=38, placeholder_text="namemiddlename.lastname@my.smciligan.edu.ph", fg_color="#191a20", border_color="#41434d", text_color="#f5f5f7")
    self.captainentry.pack(fill="x", padx=18, pady=(0,12))

    ctk.CTkButton(self.f, text="Add Team", height=35, fg_color="#41434d", hover_color="#555762", text_color="white", command=self.addteam).pack(anchor="w", padx=18, pady=(0,15))

    list = ctk.CTkFrame(self, fg_color="transparent")
    list.pack(fill="x", padx=25, pady=(18,8))

    ctk.CTkLabel(list, text="Registered Teams", font=("arial", 16, "bold"), text_color="#f5f5f7").pack(side="left")

    self.teamscount = ctk.CTkLabel(list, text="0 / 7 teams", font=("arial", 12, "bold"), text_color="#a0a1aa")
    self.teamscount.pack(side="right")

    self.teamlist = ctk.CTkScrollableFrame(self, fg_color="#23242b", corner_radius=10, border_width=1, border_color="#303139")
    self.teamlist.pack(fill="both", expand=True, padx=25, pady=(0,10))

    self.readycount = ctk.CTkLabel(self, text="", font=("arial", 13, "bold"), text_color="#a0a1aa")
    self.readycount.pack(anchor="e", padx=25, pady=(5,15))

  def showteams(self):
    loadtournament()

    for widget in self.teamlist.winfo_children():
      widget.destroy()

    teams = self.data["teams"]

    self.teamscount.configure(text=str(len(teams)) + " / 7 teams")

    if len(teams) == 0:
      ctk.CTkLabel(self.teamlist, text="No teams registered yet.", font=("arial", 13), text_color="#a0a1aa").pack(pady=25)

    for i, team in enumerate(teams):
      self.teamrow(i, team)

    if len(self.data["games"]) > 0:
      self.readycount.configure(text="Games Generated", text_color="#62d98b")
    else:
      self.readycount.configure(text="Teams done: " + str(len(self.data["ready"])) + " / 7 teams", text_color="#a0a1aa")

  def teamrow(self, i, team):
    if team in self.data["ready"]:
      bordercolor = "#2f8a4f"
    else:
      bordercolor = "#303139"

    row = ctk.CTkFrame(self.teamlist, fg_color="#292a31", corner_radius=8, border_width=2, border_color=bordercolor)
    row.pack(fill="x", padx=8, pady=4)

    ctk.CTkLabel(row, text=str(i + 1).zfill(2), width=35, font=("arial", 13, "bold"), text_color="#a0a1aa").pack(side="left", padx=(10,5), pady=12)
    info = ctk.CTkFrame(row, fg_color="transparent")
    info.pack(side="left", padx=8, pady=8)

    captain = self.data["captains"].get(team, "None")
    players = self.data["players"].get(team, [])

    if team in self.data["ready"]:
      teamlabel(info, team, ("arial", 13, "bold")).pack(anchor="w")
    else:
      ctk.CTkLabel(info, text=team, font=("arial", 13, "bold"), text_color="#f5f5f7").pack(anchor="w")
    ctk.CTkLabel(info, text="Captain Ball: " + captain + "   |   Players: " + str(len(players)), font=("arial", 11), text_color="#a0a1aa").pack(anchor="w")

    if team in self.data["ready"]:
      ctk.CTkLabel(info, text="● Done", font=("arial", 11, "bold"), text_color="#62d98b").pack(anchor="w")
    else:
      ctk.CTkLabel(info, text="●  Adding Players", font=("arial", 11, "bold"), text_color="#ffa600").pack(anchor="w")

    def removeteam():
      self.removeteam1(team)

    def viewteam():
      self.viewteam(team)

    removebutton = ctk.CTkButton(row, text="Remove", width=80, height=30, fg_color="#303139", hover_color="#484a54", text_color="white", command=removeteam)
    removebutton.pack(side="right", padx=10, pady=7)

    if len(self.data["games"]) > 0 and not is_all_done(self.sport):
      removebutton.configure(state="disabled")
    ctk.CTkButton(row, text="View", width=80, height=30, fg_color="#41434d", hover_color="#555762", text_color="white", command=viewteam).pack(side="right", pady=7)

  def viewteam(self, team):
    for widget in self.winfo_children():
      widget.destroy()

    top = ctk.CTkFrame(self, fg_color="transparent")
    top.pack(fill="x", padx=25, pady=(5,15))

    ctk.CTkLabel(top, text=team, font=("arial", 23, "bold"), text_color="#f5f5f7").pack(side="left")
    ctk.CTkButton(top, text="← Back to Teams", width=140, height=34, fg_color="#41434d", hover_color="#555762", text_color="white", command=self.backtoteams).pack(side="right")

    c = ctk.CTkFrame(self, fg_color="#23242b", corner_radius=10, border_width=1, border_color="#303139")
    c.pack(fill="x", padx=25, pady=5)

    ctk.CTkLabel(c, text="CAPTAIN BALL", font=("arial", 11, "bold"), text_color="#a0a1aa").pack(anchor="w", padx=18, pady=(15,5))

    captain = self.data["captains"].get(team, "")
    user = UserAccount()
    accounts = user.accounts

    if captain in accounts:
      acc = accounts[captain]
      ctk.CTkLabel(c, text=user.get_fullname(captain), font=("arial", 16, "bold"), text_color="#f5f5f7").pack(anchor="w", padx=18)
      ctk.CTkLabel(c, text=captain, font=("arial", 12), text_color="#a0a1aa").pack(anchor="w", padx=18)
      ctk.CTkLabel(c, text="College: " + acc["college"], font=("arial", 12), text_color="#a0a1aa").pack(anchor="w", padx=18, pady=(0,15))
    else:
      ctk.CTkLabel(c, text="No captain ball", font=("arial", 14), text_color="#a0a1aa").pack(anchor="w", padx=18, pady=(0,15))

    players = self.data["players"].get(team, [])

    ctk.CTkLabel(self, text="Players (" + str(len(players)) + ")", font=("arial", 16, "bold"), text_color="#f5f5f7").pack(anchor="w", padx=25, pady=(18,8))

    playerlist = ctk.CTkScrollableFrame(self, fg_color="#23242b", corner_radius=10, border_width=1, border_color="#303139")
    playerlist.pack(fill="both", expand=True, padx=25, pady=(0,15))

    if len(players) == 0:
      ctk.CTkLabel(playerlist, text="The captain ball has not added any players yet.", font=("arial", 13), text_color="#a0a1aa").pack(pady=25)

    for i, player in enumerate(players):
      row = ctk.CTkFrame(playerlist, fg_color="#292a31", corner_radius=8)
      row.pack(fill="x", padx=8, pady=4)

      ctk.CTkLabel(row, text=str(i + 1).zfill(2), width=35, font=("arial", 13, "bold"), text_color="#a0a1aa").pack(side="left", padx=(10,5), pady=10)
      if player in accounts:
        playercollege = accounts[player]["college"]
      else:
        playercollege = "Not registered"

      ctk.CTkLabel(row, text=user.get_fullname(player), font=("arial", 13, "bold"), text_color="#f5f5f7").pack(side="left", padx=8, pady=10)
      ctk.CTkLabel(row, text=player + "   |   " + playercollege, font=("arial", 11), text_color="#a0a1aa").pack(side="left", padx=8, pady=10)

  def backtoteams(self):
    for widget in self.winfo_children():
      widget.destroy()

    self.page()
    self.showteams()

  def addteam(self):
    loadtournament()

    selected = []
    for college in COLLEGES:
      if self.checkboxes[college].get() == 1:
        selected.append(college)

    if len(selected) == 0:
      self.show_notif("Please check at least one college", "red")
      return

    if len(selected) > 3:
      self.show_notif("A merged team can only have up to 3 colleges", "red")
      return

    if len(self.data["teams"]) >= 7:
      self.show_notif("The maximum number of teams is 7.", "red")
      return

    for team in self.data["teams"]:
      for college in selected:
        if college in team.split(" x "):
          self.show_notif(college + " already has a team!", "red")
          return

    name = " x ".join(selected)

    captain = self.captainentry.get().strip().lower()

    if captain == "":
      self.show_notif("Please enter the captain ball username", "red")
      return

    accounts = UserAccount().accounts
    if captain not in accounts or accounts[captain]["role"] != "student":
      self.show_notif("Captain ball must be a registered student", "red")
      return

    captaincollege = accounts[captain]["college"]
    if captaincollege not in selected:
      self.show_notif("Student is from " + captaincollege + ", not from " + name, "red")
      return

    if captain in self.data["captains"].values():
      self.show_notif("That student is already a captain ball", "red")
      return

    self.data["teams"].append(name)
    self.data["captains"][name] = captain
    self.data["players"][name] = []

    self.resettourna()

    savetournament()

    for college in COLLEGES:
      self.checkboxes[college].deselect()
    self.captainentry.delete(0, "end")

    self.showteams()
    self.show_notif("Team " + name + " added successfully!", "blue")

  def removeteam1(self, removedname):
    loadtournament()

    if removedname not in self.data["teams"]:
      self.showteams()
      return

    if len(self.data["games"]) > 0 and not is_all_done(self.sport):
      self.show_notif("You can't remove a team until all games are done", "red")
      return

    if len(self.data["games"]) > 0:
      self.data["ready"] = []

    self.data["teams"].remove(removedname)

    if removedname in self.data["captains"]:
      del self.data["captains"][removedname]
    if removedname in self.data["players"]:
      del self.data["players"][removedname]
    if removedname in self.data["ready"]:
      self.data["ready"].remove(removedname)

    self.resettourna()

    savetournament()

    self.showteams()

    self.show_notif(removedname + " was removed", "red")

  def resettourna(self):
    self.data["games"] = []
    self.data["scores"] = {}
    self.data["bracket"] = {}
    self.data["rankings"] = []


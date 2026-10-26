import os
import customtkinter as ctk
from PIL import Image, ImageTk
from shared.tournamentdata import sports_data, getgameteam
from shared.collegecolors import drawteam

class Bracket(ctk.CTkFrame):
  def __init__(self, master, sport):
    super().__init__(master, fg_color="#191a20")

    self.sport=sport
    self.data=sports_data[sport]

    projectfolder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    self.imagepath = os.path.join(projectfolder, "images", "finalbrackethaha.png")

    self.originalimage = None
    self.image = None
    self.canvas = None

    self.showbracket()

  def showbracket(self):
    for widget in self.winfo_children():
      widget.destroy()

    ctk.CTkLabel(self, text="Double Elimination Bracket", font=("arial", 22, "bold"), text_color="#f5f5f7").pack(anchor="w", padx=20, pady=(15,5))

    self.canvas = ctk.CTkCanvas(self, bg="#191a20", highlightthickness=0, bd=0)
    self.canvas.pack(fill="both", expand=True, padx=5, pady=5)

    if not os.path.exists(self.imagepath):
      self.canvas.create_text(300, 100, text="Bracket image not found:\n"
                                             "images/finalbrackethaha.png", fill="#f5f5f7", font=("arial", 16))
      return

    self.originalimage = Image.open(self.imagepath).convert("RGB")

    w, h = self.originalimage.size
    self.originalimage = self.originalimage.crop((0, int(h * 0.27), w, int(h * 0.77)))
    self.canvas.bind("<Configure>", self.resizebracket)
    self.after(100, self.resizebracket)

  def getgame(self, number):
    for game in self.data.get("games", []):
      if game.get("game") == number:
        return game
    return None

  def getteam(self, game, slot):
    team = getgameteam(self.data, game, slot)
    return "" if team == "Waiting" else team

  def getslot(self, gamenumber, slot):
    return self.getteam(self.getgame(gamenumber), slot)

  def getresult(self, gamenumber, resulttype):
    game = self.getgame(gamenumber)

    if not game:
      return ""

    if game.get("status") != "Completed":
      return ""

    return game.get(resulttype) or ""

  def resizebracket(self, event=None):
    if self.originalimage is None:
      return

    width = self.canvas.winfo_width()
    height = self.canvas.winfo_height()

    if width < 2 or height < 2:
      return

    stretched = self.originalimage.resize((width, height), Image.Resampling.LANCZOS)

    self.image = ImageTk.PhotoImage(stretched)

    self.canvas.delete("all")

    self.imagewidth = width
    self.imageheight = height

    self.canvas.create_image(0, 0, image=self.image, anchor="nw")

    self.addteamlabels()

  def addteamlabels(self):
    positions = {
      1: (0.104, 0.054),
      2: (0.104, 0.092),
      3: (0.104, 0.191),
      4: (0.104, 0.228),
      5: (0.104, 0.329),
      6: (0.104, 0.366),
      7: (0.314, 0.434),

      "W1": (0.314, 0.126),
      "W2": (0.314, 0.163),
      "W3": (0.314, 0.397),
      "W4": (0.511, 0.259),
      "W5": (0.511, 0.297),
      "W9": (0.921, 0.530),
      "W11": (0.921, 0.568),
      "L1": (0.117, 0.770),
      "L2": (0.117, 0.807),
      "L4": (0.310, 0.770),
      "L3": (0.310, 0.807),
      "W6": (0.310, 0.916),
      "L5": (0.310, 0.952),
      "W7": (0.511, 0.839),
      "W8": (0.511, 0.876),
      "L9": (0.710, 0.839),
      "W10": (0.710, 0.877)
    }

    self.teamlabel = {}

    self.fontsize = max(8, min(12, int(self.imagewidth / 130)))

    for key, (x, y) in positions.items():
      self.teamlabel[key] = (int(self.imagewidth * x), int(self.imageheight * y))

    self.updatebracket()

  def updatebracket(self):
    self.data = sports_data[self.sport]

    teams = self.data.get("teams", [])

    result = {
      "W1": (1, "winner"),
      "L1": (1, "loser"),
      "W2": (2, "winner"),
      "L2": (2, "loser"),
      "W3": (3, "winner"),
      "L3": (3, "loser"),
      "W4": (4, "winner"),
      "L4": (4, "loser"),
      "W5": (5, "winner"),
      "L5": (5, "loser"),
      "W6": (6, "winner"),
      "W7": (7, "winner"),
      "W8": (8, "winner"),
      "W9": (9, "winner"),
      "L9": (9, "loser"),
      "W10": (10, "winner"),
      "W11": (11, "winner")
    }

    for key, (x, y) in self.teamlabel.items():
      text=""

      if isinstance(key, int):
        if len(teams) >= key:
          text = teams[key - 1]

      elif key in result:
        gamenumber, resulttype = result[key]
        text = self.getresult(gamenumber, resulttype)

      drawteam(self.canvas, x, y, text, ("arial", self.fontsize, "bold"))
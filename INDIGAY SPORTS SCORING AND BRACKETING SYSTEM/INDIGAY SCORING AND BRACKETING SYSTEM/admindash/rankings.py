import os
import customtkinter as ctk
from PIL import Image, ImageTk
from shared.tournamentdata import sports_data
from shared.collegecolors import drawteam


class Rankings(ctk.CTkFrame):
    def __init__(self, master, sport):
        super().__init__(master, fg_color="transparent")
        self.sport = sport

        projectfolder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.imagepath = os.path.join(projectfolder, "images", "ranking.png")

        self.originalimage = None
        self.image = None

        self.show_rankings()

    def show_rankings(self):
        self.canvas = ctk.CTkCanvas(self, bg="#191a20", highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True, padx=5, pady=5)

        if not os.path.exists(self.imagepath):
            self.canvas.create_text(300, 100, text="Ranking image not found:\nimages/ranking.png",
                                    fill="#f5f5f7", font=("Arial", 16))
            return

        self.originalimage = Image.open(self.imagepath).convert("RGB")

        w, h = self.originalimage.size
        self.originalimage = self.originalimage.crop((int(w * 0.13), int(h * 0.08), int(w * 0.87), int(h * 0.865)))

        self.canvas.bind("<Configure>", self.draw_rankings)

    def get_team(self, placement):
        rankings = sports_data[self.sport].get("rankings", [])

        for entry in rankings:
            parts = entry.split("|", 1)
            if len(parts) == 2 and parts[0] == placement:
                return parts[1]

        return ""

    def draw_rankings(self, event=None):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width < 2 or height < 2:
            return

        imagewidth, imageheight = self.originalimage.size
        scale = min(width / imagewidth, height / imageheight)
        newwidth = int(imagewidth * scale)
        newheight = int(imageheight * scale)

        resized = self.originalimage.resize((newwidth, newheight), Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(resized)

        left = (width - newwidth) // 2
        top = (height - newheight) // 2

        self.canvas.delete("all")
        self.canvas.create_image(left, top, image=self.image, anchor="nw")

        podiumfont = max(9, int(newwidth / 45))
        rowfont = max(9, int(newwidth / 38))

        podium = [
            ("1st", 0.229, 0.197),
            ("CHAMPION", 0.493, 0.094),
            ("2nd", 0.770, 0.285)
        ]

        for placement, x, y in podium:
            team = self.get_team(placement)

            px = left + int(newwidth * x)
            py = top + int(newheight * y)

            drawteam(self.canvas, px, py - 8, team, ("Arial", podiumfont, "bold"), anchor="s")

        rows = [
            ("3rd", 0.655),
            ("4th", 0.748),
            ("5th", 0.842),
            ("6th", 0.936)
        ]

        for placement, y in rows:
            drawteam(self.canvas, left + int(newwidth * 0.19), top + int(newheight * y),
                     self.get_team(placement), ("Arial", rowfont, "bold"), anchor="w")

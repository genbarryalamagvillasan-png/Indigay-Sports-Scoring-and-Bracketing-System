import customtkinter as ctk
from shared.tournamentdata import sports_data, loadtournament, get_current_game, is_all_done, get_match_text


class SportSelect(ctk.CTkFrame):
    def __init__(
        self,
        master,
        on_sport_select=None,
        on_logout=None,
        username="Student",
        on_select=None
    ):
        super().__init__(master, fg_color="#191a20")

        self.on_select = on_sport_select or on_select
        self.on_logout = on_logout
        self.username = username

        self.sports = list(sports_data.keys())

        self.show_sports()

    def show_sports(self):
        for widget in self.winfo_children():
            widget.destroy()

        loadtournament()

        main = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        main.pack(
            fill="both",
            expand=True,
            padx=27,
            pady=25
        )

        ctk.CTkLabel(
            main,
            text="SELECT A SPORT",
            font=("Arial", 28, "bold"),
            text_color="#f5f5f7"
        ).pack(anchor="w")

        ctk.CTkLabel(
            main,
            text="INDIGAY / SPORTS / SELECT A SPORT",
            font=("Arial", 13),
            text_color="#8190aa"
        ).pack(anchor="w", pady=(7, 17))

        ctk.CTkLabel(
            main,
            text="Choose a sport to view its teams, games, scores, and bracket.",
            font=("Arial", 14),
            text_color="#c2c5ce"
        ).pack(anchor="w")

        header = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )
        header.pack(fill="x", pady=(12, 25))

        ctk.CTkLabel(
            header,
            text=f"Welcome, {self.username}!",
            font=("Arial", 14),
            text_color="#c2c5ce"
        ).pack(side="left")

        if self.on_logout:
            ctk.CTkButton(
                header,
                text="Logout",
                width=100,
                height=34,
                fg_color="#8b3038",
                hover_color="#a83b45",
                text_color="white",
                command=self.on_logout
            ).pack(side="right")

        ctk.CTkButton(
            header,
            text="Refresh",
            width=100,
            height=34,
            fg_color="#303139",
            hover_color="#41424b",
            text_color="#f5f5f7",
            command=self.show_sports
        ).pack(side="right", padx=(0, 10))


        sports_area = ctk.CTkScrollableFrame(
            main,
            fg_color="transparent",
            corner_radius=0
        )
        sports_area.pack(fill="both", expand=True)

        for column in range(3):
            sports_area.grid_columnconfigure(
                column,
                weight=1,
                uniform="sport"
            )

        for index, sport in enumerate(self.sports):
            row = index // 3
            column = index % 3

            self.create_sport_card(
                sports_area,
                sport,
                row,
                column
            )

    def create_sport_card(self, parent, sport, row, column):
        card = ctk.CTkFrame(
            parent,
            fg_color="#222329",
            border_width=1,
            border_color="#303139",
            corner_radius=10,
            height=300
        )
        card.grid(
            row=row,
            column=column,
            padx=7,
            pady=8,
            sticky="nsew"
        )
        card.grid_propagate(False)

        ctk.CTkLabel(
            card,
            text="🏆",
            font=("Arial", 25),
            text_color="#f5f5f7"
        ).pack(pady=(25, 8))

        ctk.CTkLabel(
            card,
            text=sport,
            font=("Arial", 18, "bold"),
            text_color="#f5f5f7"
        ).pack(pady=(0, 10))

        current_game = get_current_game(sport)
        all_done = is_all_done(sport)

        if all_done:
            ctk.CTkLabel(
                card,
                text="✓  Done",
                font=("Arial", 12, "bold"),
                text_color="#ffffff",
                fg_color="#0B6D00",
                corner_radius=12,
                width=140,
                height=26
            ).pack(pady=(0, 10))
        elif current_game is not None and current_game.get("status") == "In Progress":
            ctk.CTkLabel(
                card,
                text="●  In Playing",
                font=("Arial", 12, "bold"),
                text_color="#ffffff",
                fg_color="#2f8a4f",
                corner_radius=12,
                width=140,
                height=26
            ).pack(pady=(0, 10))
        else:
            ctk.CTkLabel(
                card,
                text="Not Playing",
                font=("Arial", 12, "bold"),
                text_color="#c2c5ce",
                fg_color="#303139",
                corner_radius=12,
                width=140,
                height=26
            ).pack(pady=(0, 10))

        ctk.CTkLabel(
            card,
            text=get_match_text(sport),
            font=("Arial", 14, "bold"),
            text_color="#f5f5f7",
            justify="center"
        ).pack(pady=(0, 15))

        def opensport():
            self.open_sport(sport)

        ctk.CTkButton(
            card,
            text="View Sport    →",
            height=42,
            fg_color="#303139",
            hover_color="#41424b",
            border_width=1,
            border_color="#454650",
            text_color="#f5f5f7",
            font=("Arial", 14, "bold"),
            command=opensport
        ).pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=15
        )

    def open_sport(self, sport):
        if self.on_select:
            self.on_select(sport)

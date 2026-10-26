import os
import customtkinter as ctk
from PIL import Image
from shared.tournamentdata import sports_data, getgameteam, savetournament, loadtournament, get_current_game, is_all_done, is_all_ready, makegames, SET_SPORTS
from authActivity.backend.UserAccount import UserAccount, SCHOOL_DOMAIN
from shared.collegecolors import teamlabel
from admindash.bracket import Bracket
from admindash.rankings import Rankings


class StudentDashboard(ctk.CTkFrame):
    def __init__(self, master, sport, on_back=None, username=None):
        super().__init__(master, fg_color="#191a20")

        self.sport = sport
        self.on_back = on_back
        self.username = username

        self.scoreboard_timer = None

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color="#202127"
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.content.pack(
            side="left",
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        self.build_sidebar()
        self.show_dashboard()



    def build_sidebar(self):
        projectfolder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logopath = os.path.join(projectfolder, "images", "logo.png")

        if os.path.exists(logopath):
            logo = Image.open(logopath)
            self.logo = ctk.CTkImage(
                light_image=logo,
                dark_image=logo,
                size=(190, int(190 * logo.height / logo.width))
            )
            ctk.CTkLabel(
                self.sidebar,
                image=self.logo,
                text=""
            ).pack(pady=(25, 15))

        ctk.CTkLabel(
            self.sidebar,
            text="Scoring and Bracketing System",
            font=("Arial", 12),
            text_color="#8b9bb4"
        ).pack(pady=(0, 30))

        self.dashbutton = self.nav_button(
            "Dashboard",
            self.show_dashboard
        )
        self.gamebutton = self.nav_button(
            "Games",
            self.show_games
        )
        self.bracketbutton = self.nav_button(
            "Bracket",
            self.show_bracket
        )

        self.rankingbutton = self.nav_button(
            "Rankings",
            self.show_rankings
        )

        self.teambutton = None
        if self.get_my_team() is not None:
            self.teambutton = self.nav_button(
                "My Team",
                self.show_my_team
            )

        ctk.CTkButton(
            self.sidebar,
            text="Back to Sports",
            height=42,
            fg_color="#303139",
            hover_color="#41424b",
            text_color="white",
            font=("Arial", 14),
            command=self.back_to_sports
        ).pack(
            side="bottom",
            fill="x",
            padx=13,
            pady=15
        )

    def nav_button(self, text, command):
        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            anchor="w",
            height=44,
            corner_radius=7,
            fg_color="transparent",
            hover_color="#34353d",
            text_color="#f5f5f7",
            font=("Arial", 14),
            command=command
        )
        button.pack(fill="x", padx=11, pady=5)

        return button

    def activebutton(self, button):
        buttons = [self.dashbutton, self.gamebutton, self.bracketbutton, self.rankingbutton]

        if self.teambutton is not None:
            buttons.append(self.teambutton)

        for b in buttons:
            b.configure(fg_color="transparent")

        button.configure(fg_color="#6b6b6a", text_color="white")
        self.actbut = button


    def clear_content(self):
        if self.scoreboard_timer is not None:
            self.after_cancel(self.scoreboard_timer)
            self.scoreboard_timer = None

        for widget in self.content.winfo_children():
            widget.destroy()

    def heading(self, title):
        ctk.CTkLabel(
            self.content,
            text=title,
            font=("Arial", 28, "bold"),
            text_color="#f5f5f7"
        ).pack(anchor="w")



    def get_games(self):
        self.data = sports_data.get(self.sport, {})
        return self.data.get("games", [])

    def empty_message(self, parent, message):
        ctk.CTkLabel(
            parent,
            text=message,
            font=("Arial", 13),
            text_color="#aeb3c0"
        ).pack(pady=20)

    def show_dashboard(self):
        self.activebutton(self.dashbutton)
        self.clear_content()

        self.heading(
            "STUDENT DASHBOARD"
        )

        self.data = sports_data.get(self.sport, {})
        teams = self.data.get("teams", [])
        games = self.get_games()

        stats = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        stats.pack(fill="x")

        for column in range(2):
            stats.grid_columnconfigure(column, weight=1)

        details = [
            ("Registered Teams", len(teams)),
            ("Total Games", len(games)),
            ("Tournament Format", "Double Elimination"),
            ("Selected Sport", self.sport)
        ]

        for index, (title, value) in enumerate(details):
            card = ctk.CTkFrame(
                stats,
                fg_color="#222329",
                border_width=1,
                border_color="#303139",
                corner_radius=9
            )
            card.grid(
                row=index // 2,
                column=index % 2,
                padx=5,
                pady=5,
                sticky="nsew"
            )

            ctk.CTkLabel(
                card,
                text=title,
                font=("Arial", 12),
                text_color="#8b9bb4"
            ).pack(anchor="w", padx=18, pady=(18, 8))

            ctk.CTkLabel(
                card,
                text=str(value),
                font=("Arial", 20, "bold"),
                text_color="#f5f5f7"
            ).pack(anchor="w", padx=18, pady=(0, 18))

        live = ctk.CTkFrame(
            self.content,
            fg_color="#222329",
            border_width=1,
            border_color="#303139",
            corner_radius=9
        )
        live.pack(fill="both", expand=True, pady=(20, 0))

        ctk.CTkLabel(
            live,
            text="Live Scoreboard",
            font=("Arial", 18, "bold"),
            text_color="#f5f5f7"
        ).pack(anchor="w", padx=16, pady=15)

        self.scoreboard_box = ctk.CTkFrame(
            live,
            fg_color="transparent"
        )
        self.scoreboard_box.pack(fill="both", expand=True)

        self.scoreboard_shown = None

        self.update_scoreboard()

    def show_games(self):
        self.activebutton(self.gamebutton)
        self.clear_content()

        self.heading(
            "GAMES"
        )

        scroll = ctk.CTkScrollableFrame(
            self.content,
            fg_color="transparent",
            corner_radius=0
        )
        scroll.pack(fill="both", expand=True)

        games = self.get_games()

        if not games:
            self.empty_message(scroll, "No games available yet.")
            return

        for game in games:
            card = ctk.CTkFrame(
                scroll,
                fg_color="#222329",
                border_width=1,
                border_color="#303139",
                corner_radius=10
            )
            card.pack(fill="x", padx=5, pady=7)

            top = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
            top.pack(fill="x", padx=16, pady=(12, 5))

            ctk.CTkLabel(
                top,
                text=f"Game {game.get('game', '?')}",
                font=("Arial", 16, "bold"),
                text_color="#f5f5f7"
            ).pack(side="left")

            team1 = getgameteam(self.data, game, "team1")
            team2 = getgameteam(self.data, game, "team2")
            if team1 == "Waiting":
                team1 = "TBD"
            if team2 == "Waiting":
                team2 = "TBD"

            status = game.get("status", "Waiting")
            if status == "Completed" and not game.get("winner"):
                status = "Waiting"
            if team1 in ("TBD", "Waiting") or team2 in ("TBD", "Waiting"):
                if status != "Completed":
                    status = "Waiting"

            ctk.CTkLabel(
                top,
                text=status,
                font=("Arial", 12, "bold"),
                text_color="#f5f5f7",
                fg_color=(
                    "#206b45"
                    if status == "Completed"
                    else "#454650"
                ),
                corner_radius=8
            ).pack(side="right", padx=2, pady=2)

            teams_row = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
            teams_row.pack(fill="x", padx=16, pady=10)

            if self.sport in SET_SPORTS:
                score1 = game.get("sets_won1", 0)
                score2 = game.get("sets_won2", 0)
            else:
                score1 = game.get("score1", 0) or 0
                score2 = game.get("score2", 0) or 0

            teamlabel(
                teams_row,
                team1,
                ("Arial", 15, "bold")
            ).pack(side="left", expand=True, anchor="w")

            ctk.CTkLabel(
                teams_row,
                text=f"{score1} - {score2}",
                font=("Arial", 20, "bold"),
                text_color="#f5f5f7"
            ).pack(side="left", padx=15)

            teamlabel(
                teams_row,
                team2,
                ("Arial", 15, "bold")
            ).pack(side="left", expand=True, anchor="e")

            if status == "Completed":
                winner = game.get("winner", "")
                loser = game.get("loser", "")

                if winner:
                    ctk.CTkLabel(
                        card,
                        text=f"Winner: {winner}",
                        font=("Arial", 13, "bold"),
                        text_color="#78c99a"
                    ).pack(anchor="w", padx=16, pady=(5, 3))

                if loser:
                    ctk.CTkLabel(
                        card,
                        text=f"Loser: {loser}",
                        font=("Arial", 13, "bold"),
                        text_color="#e58b83"
                    ).pack(anchor="w", padx=16, pady=(3, 12))
            else:
                ctk.CTkLabel(
                    card,
                    text="Winner: Pending",
                    font=("Arial", 12),
                    text_color="#8b9bb4"
                ).pack(anchor="w", padx=16, pady=(3, 12))

    def update_scoreboard(self):
        if not self.scoreboard_box.winfo_exists():
            return

        loadtournament()

        game = get_current_game(self.sport)

        if is_all_done(self.sport):
            shown = "done"
        elif game is None:
            shown = "none"
        else:
            shown = "Game " + str(game["game"])

        if shown != self.scoreboard_shown:
            for widget in self.scoreboard_box.winfo_children():
                widget.destroy()

            self.draw_scoreboard(shown, game)
            self.scoreboard_shown = shown

        if shown != "done" and shown != "none":
            self.fill_scoreboard(game)

        self.scoreboard_timer = self.after(2000, self.update_scoreboard)

    def draw_scoreboard(self, shown, game):
        box = self.scoreboard_box

        if shown == "done":
            self.empty_message(box, "All matches are done.")
            return

        if shown == "none":
            self.empty_message(box, "No current match.")
            return

        data = sports_data[self.sport]
        team1 = getgameteam(data, game, "team1")
        team2 = getgameteam(data, game, "team2")

        self.status_label = ctk.CTkLabel(
            box,
            text="",
            font=("Arial", 13, "bold"),
            text_color="#ffffff",
            corner_radius=12,
            width=150,
            height=28
        )
        self.status_label.pack(pady=(30, 10))

        ctk.CTkLabel(
            box,
            text=shown.upper(),
            font=("Arial", 22, "bold"),
            text_color="#f5f5f7"
        ).pack(pady=(0, 20))

        board = ctk.CTkFrame(box, fg_color="transparent")
        board.pack(fill="x", padx=30)

        for column in range(3):
            board.grid_columnconfigure(column, weight=1)

        self.score1_label = self.score_card(board, team1, 0)

        ctk.CTkLabel(
            board,
            text="VS",
            font=("Arial", 20, "bold"),
            text_color="#8b9bb4"
        ).grid(row=0, column=1)

        self.score2_label = self.score_card(board, team2, 2)

        self.set_label = ctk.CTkLabel(
            box,
            text="",
            font=("Arial", 15, "bold"),
            text_color="#c2c5ce"
        )
        if self.sport in SET_SPORTS:
            self.set_label.pack(pady=(20, 0))


    def fill_scoreboard(self, game):
        if game.get("status") == "In Progress":
            self.status_label.configure(text="●  LIVE", fg_color="#2f8a4f")
        else:
            self.status_label.configure(text="Waiting to start", fg_color="#454650")

        if self.sport in SET_SPORTS:
            sets = game.get("sets", [])
            set_number = 1
            score1 = 0
            score2 = 0

            for i, item in enumerate(sets):
                if not item.get("winner"):
                    set_number = i + 1
                    score1 = item.get("score1", 0)
                    score2 = item.get("score2", 0)
                    break

            self.set_label.configure(
                text="Set " + str(set_number) + "     |     Sets won: "
                     + str(game.get("sets_won1", 0)) + " - " + str(game.get("sets_won2", 0))
            )
        else:
            score1 = game.get("score1", 0) or 0
            score2 = game.get("score2", 0) or 0

        self.score1_label.configure(text=str(score1))
        self.score2_label.configure(text=str(score2))

    def score_card(self, parent, team, column):
        card = ctk.CTkFrame(
            parent,
            fg_color="#292a31",
            border_width=1,
            border_color="#303139",
            corner_radius=10
        )
        card.grid(row=0, column=column, sticky="nsew", padx=10)

        header = ctk.CTkFrame(
            card,
            fg_color="#1e1f25",
            corner_radius=8,
            height=42
        )
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        teamlabel(header, team, ("Arial", 18, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        score_label = ctk.CTkLabel(
            card,
            text="0",
            font=("Arial", 70, "bold"),
            text_color="#f5f5f7"
        )
        score_label.pack(pady=20)

        return score_label

    def show_bracket(self):
        self.activebutton(self.bracketbutton)
        self.clear_content()

        self.heading(
            "TOURNAMENT BRACKET"
        )

        bracket = Bracket(self.content, self.sport)
        bracket.pack(fill="both", expand=True)

    def show_rankings(self):
        self.activebutton(self.rankingbutton)
        self.clear_content()
        self.heading(
            "RANKINGS"
        )
        rankingview = Rankings(self.content, self.sport)
        rankingview.pack(fill="both", expand=True)

    def get_my_team(self):
        captains = sports_data[self.sport]["captains"]

        for team in captains:
            if captains[team] == self.username:
                return team

        return None

    def team_removed(self):
        self.show_dashboard()
        self.master.show_notif("Your team was removed by the admin", "red")

    def is_team_locked(self, team):
        data = sports_data[self.sport]
        return team in data["ready"] or len(data["games"]) > 0

    def show_my_team(self):
        self.activebutton(self.teambutton)
        self.clear_content()

        loadtournament()

        team = self.get_my_team()

        if team is None:
            self.team_removed()
            return

        locked = self.is_team_locked(team)

        self.heading(
            "MY TEAM"
        )

        if locked:
            ctk.CTkLabel(
                self.content,
                text="✓  Your team is done adding players. The players can no longer be changed.",
                font=("Arial", 13, "bold"),
                text_color="#ffffff",
                fg_color="#2f8a4f",
                corner_radius=9,
                height=45
            ).pack(fill="x")
        else:
            self.add_player_form(team)

        players = sports_data[self.sport]["players"].get(team, [])

        ctk.CTkLabel(
            self.content,
            text="Players (" + str(len(players)) + ")",
            font=("Arial", 16, "bold"),
            text_color="#f5f5f7"
        ).pack(anchor="w", pady=(20, 8))

        player_list = ctk.CTkScrollableFrame(
            self.content,
            fg_color="#222329",
            border_width=1,
            border_color="#303139",
            corner_radius=9
        )
        player_list.pack(fill="both", expand=True)

        if len(players) == 0:
            self.empty_message(player_list, "No players added yet.")

        user = UserAccount()

        for i, player in enumerate(players):
            self.player_row(player_list, i, player, user, locked)

        if not locked:
            ctk.CTkButton(
                self.content,
                text="Done Adding Players",
                height=40,
                fg_color="#2f8a4f",
                hover_color="#3a9d5c",
                text_color="white",
                font=("Arial", 13, "bold"),
                command=self.done_adding
            ).pack(anchor="e", pady=(12, 0))

    def player_row(self, player_list, i, player, user, locked):
        row = ctk.CTkFrame(
            player_list,
            fg_color="#292a31",
            corner_radius=8
        )
        row.pack(fill="x", padx=8, pady=4)

        ctk.CTkLabel(
            row,
            text=str(i + 1) + ".  " + user.get_fullname(player),
            font=("Arial", 13, "bold"),
            text_color="#f5f5f7"
        ).pack(side="left", padx=12, pady=10)

        ctk.CTkLabel(
            row,
            text=player,
            font=("Arial", 11),
            text_color="#8b9bb4"
        ).pack(side="left", padx=5, pady=10)

        if locked:
            return

        def removeplayer():
            self.remove_player(player)

        ctk.CTkButton(
            row,
            text="Remove",
            width=80,
            height=30,
            fg_color="#303139",
            hover_color="#484a54",
            text_color="white",
            command=removeplayer
        ).pack(side="right", padx=10, pady=7)

    def add_player_form(self, team):
        form = ctk.CTkFrame(
            self.content,
            fg_color="#222329",
            border_width=1,
            border_color="#303139",
            corner_radius=9
        )
        form.pack(fill="x")

        ctk.CTkLabel(
            form,
            text="PLAYER USERNAME  (the player must be registered and from " + team + ")",
            font=("Arial", 11, "bold"),
            text_color="#8b9bb4"
        ).pack(anchor="w", padx=16, pady=(15, 5))

        self.player_entry = ctk.CTkEntry(
            form,
            height=38,
            placeholder_text="namemiddlename.lastname" + SCHOOL_DOMAIN,
            fg_color="#191a20",
            border_color="#41434d",
            text_color="#f5f5f7"
        )
        self.player_entry.pack(fill="x", padx=16, pady=(0, 12))

        ctk.CTkButton(
            form,
            text="Add Player",
            height=35,
            fg_color="#41434d",
            hover_color="#555762",
            text_color="white",
            command=self.add_player
        ).pack(anchor="w", padx=16, pady=(0, 15))

    def done_adding(self):
        loadtournament()

        data = sports_data[self.sport]
        team = self.get_my_team()

        if team is None:
            self.team_removed()
            return

        if len(data["players"].get(team, [])) == 0:
            self.master.show_notif("Please add player first", "red")
            return

        if team not in data["ready"]:
            data["ready"].append(team)
        savetournament()

        if len(data["games"]) == 0 and is_all_ready(self.sport):
            makegames(self.sport)
            self.show_my_team()
            self.master.show_notif("All teams are done! The games are now generated", "blue")
            return

        self.show_my_team()
        self.master.show_notif(team + " is done adding players", "blue")

    def add_player(self):
        loadtournament()

        team = self.get_my_team()

        if team is None:
            self.team_removed()
            return

        if self.is_team_locked(team):
            self.master.show_notif("Your team is already done adding players", "red")
            return
        players = sports_data[self.sport]["players"]
        username = self.player_entry.get().strip().lower()

        if username == "":
            self.master.show_notif("Please enter the player username", "red")
            return

        user = UserAccount()
        accounts = user.accounts

        if username not in accounts or accounts[username]["role"] != "student":
            self.master.show_notif("That player is not registered", "red")
            return

        playercollege = accounts[username]["college"]
        if playercollege not in team.split(" x "):
            self.master.show_notif("That player is from " + playercollege + ", not from " + team, "red")
            return

        if username in sports_data[self.sport]["captains"].values():
            self.master.show_notif("That student is already the captain ball", "red")
            return

        for otherteam in players:
            if username in players[otherteam]:
                self.master.show_notif("That player is already in " + otherteam, "red")
                return

        if team not in players:
            players[team] = []

        players[team].append(username)
        savetournament()

        self.show_my_team()
        self.master.show_notif(user.get_fullname(username) + " was added", "blue")

    def remove_player(self, name):
        loadtournament()

        team = self.get_my_team()

        if team is None:
            self.team_removed()
            return

        if self.is_team_locked(team):
            self.master.show_notif("Your team is already done adding players", "red")
            return

        if name in sports_data[self.sport]["players"].get(team, []):
            sports_data[self.sport]["players"][team].remove(name)
        savetournament()

        self.show_my_team()
        self.master.show_notif(UserAccount().get_fullname(name) + " was removed", "red")


    def back_to_sports(self):
        if self.on_back:
            self.on_back()
            

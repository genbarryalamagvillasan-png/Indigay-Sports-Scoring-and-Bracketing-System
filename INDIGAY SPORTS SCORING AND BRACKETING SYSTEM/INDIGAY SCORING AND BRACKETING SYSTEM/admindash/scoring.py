import customtkinter as ctk
from shared.tournamentdata import sports_data, savetournament, loadtournament, getgameteam, SET_SPORTS
from shared.ranking import updaterankings
from shared.collegecolors import teamlabel

class Scoring(ctk.CTkFrame):
    def __init__(self, master, sport, show_notif):
        super().__init__(master, fg_color='#191a20')
        self.sport = sport
        self.show_notif = show_notif
        self.data = sports_data[sport]
        self.selectedgame = None
        self.issetscoring = sport in SET_SPORTS
        self.showscoring()

    def showscoring(self):
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self, text='Game Scoring', font=('Arial', 28, 'bold'), text_color='#f5f5f7').pack(anchor='w', padx=25, pady=(10, 0))
        ctk.CTkLabel(self, text='INDIGAY / ' + self.sport + ' / Scoring', font=('Arial', 14), text_color='#a0a1aa').pack(anchor='w', padx=25, pady=(0, 15))
        
        if not self.data['games']:
            ctk.CTkLabel(self, text='No games yet. Waiting for all 7 captain balls to finish adding players.', font=('Arial', 14), text_color='#a0a1aa').pack(pady=30)
            return
        
        self.gameoptions = []

        for game in self.data['games']:
            team1 = self.getteam(game, 'team1')
            team2 = self.getteam(game, 'team2')
            self.gameoptions.append('Game ' + str(game['game']) + ': ' + team1 + ' vs ' + team2)
        
        self.topframe = ctk.CTkFrame(self, fg_color='#23242b', corner_radius=12)
        self.topframe.pack(fill='x', padx=25, pady=(0, 12))
        self.topframe.grid_columnconfigure(0, weight=3)
        self.topframe.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.topframe, text='Select Game', font=('Arial', 14, 'bold'), text_color='#f5f5f7').grid(row=0, column=0, sticky='w', padx=15, pady=(10, 0))
        
        self.game_menu = ctk.CTkOptionMenu(self.topframe, values=self.gameoptions, command=self.selectgame, width=300, height=38, fg_color="#a0a1aa")
        self.game_menu.grid(row=1, column=0, sticky='ew', padx=15, pady=(5, 12))
        
        statusframe = ctk.CTkFrame(self.topframe, fg_color='#292a31', corner_radius=8)
        statusframe.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=12, pady=10)
        
        ctk.CTkLabel(statusframe, text='Game Status', text_color='#a0a1aa', font=('Arial', 12)).pack(anchor='w', padx=12, pady=(8, 2))
        
        self.statuslabel = ctk.CTkLabel(statusframe, text='Not Scheduled', text_color='#ffffff', fg_color='#303f68', corner_radius=15, font=('Arial', 13, 'bold'))
        self.statuslabel.pack(anchor='w', padx=12, pady=(0, 8))
        
        self.matchframe = ctk.CTkFrame(self, fg_color='#23242b', corner_radius=12, border_width=1, border_color='#303139')
        self.matchframe.pack(fill='both', expand=True, padx=25, pady=(0, 15))

        current = self.getcurrentgame()

        if current:
            selectedoption = next((option for option in self.gameoptions if option.startswith("Game " + str(current["game"]) + ": ")), self.gameoptions[0])
        else:
            selectedoption = self.gameoptions[0]

        self.game_menu.set(selectedoption)
        self.selectgame(selectedoption)

    def getteam(self, game, slot):
        return getgameteam(self.data, game, slot)

    def reloadgame(self):
        number = self.selectedgame["game"]
        loadtournament()

        for game in self.data["games"]:
            if game["game"] == number:
                self.selectedgame = game
                return game

        return None

    def getcurrentgame(self):
        for game in self.data['games']:
            if game.get("status") == "Completed" and game.get("winner"):
                continue
            
            team1 = self.getteam(game, 'team1')
            team2 = self.getteam(game, 'team2')
            
            if team1 == 'Waiting' or team2 == 'Waiting':
                continue
            
            ready = True

            for slot in ['team1', 'team2']:
                source = game.get(slot + '_source')
                if source:
                    result, sourcenumber = source
                    sourcegame = None
                    for previous in self.data['games']:
                        if previous['game'] == sourcenumber:
                            sourcegame = previous
                            break
                    
                    if sourcegame is None or not sourcegame.get(result):
                        ready = False
                        break
            
            if ready:
                return game
        
        return None

    def selectgame(self, choice):
        game_number = int(choice.split(':')[0].replace('Game ', ''))

        self.selectedgame = None
        
        for game in self.data['games']:
            if game['game'] == game_number:
                self.selectedgame = game
                break

        if self.selectedgame is None:
            return

        for widget in self.matchframe.winfo_children():
            widget.destroy()

        game = self.selectedgame
        team1 = self.getteam(game, 'team1')
        team2 = self.getteam(game, 'team2')
        current = self.getcurrentgame()

        if game.get("game") == 13 and game.get("status") == "Waiting":
            status = "Waiting"
        elif game.get("status") == "Completed" and game.get("winner"):
            status = "Completed"
        elif team1 == "Waiting" or team2 == "Waiting":
            status = "Waiting"
        elif current and current["game"] == game["game"]:
            if game.get("status") == "In Progress":
                status = "In Progress"
            else:
                status = "Scheduled"
        elif game.get("status") == "In Progress":
            status = "In Progress"
        else:
            status = "Not Scheduled"
        self.statuslabel.configure(text=status)
        
        ctk.CTkLabel(self.matchframe, text='GAME ' + str(game['game']), font=('Arial', 25, 'bold'), text_color='#f5f5f7').pack(pady=(12, 0))
        vsrow = ctk.CTkFrame(self.matchframe, fg_color='transparent')
        vsrow.pack(pady=(0, 8))
        teamlabel(vsrow, team1, ('Arial', 15, 'bold')).pack(side='left')
        ctk.CTkLabel(vsrow, text='     VS.     ', font=('Arial', 15, 'bold'), text_color='#a0a1aa').pack(side='left')
        teamlabel(vsrow, team2, ('Arial', 15, 'bold')).pack(side='left')
        
        if self.issetscoring:
            self.showsetscoring(game, team1, team2, status)
        else:
            self.showregularscoring(game, team1, team2, status)

    def createscorecard(self, parent, team, score, column):
        card = ctk.CTkFrame(parent, fg_color='#292a31', corner_radius=10, border_width=1, border_color='#303139')
        card.grid(row=0, column=column, sticky='nsew', padx=8, pady=5)
        
        header = ctk.CTkFrame(card, fg_color='#1e1f25', corner_radius=6, height=38)
        header.pack(fill='x', padx=1, pady=1)
        header.pack_propagate(False)
        teamlabel(header, team, ('Arial', 16, 'bold')).place(relx=0.5, rely=0.5, anchor='center')
        
        scorelabel = ctk.CTkLabel(card, text=str(score), font=('Arial', 42, 'bold'), text_color='#f5f5f7')
        scorelabel.pack(pady=(4, 8))
        
        buttons = ctk.CTkFrame(card, fg_color='transparent')
        buttons.pack(fill='x', padx=8, pady=(0, 10))
        
        if self.sport == 'Basketball':
            pointlist = [1, 2, 3]
        else:
            pointlist = [1]

        for index in range(len(pointlist)):
            buttons.grid_columnconfigure(index, weight=1)
        for index, points in enumerate(pointlist):
            ctk.CTkButton(buttons, text='+' + str(points), height=32, fg_color='#41434d', hover_color='#555762', command=self.makescorechange(column, points, scorelabel)).grid(row=0, column=index, sticky='ew', padx=2, pady=2)
        for index, points in enumerate(pointlist):
            ctk.CTkButton(buttons, text='-' + str(points), height=32, fg_color='#7b343b', hover_color='#963e47', command=self.makescorechange(column, -points, scorelabel)).grid(row=1, column=index, sticky='ew', padx=2, pady=2)
        if column == 0:
            self.score1label = scorelabel
            self.score1buttons = buttons
        else:
            self.score2label = scorelabel
            self.score2buttons = buttons

    def showregularscoring(self, game, team1, team2, status):
        if status in ["Waiting", "Not Scheduled"]:
            ctk.CTkLabel(
                self.matchframe,
                text="Waiting for this game to be scheduled.",
                font=("Arial", 18, "bold"),
                text_color="#a0a1aa"
            ).pack(pady=25)
            return

        if status == "Completed":
            ctk.CTkLabel(self.matchframe, text="Match Completed", font=("arial", 20, "bold"), text_color="#62d98b").pack(pady=15)
            return
        
        teamsframe = ctk.CTkFrame(self.matchframe, fg_color='transparent')
        teamsframe.pack(fill='x', expand=False, padx=20, pady=5)
        teamsframe.grid_columnconfigure(0, weight=1)
        teamsframe.grid_columnconfigure(1, weight=1)
        
        self.createscorecard(teamsframe, team1, game.get('score1', 0) or 0, 0)
        self.createscorecard(teamsframe, team2, game.get('score2', 0) or 0, 1)
        
        self.savebutton = ctk.CTkButton(self.matchframe, text='Done - Save Result', height=40, font=('Arial', 14, 'bold'), fg_color='#245b3b', hover_color='#306d48', command=self.done)
        self.savebutton.pack(fill='x', padx=20, pady=(8, 12))

        if status not in ['Scheduled', 'In Progress']:
            self.disablescorebuttons()
            self.savebutton.configure(state='disabled')

    def showsetscoring(self, game, team1, team2, status):
        if status in ["Waiting", "Not Scheduled"]:
            ctk.CTkLabel(
                self.matchframe,
                text="Waiting for this game to be scheduled.",
                font=("Arial", 18, "bold"),
                text_color="#a0a1aa"
            ).pack(pady=25)
            return

        if not game.get("sets"):
            game["sets"] = [{"score1": 0, "score2": 0, "winner": None}
                            for _ in range(3)]

        sets = game['sets']

        results = ctk.CTkFrame(self.matchframe, fg_color='transparent')
        results.pack(fill='x', padx=20, pady=(0, 5))
        
        for index, item in enumerate(sets):
            if item.get('winner'):
                result_text = 'Set ' + str(index + 1) + ': ' + str(item['score1']) + ' - ' + str(item['score2'])
            else:
                result_text = 'Set ' + str(index + 1) + ': Not played'
            ctk.CTkLabel(results, text=result_text, font=('Arial', 12), text_color='#f5f5f7', fg_color='#303139', corner_radius=6).pack(side='left', expand=True, fill='x', padx=3, pady=3)
        
        activeset = None

        for index, item in enumerate(sets):
            if not item.get('winner'):
                activeset = index
                break
        if game.get("status") == "Completed" and game.get("winner"):
            ctk.CTkLabel(
                self.matchframe,
                text="Match Completed",
                font=("Arial", 20, "bold"),
                text_color="#62d98b"
            ).pack(pady=15)
            return

        if activeset is None:
            ctk.CTkLabel(
                self.matchframe,
                text="No playable set found. Check this game's set data.",
                font=("Arial", 16, "bold"),
                text_color="#e6b566"
            ).pack(pady=15)
            return
        
        setdata = sets[activeset]
        
        ctk.CTkLabel(self.matchframe, text='SET ' + str(activeset + 1), font=('Arial', 18, 'bold'), text_color='#f5f5f7').pack(pady=(2, 0))
        
        teamsframe = ctk.CTkFrame(self.matchframe, fg_color='transparent')
        teamsframe.pack(fill='x', expand=False, padx=20, pady=3)
        teamsframe.grid_columnconfigure(0, weight=1)
        teamsframe.grid_columnconfigure(1, weight=1)
        
        self.createscorecard(teamsframe, team1, setdata['score1'], 0)
        self.createscorecard(teamsframe, team2, setdata['score2'], 1)
        self.savebutton = ctk.CTkButton(self.matchframe, text='Done - Save Set Result', height=40, font=('Arial', 14, 'bold'), fg_color='#245b3b', hover_color='#306d48', command=self.savesetresult)
        self.savebutton.pack(fill='x', padx=20, pady=(8, 12))
        
        if status not in ['Scheduled', 'In Progress']:
            self.disablescorebuttons()
            self.savebutton.configure(state='disabled')

    def makescorechange(self, column, points, scorelabel):
        def update_score():
            game = self.reloadgame()
            current = self.getcurrentgame()

            if game is None or (game.get('status') == 'Completed' and game.get('winner')) or current is None:
                return

            if game['game'] != current['game']:
                return

            key = 'score1' if column == 0 else 'score2'

            if self.issetscoring:
                if not game.get('sets'):
                    game['sets'] = [{'score1': 0, 'score2': 0, 'winner': None} for _ in range(3)]
                activeset = next((item for item in game['sets'] if not item.get('winner')), None)

                if activeset is None:
                    return

                newscore = max(0, activeset.get(key, 0) + points)
                if newscore == activeset.get(key, 0):
                    return

                activeset[key] = newscore
                scorelabel.configure(text=str(activeset[key]))
            else:
                newscore = max(0, (game.get(key) or 0) + points)
                if newscore == (game.get(key) or 0):
                    return

                game[key] = newscore
                scorelabel.configure(text=str(game[key]))
            
            game['status'] = 'In Progress'
            self.statuslabel.configure(text='In Progress')
            savetournament()

        return update_score

    def disablescorebuttons(self):
        for button in self.score1buttons.winfo_children():
            button.configure(state='disabled')
        
        for button in self.score2buttons.winfo_children():
            button.configure(state='disabled')

    def checkresetfinal(self, game):
        if game.get("game") != 12:
            return

        team1 = self.getteam(game, "team1")
        team2 = self.getteam(game, "team2")

        game9 = next((item for item in self.data["games"] if item ["game"] == 9), None)

        if game9 is None:
            return

        winnerfinalist = game9.get("winner")

        if game.get("winner") != winnerfinalist:
            game13 = next((item for item in self.data["games"] if item["game"] == 13), None)

            if game13 is None:
                game13 = {
                    "game": 13, "team1": None, "team2": None,
                    "score1": 0, "score2": 0,
                    "winner": None, "loser": None,
                    "status": "Waiting",
                    "team1_source": None, "team2_source": None
                }
                self.data["games"].append(game13)

            game13.update({
                "team1": team1,
                "team2": team2,
                "score1": 0,
                "score2": 0,
                "winner": None,
                "loser": None,
                "status": "Scheduled",
                "team1_source": None,
                "team2_source": None,
                "sets_won1": 0,
                "sets_won2": 0,
                "sets": []
            })
        else:

            for item in self.data["games"]:
                if item["game"] == 13:
                    item.update({
                        "team1": None,
                        "team2": None,
                        "score1": 0,
                        "score2": 0,
                        "winner": None,
                        "loser": None,
                        "status": "Waiting",
                        "sets_won1": 0,
                        "sets_won2": 0,
                        "sets": []
                    })

    def savesetresult(self):
        game = self.reloadgame()
        current = self.getcurrentgame()

        if game is None or current is None or current['game'] != game['game']:
            self.statuslabel.configure(text='Not Scheduled')
            return

        team1 = self.getteam(game, 'team1')
        team2 = self.getteam(game, 'team2')

        if not game.get('sets'):
            game['sets'] = [{'score1': 0, 'score2': 0, 'winner': None} for _ in range(3)]
        sets = game['sets']

        activeset = next((item for item in sets if not item.get('winner')), None)

        if activeset is None:
            return

        score1 = activeset['score1']
        score2 = activeset['score2']

        if score1 == score2:
            self.show_notif("Scores are tied", "red")
            return
        
        activeset['winner'] = team1 if score1 > score2 else team2
        game['sets_won1'] = sum((1 for item in sets if item.get('winner') == team1))
        game['sets_won2'] = sum((1 for item in sets if item.get('winner') == team2))

        if game['sets_won1'] >= 2:
            game['winner'] = team1
            game['loser'] = team2
            game['status'] = 'Completed'
        elif game['sets_won2'] >= 2:
            game['winner'] = team2
            game['loser'] = team1
            game['status'] = 'Completed'
        else:
            game['status'] = 'In Progress'

        if game.get("status") == "Completed":
            self.checkresetfinal(game)
            updaterankings(self.data, game)

        savetournament()

        if game.get("status") == "Completed":
            self.showscoring()
        else:
            self.selectgame(self.game_menu.get())

    def done(self):
        game = self.reloadgame()
        current = self.getcurrentgame()

        if game is None or current is None or current['game'] != game['game']:
            self.statuslabel.configure(text='Not Scheduled')
            return

        team1 = self.getteam(game, 'team1')
        team2 = self.getteam(game, 'team2')

        score1 = game.get('score1') or 0
        score2 = game.get('score2') or 0

        if score1 == score2:
            self.show_notif("Scores are tied", "red")
            return

        game['team1'] = team1
        game['team2'] = team2

        if score1 > score2:
            game['winner'] = team1
            game['loser'] = team2
        else:
            game['winner'] = team2
            game['loser'] = team1
        game['status'] = 'Completed'
        self.checkresetfinal(game)
        updaterankings(self.data, game)
        savetournament()
        self.showscoring()

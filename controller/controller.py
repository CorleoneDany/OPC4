"""Reprents the controller."""

from model import Player, Match, Tournament

from view import (
    MotherView,
    MainMenu,
    CreateTournamentView,
    RetrieveTournamentView,
    CreatePlayersView,
    CreateMatchView,
    ShowMatches,
    ChooseMatchView,
    ModifyMatchView,
    PlayerMenuView,
)


class Controller:
    """Reprents the controller."""

    def __init__(self):
        """Init class with attributes."""
        self.view = MainMenu(observer=self)
        self.running = True
        self.context = {}
        self.tournament = None

    def run(self):
        while self.running:
            self.view.display()

    def execute(self, command):
        name = command["name"]
        if name == "create_tournament":
            self.view = CreateTournamentView(observer=self)
            self.create_tournament()
        elif name == "retrieve_tournament":
            self.view = RetrieveTournamentView(observer=self)
        elif name == "main_page":
            self.view = MainMenu(observer=self)
        elif name == "player_menu":
            self.view = PlayerMenuView(observer=self)
        elif name == "ask_player_creation":
            self.view = CreatePlayersView(observer=self)
        elif name == "create_player":
            for players_needed in range(8):
                data = self.context[f"player{players_needed}"]
                player = Player(**data)
                self.tournament.players.append(player)
        elif name == "create_matchs":
            self.tournament.create_first_rounds()
            self.view = CreateMatchView(observer=self, matches=self.tournament.rounds)
        elif name == "select_match":
            self.view = ChooseMatchView(observer=self, matches=self.tournament.rounds)
        elif name == "modify_match":
            self.view = ModifyMatchView(
                observer=self, match=self.context["chosen_match"]
            )
            self.update_score(self.match, self.context["chosen_winner"])
            self.context["chosen_winner"] = None
        elif name == "wrong_command":
            self.view.wrong_command()

    def update_score(self, match, choice):
        if choice == 1:
            match.player_1.score += 1
        elif choice == 2:
            match.player_2.score += 1
        elif choice:
            match.player_1.score += 0.5
            match.player_2.score += 0.5

    def next_turn(self):
        for match in self.tournament.matches:
            if self.tournament.matches.winner_alias:
                pass
            else:
                self.view = ChooseMatchView(observer=self)

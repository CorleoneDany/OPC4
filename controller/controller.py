"""Reprents the controller."""

from model import DB, Player, Match, Tournament

from view import (
    MotherView,
    MainMenu,
    CreateTournamentView,
    RetrieveTournamentView,
    CreatePlayersView,
    CreateMatchView,
    ShowMatches,
    ChooseMatch,
    InputMatchWinner,
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
            self.view = CreateMatchView(observer=self)
        elif name == "wrong_command":
            self.view.wrong_command()

    def create_tournament(self):
        self.view.display()
        data = self.context["tournament_data"]
        self.tournament = Tournament(**data)
        print("Tournoi créé avec succès.")

    def create_first_matchs(self, high_ranks, low_ranks):
        for match_ups in range(4):
            self.tournament.matchs.append(high_ranks, low_ranks)
            self.view.display_created_match(self.tournament.matchs)

    def update_score(self, match, choice):
        if choice == 1:
            match.player_1.score += 1
        elif choice == 2:
            match.player_2.score += 1
        elif choice:
            match.player_1.score += 0.5
            match.player_2.score += 0.5

    def next_turn(self):
        pass

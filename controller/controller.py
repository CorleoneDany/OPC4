"""Reprents the controller."""

from model import DB, Player, Match, Tournament

from view import (
    MotherView,
    MainMenu,
    CreateTournamentView,
    RetrieveTournamentView,
    CreatePlayerView,
    CreatedPlayerView,
    CreateMatchView,
    ShowMatches,
    ChooseMatch,
    InputMatchWinner,
)


class Controller:
    """Reprents the controller."""

    def __init__(self):
        """Init class with attributes."""
        self.view = MainMenu(self)
        self.running = True
        self.context = {}

    def run(self):
        while self.running:
            self.view.display()

    def update(self, command):
        if command == "create_tournament":
            self.view = CreateTournamentView(self)
        elif command == "retrieve_tournament":
            self.view = RetrieveTournamentView(self)
        elif command == "wrong_command":
            self.view.wrong_command()

    def display_menu(self):
        choice = self.view.display()
        if choice == 1:
            self.create_tournament()
            self.create_player_lists()
            player_list = self.return_player_list()
            self.create_first_matchs(**player_list)
        elif choice == 2:
            print("Fonction en cours de dev")

        self.view.display_all_matches(self.tournament.matchs)
        self.choose_match()

    def display_matches(self):
        self.view.display_matches(self.tournament.matchs)
        self.view.choose_match()

    def create_tournament(self):
        data = self.view.ask_tournament_data()
        self.tournament = Tournament(**data)
        print("Tournoi créé avec succès.")
        self.create_player_list()

    def create_player_list(self, number_of_players=8):
        for number in range(number_of_players):
            self.tournament.players.append(self.view.ask_player_data())
            self.view.display_last_player_created(self.tournament.players)

    def return_player_list(self):
        sorted_players = sorted(self.tournament.players, key=lambda i: i["ranking"])
        return {
            "high_ranks": sorted_players(range(0, 3)),
            "low_ranks": sorted_players(range(4, 7)),
        }

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

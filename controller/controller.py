"""Reprents the controller."""

from model import DB, Player, Match, Tournament

from view import Base


class Controller:
    """Reprents the controller."""

    def __init__(self):
        """Init class with attributes."""
        self.view = Base()

    def display_menu(self):
        choice = self.view.display_menu()
        if choice == 1:
            data = self.view.ask_tournament_data()
            self.tournament = Tournament(**data)
            self.create_player_list()
        elif choice == 2:
            print("Fonction en cours de dev")

    def create_player_list(self, number_of_players=8):
        for number in range(number_of_players):
            self.tournament.players.append(self.view.ask_player_data)

    def run(self):
        self.display_menu()

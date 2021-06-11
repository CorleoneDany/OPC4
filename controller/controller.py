"""Reprents the controller."""

from view.base import SelectPlayerView
from model import Player, Match, Tournament, player

from faker import Faker

from view import (
    MainMenu,
    CreateTournamentView,
    RetrieveTournamentView,
    CreatePlayersView,
    CreateMatchView,
    ShowMatches,
    ChooseMatchView,
    ModifyMatchView,
    PlayerMenuView,
    SelectPlayerView,
)


# todo récupérer les joueurs déjà créés lors de la création du tournoi
# afficher la liste de joueurs en bdd et proposer de les ajouter via une selection
# tant qu'il y a - de 8 joueurs continuer
# créer une commande qui crée 8 joueurs random https://faker.readthedocs.io/en/master/

# faker.date()
# faker.name() first name et last name ?
# random sex ?
# random.randrange()
# fake.profile()


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
        if name == "main_page":
            self.view = MainMenu(observer=self)
        elif name == "create_tournament":
            self.view = CreateTournamentView(observer=self)
            self.view.display()
            self.tournament = Tournament(**self.context["tournament_data"])
        elif name == "retrieve_tournament":
            self.view = RetrieveTournamentView(observer=self)
        elif name == "player_menu":
            self.view = PlayerMenuView(observer=self)
        elif name == "select_player":
            self.view = SelectPlayerView(observer=self)
        elif name == "ask_players_creation":
            self.view = CreatePlayersView(observer=self)
        elif name == "create_players":
            Player.create_players(self.context, self.tournament)
            self.tournament.save()
        elif name == "create_matchs":
            self.tournament.create_turn()
            self.view = CreateMatchView(observer=self, matches=self.tournament.rounds)
        elif name == "select_match":
            self.view = ChooseMatchView(observer=self, matches=self.tournament.rounds)
        elif name == "modify_match":
            self.view = ModifyMatchView(
                observer=self, match=self.context["chosen_match"]
            )
            self.update_score(
                self.context["chosen_match"], self.context["chosen_winner"]
            )
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

    def next_rounds(self):
        for match in self.tournament.matches:
            if self.tournament.matches.winner_alias:
                pass
            else:
                self.view = ChooseMatchView(observer=self)

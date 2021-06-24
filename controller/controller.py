"""Reprents the controller."""

import datetime

from view.base import SelectPlayerView
from model import Player, Match, Tournament

from tinydb import TinyDB, Query
import config

from view import (
    MainMenu,
    CreateTournamentView,
    RetrieveTournamentView,
    CreatePlayerView,
    CreateMatchView,
    ShowMatches,
    ChooseMatchView,
    ModifyMatchView,
    PlayerMenuView,
    SelectPlayerView,
)


# todo récupérer les joueurs déjà créés lors de la création du tournoi
# afficher la liste de joueurs en bdd et proposer de les ajouter via une selection


class Controller:
    """Reprents the controller."""

    def __init__(self):
        """Init class with attributes."""
        self.view = MainMenu(observer=self)
        self.running = True
        self.context = {}
        self.tournament = None

    def run(self):
        """Launch the program."""
        if len(Player.list()) < 1:
            Player.create_height_players()

        while self.running:
            self.view.display()

    def execute(self, command):
        """Execute the given command."""
        name = command["name"]
        if name == "main_page":
            self.view = MainMenu(observer=self)
        elif name == "create_tournament":
            self.view = CreateTournamentView(observer=self)
            self.view.display()
            self.tournament = Tournament(**self.context["tournament_data"])
        elif name == "retrieve_tournament":
            self.view = RetrieveTournamentView(observer=self)
            self.view.display(Tournament.list())
            self.tournament = Tournament.get(self.context["chosen_tournament"])
        elif name == "player_menu":
            self.view = PlayerMenuView(observer=self, players=self.tournament.players)
        elif name == "select_player":
            self.view = SelectPlayerView(observer=self, players=Player.list())
            self.view.display()
            self.tournament.players.append(Player.get(self.context["chosen_player"]))
        elif name == "ask_player_creation":
            self.view = CreatePlayerView(observer=self)
            player = Player(*self.context["player_created"])
            player.save()
            self.tournament.players.append(player)
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
        """Update the score."""
        if choice == 1:
            match.player_1.score += 1
        elif choice == 2:
            match.player_2.score += 1
        elif choice:
            match.player_1.score += 0.5
            match.player_2.score += 0.5

    def next_rounds(self):
        """Initialize the next rounds."""
        for match in self.tournament.matches:
            if self.tournament.matches.winner_alias:
                pass
            else:
                self.view = ChooseMatchView(observer=self)

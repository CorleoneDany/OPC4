"""Reprents the controller."""

from model import Player, Tournament
from view import (
    MainMenu,
    CreateTournamentView,
    RetrieveTournamentView,
    CreatePlayerView,
    CreateMatchView,
    ChooseMatchView,
    ModifyMatchView,
    PlayerMenuView,
    SelectPlayerView,
    EndTournamentView,
)


class Controller:
    """Represents the controller."""

    def __init__(self):
        """Init class with attributes."""
        self.view = MainMenu(observer=self, tournaments=Tournament.list())
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
            self.view.display_player_menu()
        elif name == "retrieve_tournament":
            self.view = RetrieveTournamentView(observer=self)
            self.view.display(Tournament.list())
            self.tournament = Tournament.get(self.context["chosen_tournament"])
            if self.tournament.turn_finished():
                if self.tournament.is_finished():
                    self.execute({"name": "end_tournament"})
                else:
                    self.execute({"name": "create_matchs"})
            else:
                self.execute({"name": "choose_match"})
        elif name == "player_menu":
            self.view = PlayerMenuView(observer=self, players=self.tournament.players)
        elif name == "select_player":
            self.view = SelectPlayerView(
                observer=self,
                players=Player.list(),
                tournament_players=self.tournament.players,
            )
        elif name == "add_player":
            self.tournament.players.append(Player.get(self.context["chosen_player"]))
        elif name == "ask_player_creation":
            self.view = CreatePlayerView(observer=self)
            self.view.display()
            player = Player(**self.context["player_to_create"])
            player.save()
            self.tournament.players.append(player)
        elif name == "create_matchs":
            self.tournament.create_turn()
            self.tournament.save()
            self.view = CreateMatchView(observer=self, matches=self.tournament.matchs)
        elif name == "choose_match":
            self.view = ChooseMatchView(observer=self, matches=self.tournament.matchs)
        elif name == "modify_match":
            self.view = ModifyMatchView(
                observer=self,
                match=self.tournament.get_match(self.context["chosen_match"]),
            )
            self.view.display()
            self.view.match.finish(self.context["chosen_winner"])
            if self.tournament.turn_finished():
                if self.tournament.is_finished():
                    self.execute({"name": "end_tournament"})
                else:
                    self.execute({"name": "create_matchs"})
            else:
                self.view.change_match()
        elif name == "end_tournament":
            self.tournament.save()
            self.view = EndTournamentView(
                observer=self, players=self.tournament.get_players_by_score()
            )
            self.running = False
        elif name == "wrong_command":
            self.view.wrong_command()


# bug lors de s??lection des joueurs si non boucle infinie
# resolu en ajoutant un bool??en qui casse la boucle si le choix est en non puis renvoie
# au menu des joueurs

# boucle infinie lors de fin du tournoi
# le programme se ferme d??sormais a la fin du tournoi, avant le display tournait
# en boucle

# si winner de player ??tait une chaine vide le programme crash
# d??sormais pour mettre un match nul je demande un int ?? 0

# amelioration
# les joueurs d??j?? s??lectionn??s dans le tournoi ne sont plus affich??s sur l'??cran
# de chargement

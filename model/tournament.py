"""Represents the tournament"""

import datetime
from .match import Match
from tinydb import TinyDB, Query


class Tournament:
    """Represents the tournament"""

    def __init__(
        self,
        name,
        location,
        start_date: datetime.date,
        ending_date: datetime.date,
        desc,
    ):
        """Init class with attributes."""
        self.id = int
        self.name = name
        self.location = location
        self.turns = 4
        self.players = []
        self.rounds = []
        self.start_date = start_date
        self.ending_date = ending_date
        self.desc = desc

    def save(self):
        # Si l'id est vide sauvegarder l'objet puis lui attribuer un ID
        # Sinon s'il existe déjà juste mettre à jour l'objet sauvegardé en bdd
        pass

    def get(self):
        pass

    def create_first_rounds(self):
        sorted_players = sorted(self.players, key=lambda i: i["ranking"])
        high_ranks = sorted_players(range(0, 3))
        low_ranks = sorted_players(range(4, 7))

        for id, (high_ranks, low_ranks) in enumerate(zip(high_ranks, low_ranks)):
            self.rounds.append(Match(high_ranks, low_ranks))

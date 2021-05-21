"""Represents the tournament"""

import datetime

from tinydb import TinyDB, Query

from .bdd import DB
from .match import Match
from src import config


class Tournament(DB):
    """Represents the tournament"""

    table = TinyDB(config.DB_PATH).table("tournament")

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

    def serialized(self):
        return {
            "name": self.name,
            "location": self.location,
            "turns": self.turns,
            "players": self.players,
            "rounds": self.rounds,
            "start_date": self.start_date,
            "ending_date": self.ending_date,
            "desc": self.desc,
        }

    @classmethod
    def deserialized(self, document):
        tournament = Tournament(**document)
        tournament.doc_id = document.doc_id
        return tournament

    def create_first_rounds(self):
        sorted_players = sorted(self.players, key=lambda i: i["ranking"])
        high_ranks = sorted_players(range(0, 3))
        low_ranks = sorted_players(range(4, 7))

        for id, (high_ranks, low_ranks) in enumerate(zip(high_ranks, low_ranks)):
            self.rounds.append(Match(high_ranks, low_ranks))

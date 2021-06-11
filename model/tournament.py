"""Represents the tournament"""

import datetime

from tinydb import TinyDB, Query

from .bdd import DB
from .match import Match
from .player import Player
import config


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
        self.max_turns = 4
        self.turns = []
        self.players = []
        self.matchs = []
        self.start_date = start_date
        self.ending_date = ending_date
        self.desc = desc
        self.first_team = []
        self.second_team = []

    def serialized(self):
        return {
            "name": self.name,
            "location": self.location,
            "turns": self.turns,
            "players": self.players,
            "matchs": self.matchs,
            "start_date": self.start_date,
            "ending_date": self.ending_date,
            "desc": self.desc,
            "first_team": self.first_team,
            "second_team": self.second_team,
        }

    @property
    def current_turn(self):
        return self.turn[-1] if self.turns else None

    @classmethod
    def deserialized(cls, document):
        tournament = Tournament(**document)
        tournament.doc_id = document.doc_id
        return tournament

    def create_first_turn(self):
        sorted_players = sorted(self.players, key=lambda i: i["ranking"])
        self.first_team = sorted_players(range(0, 3))
        self.second_team = sorted_players(range(4, 7))

        for id, (self.first_team, second_team) in enumerate(
            zip(self.first_team, self.second_team)
        ):
            self.matchs.append(Match(self.first_team, second_team))

    def create_next_turn(self):
        # ajouter les matchs dans les turns avant de les effacer
        self.matchs.clear()
        sorted_first_team = sorted(self.first_team, key=lambda i: i["score"])
        sorted_second_team = sorted(self.second_team, key=lambda i: i["score"])

        for id, (sorted_first_team, sorted_second_team) in enumerate(
            zip(sorted_first_team, sorted_second_team)
        ):
            self.matchs.append(Match(sorted_first_team, sorted_second_team))

    def create_turn(self):
        if not self.turns:
            self.create_first_turn()
        else:
            self.create_next_turn()

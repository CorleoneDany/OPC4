"""Represents the matchs / rounds"""

from tinydb import TinyDB, Query


from .bdd import DB
from .player import Player
import config


class Match(DB):
    """Represent the matchs / rounds"""

    table = TinyDB(config.DB_PATH).table("match")

    def __init__(self, player_1, player_2):
        """Init class with attributes."""
        self.doc_id = None
        self.player_1 = player_1
        self.player_2 = player_2
        self.winner_alias = None

    @property
    def alias(self):
        """Return the match's alias."""
        return f"{self.player_1.alias} contre {self.player_2.alias}"

    def serialized(self):
        """Return the serialized object."""
        return {
            "player_1": self.player_1,
            "player_2": self.player_2,
            "player_alias": self.alias,
            "winner_alias": self.winner_alias,
        }

    @classmethod
    def deserialized(cls, document):
        """Return the deserialized object."""
        match = Match(**document)
        match.doc_id = document.doc_id
        return match

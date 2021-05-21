"""Represents the player"""

import datetime

from tinydb import TinyDB, Query

from .bdd import DB
from src import config


class Player(DB):
    """Represents the player"""

    table = TinyDB(config.DB_PATH).table("players")

    def __init__(
        self, first_name, last_name, date_of_birth: datetime.date, sex: int, rank
    ):
        """Init class with attributes."""
        self.player_id = int
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.rank = rank
        self.score = int

    @property
    def alias(self):
        return f"{self.first_name[0]}.{self.last_name}"

    def serialized(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "alias": self.alias,
            "date_of_birth": self.date_of_birth,
            "sex": self.sex,
            "rank": self.rank,
            "score": self.score,
        }

    @classmethod
    def deserialized(self, document):
        player = Player(**document)
        player.doc_id = document.doc_id
        return player

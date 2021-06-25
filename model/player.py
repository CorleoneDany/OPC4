"""Represents the player"""

import datetime

from random import randint

from tinydb import TinyDB, Query, table

from faker import Faker

from .bdd import DB
import config


class Player(DB):
    """Represents the player"""

    table = TinyDB(config.DB_PATH).table("players")

    def __init__(
        self,
        first_name,
        last_name,
        date_of_birth: str,
        sex,
        rank,
        score=0,
        doc_id=None,
    ):
        """Init class with attributes."""
        self.doc_id = doc_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.rank = rank
        self.score = score
        self.players_faced = []

    @property
    def alias(self):
        """Return the alias."""
        return f"{self.first_name[0]}.{self.last_name}"

    def serialized(self):
        """Return the serialized object."""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "sex": self.sex,
            "rank": self.rank,
            "score": self.score,
        }

    @classmethod
    def deserialized(cls, document):
        """Return the deserialized object."""
        player = Player(**document)
        player.doc_id = document.doc_id
        return player

    @classmethod
    def create_height_players(self):
        """Create 8 random players in the database."""
        for _ in range(8):
            faker = Faker()
            profile = faker.profile()
            first_name, last_name = profile["name"].split()
            params = {
                "first_name": first_name,
                "last_name": last_name,
                "date_of_birth": profile["birthdate"].strftime("%d/%m/%Y"),
                "sex": profile["sex"],
                "rank": randint(500, 5000),
            }
            player = Player(**params)
            player.save()

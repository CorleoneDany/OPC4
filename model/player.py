"""Represents the player."""

from random import randint

from tinydb import TinyDB

from faker import Faker

from .bdd import DB
import config


class Player(DB):
    """Represents the player."""

    table = TinyDB(config.DB_PATH).table("players")

    def __init__(
        self,
        first_name,
        last_name,
        date_of_birth,
        sex,
        rank=0,
        score=0,
        doc_id=None,
        players_faced=[],
    ):
        """Init class with attributes."""
        self.doc_id = doc_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.rank = int(rank) or 0
        self.score = int(score) or 0
        self.players_faced = players_faced

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
            "players_faced": self.players_faced,
        }

    @classmethod
    def deserialized(cls, document):
        """Return the deserialized object."""
        player = Player(**document)
        player.doc_id = document.doc_id
        return player

    @classmethod
    def get_many_players(cls, players_id):
        """Get many players from a list of ids."""
        players = []
        for player_id in players_id:
            players.append(cls.get(player_id))
        return players

    @classmethod
    def create_height_players(self):
        """Create 8 random players in the database."""
        for _ in range(8):
            faker = Faker()
            profile = faker.profile()
            first_name, last_name = profile["name"].split(None, 1)
            params = {
                "first_name": first_name,
                "last_name": last_name,
                "date_of_birth": profile["birthdate"].strftime("%d/%m/%Y"),
                "sex": profile["sex"],
                "rank": randint(500, 5000),
            }
            player = Player(**params)
            player.save()

    @classmethod
    def return_many_ids(cls, players):
        """Return a list of ids from a players list."""
        ids = []
        for player in players:
            ids.append(player.doc_id)
        return ids

"""Represents the tournament"""

import datetime
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
        self.id = None
        self.name = name
        self.location = location
        self.turns = 4
        self.players = []
        self.start_date = start_date
        self.ending_date = ending_date
        self.desc = desc

    def save():
        # Si l'id est vide sauvegarder l'objet puis lui attribuer un ID
        # Sinon s'il existe déjà juste mettre à jour l'objet sauvegardé en bdd
        pass

    def get(self):
        pass

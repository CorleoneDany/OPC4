"""Represents the player"""

import datetime


class Player:
    """Represents the player"""

    def __init__(
        self, first_name, last_name, date_of_birth: datetime.date, sex: int, rank
    ):
        """Init class with attributes."""
        self.player_id = int
        self.first_name = first_name
        self.last_name = last_name
        self.alias = f"{self.first_name[0]}.{self.last_name}"
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.rank = rank
        self.score = int

    def save(self):
        pass

    def get(self):
        pass

    def all(self):
        pass
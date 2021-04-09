"""Represents the database"""

from tinydb import TinyDB, Query


class DB:
    """Represents the tournament"""

    def __init__(self):
        """Init class with attributes."""
        self.db = TinyDB("DB.json")
